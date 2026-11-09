#!/usr/bin/env python3
"""Generate Expressive Neural TTS Voice Seeds & Post-Mix Voiceover Tracks (v3.0).

Replaces all legacy macOS `say -v Tingting` + `asetrate` pitch-shifted seeds with
natural Microsoft Neural TTS (`edge-tts`) voices with human breathing pauses and
zero formant distortion. Also records provenance in `voice_seeds_manifest.json`
for verification by `manju_qa_gate.py`.
"""

from __future__ import annotations

import asyncio
import json
import subprocess
from pathlib import Path

import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_DRAMA_DIR = BASE_DIR / "pipelines" / "short_drama"
ASSETS_DIR = SHORT_DRAMA_DIR / "assets_manju_v2"
SEEDS_MANIFEST_PATH = ASSETS_DIR / "voice_seeds_manifest.json"

# Canonical mapping of characters to natural Neural TTS voices (0 formant shift!)
VOICE_SEED_SPECS = {
    "manju_mother_warm_alto_seed.wav": {
        "character_id": "wang_xiuhe",
        "voice": "zh-CN-XiaoxiaoNeural",
        "rate": "-5%",
        "pitch": "-2Hz",
        "sample_text": "小五儿……别怕，有娘在，就算你以后变成傻子，娘也照料你一辈子。",
        "desc": "Warm, emotional, maternal young noblewoman voice (zh-CN-XiaoxiaoNeural)",
    },
    "manju_son_clear_boy_seed.wav": {
        "character_id": "chu_zheng_6yo",
        "voice": "zh-CN-YunxiaNeural",
        "rate": "+0%",
        "pitch": "+4Hz",
        "sample_text": "娘……您别哭了，小五儿再也不调皮爬高了，小五儿听娘的话。",
        "desc": "Authentic 6-year-old boy child voice (zh-CN-YunxiaNeural)",
    },
    "manju_modern_man_tenor_seed.wav": {
        "character_id": "modern_protagonist",
        "voice": "zh-CN-YunxiNeural",
        "rate": "-4%",
        "pitch": "-3Hz",
        "sample_text": "我不是坠海死了吗？这具六岁孩童的身体……难道我重生到了另一个世界？",
        "desc": "Mature, expressive 28-year-old adult male voice for inner monologue OS (zh-CN-YunxiNeural)",
    },
    "manju_stewardess_urgent_alto_seed.wav": {
        "character_id": "stewardess_broadcast",
        "voice": "zh-CN-XiaoyiNeural",
        "rate": "+6%",
        "pitch": "+0Hz",
        "sample_text": "女士们先生们，飞机遭遇强气流！请立即系好安全带，拉下氧气面罩！",
        "desc": "Clear, professional, urgent airline cabin attendant broadcast voice (zh-CN-XiaoyiNeural, zero pitch-shift distortion)",
    },
    "manju_wuanran_charismatic_baritone_seed.wav": {
        "character_id": "wu_anran",
        "voice": "zh-CN-YunjianNeural",
        "rate": "-6%",
        "pitch": "-4Hz",
        "sample_text": "善杀人者，必善医。小子，算你命不好，遇上我血影宗主了！",
        "desc": "Deep, magnetic, dangerous martial arts sect master baritone (zh-CN-YunjianNeural)",
    },
    "manju_zhangdeli_gatekeeper_seed.wav": {
        "character_id": "zhang_deli",
        "voice": "zh-CN-YunyangNeural",
        "rate": "+2%",
        "pitch": "-2Hz",
        "sample_text": "我家五少爷摔伤后一言不发，太守老爷正重金悬赏名医呢！",
        "desc": "Middle-aged Chu Mansion gatekeeper Zhang Deli voice (zh-CN-YunyangNeural)",
    },
    "manju_father_authoritative_baritone_seed.wav": {
        "character_id": "chu_mingtang",
        "voice": "zh-CN-YunjianNeural",
        "rate": "-2%",
        "pitch": "-6Hz",
        "sample_text": "备什么轿，备马！小五儿若有三长两短，我决不轻饶！",
        "desc": "Authoritative 40-year-old Prefect Chu Mingtang baritone (zh-CN-YunjianNeural)",
    },
    "manju_chuyuan_spirited_teen_seed.wav": {
        "character_id": "chu_yuan",
        "voice": "zh-CN-YunxiNeural",
        "rate": "+6%",
        "pitch": "+6Hz",
        "sample_text": "小五儿小心！来人啊，小五从假山上摔下来了，快叫大夫！",
        "desc": "Spirited 13-year-old teenager Chu Yuan voice (zh-CN-YunxiNeural)",
    },
    "manju_licheng_urgent_steward_seed.wav": {
        "character_id": "li_cheng",
        "voice": "zh-CN-YunyangNeural",
        "rate": "+8%",
        "pitch": "+2Hz",
        "sample_text": "老爷不好了！五少爷在畅春园摔下假山，满脸是血，老夫人命小的速来禀报！",
        "desc": "Urgent Chu Mansion steward Li Cheng voice (zh-CN-YunyangNeural)",
    },
}


async def synthesize_seed(filename: str, spec: dict) -> dict:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    tmp_mp3 = ASSETS_DIR / f"_tmp_{filename}.mp3"
    out_wav = ASSETS_DIR / filename

    communicate = edge_tts.Communicate(
        text=spec["sample_text"],
        voice=spec["voice"],
        rate=spec["rate"],
        pitch=spec["pitch"],
    )
    await communicate.save(str(tmp_mp3))

    # Convert cleanly to 44.1kHz stereo 16-bit PCM WAV with gentle loudness normalization (NO asetrate distortion!)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(tmp_mp3),
        "-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar",
        "44100",
        "-ac",
        "2",
        "-c:a",
        "pcm_s16le",
        str(out_wav),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tmp_mp3.unlink(missing_ok=True)

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(out_wav)],
        check=True,
        capture_output=True,
        text=True,
    )
    duration = round(float(probe.stdout.strip()), 3)
    print(f"✅ Synthesized neural seed: {filename} ({spec['voice']}, {duration}s)")
    return {
        "filename": filename,
        "character_id": spec["character_id"],
        "engine": "edge-tts",
        "voice": spec["voice"],
        "rate": spec["rate"],
        "pitch": spec["pitch"],
        "sample_text": spec["sample_text"],
        "duration_sec": duration,
        "asetrate_used": False,
    }


async def main() -> None:
    records = {}
    for fname, spec in VOICE_SEED_SPECS.items():
        records[fname] = await synthesize_seed(fname, spec)

    SEEDS_MANIFEST_PATH.write_text(
        json.dumps({"version": "3.0", "engine": "edge-tts", "seeds": records}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"🎯 Saved neural voice seed provenance manifest -> {SEEDS_MANIFEST_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
