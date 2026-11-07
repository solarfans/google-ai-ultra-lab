#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remote Batch Render Script for Chu Shi Chun Qiu Short Drama on Colab G4.
Renders Shot 01, Shot 03, Shot 04, and Shot 05 in a single G4 container session.
Uses pure safetensors UNet loading (bypasses PEFT/torchao compatibility issues).
"""

import sys
import subprocess
import os
import time
import base64

# Silence tqdm and huggingface verbose progress bars completely
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TQDM_DISABLE"] = "1"

print("==================================================")
print("🎬 [REMOTE G4] 楚氏春秋·外传章 - 批量分镜画格渲染启动")
print("==================================================")

# 1. Check and install dependencies
try:
    import diffusers
    import transformers
    import safetensors
except ImportError:
    print("[REMOTE G4] 正在安装 diffusers, transformers, accelerate, safetensors...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-q",
        "diffusers==0.32.2", "transformers", "accelerate", "safetensors"
    ])
    import diffusers
    import transformers
    import safetensors

import torch
from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

# 2. Check Device
if torch.cuda.is_available():
    gpu_name = torch.cuda.get_device_name(0)
    vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"⚡ 检测到顶级 GPU: {gpu_name} ({vram:.2f} GB 显存)")
else:
    print("❌ 未检测到 CUDA GPU!", file=sys.stderr)
    sys.exit(1)

# 3. Model Configuration: Direct UNet Loading (Bypasses PEFT/torchao)
base_repo = "stabilityai/stable-diffusion-xl-base-1.0"
repo = "ByteDance/SDXL-Lightning"
ckpt = "sdxl_lightning_4step_unet.safetensors"

t_load0 = time.time()
print(f"📦 正在装载 SDXL-Lightning 4-Step 原生 UNet ({ckpt})...")
unet_path = hf_hub_download(repo, ckpt)
unet = UNet2DConditionModel.from_config(base_repo, subfolder="unet").to("cuda", torch.float16)
unet.load_state_dict(load_file(unet_path))

print(f"📦 正在装配 SDXL-Base 全链路 Pipeline (VAE / Text Encoders)...")
pipe = StableDiffusionXLPipeline.from_pretrained(
    base_repo,
    unet=unet,
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")

# 4. Sampler configuration for trailing timesteps
pipe.scheduler = EulerDiscreteScheduler.from_config(
    pipe.scheduler.config,
    timestep_spacing="trailing"
)
print(f"✅ 模型装载完成，显存锁定完毕，总计耗时: {time.time() - t_load0:.2f} 秒")

# 5. Shot Batch Definitions (Shots 01, 03, 04, 05)
BATCH_SHOTS = [
    {
        "id": "shot01",
        "title": "Shot 01: 太监仓皇跪报",
        "filename": "shot01_eunuch_panic.png",
        "prompt": (
            "A cinematic medium shot inside a lavish Han dynasty imperial study room. "
            "In the center, a panicked 20-year-old palace eunuch wearing blood-stained azure silk robes "
            "stumbles and falls to his knees onto a red carpet, pointing trembling hands toward the heavy dark palace doors. "
            "In the background, a bronze incense burner on a carved wooden table emitting faint curls of smoke. "
            "Distant lightning flashes through wooden latticed windows, dramatic candlelight flickering, deep shadows, "
            "stormy night, ancient palace interior, 35mm film still, masterwork, 8k resolution, photorealistic, historical drama."
        ),
        "negative_prompt": (
            "text, watermark, subtitles, English letters, blurry, deformed limbs, modern clothes, extra fingers, "
            "cartoon, distorted faces, anime, oversaturated, low quality, double faces"
        ),
        "seed": 101,
        "width": 1344,
        "height": 768,
    },
    {
        "id": "shot03",
        "title": "Shot 03: 殿门大开孔明入殿",
        "filename": "shot03_zhuge_entrance.png",
        "prompt": (
            "A cinematic wide shot inside a dark Han imperial palace hall. "
            "The heavy carved red palace doors creak wide open to a stormy night. "
            "Torrential rain pouring outside illuminated by sharp lightning flashes. "
            "Chancellor Zhuge Liang, a 54-year-old dignified scholar statesman with serene expression and subtle sorrow in his eyes, "
            "wearing a black Taoist crane robe and headdress, holding a white feather fan, calmly steps across the threshold into the hall. "
            "Flanked behind by armored imperial guards in dark iron armor holding halberds and a 22-year-old cold noblewoman "
            "in dark purple martial attire with an ancient sword at her waist. "
            "Wet stone floor reflections, atmospheric smoke, 35mm film still, masterwork, 8k resolution, photorealistic, historical drama."
        ),
        "negative_prompt": (
            "text, watermark, subtitles, English letters, blurry, modern weapons, deformed limbs, extra fingers, "
            "cartoon, distorted faces, anime, low quality"
        ),
        "seed": 303,
        "width": 1344,
        "height": 768,
    },
    {
        "id": "shot04",
        "title": "Shot 04: 君臣对峙过肩镜头",
        "filename": "shot04_confrontation_ots.png",
        "prompt": (
            "A cinematic over-the-shoulder shot (OTS) in a candlelit imperial study. "
            "In the foreground out of focus, the back and shoulder of Chancellor Zhuge Liang holding a white feather fan. "
            "In sharp focus across the massive sandalwood desk, 28-year-old Emperor Liu Shan wearing a dark imperial yellow silk robe "
            "embroidered with golden dragons slowly puts down his calligraphy brush, raising cold, sharp, mocking eyes directly into Zhuge Liang's eyes. "
            "Intense psychological tension between emperor and chancellor, flickering candlelight on dark wood, "
            "ancient Chinese palace, 35mm film still, masterwork, 8k resolution, photorealistic, historical drama."
        ),
        "negative_prompt": (
            "text, watermark, subtitles, English letters, distorted faces, blurry, deformed limbs, extra fingers, "
            "cartoon, duplicate, anime, low quality"
        ),
        "seed": 404,
        "width": 1344,
        "height": 768,
    },
    {
        "id": "shot05",
        "title": "Shot 05: 拔剑与终局阻拦",
        "filename": "shot05_sword_drawn.png",
        "prompt": (
            "A dynamic cinematic medium-close shot in a grand palace hall. "
            "A 22-year-old cold and proud Chinese noblewoman with high hair bun in dark purple martial silk furiously draws an ancient Han sword, "
            "the sharp steel blade gleaming cold silver in the flash of lightning. "
            "Beside her, 54-year-old Chancellor Zhuge Liang gently raises his white feather fan to halt her sword, "
            "his eyes closed in deep grief and resignation. "
            "Dramatic cinematic composition, flickering candlelight and rain shadows, ancient palace hall, "
            "35mm film still, masterwork, 8k resolution, photorealistic, historical drama."
        ),
        "negative_prompt": (
            "text, watermark, subtitles, English letters, extra fingers, cartoon, deformed limbs, blurry, "
            "modern clothes, distorted faces, anime, low quality"
        ),
        "seed": 505,
        "width": 1344,
        "height": 768,
    }
]

print(f"\n🎨 开始批量渲染队列，共计 {len(BATCH_SHOTS)} 个分镜画格...")
t_batch_start = time.time()

for idx, shot in enumerate(BATCH_SHOTS, 1):
    print(f"\n--- [{idx}/{len(BATCH_SHOTS)}] 正在渲染: {shot['title']} ---")
    print(f"    分辨率: {shot['width']}x{shot['height']}, 步数: 4, Seed: {shot['seed']}")
    
    generator = torch.Generator(device="cuda").manual_seed(shot["seed"])
    t_shot0 = time.time()
    
    image = pipe(
        prompt=shot["prompt"],
        negative_prompt=shot["negative_prompt"],
        width=shot["width"],
        height=shot["height"],
        num_inference_steps=4,
        guidance_scale=0.0,
        generator=generator
    ).images[0]
    
    infer_time = time.time() - t_shot0
    print(f"    ✨ 纯 GPU 推理耗时: {infer_time:.2f} 秒")
    
    # Save image in container
    output_path = f"/content/{shot['filename']}"
    image.save(output_path, "PNG")
    size_kb = os.path.getsize(output_path) / 1024
    print(f"    💾 图像已保存至 {output_path} ({size_kb:.2f} KB)")
    
    # Stream base64 with shot id
    with open(output_path, "rb") as f:
        b64_str = base64.b64encode(f.read()).decode("utf-8")
    
    print(f"===BASE64_IMAGE_START:{shot['id']}===")
    print(b64_str)
    print(f"===BASE64_IMAGE_END:{shot['id']}===")

total_batch_time = time.time() - t_batch_start
print("\n==================================================")
print(f"🎉 全部 {len(BATCH_SHOTS)} 个分镜画格批量渲染完毕！总耗时: {total_batch_time:.2f} 秒")
print(f"🏁 [REMOTE G4] 任务圆满完成，即将释放 GPU 容器")
print("==================================================")
