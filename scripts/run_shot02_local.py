#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Runner for Shot 02 on Colab G4.
Orchestrates remote execution, extracts generated image, and tracks exact CU consumption.
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
    remote_script = root / "scripts" / "render_shot02_remote.py"
    output_asset = root / "pipelines" / "short_drama" / "assets" / "shot02_liushan_portrait.png"
    output_asset.parent.mkdir(parents=True, exist_ok=True)

    print("==================================================")
    print("🎬 《楚氏春秋·外传章》 G4 短剧定妆画格渲染执行器")
    print("==================================================")
    print(f"📄 远程执行脚本 : {remote_script.name}")
    print(f"🎯 目标输出路径 : {output_asset}")

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

    in_b64 = False
    b64_lines = []
    remote_logs = []

    for line in iter(proc.stdout.readline, ""):
        line_s = line.strip()
        if "===BASE64_IMAGE_START===" in line_s:
            in_b64 = True
            continue
        elif "===BASE64_IMAGE_END===" in line_s:
            in_b64 = False
            continue

        if in_b64:
            b64_lines.append(line_s)
        else:
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
    print(f"⏱️ 总耗时           : {total_sec:.1f} 秒 ({total_sec / 60:.2f} 分钟)")
    print(f"💰 任务后算力余额   : {after.get('balance')} CU")
    print(f"📉 实际消耗算力     : {delta:.2f} CU")
    print(f"🖥️ 释放后活跃实例数 : {after.get('active')} (0 代表无任何空跑挂机)")

    # 3. Save Image
    if b64_lines:
        full_b64 = "".join(b64_lines)
        img_bytes = base64.b64decode(full_b64)
        with open(output_asset, "wb") as f:
            f.write(img_bytes)
        file_size_kb = len(img_bytes) / 1024
        print(f"✅ 定妆首帧图像成功拉回本地: {output_asset}")
        print(f"📊 文件大小: {file_size_kb:.2f} KB")
        return 0
    else:
        print("❌ 未能截获生成的 Base64 图像数据！请检查上方云端日志。")
        return returncode if returncode != 0 else 1


if __name__ == "__main__":
    sys.exit(main())
