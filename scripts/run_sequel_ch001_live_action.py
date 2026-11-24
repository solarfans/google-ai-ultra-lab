#!/usr/bin/env python3
"""Closed-loop Live-Action Chinese Historical Cinema runner for 《楚氏春秋》 Sequel CH001.

Adapts `novel-continuation-lab/books/chushi-chunqiu/accepted/CH001.md` (《第001章 杯散之后》,
100% adult cast) via Google Flow (`gflow-cli`):
  - Stage `actors`: 3 photorealistic casting portraits (`nano2.1` t2i, 3:4)
  - Stage `plates`: 6 multi-ref 16:9 cinema keyframe plates (`nano2.1` i2i)
  - Stage `videos`: 6 10s 720p live-action cinema clips (`omni-1.2-flash` i2v)

Enforces `--count 1` and `--max-credits`, never auto-retries WAF/refusal exit codes
(`10`, `22`, `23`, `36`, `45`), and records per-step wall-clock timings, media IDs,
and ffprobe telemetry in `pipelines/short_drama/sequel_ch001_live_action/metrics.json`.
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
WORK_DIR = BASE_DIR / "pipelines" / "short_drama" / "sequel_ch001_live_action"
ACTORS_DIR = WORK_DIR / "actors"
PLATES_DIR = WORK_DIR / "plates"
RENDERS_DIR = WORK_DIR / "renders"
METRICS_PATH = WORK_DIR / "metrics.json"

NO_AUTO_RETRY_EXIT_CODES = {10, 22, 23, 36, 45}

ACTORS: dict[str, dict[str, str]] = {
    "chuzheng": {
        "file": "actor_chuzheng.jpg",
        "prompt": (
            "Photorealistic live-action film casting portrait, 26-year-old handsome East Asian Chinese male actor (Chu Zheng), "
            "sharp intelligent dark eyes, calm subtly smiling aristocratic expression, natural human skin texture with realistic pores, "
            "traditional Song-Ming dynasty dark teal-black (玄青) silk robe with subtle dark-silver cloud embroidery, "
            "white jade hair crown, neutral warm gray studio backdrop, even neutral white studio key lighting, "
            "shot on ARRI Alexa 65 85mm lens, strictly photorealistic real human actor, zero anime, zero 3D CG, no text."
        ),
    },
    "chuxuan": {
        "file": "actor_chuxuan.jpg",
        "prompt": (
            "Photorealistic live-action film casting portrait, 32-year-old stern aristocratic East Asian Chinese male actor (Chu Xuan), "
            "sharp chiseled jawline, calculating deep-set eyes, neatly trimmed subtle noble facial hair, natural human skin texture, "
            "deep burgundy-plum (深绛紫) embroidered heavy silk robe with dark bronze belt clasp, "
            "ornate gold filigree hair crown, neutral warm gray studio backdrop, even neutral white studio key lighting, "
            "shot on ARRI Alexa 65 85mm lens, strictly photorealistic real human actor, zero anime, zero 3D CG, no text."
        ),
    },
    "ningxiaoxian": {
        "file": "actor_ningxiaoxian.jpg",
        "prompt": (
            "Photorealistic live-action film casting portrait, 27-year-old graceful poised East Asian Chinese actress (Ning Xiaoxian), "
            "refined noble oval face, cool calm intelligent eyes with a hint of weariness, natural skin texture, "
            "moon-white (月白) woven silk cloak with fur-trimmed collar over pale celadon silk inner robe, "
            "understated jade and silver hairpin, neutral warm gray studio backdrop, even neutral white studio key lighting, "
            "shot on ARRI Alexa 65 85mm lens, strictly photorealistic real human actress, zero anime, zero 3D CG, no text."
        ),
    },
}

CINEMA_STYLE_LOCK = (
    "Shot on ARRI Alexa 65 anamorphic lens, shallow depth of field, warm amber paper lantern key light "
    "against deep midnight indigo courtyard shadows, wet dark stone pavement, realistic film grain, "
    "strictly photorealistic live-action Chinese historical TV drama aesthetic like Longest Day in Chang'an "
    "and Brotherhood of Blades, zero anime, zero CGI, zero text, zero watermark."
)

PLATES: dict[str, dict[str, Any]] = {
    "Shot01": {
        "file": "plate_shot01.jpg",
        "refs": ["actor_chuzheng.jpg", "actor_chuxuan.jpg"],
        "prompt": (
            f"{CINEMA_STYLE_LOCK} "
            "Medium two-shot outside a traditional Chinese wooden tavern at night under warm swaying red paper lanterns and wet cobblestone street; "
            "Chu Zheng (from first ref, right, dark teal-black silk robe with white jade crown) stepping over the wooden threshold "
            "facing his older brother Chu Xuan (from second ref, left, deep burgundy-plum silk robe with gold filigree crown) "
            "waiting calmly under the eaves, completely sober, subtle tension in their eyes."
        ),
    },
    "Shot02": {
        "file": "plate_shot02.jpg",
        "refs": ["actor_chuzheng.jpg", "actor_chuxuan.jpg"],
        "prompt": (
            f"{CINEMA_STYLE_LOCK} "
            "Tight cinematic medium two-shot under the lantern-lit wooden tavern eaves with dark saddled horse silhouettes in the misty street background; "
            "Chu Xuan (from second ref, on left, burgundy-plum silk robe) glancing sidelong with a faint cold smile, "
            "Chu Zheng (from first ref, on right, dark teal-black silk robe) answering with calm amused composure, dramatic chiaroscuro lantern lighting."
        ),
    },
    "Shot03": {
        "file": "plate_shot03.jpg",
        "refs": ["actor_ningxiaoxian.jpg"],
        "prompt": (
            f"{CINEMA_STYLE_LOCK} "
            "Inside a quiet night courtyard of an ancient county yamen, warm amber candlelight spilling from an open carved wooden chamber doorway; "
            "Ning Xiaoxian (from ref, 27-year-old graceful actress in moon-white silk cloak with fur collar) stands framed in the glowing doorway, "
            "hands clasped tightly in front of her, weary yet piercingly composed gaze toward camera."
        ),
    },
    "Shot04": {
        "file": "plate_shot04.jpg",
        "refs": ["actor_chuxuan.jpg", "actor_chuzheng.jpg"],
        "prompt": (
            f"{CINEMA_STYLE_LOCK} "
            "Night yamen courtyard outside freshly closed dark carved wooden chamber doors, warm interior light now shut away leaving only dim swaying courtyard lanterns; "
            "Chu Xuan (from first ref, on left, burgundy-plum silk robe) gazes toward the shut door in three-quarter profile, "
            "while Chu Zheng (from second ref, on right, dark teal-black silk robe) stands a pace away with calm guarded poise."
        ),
    },
    "Shot05": {
        "file": "plate_shot05.jpg",
        "refs": ["actor_chuzheng.jpg", "actor_chuxuan.jpg"],
        "prompt": (
            f"{CINEMA_STYLE_LOCK} "
            "Urgent night yamen courtyard scene under flickering amber lanterns; "
            "a nervous 45-year-old Chinese county prefect in dark green embroidered Song-Ming official robe hurriedly bows in the left foreground "
            "holding up a mud-stained urgent dispatch scroll, while Chu Zheng (from first ref, center, dark teal-black robe) "
            "and Chu Xuan (from second ref, right, burgundy-plum robe) look on intently."
        ),
    },
    "Shot06": {
        "file": "plate_shot06.jpg",
        "refs": ["actor_chuzheng.jpg", "actor_chuxuan.jpg"],
        "prompt": (
            f"{CINEMA_STYLE_LOCK} "
            "Intimate cinematic close-up two-shot in the blue-black night courtyard; "
            "Chu Xuan (from second ref, right, burgundy-plum robe) leans in slightly reaching a steady hand toward a small fallen dark locust leaf "
            "resting on the left shoulder of Chu Zheng (from first ref, left, dark teal-black robe), "
            "warm lantern rim light illuminating both actors' intensely nuanced real faces."
        ),
    },
}

VIDEO_LOCK = (
    "Strictly clean photorealistic live-action film footage matching the initial frame, "
    "ZERO burned-in subtitles, ZERO on-screen captions, ZERO text overlays, ZERO background music."
)

VIDEOS: dict[str, dict[str, str]] = {
    "Shot01": {
        "file": "shot01_raw.mp4",
        "plate": "plate_shot01.jpg",
        "subtitle": "楚轩：小五，你连酒楼掌柜的生意也管？ / 楚铮：父亲叫我少惹是非，只好拿灯笼练练手。",
        "prompt": (
            f"{VIDEO_LOCK} "
            "Tavern eaves at night, warm red paper lanterns swaying in a cool breeze, natural subtle camera push-in. "
            "First, Chu Xuan on the left looks at his younger brother with a faint cool smile and speaks in a calm aristocratic Mandarin baritone with natural lip-sync: "
            "\"小五，你连酒楼掌柜的生意也管？\" "
            "Then Chu Zheng on the right steps down the wooden threshold with an effortless smile and replies in a crisp young adult Mandarin voice with natural lip-sync: "
            "\"父亲叫我少惹是非，如今只好拿灯笼练练手。\" "
            "Authentic night breeze, wooden step, and silk robe Foley sound."
        ),
    },
    "Shot02": {
        "file": "shot02_raw.mp4",
        "plate": "plate_shot02.jpg",
        "subtitle": "楚轩：回京路上，南线鹰堂的人不必跟着小仙了。 / 楚铮：轻如在鹰堂有规矩，回京我难免挨数落。",
        "prompt": (
            f"{VIDEO_LOCK} "
            "Tight lantern-lit cinematic medium two-shot under the tavern eaves, subtle handheld film breathing, distant horse snort in misty street. "
            "First, Chu Xuan on the left says evenly in a measured aristocratic Mandarin baritone with natural lip-sync: "
            "\"回京路上，南线鹰堂的人，就不必再跟着小仙了。\" "
            "Then Chu Zheng on the right smiles politely yet firmly, replying in a calm poised young adult Mandarin voice with natural lip-sync: "
            "\"轻如在鹰堂里有规矩，叫他们明日走人，回京我难免挨数落。\" "
            "Authentic distant horse snort and quiet night street Foley sound."
        ),
    },
    "Shot03": {
        "file": "shot03_raw.mp4",
        "plate": "plate_shot03.jpg",
        "subtitle": "宁小仙：若遇上山匪，夫君人马自然护我；若不是山匪，多几名高手又有何用？",
        "prompt": (
            f"{VIDEO_LOCK} "
            "Warm candlelight doorway in the quiet night courtyard, gentle slow push-in toward Ning Xiaoxian. "
            "The night breeze stirs her moon-white silk cloak; her clasped knuckles tighten slightly in front of her, "
            "and she looks steadily ahead speaking calmly yet icily in a dignified, weary Mandarin female voice with exact natural lip-sync: "
            "\"若遇上山匪，夫君的人马自然会护着我。若遇上的不是山匪，多几名高手又有何用？\" "
            "Quiet night courtyard wind and soft silk cloak rustle Foley sound."
        ),
    },
    "Shot04": {
        "file": "shot04_raw.mp4",
        "plate": "plate_shot04.jpg",
        "subtitle": "楚轩：小仙今日劳累，外头的事有劳五弟。 / 楚铮：总不能让嫂嫂一路听着刀剑响。",
        "prompt": (
            f"{VIDEO_LOCK} "
            "Night courtyard outside the closed wooden doors, swaying lantern shadows, subtle cinematic tracking move. "
            "First, Chu Xuan gazes briefly at the shut chamber door, then turns calmly to Chu Zheng with cool courtesy and speaks in a refined Mandarin baritone with natural lip-sync: "
            "\"小仙今日劳累，外头的事，有劳五弟处置。\" "
            "Then Chu Zheng bows slightly with a faint dry smile and replies in a calm composed Mandarin voice with natural lip-sync: "
            "\"总不能让嫂嫂一路听着刀剑响。\" "
            "Quiet courtyard night wind and soft footstep Foley sound."
        ),
    },
    "Shot05": {
        "file": "shot05_raw.mp4",
        "plate": "plate_shot05.jpg",
        "subtitle": "刘海：汝西县城外发现男尸，疑遭劫杀！ / 楚轩：倒是巧了……这便有了人命。",
        "prompt": (
            f"{VIDEO_LOCK} "
            "Urgent night courtyard scene under flickering amber lanterns, tense slow push-in. "
            "First, the nervous county prefect on the left bows anxiously holding up the mud-stained dispatch scroll and speaks urgently in a strained middle-aged Mandarin voice with natural lip-sync: "
            "\"知府急报！汝西县城外发现一具男尸，疑是遭匪人劫杀！\" "
            "Chu Zheng's gaze cools subtly as Chu Xuan on the right glances sideways at him with a cold knowing smirk and speaks in a low incisive Mandarin baritone with natural lip-sync: "
            "\"倒是巧了……这便有了人命。\" "
            "Paper scroll rustle and urgent courtyard Foley sound."
        ),
    },
    "Shot06": {
        "file": "shot06_raw.mp4",
        "plate": "plate_shot06.jpg",
        "subtitle": "楚铮：大哥，小弟今日竟叫你操心了。 / 楚轩：自家兄弟，何须客气。",
        "prompt": (
            f"{VIDEO_LOCK} "
            "Dramatic slow push-in cinematic close-up in blue-amber night courtyard light. "
            "Chu Xuan gently brushes a fallen dark locust leaf off Chu Zheng's left shoulder and straightens his collar. "
            "Chu Zheng smiles faintly and speaks in a calm guarded Mandarin voice with natural lip-sync: "
            "\"大哥，小弟今日竟叫你操心了。\" "
            "Chu Xuan replies in a low intimate Mandarin baritone with natural lip-sync: "
            "\"自家兄弟，何须客气。\" "
            "The camera holds for the final second on Chu Zheng's cool, watchful eyes as he stares after his brother. "
            "Soft silk cloth brush and quiet night breeze Foley sound."
        ),
    },
}


def extract_json_payload(stdout: str) -> dict[str, Any] | None:
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


def find_media_id(payload: dict[str, Any] | None) -> str | None:
    if not payload:
        return None
    for key in ("media_id", "mediaId", "video_id", "id", "asset_id"):
        val = payload.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    for nested_key in ("result", "video", "media", "data", "image"):
        nested = payload.get(nested_key)
        if isinstance(nested, dict):
            found = find_media_id(nested)
            if found:
                return found
    return None


def run_ffprobe(media_path: Path) -> dict[str, Any]:
    if not media_path.exists():
        return {"exists": False}
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(media_path)],
        capture_output=True,
        text=True,
        check=False,
    )
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
        "duration_sec": round(float(fmt.get("duration", 0.0)), 3) if fmt.get("duration") else None,
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
        "benchmark_name": "ChuShiChunQiu Sequel CH001 Live-Action (Google Flow) vs Legacy Colab Manju",
        "source_chapter": "novel-continuation-lab/books/chushi-chunqiu/accepted/CH001.md",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "prior_3d_manju_probe": {
            "shot01_8s_720p_elapsed_sec": 119.41,
            "shot01_credits_spent": 24,
            "shot01_upscale_1080p_rc": 15,
            "shot01_upscale_error": "BrowserSessionClosedError / TargetClosedError",
            "shot02_minor_filter_rc": 1,
            "shot02_minor_filter_error": "Flow failed the generation (code 3): PUBLIC_ERROR_MINOR",
        },
        "actors": {},
        "plates": {},
        "videos": {},
    }


def save_metrics(metrics: dict[str, Any]) -> None:
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    metrics["updated_at_utc"] = datetime.now(timezone.utc).isoformat()
    METRICS_PATH.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def jitter_sleep(idx: int, jitter: float, label: str) -> None:
    if idx > 0 and jitter > 0:
        pause = round(random.uniform(max(2.0, jitter * 0.6), jitter), 2)
        print(f"[JITTER] Sleeping {pause}s before {label}...", flush=True)
        time.sleep(pause)


def run_gflow(cmd: list[str]) -> tuple[int, float, dict[str, Any] | None, str, str]:
    t0 = time.monotonic()
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    elapsed = round(time.monotonic() - t0, 2)
    payload = extract_json_payload(proc.stdout)
    return proc.returncode, elapsed, payload, proc.stdout[-1200:], proc.stderr[-1200:]


def stage_actors(project_id: str, targets: list[str], jitter: float, force: bool, metrics: dict[str, Any]) -> int:
    ACTORS_DIR.mkdir(parents=True, exist_ok=True)
    keys = [k for k in ACTORS if not targets or k in targets]
    for idx, key in enumerate(keys):
        spec = ACTORS[key]
        out_path = ACTORS_DIR / spec["file"]
        if out_path.exists() and out_path.stat().st_size > 20_000 and not force:
            print(f"[SKIP] actor {key} exists: {out_path.name}", flush=True)
            continue
        jitter_sleep(idx, jitter, f"actor:{key}")
        cmd = [
            "gflow", "image", "t2i",
            "--model", "nano2.1",
            "--aspect", "3:4",
            "-n", "1",
            "--project", project_id,
            "--out-file", str(out_path),
            "-o", "json",
            spec["prompt"],
        ]
        print(f"[RUN] actor {key} -> {out_path.name}", flush=True)
        rc, elapsed, payload, out_tail, err_tail = run_gflow(cmd)
        probe = run_ffprobe(out_path)
        metrics["actors"][key] = {
            "out_file": str(out_path),
            "returncode": rc,
            "elapsed_sec": elapsed,
            "media_id": find_media_id(payload),
            "json_payload": payload,
            "ffprobe": probe,
            "stdout_tail": out_tail,
            "stderr_tail": err_tail,
        }
        save_metrics(metrics)
        print(f"[DONE] actor {key} rc={rc} elapsed={elapsed}s size={probe.get('size_bytes')}", flush=True)
        if rc != 0:
            return rc
    return 0


def stage_plates(project_id: str, targets: list[str], jitter: float, force: bool, metrics: dict[str, Any]) -> int:
    PLATES_DIR.mkdir(parents=True, exist_ok=True)
    keys = [k for k in PLATES if not targets or k in targets]
    for idx, key in enumerate(keys):
        spec = PLATES[key]
        out_path = PLATES_DIR / spec["file"]
        if out_path.exists() and out_path.stat().st_size > 20_000 and not force:
            print(f"[SKIP] plate {key} exists: {out_path.name}", flush=True)
            continue
        jitter_sleep(idx, jitter, f"plate:{key}")
        cmd = [
            "gflow", "image", "i2i",
            "--model", "nano2.1",
            "--aspect", "16:9",
            "-n", "1",
            "--project", project_id,
            "--out-file", str(out_path),
            "-o", "json",
        ]
        for ref_name in spec["refs"]:
            ref_path = ACTORS_DIR / ref_name
            if not ref_path.exists():
                raise FileNotFoundError(f"Missing actor portrait for {key}: {ref_path}")
            cmd.extend(["--ref", str(ref_path)])
        cmd.append(spec["prompt"])
        print(f"[RUN] plate {key} -> {out_path.name} (refs={spec['refs']})", flush=True)
        rc, elapsed, payload, out_tail, err_tail = run_gflow(cmd)
        probe = run_ffprobe(out_path)
        metrics["plates"][key] = {
            "out_file": str(out_path),
            "refs": spec["refs"],
            "returncode": rc,
            "elapsed_sec": elapsed,
            "media_id": find_media_id(payload),
            "json_payload": payload,
            "ffprobe": probe,
            "stdout_tail": out_tail,
            "stderr_tail": err_tail,
        }
        save_metrics(metrics)
        print(f"[DONE] plate {key} rc={rc} elapsed={elapsed}s size={probe.get('size_bytes')}", flush=True)
        if rc != 0:
            return rc
    return 0


def stage_videos(
    project_id: str,
    targets: list[str],
    model: str,
    duration: int,
    resolution: str,
    max_credits: int,
    jitter: float,
    force: bool,
    metrics: dict[str, Any],
) -> int:
    RENDERS_DIR.mkdir(parents=True, exist_ok=True)
    keys = [k for k in VIDEOS if not targets or k in targets]
    for idx, key in enumerate(keys):
        spec = VIDEOS[key]
        plate_path = PLATES_DIR / spec["plate"]
        if not plate_path.exists():
            raise FileNotFoundError(f"Missing keyframe plate for {key}: {plate_path}")
        out_path = RENDERS_DIR / spec["file"]
        if out_path.exists() and out_path.stat().st_size > 100_000 and not force:
            print(f"[SKIP] video {key} exists: {out_path.name}", flush=True)
            continue
        jitter_sleep(idx, jitter, f"video:{key}")
        cmd = [
            "gflow", "video", "i2v",
            "--initial-frame", str(plate_path),
            "--aspect", "16:9",
            "--model", model,
            "--duration", str(duration),
            "--count", "1",
            "--max-credits", str(max_credits),
            "--project", project_id,
            "--out-file", str(out_path),
            "-o", "json",
            spec["prompt"],
        ]
        if resolution.lower() != "none":
            cmd.extend(["--resolution", resolution])
        print(f"[RUN] video {key} -> {out_path.name} (model={model}, dur={duration}s, res={resolution})", flush=True)
        rc, elapsed, payload, out_tail, err_tail = run_gflow(cmd)
        probe = run_ffprobe(out_path)
        metrics["videos"][key] = {
            "plate": str(plate_path),
            "out_file": str(out_path),
            "subtitle": spec["subtitle"],
            "returncode": rc,
            "elapsed_sec": elapsed,
            "media_id": find_media_id(payload),
            "json_payload": payload,
            "ffprobe": probe,
            "stdout_tail": out_tail,
            "stderr_tail": err_tail,
        }
        save_metrics(metrics)
        print(f"[DONE] video {key} rc={rc} elapsed={elapsed}s size={probe.get('size_bytes')}", flush=True)
        if rc != 0:
            if rc in NO_AUTO_RETRY_EXIT_CODES:
                print(f"[ABORT] Non-retryable exit code {rc} on {key}; stopping cleanly.", flush=True)
            return rc
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Live-Action 《楚氏春秋》 Sequel CH001 Google Flow Runner")
    parser.add_argument("--project", required=True, help="Flow project UUID")
    parser.add_argument("--stage", choices=["actors", "plates", "videos", "all"], default="all")
    parser.add_argument("--shots", default="", help="Comma-separated filter (e.g. chuzheng or Shot01 or Shot02,Shot03)")
    parser.add_argument("--model", default="omni-1.2-flash")
    parser.add_argument("--duration", type=int, default=10)
    parser.add_argument("--resolution", default="720p")
    parser.add_argument("--max-credits", type=int, default=120)
    parser.add_argument("--jitter", type=float, default=6.0)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    targets = [t.strip() for t in args.shots.split(",") if t.strip()]
    metrics = load_metrics()
    metrics["project_id"] = args.project
    metrics.setdefault("credits_before", 24836)
    save_metrics(metrics)

    if args.stage in ("actors", "all"):
        rc = stage_actors(args.project, targets, args.jitter, args.force, metrics)
        if rc != 0:
            return rc
    if args.stage in ("plates", "all"):
        rc = stage_plates(args.project, targets, args.jitter, args.force, metrics)
        if rc != 0:
            return rc
    if args.stage in ("videos", "all"):
        rc = stage_videos(
            args.project,
            targets,
            args.model,
            args.duration,
            args.resolution,
            args.max_credits,
            args.jitter,
            args.force,
            metrics,
        )
        if rc != 0:
            return rc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
