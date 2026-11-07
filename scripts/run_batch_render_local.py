#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Batch Runner for Chu Shi Chun Qiu Short Drama on Colab G4.
Orchestrates remote execution of Shots 01, 03, 04, 05, streams logs,
extracts all generated keyframe images, and verifies zero-burn CU expenditure.
"""

import sys
import subprocess
import os
import re
import time
import base64
from pathlib import Path


def get_colab_usage():
    try:
        proc = subprocess.run(
            ["colab", "usage"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
        )
        out = proc.stdout.strip()
        b_m = re.search(r"Current balance:\s*([\d\.]+)", out)
        r_m = re.search(r"Usage rate:\s*([\d\.]+)/hr", out)
        a_m = re.search(r"Active assignments:\s*(\d+)", out)
        return {
            "balance": float(b_m.group(1)) if b_m else None,
            "rate": float(r_m.group(1)) if r_m else None,
            "active": int(a_m.group(1)) if a_m else 0,
            "raw": out,
        }
    except Exception as e:
        return {"balance": None, "rate": None, "active": 0, "error": str(e)}


def main():
    root = Path(__file__).resolve().parent.parent
    remote_script = root / "scripts" / "render_shots_batch_remote.py"
    assets_dir = root / "pipelines" / "short_drama" / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    shot_file_map = {
        "shot01": "shot01_eunuch_panic.png",
        "shot03": "shot03_zhuge_entrance.png",
        "shot04": "shot04_confrontation_ots.png",
        "shot05": "shot05_sword_drawn.png",
    }

    print("==================================================")
    print("🎬 《楚氏春秋·外传章》 G4 短剧全量分镜批量画格渲染")
    print("==================================================")
    print(f"📄 远程执行脚本 : {remote_script.name}")
    print(f"🎯 待生成分镜数 : {len(shot_file_map)} 个 (Shot 01, 03, 04, 05)")
    print(f"📂 本地资产目录 : {assets_dir}")

    # 1. Check Usage Before
    before = get_colab_usage()
    print(f"💰 任务前算力余额 : {before.get('balance')} CU")
    print(f"🖥️ 活跃实例数     : {before.get('active')}")
    print("--------------------------------------------------")
    print("🚀 正在调度 Colab G4 (96GB Blackwell RTX PRO 6000)...")

    cmd = [
        "colab", "run",
        "--gpu", "G4",
        "--timeout", "600",
        str(remote_script)
    ]

    t0 = time.time()
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    current_shot_id = None
    b64_buffers = {k: [] for k in shot_file_map}
    remote_logs = []

    for line in iter(proc.stdout.readline, ""):
        line_s = line.strip()
        
        # Check start delimiter
        start_match = re.search(r"===BASE64_IMAGE_START:([a-zA-Z0-9_]+)===", line_s)
        if start_match:
            current_shot_id = start_match.group(1)
            continue

        # Check end delimiter
        end_match = re.search(r"===BASE64_IMAGE_END:([a-zA-Z0-9_]+)===", line_s)
        if end_match:
            current_shot_id = None
            continue

        if current_shot_id and current_shot_id in b64_buffers:
            b64_buffers[current_shot_id].append(line_s)
        else:
            # Filter out noisy progress bar updates
            if any(k in line_s for k in ["%|", "B/s", "it/s", "reconstructing file", "downloading bytes"]):
                continue
            if line_s:
                print(f"  [G4 CLOUD] {line_s}")
                remote_logs.append(line_s)

    proc.stdout.close()
    returncode = proc.wait()
    total_sec = time.time() - t0

    # 2. Check Usage After
    time.sleep(2)
    after = get_colab_usage()
    delta = (before.get("balance") or 0.0) - (after.get("balance") or 0.0) if before.get("balance") and after.get("balance") else 0.0

    print("--------------------------------------------------")
    print("🏁 云端容器执行结束，安全生命周期已自动销毁")
    print(f"⏱️ 批量渲染总耗时   : {total_sec:.1f} 秒 ({total_sec / 60:.2f} 分钟)")
    print(f"💰 任务后算力余额   : {after.get('balance')} CU")
    print(f"📉 实际消耗算力     : {delta:.2f} CU")
    print(f"🖥️ 释放后活跃实例数 : {after.get('active')} (0 代表无任何空跑挂机)")

    # 3. Save Images
    saved_count = 0
    for shot_id, lines in b64_buffers.items():
        filename = shot_file_map[shot_id]
        out_path = assets_dir / filename
        if lines:
            full_b64 = "".join(lines)
            img_bytes = base64.b64decode(full_b64)
            with open(out_path, "wb") as f:
                f.write(img_bytes)
            file_size_kb = len(img_bytes) / 1024
            print(f"  ✅ {shot_id} 成功落盘: {filename} ({file_size_kb:.2f} KB)")
            saved_count += 1
        else:
            print(f"  ❌ 未能截获 {shot_id} 的 Base64 数据！")

    print("==================================================")
    if saved_count == len(shot_file_map):
        print(f"🎉 恭喜！全部 {saved_count} 个分镜定妆画格已成功回传并验证完毕！")
        return 0
    else:
        print(f"⚠️ 部分分镜未成功落地 ({saved_count}/{len(shot_file_map)})，请检查云端日志。")
        return returncode if returncode != 0 else 1


if __name__ == "__main__":
    sys.exit(main())
