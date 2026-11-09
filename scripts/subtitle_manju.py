#!/usr/bin/env python3
"""Zero-CU Local Subtitle Burn-in & Visual-Dialogue Sync Auditor for AI Manju (v2.0).

Supports two output modes:
1. `--mode audit` (Default during pipeline tuning):
   Burns top-left Shot/Timestamp HUD + bottom clean dialogue subtitles (NO `【角色名】` bracket prefix!).
2. `--mode release` (Clean subtitle mode):
   Burns only clean bottom dialogue subtitles without HUD or speaker brackets.
   (Note: Unsubtitled raw master `ChuShiChunQiu_EpXX_<Title>_Master_v2.mp4` is always preserved.)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_DRAMA_DIR = BASE_DIR / "pipelines" / "short_drama"
VAULT_PATH = SHORT_DRAMA_DIR / "character_vault.json"
ASSETS_DIR = SHORT_DRAMA_DIR / "assets_manju_v2"

FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]


def load_cjk_font(size: int) -> ImageFont.FreeTypeFont:
    for fp in FONT_CANDIDATES:
        if Path(fp).exists():
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


def parse_window(win_str: str) -> tuple[float, float]:
    parts = win_str.replace("-", "–").split("–")
    def _to_sec(s: str) -> float:
        s = s.strip()
        if ":" in s:
            m, sec = s.split(":", 1)
            return int(m) * 60.0 + float(sec)
        return float(s)
    return _to_sec(parts[0]), _to_sec(parts[1])


def render_subtitle_overlay_png(
    out_png: Path,
    width: int,
    height: int,
    line_text: str,
    shot_badge: str = "",
) -> None:
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font_sub = load_cjk_font(34)
    font_badge = load_cjk_font(22)

    if shot_badge:
        bbox_b = draw.textbbox((0, 0), shot_badge, font=font_badge)
        bw, bh = bbox_b[2] - bbox_b[0], bbox_b[3] - bbox_b[1]
        draw.rounded_rectangle(
            (24, 20, 24 + bw + 28, 20 + bh + 18),
            radius=8,
            fill=(15, 23, 42, 195),
            outline=(250, 204, 21, 220),
            width=2,
        )
        draw.text((38, 27), shot_badge, font=font_badge, fill=(254, 240, 138, 255))

    if not line_text:
        img.save(out_png)
        return

    # Pure spoken dialogue only — NEVER prepend 【角色名】 speaker brackets!
    full_text = line_text.strip()
    max_chars = 24
    lines = []
    cur = full_text
    while len(cur) > max_chars:
        split_idx = max_chars
        for p in ("，", "！", "？", "。", "…", "、"):
            pos = cur.rfind(p, 0, max_chars + 2)
            if pos > 6:
                split_idx = pos + 1
                break
        lines.append(cur[:split_idx])
        cur = cur[split_idx:]
    if cur:
        lines.append(cur)

    line_h = 46
    total_h = len(lines) * line_h
    base_y = height - 42 - total_h

    max_w = 0
    for ln in lines:
        bb = draw.textbbox((0, 0), ln, font=font_sub)
        max_w = max(max_w, bb[2] - bb[0])

    pad_x, pad_y = 28, 14
    box_x0 = (width - max_w) // 2 - pad_x
    box_x1 = (width + max_w) // 2 + pad_x
    box_y0 = base_y - pad_y
    box_y1 = base_y + total_h + pad_y - 4

    draw.rounded_rectangle(
        (box_x0, box_y0, box_x1, box_y1),
        radius=12,
        fill=(10, 14, 22, 175),
        outline=(255, 255, 255, 60),
        width=1,
    )

    for i, ln in enumerate(lines):
        bb = draw.textbbox((0, 0), ln, font=font_sub)
        lw = bb[2] - bb[0]
        tx = (width - lw) // 2
        ty = base_y + i * line_h
        for dx, dy in ((-2, -2), (2, -2), (-2, 2), (2, 2), (0, 2)):
            draw.text((tx + dx, ty + dy), ln, font=font_sub, fill=(0, 0, 0, 240))
        draw.text((tx, ty), ln, font=font_sub, fill=(255, 248, 220, 255))

    img.save(out_png)


def subtitle_single_shot(
    shot: dict,
    in_mp4: Path,
    out_mp4: Path,
    global_offset: float,
    include_audit_badge: bool = True,
) -> None:
    width, height = 1344, 768
    d1_start, d1_end = parse_window(shot["dialogue_1"]["window"])
    d2_start, d2_end = parse_window(shot["dialogue_2"]["window"])

    badge = (
        f"{shot['shot_id']} ({global_offset:04.1f}s–{global_offset+10.125:04.1f}s)"
        if include_audit_badge
        else ""
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        png_idle = tmp / "ov_idle.png"
        png_d1 = tmp / "ov_d1.png"
        png_d2 = tmp / "ov_d2.png"

        render_subtitle_overlay_png(png_idle, width, height, "", shot_badge=badge)
        render_subtitle_overlay_png(png_d1, width, height, shot["dialogue_1"]["line"], shot_badge=badge)
        render_subtitle_overlay_png(png_d2, width, height, shot["dialogue_2"]["line"], shot_badge=badge)

        fc = (
            f"[0:v][1:v]overlay=0:0:enable='lt(t,{d1_start:.3f})+between(t,{d1_end:.3f},{d2_start:.3f})+gt(t,{d2_end:.3f})'[v1];"
            f"[v1][2:v]overlay=0:0:enable='between(t,{d1_start:.3f},{d1_end:.3f})'[v2];"
            f"[v2][3:v]overlay=0:0:enable='between(t,{d2_start:.3f},{d2_end:.3f})'[vout]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", str(in_mp4),
            "-i", str(png_idle),
            "-i", str(png_d1),
            "-i", str(png_d2),
            "-filter_complex", fc,
            "-map", "[vout]",
            "-map", "0:a",
            "-c:v", "libx264", "-crf", "18", "-preset", "fast",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            "-c:a", "copy",
            str(out_mp4),
            "-loglevel", "error",
        ]
        subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=SHORT_DRAMA_DIR / "ep01_beizhao_chushi_manifest.json")
    parser.add_argument("--mode", choices=["audit", "release"], default="audit")
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    include_badge = args.mode == "audit"
    ep_tag = "Ep02" if "ep02" in args.manifest.name.lower() else "Ep01"
    ep_slug = "ZhuanshiChongsheng" if ep_tag == "Ep02" else "BeizhaoChushi"

    sub_shots = []
    for idx, shot in enumerate(manifest["shots"]):
        shot_id = shot["shot_id"]
        in_name = shot.get("output_mp4") or f"{shot['output_prefix']}.mp4"
        in_mp4 = ASSETS_DIR / in_name
        out_mp4 = ASSETS_DIR / f"ChuShiChunQiu_{ep_tag}_{shot_id}_Subtitled.mp4"
        subtitle_single_shot(
            shot=shot,
            in_mp4=in_mp4,
            out_mp4=out_mp4,
            global_offset=idx * 10.125,
            include_audit_badge=include_badge,
        )
        sub_shots.append(out_mp4)
        print(f"✅ Burned clean dialogue subtitles (HUD={include_badge}) onto {out_mp4.name}")

    concat_list = Path(f"/tmp/{ep_tag.lower()}_subtitled_concat.txt")
    concat_list.write_text("".join(f"file '{p}'\n" for p in sub_shots), encoding="utf-8")
    master_sub = SHORT_DRAMA_DIR / f"ChuShiChunQiu_{ep_tag}_{ep_slug}_Subtitled_Audit.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", "-movflags", "+faststart", str(master_sub), "-loglevel", "error"],
        check=True,
    )
    print(f"🎬 Master Subtitled Video ready: {master_sub} ({master_sub.stat().st_size / (1024**2):.2f} MB)")


if __name__ == "__main__":
    main()
