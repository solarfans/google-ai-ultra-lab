#!/usr/bin/env python3
"""Single-Session G4 Batch Renderer for Episode 3《楚氏春秋·第三章 颠倒乾坤》(Shots 01–06).

Executes all 6 shots of Episode 3 in ONE single Colab G4 session:
- 1x cold start (~175s) amortized across 6 shots
- 0s model reload for Shots 02–06 (`--highvram --disable-mmap --fast`)
- 6-step Turbo schedule + deduplicated reference tokens (~205s per shot)
- Hard per-shot timeout (`MAX_SHOT_WAIT_SEC = 420.0`) and `try...finally` teardown
"""

from __future__ import annotations

import base64
import glob
import json
import os
import shutil
import subprocess
import threading
import time
import urllib.request
from pathlib import Path

COMFY_DIR = Path("/content/ComfyUI")
REPO_DIR = Path("/content/google-ai-ultra-lab")

HF_MODELS = [
    (
        "diffusion_models",
        "Minimax-h3_Singularity_ref2va_Pruned_v1.3_int8.safetensors",
        "https://huggingface.co/WarmBloodAban/Minimax-h3_Singularity/resolve/main/Minimax-h3_Singularity_ref2va_Pruned_v1.3_int8.safetensors",
    ),
    (
        "text_encoders",
        "qwen3vl_32b_heretic_minimax_h3_nvfp4.safetensors",
        "https://huggingface.co/Momoking/Qwen3-VL-32B-Heretic-MiniMax-H3-NVFP4/resolve/main/qwen3vl_32b_heretic_minimax_h3_nvfp4.safetensors",
    ),
    (
        "vae",
        "minimax_h3_video_vae_fp16.safetensors",
        "https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_video_vae_fp16.safetensors",
    ),
    (
        "vae",
        "minimax_h3_audio_vae_fp32.safetensors",
        "https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_audio_vae_fp32.safetensors",
    ),
    (
        "loras",
        "minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors",
        "https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/loras/minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors",
    ),
]

SHOT_JOBS = [
    ("Ep03_Shot01", "compiled_ep03_shot01.json", "manju_ep03_shot01_tea_dragon"),
    ("Ep03_Shot02", "compiled_ep03_shot02.json", "manju_ep03_shot02_xueyu_pact"),
    ("Ep03_Shot03", "compiled_ep03_shot03.json", "manju_ep03_shot03_dropped_bowl"),
    ("Ep03_Shot04", "compiled_ep03_shot04.json", "manju_ep03_shot04_father_rejoice"),
    ("Ep03_Shot05", "compiled_ep03_shot05.json", "manju_ep03_shot05_secret_sect"),
    ("Ep03_Shot06", "compiled_ep03_shot06.json", "manju_ep03_shot06_diandao_qiankun"),
]

MAX_SHOT_WAIT_SEC = 420.0
MAX_BOOT_WAIT_SEC = 120


def sh(cmd: str, check: bool = True) -> str:
    print(f"🔧 $ {cmd}", flush=True)
    p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if p.returncode != 0:
        print(f"⚠️ rc={p.returncode}: {p.stderr[-800:]}", flush=True)
        if check:
            raise RuntimeError(f"Command failed (rc={p.returncode}): {cmd}")
    return p.stdout


def download_hf_models() -> None:
    t0 = time.time()
    lines = []
    for subdir, fname, url in HF_MODELS:
        dest_dir = COMFY_DIR / "models" / subdir
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / fname
        if dest_file.exists() and dest_file.stat().st_size > 100_000_000:
            continue
        lines.append(f"{url}\n  dir={dest_dir}\n  out={fname}\n")
    if not lines:
        return
    aria_input = Path("/tmp/aria2_hf_models.txt")
    aria_input.write_text("".join(lines), encoding="utf-8")
    print("🚀 [Thread-A] Pulling 42.3 GB MiniMax-H3 weights from HF CDN to local NVMe...", flush=True)
    sh(
        f"aria2c -i {aria_input} -j 5 -x 16 -s 16 -k 16M "
        "--file-allocation=none --continue=true --console-log-level=warn --summary-interval=15"
    )
    print(f"🔥 [Thread-A] All 5 MiniMax-H3 weights staged on NVMe in {time.time() - t0:.1f}s!", flush=True)


def setup_comfy_and_assets() -> None:
    t0 = time.time()
    cn_dir = COMFY_DIR / "custom_nodes"
    cn_dir.mkdir(parents=True, exist_ok=True)
    sh(
        f"git clone --depth 1 -q https://github.com/NikoDemon80/ComfyUI-H3-Motion-Context.git {cn_dir}/ComfyUI-H3-Motion-Context && "
        f"git clone --depth 1 -q https://github.com/aa335615543-ux/BUNNY_H3_Conditioning_Bridge.git {cn_dir}/BUNNY_H3_Conditioning_Bridge"
    )
    bunny_models = cn_dir / "BUNNY_H3_Conditioning_Bridge" / "models"
    bunny_models.mkdir(parents=True, exist_ok=True)
    sh(
        f"aria2c -x 8 -s 8 -d {bunny_models} -o BUNNY_H3_ActionLogic_Bridge_V2.safetensors "
        "https://huggingface.co/JOKER141/BUNNY_H3_Conditioning_Bridge/resolve/main/BUNNY_H3_ActionLogic_Bridge_V2.safetensors"
    )
    if REPO_DIR.exists():
        shutil.rmtree(REPO_DIR)
    sh(f"git clone --depth 1 -q https://github.com/solarfans/google-ai-ultra-lab.git {REPO_DIR}")

    in_dir = COMFY_DIR / "input"
    in_dir.mkdir(parents=True, exist_ok=True)
    assets_src = REPO_DIR / "pipelines/short_drama/assets_manju_v2"
    for item in assets_src.iterdir():
        if item.is_file() and (item.suffix in (".png", ".wav")):
            shutil.copy2(item, in_dir / item.name)
            print(f"  📥 Staged input asset: {item.name}", flush=True)

    pkgs = "gguf imageio-ffmpeg librosa soundfile tiktoken sentencepiece sox accelerate einops scipy av"
    sh(
        f"if command -v uv >/dev/null 2>&1; then "
        f"uv pip install --system -q -r {COMFY_DIR}/requirements.txt {pkgs}; "
        f"else pip install -q -r {COMFY_DIR}/requirements.txt {pkgs}; fi"
    )
    print(f"✅ [Thread-B] ComfyUI environment + assets ready in {time.time() - t0:.1f}s!", flush=True)


def run_single_shot(shot_id: str, wf_fname: str, out_prefix: str) -> None:
    t_shot = time.time()
    wf_path = REPO_DIR / "pipelines/short_drama/workflows" / wf_fname
    prompt_graph = json.loads(wf_path.read_text(encoding="utf-8"))

    req = urllib.request.Request(
        "http://127.0.0.1:8188/prompt",
        data=json.dumps({"prompt": prompt_graph}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    resp_data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode("utf-8"))
    prompt_id = resp_data["prompt_id"]
    print(f"\n🎬 [{shot_id}] Queued prompt_id={prompt_id} ({wf_fname})...", flush=True)

    last_log_len = Path("/tmp/comfyui.log").stat().st_size if Path("/tmp/comfyui.log").exists() else 0
    while True:
        elapsed = time.time() - t_shot
        if elapsed > MAX_SHOT_WAIT_SEC:
            raise TimeoutError(
                f"[{shot_id}] Hard timeout exceeded ({elapsed:.1f}s > {MAX_SHOT_WAIT_SEC}s)! Aborting to protect CU."
            )
        time.sleep(2.5)
        if Path("/tmp/comfyui.log").exists():
            cur_log = Path("/tmp/comfyui.log").read_text(errors="ignore")
            if len(cur_log) > last_log_len:
                new_chunk = cur_log[last_log_len:]
                last_log_len = len(cur_log)
                for line in new_chunk.splitlines():
                    if any(k in line for k in ("%|", "Prompt executed", "Error", "Exception", "Traceback")):
                        print(f"  [{shot_id}] {line[-140:]}", flush=True)

        hist = json.loads(urllib.request.urlopen(f"http://127.0.0.1:8188/history/{prompt_id}", timeout=5).read().decode("utf-8"))
        if prompt_id in hist:
            status = hist[prompt_id].get("status", {})
            if status.get("status_str") == "error":
                log_tail = Path("/tmp/comfyui.log").read_text(errors="ignore")[-3000:]
                raise RuntimeError(f"[{shot_id}] ComfyUI error: {status}\n{log_tail}")
            print(f"🎉 [{shot_id}] Render completed in {time.time() - t_shot:.1f}s!", flush=True)
            break

    mp4_files = sorted(glob.glob(str(COMFY_DIR / "output" / f"{out_prefix}*.mp4")), key=os.path.getmtime)
    if not mp4_files:
        raise RuntimeError(f"[{shot_id}] Missing output MP4 for prefix {out_prefix}!")
    final_mp4 = Path(mp4_files[-1])
    print(f"✅ [{shot_id}] Output verified: {final_mp4.name} ({final_mp4.stat().st_size / (1024**2):.2f} MB)", flush=True)

    b64_str = base64.b64encode(final_mp4.read_bytes()).decode("ascii")
    print(f"===BEGIN_MP4_{shot_id}===", flush=True)
    for idx in range(0, len(b64_str), 76):
        print(b64_str[idx : idx + 76], flush=True)
    print(f"===END_MP4_{shot_id}===", flush=True)


def main() -> None:
    t_start = time.time()
    print("=== [Ep03 Batch G4] Checking Hardware ===", flush=True)
    print(sh("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader").strip(), flush=True)
    sh("apt-get update -qq && apt-get install -y -qq aria2 ffmpeg sox libsox-fmt-all")
    if not (COMFY_DIR / "main.py").exists():
        sh(f"git clone --depth 1 -q https://github.com/comfyanonymous/ComfyUI.git {COMFY_DIR}")

    errs: list[Exception] = []

    def _run_dl() -> None:
        try:
            download_hf_models()
        except Exception as e:
            errs.append(e)

    t_dl = threading.Thread(target=_run_dl, daemon=True)
    t_dl.start()
    setup_comfy_and_assets()
    t_dl.join()
    if errs:
        raise RuntimeError(f"Model download failed: {errs[0]}") from errs[0]

    comfy_log = open("/tmp/comfyui.log", "w")
    proc = subprocess.Popen(
        ["python3", "main.py", "--listen", "127.0.0.1", "--port", "8188", "--highvram", "--disable-mmap", "--fast"],
        cwd=str(COMFY_DIR),
        stdout=comfy_log,
        stderr=subprocess.STDOUT,
    )

    try:
        readiness_ok = False
        for _ in range(MAX_BOOT_WAIT_SEC):
            if proc.poll() is not None:
                log_tail = Path("/tmp/comfyui.log").read_text(errors="ignore")[-2000:]
                raise RuntimeError(f"ComfyUI exited prematurely during boot (rc={proc.returncode}):\n{log_tail}")
            time.sleep(1.0)
            try:
                urllib.request.urlopen("http://127.0.0.1:8188/system_stats", timeout=2)
                readiness_ok = True
                break
            except Exception:
                pass

        if not readiness_ok:
            log_tail = Path("/tmp/comfyui.log").read_text(errors="ignore")[-2000:]
            raise TimeoutError(f"ComfyUI failed readiness check after {MAX_BOOT_WAIT_SEC}s:\n{log_tail}")

        print(
            f"✅ ComfyUI online at T+{time.time() - t_start:.1f}s! Executing {len(SHOT_JOBS)}-shot Ep03 batch queue...",
            flush=True,
        )
        for shot_id, wf_fname, out_prefix in SHOT_JOBS:
            run_single_shot(shot_id, wf_fname, out_prefix)

        print(
            f"\n🏁 All {len(SHOT_JOBS)} shots of Episode 3 rendered in {time.time() - t_start:.1f}s total! Releasing G4 VM.",
            flush=True,
        )
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
        comfy_log.close()


if __name__ == "__main__":
    main()
