#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local 0-CU Audio Synthesizer for 《楚氏春秋·正传第一卷：杯底波澜》
Uses edge-tts via uv tool run.
"""

import os
import json
import subprocess
import re

SPEC_FILE = "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/chu_shi_chun_qiu_zhengzhuan_ep01.json"
AUDIO_DIR = "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/assets/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

with open(SPEC_FILE, "r", encoding="utf-8") as f:
    spec = json.load(f)

voice_map = {
    "旁白 / 空镜": "zh-CN-YunjianNeural",
    "楚铮": "zh-CN-YunxiNeural",
    "楚轩": "zh-CN-YunjianNeural",
    "贾道": "zh-CN-YunyangNeural",
    "张岐": "zh-CN-YunxiNeural",
}

for shot in spec["shots"]:
    sid = shot["shot_id"]
    speaker = shot["speaker"]
    raw_text = shot["dialogue"]
    # Strip speaker prefix e.g. 【楚五公子 · 楚铮】
    clean_text = re.sub(r"【.*?】", "", raw_text).strip()
    
    voice = voice_map.get(speaker, "zh-CN-YunxiNeural")
    out_mp3 = os.path.join(AUDIO_DIR, f"shot{sid:02d}_voice.mp3")
    
    print(f"🎙️ [Shot {sid:02d}] Synthesizing ({speaker} -> {voice}): {clean_text}")
    cmd = [
        "uv", "tool", "run", "edge-tts",
        "--voice", voice,
        "--text", clean_text,
        "--write-media", out_mp3
    ]
    subprocess.check_call(cmd)
    
    # Probe duration with ffprobe
    probe = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", out_mp3
    ], text=True).strip()
    dur = float(probe)
    print(f"   ✅ Saved: {out_mp3} ({dur:.2f}s)")

print("\n🎉 All 6 audio voiceovers generated successfully at 0 CU!")
