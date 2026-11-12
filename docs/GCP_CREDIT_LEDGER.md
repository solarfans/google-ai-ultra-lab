# Google Cloud 赠金与 Google AI Ultra 跨池算力总账本 (GCP Credit Ledger)

> **最后更新**：`2026-11-13 00:22 SGT`  
> **关联 GCP 项目**：`project-665ac784-237e-4a71-ad0` (`My Billing Account (Google AI Ultra Main)`)  
> **官方计费折算汇率**：`1 USD = 1.2828 SGD`（按 Google Billing 实盘入账 `US$300 -> SGD 384.83`、`US$100 -> SGD 128.28` 锚定）  
> **付费升级状态（防超额硬熔断）**：**`Paid Billing 未开启（Free Trial 保护态）`** —— 即使赠金耗尽也只会停机/拒绝 API，**0% 信用卡超额扣费风险**  
> **自动维护脚本**：[`scripts/gcp_credit_ledger.py`](../scripts/gcp_credit_ledger.py) | 数据源：[`docs/gcp_credit_ledger.json`](./gcp_credit_ledger.json)

---

## 一、 赠金总览仪表盘（Executive Balance Summary）

| 指标项 | 美元口径 (USD) | 新币口径 (SGD) | 占比 / 到期护栏 |
| :--- | ---: | ---: | :--- |
| **GCP 账面初始赠金总额** | `$400.00` | **`SGD 513.11`** | Free Trial `SGD 384.83` + 2026-11 GDP 月度 `SGD 128.28` |
| **累计已消耗赠金（估算）** | `$19.79` | **`SGD 25.39`** | 含《伊利丹 Ep01》`SGD 23.76` + 双机 VPN 5 天摊销 `SGD 1.63` |
| **当前预计剩余可用总额** | **`$380.21`** | **`SGD 487.72`** | **剩余 `95.05%`**（安全水位 > 80%） |
| ↳ *若优先抵扣 90 天试用赠金* | `$280.20` | `SGD 359.44` (另加月度 `SGD 128.28`) | Free Trial **2027-02-07** 到期清零 |
| ↳ *若优先抵扣 11 月开发者赠金* | `$80.21` | `SGD 102.89` (另加试用 `SGD 384.83`) | GDP 月度福利按月发放 US$100 |

---

## 二、 分池权益清单：GCP 赠金池 vs. 零赠金消耗订阅池

### 2.1 GCP 账单赠金池（消费会扣减本账本余额）

| 赠金池 ID | 名称 | 入账日期 | 到期日 | 初始额度 (USD) | 初始额度 (SGD) | 规则与风控说明 |
| :--- | :--- | :---: | :---: | ---: | ---: | :--- |
| `GCP_FREE_TRIAL_90D` | Google Cloud 90-Day Free Trial Credit | `2026-11-08` | **`2027-02-07`** | `$300.00` | **`SGD 384.83`** | 90-day validity; non-renewable; Paid Upgrade NOT enabled (hard zero-overcharge protection). |
| `GDP_ULTRA_MONTHLY_2026_11` | Google Developer Program Premium Benefit (Ultra Monthly Credit - Nov 2026) | `2026-11-08` | **`2027-11-08`** | `$100.00` | **`SGD 128.28`** | CREDIT_TYPE_MONTHLY applied to My Billing Account via Google Builders Hub. |

> **另注（独立小号）**：Google AI Pro 副账号（`My Billing Account 2`）另有独立 `US$10.00/月` GDP 赠金，专供美西备用 VPN 节点 `node-us-pro-01`（内置 `35GB/月` 流量熔断锁，月耗 `$4~$8`，自给自足，不占用主账号上述额度）。

### 2.2 Google AI Ultra 固定月度订阅池（**`SGD 0.00` 赠金消耗 —— 视频生产默认主力！**）

| 独立配额池 | 调用入口 | 月度额度规则 | 2026-11-13 实测余额 | 重置/刷新时间 | GCP 赠金消耗 |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Google Flow Video Credits (Channel A — Primary Cinema Engine)** | `https://flow.google.com (AGY Persistent Built-in Browser)` | 25,000 credits/mo (non-rollover) | **`25,050 credits`** | `2026-12-07 16:21 SGT` | **`$0.00`** |
| **Google Flow Music Credits (Commercial License)** | `Google Flow Music` | 30,000 credits/mo | **`30,000 credits`** | `Monthly billing cycle` | **`$0.00`** |
| **Colab Enterprise/Pro+ GPU Compute Units (G4 96GB Blackwell)** | `colab-cli / ultra_meter.py` | 2,000 CU/mo (+ rollover) | **`2,477.54 CU (0 active instances, 0.0 CU/h)`** | `Monthly billing cycle` | **`$0.00`** |

---

## 三、 逐笔消费明细流水账（Itemized Transaction Ledger）

| 流水号 | 日期 | 类别 | 关联工程 / 管线 | 调用服务与精确规格明细 | 消费 (USD) | 消费 (SGD) | 授权与备注 |
| :--- | :---: | :--- | :--- | :--- | ---: | ---: | :--- |
| `TX-20261108-001` | `2026-11-08 ~ 2026-11-12` | `INFRA_VPN` | `gcp_dual_node_vpn` | **Compute Engine + VPC Egress (5 days accrued @ ~US$7.60/mo)**<br>5 days × US$0.253/day (node-tw-entry-01 + node-us-exit-01) | `$1.27` | **`SGD 1.63`** | Owner (2026-11-08 VPN deployment) — Ongoing monthly infrastructure (~SGD 9.75/mo), guarded by 250GB/mo traffic_guard.sh. |
| `TX-20261112-002` | `2026-11-12` | `VERTEX_AI_CINEMA` | `pipelines/warcraft_illidan_ep01` | **Vertex AI veo-3.1-generate-001 (1080p + Native Audio) + lyria-002**<br>8 Veo 3.1 clips = 46s raw (shot01 4s, shot02 6s, shot03 4s, shot04 6s, shot05 6s, shot06 6s, shot07 6s, shot08 8s) @ $0.40/s ($18.40) + 2 Lyria-002 30s stems @ $0.06 ($0.12); 0 wasted retries | `$18.52` | **`SGD 23.76`** | Owner (Illidan Ep01 benchmark validation prior to Channel A Flow login) — Delivered 42.10s 1080p Cinema Master. Subsequent episodes switched to Channel A (Google Flow 25,050 monthly credits = $0 GCP spend). |

---

## 四、 官方单价速查表与防超支硬护栏（Unit Pricing & Guardrails）

### 4.1 GCP / Vertex AI 常用服务官方计费基准

| 模型 / 服务项 | 计费单位 | 单价 (USD) | 单价 (SGD) | 生产调度策略 |
| :--- | :---: | ---: | ---: | :--- |
| `veo-3.1-generate-001_1080p_audio` | `per_second` | `$0.40` | `SGD 0.5131` | Vertex AI Channel B flagship Veo 3.1 Quality with native 48kHz audio & lip-sync (LOCKED by default; use Channel A Flow instead). |
| `veo-3.1-fast-generate-001_audio` | `per_second` | `$0.12` | `SGD 0.1539` | Vertex AI Veo 3.1 Fast with audio. |
| `veo-3.1-lite-generate-001` | `per_second` | `$0.08` | `SGD 0.1026` | Vertex AI Veo 3.1 Lite (0 credits on Flow Lower Priority!). |
| `lyria-002_30s_stem` | `per_30s_clip` | `$0.06` | `SGD 0.0770` | Vertex AI Lyria-002 instrumental film score (~$0.12 / SGD 0.15 per 2-stem episode). |
| `gcp_dual_node_vpn_fixed` | `per_month` | `$7.60` | `SGD 9.7500` | node-tw-entry-01 (asia-east1-b e2-micro + static IP) + node-us-exit-01 (us-west1-b Free Tier e2-micro), 250GB/mo cap. |

### 4.2 四条防超额死规（Mandatory Anti-Overrun Guardrails）

1. **视频生成强制走通道 A（`flow.google.com` 网页月度积分池）**：
   - Antigravity 内置浏览器已完成 Google AI Ultra 账号持久化登录（实测可用 **`25,050` Credits**，12 月 7 日清零重置）。
   - 制作电影级短片（`Omni 1.2 Flash` / `Veo 3.1 Quality` / `Veo 3.1 Lite`）**默认 100% 走通道 A**，对 GCP 赠金消耗为 **`$0.00`**。
2. **通道 B（Vertex AI 视频 API）默认上锁**：
   - 未经 Owner 在当前对话中明确批准，**严禁 AGY 私自调用 `veo-3.1-generate-001` API 烧赠金渲染视频**（单集 45 秒约耗 `$18.40` / `SGD 23.60`）。
   - 通道 B 唯一允许日常自动调用的只有 **`lyria-002` 电影交响配乐生成**（每首 30 秒仅 `$0.06` / `SGD 0.08`，整集双轨配乐仅约 `SGD 0.15`，几乎零成本）。
3. **任何 GCP 赠金消耗必须先算账、后执行、当场记账**：
   - 执行前运行 `python3 scripts/gcp_credit_ledger.py estimate ...` 预估金额；
   - 执行后立即运行 `python3 scripts/gcp_credit_ledger.py log ...` 追加流水并重新生成本 Markdown 账本推送到 GitHub。
4. **双层物理防爆仓底线**：
   - GCP `My Billing Account` 保持 **Free Trial 未升级 Paid** 状态；双机 VPN 部署了 `/etc/cron.d/xray-traffic-guard` (`250GB/月` 自动停流脚本)；即使极端误操作也绝不可能触发银行卡扣款。
