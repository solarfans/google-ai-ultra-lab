#!/usr/bin/env python3
"""Cinema mastering, subtitle burn-in, and A/B comparison builder for 《楚氏春秋》 Sequel CH001.

Produces:
  1. `exports/ChuShiChunQiu_Sequel_Ch001_LiveAction_1080p_Clean.mp4` (2.35:1 letterbox, no subs)
  2. `exports/ChuShiChunQiu_Sequel_Ch001_LiveAction_1080p_Subtitled.mp4` (subs inside bottom black bar)
  3. `exports/ChuShiChunQiu_Legacy_Colab_Ep03_Baseline.mp4` (existing Colab Ep03 6-shot concat)
  4. `exports/ChuShiChunQiu_Flow_LiveAction_vs_Colab_Manju_Compare.mp4` (20s 1920x1080 split-screen A/B)
"""

from __future__ import annotations

import json
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_DRAMA_DIR = BASE_DIR / "pipelines" / "short_drama"
WORK_DIR = SHORT_DRAMA_DIR / "sequel_ch001_live_action"
RENDERS_DIR = WORK_DIR / "renders"
AUDIO_DIR = WORK_DIR / "audio"
EXPORTS_DIR = WORK_DIR / "exports"
METRICS_PATH = WORK_DIR / "metrics.json"
LEGACY_DIR = SHORT_DRAMA_DIR / "assets_manju_v2"
PRIMARY_BGM = BASE_DIR / "assets" / "music_library" / "chushi_chunqiu" / "ccq_01_nocturnal_intrigue.wav"
FALLBACK_BGM = BASE_DIR / "assets" / "music_library" / "how_markets_break" / "hmb_04_aftermath_resolve.wav"

FONT_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]

# Exact dialogue lines paired with observed SRT/silencedetect offsets inside each 10s shot
SHOT_SUBTITLES: dict[str, list[tuple[float, float, str]]] = {
    "Shot01": [
        (1.20, 4.10, "小五，你连酒楼掌柜的生意也管？"),
        (5.40, 9.60, "父亲叫我少惹是非，如今只好拿灯笼练练手。"),
    ],
    "Shot02": [
        (1.10, 4.50, "回京路上，南线鹰堂的人，就不必再跟着小仙了。"),
        (5.30, 9.75, "轻如在鹰堂里有规矩，叫他们明日走人，回京我难免挨数落。"),
    ],
    "Shot03": [
        (1.20, 4.80, "若遇上山匪，夫君的人马自然会护着我。"),
        (5.50, 9.25, "若遇上的不是山匪，多几名高手又有何用？"),
    ],
    "Shot04": [
        (1.90, 5.70, "小仙今日劳累，外头的事，有劳五弟处置。"),
        (7.10, 9.70, "总不能让嫂嫂一路听着刀剑响。"),
    ],
    "Shot05": [
        (0.80, 6.45, "知府急报！汝西县城外发现一具男尸，疑是遭匪人劫杀！"),
        (6.90, 9.45, "倒是巧了……这便有了人命。"),
    ],
    "Shot06": [
        (2.10, 4.45, "大哥，小弟今日竟叫你操心了。"),
        (4.80, 7.10, "自家兄弟，何须客气。"),
    ],
}


def load_cjk_font(size: int) -> ImageFont.FreeTypeFont:
    for fp in FONT_CANDIDATES:
        if Path(fp).exists():
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nk=1:nw=1", str(path)],
        text=True,
    ).strip()
    return float(out)


def render_subtitle_png(text: str, out_png: Path, width: int = 1920, height: int = 1080) -> None:
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = load_cjk_font(38)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (width - tw) // 2
    # Center vertically inside the bottom 132px letterbox bar (y: 948..1080)
    y = 948 + (132 - th) // 2 - 4
    draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, 210))
    draw.text((x, y), text, font=font, fill=(246, 243, 234, 255))
    img.save(out_png)


def render_compare_overlay_png(out_png: Path) -> None:
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Center vertical divider
    draw.rectangle([958, 0, 962, 1080], fill=(220, 185, 110, 190))

    title_font = load_cjk_font(30)
    sub_font = load_cjk_font(26)

    # Left badge
    draw.rounded_rectangle([36, 32, 740, 96], radius=12, fill=(20, 24, 34, 225), outline=(140, 150, 170, 180), width=2)
    draw.text((58, 48), "Colab G4 · MiniMax-H3 int8（旧版开源3D漫剧）", font=title_font, fill=(225, 230, 240, 255))

    # Right badge
    draw.rounded_rectangle([996, 32, 1830, 96], radius=12, fill=(38, 22, 14, 225), outline=(235, 185, 95, 220), width=2)
    draw.text((1018, 48), "Google Flow · Nano2.1 + Omni 1.2 Flash（新版真人电影）", font=title_font, fill=(255, 232, 180, 255))

    # Bottom footer strip
    draw.rectangle([0, 976, 1920, 1080], fill=(10, 12, 16, 225))
    footer = "同源《楚氏春秋》实测对比｜左：旧版 Colab 开源模型 3D 漫剧  vs  右：新版 Google Flow 真人古装实拍（0 CU / $0 GCP）"
    bbox = draw.textbbox((0, 0), footer, font=sub_font)
    fx = (1920 - (bbox[2] - bbox[0])) // 2
    draw.text((fx, 1012), footer, font=sub_font, fill=(242, 238, 228, 255))
    img.save(out_png)


def run_cmd(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed (rc={proc.returncode}): {' '.join(cmd)}\n{proc.stderr[-1500:]}")


def main() -> int:
    t0 = time.monotonic()
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    shot_ids = ["Shot01", "Shot02", "Shot03", "Shot04", "Shot05", "Shot06"]
    shot_paths = [RENDERS_DIR / f"{sid.lower()}_raw.mp4" for sid in shot_ids]
    for p in shot_paths:
        if not p.exists():
            raise FileNotFoundError(f"Missing Flow render: {p}")
    bgm_path = PRIMARY_BGM if PRIMARY_BGM.exists() else FALLBACK_BGM
    if not bgm_path.exists():
        raise FileNotFoundError(f"Missing BGM track: {bgm_path}")

    durations = [probe_duration(p) for p in shot_paths]
    total_dur = sum(durations)
    print(f"[INFO] 6 Flow clips total duration: {total_dur:.3f}s ({durations}); BGM={bgm_path.name}")

    # 1. Build Clean 1080p 2.35:1 Widescreen Master with normalized native audio + subtle -22 dB BGM bed
    clean_mp4 = EXPORTS_DIR / "ChuShiChunQiu_Sequel_Ch001_LiveAction_1080p_Clean.mp4"
    inputs: list[str] = []
    for p in shot_paths:
        inputs.extend(["-i", str(p)])
    inputs.extend(["-stream_loop", "-1", "-i", str(bgm_path)])

    filter_parts: list[str] = []
    concat_refs: list[str] = []
    for idx, dur in enumerate(durations):
        fade_out_start = max(0.0, dur - 0.08)
        filter_parts.append(
            f"[{idx}:v]scale=1920:1080:flags=lanczos,fps=24,format=yuv420p,"
            f"eq=contrast=1.04:saturation=1.03,"
            f"drawbox=x=0:y=0:w=1920:h=132:color=black:t=fill,"
            f"drawbox=x=0:y=948:w=1920:h=132:color=black:t=fill[v{idx}]"
        )
        filter_parts.append(
            f"[{idx}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
            f"loudnorm=I=-15:TP=-1.5:LRA=11,"
            f"afade=t=in:st=0:d=0.04,afade=t=out:st={fade_out_start:.3f}:d=0.08[a{idx}]"
        )
        concat_refs.append(f"[v{idx}][a{idx}]")

    filter_parts.append(f"{''.join(concat_refs)}concat=n=6:v=1:a=1[vconcat][adialog]")
    bgm_idx = len(shot_paths)
    bgm_fade_out = max(0.0, total_dur - 2.0)
    filter_parts.append(
        f"[{bgm_idx}:a]atrim=0:{total_dur:.3f},asetpts=PTS-STARTPTS,"
        f"aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"volume=-22dB,afade=t=in:st=0:d=1.2,afade=t=out:st={bgm_fade_out:.3f}:d=2.0[abgm]"
    )
    filter_parts.append("[adialog][abgm]amix=inputs=2:duration=first:normalize=0[aout]")

    run_cmd([
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", ";".join(filter_parts),
        "-map", "[vconcat]",
        "-map", "[aout]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
        str(clean_mp4),
    ])
    print(f"[OK] Built Clean master: {clean_mp4} ({clean_mp4.stat().st_size} bytes)")

    # 2. Burn crisp Chinese subtitles inside the bottom 132px black letterbox bar
    sub_mp4 = EXPORTS_DIR / "ChuShiChunQiu_Sequel_Ch001_LiveAction_1080p_Subtitled.mp4"
    with tempfile.TemporaryDirectory(prefix="ccq_subs_") as tmp_dir_str:
        tmp_dir = Path(tmp_dir_str)
        sub_events: list[tuple[float, float, Path]] = []
        offset = 0.0
        for idx, sid in enumerate(shot_ids):
            for local_start, local_end, text in SHOT_SUBTITLES[sid]:
                png_path = tmp_dir / f"sub_{len(sub_events):02d}.png"
                render_subtitle_png(text, png_path)
                sub_events.append((offset + local_start, offset + local_end, png_path))
            offset += durations[idx]

        sub_inputs = ["-i", str(clean_mp4)]
        for _, _, png_path in sub_events:
            sub_inputs.extend(["-i", str(png_path)])

        ov_parts: list[str] = []
        prev_label = "0:v"
        for i, (st, et, _) in enumerate(sub_events, start=1):
            next_label = f"ov{i}"
            ov_parts.append(f"[{prev_label}][{i}:v]overlay=0:0:enable='between(t,{st:.3f},{et:.3f})'[{next_label}]")
            prev_label = next_label

        run_cmd([
            "ffmpeg", "-y",
            *sub_inputs,
            "-filter_complex", ";".join(ov_parts),
            "-map", f"[{prev_label}]",
            "-map", "0:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "copy", "-movflags", "+faststart",
            str(sub_mp4),
        ])
    print(f"[OK] Built Subtitled master: {sub_mp4} ({sub_mp4.stat().st_size} bytes)")

    # 3. Concatenate existing Colab G4 Ep03 subtitled baseline
    colab_mp4 = EXPORTS_DIR / "ChuShiChunQiu_Legacy_Colab_Ep03_Baseline.mp4"
    colab_clips = [LEGACY_DIR / f"ChuShiChunQiu_Ep03_Shot0{i}_Subtitled.mp4" for i in range(1, 7)]
    for cp in colab_clips:
        if not cp.exists():
            raise FileNotFoundError(f"Missing legacy Colab clip: {cp}")
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as tf:
        for cp in colab_clips:
            tf.write(f"file '{cp}'\n")
        concat_txt = Path(tf.name)
    try:
        run_cmd([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
            "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            str(colab_mp4),
        ])
    finally:
        concat_txt.unlink(missing_ok=True)
    print(f"[OK] Built Legacy Colab baseline: {colab_mp4} ({colab_mp4.stat().st_size} bytes)")

    # 4. Build 20s 1920x1080 Split-Screen A/B Comparison Video
    compare_mp4 = EXPORTS_DIR / "ChuShiChunQiu_Flow_LiveAction_vs_Colab_Manju_Compare.mp4"
    with tempfile.TemporaryDirectory(prefix="ccq_cmp_") as tmp_dir_str:
        overlay_png = Path(tmp_dir_str) / "compare_overlay.png"
        render_compare_overlay_png(overlay_png)

        c_shot01 = LEGACY_DIR / "ChuShiChunQiu_Ep03_Shot01_Subtitled.mp4"
        c_shot05 = LEGACY_DIR / "ChuShiChunQiu_Ep03_Shot05_Subtitled.mp4"
        f_shot01 = RENDERS_DIR / "shot01_raw.mp4"
        f_shot06 = RENDERS_DIR / "shot06_raw.mp4"

        fc = ";".join([
            "[0:v]trim=0:10,setpts=PTS-STARTPTS,scale=960:548:flags=lanczos,pad=960:1080:0:266:color=#0C0E12,fps=24[l1]",
            "[1:v]trim=0:10,setpts=PTS-STARTPTS,scale=960:540:flags=lanczos,pad=960:1080:0:270:color=#0C0E12,fps=24[r1]",
            "[l1][r1]hstack=inputs=2[pair1]",
            "[2:v]trim=0:10,setpts=PTS-STARTPTS,scale=960:548:flags=lanczos,pad=960:1080:0:266:color=#0C0E12,fps=24[l2]",
            "[3:v]trim=0:10,setpts=PTS-STARTPTS,scale=960:540:flags=lanczos,pad=960:1080:0:270:color=#0C0E12,fps=24[r2]",
            "[l2][r2]hstack=inputs=2[pair2]",
            "[1:a]atrim=0:10,asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,loudnorm=I=-15:TP=-1.5:LRA=11[a1]",
            "[3:a]atrim=0:10,asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,loudnorm=I=-15:TP=-1.5:LRA=11[a2]",
            "[pair1][a1][pair2][a2]concat=n=2:v=1:a=1[vbase][aout]",
            "[vbase][4:v]overlay=0:0,format=yuv420p[vfinal]",
        ])
        run_cmd([
            "ffmpeg", "-y",
            "-i", str(c_shot01),
            "-i", str(f_shot01),
            "-i", str(c_shot05),
            "-i", str(f_shot06),
            "-i", str(overlay_png),
            "-filter_complex", fc,
            "-map", "[vfinal]",
            "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            str(compare_mp4),
        ])
    print(f"[OK] Built Split-Screen Compare: {compare_mp4} ({compare_mp4.stat().st_size} bytes)")

    # Record assembly telemetry into metrics.json
    if METRICS_PATH.exists():
        m: dict[str, Any] = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    else:
        m = {}
    m["assembly"] = {
        "elapsed_sec": round(time.monotonic() - t0, 2),
        "bgm_source": str(bgm_path),
        "flowmusic_resolution": {
            "song_url": "https://www.flowmusic.app/song/292f4645-347d-4290-b6d5-d9537a369210",
            "gcs_wav_url": "https://storage.googleapis.com/producer-app-public/clips/292f4645-347d-4290-b6d5-d9537a369210.wav",
            "status": "downloaded_via_gcs_public_wav_endpoint",
            "detail": "UI blob download returns dl.path()==null in AGY webview sandbox; fetched lossless WAV directly via https://storage.googleapis.com/producer-app-public/clips/<song_uuid>.wav and normalized to 48kHz stereo pcm_s16le.",
        },
        "exports": {
            "clean_1080p": {"path": str(clean_mp4), "size_bytes": clean_mp4.stat().st_size, "duration_sec": round(probe_duration(clean_mp4), 3)},
            "subtitled_1080p": {"path": str(sub_mp4), "size_bytes": sub_mp4.stat().st_size, "duration_sec": round(probe_duration(sub_mp4), 3)},
            "colab_baseline": {"path": str(colab_mp4), "size_bytes": colab_mp4.stat().st_size, "duration_sec": round(probe_duration(colab_mp4), 3)},
            "split_compare": {"path": str(compare_mp4), "size_bytes": compare_mp4.stat().st_size, "duration_sec": round(probe_duration(compare_mp4), 3)},
        },
    }
    METRICS_PATH.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
