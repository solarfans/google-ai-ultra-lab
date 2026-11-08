#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Master Composer for 《楚氏春秋·正传第一卷：杯底波澜》 (Qwen-Image + MiniMax-H3 Engine)
Composites 1344x768 video clips, dialogue audio, subtitles, and character badges into the final MP4 master.
Zero CCU spent on Colab GPU; 100% executed locally on Apple Silicon.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SHORT_DRAMA_DIR = ROOT_DIR / "pipelines" / "short_drama"
ASSETS_DIR = SHORT_DRAMA_DIR / "assets"
AUDIO_DIR = ASSETS_DIR / "audio"
SUB_DIR = ASSETS_DIR / "subtitles"
CLIPS_DIR = ASSETS_DIR / "clips"
SPEC_FILE = SHORT_DRAMA_DIR / "chu_shi_chun_qiu_ep01_beizhao_chushi.json"

FINAL_MP4 = SHORT_DRAMA_DIR / "chu_shi_chun_qiu_ep01_qwen_minimax_master.mp4"
FINAL_SRT = SHORT_DRAMA_DIR / "chu_shi_chun_qiu_ep01_qwen_minimax_master.srt"


def get_media_duration(file_path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)
    ], text=True).strip()
    return float(out)


def main():
    print("==================================================")
    print("🎬 [LOCAL] 楚氏春秋·正传第一卷：杯底波澜")
    print("🔥 Qwen-Image + MiniMax-H3 最终母带合成引擎")
    print("==================================================")

    if not SPEC_FILE.exists():
        print(f"❌ 剧本配置文件未找到: {SPEC_FILE}")
        return 1

    with open(SPEC_FILE, "r", encoding="utf-8") as f:
        spec = json.load(f)

    shot_rendered_segments = []
    srt_entries = []
    timeline_sec = 0.0

    for shot in spec["shots"]:
        sid = f"shot{shot['shot_id']:02d}"
        clip_mp4 = CLIPS_DIR / f"{sid}_clip.mp4"
        audio_mp3 = AUDIO_DIR / f"{sid}_voice.mp3"
        sub_png = SUB_DIR / f"{sid}_sub.png"

        if not clip_mp4.exists():
            print(f"❌ 缺少视频片段: {clip_mp4}")
            return 1

        # Use voice audio if present, otherwise calculate from clip or spec duration
        has_audio = audio_mp3.exists()
        if has_audio:
            dur = get_media_duration(audio_mp3) + 0.5
        else:
            dur = shot.get("duration_sec", 4.0)

        # Build SRT entry if dialogue is present
        line = shot.get("dialogue_line")
        speaker_name = spec.get("characters", {}).get(shot.get("speaker"), {}).get("name_zh", "旁白") if shot.get("speaker") else "旁白"
        if line:
            start_str = f"{int(timeline_sec // 3600):02d}:{int((timeline_sec % 3600) // 60):02d}:{int(timeline_sec % 60):02d},000"
            end_t = timeline_sec + dur
            end_str = f"{int(end_t // 3600):02d}:{int((end_t % 3600) // 60):02d}:{int(end_t % 60):02d},000"
            srt_entries.append(
                f"{len(srt_entries) + 1}\n{start_str} --> {end_str}\n【{speaker_name}】{line}\n"
            )

        seg_mp4 = CLIPS_DIR / f"{sid}_qwen_minimax_seg.mp4"
        print(f"🎞️ [Segment {sid}] 合成中: 时长 {dur:.2f}s | 角色: {speaker_name}...")

        # Compose clip with subtitle card (if present) and audio
        if sub_png.exists():
            filter_complex = (
                f"[0:v]loop=loop=-1:size=25:start=0,"
                f"scale=1344:768:force_original_aspect_ratio=decrease,pad=1344:768:(ow-iw)/2:(oh-ih)/2[base];"
                f"[1:v]scale=1344:768[sub];"
                f"[base][sub]overlay=0:0[v]"
            )
            inputs = ["-i", str(clip_mp4), "-i", str(sub_png)]
        else:
            filter_complex = (
                f"[0:v]loop=loop=-1:size=25:start=0,"
                f"scale=1344:768:force_original_aspect_ratio=decrease,pad=1344:768:(ow-iw)/2:(oh-ih)/2[v]"
            )
            inputs = ["-i", str(clip_mp4)]

        if has_audio:
            cmd = [
                "ffmpeg", "-y",
                *inputs,
                "-i", str(audio_mp3),
                "-filter_complex", filter_complex,
                "-map", "[v]",
                "-map", f"{len(inputs)//2}:a",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-t", f"{dur:.2f}",
                "-c:a", "aac",
                "-b:a", "192k",
                str(seg_mp4)
            ]
        else:
            cmd = [
                "ffmpeg", "-y",
                *inputs,
                "-filter_complex", filter_complex,
                "-map", "[v]",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-t", f"{dur:.2f}",
                str(seg_mp4)
            ]

        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        shot_rendered_segments.append(seg_mp4)
        timeline_sec += dur

    # Concat all segments into master MP4
    concat_list_file = SHORT_DRAMA_DIR / "concat_qwen_minimax.txt"
    with open(concat_list_file, "w") as f:
        for seg in shot_rendered_segments:
            f.write(f"file '{seg.resolve()}'\n")

    print(f"\n📦 正在拼接最终 1344x768 母带短剧 (总时长: {timeline_sec:.2f}s)...")
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(FINAL_MP4)
    ]
    subprocess.check_call(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    concat_list_file.unlink(missing_ok=True)

    # Save master SRT
    with open(FINAL_SRT, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_entries))

    mp4_size_mb = os.path.getsize(FINAL_MP4) / (1024 * 1024)
    print("==================================================")
    print(f"🎉 [SUCCESS] 最终短剧母带合成成功！")
    print(f"🎬 成片路径: {FINAL_MP4.name} ({mp4_size_mb:.2f} MB)")
    print(f"📝 外挂字幕: {FINAL_SRT.name}")
    print(f"⏱️ 总时长  : {timeline_sec:.2f} 秒")
    print("==================================================")
    return 0


if __name__ == "__main__":
    sys.exit(main())
