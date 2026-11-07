#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remote G4 Execution Script for 《楚氏春秋·正传第一卷：杯底波澜》
Stage 1: Generates 6 authentic Han Dynasty keyframes via full SDXL 1.0 (25-30 steps).
Stage 2: Generates 6 real dynamic 3D video clips via Stable Video Diffusion (SVD-XT) on 96GB GPU.
Stage 3: Streams base64 encoded PNGs and MP4 clips back to local orchestrator.
"""

import sys
import subprocess
import os
import time
import base64
from pathlib import Path

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TQDM_DISABLE"] = "1"

print("==================================================")
print("🎬 [REMOTE G4] 楚氏春秋·正传第一卷：杯底波澜 - 工业级视频与画格渲染")
print("==================================================")

# 1. Install required packages
try:
    import diffusers
    import transformers
    import safetensors
    import accelerate
    import imageio
except ImportError:
    print("[REMOTE G4] 正在安装必要驱动与依赖库 (diffusers, accelerate, imageio)...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-q",
        "diffusers==0.32.2", "transformers", "accelerate", "safetensors", "imageio[ffmpeg]"
    ])
    import diffusers
    import transformers
    import safetensors
    import imageio

import torch
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler, StableVideoDiffusionPipeline
from PIL import Image

# 2. Check GPU Device
if not torch.cuda.is_available():
    print("❌ 未检测到 CUDA GPU! 必须在 GPU 实例上执行", file=sys.stderr)
    sys.exit(1)

gpu_name = torch.cuda.get_device_name(0)
vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
print(f"⚡ 检测到顶级云端 GPU: {gpu_name} ({vram:.2f} GB 显存)")

# 3. Shot Specifications for Chapter 1
SHOTS = [
    {
        "id": "shot01",
        "title": "来兮楼夜宴·玉杯清碰",
        "prompt": "Extreme macro close-up of two exquisite Chinese mutton-fat white jade wine cups clinking together, a drop of clear amber wine splashing in mid-air. Blurred background of a grand ancient Han-dynasty banquet hall, glowing warm crimson silk lanterns, autumn night candlelight reflections. 35mm film still, master cinematic lighting, 8k resolution.",
        "negative_prompt": "text, watermark, subtitles, English letters, blurry, deformed fingers, glass cups, modern clothes",
        "seed": 4201,
        "motion_bucket": 110,
    },
    {
        "id": "shot02",
        "title": "来兮楼主案·五公子发难",
        "prompt": "A handsome 24-year-old Chinese noble warrior general Chu Zheng with sharp aristocratic features, slight sardonic cold smirk, intense dark eyes harboring ruthless intellect, leaning casually back against dark carved banquet table, long finger tapping rim of jade cup. Dressed in authentic Han-dynasty black silk tailored robe (Xuan-Yi) with subtle dark gold trim, dark hair in noble knot. Dramatic warm candlelight casting sharp shadows, ultra-photorealistic, 8k.",
        "negative_prompt": "Japanese, samurai, kimono, katana, elderly, beard, woman, modern clothes, deformed face, cartoon",
        "seed": 4202,
        "motion_bucket": 125,
    },
    {
        "id": "shot03",
        "title": "宴席跪拜·战将请罪",
        "prompt": "A burly 42-year-old battle-hardened Chinese commander Jia Dao with full black beard, rugged weathered face drenched in nervous oily sweat, kneeling deeply on crimson banquet carpet before imperial table, hands trembling in fear. Wearing authentic Han-dynasty iron lamellar scale armor, bronze tiger pauldron. Tense atmosphere, cinematic realism.",
        "negative_prompt": "Japanese, samurai, kimono, clean-shaven, smiling, relaxed, modern clothes, cartoon",
        "seed": 4203,
        "motion_bucket": 105,
    },
    {
        "id": "shot04",
        "title": "宴席上座·长公子调和",
        "prompt": "An elegant 28-year-old Chinese aristocratic statesman Chu Xuan with gentle refined face, calm inscrutable eyes like deep fathomless water, subtle composed smile concealing intense ambition, holding a slender white jade wine pitcher and pouring wine. Wearing authentic Han jade-green wide-sleeved silk robe (Shenyi) with white jade crown. Soft warm banquet candlelight, dignified imperial poise, 8k resolution.",
        "negative_prompt": "Japanese, kimono, samurai, anger, warrior, armor, beard, woman, modern clothes, cartoon",
        "seed": 4204,
        "motion_bucket": 115,
    },
    {
        "id": "shot05",
        "title": "深夜黑漆马车·兄弟机锋",
        "prompt": "Inside an ancient heavy black-lacquered horse carriage at night, dimly illuminated by glowing red charcoal embers in a small bronze brazier. Chu Zheng leaning near window curtain, his sharp cold profile highlighted in deep red charcoal glow, staring with mocking fierce eyes at his brother across the low desk. Heavy tension, cinematic masterpiece.",
        "negative_prompt": "Japanese, modern interior, electric lights, bright colors, deformed face, cartoon",
        "seed": 4205,
        "motion_bucket": 120,
    },
    {
        "id": "shot06",
        "title": "幽暗驿馆·长剑出鞘",
        "prompt": "Inside a dim ancient courtyard room lit only by cold silver moonlight through carved lattice window. Young general Chu Zheng standing tall in black cape, gripping a meteorite black-iron Han straight sword, drawing it half an inch from its ornate scabbard, the cold steel blade reflecting a sharp beam of light across his eyes. Dark cinematic atmosphere, dynamic.",
        "negative_prompt": "Japanese katana, samurai, bright daylight, kimono, modern weapons, deformed hands, cartoon",
        "seed": 4206,
        "motion_bucket": 135,
    }
]

# 4. Stage 1: Render High-Fidelity Keyframes via SDXL Base 1.0
t0 = time.time()
print("\n📦 [STAGE 1] 装配 SDXL-Base 1.0 生成正传正统汉代定妆画格...")
sdxl_repo = "stabilityai/stable-diffusion-xl-base-1.0"
sdxl_pipe = StableDiffusionXLPipeline.from_pretrained(
    sdxl_repo,
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
).to("cuda")

sdxl_pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    sdxl_pipe.scheduler.config,
    use_karras_sigmas=True
)

keyframe_images = {}
for shot in SHOTS:
    sid = shot["id"]
    print(f"🎨 [Keyframe] 正在渲染 {sid}: {shot['title']}...")
    generator = torch.Generator(device="cuda").manual_seed(shot["seed"])
    img = sdxl_pipe(
        prompt=shot["prompt"],
        negative_prompt=shot["negative_prompt"],
        width=1024,
        height=576,
        num_inference_steps=25,
        guidance_scale=7.5,
        generator=generator
    ).images[0]
    
    png_path = f"/tmp/{sid}_keyframe.png"
    img.save(png_path)
    keyframe_images[sid] = img
    print(f"   ✅ 完成画格: {png_path}")

# Free SDXL pipeline from memory to make room for SVD-XT
del sdxl_pipe
torch.cuda.empty_cache()
print("🧹 SDXL 模型已卸载，显存已整理完毕。")

# 5. Stage 2: Render Real 3D Dynamic Video Clips via SVD-XT
print("\n🎥 [STAGE 2] 装配 SVD-XT (Stable Video Diffusion) 生成 25 帧真动态短视频...")
svd_repo = "stabilityai/stable-video-diffusion-img2vid-xt"
svd_pipe = StableVideoDiffusionPipeline.from_pretrained(
    svd_repo,
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")

clip_paths = {}
for shot in SHOTS:
    sid = shot["id"]
    print(f"🎬 [Video] 正在为 {sid} 生成 3D 摄像机与人物物理动态...")
    input_img = keyframe_images[sid].resize((1024, 576))
    
    generator = torch.Generator(device="cuda").manual_seed(shot["seed"])
    frames = svd_pipe(
        input_img,
        height=576,
        width=1024,
        num_frames=25,
        fps=7,
        motion_bucket_id=shot["motion_bucket"],
        noise_aug_strength=0.02,
        decode_chunk_size=8,
        generator=generator
    ).frames[0]
    
    mp4_path = f"/tmp/{sid}_clip.mp4"
    imageio.mimwrite(mp4_path, frames, fps=7, codec="libx264")
    clip_paths[sid] = mp4_path
    clip_size_kb = os.path.getsize(mp4_path) / 1024
    print(f"   ✅ 视频生成完毕: {mp4_path} ({clip_size_kb:.2f} KB)")

del svd_pipe
torch.cuda.empty_cache()

# 6. Stage 3: Stream Base64 Buffers back to Host
print("\n🚀 [STAGE 3] 开始回传画格与视频 Base64 数据流...")
for shot in SHOTS:
    sid = shot["id"]
    # 1) Keyframe PNG
    png_path = f"/tmp/{sid}_keyframe.png"
    with open(png_path, "rb") as f:
        png_b64 = base64.b64encode(f.read()).decode("utf-8")
    print(f"<<<B64_KEYFRAME:{sid}:START>>>")
    chunk_size = 65536
    for i in range(0, len(png_b64), chunk_size):
        print(png_b64[i:i+chunk_size])
    print(f"<<<B64_KEYFRAME:{sid}:END>>>")
    
    # 2) Video Clip MP4
    mp4_path = clip_paths[sid]
    with open(mp4_path, "rb") as f:
        mp4_b64 = base64.b64encode(f.read()).decode("utf-8")
    print(f"<<<B64_CLIP:{sid}:START>>>")
    for i in range(0, len(mp4_b64), chunk_size):
        print(mp4_b64[i:i+chunk_size])
    print(f"<<<B64_CLIP:{sid}:END>>>")

total_time = time.time() - t0
print("==================================================")
print(f"🏁 [REMOTE G4] 全部 6 个真视频分镜与定妆画格渲染完成！总耗时: {total_time:.2f} 秒")
print("==================================================")
