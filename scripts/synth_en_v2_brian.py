#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
import shutil
import subprocess
import wave
from array import array
from pathlib import Path

import edge_tts

ROOT = Path("/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab")
VOICE = "en-US-BrianMultilingualNeural"
RATE = "+0%"
SR = 48000


def trim_wav_pcm16(in_wav: Path, out_wav: Path, thresh_db: float = -42.0, pad_ms: float = 35.0) -> float:
    with wave.open(str(in_wav), "rb") as wf:
        assert wf.getnchannels() == 1
        assert wf.getsampwidth() == 2
        sr = wf.getframerate()
        samples = array("h")
        samples.frombytes(wf.readframes(wf.getnframes()))

    thresh = int(32767 * (10.0 ** (thresh_db / 20.0)))
    nonzero = [i for i, v in enumerate(samples) if abs(v) > thresh]
    if nonzero:
        pad = int(sr * (pad_ms / 1000.0))
        start = max(0, nonzero[0] - pad)
        end = min(len(samples), nonzero[-1] + pad)
        trimmed = samples[start:end]
    else:
        trimmed = samples

    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(trimmed.tobytes())

    return len(trimmed) / float(sr)


async def synth_segments(lines: list[str], seg_dir: Path) -> list[tuple[Path, float]]:
    results: list[tuple[Path, float]] = []
    for idx, line in enumerate(lines, start=1):
        raw_mp3 = seg_dir / f"seg_{idx:02d}_raw.mp3"
        pcm_wav = seg_dir / f"seg_{idx:02d}_pcm.wav"
        trim_wav = seg_dir / f"seg_{idx:02d}.wav"
        comm = edge_tts.Communicate(line, voice=VOICE, rate=RATE)
        await asyncio.wait_for(comm.save(str(raw_mp3)), timeout=20.0)
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(raw_mp3), "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(pcm_wav)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        dur = trim_wav_pcm16(pcm_wav, trim_wav)
        raw_mp3.unlink(missing_ok=True)
        pcm_wav.unlink(missing_ok=True)
        results.append((trim_wav, dur))
        print(f"SEG {idx}/6: {dur:.3f}s | {line}")
    return results


def stitch_and_mix(lines: list[str], segs: list[tuple[Path, float]]) -> None:
    audio_en = ROOT / "pipelines/ai_explainer_ep01/audio_en"
    speech_sum = sum(d for _, d in segs)

    lead_sec = 0.45
    pause_sec = 0.45
    tail_sec = 0.80
    est_total = lead_sec + speech_sum + pause_sec * (len(segs) - 1) + tail_sec
    if est_total > 57.5:
        lead_sec = 0.35
        pause_sec = 0.25
        tail_sec = 0.45

    raw_full = audio_en / "ep01_en_v2_brian_raw.wav"
    dry_wav = audio_en / "ep01_en_v2_brian_dry.wav"
    dry_mp3 = audio_en / "ep01_en_v2_brian_dry.mp3"
    mix_mp3 = audio_en / "ep01_en_v2_brian_mix.mp3"
    bgm_wav = ROOT / "assets/music_library/how_markets_break/hmb_02_data_analysis.wav"
    remotion_voice = ROOT / "pipelines/ai_explainer_ep01/pk_talkcraft/remotion/public/voice_en_brian_mix.mp3"

    out_samples = array("h", [0] * int(SR * lead_sec))
    pause_arr = array("h", [0] * int(SR * pause_sec))
    tail_arr = array("h", [0] * int(SR * tail_sec))

    timeline = []
    cursor = lead_sec
    for idx, ((seg_wav, dur), line) in enumerate(zip(segs, lines), start=1):
        with wave.open(str(seg_wav), "rb") as wf:
            seg_arr = array("h")
            seg_arr.frombytes(wf.readframes(wf.getnframes()))
        out_samples.extend(seg_arr)
        start_sec = 0.0 if idx == 1 else cursor
        cursor += dur
        if idx < len(segs):
            out_samples.extend(pause_arr)
            cursor += pause_sec
        else:
            out_samples.extend(tail_arr)
            cursor += tail_sec
        timeline.append(
            {
                "index": idx,
                "text": line,
                "speech_duration_sec": round(dur, 3),
                "start_sec": round(start_sec, 3),
                "end_sec": round(cursor, 3),
            }
        )

    with wave.open(str(raw_full), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(out_samples.tobytes())

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(raw_full),
            "-af",
            "loudnorm=I=-18:TP=-1.5:LRA=9",
            "-ar",
            str(SR),
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(dry_wav),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(dry_wav), "-b:a", "192k", str(dry_mp3)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    with wave.open(str(dry_wav), "rb") as wf:
        total_dur = wf.getnframes() / float(wf.getframerate())

    fps = 30
    total_frames = int(round(total_dur * fps))
    fade_out_start = max(0.0, total_dur - 1.5)
    filter_complex = (
        f"[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0[voice];"
        f"[1:a]atrim=0:{total_dur:.3f},asetpts=PTS-STARTPTS,volume=-21dB,"
        f"afade=t=in:st=0:d=0.5,afade=t=out:st={fade_out_start:.3f}:d=1.5[bgm];"
        f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2,alimiter=limit=0.95[out]"
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(dry_wav),
            "-i",
            str(bgm_wav),
            "-filter_complex",
            filter_complex,
            "-map",
            "[out]",
            "-b:a",
            "192k",
            str(mix_mp3),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    remotion_voice.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mix_mp3, remotion_voice)

    prev = 0
    for i, item in enumerate(timeline):
        item["start_frame"] = prev
        end_f = total_frames if i == len(timeline) - 1 else int(round(item["end_sec"] * fps))
        item["end_frame"] = end_f
        prev = end_f

    manifest = {
        "voice": VOICE,
        "rate": RATE,
        "bgm_track": str(bgm_wav),
        "fps": fps,
        "lead_sec": lead_sec,
        "pause_sec": pause_sec,
        "tail_sec": tail_sec,
        "total_duration_sec": round(total_dur, 3),
        "total_frames": total_frames,
        "dry_wav": str(dry_wav),
        "dry_mp3": str(dry_mp3),
        "mix_mp3": str(mix_mp3),
        "remotion_voice": str(remotion_voice),
        "segments": timeline,
    }
    manifest_path = audio_en / "manifest_en_v2_brian.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"BRIAN_FINAL_DUR={total_dur:.3f}s | TOTAL_FRAMES={total_frames} | pause={pause_sec}s | tail={tail_sec}s")
    for item in timeline:
        print(
            f"  S{item['index']}: [{item['start_sec']:.3f}s -> {item['end_sec']:.3f}s] "
            f"frames [{item['start_frame']} -> {item['end_frame']}] (speech {item['speech_duration_sec']:.2f}s)"
        )


def main() -> int:
    script_path = ROOT / "pipelines/ai_explainer_ep01/script_lines_en.txt"
    lines = [ln.strip() for ln in script_path.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.strip().startswith("#")]
    seg_dir = ROOT / "pipelines/ai_explainer_ep01/audio_en/brian_segments"
    seg_dir.mkdir(parents=True, exist_ok=True)
    segs = asyncio.run(synth_segments(lines, seg_dir))
    stitch_and_mix(lines, segs)

    # Pre-crop portrait to exact 832x480 with Lanczos
    portrait_src = ROOT / "assets/digital_twin/portraits/anchor_v1_charcoal_shirt.png"
    portrait_dst = ROOT / "pipelines/ai_explainer_ep01/outputs/anchor_832x480.png"
    portrait_dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(portrait_src),
            "-vf",
            "scale=832:480:force_original_aspect_ratio=increase:flags=lanczos,crop=832:480",
            str(portrait_dst),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(f"CROPPED_PORTRAIT={portrait_dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
