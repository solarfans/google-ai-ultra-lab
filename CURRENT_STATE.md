# Google AI Ultra Lab — Current State & Ledger

**最后更新**：2026-11-10 23:36 SGT (MacBook Pro)  
**项目状态**：`AI_MANJU_SOP_V4_5_HYBRID_PIPELINE_LIVE / EP01_EP02_V2_AND_EP03_DELIVERED / ZERO_BURN_SAFE`  
**负责席位**：Antigravity Desktop (MacBook)  
**核心操作总纲**：[**skills/google-ai-ultra/SKILL.md**](./skills/google-ai-ultra/SKILL.md) | [**docs/AI_MANJU_AND_ULTRA_SOP.md**](./docs/AI_MANJU_AND_ULTRA_SOP.md) | [**docs/research/GOOGLE_AI_ULTRA_VALUE_AND_CREATOR_STRATEGY_2026-11-10.md**](./docs/research/GOOGLE_AI_ULTRA_VALUE_AND_CREATOR_STRATEGY_2026-11-10.md)

---

## 1. 订阅与五大独立成本池清单（2026-11-10 核实口径）

| 权益项目 | 官方标称/2026-11-10 规则 | 当前实测状态 | 生产定位与验证凭据 |
| :--- | :--- | :--- | :--- |
| **会员级别** | Google AI Ultra 20x (30 TB) | **已确认** | Google One 首页显示 "Google AI Ultra, 30 TB"；Apple 订阅 `₺2,949.99/月` |
| **1. AGY / Gemini 4 Argon** | Ultra 20x 档位 | **已就绪（余量充裕）** | 常驻总导演、连续性编剧、多模态抽帧与音轨冷读 QA |
| **2. Colab GPU 算力 (`CU`)** | 标准发放 2,000 CU/月（含历史结余） | **已确认 (`2,480.89 CU`)** | `ultra_meter.py usage` 实测余额 `2,480.89 CU`，**活跃实例 `0` (`0.00 CU/h`)**；主力跑 `MiniMax-H3` 角色表演与口型 |
| **3. Flow Video (`Credits`)** | 25,000 credits/月（按月刷新不结转） | **已就绪** | `Veo 3.1 Lite`（Ultra 20x Lower Priority 为 **`0 credits`**）+ `Omni Flash 1.2`（前 10s 为 `3 credits/s`）；用于空镜、大场面转场与三镜同题 A/B |
| **4. Flow Music (`Credits`)** | 30,000 credits/月（含商业授权） | **已就绪** | Member 明确包含商业使用权，独立于视频积分池，用于古风主题曲与情绪铺底 BGM |
| **5. GDP Cloud & 30TB Drive** | US$100/月 Cloud Credits + 30TB Drive | **2026-11 已入账 (`SGD 128.28`)** | Cloud Billing 含 `Free Trial SGD 384.83` + `GDP Monthly SGD 128.28`；30TB Drive 归档无损母带与大模型权重 |
| **本地 M3 Pro 算力** | Apple Silicon M3 Pro 36GB | **已部署运行** | 本地零成本执行 `edge-tts` Neural 音色合成、FFmpeg 双轨混音、6 道门禁质检与字幕压制 |

---

## 2. 《楚氏春秋》3D 国漫生产进度与 v4.5 工业化管线（2026-11-10 SGT）

- **已交付成片基线**：
  - **第 1 集《北赵楚氏》(`50.66s`)**：已完成 5 镜 3D 国漫动态渲染、Shot 03 单镜手术刀修复与去 `【角色名】` 纯台词字幕压制（[`ChuShiChunQiu_Ep01_BeizhaoChushi_Master_v2.mp4`](./pipelines/short_drama/ChuShiChunQiu_Ep01_BeizhaoChushi_Master_v2.mp4) / [`Subtitled_Audit.mp4`](./pipelines/short_drama/ChuShiChunQiu_Ep01_BeizhaoChushi_Subtitled_Audit.mp4)）。
  - **第 2 集 v2《转世重生》(`60.75s`，6 镜全重制精修版)**：
    - 彻底解决 v1 的 6 项缺陷：移除空姐站座位旁拿电话广播的常识错误、全面替换为 `edge-tts` Neural 音色种子（消除 `say`/`asetrate` 鬼叫失真）、落地 **“闭嘴演眼神 + 28 岁成年男声混响内心独白（OS）”** 与 **“画外航空带通滤波广播（PA）”**、100% 还原原著第二章核心名场面（王秀荷磕头滴血认母、吴安然逃亡平原郡回味豆花店两指按铜钱入木桌毛遂自荐、楚府偏厅暗施十成大搜魂手反助楚铮贯通任督二脉）；
    - 单次 Colab G4 会话耗时 `25.46 min`、消耗 `4.08 CU` 完成 6 镜渲染；成片已交付至 [`ChuShiChunQiu_Ep02_ZhuanshiChongsheng_Master_v2.mp4`](./pipelines/short_drama/ChuShiChunQiu_Ep02_ZhuanshiChongsheng_Master_v2.mp4) 与 [`ChuShiChunQiu_Ep02_ZhuanshiChongsheng_Subtitled_Audit.mp4`](./pipelines/short_drama/ChuShiChunQiu_Ep02_ZhuanshiChongsheng_Subtitled_Audit.mp4)。
  - **第 3 集《颠倒乾坤》(`60.77s`，原著第三章 6 镜完整出片)**：
    - 100% 还原原著第三章《颠倒乾坤》全部 6 幕核心剧情与草蛇灰线：
      1. `Shot 01`：吴安然并指御气将大赵云山绿茶凝成碧绿水龙盘旋飞舞诱徒，楚铮惊喜答应拜师学武；
      2. `Shot 02`：后院阳光草坪抚白猫“雪玉”，楚铮闭嘴按胸口与体内残留的小楚铮灵魂共鸣立誓（`single_inner_monologue_os`，28 岁成年男声混响 OS）；
      3. `Shot 03`：楚铮苦脸撒娇拒喝苦药开口唤娘，母亲王秀荷手中青花药碗摔碎在地、喜极而泣紧抱小五儿；
      4. `Shot 04`：书房内楚铮高声向父亲楚名棠请安，楚名棠狂喜抱儿转圈大笑并定下择日行拜师大礼；
      5. `Shot 05`：暮色回廊下，靖北侯派驻楚府的高总管（新增设定卡 `manju_char_gaoshiying_sheet_1344x768.png` 与 `zh-CN-YunyangNeural` 低音种子）向王秀荷密报吴安然乃魔门血影宗主“魔秀士”，王秀荷神秘微笑道“那可真是巧了”并嘱咐瞒着楚名棠；
      6. `Shot 06`：点题高潮《颠倒乾坤》——书房读繁体《论语》《史记》，王秀荷温柔讲述“后汉太宗刘禅雄才大略，五年一统天下”，楚铮闭嘴石化瞪圆双眼（成年灵魂抓狂 OS：“扶不起的阿斗竟一统天下？！这历史简直颠倒乾坤！”）。
    - 单次 Colab G4 会话耗时 `25.60 min`、仅消耗 **`3.57 CU` (`0.595 CU/镜`)** 完成 6 镜渲染并自动销毁实例；6 道门禁（含 Gate 6 `--post-render` 成片声学门禁）全绿通过，交付 [`ChuShiChunQiu_Ep03_DiandaoQiankun_Master_v2.mp4`](./pipelines/short_drama/ChuShiChunQiu_Ep03_DiandaoQiankun_Master_v2.mp4) (`46.44 MB`) 与 [`ChuShiChunQiu_Ep03_DiandaoQiankun_Subtitled_Audit.mp4`](./pipelines/short_drama/ChuShiChunQiu_Ep03_DiandaoQiankun_Subtitled_Audit.mp4) (`42.38 MB`)。
- **v4.5 管线合并升级（吸收 2026-11-10 Ultra & Creator Strategy 研究成果）**：
  1. **6 道 Pre-Flight + Post-Render 自动化门禁（[`scripts/manju_qa_gate.py`](./scripts/manju_qa_gate.py) v4.5）**：在渲染前 5 道门禁基础上，新增 **Gate 6 (`--post-render`)**，对每个实际渲染出的 MP4 执行 `ffprobe` 流完整性核验与对白时间窗 PCM 声学能量（`dBFS > -36 dBFS`）核查，杜绝空轨、截断与假通过。
  2. **SHA-256 指纹校验断点续跑（[`scripts/manju_compiler.py`](./scripts/manju_compiler.py) v3.2）**：不再仅凭 `status == "completed"` 盲目跳过；必须同时满足 `output_mp4` 存在有效且 `input_fingerprint`（覆盖首帧图像哈希、台词、模式、角色）完全一致才跳过，并预留 `model_backend`（`h3_comfyui` / `flow_veo_3_1_lite` / `flow_omni_1_2`）混合路由字段。
  3. **经验教训与防呆台账**：全量归档于 [`pipelines/short_drama/LESSONS_LEARNED.md`](./pipelines/short_drama/LESSONS_LEARNED.md)（`LL-001` 至 `LL-007`）。

---

## 3. 下一步行动计划（Phase 4：第 4 集《上京风云》推进 + 1–3 集合集长片包装）

1. **第 3 集《颠倒乾坤》视听验收与第 4 集《上京风云》筹备**：推进原著第四章《上京风云》（北赵国都上京皇宫御书房赵王与琳贵妃楚琳夜谈、楚铮正式拜师吴安然习练魔门筑基功法与《颠倒乾坤》）。
2. **双画幅与长短结合发行包装**：保留 `16:9 Clean Master` 与独立分轨，导出 `9:16` 竖屏安全区版；应对 YouTube `2027-02-01` YPP 新门槛（8,000 长视频观看小时或 2,000 万 Shorts/90 天），将已完成的第 1–3 集（开篇平原本纪三部曲）合成为长视频合集。

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
