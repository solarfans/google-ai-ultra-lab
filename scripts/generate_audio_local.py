#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local 0-CU Audio Synthesizer for 《楚氏春秋·第一集：北赵楚氏·假山觉醒》
Uses edge-tts via uv tool run.
"""

import os
import json
import subprocess
import re

SPEC_FILE = "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/chu_shi_chun_qiu_ep01_beizhao_chushi.json"
AUDIO_DIR = "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/assets/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

with open(SPEC_FILE, "r", encoding="utf-8") as f:
    spec = json.load(f)

# Chinese voice mapping for the characters
voice_map = {
    "young_chu_zheng": "zh-CN-YunxiNeural",
    "zhao_ying": "zh-CN-YunyangNeural",
    "young_chu_xuan": "zh-CN-YunjianNeural",
    "narrator": "zh-CN-YunjianNeural",
}

shot_lines = [
    (1, "narrator", "北赵平原郡，第一世家楚氏手握十万精兵，威震天下。"),
    (2, "zhao_ying", "两位好威风啊！不过是我赵家养的一条鹰犬，也配在皇家行宫摆谱？"),
    (3, "narrator", "假山高处青石松脱，幼弟楚铮失足跌落，伴随惊呼坠下！"),
    (4, "narrator", "假山喋血，鲜血顺着额角蜿蜒滑落。双睫颤动，双眸骤然睁开！"),
    (5, "young_chu_zheng", "前世尔等将朕逼上绝路，这一世……朕要这天下尽归楚氏！"),
    (6, "narrator", "九天龙吟惊落月，安阳杀神，于此刻觉醒！"),
]

for sid, spk_key, text in shot_lines:
    voice = voice_map.get(spk_key, "zh-CN-YunjianNeural")
    out_mp3 = os.path.join(AUDIO_DIR, f"shot{sid:02d}_voice.mp3")
    
    print(f"🎙️ [Shot {sid:02d}] 合成配音 ({spk_key} -> {voice}): {text}")
    cmd = [
        "uv", "tool", "run", "edge-tts",
        "--voice", voice,
        "--text", text,
        "--write-media", out_mp3
    ]
    subprocess.check_call(cmd)
    
    probe = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", out_mp3
    ], text=True).strip()
    dur = float(probe)
    print(f"   ✅ Saved: {out_mp3} ({dur:.2f}s)")

print("\n🎉 全部 6 段配音音频本地 0 CU 录制完成！")
