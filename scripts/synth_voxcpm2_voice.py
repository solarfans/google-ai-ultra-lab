#!/usr/bin/env python3
"""Mac Apple Silicon (MPS) VoxCPM2 batch voice synthesizer for AI explainer scripts.

Zero-burn local execution:
- Uses openbmb/VoxCPM2 (~6.4GB weights) with PYTORCH_ENABLE_MPS_FALLBACK=1
- Clones owner voice from a 12-15s clean reference WAV
- Synthesizes line-by-line, trims leading/trailing silence, inserts natural pauses,
  normalizes loudness to -18 LUFS for review/mastering, and outputs manifest.json.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf


def _trim_silence(wav: np.ndarray, sr: int, thresh_db: float = -42.0, pad_ms: float = 40.0) -> np.ndarray:
    if wav.ndim > 1:
        mono = np.mean(wav, axis=1)
    else:
        mono = wav
    peak = float(np.max(np.abs(mono))) if mono.size else 0.0
    if peak < 1e-6:
        return wav
    amp_thresh = 10.0 ** (thresh_db / 20.0)
    idx = np.where(np.abs(mono) > amp_thresh)[0]
    if idx.size == 0:
        return wav
    pad = int(sr * (pad_ms / 1000.0))
    start = max(0, int(idx[0]) - pad)
    end = min(len(wav), int(idx[-1]) + pad)
    return wav[start:end]


def main() -> int:
    parser = argparse.ArgumentParser(description="Synthesize voiceover with local VoxCPM2.")
    parser.add_argument("--script", required=True, help="Text file with one spoken line per line.")
    parser.add_argument("--ref-wav", required=True, help="16kHz/48kHz clean reference voice WAV.")
    parser.add_argument("--prompt-text", default="", help="Exact transcript of ref-wav for Ultimate Cloning mode (optional).")
    parser.add_argument("--mode", choices=["controllable", "ultimate"], default="controllable", help="Cloning mode.")
    parser.add_argument("--model-id", default="openbmb/VoxCPM2", help="HF repo id or local model dir.")
    parser.add_argument("--out-dir", required=True, help="Output directory for wav/mp3/manifest.")
    parser.add_argument("--prefix", default="ep01_zh_voxcpm2", help="Output filename prefix.")
    parser.add_argument("--timesteps", type=int, default=18, help="Inference timesteps (default 18).")
    parser.add_argument("--cfg", type=float, default=1.7, help="CFG value (default 1.7).")
    parser.add_argument("--pause-sec", type=float, default=0.28, help="Pause duration between lines.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--first-line-only", action="store_true", help="Only synthesize line 1 for quick A/B check.")
    args = parser.parse_args()

    os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
    from voxcpm import VoxCPM

    script_path = Path(args.script)
    lines = [ln.strip() for ln in script_path.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.strip().startswith("#")]
    if not lines:
        print("ERROR: no spoken lines found in script", file=sys.stderr)
        return 1
    if args.first_line_only:
        lines = lines[:1]

    out_dir = Path(args.out_dir)
    segments_dir = out_dir / "segments"
    segments_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    print(f"Loading VoxCPM2 ({args.model_id})...", flush=True)
    model = VoxCPM.from_pretrained(args.model_id, load_denoiser=False)
    sr = int(getattr(model.tts_model, "sample_rate", 48000))
    print(f"Model loaded in {time.time() - t0:.1f}s (sample_rate={sr}Hz)", flush=True)

    pause_samples = int(sr * args.pause_sec)
    pause_arr = np.zeros(pause_samples, dtype=np.float32)

    combined = []
    manifest_segments = []
    cursor_sec = 0.0

    for idx, line in enumerate(lines, start=1):
        t_line = time.time()
        kwargs = dict(
            text=line,
            cfg_value=args.cfg,
            inference_timesteps=args.timesteps,
            normalize=True,
            denoise=False,
        )
        if args.mode == "ultimate" and args.prompt_text.strip():
            kwargs["prompt_wav_path"] = args.ref_wav
            kwargs["prompt_text"] = args.prompt_text.strip()
        else:
            kwargs["reference_wav_path"] = args.ref_wav

        import torch

        torch.manual_seed(args.seed + idx - 1)
        wav = model.generate(**kwargs)

        wav = np.asarray(wav, dtype=np.float32).squeeze()
        wav = _trim_silence(wav, sr)
        dur = len(wav) / float(sr)

        seg_path = segments_dir / f"seg_{idx:02d}.wav"
        sf.write(str(seg_path), wav, sr)

        manifest_segments.append(
            {
                "index": idx,
                "text": line,
                "start_sec": round(cursor_sec, 3),
                "end_sec": round(cursor_sec + dur, 3),
                "duration_sec": round(dur, 3),
                "file": str(seg_path),
            }
        )
        combined.append(wav)
        cursor_sec += dur
        if idx < len(lines) and pause_samples > 0:
            combined.append(pause_arr)
            cursor_sec += args.pause_sec

        print(f"[{idx}/{len(lines)}] {dur:.2f}s (gen {time.time() - t_line:.1f}s): {line}", flush=True)

    raw_master = out_dir / f"{args.prefix}_raw.wav"
    master_wav = out_dir / f"{args.prefix}_master.wav"
    preview_mp3 = out_dir / f"{args.prefix}_preview.mp3"

    full_audio = np.concatenate(combined) if combined else np.zeros(sr, dtype=np.float32)
    sf.write(str(raw_master), full_audio, sr)

    # Loudness-normalize to -18 LUFS (clean studio spoken-word preview/master) at 48kHz mono
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(raw_master),
            "-af",
            "loudnorm=I=-18:TP=-1.5:LRA=9",
            "-ar",
            "48000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(master_wav),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(master_wav),
            "-b:a",
            "192k",
            str(preview_mp3),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    manifest = {
        "model_id": args.model_id,
        "mode": args.mode,
        "sample_rate": 48000,
        "inference_timesteps": args.timesteps,
        "cfg_value": args.cfg,
        "pause_sec": args.pause_sec,
        "total_duration_sec": round(cursor_sec, 3),
        "master_wav": str(master_wav),
        "preview_mp3": str(preview_mp3),
        "segments": manifest_segments,
    }
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"DONE: {master_wav} ({cursor_sec:.2f}s) | manifest={manifest_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
