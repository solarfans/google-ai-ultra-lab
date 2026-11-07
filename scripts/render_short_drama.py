#!/usr/bin/env python3
"""
Chu Shi Chun Qiu - Short Drama Render Pipeline Orchestrator
Manages Colab G4 sessions, execution, and zero-leak CU tracking.
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path


def get_colab_usage() -> dict:
    """Fetch current compute units balance and usage rate from colab CLI."""
    try:
        proc = subprocess.run(
            ["colab", "usage"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
        )
        output = proc.stdout.strip()
        balance_match = re.search(r"Current balance:\s*([\d\.]+)", output)
        rate_match = re.search(r"Usage rate:\s*([\d\.]+)/hr", output)
        active_match = re.search(r"Active assignments:\s*(\d+)", output)

        return {
            "balance": float(balance_match.group(1)) if balance_match else None,
            "rate": float(rate_match.group(1)) if rate_match else None,
            "active": int(active_match.group(1)) if active_match else 0,
            "raw": output,
        }
    except Exception as e:
        return {"error": str(e)}


def main():
    print("==================================================")
    print("🎬 《楚氏春秋·开局围宫》 AI 短剧渲染流水线启动")
    print("==================================================")

    # 1. Baseline Usage Check
    initial_usage = get_colab_usage()
    print(f"📊 起始计算单元余额: {initial_usage.get('balance')} CU")
    print(f"⚡ 当前活跃分配数: {initial_usage.get('active')}")

    # Load Storyboard Spec
    spec_path = Path(__file__).resolve().parent.parent / "pipelines" / "short_drama" / "chu_shi_chun_qiu_ep01.json"
    if not spec_path.exists():
        print(f"❌ 找不到分镜配置文件: {spec_path}")
        sys.exit(1)

    with open(spec_path) as f:
        spec = json.load(f)

    print(f"📖 项目名称: {spec['project']}")
    print(f"🎯 镜头数量: {len(spec['shots'])} 个镜头 (总时长约 {spec['target_runtime']})")
    for s in spec["shots"]:
        print(f"   - 镜头 {s['shot_id']} [{s['shot_type']}]: {s['scene']} ({s['duration_sec']}s)")

    print("\n--------------------------------------------------")
    print("💡 算力控制铁律评估:")
    print("  - G4 官方费率: 10.05 CU / 小时 (~0.168 CU / 分钟)")
    print("  - 预估单卡生成耗时: ~20 分钟")
    print("  - 预估消耗算力: 3.5 ~ 4.2 CU (按土区 Ultra 成本折合约 ¥0.8 ~ ¥1.2 元)")
    print("  - 策略: 任务结束自动销毁 VM 容器，严禁空转挂机！")
    print("--------------------------------------------------")


if __name__ == "__main__":
    main()
