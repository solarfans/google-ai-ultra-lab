#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local 0-CU Audio Synthesizer for 《楚氏春秋·第一集：空难惊魂·异界重生》
100% Canon Aligned: Modern airline crash -> ocean impact -> governor mansion rebirth.
Uses edge-tts via uv tool run.
"""

import os
import json
import subprocess
from pathlib import Path

SPEC_FILE = Path("/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/chu_shi_chun_qiu_ep01_beizhao_chushi.json")
AUDIO_DIR = Path("/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/assets/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

with open(SPEC_FILE, "r", encoding="utf-8") as f:
    spec = json.load(f)

# Chinese voice mapping for the characters
voice_map = {
    "narrator": "zh-CN-YunjianNeural",             # 沉稳旁白
    "modern_protagonist": "zh-CN-YunyangNeural",   # 现代成熟精英
    "mrs_chu": "zh-CN-XiaoxiaoNeural",             # 悲痛救子母亲
    "young_chu_zheng": "zh-CN-YunxiNeural",        # 9岁英气幼世子
}

shots = spec.get("shots", [])
print("==================================================")
print("🎙️ [LOCAL AUDIO] 开始合成《楚氏春秋·第一集》全套原著配音")
print("==================================================")

for shot in shots:
    sid = shot["shot_id"]
    spk_key = shot.get("speaker", "narrator")
    text = shot.get("dialogue_line", "")
    voice = voice_map.get(spk_key, "zh-CN-YunjianNeural")
    out_mp3 = AUDIO_DIR / f"shot{sid:02d}_voice.mp3"
    
    print(f"🎙️ [Shot {sid:02d}] 角色: {spk_key} ({voice}) -> {text}")
    cmd = [
        "uv", "tool", "run", "edge-tts",
        "--voice", voice,
        "--text", text,
        "--write-media", str(out_mp3)
    ]
    subprocess.check_call(cmd)
    
    probe = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(out_mp3)
    ], text=True).strip()
    dur = float(probe)
    print(f"   ✅ Saved: {out_mp3.name} ({dur:.2f}s)")

print("==================================================")
print("🎉 全部 6 段原著配音音频本地 0 CU 录制完成！")
print("==================================================")
