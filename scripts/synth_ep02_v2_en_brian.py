#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import json
import math
import re
import shutil
import subprocess
import wave
from array import array
from pathlib import Path

import edge_tts

ROOT = Path("/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab")
VOICE = "en-US-BrianMultilingualNeural"
RATE = "+1%"
SR = 48000
FPS = 30

PRIORITY_ACCENT_WORDS = {
    "gemini", "tasks", "task", "chat", "cloud", "briefing", "morning", "launches",
    "summary", "canvas", "websites", "google", "table", "monitors", "weekly",
    "gmail", "drive", "monday", "connect", "yes", "rogue", "free", "six", "ten",
    "pro", "ultra", "fifty", "fifteen", "global", "five-hour", "budget", "scoped",
    "skills", "slash", "first", "timing", "follow", "assistant", "background",
    "seven", "a.m.", "one-page", "research", "emails", "replies", "pauses",
    "knocks", "countries", "parallel", "rolling", "compute", "repeat", "workflows",
}

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "before", "but", "by", "for",
    "from", "get", "gets", "here", "how", "if", "in", "into", "is", "it",
    "its", "just", "me", "more", "of", "on", "one", "or", "out", "so",
    "than", "that", "the", "them", "this", "to", "until", "what", "when",
    "while", "with", "you", "your",
}


def trim_wav_pcm16(
    in_wav: Path, out_wav: Path, thresh_db: float = -50.0, pad_ms: float = 90.0
) -> tuple[float, float]:
    with wave.open(str(in_wav), "rb") as wf:
        sr = wf.getframerate()
        samples = array("h")
        samples.frombytes(wf.readframes(wf.getnframes()))
    thresh = int(32767 * (10.0 ** (thresh_db / 20.0)))
    nonzero = [i for i, v in enumerate(samples) if abs(v) > thresh]
    if nonzero:
        pad = int(sr * (pad_ms / 1000.0))
        start_idx = max(0, nonzero[0] - pad)
        end_idx = min(len(samples), nonzero[-1] + pad)
        trimmed = samples[start_idx:end_idx]
    else:
        start_idx = 0
        trimmed = samples
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(trimmed.tobytes())
    return len(trimmed) / float(sr), start_idx / float(sr)


def synth_sfx(sfx_dir: Path) -> dict[str, Path]:
    sfx_dir.mkdir(parents=True, exist_ok=True)
    files = {}

    # 1. Soft UI pop (warm damped chirp 380->640Hz, 55ms)
    pop_path = sfx_dir / "pop.wav"
    n_pop = int(SR * 0.055)
    pop_arr = array("h")
    phase = 0.0
    for i in range(n_pop):
        t = i / float(SR)
        env = math.sin(min(1.0, t / 0.008) * math.pi * 0.5) * math.exp(-t * 58.0)
        freq = 380.0 + (640.0 - 380.0) * (i / float(n_pop))
        phase += 2.0 * math.pi * freq / SR
        pop_arr.append(int(max(-32767, min(32767, 0.34 * 32767 * env * math.sin(phase)))))
    with wave.open(str(pop_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pop_arr.tobytes())
    files["pop"] = pop_path

    # 2. Soft glassy swoosh (170ms)
    whoosh_path = sfx_dir / "whoosh.wav"
    n_w = int(SR * 0.170)
    w_arr = array("h")
    lp = 0.0
    rng_state = 1234567
    for i in range(n_w):
        u = i / float(n_w)
        env = math.sin(u * math.pi) ** 1.6
        rng_state = (1103515245 * rng_state + 12345) & 0x7FFFFFFF
        white = (rng_state / float(0x3FFFFFFF)) - 1.0
        alpha = 0.06 + 0.12 * math.sin(u * math.pi)
        lp = lp + alpha * (white - lp)
        w_arr.append(int(max(-32767, min(32767, 0.25 * 32767 * env * lp))))
    with wave.open(str(whoosh_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(w_arr.tobytes())
    files["whoosh"] = whoosh_path

    # 3. Crisp short UI click/tick (26ms)
    tick_path = sfx_dir / "tick.wav"
    n_t = int(SR * 0.026)
    t_arr = array("h")
    for i in range(n_t):
        t = i / float(SR)
        env = math.exp(-t * 145.0)
        val = 0.28 * env * math.sin(2.0 * math.pi * 1120.0 * t)
        t_arr.append(int(max(-32767, min(32767, val * 32767))))
    with wave.open(str(tick_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(t_arr.tobytes())
    files["tick"] = tick_path
    return files


async def synth_segments(lines: list[str], seg_dir: Path) -> list[dict]:
    results = []
    for idx, line in enumerate(lines, start=1):
        raw_mp3 = seg_dir / f"seg_{idx:02d}_raw.mp3"
        pcm_wav = seg_dir / f"seg_{idx:02d}_pcm.wav"
        trim_wav = seg_dir / f"seg_{idx:02d}.wav"

        comm = edge_tts.Communicate(line, voice=VOICE, rate=RATE, boundary="WordBoundary")
        words: list[dict] = []
        audio_bytes = bytearray()
        async for chunk in comm.stream():
            ctype = chunk.get("type")
            if ctype == "audio":
                audio_bytes.extend(chunk["data"])
            elif ctype == "WordBoundary":
                words.append(
                    {
                        "text": chunk["text"],
                        "offset_sec": chunk["offset"] / 10_000_000.0,
                        "dur_sec": chunk["duration"] / 10_000_000.0,
                    }
                )
        raw_mp3.write_bytes(bytes(audio_bytes))

        subprocess.run(
            ["ffmpeg", "-y", "-i", str(raw_mp3), "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(pcm_wav)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        dur, trim_start_sec = trim_wav_pcm16(pcm_wav, trim_wav)
        raw_mp3.unlink(missing_ok=True)
        pcm_wav.unlink(missing_ok=True)

        if not words:
            raise RuntimeError(f"WordBoundary events missing for segment {idx}")

        # Re-base word offsets to trimmed wav
        for w in words:
            w["rel_start_sec"] = max(0.0, w["offset_sec"] - trim_start_sec)
            w["rel_end_sec"] = min(dur, max(w["rel_start_sec"] + 0.08, w["rel_start_sec"] + w["dur_sec"]))

        results.append({"wav": trim_wav, "dur": dur, "words": words, "text": line})
        print(f"SEG {idx}/{len(lines)}: {dur:.3f}s | words={len(words)} | {line[:55]}...")
    return results


def pick_accent_index(chunk_words: list[str]) -> int:
    best_idx = len(chunk_words) - 1
    best_score = -1
    for i, w in enumerate(chunk_words):
        clean = re.sub(r"[^a-zA-Z0-9\-/]", "", w).lower()
        score = 0
        if clean in PRIORITY_ACCENT_WORDS:
            score += 10
        if clean and clean not in STOPWORDS:
            score += 4
        if len(clean) >= 6:
            score += 2
        if i == len(chunk_words) - 1:
            score += 1
        if score > best_score:
            best_score = score
            best_idx = i
    return best_idx


def build_pills_for_segment(
    words: list[dict], seg_speech_start_sec: float, seg_end_sec: float, seg_idx: int
) -> list[dict]:
    # Group 2-4 words per pill, breaking cleanly at clauses or length limits
    groups: list[list[dict]] = []
    cur: list[dict] = []
    for w in words:
        cur.append(w)
        txt = w["text"].strip()
        char_len = sum(len(x["text"]) + 1 for x in cur)
        has_punct = txt.endswith((",", ".", "!", "?", ":"))
        if len(cur) >= 3 or (len(cur) >= 2 and (has_punct or char_len >= 18)):
            groups.append(cur)
            cur = []
    if cur:
        if len(cur) == 1 and groups and len(groups[-1]) <= 3:
            groups[-1].extend(cur)
        else:
            groups.append(cur)

    pills: list[dict] = []
    for g_idx, grp in enumerate(groups):
        w_texts = [x["text"] for x in grp]
        abs_start = seg_speech_start_sec + grp[0]["rel_start_sec"]
        if g_idx + 1 < len(groups):
            next_start = seg_speech_start_sec + groups[g_idx + 1][0]["rel_start_sec"]
            abs_end = next_start
        else:
            abs_end = min(seg_end_sec - 0.03, seg_speech_start_sec + grp[-1]["rel_end_sec"] + 0.14)
        start_f = int(round(abs_start * FPS))
        end_f = max(start_f + 4, int(round(abs_end * FPS)))
        acc_i = pick_accent_index(w_texts)
        pills.append(
            {
                "seg": seg_idx,
                "startFrame": start_f,
                "endFrame": end_f,
                "accentColor": "coral" if (len(pills) + seg_idx) % 2 == 0 else "cobalt",
                "words": [
                    {"text": wt, "accent": wi == acc_i}
                    for wi, wt in enumerate(w_texts)
                ],
            }
        )
    return pills


def stitch_and_mix(segs: list[dict]) -> None:
    audio_dir = ROOT / "pipelines/ai_explainer_ep02/audio"
    sfx_files = synth_sfx(audio_dir / "sfx")

    lead_sec = 0.45
    pause_sec = 0.28
    tail_sec = 0.60

    raw_full = audio_dir / "ep02_v2_en_brian_raw.wav"
    dry_wav = audio_dir / "ep02_v2_en_brian_dry.wav"
    dry_mp3 = audio_dir / "ep02_v2_en_brian_dry.mp3"
    mix_mp3 = audio_dir / "ep02_v2_en_brian_mix_sfx.mp3"
    bgm_wav = ROOT / "assets/music_library/how_markets_break/hmb_02_data_analysis.wav"
    remotion_voice = ROOT / "pipelines/ai_explainer_ep01/pk_talkcraft/remotion/public/voice_ep02_mix.mp3"

    out_samples = array("h", [0] * int(SR * lead_sec))
    pause_arr = array("h", [0] * int(SR * pause_sec))
    tail_arr = array("h", [0] * int(SR * tail_sec))

    timeline = []
    all_pills: list[dict] = []
    cursor = lead_sec
    for idx, seg in enumerate(segs, start=1):
        with wave.open(str(seg["wav"]), "rb") as wf:
            seg_arr = array("h")
            seg_arr.frombytes(wf.readframes(wf.getnframes()))
        out_samples.extend(seg_arr)
        scene_start_sec = 0.0 if idx == 1 else cursor
        speech_start_sec = cursor
        cursor += seg["dur"]
        if idx < len(segs):
            out_samples.extend(pause_arr)
            cursor += pause_sec
        else:
            out_samples.extend(tail_arr)
            cursor += tail_sec

        all_pills.extend(build_pills_for_segment(seg["words"], speech_start_sec, cursor, idx))
        timeline.append(
            {
                "index": idx,
                "text": seg["text"],
                "speech_start_sec": round(speech_start_sec, 3),
                "speech_duration_sec": round(seg["dur"], 3),
                "start_sec": round(scene_start_sec, 3),
                "end_sec": round(cursor, 3),
            }
        )

    with wave.open(str(raw_full), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(out_samples.tobytes())

    # NO speed-up atempo; natural paced narration + clean loudnorm
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(raw_full),
            "-af", "loudnorm=I=-18:TP=-1.5:LRA=9",
            "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(dry_wav),
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

    sfx_track = array("h", [0] * int(total_dur * SR))

    def read_sfx_arr(p: Path) -> array:
        with wave.open(str(p), "rb") as wf:
            a = array("h")
            a.frombytes(wf.readframes(wf.getnframes()))
        return a

    whoosh_a = read_sfx_arr(sfx_files["whoosh"])
    pop_a = read_sfx_arr(sfx_files["pop"])
    tick_a = read_sfx_arr(sfx_files["tick"])

    def overlay(buf: array, src: array, at_sec: float, gain: float) -> None:
        idx0 = int(at_sec * SR)
        for j, v in enumerate(src):
            k = idx0 + j
            if 0 <= k < len(buf):
                buf[k] = max(-32767, min(32767, int(buf[k] + v * gain)))

    # Scene 1 cursor click + halo pop
    overlay(sfx_track, pop_a, 0.42, 0.25)
    overlay(sfx_track, tick_a, 1.25, 0.22)
    for item in timeline[1:]:
        overlay(sfx_track, whoosh_a, max(0.0, item["start_sec"] - 0.05), 0.22)
        overlay(sfx_track, tick_a, item["start_sec"] + 0.06, 0.18)
        dur = item["end_sec"] - item["start_sec"]
        if dur > 4.2:
            overlay(sfx_track, pop_a, item["start_sec"] + dur * 0.48, 0.20)
        if dur > 7.5:
            overlay(sfx_track, tick_a, item["start_sec"] + dur * 0.72, 0.17)

    sfx_wav = audio_dir / "ep02_v2_sfx_bus.wav"
    with wave.open(str(sfx_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(sfx_track.tobytes())

    fade_out_start = max(0.0, total_dur - 1.8)
    # Loop bgm smoothly cleanly with -stream_loop -1 in case audio > bgm duration
    filter_complex = (
        f"[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0[voice];"
        f"[1:a]atrim=0:{total_dur:.3f},asetpts=PTS-STARTPTS,volume=-22dB,"
        f"afade=t=in:st=0:d=0.6,afade=t=out:st={fade_out_start:.3f}:d=1.8[bgm];"
        f"[2:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=-6dB[sfx];"
        f"[voice][bgm][sfx]amix=inputs=3:duration=first:dropout_transition=2,alimiter=limit=0.95[out]"
    )
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(dry_wav),
            "-stream_loop", "-1", "-i", str(bgm_wav),
            "-i", str(sfx_wav),
            "-filter_complex", filter_complex,
            "-map", "[out]", "-b:a", "192k", str(mix_mp3),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    remotion_voice.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mix_mp3, remotion_voice)

    total_frames = int(round(total_dur * FPS))
    prev = 0
    for i, item in enumerate(timeline):
        item["start_frame"] = prev
        end_f = total_frames if i == len(timeline) - 1 else int(round(item["end_sec"] * FPS))
        item["end_frame"] = end_f
        prev = end_f

    # Clamp and ensure monotonic pill frames without overlap
    for i, p in enumerate(all_pills):
        if i + 1 < len(all_pills) and p["endFrame"] > all_pills[i + 1]["startFrame"]:
            p["endFrame"] = max(p["startFrame"] + 2, all_pills[i + 1]["startFrame"])
        if p["endFrame"] > total_frames:
            p["endFrame"] = total_frames

    captions_ts = ROOT / "pipelines/ai_explainer_ep01/pk_talkcraft/remotion/src/captions_ep02.ts"
    ts_payload = {
        "fps": FPS,
        "totalFrames": total_frames,
        "totalDurationSec": round(total_dur, 3),
        "segments": [
            {
                "id": f"s{item['index']}",
                "startFrame": item["start_frame"],
                "endFrame": item["end_frame"],
                "text": item["text"],
            }
            for item in timeline
        ],
        "pills": all_pills,
    }
    captions_ts.write_text(
        "// Auto-generated by synth_ep02_v2_en_brian.py — do not hand-edit.\n"
        "export interface CaptionWord {\n"
        "  text: string;\n"
        "  accent: boolean;\n"
        "}\n\n"
        "export interface CaptionPill {\n"
        "  seg: number;\n"
        "  startFrame: number;\n"
        "  endFrame: number;\n"
        "  accentColor: 'coral' | 'cobalt';\n"
        "  words: CaptionWord[];\n"
        "}\n\n"
        "export interface CaptionSegment {\n"
        "  id: string;\n"
        "  startFrame: number;\n"
        "  endFrame: number;\n"
        "  text: string;\n"
        "}\n\n"
        f"export const CAPTIONS_EP02: {{\n"
        "  fps: number;\n"
        "  totalFrames: number;\n"
        "  totalDurationSec: number;\n"
        "  segments: CaptionSegment[];\n"
        "  pills: CaptionPill[];\n"
        f"}} = {json.dumps(ts_payload, indent=2)};\n",
        encoding="utf-8",
    )

    manifest = {
        "voice": VOICE,
        "rate": RATE,
        "fps": FPS,
        "total_duration_sec": round(total_dur, 3),
        "total_frames": total_frames,
        "pill_count": len(all_pills),
        "mix_mp3": str(mix_mp3),
        "captions_ts": str(captions_ts),
        "segments": timeline,
    }
    (audio_dir / "manifest_ep02_v2_en.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"EP02_V2_FINAL_DUR={total_dur:.3f}s | TOTAL_FRAMES={total_frames} | PILLS={len(all_pills)}")
    for item in timeline:
        print(f"  S{item['index']}: [{item['start_sec']:.3f}s -> {item['end_sec']:.3f}s] frames [{item['start_frame']} -> {item['end_frame']}]")


def main() -> int:
    lines = [
        ln.strip()
        for ln in (ROOT / "pipelines/ai_explainer_ep02/script_lines_en.txt").read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    seg_dir = ROOT / "pipelines/ai_explainer_ep02/audio/segments_v2"
    seg_dir.mkdir(parents=True, exist_ok=True)
    segs = asyncio.run(synth_segments(lines, seg_dir))
    stitch_and_mix(segs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
