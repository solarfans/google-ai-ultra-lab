#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remote Render Script for Shot 02: Liu Shan Portrait on Colab G4.
Executes inside Colab G4 container with pure safetensors UNet loading (no PEFT/torchao issues).
"""

import sys
import subprocess
import os
import time
import base64

print("==================================================")
print("🎬 [REMOTE G4] 楚氏春秋·外传章 - Shot 02 刘禅御书房定妆生成")
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
print(f"📦 正在下载并装载 SDXL-Lightning 4-Step 原生 UNet ({ckpt})...")
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
print(f"✅ 模型与调度器装载完成，显存锁定完毕，总计耗时: {time.time() - t_load0:.2f} 秒")

# 5. Prompt Specifications from chu_shi_chun_qiu_ep01.json
prompt = (
    "A cinematic solo portrait of a 28-year-old Chinese emperor, single male, centered in frame, "
    "sitting calmly alone behind a massive dark sandalwood desk in a lavish Han dynasty imperial study, "
    "holding a calligraphy brush in his right hand, writing effortlessly without looking up, showing zero panic. "
    "Sharp calm facial features, intense eyes showing hidden ambition, wearing a traditional dark imperial yellow silk robe "
    "embroidered with golden dragons. Dramatic cinematic candlelight and shadows, flickering flame reflections, "
    "ancient Chinese palace architecture, 35mm film still, highly detailed, masterwork, 8k resolution, "
    "photorealistic, historical drama."
)
negative_prompt = (
    "two people, duplicate, twins, multiple persons, double, split screen, side by side, clone, "
    "text, watermark, subtitles, English letters, blurry, deformed limbs, modern clothes, extra fingers, "
    "cartoon, distorted faces, anime, oversaturated, unrealistic lighting"
)

width = 1344
height = 768
steps = 4
guidance_scale = 0.0
seed = 42
generator = torch.Generator(device="cuda").manual_seed(seed)

print(f"🎨 开始画格渲染: 分辨率 {width}x{height}, 步数 {steps}, Seed {seed}, CFG=0.0...")
t_infer0 = time.time()
image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    width=width,
    height=height,
    num_inference_steps=steps,
    guidance_scale=guidance_scale,
    generator=generator
).images[0]
infer_time = time.time() - t_infer0
print(f"✨ 渲染完成！纯 GPU 推理耗时: {infer_time:.2f} 秒")

# 6. Save and Stream
output_path = "/content/shot02_liushan_portrait.png"
image.save(output_path, "PNG")
size_kb = os.path.getsize(output_path) / 1024
print(f"💾 图像已保存至 {output_path} ({size_kb:.2f} KB, 分辨率: {image.size})")

with open(output_path, "rb") as f:
    b64_str = base64.b64encode(f.read()).decode("utf-8")

print("===BASE64_IMAGE_START===")
print(b64_str)
print("===BASE64_IMAGE_END===")
print(f"🏁 [REMOTE G4] 任务圆满完成，即将释放 GPU 容器")
