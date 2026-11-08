# Google AI Ultra Lab — Current State & Ledger

**最后更新**：2026-11-08 SGT (MacBook Pro)  
**项目状态**：`SHORT_DRAMA_PIPELINE_ABANDONED_ARCHIVED / LESSONS_LEARNED_COMMITTED / ZERO_BURN_SAFE`  
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
| **Cloud Credits** | Ultra / Google Builders Hub 标示 US$100/月 | **2026-11 当月已申请、页面显示余额 SGD 128.28** | 2026-11-08 Owner 截图：Builders Hub Benefits `My Billing Account`、`Remaining balance: $128.28`（界面本地货币 SGD）；以后各月发放/是否自动续领尚未验证 |
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

**Owner screenshot-backed / November credit applied at benefit UI; independent Billing credit-ledger reconciliation pending.** 仅记录订阅权益，不修改 AGY 算力/内容生产工作流。

- Google Cloud **Free Trial** 已激活，Billing UI 账户名为 `My Billing Account`，项目存在；Cloud Billing Overview 明示 **SGD 385** 试用赠金（对应标准 **US$300**，是币种换算，**不是 US$385**）、**90 天**、到期日 **2027-02-07**，当时用量为 0。免费试用界面显示 `Upgrade`，Owner 未提供已升级 Paid 的证据；记录为 **Free Trial**。
- Google Builders Hub `Benefits` → **November '26 / US$100 monthly Gen AI & Cloud credits**，已选择 `My Billing Account`，勾选 `Always use this billing account` 并点击 `Apply`。之后 Benefits 卡片显示本地换算 **SGD 128.28**、`Remaining balance: $128.28` 和 `Google Cloud Billing` 入口；按截图判断 **2026-11 月度福利已应用于所选账单账户**。截图亦显示 `EXPIRING ON: NOV 8, 2027`，但尚不能据此推断各月赠金的独立到期方式。
- **两类 Credits 不要混同：** SGD 385 是 Cloud Free Trial，一次性、90 天；SGD 128.28 是本期 Ultra/Builders Hub 月度权益的本地币金额。按两张页面显示值合计 **SGD 513.28 名义额度**，但两者各自的适用产品、抵扣顺序及可否在 Free Trial 下实际消费未做 Billing Incentives/Transaction 级别核验，**不可视为已到账、可通用的现金余额**。
- **待验证：** Cloud Billing → Incentives/Credits 的实际入账明细；本月 Ultra Credits 是否允许 AI Studio Gemini API、Vertex AI、Agent Platform 及其他服务抵扣的具体条件；未来月份是否自动 Apply、是否需要人工领取、赠金有效期及抵扣顺序。不得把勾选默认 Billing Account 解释为已验证自动每月领款。
- **操作边界：** 未申请 Paid Upgrade、未启动 GPU VM/收费资源、未改动付款账户、密钥或部署。既有 Google AI Ultra Apple 订阅与 Colab CU 额度独立于 Cloud Billing 赠金。
- **证据来源：** Owner 2026-11-08 当前对话的 Google Cloud Free Trial Overview、Billing Overview、Builders Hub Benefits Apply 前/后截图；本记录不包含账户号码、付款资料或个人地址。

`hermes_surface_impact=NO_HERMES_IMPACT`; `project_ui_impact=NO_UI_IMPACT`。
