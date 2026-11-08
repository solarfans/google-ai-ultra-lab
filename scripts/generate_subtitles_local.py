#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Subtitle Generator for 《楚氏春秋·第一集：北赵楚氏·假山觉醒》
Generates high-resolution PNG subtitle cards and .srt subtitle track.
"""

import os
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

SPEC_FILE = "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/chu_shi_chun_qiu_ep01_beizhao_chushi.json"
ASSETS_DIR = "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/assets"
SUB_DIR = os.path.join(ASSETS_DIR, "subtitles")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
os.makedirs(SUB_DIR, exist_ok=True)

BADGE_COLORS = {
    "旁白": (225, 225, 235, 255),               # Frost White
    "楚 铮 (少年)": (255, 205, 80, 255),         # Imperial Dark Gold
    "赵 应 (小王爷)": (220, 100, 220, 255),       # Royal Purple
    "楚 轩 (少年长兄)": (65, 215, 165, 255),      # Jade Cyan
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

shot_dialogues = [
    (1, "旁白", "北赵平原郡，第一世家楚氏手握十万精兵，威震天下。"),
    (2, "赵 应 (小王爷)", "两位好威风啊！不过是我赵家养的一条鹰犬，也配在皇家行宫摆谱？"),
    (3, "旁白", "假山高处青石松脱，幼弟楚铮失足跌落，伴随惊呼坠下！"),
    (4, "旁白", "假山喋血，鲜血顺着额角蜿蜒滑落。双睫颤动，双眸骤然睁开！"),
    (5, "楚 铮 (少年)", "前世尔等将朕逼上绝路，这一世……朕要这天下尽归楚氏！"),
    (6, "旁白", "九天龙吟惊落月，安阳杀神，于此刻觉醒！"),
]

for sid, speaker, text in shot_dialogues:
    # 1344 x 768 transparent canvas
    img = Image.new("RGBA", (1344, 768), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    badge_str = f"【{speaker}】"
    full_str = f"{badge_str} {text}"

    # Calculate text bounding boxes
    bbox_badge = draw.textbbox((0, 0), badge_str, font=font_badge)
    badge_w = bbox_badge[2] - bbox_badge[0]

    bbox_text = draw.textbbox((0, 0), text, font=font_text)
    text_w = bbox_text[2] - bbox_text[0]
    total_w = badge_w + 12 + text_w

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
    badge_color = BADGE_COLORS.get(speaker, (220, 220, 220, 255))
    draw.text((start_x, start_y + 4), badge_str, font=font_badge, fill=badge_color)

    # Draw Text
    draw.text((start_x + badge_w + 12, start_y), text, font=font_text, fill=(255, 255, 255, 255))

    out_png = os.path.join(SUB_DIR, f"shot{sid:02d}_sub.png")
    img.save(out_png, "PNG")
    print(f"  🎨 [Subtitle Card] Generated: {out_png}")

print("\n🎉 全部 6 张高精度中文字幕卡已生成完毕！")
