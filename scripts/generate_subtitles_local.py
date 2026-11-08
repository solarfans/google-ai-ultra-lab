#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Subtitle Generator for 《楚氏春秋·第一集：空难惊魂·异界重生》
100% Canon Aligned: Dynamically reads JSON spec and renders high-res PNG subtitle cards.
"""

import os
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SPEC_FILE = Path("/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/chu_shi_chun_qiu_ep01_beizhao_chushi.json")
ASSETS_DIR = Path("/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/assets")
SUB_DIR = ASSETS_DIR / "subtitles"
SUB_DIR.mkdir(parents=True, exist_ok=True)

with open(SPEC_FILE, "r", encoding="utf-8") as f:
    spec = json.load(f)

BADGE_COLORS = {
    "旁白": (225, 225, 235, 255),               # Frost White
    "现代楚铮": (120, 200, 255, 255),           # Tech Cyan
    "楚夫人": (255, 170, 180, 255),             # Soft Rose
    "楚 铮 (少年)": (255, 215, 90, 255),         # Imperial Gold
}

# Find suitable system Chinese font on macOS
FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Arial Unicode.ttf"
]
font_path = next((p for p in FONT_CANDIDATES if os.path.exists(p)), None)

if font_path:
    font_badge = ImageFont.truetype(font_path, 28)
    font_text = ImageFont.truetype(font_path, 34)
else:
    font_badge = ImageFont.load_default()
    font_text = ImageFont.load_default()

print("==================================================")
print("🎨 [LOCAL SUBTITLE] 开始生成中文字幕卡 (1344x768 悬浮毛玻璃胶囊)")
print("==================================================")

shots = spec.get("shots", [])
char_dict = spec.get("characters", {})

for shot in shots:
    sid = shot["shot_id"]
    spk_key = shot.get("speaker")
    speaker = char_dict.get(spk_key, {}).get("name_zh", "旁白") if spk_key else "旁白"
    text = shot.get("dialogue_line", "")
    
    # 1344 x 768 transparent canvas
    img = Image.new("RGBA", (1344, 768), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    badge_str = f"【{speaker}】"

    # Calculate text bounding boxes
    bbox_badge = draw.textbbox((0, 0), badge_str, font=font_badge)
    badge_w = bbox_badge[2] - bbox_badge[0]

    bbox_text = draw.textbbox((0, 0), text, font=font_text)
    text_w = bbox_text[2] - bbox_text[0]
    total_w = badge_w + 14 + text_w

    start_x = max(40, (1344 - total_w) // 2)
    start_y = 660

    # Draw rounded pill box background
    pad_x = 24
    pad_y = 12
    card_box = [
        start_x - pad_x,
        start_y - pad_y,
        start_x + total_w + pad_x,
        start_y + 40 + pad_y
    ]
    draw.rounded_rectangle(card_box, radius=16, fill=(15, 15, 20, 205), outline=(60, 60, 75, 180), width=2)

    # Draw Badge
    badge_color = BADGE_COLORS.get(speaker, (225, 225, 235, 255))
    draw.text((start_x, start_y + 4), badge_str, font=font_badge, fill=badge_color)

    # Draw Text
    draw.text((start_x + badge_w + 14, start_y), text, font=font_text, fill=(255, 255, 255, 255))

    out_png = SUB_DIR / f"shot{sid:02d}_sub.png"
    img.save(out_png, "PNG")
    print(f"  🎨 [Shot {sid:02d}] 字幕卡完成: 【{speaker}】{text}")

print("==================================================")
print("🎉 全部 6 张高精度中文字幕卡已生成完毕！")
print("==================================================")
