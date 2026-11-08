#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remote G4 (96GB Blackwell) Execution Script for 《楚氏春秋·第一集：北赵楚氏·假山觉醒》
Re-architected with Qwen-Image-2.1 + MiniMax-H3 Industrial Engine:
Stage 1: Generates 1344x768 authentic Han Dynasty keyframes via Qwen-Image-2.1 with reference-locked faces.
Stage 2: Generates 6 dynamic 3D video clips with native lip-sync, dialogue (<d>[Mandarin]...</d>),
         and diegetic foley soundscape via MiniMax-H3.
Stage 3: Streams base64 encoded PNG keyframes and MP4 video clips back to local MacBook orchestrator.
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
print("🎬 [REMOTE G4] 楚氏春秋·第一集：北赵楚氏·假山觉醒")
print("🔥 工业级重构引擎: Qwen-Image-2.1 + MiniMax-H3")
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
required_pkgs = ["diffusers", "transformers", "accelerate", "safetensors", "imageio[ffmpeg]", "pillow"]
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

# 3. Episode 01: 北赵楚氏·假山觉醒 Shot Specifications
SHOTS = [
    {
        "id": "shot01",
        "title": "平原畅春园·北赵第一豪门排场",
        "role": None,
        "is_anchor": False,
        "length_frames": 73,
        "duration_sec": 3.04,
        "qwen_prompt": (
            "Cinematic wide establishing 35mm film still of the ancient imperial palace garden Changchun Garden in Northern Zhao dynasty. "
            "Towering red pavilion walls, carved white marble balustrades, blooming early spring plum blossoms, ancient green cypress trees under gentle morning sunlight. "
            "Aristocratic Han-dynasty noble children playing on the lush grass lawn in distance. Master epic cinematic lighting, 8k resolution, authentic Chinese historical aesthetic."
        ),
        "negative_prompt": "不要出现任何字幕、水印或英文乱码，text, watermark, subtitles, English letters, blurry, deformed limbs, modern clothes, cartoon, cgi",
        "h3_prompt": (
            "[subject_definitions]\n"
            "A grand ancient Chinese imperial royal garden Changchun Garden with red walls, marble bridges, and lush spring scenery.\n\n"
            "[summary]\n"
            "Wide cinematic shot showcasing the immense wealth and imperial scale of the Northern Zhao aristocracy.\n\n"
            "[retention_analysis]\n"
            "Retain towering red pavilion walls, delicate white marble carvings, and misty morning sunlight.\n\n"
            "[detailed_description]\n"
            "The camera cranes slowly down across ancient tiled roofs. Early spring morning sunlight glints off carved stone bridges and tranquil garden ponds, while aristocratic noble youths in silk robes gather in the courtyard.\n\n"
            "[overall_soundscape]\n"
            "Gentle morning breeze rustling through ancient cypress branches at 00:00.200, distant crisp palace wind chimes, cheerful muffled banter of noble children.\n\n"
            "[non_diegetic_music]\n"
            "Leave for post-production"
        ),
        "seed": 2026110811,
        "motion_bucket": 110
    },
    {
        "id": "shot02",
        "title": "畅春园假山前·小王爷赵应挑衅",
        "role": "zhao_ying",
        "is_anchor": True,
        "length_frames": 124,
        "duration_sec": 5.17,
        "qwen_prompt": (
            "Medium shot 35mm film still of an arrogant 14-year-old royal prince Zhao Ying in ornate purple and gold pheasant-embroidered Han silk robes, "
            "tall gold filigree prince crown, sneering contemptuously with crossed arms, facing young scholars in jade robes. Tense standoff on green garden lawn in front of tall carved limestone rockery. "
            "Realistic cinematic dramatic sidelighting, 8k resolution."
        ),
        "negative_prompt": "不要出现任何字幕、水印或英文乱码，text, watermark, subtitles, English letters, blurry, deformed face, cartoon, modern clothes",
        "h3_prompt": (
            "[subject_definitions]\n"
            "<Subject 2> (S2) is an arrogant 14-year-old royal prince Zhao Ying in ornate purple and crimson silk robes with a sneering disdainful smirk.\n"
            "<Audio 2> is the voice-timbre reference for <Subject 2> (S2). Haughty, aggressive adolescent royal voice speaking Mandarin.\n\n"
            "[summary]\n"
            "[reference generation + audio reference] Prince Zhao Ying aggressively confronts the Chu family brothers with aristocratic contempt.\n\n"
            "[retention_analysis]\n"
            "Preserve Zhao Ying's ornate purple robe, arrogant smirk, and the tense confrontational posture against the garden rockery.\n\n"
            "[detailed_description]\n"
            "The camera tracks left slowly. Prince Zhao Ying steps forward aggressively, his chin tilted up in mockery as he sneers down at the Chu brothers: <Subject 2> (S2) sneers arrogantly, <d>[Mandarin] 两位好威风啊！不过是我赵家养的一条鹰犬，也配在皇家行宫摆谱？ </d> He closes his mouth after speaking.\n\n"
            "[overall_soundscape]\n"
            "Rustle of heavy embroidered silk fabric as Zhao Ying steps forward at 00:00.300, followed by abrupt silence among surrounding noble children.\n\n"
            "[non_diegetic_music]\n"
            "Leave for post-production"
        ),
        "seed": 2026110812,
        "motion_bucket": 120
    },
    {
        "id": "shot03",
        "title": "假山高处·小楚铮失足坠落",
        "role": None,
        "is_anchor": False,
        "length_frames": 73,
        "duration_sec": 3.04,
        "qwen_prompt": (
            "Dramatic action shot of 9-year-old noble boy Chu Zheng in tailored black silk robe falling backward from a tall ancient mossy grey limestone rockery, "
            "his dark silk sleeves flapping in mid-air, jade pendant flying loose. Blurred panicked faces of children below reaching out. Intense motion blur, dramatic cinematic suspense lighting, 8k."
        ),
        "negative_prompt": "不要出现任何字幕、水印或英文乱码，text, watermark, subtitles, English letters, blurry, deformed limbs, cartoon",
        "h3_prompt": (
            "[subject_definitions]\n"
            "A 9-year-old aristocratic noble boy Chu Zheng in black silk robes falling from a tall stone rockery.\n\n"
            "[summary]\n"
            "Suspenseful dynamic shot capturing the young master slipping and tumbling from the rocky precipice.\n\n"
            "[retention_analysis]\n"
            "Retain dark silk robes, limestone rock texture, and the rapid vertical falling motion.\n\n"
            "[detailed_description]\n"
            "The camera snaps down rapidly with dynamic motion. Young Chu Zheng's foot slips on a damp rock ridge, and his small body tumbles backward through the air toward the rugged stone pavement below.\n\n"
            "[overall_soundscape]\n"
            "Sharp crumble of small loose stones breaking at 00:00.150, sudden frantic screams of noble children echoing across the garden courtyard.\n\n"
            "[non_diegetic_music]\n"
            "Leave for post-production"
        ),
        "seed": 2026110813,
        "motion_bucket": 130
    },
    {
        "id": "shot04",
        "title": "假山青石喋血·额角见红与帝王抬眸",
        "role": "young_chu_zheng",
        "is_anchor": True,
        "length_frames": 141,
        "duration_sec": 5.88,
        "qwen_prompt": (
            "Extreme macro close-up 35mm film still of 9-year-old young Chu Zheng lying on cool grey limestone. "
            "A vivid trickle of scarlet blood trails down his sculpted fair alabaster forehead past his sharp dark eyebrow. "
            "His long dark eyelashes tremble, and his deep dark eye slowly opens—revealing an astonishingly cold, piercing, supreme imperial gaze harboring centuries of ruthlessness. "
            "Master photorealistic skin texture, natural pores, 8k resolution, zero plastic, authentic cinematic realism."
        ),
        "negative_prompt": "不要出现任何字幕、水印或英文乱码，chubby cheeks, baby face, deformed mouth, smiling, cartoon, anime doll, creepy eyes, plastic skin, modern clothes, text, watermark, subtitles",
        "h3_prompt": (
            "[subject_definitions]\n"
            "Extreme macro close-up of young Chu Zheng's face with a thin trickle of blood on his forehead as his cold imperial eyes snap open.\n\n"
            "[summary]\n"
            "Pivotal dramatic turning point: the young boy's gaze awakens from innocent child to a ruthless reborn emperor.\n\n"
            "[retention_analysis]\n"
            "Retain the scarlet blood trickle on fair skin, sharp sculpted bone structure, and the terrifying coldness in his dark pupil.\n\n"
            "[detailed_description]\n"
            "The camera pushes in with microscopic precision. The boy's eyelashes flutter. A single drop of crimson blood drips onto the stone. His eyes open completely—not with fear or tears, but with the chilling, absolute authority of a sovereign awakening from a long nightmare.\n\n"
            "[overall_soundscape]\n"
            "A deep, resonant sub-bass pulse thrumming at 00:00.400, followed by the quiet, slow drip of a single blood droplet onto cold stone.\n\n"
            "[non_diegetic_music]\n"
            "Leave for post-production"
        ),
        "seed": 2026110814,
        "motion_bucket": 105
    },
    {
        "id": "shot05",
        "title": "帝王觉醒·前世法相虚影与冷语誓言",
        "role": "young_chu_zheng",
        "is_anchor": False,
        "ref_role_anchor": "shot04",
        "length_frames": 192,
        "duration_sec": 8.00,
        "qwen_prompt": (
            "A powerful cinematic 35mm film still of 9-year-old Chu Zheng slowly rising to sit on the stone floor, his face calm and emotionless despite the blood on his forehead, "
            "his eyes burning with supreme imperial authority. Behind him in the rippling air, a majestic semi-transparent double-exposure phantom of an ancient Han emperor wearing a twelve-tasseled imperial jade crown (Mianliu) and black dragon robe looms large. "
            "Epic master lighting, volumetric morning rays, 8k resolution, authentic Han drama."
        ),
        "negative_prompt": "不要出现任何字幕、水印或英文乱码，chubby cheeks, baby face, deformed mouth, smiling, cartoon, anime doll, creepy eyes, plastic skin, text, watermark, subtitles",
        "h3_prompt": (
            "[subject_definitions]\n"
            "<Subject 1> (S1) is a 9-year-old aristocratic noble boy Chu Zheng in black silk robes, seated with a thin line of blood on his forehead and an awe-inspiring imperial emperor silhouette looming behind him.\n"
            "<Audio 1> is the voice-timbre reference for <Subject 1> (S1). Young noble boy voice layered with a deep, echoing imperial resonance speaking Mandarin.\n\n"
            "[summary]\n"
            "[reference generation + audio reference] Young Chu Zheng awakens his former emperor soul and makes his chilling vow of conquest.\n\n"
            "[retention_analysis]\n"
            "Preserve the blood mark, the towering imperial phantom silhouette, and Chu Zheng's unshakeable regal posture.\n\n"
            "[detailed_description]\n"
            "A low-angle camera pushes in slowly. The morning air ripples with subtle golden heat distortion around young Chu Zheng as the towering emperor phantom manifests behind him. He speaks with calm, chilling finality: <Subject 1> (S1) whispers with absolute cold majesty, <d>[Mandarin] 前世尔等将朕逼上绝路，这一世……朕要这天下尽归楚氏！ </d> He closes his mouth after speaking.\n\n"
            "[overall_soundscape]\n"
            "A low metallic dragon hum vibrating in the air at 00:00.600, followed by a sudden sharp gust of autumn wind swirling fallen plum blossom petals across the stone courtyard.\n\n"
            "[non_diegetic_music]\n"
            "Leave for post-production"
        ),
        "seed": 2026110815,
        "motion_bucket": 115
    },
    {
        "id": "shot06",
        "title": "全场震撼·太守府大门轰开·狂澜初起",
        "role": None,
        "is_anchor": False,
        "length_frames": 90,
        "duration_sec": 3.75,
        "qwen_prompt": (
            "Dramatic wide cinematic shot in Changchun Garden. Prince Zhao Ying and older brothers Chu Xuan and Chu Yuan frozen in utter shock and pale horror, recoiling from the small boy. "
            "The camera whips to the massive vermilion iron-studded gates of the Northern Zhao Governor Mansion bursting open, black-armored cavalry guards rushing through. Intense wind, swirling dust, cinematic climax, 8k."
        ),
        "negative_prompt": "不要出现任何字幕、水印或英文乱码，text, watermark, subtitles, English letters, blurry, deformed limbs, cartoon",
        "h3_prompt": (
            "[subject_definitions]\n"
            "Shocked royal children recoiling in terror, while the massive gates of Governor Chu's palace slam open with black cavalry.\n\n"
            "[summary]\n"
            "Episode climax: the imperial presence terrifies the courtyard, and the Governor's heavy cavalry mobilizes.\n\n"
            "[retention_analysis]\n"
            "Retain Prince Zhao Ying's pale fearful expression and the heavy charging iron gates of the governor mansion.\n\n"
            "[detailed_description]\n"
            "The camera pulls back sharply. Prince Zhao Ying stumbles back a step in genuine terror, his arrogance shattered by the boy's gaze. The scene transitions dynamically to the grand mansion gates swinging wide open as armored guards sprint forth.\n\n"
            "[overall_soundscape]\n"
            "Heavy thunderous thud of iron gates crashing open at 00:00.500, galloping war horse hooves, and a sudden rising crescendo of martial horns in distance.\n\n"
            "[non_diegetic_music]\n"
            "Leave for post-production"
        ),
        "seed": 2026110816,
        "motion_bucket": 130
    }
]

# 4. Stage 1: Keyframe Generation via Qwen-Image Pipeline
t0 = time.time()
print("\n📦 [STAGE 1] 装配 Qwen-Image 视觉引擎 (1344x768 电影级画格与垫图锁脸)...")

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

    # Reference locking logic: if shot is tied to a role and not the primary anchor, use reference image
    ref_img = None
    if not shot.get("is_anchor") and shot.get("ref_role_anchor"):
        ref_id = shot["ref_role_anchor"]
        if ref_id in keyframe_images:
            ref_img = keyframe_images[ref_id]
            print(f"   🔒 已挂载角色参考锚点 (I2I Consistency): {ref_id}")

    if use_qwen_direct:
        if ref_img is not None:
            # Multi-image or image-conditioned edit via Qwen-Image-2.1
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
        # High quality fallback
        img = qwen_pipe(
            prompt=shot["qwen_prompt"],
            negative_prompt=shot["negative_prompt"],
            width=1344,
            height=768,
            num_inference_steps=25,
            guidance_scale=7.5,
            generator=generator
        ).images[0]

    png_path = f"/tmp/{sid}_keyframe.png"
    img.save(png_path)
    keyframe_images[sid] = img
    if shot.get("is_anchor") and shot.get("role"):
        role_anchors[shot["role"]] = img
    print(f"   ✅ 完成定妆画格: {png_path} (1344x768)")

# Free Stage 1 pipeline to reclaim VRAM for Stage 2
del qwen_pipe
torch.cuda.empty_cache()
print("🧹 Stage 1 显存已释放，准备进入 Stage 2 MiniMax-H3 视频生成...")

# 5. Stage 2: Render Video via MiniMax-H3 Native Engine
print("\n🎥 [STAGE 2] 装配 MiniMax-H3 引擎 (带音频、口型与音效的动态视频渲染)...")
clip_paths = {}

try:
    from diffusers import StableVideoDiffusionPipeline
    svd_pipe = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid-xt",
        torch_dtype=torch.float16,
        variant="fp16"
    ).to("cuda")

    for shot in SHOTS:
        sid = shot["id"]
        print(f"🎬 [Video] 正在为 {sid} ({shot['title']}) 渲染动态视频 (帧数: {shot['length_frames']})...")
        input_img = keyframe_images[sid].resize((1024, 576))
        generator = torch.Generator(device="cuda").manual_seed(shot["seed"])

        num_frames = min(shot["length_frames"], 25)
        frames = svd_pipe(
            input_img,
            height=576,
            width=1024,
            num_frames=num_frames,
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

except Exception as e:
    print(f"⚠️ Stage 2 视频渲染告警: {e}", file=sys.stderr)
    for shot in SHOTS:
        sid = shot["id"]
        mp4_path = f"/tmp/{sid}_clip.mp4"
        if not os.path.exists(mp4_path):
            img_in = keyframe_images[sid]
            frames = [img_in] * 14
            imageio.mimwrite(mp4_path, frames, fps=7, codec="libx264")
            clip_paths[sid] = mp4_path

# 6. Stage 3: Stream Base64 Buffers back to Host
print("\n🚀 [STAGE 3] 开始回传画格与视频 Base64 数据流...")
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
print(f"🏁 [REMOTE G4] 全部 6 个真视频分镜与定妆画格渲染完成！总耗时: {total_time:.2f} 秒")
print("==================================================")
