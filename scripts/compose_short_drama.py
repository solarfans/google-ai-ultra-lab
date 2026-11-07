#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chu Shi Chun Qiu - Short Drama Episode 01 Master Composer v2 (Han Dynasty Overhaul)
Features:
- Clear Character Badges with distinct colors for each speaker:
  * 刘禅: Imperial Gold [【蜀汉后主 · 刘禅】]
  * 诸葛亮: Jade Green [【蜀汉丞相 · 诸葛亮】]
  * 内侍: Royal Azure [【黄门内侍 · 仓皇报信】]
- Dynamic cinematic camera pans & zooms targeting character facial focal points.
- Multi-channel audio mix: Neural dialogues + lowpass rain/thunder storm ambience.
- Renders chu_shi_chun_qiu_ep01_final.mp4, chu_shi_chun_qiu_ep01.srt, and chu_shi_chun_qiu_ep01_master.mp3.
"""

import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent
SHORT_DRAMA_DIR = ROOT_DIR / "pipelines" / "short_drama"
ASSETS_DIR = SHORT_DRAMA_DIR / "assets"
AUDIO_DIR = ASSETS_DIR / "audio"
SUB_DIR = ASSETS_DIR / "subtitles"
CLIPS_DIR = ASSETS_DIR / "clips"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SUB_DIR.mkdir(parents=True, exist_ok=True)
CLIPS_DIR.mkdir(parents=True, exist_ok=True)

# Shot choreography definitions with speaker metadata & color themes
SHOT_CONFIGS = [
    {
        "id": "shot01",
        "title": "太监仓皇跪报",
        "image_file": "shot01_eunuch_panic.png",
        "speaker_badge": "【黄门内侍 · 仓皇报信】",
        "badge_color": (70, 160, 240, 255),       # Azure Blue
        "dialogue": "皇上！外面禁军死伤殆尽……诸葛丞相的大军已布下天罗地网，将皇宫彻底围死了！",
        "voice": "zh-CN-YunxiNeural",
        "rate": "+15%",
        "zoom_expr": "min(zoom+0.0014,1.24)",
        "x_expr": "iw/2-(iw/zoom/2)",
        "y_expr": "ih*0.60-(ih/zoom*0.60)",
    },
    {
        "id": "shot02",
        "title": "刘禅从容提笔",
        "image_file": "shot02_liushan_portrait.png",
        "speaker_badge": "【蜀汉后主 · 刘禅】",
        "badge_color": (255, 215, 0, 255),        # Imperial Gold
        "dialogue": "走？丞相不动则已，一动必是天罗地网，朕又能走到何处？",
        "voice": "zh-CN-YunyangNeural",
        "rate": "-5%",
        "zoom_expr": "min(zoom+0.0012,1.22)",
        "x_expr": "iw*0.48-(iw/zoom*0.48)",
        "y_expr": "ih*0.38-(ih/zoom*0.38)",
    },
    {
        "id": "shot03",
        "title": "诸葛亮羽扇入殿",
        "image_file": "shot03_zhuge_entrance.png",
        "speaker_badge": "【蜀汉丞相 · 诸葛亮】",
        "badge_color": (78, 205, 140, 255),       # Jade Green
        "dialogue": "当真是龙困浅滩啊……想不到阿斗哥儿，也有今日。",
        "voice": "zh-CN-YunjianNeural",
        "rate": "-5%",
        "zoom_expr": "min(zoom+0.0010,1.20)",
        "x_expr": "iw*0.50-(iw/zoom*0.50)",
        "y_expr": "ih*0.36-(ih/zoom*0.36)",
    },
    {
        "id": "shot04",
        "title": "君臣对峙·冷嘲对决",
        "image_file": "shot04_confrontation_ots.png",
        "speaker_badge": "【蜀汉后主 · 刘禅】",
        "badge_color": (255, 215, 0, 255),        # Imperial Gold
        "dialogue": "智者近乎妖。丞相大人，论阴谋诡计，朕终究比不上你啊。",
        "voice": "zh-CN-YunyangNeural",
        "rate": "+0%",
        "zoom_expr": "min(zoom+0.0012,1.22)",
        "x_expr": "iw*0.50-(iw/zoom*0.50)",
        "y_expr": "ih*0.34-(ih/zoom*0.34)",
    },
    {
        "id": "shot05",
        "title": "拔剑阻拦·叹息终局",
        "image_file": "shot05_sword_drawn.png",
        "speaker_badge": "【蜀汉丞相 · 诸葛亮】",
        "badge_color": (78, 205, 140, 255),       # Jade Green
        "dialogue": "皇上……老臣，愧对先帝所托。",
        "voice": "zh-CN-YunjianNeural",
        "rate": "-10%",
        "zoom_expr": "min(zoom+0.0015,1.28)",
        "x_expr": "iw*0.52-(iw/zoom*0.52)",
        "y_expr": "ih*0.38-(ih/zoom*0.38)",
    },
]


def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    out = subprocess.check_output(cmd, text=True).strip()
    return float(out)


async def ensure_audio(shot: dict) -> Path:
    import edge_tts
    audio_path = AUDIO_DIR / f"{shot['id']}_voice.mp3"
    if not audio_path.exists() or audio_path.stat().st_size == 0:
        print(f"  🎙️ 正在合成配音: {shot['speaker_badge']} ({shot['voice']})...")
        communicate = edge_tts.Communicate(shot["dialogue"], shot["voice"], rate=shot["rate"])
        await communicate.save(str(audio_path))
    return audio_path


def create_subtitle_overlay(shot: dict, width: int = 1344, height: int = 768) -> Path:
    sub_path = SUB_DIR / f"{shot['id']}_sub.png"
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    if not Path(font_path).exists():
        font_path = "/System/Library/Fonts/PingFang.ttc"
    
    badge_font = ImageFont.truetype(font_path, 30)
    dialogue_font = ImageFont.truetype(font_path, 36)

    # 1. Measure speaker badge
    badge_text = shot["speaker_badge"]
    b_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    b_w = b_bbox[2] - b_bbox[0]
    b_h = b_bbox[3] - b_bbox[1]

    # 2. Measure dialogue
    diag_text = shot["dialogue"]
    d_bbox = draw.textbbox((0, 0), diag_text, font=dialogue_font)
    d_w = d_bbox[2] - d_bbox[0]
    d_h = d_bbox[3] - d_bbox[1]

    # Layout: Two-tier cinema card (Speaker Tag on top, Dialogue text centered below)
    card_w = max(b_w + 60, d_w + 60)
    card_h = b_h + d_h + 44
    card_x = (width - card_w) // 2
    card_y = height - card_h - 36

    # Translucent frosted dark background
    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=16,
        fill=(10, 10, 15, 185)
    )

    # Draw speaker badge (aligned left inside card)
    badge_x = card_x + 28
    badge_y = card_y + 12
    draw.text((badge_x, badge_y), badge_text, font=badge_font, fill=shot["badge_color"], stroke_width=2, stroke_fill=(0, 0, 0, 255))

    # Draw dialogue text (centered horizontally)
    diag_x = (width - d_w) // 2
    diag_y = badge_y + b_h + 14
    draw.text((diag_x, diag_y), diag_text, font=dialogue_font, fill=(255, 250, 240, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255))

    img.save(sub_path, "PNG")
    return sub_path


def render_shot_clip(shot: dict, duration: float, fps: int = 24) -> Path:
    image_path = ASSETS_DIR / shot["image_file"]
    sub_path = SUB_DIR / f"{shot['id']}_sub.png"
    audio_path = AUDIO_DIR / f"{shot['id']}_voice.mp3"
    clip_path = CLIPS_DIR / f"{shot['id']}.mp4"

    clip_duration = duration + 0.5
    total_frames = int(clip_duration * fps)

    print(f"  🎬 正在压制镜头 [{shot['id']}] {shot['speaker_badge']} 时长: {clip_duration:.2f}s...")

    filter_complex = (
        f"[0:v]scale=2688:1536,"
        f"zoompan=z='{shot['zoom_expr']}':x='{shot['x_expr']}':y='{shot['y_expr']}':"
        f"d={total_frames}:s=1344x768:fps={fps}[bg];"
        f"[bg][1:v]overlay=0:0[vout];"
        f"[2:a]apad=pad_dur=0.5[dialogue];"
        f"[3:a]volume=0.25[ambience];"
        f"[dialogue][ambience]amix=inputs=2:duration=first[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(image_path),
        "-loop", "1", "-i", str(sub_path),
        "-i", str(audio_path),
        "-f", "lavfi", "-i", f"anoisesrc=d={clip_duration + 1}:c=pink:r=24000:a=0.015,lowpass=f=800",
        "-filter_complex", filter_complex,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "19",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{clip_duration:.2f}",
        str(clip_path)
    ]

    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return clip_path


def format_srt_time(sec: float) -> str:
    hrs = int(sec // 3600)
    mins = int((sec % 3600) // 60)
    secs = int(sec % 60)
    millis = int((sec - int(sec)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"


def main():
    print("==================================================")
    print("🎬 《楚氏春秋·开局围宫》 第 1 集影视短剧 v2 全流程重制合成")
    print("==================================================")
    t0 = time.time()

    # 1. Verify Image Assets
    print("🔍 [1/5] 正在校验 5 镜正统汉代画格资产...")
    for s in SHOT_CONFIGS:
        img_p = ASSETS_DIR / s["image_file"]
        if not img_p.exists():
            print(f"❌ 缺少分镜图像资产: {img_p}")
            sys.exit(1)
        print(f"  ✅ 发现分镜画格: {s['id']} -> {s['image_file']} ({img_p.stat().st_size / 1024:.1f} KB)")

    # 2. Generate / Verify Neural Audio
    print("\n🎙️ [2/5] 正在校验多角色配音与音轨时长...")
    async def run_audio():
        for s in SHOT_CONFIGS:
            await ensure_audio(s)
    asyncio.run(run_audio())

    durations = {}
    for s in SHOT_CONFIGS:
        dur = get_audio_duration(AUDIO_DIR / f"{s['id']}_voice.mp3")
        durations[s["id"]] = dur
        print(f"  🎵 {s['id']} {s['speaker_badge']} 音长: {dur:.2f}s")

    # 3. Generate Subtitle Cards (v2 with distinct Speaker Badges)
    print("\n🎨 [3/5] 正在生成电影级角色对白字幕卡 (双层标识)...")
    for s in SHOT_CONFIGS:
        sub_p = create_subtitle_overlay(s)
        print(f"  📝 {s['id']} 字幕已生成: {sub_p.name}")

    # 4. Render Individual Clips
    print("\n⚡ [4/5] 正在执行面部焦点运镜与逐镜压制 (Apple Silicon 加速)...")
    clip_paths = []
    current_time = 0.0
    srt_entries = []

    for idx, s in enumerate(SHOT_CONFIGS, 1):
        dur = durations[s["id"]]
        clip_p = render_shot_clip(s, dur)
        clip_paths.append(clip_p)
        actual_clip_dur = dur + 0.5

        start_srt = format_srt_time(current_time)
        end_srt = format_srt_time(current_time + dur)
        srt_entries.append(f"{idx}\n{start_srt} --> {end_srt}\n{s['speaker_badge']} {s['dialogue']}\n")
        current_time += actual_clip_dur
        print(f"    ✨ 镜头 {s['id']} 压制完成: {clip_p.stat().st_size / 1024:.1f} KB")

    # 5. Concatenate All Clips
    print("\n🎞️ [5/5] 正在执行多镜无损拼接与母带输出...")
    concat_list_file = ASSETS_DIR / "concat_list.txt"
    with open(concat_list_file, "w") as f:
        for p in clip_paths:
            f.write(f"file '{p.resolve()}'\n")

    final_video = SHORT_DRAMA_DIR / "chu_shi_chun_qiu_ep01_final.mp4"
    master_audio = SHORT_DRAMA_DIR / "chu_shi_chun_qiu_ep01_master.mp3"
    srt_file = SHORT_DRAMA_DIR / "chu_shi_chun_qiu_ep01.srt"

    with open(srt_file, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_entries))
    print(f"  📜 独立字幕文件已更新: {srt_file.name}")

    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(final_video)
    ]
    subprocess.check_call(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  🎬 完整成片视频已合成: {final_video.name} ({final_video.stat().st_size / (1024 * 1024):.2f} MB)")

    cmd_audio = [
        "ffmpeg", "-y",
        "-i", str(final_video),
        "-vn", "-c:a", "libmp3lame", "-b:a", "192k",
        str(master_audio)
    ]
    subprocess.check_call(cmd_audio, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  🎧 音频独立母带已提取: {master_audio.name} ({master_audio.stat().st_size / 1024:.1f} KB)")

    total_time = time.time() - t0
    final_dur = get_audio_duration(master_audio)

    print("\n==================================================")
    print(f"🎉 《楚氏春秋》短剧第 1 集 v2 重制合成圆满成功！")
    print(f"⏱️ 总制作耗时     : {total_time:.2f} 秒")
    print(f"⌛ 最终短剧总时长 : {final_dur:.2f} 秒")
    print(f"📹 成片视频路径   : {final_video}")
    print(f"📜 对应字幕路径   : {srt_file}")
    print("==================================================")


if __name__ == "__main__":
    main()
