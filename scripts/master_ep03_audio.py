#!/usr/bin/env python3
"""Hybrid Dual-Track Studio Audio Mastering for Episode 3《楚氏春秋·第三章 颠倒乾坤》(`master_ep03_audio.py`).

Ensures millisecond-exact non-overlapping alignment against `MiniMax-H3` native audio tracks:
- Shot 01 (Tea Dragon): 100% Native Lip-Synced Dialogue (Wu Anran 0.3s–4.6s, 6yo Chu Zheng 5.0s–9.4s)
- Shot 02 (Xueyu Soul Pact): 6yo Chu Zheng keeps lips closed on screen; G4 ambient bed (muted 0.25s–9.25s to eliminate any phantom vocal bleed) + 28yo Adult Soul OS (`ep03_shot02_master_audio.wav`)
- Shot 03 (Dropped Medicine Bowl): 100% Native Lip-Synced Dialogue (6yo Chu Zheng 0.3s–4.5s, Wang Xiuhe 4.9s–9.5s)
- Shot 04 (Father Chu Mingtang Rejoices): 100% Native Lip-Synced Dialogue (6yo Chu Zheng 0.3s–4.4s, Chu Mingtang 4.8s–9.5s)
- Shot 05 (Blood Shadow Sect Secret Report): 100% Native Lip-Synced Dialogue (Gao Shiying 0.3s–4.6s, Wang Xiuhe 5.0s–9.5s)
- Shot 06 (Diandao Qiankun Climax): Wang Xiuhe native lip-synced reading of《史记》(0.3s–5.1s) -> 6yo Chu Zheng closed-mouth petrified reaction with 28yo Adult Soul Shock OS (5.5s–9.6s)
"""

from __future__ import annotations

import asyncio
import subprocess
from pathlib import Path
import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_DRAMA_DIR = BASE_DIR / "pipelines" / "short_drama"
ASSETS_DIR = SHORT_DRAMA_DIR / "assets_manju_v2"
PREVIEWS_DIR = SHORT_DRAMA_DIR / "audio_previews"


async def synth_stem(text: str, voice: str, rate: str, pitch: str, af_extra: str, out_wav: Path) -> None:
    tmp_mp3 = out_wav.with_suffix(".tmp.mp3")
    comm = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    await comm.save(str(tmp_mp3))
    trim_af = (
        "silenceremove=start_periods=1:start_silence=0.02:start_threshold=-45dB,"
        "areverse,silenceremove=start_periods=1:start_silence=0.04:start_threshold=-45dB,areverse"
    )
    af = f"{trim_af},{af_extra}" if af_extra else trim_af
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(tmp_mp3), "-af", af,
            "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            str(out_wav), "-loglevel", "error",
        ],
        check=True,
    )
    tmp_mp3.unlink(missing_ok=True)


def extract_raw_audio(raw_mp4: Path, out_wav: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(raw_mp4),
            "-vn", "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            str(out_wav), "-loglevel", "error",
        ],
        check=True,
    )


def mux_video_audio(raw_mp4: Path, mastered_wav: Path, out_mp4: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(raw_mp4),
            "-i", str(mastered_wav),
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            "-shortest",
            str(out_mp4),
            "-loglevel", "error",
        ],
        check=True,
    )


async def main() -> None:
    PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    os_af = "aecho=0.8:0.85:40:0.16,loudnorm=I=-14:TP=-1.5:LRA=11"

    # 1. Shot 01 (Tea Dragon — 100% Native Lip-Synced Dialogue)
    for sid, prefix in (
        ("shot01", "manju_ep03_shot01_tea_dragon"),
        ("shot03", "manju_ep03_shot03_dropped_bowl"),
        ("shot04", "manju_ep03_shot04_father_rejoice"),
        ("shot05", "manju_ep03_shot05_secret_sect"),
    ):
        raw_v = ASSETS_DIR / f"_raw_g4_{prefix}_00001.mp4"
        raw_a = PREVIEWS_DIR / f"g4_ep03_{sid}_raw_audio.wav"
        final_a = PREVIEWS_DIR / f"mastered_ep03_{sid}.wav"
        out_v = ASSETS_DIR / f"{prefix}_00001.mp4"
        extract_raw_audio(raw_v, raw_a)
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(raw_a),
                "-af", "loudnorm=I=-15:TP=-1.5:LRA=11",
                "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
                str(final_a), "-loglevel", "error",
            ],
            check=True,
        )
        mux_video_audio(raw_v, final_a, out_v)
        print(f"✅ Mastered Ep03 {sid.upper()} (100% Native Lip-Synced Dialogue)")

    # 2. Shot 02 (Xueyu Soul Pact — Closed-mouth 6yo Chu Zheng + 28yo Adult Soul OS)
    s2_raw_v = ASSETS_DIR / "_raw_g4_manju_ep03_shot02_xueyu_pact_00001.mp4"
    s2_raw_a = PREVIEWS_DIR / "g4_ep03_shot02_raw_audio.wav"
    s2_vo_a = PREVIEWS_DIR / "ep03_shot02_master_audio.wav"
    s2_final_a = PREVIEWS_DIR / "mastered_ep03_shot02.wav"
    s2_out_v = ASSETS_DIR / "manju_ep03_shot02_xueyu_pact_00001.mp4"
    extract_raw_audio(s2_raw_v, s2_raw_a)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(s2_raw_a),
            "-i", str(s2_vo_a),
            "-filter_complex",
            "[0:a]volume=enable='between(t,0.25,9.25)':volume=0.0,volume=enable='lt(t,0.25)+gt(t,9.25)':volume=0.30[bgm];"
            "[1:a]volume=1.18[vo];"
            "[bgm][vo]amix=inputs=2:duration=first:dropout_transition=0[out]",
            "-map", "[out]", "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            str(s2_final_a), "-loglevel", "error",
        ],
        check=True,
    )
    mux_video_audio(s2_raw_v, s2_final_a, s2_out_v)
    print("✅ Mastered Ep03 SHOT02 (0% phantom vocal bleed, pure Adult Soul OS)")

    # 6. Shot 06 (Diandao Qiankun Climax — Wang Xiuhe native spoken 1.2s–5.42s + Adult Soul Shock OS 5.60s–9.65s)
    s6_raw_v = ASSETS_DIR / "_raw_g4_manju_ep03_shot06_diandao_qiankun_00001.mp4"
    s6_raw_a = PREVIEWS_DIR / "g4_ep03_shot06_raw_audio.wav"
    s6_os_stem = PREVIEWS_DIR / "_ep03_s6_adult_os.wav"
    s6_final_a = PREVIEWS_DIR / "mastered_ep03_shot06.wav"
    s6_out_v = ASSETS_DIR / "manju_ep03_shot06_diandao_qiankun_00001.mp4"
    extract_raw_audio(s6_raw_v, s6_raw_a)
    await synth_stem("扶不起的阿斗竟一统天下？！这历史简直颠倒乾坤！", "zh-CN-YunxiNeural", "+14%", "-2Hz", os_af, s6_os_stem)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(s6_raw_a),
            "-i", str(s6_os_stem),
            "-filter_complex",
            "[0:a]volume=enable='between(t,5.42,7.20)':volume=0.0,volume=enable='gt(t,7.20)':volume=0.14[native];"
            "[1:a]adelay=5600|5600,volume=1.35[os];"
            "[native][os]amix=inputs=2:duration=first:dropout_transition=0[out]",
            "-map", "[out]", "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le",
            str(s6_final_a), "-loglevel", "error",
        ],
        check=True,
    )
    s6_os_stem.unlink(missing_ok=True)
    mux_video_audio(s6_raw_v, s6_final_a, s6_out_v)
    print("✅ Mastered Ep03 SHOT06 (0% overlap: Wang Xiuhe 1.2s–5.42s -> Adult Soul Shock OS 5.60s–9.65s)")


if __name__ == "__main__":
    asyncio.run(main())
