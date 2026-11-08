#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate 9-Year-Old Noble Boy Window Scene for Shot 06 on Colab G4.
Strictly ensures 9yo child stature, royal blue silk robes, open window, ancient city & cavalry.
"""

import sys
import os
import time
import base64
import torch
import subprocess

print("==================================================")
print("🎬 [COLAB G4] 生成 Shot 06: 9岁小世子推窗放眼十万大军")
print("🔥 彻底消除成年人变异，锁定 9 岁幼童身形与王孙贵气")
print("==================================================")

# Install required packages if missing
required = ["diffusers", "transformers", "accelerate", "safetensors", "pillow"]
missing = [p for p in required if not __import__("pkgutil").find_loader(p)]
if missing:
    print(f"📦 安装依赖: {missing}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + missing)

from diffusers import AutoPipelineForText2Image, DPMSolverMultistepScheduler
from PIL import Image

print(f"⚡ GPU: {torch.cuda.get_device_name(0)} (显存: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB)")

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
).to("cuda")

pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config,
    use_karras_sigmas=True
)

prompt = (
    "Cinematic 35mm film still of a 9-year-old noble Chinese boy prince Chu Zheng standing beside an open carved dark sandalwood window inside an ancient palace room. "
    "He has a cute 9-year-old child face, petite child stature, small delicate hands resting on the window ledge, topknot hairstyle with a small jade hairpin. "
    "Wearing an exquisite royal blue silk Chinese robe with shimmering gold brocade collar and cuffs. "
    "He looks out sideways toward the majestic sprawling ancient capital city of Pingyuan under golden morning mist: "
    "towering vermilion fortress walls, fluttering battle flags, marching armored cavalry patrols and horsemen in the distance. "
    "Master historical drama cinematography, beautiful sidelighting, natural skin texture, 8k resolution, photorealistic."
)

negative_prompt = (
    "adult, man, mature, tall, beard, mustache, 20 years old, 30 years old, teenager, "
    "modern clothes, skyscrapers, cars, deformed limbs, blurry, text, watermark, subtitles, cartoon, cgi, 3d render"
)

# Generate with seeds
seeds = [2026110831, 2026110832, 2026110833]
for idx, s in enumerate(seeds):
    print(f"🎨 [Seed {s}] 正在生成 1344x768 电影级画格...")
    generator = torch.Generator(device="cuda").manual_seed(s)
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=1344,
        height=768,
        num_inference_steps=25,
        guidance_scale=7.5,
        generator=generator
    ).images[0]
    
    out_path = f"/tmp/shot06_boy_candidate_{idx}.png"
    image.save(out_path)
    b64 = base64.b64encode(open(out_path, "rb").read()).decode("utf-8")
    print(f"B64_KEYFRAME_CANDIDATE_{idx}_START")
    print(b64)
    print(f"B64_KEYFRAME_CANDIDATE_{idx}_END")

print("✅ 全部画格生成完毕！")
del pipe
torch.cuda.empty_cache()
