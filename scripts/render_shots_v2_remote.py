#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remote Batch Render Script v2: Authentic Han Dynasty High-Fidelity Renders on Colab G4.
Features:
- Full SDXL 1.0 Base (25 steps, CFG=7.5) with DPMSolverMultistepScheduler.
- Complete eradication of monochrome collapse (rich saturation, imperial crimson, gold, warm candlelight).
- Authentic Chinese Three Kingdoms / Han Dynasty aesthetics (Hanfu, Tongtian Guan, feather fan, Han Jian).
- Strict exclusion of Japanese Sengoku/kimono/samurai artifacts and distorted facial deformities.
"""

import sys
import subprocess
import os
import time
import base64

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TQDM_DISABLE"] = "1"

print("==================================================")
print("🎬 [REMOTE G4] 楚氏春秋·外传章 - 正统汉代高画质分镜画格渲染 (v2)")
print("==================================================")

# 1. Check and install dependencies
try:
    import diffusers
    import transformers
    import safetensors
    import accelerate
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
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler

# 2. Check Device
if torch.cuda.is_available():
    gpu_name = torch.cuda.get_device_name(0)
    vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"⚡ 检测到顶级 GPU: {gpu_name} ({vram:.2f} GB 显存)")
else:
    print("❌ 未检测到 CUDA GPU!", file=sys.stderr)
    sys.exit(1)

# 3. Model Configuration: Full SDXL Base 1.0 (25-30 steps, CFG=7.5)
base_repo = "stabilityai/stable-diffusion-xl-base-1.0"
t_load0 = time.time()
print(f"📦 正在装配满血 SDXL-Base 1.0 (FP16)...")

pipe = StableDiffusionXLPipeline.from_pretrained(
    base_repo,
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
).to("cuda")

# Use DPMSolverMultistepScheduler (Karras) for photorealistic human portraits
pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config,
    use_karras_sigmas=True,
    algorithm_type="sde-dpmsolver++"
)
print(f"✅ 满血模型与调度器装载完成，耗时: {time.time() - t_load0:.2f} 秒")

# 4. Shot Definitions (Authentic Chinese Han Dynasty / Zero Sengoku / High Saturation)
V2_SHOTS = [
    {
        "id": "shot01",
        "title": "Shot 01: 太监仓皇跪报 (内侍对白)",
        "filename": "shot01_eunuch_panic.png",
        "prompt": (
            "A cinematic medium shot inside an authentic Han dynasty imperial palace study room. "
            "In the center on a rich crimson red carpet, a panicked 20-year-old young Chinese court eunuch "
            "wearing azure blue Hanfu servant robes stumbles to his knees, pointing trembling hands toward the heavy dark palace doors. "
            "Carved dark sandalwood tables, bronze incense burner emitting curls of smoke. "
            "Warm golden candlelight reflections, storm rain outside wooden latticed windows, "
            "vibrant colors, photorealistic, 8k resolution, cinematic Chinese historical epic, authentic Han Dynasty."
        ),
        "negative_prompt": (
            "Japanese, samurai, kimono, katana, ninja, anime, cartoon, 3d render, deformed face, creepy eyes, "
            "melted face, ugly, monstrous, extra fingers, monochrome, black and white, grayscale, washed out"
        ),
        "seed": 102,
        "width": 1344,
        "height": 768,
    },
    {
        "id": "shot02",
        "title": "Shot 02: 刘禅从容提笔 (刘禅对白)",
        "filename": "shot02_liushan_portrait.png",
        "prompt": (
            "A cinematic solo close-up portrait of 28-year-old Chinese Emperor Liu Shan, handsome dignified facial features, "
            "clear intense eyes showing hidden regal ambition, sitting calmly behind a massive dark sandalwood imperial desk. "
            "Wearing authentic Han Dynasty imperial Xuan-Yi (traditional black silk ceremonial robe with vibrant crimson red borders "
            "and intricate gold Han dragon embroidery), wearing a Chinese emperor Tongtian Guan cap with jade pin. "
            "Holding a calligraphy brush in hand, writing calmly without panic. "
            "Warm golden candlelight illuminating his face and robe, vibrant colors, rich cinematic lighting, "
            "photorealistic, 8k resolution, authentic Three Kingdoms Han dynasty."
        ),
        "negative_prompt": (
            "Japanese, kimono, samurai, katana, jinbaori, eboshi, anime, cartoon, creepy, ugly, deformed eyes, "
            "melted mouth, monstrosity, monochrome, black and white, grayscale, pale"
        ),
        "seed": 204,
        "width": 1344,
        "height": 768,
    },
    {
        "id": "shot03",
        "title": "Shot 03: 诸葛亮羽扇入殿 (诸葛亮对白)",
        "filename": "shot03_zhuge_entrance.png",
        "prompt": (
            "A cinematic medium shot of Chancellor Zhuge Liang stepping into the Han imperial palace hall. "
            "A 54-year-old dignified Chinese statesman with a neat long black and gray beard, wise serene eyes, "
            "wearing authentic Chinese Han Dynasty scholar robe (dark silk Hanfu with crimson borders) and Chinese Jinxian Guan headdress, "
            "gracefully holding a white crane feather fan in his hand. "
            "Palace doors open behind him revealing rain and distant lightning. "
            "Elite Han palace guards in dark iron scale armor holding halberds stand behind. "
            "Atmospheric palace smoke, warm candle glow, photorealistic, 8k resolution, authentic Chinese Three Kingdoms."
        ),
        "negative_prompt": (
            "Japanese, samurai, kimono, katana, eboshi, ninja, anime, cartoon, distorted faces, melted face, ugly, "
            "creepy, monochrome, black and white, grayscale"
        ),
        "seed": 305,
        "width": 1344,
        "height": 768,
    },
    {
        "id": "shot04",
        "title": "Shot 04: 君臣对峙·刘禅冷嘲 (刘禅对白)",
        "filename": "shot04_confrontation_ots.png",
        "prompt": (
            "A dramatic cinematic medium-close shot of Emperor Liu Shan sitting at his sandalwood imperial desk. "
            "He slowly puts down his calligraphy brush, lifting cold mocking eyes and a subtle sneer directly confronting the viewer. "
            "Wearing imperial Han dragon robe in rich black silk with crimson red trim and golden embroidery. "
            "Flickering golden candlelight illuminating his sharp handsome facial features. "
            "Intense psychological confrontation, sharp focus, 35mm film still, photorealistic, 8k resolution, "
            "authentic Chinese Three Kingdoms."
        ),
        "negative_prompt": (
            "Japanese, samurai, kimono, katana, anime, cartoon, distorted eyes, melted face, ugly, monstrosity, "
            "duplicate, monochrome, black and white, grayscale"
        ),
        "seed": 408,
        "width": 1344,
        "height": 768,
    },
    {
        "id": "shot05",
        "title": "Shot 05: 拔剑阻拦·诸葛亮叹息 (诸葛亮对白)",
        "filename": "shot05_sword_drawn.png",
        "prompt": (
            "A dynamic cinematic medium shot in an ancient Han palace hall. "
            "In the foreground, a 22-year-old Chinese noble lady warrior in dark crimson Hanfu martial dress "
            "draws a straight double-edged Chinese Han Jian sword (gleaming cold silver blade, straight blade). "
            "Beside her, Chancellor Zhuge Liang gently raises his white crane feather fan to halt her sword, "
            "closing his eyes in profound sorrow and grief, three-strand long beard blowing gently. "
            "Dramatic candlelight and rain shadows, deep emotional tension, photorealistic, 8k resolution, "
            "authentic Han Dynasty."
        ),
        "negative_prompt": (
            "katana, curved sword, Japanese, samurai, kimono, anime, cartoon, deformed fingers, melted face, ugly, "
            "monstrosity, monochrome, black and white, grayscale"
        ),
        "seed": 512,
        "width": 1344,
        "height": 768,
    }
]

print(f"\n🎨 开始渲染 v2 汉代正统全色画格，共计 {len(V2_SHOTS)} 个分镜...")
t_batch_start = time.time()

for idx, shot in enumerate(V2_SHOTS, 1):
    print(f"\n--- [{idx}/{len(V2_SHOTS)}] 正在精细渲染: {shot['title']} ---")
    print(f"    分辨率: {shot['width']}x{shot['height']}, 步数: 25, CFG: 7.5, Seed: {shot['seed']}")
    
    generator = torch.Generator(device="cuda").manual_seed(shot["seed"])
    t_shot0 = time.time()
    
    image = pipe(
        prompt=shot["prompt"],
        negative_prompt=shot["negative_prompt"],
        width=shot["width"],
        height=shot["height"],
        num_inference_steps=25,
        guidance_scale=7.5,
        generator=generator
    ).images[0]
    
    infer_time = time.time() - t_shot0
    print(f"    ✨ 纯 GPU 推理耗时: {infer_time:.2f} 秒")
    
    output_path = f"/content/{shot['filename']}"
    image.save(output_path, "PNG")
    size_kb = os.path.getsize(output_path) / 1024
    print(f"    💾 图像已保存至 {output_path} ({size_kb:.2f} KB)")
    
    with open(output_path, "rb") as f:
        b64_str = base64.b64encode(f.read()).decode("utf-8")
    
    print(f"===BASE64_IMAGE_START:{shot['id']}===")
    print(b64_str)
    print(f"===BASE64_IMAGE_END:{shot['id']}===")

total_batch_time = time.time() - t_batch_start
print("\n==================================================")
print(f"🎉 全部 5 镜正统汉代高饱和度画格批量渲染完毕！总耗时: {total_batch_time:.2f} 秒")
print(f"🏁 [REMOTE G4] 任务圆满完成，即将释放 GPU 容器")
print("==================================================")
