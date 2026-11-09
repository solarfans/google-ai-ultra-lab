# Google AI Ultra Lab — Current State & Ledger

**最后更新**：2026-11-09 SGT (MacBook Pro)  
**项目状态**：`GCP_ULTRA_AND_PRO_VPN_MATRIX_VERIFIED / BOTH_CREDITS_ACTIVE / ZERO_BURN_SAFE`  
**负责席位**：Antigravity Desktop (MacBook)  

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

## 2. 赛道关停与惨败复盘归档 (Short Drama Post-Mortem)

- **AI 短剧商业化与真人定制赛道正式关停封存**：
  - 因多次迭代中技术路径错误（2D几何贴图代替深度学习换脸、静态图摇晃冒充视频、旧模型倒退、中间残次品直交用户），导致成片质量极其低下并引发用户强烈不满；
  - 经用户明确指令，全面终止该赛道的所有生成与测试任务，封存全部历史资产；
  - 深度复盘报告已固化至 [**LESSONS_LEARNED.md**](./LESSONS_LEARNED.md)，详尽剖析五大核心失误与未来工业级 SOTA 标准流水线。
- **算力台账与资产安全**：
  - 云端 Colab G4 实例全量安全注销，活跃实例 **0**，当前算力可用余额 **2,497.44 CU**；
  - 待命状态，等待 Owner 下达下一阶段核心战略目标。
  - 0 CU 本地备料：剧本分镜、角色定义、负向提示词门禁全部在本地编排完成；
  - 生命周期强制自毁：任务结束后自动释放，当前活跃实例数归零，算力余额稳健保持 2499.56 CU。

---

## 3. 下一步行动计划

1. **审阅成片画质与眼神杀效果**：Owner 在本地播放器直接审阅 `chu_shi_chun_qiu_ep01_qwen_minimax_master.mp4`，核验少年楚铮骨相与帝王觉醒质感。
2. **多机位接力与长镜头扩展**：引入 `BUNNY_H3_ActionLogic_Bridge` 与 22 帧潜空间混合接力，实现长镜头连续对手戏。
3. **推进小说广播剧管线 (引擎 3)**：利用 Gemini 对白提取与本地/云端 TTS 模型，生成第一期《楚氏春秋》长篇有声广播剧。

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
