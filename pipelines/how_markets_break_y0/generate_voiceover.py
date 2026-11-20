#!/usr/bin/env python3
"""
Generate restrained institutional English documentary voiceover via edge-tts (0 CU / $0).
Produces 7 beat WAV files (48kHz mono) plus word-aligned subtitle cues in voiceover_timeline.json.
Includes per-beat retry and per-beat JSON caching so transient WebSocket drops never stall progress.
"""
from __future__ import annotations

import asyncio
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import edge_tts

ROOT = Path(__file__).resolve().parent
BEATS_DIR = ROOT / "audio" / "beats"
TIMELINE_PATH = ROOT / "audio" / "voiceover_timeline.json"

VOICE = "en-US-AndrewMultilingualNeural"
RATE = "-4%"
PITCH = "-2Hz"

BEATS = [
    {
        "beat_id": "beat01",
        "text": "Tech stocks are down. Bitcoin is down. Even gold — the oldest safe haven on earth — is crashing. When everything falls at once, it isn't panic. It's a liquidity trap.",
    },
    {
        "beat_id": "beat02",
        "text": "Look at the last two weeks. From their November highs, the Nasdaq dropped over seven percent. Bitcoin tumbled twenty-three percent. And gold? Down thirteen percent — nearly twice as hard as tech.",
    },
    {
        "beat_id": "beat03",
        "text": "Wait. Gold is supposed to rally when stocks fall. So why did safe havens break their own script?",
    },
    {
        "beat_id": "beat04",
        "text": "Look behind the curtain. Ten-year U.S. Treasury yields pierced five percent. The U.S. dollar surged past one hundred and three. And the VIX nearly doubled, breaking thirty.",
    },
    {
        "beat_id": "beat05",
        "text": "When cash suddenly yields five percent risk-free and leverage unwinds, funds don't sell what they hate. They sell whatever is liquid to meet margin calls — dumping tech, crypto, and profitable gold bars together.",
    },
    {
        "beat_id": "beat06",
        "text": "So — are we officially in a bear market? Not necessarily. Historically, forced liquidity squeezes look identical to the start of a crash — until yields peak and forced selling runs out of fuel.",
    },
    {
        "beat_id": "beat07",
        "text": "In Episode One, we dissect the exact three liquidity signals that separate a violent flush from a true bear market. Subscribe to How Markets Break.",
    },
]


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def split_caption_phrases(text: str, max_chars: int = 58) -> list[str]:
    """Split text into natural documentary subtitle clauses <= max_chars."""
    raw_clauses = re.split(r"(?<=[.?!—])\s+", text.strip())
    phrases: list[str] = []
    for clause in raw_clauses:
        clause = clause.strip()
        if not clause:
            continue
        if len(clause) <= max_chars:
            phrases.append(clause)
            continue
        words = clause.split(" ")
        cur = ""
        for w in words:
            cand = f"{cur} {w}".strip() if cur else w
            if len(cand) <= max_chars:
                cur = cand
            else:
                if cur:
                    phrases.append(cur)
                cur = w
        if cur:
            phrases.append(cur)
    return phrases


def align_phrases_to_words(
    phrases: list[str], word_events: list[dict[str, Any]], total_dur: float
) -> list[dict[str, Any]]:
    """Map subtitle phrases onto edge-tts WordBoundary timings with proportional fallback."""
    if not word_events:
        total_chars = sum(max(1, len(p)) for p in phrases)
        cues = []
        t = 0.0
        for p in phrases:
            dt = total_dur * (max(1, len(p)) / total_chars)
            cues.append({"start": round(t, 3), "end": round(min(total_dur, t + dt), 3), "text": p})
            t += dt
        if cues:
            cues[-1]["end"] = round(total_dur, 3)
        return cues

    cues: list[dict[str, Any]] = []
    w_idx = 0
    n_words = len(word_events)
    for i, phrase in enumerate(phrases):
        tokens = re.findall(r"[A-Za-z0-9']+", phrase)
        take = max(1, len(tokens))
        start_idx = min(w_idx, n_words - 1)
        end_idx = min(n_words - 1, start_idx + take - 1)
        start_s = float(word_events[start_idx]["start"])
        if i == 0:
            start_s = 0.0
        if i == len(phrases) - 1:
            end_s = total_dur
        else:
            next_start = float(word_events[min(n_words - 1, end_idx + 1)]["start"])
            own_end = float(word_events[end_idx]["end"])
            end_s = max(own_end, (own_end + next_start) / 2.0)
        cues.append({"start": round(start_s, 3), "end": round(min(total_dur, max(start_s + 0.2, end_s)), 3), "text": phrase})
        w_idx = min(n_words - 1, end_idx + 1)
    return cues


async def synth_one(beat: dict[str, str]) -> dict[str, Any]:
    beat_id = beat["beat_id"]
    text = beat["text"]
    mp3_path = BEATS_DIR / f"{beat_id}.mp3"
    wav_path = BEATS_DIR / f"{beat_id}.wav"
    meta_path = BEATS_DIR / f"{beat_id}.json"

    if meta_path.is_file() and wav_path.is_file() and wav_path.stat().st_size > 10_000:
        cached = json.loads(meta_path.read_text(encoding="utf-8"))
        if cached.get("text") == text:
            return cached

    last_err: Exception | None = None
    audio_chunks: list[bytes] = []
    word_events: list[dict[str, Any]] = []

    for attempt in range(4):
        try:
            audio_chunks = []
            word_events = []
            comm = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH, boundary="WordBoundary")
            async for chunk in comm.stream():
                ctype = chunk.get("type")
                if ctype == "audio":
                    audio_chunks.append(chunk["data"])
                elif ctype == "WordBoundary":
                    offset_s = float(chunk["offset"]) / 10_000_000.0
                    dur_s = float(chunk["duration"]) / 10_000_000.0
                    word_events.append(
                        {
                            "text": chunk.get("text", ""),
                            "start": offset_s,
                            "end": offset_s + dur_s,
                        }
                    )
            if audio_chunks:
                break
            raise RuntimeError("Empty audio chunks returned by edge-tts")
        except Exception as exc:
            last_err = exc
            await asyncio.sleep(1.5 * (attempt + 1))
    else:
        raise RuntimeError(f"Failed edge-tts synthesis for {beat_id} after 4 attempts: {last_err}")

    mp3_path.write_bytes(b"".join(audio_chunks))
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(mp3_path),
            "-ar",
            "48000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(wav_path),
        ],
        check=True,
    )
    dur = probe_duration(wav_path)
    phrases = split_caption_phrases(text)
    cues = align_phrases_to_words(phrases, word_events, dur)
    result = {
        "beat_id": beat_id,
        "wav": str(wav_path),
        "mp3": str(mp3_path),
        "duration_sec": round(dur, 3),
        "text": text,
        "word_count": len(word_events),
        "cues": cues,
    }
    meta_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


async def main_async() -> None:
    BEATS_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for beat in BEATS:
        res = await synth_one(beat)
        results.append(res)
        print(f"[voice] {res['beat_id']}: {res['duration_sec']:.2f}s ({res['word_count']} word events, {len(res['cues'])} cues)")
        await asyncio.sleep(0.8)

    TIMELINE_PATH.write_text(
        json.dumps(
            {
                "voice": VOICE,
                "rate": RATE,
                "pitch": PITCH,
                "pause_between_beats_sec": 0.45,
                "beats": results,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"Saved timeline: {TIMELINE_PATH}")


if __name__ == "__main__":
    asyncio.run(main_async())
