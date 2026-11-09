#!/usr/bin/env python3
"""Gate 2 Automated Single-Shot 10s AI Manju MVP Renderer on Colab G4 (96GB Blackwell).

Executes the《楚氏春秋》第一章《北赵楚氏》opening 10-second 3D Guoman CG shot
(`minimax_h3_manju_mvp_10s.json`) on a fresh Colab G4 VM with zero Drive FUSE dependency,
streams the rendered H.264+AAC MP4 back to local disk, and exits so `colab run` immediately
releases the G4 instance (Zero-Burn SOP compliant).
"""

from __future__ import annotations

import base64
import glob
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import urllib.error
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
            print(f"⚡ Model already present: {fname}", flush=True)
            continue
        lines.append(f"{url}\n  dir={dest_dir}\n  out={fname}\n")

    if not lines:
        return

    aria_input = Path("/tmp/aria2_hf_models.txt")
    aria_input.write_text("".join(lines), encoding="utf-8")
    print("🚀 [Thread-A] Pulling 42.3 GB MiniMax-H3 weights from HF CDN to local NVMe via aria2c...", flush=True)
    sh(
        f"aria2c -i {aria_input} -j 5 -x 16 -s 16 -k 16M "
        "--file-allocation=none --continue=true --console-log-level=warn --summary-interval=15"
    )
    print(f"🔥 [Thread-A] All 5 MiniMax-H3 weights staged on NVMe in {time.time() - t0:.1f}s!", flush=True)


def setup_comfy_and_assets() -> None:
    t0 = time.time()
    print("🚀 [Thread-B] Setting up ComfyUI + custom nodes + Gate 1 assets...", flush=True)
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
        if item.is_file():
            shutil.copy2(item, in_dir / item.name)
            print(f"  📥 Staged input asset: {item.name} ({item.stat().st_size / 1024:.1f} KB)", flush=True)

    pkgs = "gguf imageio-ffmpeg librosa soundfile tiktoken sentencepiece sox accelerate einops scipy av"
    sh(
        f"if command -v uv >/dev/null 2>&1; then "
        f"uv pip install --system -q -r {COMFY_DIR}/requirements.txt {pkgs}; "
        f"else pip install -q -r {COMFY_DIR}/requirements.txt {pkgs}; fi"
    )
    print(f"✅ [Thread-B] ComfyUI environment + assets ready in {time.time() - t0:.1f}s!", flush=True)


def main() -> None:
    t_start = time.time()
    print("=== [Gate 2] Checking GPU Hardware ===", flush=True)
    print(sh("nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader").strip(), flush=True)

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

    print("=== [Gate 2] Starting ComfyUI Server (--highvram --disable-mmap --fast) ===", flush=True)
    comfy_log = open("/tmp/comfyui.log", "w")
    proc = subprocess.Popen(
        [
            "python3",
            "main.py",
            "--listen",
            "127.0.0.1",
            "--port",
            "8188",
            "--highvram",
            "--disable-mmap",
            "--fast",
        ],
        cwd=str(COMFY_DIR),
        stdout=comfy_log,
        stderr=subprocess.STDOUT,
    )

    server_up = False
    for _ in range(90):
        time.sleep(1.0)
        try:
            urllib.request.urlopen("http://127.0.0.1:8188/system_stats", timeout=2)
            server_up = True
            break
        except Exception:
            pass
    if not server_up:
        log_tail = Path("/tmp/comfyui.log").read_text(errors="ignore")[-2000:]
        raise RuntimeError(f"ComfyUI failed to start:\n{log_tail}")

    print(f"✅ ComfyUI online at T+{time.time() - t_start:.1f}s! Submitting minimax_h3_manju_mvp_10s.json...", flush=True)
    wf_path = REPO_DIR / "pipelines/short_drama/workflows/minimax_h3_manju_mvp_10s.json"
    prompt_graph = json.loads(wf_path.read_text(encoding="utf-8"))

    req = urllib.request.Request(
        "http://127.0.0.1:8188/prompt",
        data=json.dumps({"prompt": prompt_graph}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp_data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode("utf-8"))
    except urllib.error.HTTPError as he:
        err_body = he.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"ComfyUI prompt validation failed ({he.code}): {err_body}") from he

    prompt_id = resp_data["prompt_id"]
    print(f"🎬 Queued prompt_id={prompt_id}. Monitoring execution...", flush=True)

    t_render = time.time()
    last_log_len = 0
    while True:
        time.sleep(3.0)
        if Path("/tmp/comfyui.log").exists():
            cur_log = Path("/tmp/comfyui.log").read_text(errors="ignore")
            if len(cur_log) > last_log_len:
                new_chunk = cur_log[last_log_len:]
                last_log_len = len(cur_log)
                for line in new_chunk.splitlines():
                    if any(k in line for k in ("%|", "Prompt executed", "Error", "Exception", "Traceback", "Loading", "Requested")):
                        print(f"  [ComfyUI] {line[-140:]}", flush=True)

        hist_raw = urllib.request.urlopen(f"http://127.0.0.1:8188/history/{prompt_id}", timeout=5).read().decode("utf-8")
        hist = json.loads(hist_raw)
        if prompt_id in hist:
            status = hist[prompt_id].get("status", {})
            if status.get("status_str") == "error":
                log_tail = Path("/tmp/comfyui.log").read_text(errors="ignore")[-3000:]
                raise RuntimeError(f"ComfyUI execution error: {status}\nLog:\n{log_tail}")
            print(f"🎉 Render completed in {time.time() - t_render:.1f}s!", flush=True)
            break

    mp4_files = sorted(glob.glob(str(COMFY_DIR / "output" / "ChuShiChunQiu_Manju_MVP_10s*.mp4")), key=os.path.getmtime)
    if not mp4_files:
        mp4_files = sorted(glob.glob(str(COMFY_DIR / "output" / "*.mp4")), key=os.path.getmtime)
    if not mp4_files:
        raise RuntimeError("No output MP4 found in /content/ComfyUI/output/!")

    final_mp4 = Path(mp4_files[-1])
    sz_mb = final_mp4.stat().st_size / (1024**2)
    print(f"✅ Output MP4 verified: {final_mp4} ({sz_mb:.2f} MB)", flush=True)
    probe = sh(
        f"ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,channels,sample_rate "
        f"-show_entries format=duration -of json {final_mp4}"
    )
    print(f"📊 FFprobe metadata:\n{probe}", flush=True)

    b64_str = base64.b64encode(final_mp4.read_bytes()).decode("ascii")
    print("===BEGIN_MP4_B64===", flush=True)
    for idx in range(0, len(b64_str), 76):
        print(b64_str[idx : idx + 76], flush=True)
    print("===END_MP4_B64===", flush=True)

    proc.terminate()
    print(f"🏁 Total Gate 2 G4 session time: {time.time() - t_start:.1f}s. Releasing G4 VM now.", flush=True)


if __name__ == "__main__":
    main()
