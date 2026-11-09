# Google AI Ultra Lab — Current State & Ledger

**最后更新**：2026-11-09 15:35 SGT (MacBook Pro)  
**项目状态**：`AI_MANJU_SOP_V2_SOLIDIFIED / GCP_ULTRA_AND_PRO_VPN_MATRIX_VERIFIED / ZERO_BURN_SAFE`  
**负责席位**：Antigravity Desktop (MacBook)  
**核心操作总纲**：[**docs/AI_MANJU_AND_ULTRA_SOP.md**](./docs/AI_MANJU_AND_ULTRA_SOP.md)  

---

## 1. 订阅与权益状态清单

| 权益项目 | 官方标称/社区数据 | 当前实测状态 | 验证方式/凭据 |
| :--- | :--- | :--- | :--- |
| **会员级别** | Google AI Ultra 30 TB |  **已确认** | Google One 首页已显示 "Google AI Ultra, 30 TB" (Melvin Guo) |
| **订阅成本** | ₺2,949.99 / 月 |  **已确认** | Apple 订阅页面截图证实，12 月 7 日自动续费 |
| **YouTube Premium** | 个人与品牌频道会员 |  **已确认** | 个人身份与 yoursolar 品牌频道均显示 Premium 标识 |
| **Colab 算力** | 约 2,000 ~ 2,500 CU/月 |  **已确认 (2,497.44 CU)** | `colab usage` 回读当前余额：2,497.44 CU，活跃实例 0 |
| **G4 96GB GPU** | NVIDIA RTX PRO 6000 Ada/Blackwell |  **已验证，当前 0 活跃** | 实例已彻底关机自毁，无任何后台漏费风险 |
| **Cloud Credits** | Ultra / Google Builders Hub 标示 US$100/月 | **2026-11 已入账 / BOTH_CREDITS_ACTIVE / BILLING_VERIFIED** | Google Cloud Billing → Credits 实际账单：`Google Developer Program premium benefit - CREDIT_TYPE_MONTHLY`，Available / 100%，SGD 128.28；后续月份自动发放、适用产品与抵扣顺序仍待验证 |
| **Google Flow** | 约 25,000 点 / 月 | ⏳ 待使用 | 网页后台已确认包含 |
| **Antigravity** | Gemini 4 Argon + Claude Opus |  **已就绪** | 顶级模型池在 AGY 中可用 |
| **本地 M3 Pro 算力** | Apple Silicon M3 Pro 36GB |  **已部署运行 (43.9 tok/s)** | 本地私有无审查大模型 (9B Heretic Uncensored)，32K 上下文 |

---

## 2. 赛道重构：放弃真人定制短剧，全面转向【3D 国漫 CG 级 AI 漫剧】 (2026-11-09 SGT)

- **11-08 真人短剧惨败复盘与封存**：
  - 11-08 尝试使用家庭真人照片制作古装短剧，因触犯“真人恐怖谷效应”及工程偷工减料（OpenCV 2D 贴图换脸、`ffmpeg` 晃动静态死图冒充视频、模型退回 SDXL/SVD-XT、将半成品抛给用户）导致彻底失败，复盘已永久归档至 [**LESSONS_LEARNED.md**](./LESSONS_LEARNED.md)。
- **11-09 战略降维与《AI 漫剧工业化生产总纲 v2.0》固化**：
  - 经深度精读 Owner 过去 7 日 X 点赞（50+ 篇推文 / 11 篇万字长文，含 `@Delroy715`、`@aggs8p`、`@TuyetloanP81840`、`@EianLu`、`@leaf_sanren`、`@yangleiocx3`）及红果免费短剧 2025–2026 行业大盘数据，正式将主航道切换为 **【AI 漫剧（非真人出镜，默认锁定 3D 国漫 / UE5 影视 CG 风）】**；
  - 完整操作 SOP、Colab G4 75s NVMe 预热架构、MiniMax-H3 六大深坑攻克参数（`Self-Anchor Voice` 原生声纹锁死、`JoinMatch` 手动除雾、`--only-seg` 单镜 3 分钟热插拔、关闭真人毛孔 LoRA）、三类母本资产规范已归档至 [**docs/AI_MANJU_AND_ULTRA_SOP.md**](./docs/AI_MANJU_AND_ULTRA_SOP.md) 与 [**references/external_tools_audit.md**](./references/external_tools_audit.md)。
- **算力台账与资产安全**：
  - 云端 Colab G4 实例全量安全注销，活跃实例 **0**，当前算力可用余额 **2,497.44 CU**（`0.00 CU/h`）。

---

## 3. 下一步行动计划（Phase 2A：10 秒单镜头漫剧 MVP 闭环验收）

1. **Gate 1（0 CU 漫剧资产准备与颜值确认）**：生成主角【16:9 3D 国漫四联角色身份板（含全身、鞋靴、三视图与表情特写）】+【无人物纯净空镜场景图】+【第 1 镜高清首帧】，经 AGY 放大自检后交由 Owner 确认画风。
2. **Gate 2（Colab G4 + 真 ComfyUI H3 单镜渲染）**：在 G4 (96GB) 上极速挂载 ComfyUI + `MiniMax-H3 (Singularity v1.3)`（关闭真人毛孔 LoRA），生成 5~8 秒角色真开口说话、真动态、带物理拟音的漫剧单镜头，跑完立即关机查账。
3. **Gate 3（本地抽帧质检与字幕压制）**：AGY 本地抽帧核验无烧录乱码字、无变形后，用 `auto_subtitle.py` 声学包络自动对齐字幕交付验收。

---

## 4. Google Cloud Billing 与 Ultra 开发者赠金（2026-11-08 SGT）

**BOTH_CREDITS_ACTIVE / BILLING_VERIFIED — Owner screenshot-backed Google Cloud Billing Credits ledger (2026-11-08 SGT).** 仅记录订阅权益，不修改 AGY 算力/内容生产工作流。

- Google Cloud **Free Trial** 已激活，Billing UI 账户名为 `My Billing Account`，项目存在；Cloud Billing → Credits 核实 **SGD 384.83** 试用赠金（对应标准 **US$300**，是币种换算，**不是 US$385**）、**90 天**、到期日 **2027-02-07**，当时用量为 0。免费试用界面显示 `Upgrade`，Owner 未提供已升级 Paid 的证据；记录为 **Free Trial**。
- Google Builders Hub `Benefits` → **November '26 / US$100 monthly Gen AI & Cloud credits**，已选择 `My Billing Account`，勾选 `Always use this billing account` 并点击 `Apply`。之后 Benefits 卡片显示本地换算 **SGD 128.28**、`Remaining balance: $128.28` 和 `Google Cloud Billing` 入口；按截图判断 **2026-11 月度福利已应用于所选账单账户**。随后 Billing → Credits 显示该项独立 Credit 为 `Google Developer Program premium benefit - CREDIT_TYPE_MONTHLY`，状态 **Available**、剩余 **100%**、原值与剩余值均 **SGD 128.28**，入账已核实。截图亦显示 `EXPIRING ON: NOV 8, 2027`，但尚不能据此推断各月赠金的独立到期方式。
- **两类 Credits 不要混同：** Google Cloud Billing → Credits 逐项核实：`Free Trial` **SGD 384.83**，Available / 100%；`Google Developer Program premium benefit - CREDIT_TYPE_MONTHLY` **SGD 128.28**，Available / 100%。**合计 SGD 513.11 可用账面 Credit**（两笔独立入账，并非现金余额）。适用产品、抵扣顺序及 Free Trial 状态下具体消费限制仍待验证。
- **待验证：** 两笔 Credit 的服务适用范围、AI Studio Gemini API / Vertex AI / Agent Platform 等具体抵扣条件；未来月份是否自动 Apply、是否需要人工领取、月度 Credit 的实际到期时间及抵扣顺序。不得把勾选默认 Billing Account 解释为已验证自动每月领款。
- **操作边界：** 未申请 Paid Upgrade、未启动 GPU VM/收费资源、未改动付款账户、密钥或部署。既有 Google AI Ultra Apple 订阅与 Colab CU 额度独立于 Cloud Billing 赠金。
- **证据来源：** Owner 2026-11-08 当前对话的 Google Cloud Free Trial Overview、Builders Hub Benefits Apply 前/后，以及最新 **Google Cloud Billing → Credits / All credits** 截图；本记录不包含账户号码、付款资料或个人地址。

---

## 5. Google Cloud 双机接力私人 VPN 基础设施（2026-11-08 SGT）

**DEPLOYED / CONNECTIVITY_VERIFIED / US_IP_VERIFIED / TW_IP_VERIFIED / GUARDRAILS_ACTIVE**

- **目标与架构**：针对中国大陆差旅场景，在项目 `project-665ac784-237e-4a71-ad0` 下完成「台湾入口跳板 (`asia-east1-b`) ➡️ Google 内部跨洋骨干网 (`VPC`) ➡️ 美西原生出口 (`us-west1-b`)」双机接力部署，并同时提供台湾本地直连备用线路。完整技术与运维文档见 [**docs/gcp_dual_node_vpn.md**](./docs/gcp_dual_node_vpn.md)。
- **资源清单**：
  - 入口机：`node-tw-entry-01`（`asia-east1-b`, `e2-micro`, Debian 12, 10GB `pd-standard`, 静态公网 IP `35.194.245.4` / `ip-node-tw-01`, 内网 `10.140.0.2`）
  - 落地机：`node-us-exit-01`（`us-west1-b`, `e2-micro`, Debian 12, 10GB `pd-standard`, 美西公网出口 IP `35.247.83.37`）
  - 防火墙：`fw-allow-proxy-in`（放行 `proxy-entry` 的 `8443/2053` 端口）、`fw-allow-internal-xray`（放行 `10.128.0.0/9` 内部 `10808` 端口）
- **协议与安全护栏**：
  - 采用 `Xray-core v26.1.23`，外部协议 `VLESS + XTLS-RPRX-Vision + REALITY`（SNI `www.apple.com:443`）；
  - 已启用 `250GB/月` 流量自动熔断锁（`traffic_guard.sh` + `/etc/cron.d/xray-traffic-guard`）及 `play.googleapis.com` 遥测域名黑洞拦截；
  - 固定月租约 US$7.6/月（美西 `e2-micro` 命中 Free Tier，台湾 `e2-micro` 由 Cloud Credits 抵扣），未升级 Paid Billing，无现金超支风险。
- **端到端实测结果**：
  - **🇺🇸 美西专线 (`35.194.245.4:8443`)**：实测出口 IP `35.247.83.37` (`The Dalles, Oregon, US`)，MacBook 与 iPhone Hiddify 均连接验证通过；
  - **🇹🇼 台湾直连 (`35.194.245.4:2053`)**：实测出口 IP `35.194.245.4` (`Taipei, Taiwan, TW`)，MacBook 与 iPhone Hiddify 均连接验证通过；
  - 敏感凭据（UUID、REALITY 私钥/公钥、ShortId、完整 `vless://` 链接）严格隔离于本地，未写入 GitHub 仓库。

---

## 6. Google AI Pro 独立美西备用 VPN 节点与全球 4 线矩阵（2026-11-09 SGT）

**DEPLOYED / PRO_US_NODE_VERIFIED / 35GB_TRAFFIC_LOCK_ACTIVE / GLOBAL_4_LINE_MATRIX_READY**

- **Google AI Pro 开发者月度赠金与独立节点部署**：
  - 账户与计费池：`maxli1985939495-org` / `My Billing Account 2`，拥有 `Google Developer Program premium benefit - CREDIT_TYPE_MONTHLY` **US$10.00 / 月**（Available 100%）。
  - 节点规格与地址：`node-us-pro-01`（`us-west1-b` 美国俄勒冈，命中 GCP 免费层区域，机器固定月租 `$0`；`e2-micro`, Debian 12, 10GB `pd-standard`，公网 IP `136.86.239.13:8443`）。
  - 协议与流量熔断锁：`Xray-core v26.1.23` (`VLESS + XTLS-RPRX-Vision + REALITY`, SNI `www.apple.com:443`) + TCP BBR + **35GB/月 自动流量熔断锁**（因 GCP 出站往中国方向流量单价约 `$0.23/GB`、其他互联网约 `$0.12/GB`，设定 35GB 阈值确保月度流量费恒定控制在 `$4~$8` 以内，100% 由每月 `$10` 赠金覆盖，零扣卡风险）。
- **全球 4 线高可用 VPN 矩阵汇总**：
  1. **🇺🇸 `GCP-美西专线` (Google AI Ultra)**：`35.194.245.4:8443`（台湾跳板 ➡️ 谷歌跨洋内网 ➡️ 美西原生出口 `35.247.83.37`，250GB/月锁）
  2. **🇹🇼 `GCP-台湾直连` (Google AI Ultra)**：`35.194.245.4:2053`（台湾台北直连出口 `35.194.245.4`，共享 250GB/月锁）
  3. **🇺🇸 `GCP-Pro-美西独享` (Google AI Pro)**：`136.86.239.13:8443`（独立账号/独立美西原生出口 `136.86.239.13`，35GB/月锁）
  4. **🇸🇬 `VPN_ZZ` 新加坡专线 (Tencent Cloud Lighthouse)**：`43.134.74.51:443`（`sing-box 1.14.0` VLESS+REALITY，5 个独立客户端身份，1TB/月流量包）

`hermes_surface_impact=NO_HERMES_IMPACT`; `project_ui_impact=NO_UI_IMPACT`。
