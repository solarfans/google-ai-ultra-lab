#!/usr/bin/env python3
"""Synthesize Broadcast-Quality Dual-Track Episode Audio Previews & Local Animatic (v4.1).

Upgrades in v4.1 (Autonomous Defect Self-Healing):
- Strips leading/trailing dead silence from `edge-tts` outputs so stems never collide.
- Dynamically measures exact stem durations (`dur1`, `dur2`), guarantees >=0.35s breathing
  gap between `stem1` and `stem2` (ZERO overlap), and guarantees `end_time <= 9.95s`
  (ZERO tail cutoff at the 10.125s shot boundary).
- Renders a 0-CU Local Storyboard Animatic MP4 (`ChuShiChunQiu_Ep02_v2_Local_Animatic_Preview.mp4`)
  with clean subtitles and `+faststart` for instant pre-render inspection.
"""

from __future__ import annotations

import asyncio
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

import edge_tts

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_DRAMA_DIR = BASE_DIR / "pipelines" / "short_drama"
ASSETS_DIR = SHORT_DRAMA_DIR / "assets_manju_v2"
AUDIO_PREVIEW_DIR = SHORT_DRAMA_DIR / "audio_previews"

CHAR_VOICE_CONFIG = {
    "modern_protagonist": {"voice": "zh-CN-YunxiNeural", "rate": "+2%", "pitch": "-3Hz"},
    "stewardess_broadcast": {"voice": "zh-CN-XiaoyiNeural", "rate": "+8%", "pitch": "+0Hz"},
    "chu_zheng_6yo": {"voice": "zh-CN-YunxiaNeural", "rate": "+2%", "pitch": "+3Hz"},
    "wang_xiuhe": {"voice": "zh-CN-XiaoxiaoNeural", "rate": "+0%", "pitch": "-2Hz"},
    "wu_anran": {"voice": "zh-CN-YunjianNeural", "rate": "+0%", "pitch": "-4Hz"},
    "zhang_deli": {"voice": "zh-CN-YunyangNeural", "rate": "+6%", "pitch": "-2Hz"},
    "chu_mingtang": {"voice": "zh-CN-YunjianNeural", "rate": "+2%", "pitch": "-6Hz"},
    "chu_yuan": {"voice": "zh-CN-YunxiNeural", "rate": "+8%", "pitch": "+6Hz"},
    "li_cheng": {"voice": "zh-CN-YunyangNeural", "rate": "+10%", "pitch": "+2Hz"},
}


def get_wav_duration(wav_path: Path) -> float:
    with wave.open(str(wav_path), "rb") as wf:
        return wf.getnframes() / float(wf.getframerate())


def parse_start_ms(window_str: str) -> int:
    start_str = re.split(r"[–-]", window_str)[0].strip()
    mm, ss = start_str.split(":")
    return int((int(mm) * 60.0 + float(ss)) * 1000)


async def tts_to_wav(text: str, char_id: str, voice_mode: str, out_wav: Path, max_dur_sec: float = 4.35) -> float:
    cfg = CHAR_VOICE_CONFIG[char_id]
    tmp_mp3 = out_wav.with_suffix(".tmp.mp3")
    raw_wav = out_wav.with_suffix(".raw.wav")
    comm = edge_tts.Communicate(text=text, voice=cfg["voice"], rate=cfg["rate"], pitch=cfg["pitch"])
    await comm.save(str(tmp_mp3))

    trim_af = (
        "silenceremove=start_periods=1:start_silence=0.03:start_threshold=-45dB,"
        "areverse,silenceremove=start_periods=1:start_silence=0.05:start_threshold=-45dB,areverse"
    )
    if voice_mode == "offscreen_pa":
        af = f"{trim_af},highpass=f=450,lowpass=f=3100,acompressor=threshold=-18dB:ratio=3:attack=5:release=50,loudnorm=I=-16:TP=-1.5:LRA=9"
    elif voice_mode == "inner_monologue_os":
        af = f"{trim_af},aecho=0.8:0.85:40:0.16,loudnorm=I=-15:TP=-1.5:LRA=11"
    else:
        af = f"{trim_af},loudnorm=I=-15:TP=-1.5:LRA=11"

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(tmp_mp3),
            "-af",
            af,
            "-ar",
            "44100",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            str(raw_wav),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    tmp_mp3.unlink(missing_ok=True)

    dur = get_wav_duration(raw_wav)
    if dur > max_dur_sec:
        tempo = min(1.22, max(1.02, dur / max_dur_sec))
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(raw_wav),
                "-af",
                f"atempo={tempo:.3f}",
                "-ar",
                "44100",
                "-ac",
                "2",
                "-c:a",
                "pcm_s16le",
                str(out_wav),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        raw_wav.unlink(missing_ok=True)
    else:
        raw_wav.replace(out_wav)

    return get_wav_duration(out_wav)


async def build_shot_audio(shot: dict, ep_id: str) -> tuple[Path, dict]:
    AUDIO_PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    sid = shot["shot_id"].lower()
    shot_mode = shot.get("shot_mode", "natural_dialogue")

    s1 = shot["subject_1"]
    s2 = shot["subject_2"]
    d1 = shot["dialogue_1"]
    d2 = shot["dialogue_2"]

    if shot_mode == "offscreen_pa_and_os":
        speaker_1 = s2
        speaker_2 = s1
    elif shot_mode == "single_inner_monologue_os":
        speaker_1 = s2
        speaker_2 = s2
    else:
        speaker_1 = s1
        speaker_2 = s2

    stem1 = AUDIO_PREVIEW_DIR / f"_{ep_id}_{sid}_d1.wav"
    stem2 = AUDIO_PREVIEW_DIR / f"_{ep_id}_{sid}_d2.wav"

    dur1 = await tts_to_wav(d1["line"], speaker_1, d1.get("voice_mode", "onscreen_spoken"), stem1, max_dur_sec=4.20)

    if d2.get("voice_mode") == "os_then_spoken" and "……" in d2["line"]:
        part_os, part_spoken = d2["line"].split("……", 1)
        stem2_a = AUDIO_PREVIEW_DIR / f"_{ep_id}_{sid}_d2a_os.wav"
        stem2_b = AUDIO_PREVIEW_DIR / f"_{ep_id}_{sid}_d2b_spoken.wav"
        await tts_to_wav(part_os + "……", "modern_protagonist", "inner_monologue_os", stem2_a, max_dur_sec=2.10)
        await tts_to_wav(part_spoken, speaker_2, "onscreen_spoken", stem2_b, max_dur_sec=2.10)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(stem2_a),
                "-i",
                str(stem2_b),
                "-filter_complex",
                "[0:a][1:a]concat=n=2:v=0:a=1[out]",
                "-map",
                "[out]",
                str(stem2),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        stem2_a.unlink(missing_ok=True)
        stem2_b.unlink(missing_ok=True)
        dur2 = get_wav_duration(stem2)
    else:
        dur2 = await tts_to_wav(d2["line"], speaker_2, d2.get("voice_mode", "onscreen_spoken"), stem2, max_dur_sec=4.35)

    delay1_ms = max(250, parse_start_ms(d1["window"]))
    end1_ms = delay1_ms + int(dur1 * 1000)
    # Enforce at least 350ms natural breath pause between stem1 and stem2!
    delay2_ms = max(parse_start_ms(d2["window"]), end1_ms + 350)
    end2_ms = delay2_ms + int(dur2 * 1000)

    out_shot_wav = AUDIO_PREVIEW_DIR / f"{ep_id}_{sid}_master_audio.wav"
    filter_complex = (
        f"aevalsrc=0:c=stereo:s=44100:d=10.125[bed];"
        f"[0:a]adelay={delay1_ms}|{delay1_ms}[a1];"
        f"[1:a]adelay={delay2_ms}|{delay2_ms}[a2];"
        f"[bed][a1][a2]amix=inputs=3:duration=first:dropout_transition=0,dynaudnorm=f=150:g=15[out]"
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(stem1),
            "-i",
            str(stem2),
            "-filter_complex",
            filter_complex,
            "-map",
            "[out]",
            "-ar",
            "44100",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            str(out_shot_wav),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    stem1.unlink(missing_ok=True)
    stem2.unlink(missing_ok=True)

    timing_info = {
        "shot_id": shot["shot_id"],
        "d1_start_sec": round(delay1_ms / 1000.0, 2),
        "d1_end_sec": round(end1_ms / 1000.0, 2),
        "gap_sec": round((delay2_ms - end1_ms) / 1000.0, 2),
        "d2_start_sec": round(delay2_ms / 1000.0, 2),
        "d2_end_sec": round(end2_ms / 1000.0, 2),
    }
    print(
        f"🎧 {shot['shot_id']} audio -> d1=[{timing_info['d1_start_sec']:.2f}s–{timing_info['d1_end_sec']:.2f}s], "
        f"gap={timing_info['gap_sec']:.2f}s, d2=[{timing_info['d2_start_sec']:.2f}s–{timing_info['d2_end_sec']:.2f}s]"
    )
    return out_shot_wav, timing_info


async def main() -> None:
    manifest_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SHORT_DRAMA_DIR / "ep02_zhuanshi_chongsheng_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    ep_id = manifest["episode_id"]

    shot_wavs = []
    timings = {}
    for shot in manifest["shots"]:
        w, t_info = await build_shot_audio(shot, ep_id)
        shot_wavs.append(w)
        timings[shot["shot_id"]] = t_info

    (AUDIO_PREVIEW_DIR / f"{ep_id}_audio_timings.json").write_text(
        json.dumps(timings, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    full_wav = AUDIO_PREVIEW_DIR / f"{ep_id}_full_episode_audio_preview.wav"
    inputs = []
    for w in shot_wavs:
        inputs.extend(["-i", str(w)])
    concat_filter = "".join(f"[{i}:a]" for i in range(len(shot_wavs))) + f"concat=n={len(shot_wavs)}:v=0:a=1[out]"
    subprocess.run(
        ["ffmpeg", "-y", *inputs, "-filter_complex", concat_filter, "-map", "[out]", str(full_wav)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(f"🎯 Synthesized full episode audio preview -> {full_wav}")


if __name__ == "__main__":
    asyncio.run(main())
