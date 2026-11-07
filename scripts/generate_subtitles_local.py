#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Subtitle Generator for 《楚氏春秋·正传第一卷：杯底波澜》
Generates high-resolution PNG subtitle cards and .srt subtitle track.
"""

import os
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

SPEC_FILE = "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/chu_shi_chun_qiu_zhengzhuan_ep01.json"
ASSETS_DIR = "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/assets"
SUB_DIR = os.path.join(ASSETS_DIR, "subtitles")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
os.makedirs(SUB_DIR, exist_ok=True)

with open(SPEC_FILE, "r", encoding="utf-8") as f:
    spec = json.load(f)

# Colors for character badges
BADGE_COLORS = {
    "旁白 / 空镜": (220, 220, 235, 255),       # Ivory / Frost White
    "楚铮": (255, 205, 85, 255),               # Noble Dark Gold
    "楚轩": (65, 215, 165, 255),               # Imperial Jade Cyan
    "贾道": (235, 115, 75, 255),               # Battle-hardened Crimson Bronze
    "张岐": (160, 180, 240, 255),              # Covert Scout Azure
}

# Find suitable system Chinese font on macOS
FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Arial Unicode.ttf"
]
font_path = None
for p in FONT_CANDIDATES:
    if os.path.exists(p):
        font_path = p
        break

if not font_path:
    print("Warning: Defaulting to basic font.")
    font_badge = ImageFont.load_default()
    font_text = ImageFont.load_default()
else:
    font_badge = ImageFont.truetype(font_path, 28)
    font_text = ImageFont.truetype(font_path, 34)

srt_entries = []
current_time = 0.0

for shot in spec["shots"]:
    sid = shot["shot_id"]
    speaker = shot["speaker"]
    dialogue = shot["dialogue"]
    audio_file = os.path.join(AUDIO_DIR, f"shot{sid:02d}_voice.mp3")
    
    # Get audio duration
    probe = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_file
    ], text=True).strip()
    dur = float(probe)
    
    # Parse badge and clean text
    if "】" in dialogue:
        badge_text, text = dialogue.split("】", 1)
        badge_text = badge_text + "】"
    else:
        badge_text = f"【{speaker}】"
        text = dialogue
    
    # Render 1344x768 transparent subtitle image
    W, H = 1344, 768
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw dark translucent backdrop
    box_w = W - 120
    box_h = 130
    box_x = 60
    box_y = H - box_h - 40
    
    # Rounded dark slate background
    draw.rounded_rectangle(
        [box_x, box_y, box_x + box_w, box_y + box_h],
        radius=16,
        fill=(12, 14, 20, 205),
        outline=(255, 255, 255, 30),
        width=1
    )
    
    # Draw speaker badge
    badge_color = BADGE_COLORS.get(speaker, (255, 255, 255, 255))
    draw.text((box_x + 35, box_y + 18), badge_text, font=font_badge, fill=badge_color)
    
    # Draw dialogue text
    draw.text((box_x + 35, box_y + 65), text.strip(), font=font_text, fill=(255, 255, 255, 245))
    
    sub_png = os.path.join(SUB_DIR, f"shot{sid:02d}_sub.png")
    img.save(sub_png, "PNG")
    print(f"✅ Generated subtitle card: {sub_png}")
    
    # Add SRT entry
    start_s = current_time
    end_s = current_time + dur
    def fmt_time(s):
        hrs = int(s // 3600)
        mins = int((s % 3600) // 60)
        secs = int(s % 60)
        ms = int((s - int(s)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"
    
    srt_entries.append(f"{sid}\n{fmt_time(start_s)} --> {fmt_time(end_s)}\n{badge_text} {text.strip()}\n")
    current_time = end_s

srt_path = "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/chu_shi_chun_qiu_zhengzhuan_ep01.srt"
with open(srt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(srt_entries))

print(f"🎉 Generated master SRT subtitle: {srt_path} (Total runtime: {current_time:.2f}s)")
