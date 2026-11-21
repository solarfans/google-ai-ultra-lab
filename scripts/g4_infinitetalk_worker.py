#!/usr/bin/env python3
"""Colab G4 (96GB Blackwell) remote worker for InfiniteTalk I2V talking avatar."""
from __future__ import annotations

import glob
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

COMFY_DIR = Path("/content/ComfyUI")
LOG_FILE = Path("/tmp/comfyui_g4.log")
PORT = 8188


def run(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    print(f"[G4] $ {cmd}", flush=True)
    return subprocess.run(cmd, shell=True, check=check)


def patch_wav2vec_transformers5() -> None:
    nodes_py = COMFY_DIR / "custom_nodes/ComfyUI-WanVideoWrapper/multitalk/nodes.py"
    if not nodes_py.is_file():
        return
    txt = nodes_py.read_text(encoding="utf-8")
    target = "embeddings = wav2vec2(audio_feature.to(dtype), seq_len=int(video_length), output_hidden_states=True)"
    if target not in txt or "G4_HF5_HOOK_PATCH" in txt:
        return
    replacement = """# G4_HF5_HOOK_PATCH
            _captured_hs = []
            _hooks = []
            if hasattr(wav2vec2, "encoder") and hasattr(wav2vec2.encoder, "layers"):
                for _lyr in wav2vec2.encoder.layers:
                    _hooks.append(_lyr.register_forward_hook(lambda _m, _i, _o: _captured_hs.append(_o[0] if isinstance(_o, tuple) else _o)))
            embeddings = wav2vec2(audio_feature.to(dtype), seq_len=int(video_length), output_hidden_states=True)
            for _hk in _hooks:
                _hk.remove()
            if getattr(embeddings, "hidden_states", None) is None and _captured_hs:
                embeddings.hidden_states = [None] + _captured_hs"""
    nodes_py.write_text(txt.replace(target, replacement, 1), encoding="utf-8")
    print("[G4] Patched multitalk/nodes.py for transformers 5.x hidden_states safety", flush=True)


def download_weights() -> None:
    models = COMFY_DIR / "models"
    specs = [
        (
            "diffusion_models/Wan2_1-I2V-14B-480p_fp8_e4m3fn_scaled_KJ.safetensors",
            "https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/I2V/Wan2_1-I2V-14B-480p_fp8_e4m3fn_scaled_KJ.safetensors",
        ),
        (
            "diffusion_models/Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors",
            "https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/InfiniteTalk/Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors",
        ),
        (
            "wav2vec2/wav2vec2-chinese-base_fp16.safetensors",
            "https://huggingface.co/Kijai/wav2vec2_safetensors/resolve/main/wav2vec2-chinese-base_fp16.safetensors",
        ),
        (
            "text_encoders/umt5-xxl-enc-fp8_e4m3fn.safetensors",
            "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors",
        ),
        (
            "loras/lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors",
            "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors",
        ),
        (
            "vae/Wan2_1_VAE_bf16.safetensors",
            "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1_VAE_bf16.safetensors",
        ),
        (
            "clip_vision/clip_vision_h.safetensors",
            "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors",
        ),
    ]
    for rel_path, url in specs:
        dest = models / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.is_file() and dest.stat().st_size > 1_000_000:
            print(f"[G4] Cached {rel_path} ({dest.stat().st_size / 1e6:.1f} MB)", flush=True)
            continue
        t0 = time.time()
        cmd = (
            f'aria2c -x 16 -s 16 --file-allocation=none --console-log-level=warn '
            f'--summary-interval=15 -d "{dest.parent}" -o "{dest.name}" "{url}"'
        )
        run(cmd)
        print(f"[G4] Downloaded {rel_path} ({dest.stat().st_size / 1e6:.1f} MB in {time.time() - t0:.1f}s)", flush=True)


def http_json(url: str, payload: dict | None = None, timeout: int = 30) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def node_defaults(info: dict, class_type: str) -> dict:
    spec = info.get(class_type)
    if not spec:
        raise RuntimeError(f"Missing ComfyUI node {class_type} in /object_info")
    inputs: dict = {}
    for section in ("required", "optional"):
        for name, desc in spec.get("input", {}).get(section, {}).items():
            if not isinstance(desc, list) or not desc:
                continue
            first = desc[0]
            meta = desc[1] if len(desc) > 1 and isinstance(desc[1], dict) else {}
            if "default" in meta:
                inputs[name] = meta["default"]
            elif isinstance(first, list) and first:
                inputs[name] = first[0]
            elif first == "INT":
                inputs[name] = meta.get("min", 0)
            elif first == "FLOAT":
                inputs[name] = float(meta.get("min", 0.0))
            elif first == "BOOLEAN":
                inputs[name] = False
            elif first == "STRING":
                inputs[name] = ""
    return inputs


def first_matching_key(d: dict, candidates: list[str], fallback_idx: int = 0) -> str:
    for c in candidates:
        if c in d:
            return c
    return list(d.keys())[fallback_idx]


def build_prompt(info: dict, num_frames: int) -> dict:
    prompt: dict = {}

    # 1. VAE Loader
    d = node_defaults(info, "WanVideoVAELoader")
    k = first_matching_key(d, ["model_name", "vae_name"])
    d[k] = "Wan2_1_VAE_bf16.safetensors"
    if "precision" in d:
        d["precision"] = "bf16"
    prompt["1"] = {"class_type": "WanVideoVAELoader", "inputs": d}

    # 2. CLIP Vision Loader
    d = node_defaults(info, "CLIPVisionLoader")
    k = first_matching_key(d, ["clip_name"])
    d[k] = "clip_vision_h.safetensors"
    prompt["2"] = {"class_type": "CLIPVisionLoader", "inputs": d}

    # 3. LightX2V LoRA Select (optional/extra safety)
    d = node_defaults(info, "WanVideoLoraSelect")
    k = first_matching_key(d, ["lora", "lora_name"])
    d[k] = "lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors"
    if "strength" in d:
        d["strength"] = 1.0
    if "low_mem_load" in d:
        d["low_mem_load"] = False
    if "merge_loras" in d:
        d["merge_loras"] = False
    prompt["3"] = {"class_type": "WanVideoLoraSelect", "inputs": d}

    # 4. MultiTalk Model Loader
    d = node_defaults(info, "MultiTalkModelLoader")
    d["model"] = "Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors"
    prompt["4"] = {"class_type": "MultiTalkModelLoader", "inputs": d}

    # 5. WanVideo Main Model Loader (96GB G4 -> main_device, no block swap, sdpa)
    d = node_defaults(info, "WanVideoModelLoader")
    d["model"] = "Wan2_1-I2V-14B-480p_fp8_e4m3fn_scaled_KJ.safetensors"
    if "base_precision" in d:
        d["base_precision"] = "bf16"
    if "quantization" in d:
        d["quantization"] = "disabled"
    if "load_device" in d:
        d["load_device"] = "main_device"
    if "attention_mode" in d:
        d["attention_mode"] = "sdpa"
    d["lora"] = ["3", 0]
    d["multitalk_model"] = ["4", 0]
    prompt["5"] = {"class_type": "WanVideoModelLoader", "inputs": d}

    # 6. Wav2Vec Model Loader
    d = node_defaults(info, "Wav2VecModelLoader")
    d["model"] = "wav2vec2-chinese-base_fp16.safetensors"
    if "base_precision" in d:
        d["base_precision"] = "fp16"
    if "load_device" in d:
        d["load_device"] = "main_device"
    prompt["6"] = {"class_type": "Wav2VecModelLoader", "inputs": d}

    # 7. Text Encode Cached
    d = node_defaults(info, "WanVideoTextEncodeCached")
    d["model_name"] = "umt5-xxl-enc-fp8_e4m3fn.safetensors"
    if "precision" in d:
        d["precision"] = "bf16"
    d["positive_prompt"] = (
        "speaking naturally and expressively toward the camera, natural eye contact, "
        "subtle blinks, expressive eyebrow and head movement matching speech cadence, "
        "dark minimalist studio lighting, charcoal shirt"
    )
    d["negative_prompt"] = (
        "static frozen face, stiff mouth, distorted teeth, warped face, blurry, "
        "morphing, low quality, extra hands, distorted eyes"
    )
    if "quantization" in d:
        d["quantization"] = "disabled"
    if "use_disk_cache" in d:
        d["use_disk_cache"] = False
    if "device" in d:
        d["device"] = "gpu"
    prompt["7"] = {"class_type": "WanVideoTextEncodeCached", "inputs": d}

    # 8. LoadImage
    d = node_defaults(info, "LoadImage")
    d["image"] = "input_anchor.png"
    prompt["8"] = {"class_type": "LoadImage", "inputs": d}

    # 9. CLIP Vision Encode
    d = node_defaults(info, "WanVideoClipVisionEncode")
    d["clip_vision"] = ["2", 0]
    d["image_1"] = ["8", 0]
    if "strength_1" in d:
        d["strength_1"] = 1.0
    if "strength_2" in d:
        d["strength_2"] = 1.0
    if "force_offload" in d:
        d["force_offload"] = True
    prompt["9"] = {"class_type": "WanVideoClipVisionEncode", "inputs": d}

    # 10. LoadAudio
    d = node_defaults(info, "LoadAudio")
    d["audio"] = "input_audio.wav"
    prompt["10"] = {"class_type": "LoadAudio", "inputs": d}

    # 11. MultiTalkWav2VecEmbeds
    d = node_defaults(info, "MultiTalkWav2VecEmbeds")
    d["wav2vec_model"] = ["6", 0]
    d["audio_1"] = ["10", 0]
    d["normalize_loudness"] = True
    d["num_frames"] = num_frames
    d["fps"] = 25.0
    d["audio_scale"] = 1.0
    d["audio_cfg_scale"] = 1.0
    d["multi_audio_type"] = "para"
    prompt["11"] = {"class_type": "MultiTalkWav2VecEmbeds", "inputs": d}

    # 12. WanVideoImageToVideoMultiTalk
    d = node_defaults(info, "WanVideoImageToVideoMultiTalk")
    d["vae"] = ["1", 0]
    d["start_image"] = ["8", 0]
    d["clip_embeds"] = ["9", 0]
    d["width"] = 832
    d["height"] = 480
    d["frame_window_size"] = 81
    d["motion_frame"] = 9
    if "force_offload" in d:
        d["force_offload"] = False
    if "colormatch" in d:
        d["colormatch"] = "mkl"
    if "tiled_vae" in d:
        d["tiled_vae"] = False
    if "mode" in d:
        d["mode"] = "infinitetalk"
    prompt["12"] = {"class_type": "WanVideoImageToVideoMultiTalk", "inputs": d}

    # 13. WanVideoSampler
    d = node_defaults(info, "WanVideoSampler")
    d["model"] = ["5", 0]
    d["image_embeds"] = ["12", 0]
    d["text_embeds"] = ["7", 0]
    d["multitalk_embeds"] = ["11", 0]
    d["steps"] = 6
    d["cfg"] = 1.0
    d["shift"] = 11.0
    d["seed"] = 42
    if "force_offload" in d:
        d["force_offload"] = False
    if "scheduler" in d:
        d["scheduler"] = "dpm++_sde"
    prompt["13"] = {"class_type": "WanVideoSampler", "inputs": d}

    # 14. WanVideoPassImagesFromSamples (MultiTalk loop already outputs decoded IMAGE in samples!)
    d = node_defaults(info, "WanVideoPassImagesFromSamples")
    d["samples"] = ["13", 0]
    prompt["14"] = {"class_type": "WanVideoPassImagesFromSamples", "inputs": d}

    # 15. VHS_VideoCombine
    d = node_defaults(info, "VHS_VideoCombine")
    d["images"] = ["14", 0]
    d["audio"] = ["11", 1]
    d["frame_rate"] = 25
    d["loop_count"] = 0
    d["filename_prefix"] = "avatar_en_v2_brian"
    d["format"] = "video/h264-mp4"
    d["pix_fmt"] = "yuv420p"
    d["crf"] = 18
    d["save_output"] = True
    if "trim_to_audio" in d:
        d["trim_to_audio"] = True
    prompt["15"] = {"class_type": "VHS_VideoCombine", "inputs": d}

    return prompt


def main() -> int:
    t_start = time.time()
    run("nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv")
    run('python3 -c "import torch, transformers; print(\'torch:\', torch.__version__, \'cuda:\', torch.cuda.is_available(), \'transformers:\', transformers.__version__)"')

    assert Path("/content/input_anchor.png").is_file(), "Missing /content/input_anchor.png"
    assert Path("/content/input_audio.wav").is_file(), "Missing /content/input_audio.wav"

    audio_dur = float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", "/content/input_audio.wav"],
            text=True,
        ).strip()
    )
    num_frames = int(math.ceil(audio_dur * 25.0)) + 16
    print(f"[G4] Input audio duration: {audio_dur:.3f}s -> target num_frames={num_frames} @ 25fps", flush=True)

    run("command -v aria2c >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq aria2 >/dev/null)")

    if not COMFY_DIR.exists():
        run(f"git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git {COMFY_DIR}")
    cn = COMFY_DIR / "custom_nodes"
    cn.mkdir(parents=True, exist_ok=True)
    repos = {
        "ComfyUI-WanVideoWrapper": "https://github.com/kijai/ComfyUI-WanVideoWrapper.git",
        "ComfyUI-KJNodes": "https://github.com/kijai/ComfyUI-KJNodes.git",
        "ComfyUI-VideoHelperSuite": "https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git",
    }
    for name, url in repos.items():
        if not (cn / name).exists():
            run(f'git clone --depth 1 "{url}" "{cn / name}"')

    # Install only non-torch dependencies so existing CUDA PyTorch stays intact
    req_pkgs: list[str] = []
    skip_pat = re.compile(r"^(torch|torchvision|torchaudio|xformers|flash[-_]attn|triton|bitsandbytes)\b", re.I)
    for req_file in [
        COMFY_DIR / "requirements.txt",
        cn / "ComfyUI-WanVideoWrapper/requirements.txt",
        cn / "ComfyUI-KJNodes/requirements.txt",
        cn / "ComfyUI-VideoHelperSuite/requirements.txt",
    ]:
        if req_file.is_file():
            for ln in req_file.read_text(errors="ignore").splitlines():
                ln = ln.split("#", 1)[0].strip()
                if not ln or ln.startswith("-") or skip_pat.match(ln):
                    continue
                req_pkgs.append(ln)
    filtered_req = Path("/tmp/g4_req_filtered.txt")
    filtered_req.write_text("\n".join(sorted(set(req_pkgs))) + "\n", encoding="utf-8")
    run(f"pip install --progress-bar off -r {filtered_req} color-matcher pyloudnorm imageio-ffmpeg librosa soundfile ftfy")

    patch_wav2vec_transformers5()
    download_weights()

    (COMFY_DIR / "input").mkdir(parents=True, exist_ok=True)
    shutil.copy2("/content/input_anchor.png", COMFY_DIR / "input/input_anchor.png")
    shutil.copy2("/content/input_audio.wav", COMFY_DIR / "input/input_audio.wav")

    # Start ComfyUI headless in background
    log_fp = open(LOG_FILE, "w", encoding="utf-8")
    proc = subprocess.Popen(
        [sys.executable, "main.py", "--listen", "127.0.0.1", "--port", str(PORT), "--highvram", "--disable-mmap"],
        cwd=str(COMFY_DIR),
        stdout=log_fp,
        stderr=subprocess.STDOUT,
    )
    try:
        info = None
        for _ in range(90):
            if proc.poll() is not None:
                print(LOG_FILE.read_text(errors="ignore")[-4000:], flush=True)
                raise RuntimeError(f"ComfyUI exited early with code {proc.returncode}")
            try:
                info = http_json(f"http://127.0.0.1:{PORT}/object_info", timeout=10)
                if "WanVideoSampler" in info and "VHS_VideoCombine" in info:
                    break
            except Exception:
                pass
            time.sleep(2)
        if not info or "WanVideoSampler" not in info:
            print(LOG_FILE.read_text(errors="ignore")[-4000:], flush=True)
            raise RuntimeError("Timed out waiting for ComfyUI /object_info")

        print("[G4] ComfyUI ready! Building InfiniteTalk workflow...", flush=True)
        prompt = build_prompt(info, num_frames=num_frames)
        res = http_json(f"http://127.0.0.1:{PORT}/prompt", payload={"prompt": prompt, "client_id": "agy_g4"})
        prompt_id = res["prompt_id"]
        print(f"[G4] Submitted prompt_id={prompt_id}", flush=True)

        last_log_len = 0
        t_infer = time.time()
        while True:
            if proc.poll() is not None:
                print(LOG_FILE.read_text(errors="ignore")[-5000:], flush=True)
                raise RuntimeError(f"ComfyUI crashed during execution (code {proc.returncode})")

            # Stream new ComfyUI log lines every 15s to keep colab exec heartbeat alive
            log_txt = LOG_FILE.read_text(errors="ignore")
            if len(log_txt) > last_log_len:
                delta = log_txt[last_log_len:].strip()
                if delta:
                    for line in delta.splitlines()[-8:]:
                        print(f"[ComfyUI] {line}", flush=True)
                last_log_len = len(log_txt)

            hist = http_json(f"http://127.0.0.1:{PORT}/history/{prompt_id}", timeout=15)
            if prompt_id in hist:
                entry = hist[prompt_id]
                status = entry.get("status", {})
                if status.get("status_str") == "error":
                    print(json.dumps(status, indent=2), flush=True)
                    print(LOG_FILE.read_text(errors="ignore")[-5000:], flush=True)
                    raise RuntimeError("ComfyUI execution failed")
                outputs = entry.get("outputs", {})
                if outputs:
                    print(f"[G4] Inference complete in {time.time() - t_infer:.1f}s!", flush=True)
                    break
            else:
                print(f"[G4] Generating... elapsed={time.time() - t_infer:.0f}s", flush=True)
            time.sleep(15)

        out_files = sorted(glob.glob(str(COMFY_DIR / "output/avatar_en_v2_brian*.mp4")), key=os.path.getmtime)
        if not out_files:
            out_files = sorted(glob.glob(str(COMFY_DIR / "output/**/*.mp4"), recursive=True), key=os.path.getmtime)
        assert out_files, f"No output mp4 found! Log tail:\n{LOG_FILE.read_text(errors='ignore')[-3000:]}"

        raw_mp4 = out_files[-1]
        final_mp4 = "/content/avatar_en_v2_brian_832x480.mp4"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                raw_mp4,
                "-t",
                f"{audio_dur:.3f}",
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-crf",
                "17",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                final_mp4,
            ],
            check=True,
        )
        run(f'ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height,r_frame_rate -of default=nw=1 "{final_mp4}"')
        print(f"[G4] SUCCESS! Total G4 elapsed={time.time() - t_start:.1f}s | output={final_mp4}", flush=True)
        return 0
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        log_fp.close()


if __name__ == "__main__":
    raise SystemExit(main())
