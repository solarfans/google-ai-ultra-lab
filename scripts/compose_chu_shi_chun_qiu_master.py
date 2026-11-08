#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Composer for 《楚氏春秋·第一集：空难惊魂·异界重生》
Delivers Full 6-Shot Cinematic Episode:
- Shot 01: Modern Boeing disaster turbulence, lightning, red emergency alarm
- Shot 02: Desperate outgoing text message & colossal ocean crash
- Shot 03: Ancient Taishou mansion bedroom, carved canopy bed, incense smoke
- Shot 04: Noble mother Madam Chu weeping by bed praying
- Shot 05: 9-year-old Chu Zheng (featuring user's 9yo son with cheek mole) waking up looking at hands
- Shot 06: 9-year-old Chu Zheng (featuring user's 9yo son in blue silk robes) looking out window at 100,000 army

Full sound design: engine roar, alarms, heartbeat, ocean crash, chimes, weeping strings, war drums!
"""

import os
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PIPELINES_DIR = ROOT_DIR / "pipelines" / "short_drama"
ASSETS_DIR = PIPELINES_DIR / "assets"
AUDIO_DIR = ASSETS_DIR / "audio"
SUB_DIR = ASSETS_DIR / "subtitles"
CLIPS_DIR = ASSETS_DIR / "clips"
CLIPS_DIR.mkdir(parents=True, exist_ok=True)

FINAL_MASTER_MP4 = PIPELINES_DIR / "chu_shi_chun_qiu_ep01_full_master.mp4"
FINAL_MASTER_SRT = PIPELINES_DIR / "chu_shi_chun_qiu_ep01_full_master.srt"

SHOT_SPECS = [
    {
        "id": 1,
        "name": "shot01",
        "title": "现代客机空难·剧烈失重与红光闪烁",
        "speaker": "旁白",
        "text": "两万米高空，波音客机遭遇恐怖气流剧烈失控，机身撕裂，红光狂闪！",
        "dur": 7.632,
        "filter": (
            "[0:v]scale=1460:834,"
            "crop=1344:768:'(in_w-out_w)/2 + 24*sin(t*8.5)':'(in_h-out_h)/2 + 16*cos(t*10.0)',"
            "eq=brightness='0.08*sin(t*12.0)*gte(sin(t*12.0),0.6)'[bg];"
            "[1:v]scale=1344:768[sub];"
            "[bg][sub]overlay=0:0[v]"
        )
    },
    {
        "id": 2,
        "name": "shot02",
        "title": "绝命短信·客机轰然坠海",
        "speaker": "现代楚铮",
        "text": "我颤抖着按出最后一条短信：我爱你，永别了……下一秒，飞机撞入无尽黑夜！",
        "dur": 6.888,
        "filter": (
            "[0:v]scale=1480:846,"
            "crop=1344:768:'(in_w-out_w)/2 + 10*sin(t*1.5)':'(in_h-out_h)/2 + 15*cos(t*1.2) + 22*sin((t-4.8)*28)*gte(t,4.8)',"
            "eq=contrast='1.0 + 0.15*gte(t,4.8)*sin((t-4.8)*30)'[bg];"
            "[1:v]scale=1344:768[sub];"
            "[bg][sub]overlay=0:0[v]"
        )
    },
    {
        "id": 3,
        "name": "shot03",
        "title": "时空流转·古朴太守府卧房",
        "speaker": "旁白",
        "text": "黑暗吞噬了所有意识……再睁开眼，已是古色古香的太守府雕花大床！",
        "dur": 7.032,
        "filter": (
            "[0:v]scale=1460:834,"
            "crop=1344:768:'(in_w-out_w)*(t/7.032)':'(in_h-out_h)/2'[bg];"
            "[1:v]scale=1344:768[sub];"
            "[bg][sub]overlay=0:0[v]"
        )
    },
    {
        "id": "shot04",
        "name": "shot04",
        "title": "母爱泣血·楚夫人跪地磕头求神",
        "speaker": "楚夫人",
        "text": "大仙开恩！放过我孩儿吧！有什么罪全报应在我身上，只要他能活下来！",
        "dur": 7.056,
        "filter": (
            "[0:v]scale=1440:822,"
            "crop=1344:768:'(in_w-out_w)/2':'(in_h-out_h)*(t/7.056)'[bg];"
            "[1:v]scale=1344:768[sub];"
            "[bg][sub]overlay=0:0[v]"
        )
    },
    {
        "id": "shot05",
        "name": "shot05",
        "title": "抚面惊醒·现代灵魂入主幼童身躯",
        "speaker": "楚铮（9岁）",
        "text": "这双幼小的手……这不是我的身体！飞机坠海，我竟然穿越了？！",
        "dur": 6.288,
        "filter": (
            "[0:v]scale=1480:846,"
            "crop=1344:768:'(in_w-out_w)/2 + 6*sin(t*2.0)':'(in_h-out_h)*(1 - 0.45*t/6.288)'[bg];"
            "[1:v]scale=1344:768[sub];"
            "[bg][sub]overlay=0:0[v]"
        )
    },
    {
        "id": "shot06",
        "name": "shot06",
        "title": "推窗放眼·北赵第一豪门霸业启程",
        "speaker": "旁白",
        "text": "北越平原城，手握十万重兵的第一世家。这一世，我为楚五公子！",
        "dur": 7.296,
        "filter": (
            "[0:v]scale=1480:846,"
            "crop=1344:768:'(in_w-out_w)*(1 - t/7.296)':'(in_h-out_h)/2'[bg];"
            "[1:v]scale=1344:768[sub];"
            "[bg][sub]overlay=0:0[v]"
        )
    }
]


def render_segments():
    print("==================================================")
    print("🎬 [MASTER COMPOSER] 楚氏春秋·第一集：空难惊魂·异界重生")
    print("🔥 院线级短剧母带合成引擎 (6镜完整叙事 + 真实家庭角色融合)")
    print("==================================================")

    rendered_segments = []
    srt_lines = []
    timeline_sec = 0.0

    for idx, spec in enumerate(SHOT_SPECS, 1):
        sid = f"shot{idx:02d}"
        keyframe_png = ASSETS_DIR / f"{sid}_keyframe.png"
        audio_mixed = AUDIO_DIR / f"{sid}_mixed.mp3"
        sub_png = SUB_DIR / f"{sid}_sub.png"
        seg_mp4 = CLIPS_DIR / f"{sid}_master_seg.mp4"

        dur = spec["dur"]
        print(f"🎞️ [Segment {idx}/6] 正在渲染 {spec['title']} (时长 {dur:.2f}s)...")

        # Build SRT entry
        start_str = f"{int(timeline_sec // 3600):02d}:{int((timeline_sec % 3600) // 60):02d}:{int(timeline_sec % 60):02d},{int((timeline_sec % 1) * 1000):03d}"
        end_t = timeline_sec + dur
        end_str = f"{int(end_t // 3600):02d}:{int((end_t % 3600) // 60):02d}:{int(end_t % 60):02d},{int((end_t % 1) * 1000):03d}"
        srt_lines.append(f"{idx}\n{start_str} --> {end_str}\n【{spec['speaker']}】{spec['text']}\n")

        # Render segment video via ffmpeg
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(keyframe_png),
            "-loop", "1", "-i", str(sub_png),
            "-i", str(audio_mixed),
            "-filter_complex", spec["filter"],
            "-map", "[v]",
            "-map", "2:a",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-t", f"{dur:.3f}",
            "-c:a", "aac",
            "-b:a", "192k",
            str(seg_mp4)
        ]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        rendered_segments.append(seg_mp4)
        timeline_sec += dur
        print(f"   ✅ 完成分镜片段: {seg_mp4.name} (1344x768 @ 30fps)")

    # Save SRT
    FINAL_MASTER_SRT.write_text("\n".join(srt_lines), encoding="utf-8")
    print(f"\n📝 [SRT] 字幕文件已写入: {FINAL_MASTER_SRT.name}")

    # Concatenate all 6 segments
    concat_txt = CLIPS_DIR / "master_concat_list.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for seg in rendered_segments:
            f.write(f"file '{seg.resolve()}'\n")

    print(f"\n🎞️ [CONCAT] 正在无缝拼接 6 大分镜为最终院线母带...")
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(FINAL_MASTER_MP4)
    ]
    subprocess.check_call(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_size_mb = FINAL_MASTER_MP4.stat().st_size / (1024 * 1024)
    print("==================================================")
    print(f"🎉🎉🎉 母带交付完成: {FINAL_MASTER_MP4.name}")
    print(f"📊 总时长: {timeline_sec:.2f} 秒 | 视频分辨率: 1344x768 (16:9)")
    print(f"📦 文件大小: {total_size_mb:.2f} MB | 音频: 双声道 AAC 192k")
    print(f"📍 存储路径: {FINAL_MASTER_MP4}")
    print("==================================================")
    return 0


if __name__ == "__main__":
    sys.exit(render_segments())
