#!/usr/bin/env python3
"""
gcp_credit_ledger.py — Deterministic Google Cloud Credit & Ultra Quota Ledger Manager

Maintains `docs/gcp_credit_ledger.json` and auto-generates `docs/GCP_CREDIT_LEDGER.md`
so every dollar of GCP Free Trial (SGD 384.83, expires 2027-02-07) and GDP Monthly
Credits (SGD 128.28/mo) is tracked with line-item precision and hard budget guardrails.

Usage:
  python3 scripts/gcp_credit_ledger.py status
  python3 scripts/gcp_credit_ledger.py render
  python3 scripts/gcp_credit_ledger.py estimate --veo31-sec 46 --lyria-clips 2
  python3 scripts/gcp_credit_ledger.py log --category VERTEX_AI_SCORE --pipeline warcraft_ep02 \
      --service "Vertex AI lyria-002" --detail "2 stems @ $0.06" --usd 0.12 --notes "Ep02 score"
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = REPO_ROOT / "docs" / "gcp_credit_ledger.json"
MD_PATH = REPO_ROOT / "docs" / "GCP_CREDIT_LEDGER.md"


def load_ledger() -> dict:
    with JSON_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_ledger(data: dict) -> None:
    data["meta"]["last_updated_sgt"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M SGT")
    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def compute_totals(data: dict) -> dict:
    total_init_usd = sum(p["initial_usd"] for p in data["gcp_credit_pools"])
    total_init_sgd = sum(p["initial_sgd"] for p in data["gcp_credit_pools"])
    spent_usd = round(sum(t["usd"] for t in data["transactions"]), 2)
    spent_sgd = round(sum(t["sgd"] for t in data["transactions"]), 2)
    rem_usd = round(total_init_usd - spent_usd, 2)
    rem_sgd = round(total_init_sgd - spent_sgd, 2)
    pct_rem = round((rem_sgd / total_init_sgd) * 100.0, 2) if total_init_sgd else 0.0

    trial_pool = next(p for p in data["gcp_credit_pools"] if p["pool_id"] == "GCP_FREE_TRIAL_90D")
    gdp_pool = next(p for p in data["gcp_credit_pools"] if p["pool_id"] == "GDP_ULTRA_MONTHLY_2026_11")

    return {
        "total_init_usd": total_init_usd,
        "total_init_sgd": total_init_sgd,
        "spent_usd": spent_usd,
        "spent_sgd": spent_sgd,
        "rem_usd": rem_usd,
        "rem_sgd": rem_sgd,
        "pct_rem": pct_rem,
        "trial_if_first_sgd": round(max(0.0, trial_pool["initial_sgd"] - spent_sgd), 2),
        "gdp_if_first_sgd": round(max(0.0, gdp_pool["initial_sgd"] - spent_sgd), 2),
    }


def render_markdown(data: dict) -> str:
    t = compute_totals(data)
    meta = data["meta"]

    lines = [
        "# Google Cloud 赠金与 Google AI Ultra 跨池算力总账本 (GCP Credit Ledger)",
        "",
        f"> **最后更新**：`{meta['last_updated_sgt']}`  ",
        f"> **关联 GCP 项目**：`{meta['project_id']}` (`{meta['billing_account_label']}`)  ",
        f"> **官方计费折算汇率**：`1 USD = {meta['fx_usd_to_sgd']} SGD`（按 Google Billing 实盘入账 `US$300 -> SGD 384.83`、`US$100 -> SGD 128.28` 锚定）  ",
        f"> **付费升级状态（防超额硬熔断）**：**`Paid Billing 未开启（Free Trial 保护态）`** —— 即使赠金耗尽也只会停机/拒绝 API，**0% 信用卡超额扣费风险**  ",
        "> **自动维护脚本**：[`scripts/gcp_credit_ledger.py`](../scripts/gcp_credit_ledger.py) | 数据源：[`docs/gcp_credit_ledger.json`](./gcp_credit_ledger.json)",
        "",
        "---",
        "",
        "## 一、 赠金总览仪表盘（Executive Balance Summary）",
        "",
        "| 指标项 | 美元口径 (USD) | 新币口径 (SGD) | 占比 / 到期护栏 |",
        "| :--- | ---: | ---: | :--- |",
        f"| **GCP 账面初始赠金总额** | `${t['total_init_usd']:.2f}` | **`SGD {t['total_init_sgd']:.2f}`** | Free Trial `SGD 384.83` + 2026-11 GDP 月度 `SGD 128.28` |",
        f"| **累计已消耗赠金（估算）** | `${t['spent_usd']:.2f}` | **`SGD {t['spent_sgd']:.2f}`** | 含《伊利丹 Ep01》`SGD 23.76` + 双机 VPN 5 天摊销 `SGD 1.63` |",
        f"| **当前预计剩余可用总额** | **`${t['rem_usd']:.2f}`** | **`SGD {t['rem_sgd']:.2f}`** | **剩余 `{t['pct_rem']:.2f}%`**（安全水位 > 80%） |",
        f"| ↳ *若优先抵扣 90 天试用赠金* | `${t['trial_if_first_sgd'] / meta['fx_usd_to_sgd']:.2f}` | `SGD {t['trial_if_first_sgd']:.2f}` (另加月度 `SGD 128.28`) | Free Trial **2027-02-07** 到期清零 |",
        f"| ↳ *若优先抵扣 11 月开发者赠金* | `${t['gdp_if_first_sgd'] / meta['fx_usd_to_sgd']:.2f}` | `SGD {t['gdp_if_first_sgd']:.2f}` (另加试用 `SGD 384.83`) | GDP 月度福利按月发放 US$100 |",
        "",
        "---",
        "",
        "## 二、 分池权益清单：GCP 赠金池 vs. 零赠金消耗订阅池",
        "",
        "### 2.1 GCP 账单赠金池（消费会扣减本账本余额）",
        "",
        "| 赠金池 ID | 名称 | 入账日期 | 到期日 | 初始额度 (USD) | 初始额度 (SGD) | 规则与风控说明 |",
        "| :--- | :--- | :---: | :---: | ---: | ---: | :--- |",
    ]

    for p in data["gcp_credit_pools"]:
        lines.append(
            f"| `{p['pool_id']}` | {p['name']} | `{p['granted_date']}` | **`{p['expires_date']}`** | "
            f"`${p['initial_usd']:.2f}` | **`SGD {p['initial_sgd']:.2f}`** | {p['notes']} |"
        )

    lines.extend([
        "",
        "> **另注（独立小号）**：Google AI Pro 副账号（`My Billing Account 2`）另有独立 `US$10.00/月` GDP 赠金，专供美西备用 VPN 节点 `node-us-pro-01`（内置 `35GB/月` 流量熔断锁，月耗 `$4~$8`，自给自足，不占用主账号上述额度）。",
        "",
        "### 2.2 Google AI Ultra 固定月度订阅池（**`SGD 0.00` 赠金消耗 —— 视频生产默认主力！**）",
        "",
        "| 独立配额池 | 调用入口 | 月度额度规则 | 2026-11-13 实测余额 | 重置/刷新时间 | GCP 赠金消耗 |",
        "| :--- | :--- | :--- | :--- | :--- | :---: |",
    ])

    for q in data["non_gcp_ultra_quotas"]:
        lines.append(
            f"| **{q['name']}** | `{q['surface']}` | {q['monthly_allowance']} | **`{q['verified_balance']}`** | `{q['resets_at']}` | **`{q['gcp_burn']}`** |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 三、 逐笔消费明细流水账（Itemized Transaction Ledger）",
        "",
        "| 流水号 | 日期 | 类别 | 关联工程 / 管线 | 调用服务与精确规格明细 | 消费 (USD) | 消费 (SGD) | 授权与备注 |",
        "| :--- | :---: | :--- | :--- | :--- | ---: | ---: | :--- |",
    ])

    for tx in data["transactions"]:
        lines.append(
            f"| `{tx['tx_id']}` | `{tx['date']}` | `{tx['category']}` | `{tx['project_or_pipeline']}` | "
            f"**{tx['service']}**<br>{tx['quantity_detail']} | `${tx['usd']:.2f}` | **`SGD {tx['sgd']:.2f}`** | "
            f"{tx['authorized_by']} — {tx['notes']} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 四、 官方单价速查表与防超支硬护栏（Unit Pricing & Guardrails）",
        "",
        "### 4.1 GCP / Vertex AI 常用服务官方计费基准",
        "",
        "| 模型 / 服务项 | 计费单位 | 单价 (USD) | 单价 (SGD) | 生产调度策略 |",
        "| :--- | :---: | ---: | ---: | :--- |",
    ])

    for key, info in data["unit_pricing_reference_usd"].items():
        lines.append(
            f"| `{key}` | `{info['unit']}` | `${info['usd']:.2f}` | `SGD {info['sgd']:.4f}` | {info['notes']} |"
        )

    lines.extend([
        "",
        "### 4.2 四条防超额死规（Mandatory Anti-Overrun Guardrails）",
        "",
        "1. **视频生成强制走通道 A（`flow.google.com` 网页月度积分池）**：",
        "   - Antigravity 内置浏览器已完成 Google AI Ultra 账号持久化登录（实测可用 **`25,050` Credits**，12 月 7 日清零重置）。",
        "   - 制作电影级短片（`Omni 1.2 Flash` / `Veo 3.1 Quality` / `Veo 3.1 Lite`）**默认 100% 走通道 A**，对 GCP 赠金消耗为 **`$0.00`**。",
        "2. **通道 B（Vertex AI 视频 API）默认上锁**：",
        "   - 未经 Owner 在当前对话中明确批准，**严禁 AGY 私自调用 `veo-3.1-generate-001` API 烧赠金渲染视频**（单集 45 秒约耗 `$18.40` / `SGD 23.60`）。",
        "   - 通道 B 唯一允许日常自动调用的只有 **`lyria-002` 电影交响配乐生成**（每首 30 秒仅 `$0.06` / `SGD 0.08`，整集双轨配乐仅约 `SGD 0.15`，几乎零成本）。",
        "3. **任何 GCP 赠金消耗必须先算账、后执行、当场记账**：",
        "   - 执行前运行 `python3 scripts/gcp_credit_ledger.py estimate ...` 预估金额；",
        "   - 执行后立即运行 `python3 scripts/gcp_credit_ledger.py log ...` 追加流水并重新生成本 Markdown 账本推送到 GitHub。",
        "4. **双层物理防爆仓底线**：",
        "   - GCP `My Billing Account` 保持 **Free Trial 未升级 Paid** 状态；双机 VPN 部署了 `/etc/cron.d/xray-traffic-guard` (`250GB/月` 自动停流脚本)；即使极端误操作也绝不可能触发银行卡扣款。",
        "",
    ])

    return "\n".join(lines)


def cmd_status(data: dict) -> None:
    t = compute_totals(data)
    print("==========================================================")
    print("💳 Google Cloud Credit & AI Ultra Quota Ledger")
    print("==========================================================")
    print(f"Initial GCP Credits : USD ${t['total_init_usd']:.2f}  (SGD {t['total_init_sgd']:.2f})")
    print(f"Cumulative Spend    : USD ${t['spent_usd']:.2f}  (SGD {t['spent_sgd']:.2f})")
    print(f"Estimated Remaining : USD ${t['rem_usd']:.2f}  (SGD {t['rem_sgd']:.2f} | {t['pct_rem']:.2f}%)")
    print("----------------------------------------------------------")
    print("Zero-GCP-Burn Monthly Pools:")
    for q in data["non_gcp_ultra_quotas"]:
        print(f"  • {q['name']}: {q['verified_balance']} (Resets: {q['resets_at']})")
    print("==========================================================")


def main() -> None:
    parser = argparse.ArgumentParser(description="GCP Credit Ledger Manager")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("status", help="Print current GCP credit balance & Ultra quotas")
    sub.add_parser("render", help="Regenerate docs/GCP_CREDIT_LEDGER.md from JSON")

    est = sub.add_parser("estimate", help="Estimate Vertex AI spend before running")
    est.add_argument("--veo31-sec", type=float, default=0.0)
    est.add_argument("--veo31-fast-sec", type=float, default=0.0)
    est.add_argument("--lyria-clips", type=int, default=0)

    log_p = sub.add_parser("log", help="Append a new GCP credit expenditure transaction")
    log_p.add_argument("--date", default=dt.date.today().isoformat())
    log_p.add_argument("--category", required=True)
    log_p.add_argument("--pipeline", required=True)
    log_p.add_argument("--service", required=True)
    log_p.add_argument("--detail", required=True)
    log_p.add_argument("--usd", type=float, required=True)
    log_p.add_argument("--auth", default="Owner")
    log_p.add_argument("--notes", default="")

    args = parser.parse_args()
    data = load_ledger()

    if args.cmd in (None, "status"):
        cmd_status(data)
    elif args.cmd == "render":
        MD_PATH.write_text(render_markdown(data), encoding="utf-8")
        print(f"Rendered {MD_PATH}")
        cmd_status(data)
    elif args.cmd == "estimate":
        fx = data["meta"]["fx_usd_to_sgd"]
        usd = round(args.veo31_sec * 0.40 + args.veo31_fast_sec * 0.12 + args.lyria_clips * 0.06, 2)
        sgd = round(usd * fx, 2)
        print(f"Estimated Spend: USD ${usd:.2f} (SGD {sgd:.2f})")
    elif args.cmd == "log":
        fx = data["meta"]["fx_usd_to_sgd"]
        seq = len(data["transactions"]) + 1
        tx_id = f"TX-{args.date.replace('-', '')}-{seq:03d}"
        sgd = round(args.usd * fx, 2)
        data["transactions"].append({
            "tx_id": tx_id,
            "date": args.date,
            "category": args.category,
            "project_or_pipeline": args.pipeline,
            "service": args.service,
            "quantity_detail": args.detail,
            "usd": round(args.usd, 2),
            "sgd": sgd,
            "authorized_by": args.auth,
            "notes": args.notes,
        })
        save_ledger(data)
        MD_PATH.write_text(render_markdown(data), encoding="utf-8")
        print(f"Logged {tx_id}: USD ${args.usd:.2f} (SGD {sgd:.2f}) and updated {MD_PATH}")
        cmd_status(data)


if __name__ == "__main__":
    main()
