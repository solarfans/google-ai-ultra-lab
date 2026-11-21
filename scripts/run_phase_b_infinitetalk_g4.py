#!/usr/bin/env python3
"""Mac-side Zero-Burn orchestrator for Phase B InfiniteTalk on Colab G4."""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab")
COLAB_BIN = "/Users/kaykel/.local/bin/colab"
METER_PY = Path.home() / ".gemini/config/skills/google-ai-ultra/scripts/ultra_meter.py"
SESSION = "g4_infinitetalk"


def clean_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("VIRTUAL_ENV", None)
    return env


def run_cmd(cmd: list[str], timeout: int = 300) -> None:
    print(f"[LOCAL] $ {' '.join(cmd)}", flush=True)
    proc = subprocess.Popen(cmd, start_new_session=True, text=True, env=clean_env())
    try:
        rc = proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            proc.wait(timeout=5)
        except Exception:
            os.killpg(proc.pid, signal.SIGKILL)
        raise TimeoutError(f"Command exceeded wall-clock timeout {timeout}s: {' '.join(cmd)}")
    if rc != 0:
        raise RuntimeError(f"Command exited {rc}: {' '.join(cmd)}")


def query_usage() -> dict:
    out = subprocess.check_output(["python3", str(METER_PY), "usage", "--json"], text=True, env=clean_env())
    return json.loads(out)["usage"]


def main() -> int:
    before = query_usage()
    bal_before = float(before["balance"])
    active_before = int(before["active"])
    print(f"[PRE-FLIGHT] balance={bal_before:.2f} CU | active={active_before}", flush=True)
    if bal_before < 150.0:
        print(f"ABORT: balance {bal_before:.2f} < 150.0 CU floor", file=sys.stderr)
        return 3
    if active_before > 0:
        print("ABORT: unexpected active Colab session exists; stop-all first", file=sys.stderr)
        return 3

    anchor_local = ROOT / "pipelines/ai_explainer_ep01/outputs/anchor_832x480.png"
    audio_local = ROOT / "pipelines/ai_explainer_ep01/audio_en/ep01_en_v2_brian_dry.wav"
    worker_local = ROOT / "scripts/g4_infinitetalk_worker.py"
    out_local = ROOT / "pipelines/ai_explainer_ep01/outputs/avatar_en_v2_brian_832x480.mp4"
    out_local.parent.mkdir(parents=True, exist_ok=True)

    assert anchor_local.is_file(), f"Missing {anchor_local}"
    assert audio_local.is_file(), f"Missing {audio_local}"
    assert worker_local.is_file(), f"Missing {worker_local}"

    t0 = time.time()
    try:
        run_cmd([COLAB_BIN, "new", "--gpu", "G4", "-s", SESSION], timeout=180)
        run_cmd([COLAB_BIN, "upload", "-s", SESSION, str(anchor_local), "/content/input_anchor.png"], timeout=120)
        run_cmd([COLAB_BIN, "upload", "-s", SESSION, str(audio_local), "/content/input_audio.wav"], timeout=120)
        run_cmd([COLAB_BIN, "exec", "-s", SESSION, "-f", str(worker_local), "--timeout", "600"], timeout=2100)
        run_cmd([COLAB_BIN, "download", "-s", SESSION, "/content/avatar_en_v2_brian_832x480.mp4", str(out_local)], timeout=180)
    finally:
        print("[TEARDOWN] Executing guaranteed ultra_meter.py stop-all...", flush=True)
        subprocess.run(["python3", str(METER_PY), "stop-all", "--quota-wait", "8"], env=clean_env(), check=False)

    after = query_usage()
    bal_after = float(after["balance"])
    active_after = int(after["active"])
    cu_used = max(0.0, bal_before - bal_after)
    elapsed = time.time() - t0
    print(
        f"[POST-FLIGHT] elapsed={elapsed:.1f}s ({elapsed/60:.2f}m) | before={bal_before:.2f} | "
        f"after={bal_after:.2f} | consumed={cu_used:.2f} CU | active={active_after} | file={out_local}",
        flush=True,
    )
    if active_after != 0:
        print("WARNING: active_after != 0!", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
