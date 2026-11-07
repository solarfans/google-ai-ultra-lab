#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Master Composer for 《楚氏春秋·正传第一卷：杯底波澜》
Takes real dynamic video clips from SVD-XT, synchronizes them with Edge-TTS dialogues,
composites authentic Han-dynasty color-coded subtitle cards, and merges into the final MP4 master.
"""

import os
import json
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SHORT_DRAMA_DIR = ROOT_DIR / "pipelines" / "short_drama"
ASSETS_DIR = SHORT_DRAMA_DIR / "assets"
AUDIO_DIR = ASSETS_DIR / "audio"
SUB_DIR = ASSETS_DIR / "subtitles"
CLIPS_DIR = ASSETS_DIR / "clips"
SPEC_FILE = SHORT_DRAMA_DIR / "chu_shi_chun_qiu_zhengzhuan_ep01.json"

FINAL_MP4 = SHORT_DRAMA_DIR / "chu_shi_chun_qiu_zhengzhuan_ep01_final.mp4"
MASTER_MP3 = SHORT_DRAMA_DIR / "chu_shi_chun_qiu_zhengzhuan_ep01_master.mp3"


def get_media_duration(file_path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ], text=True).strip()
    return float(out)


def main():
    print("==================================================")
    print("🎬 [LOCAL] 楚氏春秋·正传第一卷：杯底波澜 - 成片母带合成")
    print("==================================================")

    with open(SPEC_FILE, "r", encoding="utf-8") as f:
        spec = json.load(f)

    shot_rendered_segments = []

    for shot in spec["shots"]:
        sid = f"shot{shot['shot_id']:02d}"
        clip_mp4 = CLIPS_DIR / f"{sid}_clip.mp4"
        audio_mp3 = AUDIO_DIR / f"{sid}_voice.mp3"
        sub_png = SUB_DIR / f"{sid}_sub.png"

        if not clip_mp4.exists():
            print(f"❌ 缺少视频片段: {clip_mp4}")
            return 1
        if not audio_mp3.exists():
            print(f"❌ 缺少音频文件: {audio_mp3}")
            return 1
        if not sub_png.exists():
            print(f"❌ 缺少字幕画卡: {sub_png}")
            return 1

        audio_dur = get_media_duration(audio_mp3) + 0.5  # pad 0.5s for breath
        seg_mp4 = CLIPS_DIR / f"{sid}_final_seg.mp4"

        print(f"🎞️ [Segment {sid}] 正在合成: 音频时长 {audio_dur:.2f}s...")

        # Loop the clip smoothly or slow it down to match the audio dialogue length
        # Overlay the transparent subtitle card onto the video
        filter_complex = (
            f"[0:v]loop=loop=-1:size=25:start=0,"
            f"scale=1344:768:force_original_aspect_ratio=decrease,pad=1344:768:(ow-iw)/2:(oh-ih)/2[base];"
            f"[1:v]scale=1344:768[sub];"
            f"[base][sub]overlay=0:0[v]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", str(clip_mp4),
            "-i", str(sub_png),
            "-i", str(audio_mp3),
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "2:a",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-t", f"{audio_dur:.2f}",
            "-c:a", "aac",
            "-b:a", "192k",
            str(seg_mp4)
        ]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"   ✅ 分镜片段就绪: {seg_mp4.name}")
        shot_rendered_segments.append(seg_mp4)

    # Concat all segments into the final master MP4
    concat_list_file = SHORT_DRAMA_DIR / "concat_list.txt"
    with open(concat_list_file, "w") as f:
        for seg in shot_rendered_segments:
            f.write(f"file '{seg.resolve()}'\n")

    print("\n📦 正在无损拼接最终完整短剧母带...")
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(FINAL_MP4)
    ]
    subprocess.check_call(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Extract audio master
    extract_audio_cmd = [
        "ffmpeg", "-y",
        "-i", str(FINAL_MP4),
        "-vn", "-c:a", "libmp3lame", "-q:a", "2",
        str(MASTER_MP3)
    ]
    subprocess.check_call(extract_audio_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_dur = get_media_duration(FINAL_MP4)
    size_mb = os.path.getsize(FINAL_MP4) / (1024 * 1024)

    print("==================================================")
    print(f"🎉 最终母带成片合成完毕！")
    print(f"📍 成片路径 : {FINAL_MP4}")
    print(f"⏱️ 成片时长 : {total_dur:.2f} 秒")
    print(f"💾 文件大小 : {size_mb:.2f} MB")
    print("==================================================")
    return 0


if __name__ == "__main__":
    exit(main())
