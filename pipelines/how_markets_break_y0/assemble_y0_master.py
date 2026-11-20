#!/usr/bin/env python3
"""
Assemble How Markets Break — Y0 Pilot Broadcast Masters:
  1. HowMarketsBreak_Y0_The_Liquidity_Trap_16x9_1080p_Clean.mp4
  2. HowMarketsBreak_Y0_The_Liquidity_Trap_16x9_1080p_Subtitled.mp4
  3. HowMarketsBreak_Y0_The_Liquidity_Trap_9x16_Shorts.mp4
Mirrors all 3 outputs to ~/Downloads/2026-11-20_HowMarketsBreak_Y0_Master/.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
RENDERS_DIR = ROOT / "renders"
MOTION_DIR = ROOT / "motion_assets"
AUDIO_DIR = ROOT / "audio"
TIMELINE_PATH = AUDIO_DIR / "voiceover_timeline.json"
OUT_DIR = ROOT / "output"
DOWNLOADS_DIR = Path.home() / "Downloads" / "2026-11-20_HowMarketsBreak_Y0_Master"

FONT_PATHS = [
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/SFNS.ttf",
    "/Library/Fonts/Arial.ttf",
]


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    for fp in FONT_PATHS:
        if Path(fp).is_file():
            try:
                # HelveticaNeue.ttc index 1 is Bold; 0 is Regular
                idx = 1 if (bold and fp.endswith("HelveticaNeue.ttc")) else 0
                return ImageFont.truetype(fp, size=size, index=idx)
            except Exception:
                try:
                    return ImageFont.truetype(fp, size=size)
                except Exception:
                    continue
    return ImageFont.load_default()


def ffprobe_info(path: Path) -> dict[str, Any]:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,width,height",
            "-of",
            "json",
            str(path),
        ],
        text=True,
    )
    data = json.loads(out)
    dur = float(data["format"]["duration"])
    streams = data.get("streams", [])
    has_audio = any(s.get("codec_type") == "audio" for s in streams)
    v_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
    return {
        "duration": dur,
        "has_audio": has_audio,
        "width": int(v_stream.get("width", 0)),
        "height": int(v_stream.get("height", 0)),
    }


def run_ffmpeg(args: list[str]) -> None:
    res = subprocess.run(["ffmpeg", "-y", "-v", "error", *args], capture_output=True, text=True, check=False)
    if res.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{' '.join(args)}\n{res.stderr}")


def normalize_cues(raw_cues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge awkward 'U.S.' splits and mid-sentence orphan words while never chaining across sentence boundaries."""
    merged: list[dict[str, Any]] = []
    for cue in raw_cues:
        txt = str(cue["text"]).strip()
        if not merged:
            merged.append({"start": float(cue["start"]), "end": float(cue["end"]), "text": txt})
            continue
        prev = merged[-1]["text"]
        combined_len = len(prev) + 1 + len(txt)
        is_us_abbr = prev == "U.S." or prev.endswith(" U.S.")
        sentence_ended = prev.endswith((".", "?", "!")) and not is_us_abbr
        should_merge = is_us_abbr or (
            not sentence_ended
            and combined_len <= 72
            and (len(txt) < 14 or combined_len <= 52)
        )
        if should_merge:
            merged[-1]["text"] = f"{prev} {txt}"
            merged[-1]["end"] = float(cue["end"])
        else:
            merged.append({"start": float(cue["start"]), "end": float(cue["end"]), "text": txt})
    return merged


def wrap_lines(text: str, max_line: int = 44) -> list[str]:
    if len(text) <= max_line:
        return [text]
    words = text.split(" ")
    if len(words) <= 1:
        return [text]
    # Try balanced 2-line split first when text fits <= 2 * max_line + 10
    if len(text) <= max_line * 2 + 10:
        best_split = len(words) // 2
        best_diff = 999
        for k in range(1, len(words)):
            l1 = " ".join(words[:k])
            l2 = " ".join(words[k:])
            if max(len(l1), len(l2)) <= max_line + 8:
                diff = abs(len(l1) - len(l2))
                if diff < best_diff:
                    best_diff = diff
                    best_split = k
        return [" ".join(words[:best_split]), " ".join(words[best_split:])]
    lines: list[str] = []
    cur = words[0]
    for w_tok in words[1:]:
        if len(cur) + 1 + len(w_tok) <= max_line:
            cur = f"{cur} {w_tok}"
        else:
            lines.append(cur)
            cur = w_tok
    lines.append(cur)
    return lines


def make_subtitle_png(text: str, out_png: Path, w: int, h: int, bottom_margin: int, font_size: int) -> None:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad_x, pad_y, line_gap = 28, 16, 10
    max_box_w = w - 96

    cur_size = font_size
    lines = wrap_lines(text, max_line=44 if w == 1920 else 28)
    while True:
        font = load_font(cur_size, bold=True)
        line_boxes = [draw.textbbox((0, 0), ln, font=font) for ln in lines]
        line_widths = [b[2] - b[0] for b in line_boxes]
        box_w = max(line_widths) + pad_x * 2
        if box_w <= max_box_w or cur_size <= 26:
            break
        cur_size -= 2

    line_heights = [b[3] - b[1] for b in line_boxes]
    box_h = sum(line_heights) + line_gap * (len(lines) - 1) + pad_y * 2

    bx0 = (w - box_w) // 2
    by0 = h - bottom_margin - box_h
    draw.rounded_rectangle(
        [bx0, by0, bx0 + box_w, by0 + box_h],
        radius=10,
        fill=(11, 14, 20, 215),
        outline=(56, 72, 98, 170),
        width=2,
    )
    cy = by0 + pad_y
    for ln, lw, lh, bbox in zip(lines, line_widths, line_heights, line_boxes):
        tx = (w - lw) // 2 - bbox[0]
        ty = cy - bbox[1]
        draw.text((tx, ty), ln, font=font, fill=(248, 250, 252, 255))
        cy += lh + line_gap

    img.save(out_png)


def make_vertical_header_png(out_png: Path, title: str, kicker: str) -> None:
    """Create a 1080x1920 transparent top editorial header overlay for 9:16 chart sections."""
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    f_kicker = load_font(28, bold=True)
    f_title = load_font(54, bold=True)
    draw.text((72, 230), kicker, font=f_kicker, fill=(229, 169, 59, 255))
    lines = wrap_lines(title, max_line=26)
    y = 284
    for ln in lines:
        draw.text((72, y), ln, font=f_title, fill=(248, 250, 252, 255))
        y += 66
    img.save(out_png)


def prepare_flow_clip(
    src_mp4: Path,
    dst_mp4: Path,
    target_dur: float,
    foley_wav: Path,
    trim_head: float = 0.25,
    mode: str = "16x9",
) -> float:
    """Normalize a Flow clip to exact target_dur at 30fps and extract subtle Foley audio."""
    info = ffprobe_info(src_mp4)
    raw_dur = info["duration"]
    start_ss = trim_head if raw_dur - trim_head >= target_dur * 0.85 else 0.0
    avail = max(0.5, raw_dur - start_ss)

    scale_crop = (
        "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1"
        if mode == "16x9"
        else "scale=-1:1920:force_original_aspect_ratio=increase,crop=1080:1920:(iw-1080)/2:0,setsar=1"
    )
    grade = "eq=contrast=1.06:brightness=-0.02:gamma=0.94:saturation=1.02"
    pad_s = max(0.0, target_dur - avail)
    vf = f"{scale_crop},{grade},fps=30"
    if pad_s > 0.02:
        vf += f",tpad=stop_mode=clone:stop_duration={pad_s:.3f}"
    vf += f",trim=duration={target_dur:.3f},setpts=PTS-STARTPTS,format=yuv420p"

    run_ffmpeg([
        "-ss", f"{start_ss:.3f}",
        "-i", str(src_mp4),
        "-an",
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        str(dst_mp4),
    ])

    if info["has_audio"]:
        af = f"aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={target_dur:.3f},atrim=duration={target_dur:.3f},afade=t=in:st=0:d=0.15,afade=t=out:st={max(0.0, target_dur-0.2):.3f}:d=0.2"
        run_ffmpeg([
            "-ss", f"{start_ss:.3f}",
            "-i", str(src_mp4),
            "-vn",
            "-af", af,
            "-c:a", "pcm_s16le",
            str(foley_wav),
        ])
    else:
        run_ffmpeg([
            "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={target_dur:.3f}",
            "-c:a", "pcm_s16le",
            str(foley_wav),
        ])
    return target_dur


def adjust_motion_clip(
    src_mp4: Path,
    dst_mp4: Path,
    target_dur: float,
    mode: str = "16x9",
    header_png: Path | None = None,
) -> None:
    """Adjust motion card duration cleanly and frame for 16x9 or 9x16 vertical canvas."""
    info = ffprobe_info(src_mp4)
    pad_s = max(0.0, target_dur - info["duration"])
    if mode == "16x9":
        vf = "fps=30"
        if pad_s > 0.02:
            vf += f",tpad=stop_mode=clone:stop_duration={pad_s:.3f}"
        vf += f",trim=duration={target_dur:.3f},setpts=PTS-STARTPTS,format=yuv420p"
        run_ffmpeg(["-i", str(src_mp4), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "fast", "-crf", "18", str(dst_mp4)])
    else:
        # 1080x1920 vertical canvas: place crisp 1080x608 16:9 chart at y=656 on #0B0E14 + optional top header
        vf_base = f"scale=1080:608:flags=lanczos,fps=30"
        if pad_s > 0.02:
            vf_base += f",tpad=stop_mode=clone:stop_duration={pad_s:.3f}"
        vf_base += f",trim=duration={target_dur:.3f},setpts=PTS-STARTPTS,pad=1080:1920:0:656:color=0x0B0E14"
        if header_png is not None:
            run_ffmpeg([
                "-i", str(src_mp4),
                "-loop", "1", "-framerate", "30", "-t", f"{target_dur:.3f}", "-i", str(header_png),
                "-an",
                "-filter_complex", f"[0:v]{vf_base}[bg];[bg][1:v]overlay=0:0:shortest=1,format=yuv420p",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                str(dst_mp4),
            ])
        else:
            run_ffmpeg(["-i", str(src_mp4), "-an", "-vf", f"{vf_base},format=yuv420p", "-c:v", "libx264", "-preset", "fast", "-crf", "18", str(dst_mp4)])


def build_ambient_dsp_score(out_wav: Path, duration: float) -> None:
    """Fallback restrained D-minor dark ambient underscore if neither Flow Music nor Lyria-002 ran."""
    af = (
        f"aevalsrc="
        f"0.16*sin(2*PI*73.42*t)*(0.6+0.4*sin(2*PI*0.18*t))"
        f"+0.10*sin(2*PI*110.00*t)*(0.5+0.5*sin(2*PI*0.11*t+1.2))"
        f"+0.06*sin(2*PI*146.83*t)*(0.5+0.5*sin(2*PI*0.23*t+0.4))"
        f"+0.04*sin(2*PI*174.61*t)*(0.5+0.5*sin(2*PI*0.09*t+2.1))"
        f":s=48000:d={duration:.3f},"
        f"lowpass=f=650,aformat=channel_layouts=stereo,"
        f"afade=t=in:st=0:d=1.2,afade=t=out:st={max(0.0, duration-2.2):.3f}:d=2.2"
    )
    run_ffmpeg(["-f", "lavfi", "-i", af, "-c:a", "pcm_s16le", str(out_wav)])


def build_master_tracks(mode: str, work_dir: Path, score_wav: Path) -> Path:
    tl = json.loads(TIMELINE_PATH.read_text(encoding="utf-8"))
    pause = float(tl.get("pause_between_beats_sec", 0.45))
    beats_by_id = {b["beat_id"]: b for b in tl["beats"]}

    # Check all 5 Flow renders exist
    flow_paths = {i: RENDERS_DIR / f"shot0{i}_flow.mp4" for i in range(1, 6)}
    for i, p in flow_paths.items():
        if not p.is_file():
            raise FileNotFoundError(f"Missing Flow render: {p}")

    # Header PNGs for 9:16 chart framing
    h_trap = work_dir / "hdr_trap.png"
    h_c01 = work_dir / "hdr_c01.png"
    h_c02 = work_dir / "hdr_c02.png"
    h_cas = work_dir / "hdr_cas.png"
    h_lvb = work_dir / "hdr_lvb.png"
    if mode == "9x16":
        make_vertical_header_png(h_trap, "Why Everything Crashed Together", "HOW MARKETS BREAK · LIQUIDITY TRAP")
        make_vertical_header_png(h_c01, "Even Gold Fell Nearly 2x Harder Than Tech", "NOV 4–20, 2026 · CROSS-ASSET DRAWDOWN")
        make_vertical_header_png(h_c02, "3 Signals Behind the Crash", "MACRO PRESSURE GAUGES")
        make_vertical_header_png(h_cas, "Why Funds Sell Winning Assets First", "MARGIN CALL CASCADE")
        make_vertical_header_png(h_lvb, "Liquidity Flush vs True Bear Market", "MARKET DIAGNOSTIC")

    seg_specs = []
    # Beat 1: Shot 01 (up to 6.0s) + Hook Card
    b1_total = float(beats_by_id["beat01"]["duration_sec"]) + pause
    s1_info = ffprobe_info(flow_paths[1])
    s1a_dur = min(6.0, max(4.0, s1_info["duration"] - 0.25))
    s1b_dur = max(3.5, b1_total - s1a_dur)
    seg_specs.append(("flow", flow_paths[1], s1a_dur, "seg01a"))
    seg_specs.append(("motion", MOTION_DIR / "beat01b_hook_card.mp4", s1b_dur, "seg01b", h_trap if mode == "9x16" else None))

    # Beat 2: Animated Chart 01
    b2_total = float(beats_by_id["beat02"]["duration_sec"]) + pause
    seg_specs.append(("motion", MOTION_DIR / "beat02_chart01.mp4", b2_total, "seg02", h_c01 if mode == "9x16" else None))

    # Beat 3: Shot 02 (Gold Vault)
    b3_total = float(beats_by_id["beat03"]["duration_sec"]) + pause
    seg_specs.append(("flow", flow_paths[2], b3_total, "seg03"))

    # Beat 4: Animated Chart 02
    b4_total = float(beats_by_id["beat04"]["duration_sec"]) + pause
    seg_specs.append(("motion", MOTION_DIR / "beat04_chart02.mp4", b4_total, "seg04", h_c02 if mode == "9x16" else None))

    # Beat 5: Shot 03 (Server Corridor) + Margin Cascade
    b5_total = float(beats_by_id["beat05"]["duration_sec"]) + pause
    s3_info = ffprobe_info(flow_paths[3])
    s5a_dur = min(6.0, max(4.0, s3_info["duration"] - 0.25))
    s5b_dur = max(4.0, b5_total - s5a_dur)
    seg_specs.append(("flow", flow_paths[3], s5a_dur, "seg05a"))
    seg_specs.append(("motion", MOTION_DIR / "beat05b_cascade.mp4", s5b_dur, "seg05b", h_cas if mode == "9x16" else None))

    # Beat 6: Shot 04 (Treasury Fortress) + Liquidity vs Bear
    b6_total = float(beats_by_id["beat06"]["duration_sec"]) + pause
    s4_info = ffprobe_info(flow_paths[4])
    s6a_dur = min(6.0, max(4.0, s4_info["duration"] - 0.25))
    s6b_dur = max(4.0, b6_total - s6a_dur)
    seg_specs.append(("flow", flow_paths[4], s6a_dur, "seg06a"))
    seg_specs.append(("motion", MOTION_DIR / "beat06b_lvb.mp4", s6b_dur, "seg06b", h_lvb if mode == "9x16" else None))

    # Beat 7: Shot 05 (Dawn Horizon) + End Slate
    b7_total = float(beats_by_id["beat07"]["duration_sec"]) + 2.50
    s5_info = ffprobe_info(flow_paths[5])
    s7a_dur = min(6.5, max(4.0, s5_info["duration"] - 0.25))
    s7b_dur = max(4.0, b7_total - s7a_dur)
    seg_specs.append(("flow", flow_paths[5], s7a_dur, "seg07a"))
    seg_specs.append(("motion", MOTION_DIR / "beat07b_end_slate.mp4", s7b_dur, "seg07b", None))

    # Compute exact beat start offsets matching visual blocks
    beat_starts = {
        "beat01": 0.0,
        "beat02": s1a_dur + s1b_dur,
    }
    beat_starts["beat03"] = beat_starts["beat02"] + b2_total
    beat_starts["beat04"] = beat_starts["beat03"] + b3_total
    beat_starts["beat05"] = beat_starts["beat04"] + b4_total
    beat_starts["beat06"] = beat_starts["beat05"] + s5a_dur + s5b_dur
    beat_starts["beat07"] = beat_starts["beat06"] + s6a_dur + s6b_dur
    total_dur = beat_starts["beat07"] + s7a_dur + s7b_dur

    # Render normalized segments
    video_parts: list[Path] = []
    foley_parts: list[tuple[float, Path]] = []
    t_cursor = 0.0
    for spec in seg_specs:
        kind = spec[0]
        src = spec[1]
        dur = spec[2]
        name = spec[3]
        vp = work_dir / f"{mode}_{name}.mp4"
        if kind == "flow":
            fp = work_dir / f"{mode}_{name}_foley.wav"
            prepare_flow_clip(src, vp, dur, fp, mode=mode)
            foley_parts.append((t_cursor, fp))
        else:
            hdr = spec[4]
            adjust_motion_clip(src, vp, dur, mode=mode, header_png=hdr)
        video_parts.append(vp)
        t_cursor += dur

    concat_list = work_dir / f"{mode}_concat.txt"
    concat_list.write_text("\n".join(f"file '{p}'" for p in video_parts), encoding="utf-8")
    raw_video = work_dir / f"{mode}_video_raw.mp4"
    run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(raw_video)])

    # Build narration master WAV at exact beat_starts
    voice_inputs = []
    voice_filters = []
    for i, bid in enumerate([f"beat0{k}" for k in range(1, 8)]):
        wav = Path(beats_by_id[bid]["wav"])
        delay_ms = int(round(beat_starts[bid] * 1000))
        voice_inputs.extend(["-i", str(wav)])
        voice_filters.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={delay_ms}|{delay_ms}[v{i}]")
    v_labels = "".join(f"[v{i}]" for i in range(7))
    voice_filters.append(f"{v_labels}amix=inputs=7:duration=longest:normalize=0,apad=whole_dur={total_dur:.3f},atrim=duration={total_dur:.3f},loudnorm=I=-14:TP=-1.5:LRA=9[vnorm]")
    narration_wav = work_dir / f"{mode}_narration.wav"
    run_ffmpeg([*voice_inputs, "-filter_complex", ";".join(voice_filters), "-map", "[vnorm]", "-c:a", "pcm_s16le", str(narration_wav)])

    # Build Foley composite track
    f_inputs = []
    f_filters = []
    for i, (st, fp) in enumerate(foley_parts):
        dms = int(round(st * 1000))
        f_inputs.extend(["-i", str(fp)])
        f_filters.append(f"[{i}:a]volume=0.11,adelay={dms}|{dms}[f{i}]")
    f_labels = "".join(f"[f{i}]" for i in range(len(foley_parts)))
    f_filters.append(f"{f_labels}amix=inputs={len(foley_parts)}:duration=longest:normalize=0,apad=whole_dur={total_dur:.3f},atrim=duration={total_dur:.3f}[fout]")
    foley_wav = work_dir / f"{mode}_foley.wav"
    run_ffmpeg([*f_inputs, "-filter_complex", ";".join(f_filters), "-map", "[fout]", "-c:a", "pcm_s16le", str(foley_wav)])

    # Loop/trim score_wav cleanly to total_dur + sidechain duck under narration + mix
    score_bed = work_dir / f"{mode}_score.wav"
    run_ffmpeg([
        "-stream_loop", "-1", "-i", str(score_wav),
        "-t", f"{total_dur:.3f}",
        "-af", f"aformat=sample_rates=48000:channel_layouts=stereo,volume=0.22,afade=t=in:st=0:d=1.0,afade=t=out:st={max(0.0, total_dur-2.2):.3f}:d=2.2",
        "-c:a", "pcm_s16le", str(score_bed),
    ])

    mixed_wav = work_dir / f"{mode}_mix.wav"
    mix_fc = (
        "[0:a]asplit=2[vo_main][vo_sc];"
        "[1:a][vo_sc]sidechaincompress=threshold=0.03:ratio=4.5:attack=40:release=320[music_ducked];"
        "[vo_main][music_ducked][2:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.92[mix]"
    )
    run_ffmpeg([
        "-i", str(narration_wav),
        "-i", str(score_bed),
        "-i", str(foley_wav),
        "-filter_complex", mix_fc,
        "-map", "[mix]", "-c:a", "pcm_s16le", str(mixed_wav),
    ])

    if mode == "16x9":
        clean_out = OUT_DIR / "HowMarketsBreak_Y0_The_Liquidity_Trap_16x9_1080p_Clean.mp4"
        run_ffmpeg([
            "-i", str(raw_video), "-i", str(mixed_wav),
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            str(clean_out),
        ])

    # Render timed RGBA subtitle PNGs and overlay
    w, h = (1920, 1080) if mode == "16x9" else (1080, 1920)
    b_margin = 52 if mode == "16x9" else 310
    f_size = 38 if mode == "16x9" else 42
    cue_overlays: list[tuple[float, float, Path]] = []
    sub_idx = 0
    for bid in [f"beat0{k}" for k in range(1, 8)]:
        bstart = beat_starts[bid]
        for cue in normalize_cues(beats_by_id[bid]["cues"]):
            s_abs = round(bstart + float(cue["start"]), 3)
            e_abs = round(bstart + float(cue["end"]), 3)
            if e_abs <= s_abs:
                continue
            spng = work_dir / f"{mode}_sub_{sub_idx:03d}.png"
            make_subtitle_png(cue["text"], spng, w, h, bottom_margin=b_margin, font_size=f_size)
            cue_overlays.append((s_abs, e_abs, spng))
            sub_idx += 1

    # Chain overlay filters with enable='between(t,s,e)'
    ov_inputs = ["-i", str(raw_video), "-i", str(mixed_wav)]
    ov_filters = []
    cur_v = "0:v"
    for idx, (st, en, spng) in enumerate(cue_overlays, start=2):
        ov_inputs.extend(["-i", str(spng)])
        nxt = f"ov{idx}"
        ov_filters.append(f"[{cur_v}][{idx}:v]overlay=0:0:enable='between(t,{st:.3f},{en:.3f})'[{nxt}]")
        cur_v = nxt

    out_name = (
        "HowMarketsBreak_Y0_The_Liquidity_Trap_16x9_1080p_Subtitled.mp4"
        if mode == "16x9"
        else "HowMarketsBreak_Y0_The_Liquidity_Trap_9x16_Shorts.mp4"
    )
    final_out = OUT_DIR / out_name
    ov_filters.append(f"[{cur_v}]format=yuv420p[outv]")
    run_ffmpeg([
        *ov_inputs,
        "-filter_complex", ";".join(ov_filters),
        "-map", "[outv]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
        str(final_out),
    ])
    return final_out


def resolve_score_wav(work_dir: Path) -> Path:
    for cand in [AUDIO_DIR / "flow_music_score.wav", AUDIO_DIR / "lyria_score.wav"]:
        if cand.is_file() and cand.stat().st_size > 50_000:
            return cand
    dsp_wav = work_dir / "dsp_dark_ambient.wav"
    build_ambient_dsp_score(dsp_wav, 95.0)
    return dsp_wav


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="hmb_y0_work_") as tmp:
        work_dir = Path(tmp)
        score_wav = resolve_score_wav(work_dir)
        out_16x9 = build_master_tracks("16x9", work_dir, score_wav)
        out_9x16 = build_master_tracks("9x16", work_dir, score_wav)

    clean_16x9 = OUT_DIR / "HowMarketsBreak_Y0_The_Liquidity_Trap_16x9_1080p_Clean.mp4"
    for p in [clean_16x9, out_16x9, out_9x16]:
        shutil.copy2(p, DOWNLOADS_DIR / p.name)
        info = ffprobe_info(p)
        print(f"DELIVERED: {p} ({p.stat().st_size / 1e6:.2f} MB, {info['duration']:.2f}s, {info['width']}x{info['height']}, audio={info['has_audio']})")


if __name__ == "__main__":
    main()
