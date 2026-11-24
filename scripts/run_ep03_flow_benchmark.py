#!/usr/bin/env python3
"""Closed-loop Google Flow (`gflow-cli`) benchmark runner for 《楚氏春秋》 Ep03.

Reuses the exact 6 approved 1344x768 first frames from `ep03_diandao_qiankun_manifest.json`
for an apples-to-apples A/B comparison against the legacy Colab G4 (`MiniMax-H3 int8`) run.
Enforces `--count 1` and `--max-credits`, never auto-retries WAF/refusal exit codes
(`10`, `22`, `23`, `36`, `45`), and records per-shot timing, credit deltas, and ffprobe
metadata to `pipelines/short_drama/ep03_flow_benchmark/metrics.json`.
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_DRAMA_DIR = BASE_DIR / "pipelines" / "short_drama"
MANIFEST_PATH = SHORT_DRAMA_DIR / "ep03_diandao_qiankun_manifest.json"
ASSETS_DIR = SHORT_DRAMA_DIR / "assets_manju_v2"
BENCH_DIR = SHORT_DRAMA_DIR / "ep03_flow_benchmark"
RENDERS_DIR = BENCH_DIR / "renders"
UPSCALED_DIR = BENCH_DIR / "upscaled"
METRICS_PATH = BENCH_DIR / "metrics.json"

NO_AUTO_RETRY_EXIT_CODES = {10, 22, 23, 36, 45}

SHOT_PROMPTS: dict[str, dict[str, Any]] = {
    "Shot01": {
        "speaker_mode": "onscreen_dialogue",
        "prompt": (
            "UE5 3D Chinese animation Donghua CG masterpiece matching the first frame. "
            "Smooth medium tracking shot inside the sunlit Chu Mansion hall. "
            "Martial arts master Wu Anran in slate-gray scholar robe raises two fingers with a charismatic smile, "
            "channeling glowing emerald-green Yunshan tea flowing out of the celadon teapot into mid-air as a spiraling translucent green water dragon "
            "that coils gracefully and disperses into fine mist before 6-year-old boy Chu Zheng. "
            "First, Wu Anran speaks in a charismatic deep Mandarin baritone with natural lip-sync: "
            "\"看好了！这云山绿茶化龙之术，你要不要学？\" "
            "Then 6-year-old Chu Zheng opens his bright eyes wide, claps his small hands excitedly, and replies in a crisp lively 6-year-old Mandarin boy voice with natural lip-sync: "
            "\"愿意！伯伯好厉害，小五儿要跟伯伯学功夫！\" "
            "Authentic flowing water stream whoosh and soft mist burst Foley sound, zero background music, no subtitles, no text, no watermark."
        ),
    },
    "Shot02": {
        "speaker_mode": "inner_monologue_os",
        "prompt": (
            "UE5 3D Chinese animation Donghua CG masterpiece matching the first frame. "
            "Gentle warm sunlit push-in medium close-up on the green Chu Mansion garden lawn. "
            "6-year-old Chu Zheng sits on the grass gently stroking the snow-white cat Xueyu with one hand "
            "while resting his other small hand warmly over his chest; his lips stay strictly closed the entire time with calm, tender, resolute eyes. "
            "Over the silent serene scene, a warm clear 28-year-old adult male Mandarin inner-monologue voiceover speaks softly: "
            "\"雪玉，这具身体里既有你的小主人，也有我。从今往后，世上只有小楚铮，绝不再让娘亲担心！\" "
            "Soft garden breeze and gentle cat purr Foley sound, zero background music, no subtitles, no text, no watermark."
        ),
    },
    "Shot03": {
        "speaker_mode": "onscreen_dialogue",
        "prompt": (
            "UE5 3D Chinese animation Donghua CG masterpiece matching the first frame. "
            "Emotional medium two-shot in the sunlit Chu Mansion courtyard. "
            "First, 6-year-old Chu Zheng wrinkles his small nose playfully, tugs his mother's emerald sleeve, and speaks in a lively childish Mandarin boy voice with natural lip-sync: "
            "\"娘，小五儿肚子饿了，那药好苦，我不吃药！\" "
            "Hearing her mute son speak again, Mother Wang Xiuhe gasps in stunned joy, accidentally drops the porcelain medicine bowl shattering on the stone pavement, "
            "kneels down with glistening tears and pulls Chu Zheng tightly into her embrace, speaking in a choked, loving Mandarin maternal alto voice with natural lip-sync: "
            "\"小五儿……你终于又说话了！可把娘担心死了！\" "
            "Crisp porcelain bowl shattering on stone and silk robe rustle Foley sound, zero background music, no subtitles, no text, no watermark."
        ),
    },
    "Shot04": {
        "speaker_mode": "onscreen_dialogue",
        "prompt": (
            "UE5 3D Chinese animation Donghua CG masterpiece matching the first frame. "
            "Lively celebratory medium tracking shot inside the grand wooden Chu Mansion study. "
            "First, 6-year-old Chu Zheng bows spiritedly with clasped small hands and a bright beaming smile, speaking in a clear cheerful Mandarin boy voice with natural lip-sync: "
            "\"小五儿见过父亲！孩儿的病已经全好啦！\" "
            "Prefect Chu Mingtang in deep imperial-purple official robes springs up from behind his rosewood desk in ecstatic disbelief, "
            "steps forward with glistening eyes to scoop his son up happily, laughing heartily and speaking in a resonant commanding Mandarin baritone with natural lip-sync: "
            "\"好！好！多谢吴先生妙手回春，择日便行拜师大礼！\" "
            "Teacup clink and warm wooden room Foley sound, zero background music, no subtitles, no text, no watermark."
        ),
    },
    "Shot05": {
        "speaker_mode": "onscreen_dialogue",
        "prompt": (
            "UE5 3D Chinese animation Donghua CG masterpiece matching the first frame. "
            "Slow suspenseful push-in medium two-shot in a lantern-lit corridor of the Chu Mansion at dusk. "
            "First, veteran Chief Steward Gao Shiying bows respectfully with cupped hands and speaks in a guarded, vigilant low Mandarin bass-baritone with natural lip-sync: "
            "\"回大小姐，那吴先生，竟是魔门血影宗主魔秀士！\" "
            "Wang Xiuhe pauses calmly under the warm lantern glow, instead of alarm a subtle enigmatic knowing smile curves her lips as she replies in a composed, dignified Mandarin alto voice with natural lip-sync: "
            "\"血影宗？那可真是巧了……此事暂且别告诉老爷。\" "
            "Quiet evening courtyard breeze and subtle silk movement Foley sound, zero background music, no subtitles, no text, no watermark."
        ),
    },
    "Shot06": {
        "speaker_mode": "mixed_os_climax",
        "prompt": (
            "UE5 3D Chinese animation Donghua CG masterpiece matching the first frame. "
            "Dramatic push-in close-medium two-shot beside the bookshelves in the Chu Mansion study. "
            "First, Mother Wang Xiuhe holds an open thread-bound classical history book and speaks warmly in a gentle Mandarin maternal voice with natural lip-sync: "
            "\"后汉太宗刘禅雄才大略，五年一统天下。\" "
            "The camera pushes in sharply onto 6-year-old Chu Zheng clutching a classical book; his lips remain tightly closed while his dark eyes widen in utter petrified shock, "
            "and a shocked 28-year-old adult male Mandarin inner-monologue voiceover exclaims internally: "
            "\"扶不起的阿斗竟一统天下？！这历史简直颠倒乾坤！\" "
            "Crisp ancient paper page-turn Foley sound, zero background music, no subtitles, no text, no watermark."
        ),
    },
}


def extract_json_payload(stdout: str) -> dict[str, Any] | None:
    """Parse the last valid JSON object emitted on stdout (ignoring structlog lines)."""
    decoder = json.JSONDecoder()
    best: dict[str, Any] | None = None
    idx = 0
    while True:
        pos = stdout.find("{", idx)
        if pos == -1:
            break
        try:
            obj, end = decoder.raw_decode(stdout[pos:])
            if isinstance(obj, dict):
                best = obj
            idx = pos + end
        except json.JSONDecodeError:
            idx = pos + 1
    return best


def run_ffprobe(media_path: Path) -> dict[str, Any]:
    if not media_path.exists():
        return {"exists": False}
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-of",
        "json",
        str(media_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return {"exists": True, "size_bytes": media_path.stat().st_size, "ffprobe_error": proc.stderr[-300:]}
    data = json.loads(proc.stdout)
    fmt = data.get("format", {})
    streams = data.get("streams", [])
    v_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
    a_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
    return {
        "exists": True,
        "size_bytes": media_path.stat().st_size,
        "duration_sec": round(float(fmt.get("duration", 0.0)), 3),
        "width": v_stream.get("width"),
        "height": v_stream.get("height"),
        "fps": v_stream.get("r_frame_rate"),
        "has_audio": a_stream is not None,
        "audio_codec": a_stream.get("codec_name") if a_stream else None,
        "audio_sample_rate": a_stream.get("sample_rate") if a_stream else None,
    }


def load_metrics() -> dict[str, Any]:
    if METRICS_PATH.exists():
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    return {
        "benchmark_name": "ChuShiChunQiu Ep03 Flow vs Colab",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "shots": {},
        "upscales": {},
    }


def save_metrics(metrics: dict[str, Any]) -> None:
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    metrics["updated_at_utc"] = datetime.now(timezone.utc).isoformat()
    METRICS_PATH.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find_media_id(payload: dict[str, Any] | None) -> str | None:
    if not payload:
        return None
    for key in ("media_id", "mediaId", "video_id", "id", "asset_id"):
        val = payload.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    for nested_key in ("result", "video", "media", "data"):
        nested = payload.get(nested_key)
        if isinstance(nested, dict):
            found = find_media_id(nested)
            if found:
                return found
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Ep03 《楚氏春秋》 Google Flow i2v benchmark")
    parser.add_argument("--project", required=True, help="Existing Flow project UUID")
    parser.add_argument("--shots", default="all", help="Comma-separated shot IDs (e.g. Shot01 or Shot02,Shot03) or 'all'")
    parser.add_argument("--model", default="omni-1.2-flash", help="Flow video model")
    parser.add_argument("--duration", type=int, default=8, help="Clip duration seconds (3-15 for omni-1.2-flash)")
    parser.add_argument("--resolution", default="720p", help="Resolution flag ('360p', '720p', or 'none' to omit)")
    parser.add_argument("--aspect", default="16:9", help="Video aspect ratio")
    parser.add_argument("--max-credits", type=int, default=150, help="Per-shot pre-submit credit cap")
    parser.add_argument("--jitter", type=float, default=6.0, help="Max anti-bot pause seconds between shots")
    parser.add_argument("--upscale", action="store_true", help="Also run gflow video upscale --scale 1080p after each shot")
    parser.add_argument("--force", action="store_true", help="Re-render even if output mp4 already exists")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    shots_by_id = {s["shot_id"]: s for s in manifest["shots"]}
    target_ids = list(shots_by_id.keys()) if args.shots == "all" else [s.strip() for s in args.shots.split(",") if s.strip()]

    RENDERS_DIR.mkdir(parents=True, exist_ok=True)
    UPSCALED_DIR.mkdir(parents=True, exist_ok=True)
    metrics = load_metrics()
    metrics["project_id"] = args.project
    metrics["model"] = args.model
    metrics["duration_requested"] = args.duration
    metrics["resolution_requested"] = args.resolution

    for idx, shot_id in enumerate(target_ids):
        if shot_id not in shots_by_id:
            raise KeyError(f"Unknown shot_id: {shot_id}")
        shot = shots_by_id[shot_id]
        first_frame = ASSETS_DIR / shot["first_frame"]
        if not first_frame.exists():
            raise FileNotFoundError(f"Missing first frame: {first_frame}")

        out_mp4 = RENDERS_DIR / f"{shot_id.lower()}_raw.mp4"
        if out_mp4.exists() and out_mp4.stat().st_size > 100_000 and not args.force:
            print(f"[SKIP] {shot_id} already exists: {out_mp4} ({out_mp4.stat().st_size} bytes)")
            continue

        if idx > 0 and args.jitter > 0:
            pause = round(random.uniform(max(2.0, args.jitter * 0.6), args.jitter), 2)
            print(f"[JITTER] Sleeping {pause}s before {shot_id}...", flush=True)
            time.sleep(pause)

        prompt_text = SHOT_PROMPTS[shot_id]["prompt"]
        cmd = [
            "gflow",
            "video",
            "i2v",
            "--initial-frame",
            str(first_frame),
            "--aspect",
            args.aspect,
            "--model",
            args.model,
            "--duration",
            str(args.duration),
            "--count",
            "1",
            "--max-credits",
            str(args.max_credits),
            "--project",
            args.project,
            "--out-file",
            str(out_mp4),
            "-o",
            "json",
            prompt_text,
        ]
        if args.resolution.lower() != "none":
            cmd.extend(["--resolution", args.resolution])

        print(f"[RUN] {shot_id} -> {out_mp4.name} (model={args.model}, dur={args.duration}s, res={args.resolution})", flush=True)
        t0 = time.monotonic()
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        elapsed = round(time.monotonic() - t0, 2)

        payload = extract_json_payload(proc.stdout)
        media_id = find_media_id(payload)
        probe = run_ffprobe(out_mp4)

        record: dict[str, Any] = {
            "shot_id": shot_id,
            "first_frame": str(first_frame),
            "out_file": str(out_mp4),
            "resolution_flag": args.resolution,
            "returncode": proc.returncode,
            "elapsed_sec": elapsed,
            "media_id": media_id,
            "json_payload": payload,
            "ffprobe": probe,
            "stdout_tail": proc.stdout[-1200:],
            "stderr_tail": proc.stderr[-1200:],
        }
        metrics["shots"][shot_id] = record
        save_metrics(metrics)

        print(
            f"[DONE] {shot_id} rc={proc.returncode} elapsed={elapsed}s media_id={media_id} size={probe.get('size_bytes')}",
            flush=True,
        )

        if proc.returncode != 0:
            if proc.returncode in NO_AUTO_RETRY_EXIT_CODES:
                print(f"[ABORT] Non-retryable exit code {proc.returncode} on {shot_id}; stopping cleanly.", flush=True)
            return proc.returncode

        if args.upscale and media_id:
            up_t0 = time.monotonic()
            up_cmd = [
                "gflow",
                "video",
                "upscale",
                media_id,
                "--scale",
                "1080p",
                "--project",
                args.project,
                "--out",
                str(UPSCALED_DIR),
            ]
            up_proc = subprocess.run(up_cmd, capture_output=True, text=True, check=False)
            up_elapsed = round(time.monotonic() - up_t0, 2)
            metrics["upscales"][shot_id] = {
                "media_id": media_id,
                "returncode": up_proc.returncode,
                "elapsed_sec": up_elapsed,
                "stdout_tail": up_proc.stdout[-800:],
                "stderr_tail": up_proc.stderr[-800:],
            }
            save_metrics(metrics)
            print(f"[UPSCALE] {shot_id} rc={up_proc.returncode} elapsed={up_elapsed}s", flush=True)
            if up_proc.returncode in NO_AUTO_RETRY_EXIT_CODES:
                print(f"[WARN] Upscale returned {up_proc.returncode}; skipping auto-retry.", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
