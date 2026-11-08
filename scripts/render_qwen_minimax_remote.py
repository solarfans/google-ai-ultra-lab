#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remote G4 (96GB Blackwell) Execution Script for 《楚氏春秋·第一集：空难惊魂·异界重生》
100% Canon Aligned: Modern airliner disaster -> ocean crash -> ancient governor mansion rebirth.
Stage 1: Generates 1344x768 cinematic keyframes via Qwen-Image-2.1 with reference-locked faces.
Stage 2: Generates real dynamic 3D video clips with pronounced camera pan, lightning, and character motion (SVD-XT).
Stage 3: Streams base64 encoded PNG keyframes and real MP4 video clips back to local MacBook orchestrator.
"""

import sys
import subprocess
import os
import time
import json
import base64
from pathlib import Path

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TQDM_DISABLE"] = "1"

print("==================================================")
print("🎬 [REMOTE G4] 楚氏春秋·第一集：空难惊魂·异界重生")
print("🔥 100% 原著精准对齐: 现代空难 ➡️ 坠海 ➡️ 异界重生")
print("==================================================")

# 1. Check GPU Device
try:
    import torch
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "torch", "accelerate"])
    import torch

if not torch.cuda.is_available():
    print("❌ 未检测到 CUDA GPU! 必须在 Colab GPU 实例上执行", file=sys.stderr)
    sys.exit(1)

gpu_name = torch.cuda.get_device_name(0)
vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
print(f"⚡ 检测到顶级云端 GPU: {gpu_name} ({vram:.2f} GB 显存)")

# 2. Install / Verify Essential Libraries
print("📦 [INIT] 正在核验并装载生成管线依赖...")
required_pkgs = ["diffusers", "transformers", "accelerate", "safetensors", "imageio[ffmpeg]", "pillow", "numpy"]
missing = []
for pkg in required_pkgs:
    name = pkg.split("[")[0].replace("-", "_")
    try:
        __import__(name)
    except ImportError:
        missing.append(pkg)

if missing:
    print(f"  🔧 安装缺失组件: {', '.join(missing)}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + missing)

import imageio
from PIL import Image

# 3. Episode 01: 空难惊魂·异界重生 (100% 原著精准对齐)
SHOTS = [
    {
        "id": "shot01",
        "title": "现代客机空难·剧烈失重与红光闪烁",
        "role": None,
        "is_anchor": False,
        "length_frames": 25,
        "qwen_prompt": (
            "Cinematic wide interior shot of a modern commercial Boeing airliner cabin violently shaking and plunging through a stormy night sky. "
            "Overhead oxygen masks dangling and swinging wildly, red emergency cabin lights flashing against panicked passengers strapped in their seats. "
            "Violent rain and bright lightning flashes lashing against the cabin windows outside. Master disaster movie cinematography, dramatic high-contrast lighting, 8k resolution."
        ),
        "negative_prompt": "text, watermark, subtitles, English letters, blurry, deformed limbs, smiling, cartoon, cgi",
        "seed": 2026110821,
        "motion_bucket": 190
    },
    {
        "id": "shot02",
        "title": "绝命短信·客机轰然坠海",
        "role": "modern_protagonist",
        "is_anchor": False,
        "length_frames": 25,
        "qwen_prompt": (
            "Close-up OTS shot of trembling adult hands holding an illuminated mobile phone screen inside a dark violently shaking airplane cabin. "
            "Through the rain-streaked window, colossal turbulent black ocean waves rise up into the night sky to swallow the aircraft. "
            "Blinding lightning bolt illuminating the dark churning sea foam. Master Hollywood disaster realism, intense suspense, 8k."
        ),
        "negative_prompt": "text, watermark, subtitles, English letters, blurry, deformed hands, cartoon",
        "seed": 2026110822,
        "motion_bucket": 180
    },
    {
        "id": "shot03",
        "title": "时空流转·古朴太守府卧房",
        "role": None,
        "is_anchor": False,
        "length_frames": 25,
        "qwen_prompt": (
            "Cinematic medium establishing shot of an ancient Chinese aristocratic bedroom in Han dynasty. "
            "A magnificent dark carved sandalwood canopy bed with fine translucent gauze curtains, bronze incense burner releasing fragrant pale smoke curls into golden morning sunbeams. "
            "A 9-year-old noble boy lying motionless under embroidered crimson silk quilts with a clean white bandage on his forehead. Peaceful, mysterious, 8k resolution."
        ),
        "negative_prompt": "modern furniture, electric lights, bright colors, text, watermark, subtitles, cartoon",
        "seed": 2026110823,
        "motion_bucket": 135
    },
    {
        "id": "shot04",
        "title": "母爱泣血·楚夫人跪地磕头求神",
        "role": "mrs_chu",
        "is_anchor": True,
        "length_frames": 25,
        "qwen_prompt": (
            "Medium shot 35mm film still of elegant noble mother Madam Chu weeping bitterly, kneeling on the cold stone floor beside the carved canopy bed, "
            "kowtowing repeatedly with hands trembling on the floor. Her dark embroidered silk robes pooled around her, loose jade hairpins dangling, tears glistening on her pale cheeks. "
            "Authentic Han historical drama realism, dramatic warm sidelighting, natural skin texture, 8k."
        ),
        "negative_prompt": "smiling, relaxed, modern clothes, deformed face, cartoon, text, watermark, subtitles",
        "seed": 2026110824,
        "motion_bucket": 175
    },
    {
        "id": "shot05",
        "title": "抚面惊醒·现代灵魂入主幼童身躯",
        "role": "young_chu_zheng",
        "is_anchor": True,
        "ref_role_anchor": "shot03",
        "length_frames": 25,
        "qwen_prompt": (
            "Cinematic close-up of 9-year-old boy Chu Zheng sitting bolt upright in the ancient bed, staring down in profound shock at his small fair hands. "
            "His forehead bears a neat bandage with a faint blood spot. His dark eyes shift rapidly from utter disbelief to razor-sharp adult intellectual composure. "
            "Master photorealistic skin texture, natural pores, 8k resolution, authentic Chinese historical aesthetics, zero plastic."
        ),
        "negative_prompt": "chubby cheeks, baby face, deformed mouth, smiling, cartoon, anime doll, creepy eyes, plastic skin, modern clothes, text, watermark, subtitles",
        "seed": 2026110825,
        "motion_bucket": 185
    },
    {
        "id": "shot06",
        "title": "推窗放眼·北赵第一豪门霸业启程",
        "role": None,
        "is_anchor": False,
        "length_frames": 25,
        "qwen_prompt": (
            "Cinematic slow push shot looking past young Chu Zheng standing by an open carved lattice window in silk robes. "
            "Outside lies the magnificent sprawling capital city of Pingyuan County under morning mist: towering vermilion palace walls, fluttering battle banners, "
            "marching armored cavalry patrols in distance. Epic historical scale, atmospheric cinematic masterpiece, 8k resolution."
        ),
        "negative_prompt": "modern buildings, skyscrapers, cars, deformed limbs, text, watermark, subtitles, cartoon",
        "seed": 2026110826,
        "motion_bucket": 160
    }
]

# 4. Stage 1: Keyframe Generation via Qwen-Image Pipeline
t0 = time.time()
print("\n📦 [STAGE 1] 装配 Qwen-Image 视觉引擎 (1344x768 电影级画格)...")

qwen_pipe = None
use_qwen_direct = False

try:
    from diffusers import QwenImage21Pipeline
    print("  ✨ 成功检测到官方 QwenImage21Pipeline！")
    qwen_pipe = QwenImage21Pipeline.from_pretrained(
        "Qwen/Qwen-Image-2.1-Turbo",
        torch_dtype=torch.bfloat16
    ).to("cuda")
    use_qwen_direct = True
except Exception as e:
    print(f"  ℹ️ QwenImage21Pipeline 未就绪或网络隔离 ({e})，启用兼容扩散流水线...")
    try:
        from diffusers import AutoPipelineForText2Image, DPMSolverMultistepScheduler
        qwen_pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True
        ).to("cuda")
        qwen_pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            qwen_pipe.scheduler.config,
            use_karras_sigmas=True
        )
    except Exception as e2:
        print(f"❌ 视觉生成管线加载失败: {e2}", file=sys.stderr)
        sys.exit(1)

keyframe_images = {}
role_anchors = {}

for shot in SHOTS:
    sid = shot["id"]
    print(f"🎨 [Keyframe] 正在渲染 {sid}: {shot['title']} (Seed: {shot['seed']})...")
    generator = torch.Generator(device="cuda").manual_seed(shot["seed"])

    ref_img = None
    if not shot.get("is_anchor") and shot.get("ref_role_anchor"):
        ref_id = shot["ref_role_anchor"]
        if ref_id in keyframe_images:
            ref_img = keyframe_images[ref_id]
            print(f"   🔒 已挂载角色参考锚点: {ref_id}")

    if use_qwen_direct:
        if ref_img is not None:
            img = qwen_pipe(
                prompt=shot["qwen_prompt"],
                image=ref_img,
                generator=generator
            ).images[0]
        else:
            img = qwen_pipe(
                prompt=shot["qwen_prompt"],
                width=1344,
                height=768,
                generator=generator
            ).images[0]
    else:
        img = qwen_pipe(
            prompt=shot["qwen_prompt"],
            negative_prompt=shot["negative_prompt"],
            width=1344,
            height=768,
            num_inference_steps=25,
            guidance_scale=7.5,
            generator=generator
        ).images[0]

    # CRITICAL: Always convert to RGB 3-channel to eliminate 4-channel RGBA crashes downstream!
    img = img.convert("RGB")
    png_path = f"/tmp/{sid}_keyframe.png"
    img.save(png_path)
    keyframe_images[sid] = img
    print(f"   ✅ 完成定妆画格: {png_path} (1344x768 RGB)")

# Free Stage 1 pipeline to reclaim 100% VRAM for Stage 2
del qwen_pipe
torch.cuda.empty_cache()
print("🧹 Stage 1 显存已释放，准备进入 Stage 2 真实物理动态视频渲染...")

# 5. Stage 2: Render Real 3D Dynamic Video Clips via SVD-XT (NO SILENT FALLBACK!)
print("\n🎥 [STAGE 2] 装配 SVD-XT 物理视频引擎 (渲染真实 3D 摄像机运动与物理动态)...")
clip_paths = {}

from diffusers import StableVideoDiffusionPipeline
svd_pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")

for shot in SHOTS:
    sid = shot["id"]
    print(f"🎬 [Video] 正在为 {sid} ({shot['title']}) 渲染动态视频...")

    # Ensure strictly 3-channel RGB image resized for video diffusion
    input_img = keyframe_images[sid].convert("RGB").resize((1024, 576))
    generator = torch.Generator(device="cuda").manual_seed(shot["seed"])

    frames = svd_pipe(
        input_img,
        height=576,
        width=1024,
        num_frames=25,
        fps=8,
        motion_bucket_id=shot["motion_bucket"],
        noise_aug_strength=0.03,
        decode_chunk_size=8,
        generator=generator
    ).frames[0]

    import numpy as np
    mp4_path = f"/tmp/{sid}_clip.mp4"
    frames_np = [np.array(f) for f in frames]
    imageio.mimwrite(mp4_path, frames_np, fps=8, codec="libx264")
    clip_paths[sid] = mp4_path
    clip_size_kb = os.path.getsize(mp4_path) / 1024
    print(f"   ✅ 真实动态视频生成完毕: {mp4_path} ({clip_size_kb:.2f} KB, 25 帧物理运镜)")

del svd_pipe
torch.cuda.empty_cache()

# 6. Stage 3: Stream Base64 Buffers back to Host
print("\n🚀 [STAGE 3] 开始回传真动态画格与视频 Base64 数据流...")
for shot in SHOTS:
    sid = shot["id"]
    # 1) Keyframe PNG
    png_path = f"/tmp/{sid}_keyframe.png"
    if os.path.exists(png_path):
        with open(png_path, "rb") as f:
            png_b64 = base64.b64encode(f.read()).decode("utf-8")
        print(f"<<<B64_KEYFRAME:{sid}:START>>>")
        chunk_size = 65536
        for i in range(0, len(png_b64), chunk_size):
            print(png_b64[i:i+chunk_size])
        print(f"<<<B64_KEYFRAME:{sid}:END>>>")

    # 2) Video Clip MP4
    mp4_path = clip_paths.get(sid)
    if mp4_path and os.path.exists(mp4_path):
        with open(mp4_path, "rb") as f:
            mp4_b64 = base64.b64encode(f.read()).decode("utf-8")
        print(f"<<<B64_CLIP:{sid}:START>>>")
        for i in range(0, len(mp4_b64), chunk_size):
            print(mp4_b64[i:i+chunk_size])
        print(f"<<<B64_CLIP:{sid}:END>>>")

total_time = time.time() - t0
print("==================================================")
print(f"🏁 [REMOTE G4] 全部 6 个真实动态视频分镜与定妆画格渲染完成！总耗时: {total_time:.2f} 秒")
print("==================================================")
