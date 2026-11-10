# Google AI Ultra 全生态价值最大化：AGY、自主工程、云算力、商业机会与 AI OS 联动

> **2026-11-10 SGT｜CG-A 综合研究交付｜AGY 执行参考｜本报告为全局战略研究，不是 AI 漫剧专项审计**
>
> 研究目标：基于现有 Google AI Ultra 30TB 订阅，系统发现并排序 **全部实际有价值的权益、隐藏能力、跨领域用途、收入机会**，充分利用 Gemini 4 Argon / Antigravity；识别已实现资源与新增机会；形成 AGY 可自主推进的工程与试验路线。
>
> **研究范围：**AI 短剧/漫剧只是多个试水方向之一；本报告以整个 Ultra 生态的价值最大化为目标，原漫剧报告保留为专项参考。
>
> 状态分类：**O = 官方直接证据；G = 当前 GitHub 已归档的测试/状态（需按更新时间理解）；X = Bird 原生 X 作者陈述；H = 战略假设、尚待 AGY 实测。** “可使用”与“已在此账户测通”分别记录。

## 0. 总结：推荐优先级与资源配置

**主建议不是“优先拍漫剧”，而是让 Ultra 成为面向多个业务机会的可复用 AI 工程、研究、媒体与云资源组合。**

| 优先级 | 价值路线 | 为什么现在值得投入 | 最小实交付 | 当前状态 |
| --- | --- | --- | --- | --- |
| P0 | **AGY Remote Agents + Argon 长任务工程执行** | 能跨本地/云端持续工作，覆盖现有全部 GitHub 工程与新软件产品；可快速复用 | 一项独立 GitHub 任务在 Remote Agent 完成可复现测试和代码交付；本地 AGY 无缝接续 | 官方功能已存在；本账户 Remote E2E 尚未核验 [O4] |
| P0 | **已领取 Cloud credits → 真实产品实验** | Ultra 每月 US$100 GDP credits 已在 GitHub 记载到账，不必只用于 VPN；Cloud Run 有按请求计费免费层 | Cloud Run/AI Studio 小型工具，真实调用、成本记录与用户体验测试 | Billing/赠金历史已验证；新增产品未建 [G1][O6][O7] |
| P0 | **全权益盘点与成本池明确化** | 30TB、YouTube Premium、G4 GPU、VPN 已使用；还有 Notebook、Flow Music、Project Genie、文件与研究工具 | 一页权益库存：入口、可用性、实际剩余/刷新、已用/待试 | 部分 GitHub 历史已核验；未做本轮账号实时登录 [G1][O1] |
| P1 | **专项研究/知识生产：Gemini Notebook + Deep Research + Argon** | 强来源研究、源文件整理、演示文稿、短视频、学习材料，有用范围远超漫剧 | 完成一个真实跨 20–50 份资料的研究/课程/技术文档成品 | 官方能力明确；项目级测试未做 [O10][O11] |
| P1 | **Colab GPU 变成通用按需计算服务** | 已实测 G4 96GB；可处理本地计算瓶颈，不应仅做 H3 视频 | ASR/视觉或 LLM 推理/评估三类任务的真实成本、吞吐及自动回收 | 既有 G4 可用历史，其他负载待测 [G1][O8] |
| P1 | **可变现的垂直软件与数字产品** | 用户拥有 SQE、自动化、内容研究与系统工程经验；相较泛化“AI 赚钱”更可能形成差异化 | 一个可公开演示的窄功能 MVP，至少收集真实使用反馈 | 商业假设 [H1] |
| P1 | **多品类创作与分发** | Flow/音乐/Notebook/代码动画组合不只拍戏，亦可做解释动画、教程、音频、数字内容 | 2–3 个不同品类的完整作品，比较工作量、留存、需求 | 工具存在；漫剧管线已有阶段性成果 [G1][O12] |
| P2 | **Project Genie / 3D 交互原型** | Google Argon + Project Genie/Three.js 可开发教学、游戏、交互展示 | 可玩/可交互的单场景作品及部署页面 | 官方在新加坡的 Labs 名单包含 Project Genie；账号具体入口待试 [O13][O14] |
| P2 | **个人及家庭生产力** | Google Notebook、Gemini 文件编辑、30TB、Photos、家庭权益等可以立即节省时间 | 一套资料整理/教育样例和实际可共享福利清单 | 核心权益已公开，家庭组合尚未实测 [O1][O11][O15] |
| 维护而非新建 | **VPN / GCP 节点** | 仓库已有四线已部署记录；再搭相同链路浪费时间 | 核对现有服务是否仍稳定、月度流量/赠金成本是否匹配预期 | 历史部署与 E2E 已记录，不等于今夜实时健康 [G2] |

**不建议的默认方向：**重新购买 VPN、从零重搭 Colab、重复注册多个新工具、再造统一 Agent 框架、先打造大型 SaaS 后找用户、先开十个视频账号。只有真实瓶颈出现时才增加组件。

## 1. 本轮研究覆盖与证据规模

### 1.1 检索范围

- **原始需求复核**：Ultra 全部权益与额外福利、AGY 全自主执行、Gemini 4 Argon 额度与能力、Colab/GPU、Google Cloud/私人 VPN、AI OS 升级、X 经验、Google/GitHub/社区、TikTok/YouTube、各种潜在收入与其他生活工作领域，不能只限漫剧。
- **官方资料**：Google One/Ultra 计划、GDP credits、Antigravity Remote Agents/App/CLI/模型与定时任务、Jules 退役、Colab CLI、Google Cloud Run/AI Studio、Notebook、Gemini 文件生成、Project Genie、Hypothesis Generation、家庭分享及部分地区功能。
- **当前 GitHub**：目标 repo 的 README、CURRENT_STATE、ROADMAP、AGENTS、VPN 与本地 LLM 工程记录、旧专项报告；另阅 Global Project Registry。
- **Bird 原生 X**：本轮重新读取最新 100 条点赞项目（API 单次最大 100）；上一轮任务曾从同一 Bird 只读路径取得并筛读 500 条唯一点赞、其中 45 篇长文全文。当前重新按不同主题（订阅、Agent、GPU、云服务、收入）归类，补读 8 条代表性原帖，并对 Ultra/GDP/GPU/Argon/创业主题进行了多组原生搜索。
- **X 数据时间精度**：Bird 点赞导出不包含可信的 **liked_at**；按最新点赞顺序和发帖日期筛读，不能将发帖日期直接当成点赞日期。公开原帖链接供 AGY 继续读取。

### 1.2 原始研究为何发生范围塌缩

之前的专项报告过度沿用目标仓库已有“AI 漫剧工业化”工程主题，把它当成 Ultra 全订阅的主战略，没有对 Cloud/VPN、Remote Agents、其他 Google 产品、跨领域应用和商业模型做同等级机会扫描。本报告独立重排价值优先级；漫剧既有技术审计保留为一条分支。

## 2. 已有基础：不要把完成的事情再当新任务

根据 2026-11-09 的 GitHub CURRENT_STATE/README/相关文档 [G1][G2][G3]：

| 资产/权益 | GitHub 所记状态 | 本次战略含义 |
| --- | --- | --- |
| Ultra 订阅 | Google AI Ultra 30TB；Apple 订阅记录为 ₺2,949.99/月，续费节点 12 月 7 日 | 利用现有低现金成本订阅做高价值实验，先回读实际计划标签 |
| YouTube Premium | 记录为已激活 | 直接消费权益已兑现；不是内容频道收入 |
| Colab | G4 96GB 曾实测；2026-11-09 余额 2,497.44 CU、0 活跃 | **余额不是每月发放数**；官方 Ultra 20x 为 2,000 CU/月，应分清历史存量/到账/账期 |
| Google Cloud | GDP Ultra US$100 每月权益，11 月 credits 已在 Billing 记账；另有 US$300 Free Trial 余额/90 天 | Cloud/API 实验可与现有 VPN 共享账单体系，实际抵扣通过 Billing 查 |
| 第二个 Pro credit pool | 目标文档记录 Google AI Pro US$10/月赠金、独立美西节点 | 独立账单，不将两账号 credits 直接相加为一个消费池 |
| VPN | 台湾入口→美国出口、台湾直出、Pro 美国节点、腾讯云新加坡节点，四条线路有 11/08–11/09 E2E 记录 | **已经部署**；后续优先成本、健康、应用复用，非重复搭建 |
| MacBook 本地 LLM | 9B 本地模型，约 43.9 tokens/s 的历史基准；存在 Telegram 入口/本地 API | 适合离线、快速轻量任务，复杂工程继续用 Argon/更强模型 |
| AI 漫剧 | 10s MVP、镜头工具、两集成片记录、最新 QA/语音脚本 | 已有专项路线；不排挤其他 Ultra 价值方向 |
| AGY | MacBook Desktop 本地执行、Gemini Argon 和第三方模型池历史可用 | 现在最值得补的增量是 **Remote Agents/远程协作、工程范围扩大、产品交付** |

**注意状态时间点**：表格均为 GitHub 记录，未重新登录 Cloud Billing/Apple/Colab，也未重新实测 VPN 出口。报告不把历史状态写成“2026-11-10 今夜健康”。

## 3. Google AI Ultra 权益全景：从工具、额度与地区看价值

以下分类根据 2026-11-10 已读取官方页面 [O1][O2][O9]；不同 Ultra **5x/20x** 产品组合与刷新周期不同。

### 3.1 核心权益池（先分账，不再混淆）

| 权益池 | Ultra 20x 官方基准 | 最大化价值的方法 | 状态/重点 |
| --- | --- | --- | --- |
| Gemini app / Gemini 4 Argon | 20x 配额等级，Gemini app 上下文官方标称可达 1M tokens | 多文档分析、复杂方案设计、长时研发、跨领域研究、文件成品 | 用户报告高强度使用后仍余约 96%，属于使用观察，不是绝对无限 |
| Antigravity / AGY | 高优先级、高五小时与每周额度；Argon、Gemini 3.8 Flash、Claude Sonnet/Opus 等可按当前模型列表选择 | Desktop / CLI / Remote Agents / ACP / 自动化 | 部分配额按模型/周期分开；AGY 本地高使用已成立 [O3] |
| Google Flow | **25,000 credits/月**（20x） | 图像、视频、编辑、多个创作领域 | 下期刷新，和 Colab CU 不互通 [O1][O9] |
| Flow Music Member | **30,000 credits/月**，另有会员权益 | 原创音乐、主题曲、播客配乐、短广告和音频数字资产 | 独立于 Flow 的额度池 [O1] |
| Colab | **2,000 compute units/月**（20x）、高级 GPU 动态可用 | 视觉/ASR/LLM 实验、批处理、训练与数据处理 | 历史 2,497.44 CU 是余额，不是 2,500 月费包 [O1] |
| Google Developer Program | **US$100/月 Cloud/GenAI credits**（20x；5x US$40，Pro US$10） | Gemini API、Cloud Run、Firebase、存储、适用 GCP 服务 | 已到账历史证据；每笔发放起一年有效，分 Billing Account [O5] |
| Google Drive / Gmail / Photos | **30TB** 共享容量（20x） | 模型/媒体/研究资料/资料备份与家庭共享 | 30TB 不等于 Colab 本地 VM 磁盘 |
| Gemini Notebook | Ultra 更高使用层级；官方计划表 **最多 600 sources/notebook（20x）**，另有 Audio/Video Overviews、Reports、幻灯片、深度研究 | 大型知识库、文献、课程、工作资料与多格式内容 | 2026 新 compute 额度按复杂度扣减，每 5 小时刷新到周限 [O10] |
| Google AI Studio | Gemini API 原型、Build mode、模型与评测 | 快速制作/验证应用，连接付费 API 时按 API billing 计费 | “订阅网页版 Argon 多用”不等于“API 无限免费” [O6][O7] |

### 3.2 经常被忽略的产品型权益

| 产品/能力 | 能创造什么价值 | 本案建议 |
| --- | --- | --- |
| **Antigravity Remote Agents** | Google 管理的独立云端工作空间；GitHub、Drive、上传文件及插件；本地 Mac 睡眠可继续工作 | **高优先级单独测一次 E2E** [O4] |
| **Antigravity Remote Control / Automations** | 从手机/浏览器管理本机 AGY；按指定周期启动任务；本地/远程任务分离 | 有明确持续性工作后再接入，复用已有 Hermes/Cron [O4] |
| **Gemini Desktop (macOS/Windows)** | Gemini 4 Argon 与本地开发任务间切换，Gemini app 可直接预览/修改 Docs/Sheets/PDF/Slides/代码 | 适合个人研究与办公，不额外建工具链 [O16] |
| **Deep Research / 1M 上下文** | 大量 PDF、技术资料、标准、产品/市场研究 | 优先将现有重复研究任务迁移成可复用流程 [O2] |
| **Hypothesis Generation（Google Labs Science）** | 系统整理文献、研究空白、提出可检验假设/算法候选；Standard/Advanced run | 适合材料科学、工艺、失效研究思路探索与算法实验，不等于已做实验 [O17] |
| **Project Genie / Labs** | 交互环境/世界原型；演示、可探索场景、教育或游戏概念 | **新加坡在 Labs 支持名单中**，先做交互原型而不是包装成成熟游戏引擎 [O13] |
| **Google Photos AI / image remix** | 家庭相册整理、演示图、照片创作 | 先核对本人账号的 Photo to video/Remix 可用入口，部分功能只在美国 [O1] |
| **Google Health Premium** | Pixel Watch/Fitbit 设备的健康辅导 | **官方支持 Singapore**，需有对应设备；没有则低优先 [O1] |
| **Google Home Premium Advanced** | 智能家居事件回看和家庭设备 | 当前官方可用国家列表未列 Singapore，非本轮主要价值 [O1] |
| **Gemini Tasks、AI Inbox、Chrome Auto Browse** | 个人事件处理、邮件待办与浏览器自动化 | 2026-11-10 官方当前注明 Tasks/AI Inbox 主要限美国；Chrome Auto Browse 为 US/India。不要把这些当新加坡账号已拥有的能力 [O1] |
| **Gemini Workspace apps** | Gmail、Docs、Sheets、Vids 的日常分析/写作/演示 | 可以直接节省个人工作与知识处理时间 [O1] |
| **YouTube Premium** | 无广告/背景播放等 | 已有实用消费收益；不等于 YPP 变现资格 |
| **家庭分享** | 共享容量和部分 AI 能力，支持最多 5 位其他家庭成员 | 按账号所属国家及各产品共享 quota 机制测试，Flow/AGY 部分配额可能共享 [O15] |

### 3.3 2026 年 11 月的生命周期变化（直接影响技术选型）

- **Jules**：Google 官方 2026-10-29 公告：**2026-11-11 转为只读；12-31 终止**。此前“把 Jules 作为长期独立后台工程 Agent”的建议应撤回。直接看 Antigravity Remote Agents [O18]。
- **Antigravity Remote Agents**：官方已上线，适用于个人 Pro/Ultra，项目可带 GitHub/Drive 文件；是当前最值得核验的新增生产形态 [O4]。
- **Gemini 4 Argon**：2026-10-13 已面向 Google AI Pro/Ultra 的 Gemini/AGY 开放，具有跨任务工程、研究与多模态能力；不要按旧 Gemini 3.x 配额和能力猜测 [O3]。
- **Flow**：Omni Flash 1.2 与 Veo 3.1 Lite 现为推荐路线；Lite Lower Priority 在适用 Ultra 20x 管理员配额下为 0 credits，但吞吐需实测；11 月 5 日 Veo Extend 旧功能退役，12 月 5 日另有旧版模型退役 [O9]。
- **Gemini Notebook**：2026 年 9 月开始改用工作量相关、5 小时刷新且有周上限的模型；旧静态“每天 N 次”表格不应当成无条件吞吐保证 [O10]。

## 4. AGY 全面自主执行：本地、云端与产品交付的最佳分工

### 4.1 推荐架构（少组件、能力先行）

- **MacBook AGY Desktop**：需要真实 Mac 文件、GUI、既有工程构建、已注册工具和本地工作树的任务；继续作为现有设备上的本地执行者。
- **AGY Remote Agents**：可分离到 GitHub 及 Drive 资料的代码任务、跨文件研究、独立验证、远程开发；即使 Mac 睡眠仍在 Google 的 sandbox 继续。独立云端目录不是 Mac 的透明远程桌面。
- **AGY CLI headless**：本地脚本/CI 一次性执行任务，提供明确输入、输出和退出码 [O4]。
- **Google Colab CLI**：用 GPU 的**批计算**，例如批量 ASR、嵌入模型、视频评测、大型开源模型基准、音频/图像加工；任务结束回收 VM [O8]。
- **Cloud Run / Firebase / Gemini API**：对外提供稳定的轻量 API、网页 MVP、数据存储和事件接口；按真实调用量及 GDP credits 计量 [O6][O7]。
- **30TB Drive**：大文件/媒体/模型与可恢复中间产物；GitHub 保存代码、索引、测试与发布记录。
- **现有 Hermes/Kelly**：已有 Telegram、长期持续任务、通知和调度；只做值得复用的联动，不因为 Ultra 到手就迁移全部业务。

### 4.2 本轮首选 Remote Agents 真实验证

**官方最短入口** [O4]：

1. AGY CLI 使用已登录的个人 Ultra 账号，核对 CLI 版本（官方要求 1.4.12 及以上）。
2. 使用 **agy --remote-agent** 进入远程执行；通过 **/projects** 创建远程项目并附上对应 GitHub repo 或 Drive 文件。
3. 选择一个**独立、可重试、有测试方法的小任务**，例如解析公开资料、生成小应用、修复隔离 Issue。
4. 关闭 MacBook 本地会话后，由 Remote Agents 继续执行，查看 GitHub 提交/测试/产物并从 App 或 CLI 恢复。
5. 记录所用模型、实际配额、执行时长、可读写资源与回传方式。证明比本地 AGY 少了多少人工干预。

远端可通过 AGY CLI **agy --remote-agent -c** 继续最近会话；需要交接本机文件时，明确将 GitHub/Drive/Upload 作为资源输入。不要假设 Remote Agent 自动访问本机任意目录。

### 4.3 Argon 的最优使用方式

以用户报告“连续高强度工作后仍剩余 96%”为现实起点，**优先用 Argon 干有复杂度的实事**：规划/实现/调试、跨资料比对、架构优化、视频或图像语义检查、产品分析、真实输出复验。3.8 Flash 可承担高速筛选、常规提取、工具密集型任务；不是因为怕额度就让所有任务默认降级 Flash。

任务目标直接写成 **可运行代码、实际文档、真实视频或可交互应用、实测验收**，而不是“写一份怎样做的 SOP”。需要另一模型时由 AGY 按具体任务对照推理/效果/等待成本选择。

## 5. Google Cloud / GDP credits：从已有 VPN 转向增量产品

### 5.1 不重建 VPN

目标 repo 已经归档四线路 VPN 的配置、双机接力与 Mac/iPhone 的历史 E2E（2026-11-08/09）[G1][G2]。**今晚不再把 VPN 视为“是否能靠 Ultra 免费创建”**：技术上已通过 Google Cloud credits 路线实现。下一阶段只能是有实际需求的维护：按节点流量、服务健康、实际抵扣和总账单检查，避免重复基建。

Cloud credits 是账单折抵，不是每月可直接兑换的现金，也不保证任意服务/任意持续流量无限免费。当前二个账户 US$100 与 US$10 的权益对应不同 Billing 帐本，仍需单独记录真实使用。

### 5.2 US$100/月还能形成哪些产品/服务

| 使用方式 | 具体实物 | 与现有资产怎样结合 | 最小试验 |
| --- | --- | --- | --- |
| **Cloud Run Web API** | PDF/文本转结构化、报告摘要、知识问答、工具调用接口 | AGY 编程 + Gemini API/现有 GitHub | 发布一个隔离 demo、真实请求、监控账单 |
| **Cloud Run Jobs** | 批量研究、生成日报/结果整理、图片处理调度 | GitHub Actions、现有通知渠道 | 一次任务正常/失败执行，回收状态 |
| **AI Studio / Gemini API** | 专项问答、视觉识别、文件分类、复杂问题推理后端 | Gemini 4 Argon、便宜的 Flash 模型配合 | 同样 20 个任务，比较质量/费用 |
| **Firebase** | 用户登录、轻量数据库、手机/网页产品原型 | AGY 生成前端，既有域名/资料 | 可用账号登录并保存状态的小工具 |
| **Vector Search / RAG** | 技术知识库/公开技术资料检索工具 | Drive/公开 PDF、Notebook 研究成果 | 带来源引用和错误修正的问答 Demo |
| **静态页面/产品展示** | 作品展示与付费意向收集 | AGY/Three.js、媒体资产 | 能打开、能体验、能提交反馈 |

**官方 Cloud Run request-based 免费层基准**：每月前 200 万请求、一定 vCPU/RAM 消耗免费，按照 Billing Account 汇总；GPU、长驻实例、网络流量等仍另计 [O7]。重要的是成本与规模比例，而不是为花掉赠金制造虚假流量。

**AI Studio Build** 可以极快制作应用，但官方“无需 Google Cloud 账单可发布 2 个应用的 Starter Tier”仅适用于符合条件的新用户；已有或曾有 GCP billing 账号者不适用。此账户已建立 Billing，因此应按 **Standard Deployment / Cloud Run** 路线试验，而非默认认为有两份额外免费部署权 [O6]。

### 5.3 AI Studio/Gemini API 与 Ultra 消费订阅分开

- Gemini/AGY 网页与 Desktop 配额是**订阅权益**。
- Gemini API / AI Studio 生产调用走**独立项目和 Billing**，适用时可用 GDP credits 抵扣。
- Colab CU / Flow credits / Flow Music credits / Cloud credits 不能互相兑换或替代。
- 不把“可用 Argon 96%”推导成“任意 SaaS API 零现金成本、无限吞吐”。
- GDP 赠金官方说明每笔可在**发放后一年内**使用；月度领取/发放日期取决于最初领取时间，不是所有账户自然月一号刷新 [O5]。

## 6. Colab G4：改造为通用 GPU 实验与批处理平台

**已确认的真实起点**：2026-11-09 账面约 2,497.44 CU、G4 96GB 成功分配；官方 20x 计划**每月分配 2,000 CU**，动态设备可用性不保证每次同卡 [G1][O1]。

### 6.1 优先跑的 5 类非漫剧工作

| 类别 | 例子 | 一次实验输出 | 是否值得常驻 |
| --- | --- | --- | --- |
| **开源 LLM 推理/量化** | Qwen/DeepSeek/Gemma 多模型 4/8-bit、不同上下文长度 | tokens/s、实际显存、TTFT、准确率、CU/千 token | 不建议 Colab 长驻，适合临时评估 |
| **Speech/ASR/TTS** | Whisper/faster-whisper、批量字幕、语音多角色合成 | 音频分钟数、正确率、CU/小时和人力节省 | 按需批处理 |
| **图像/视觉** | OCR、文档视觉理解、图像重建、产品图自动整理 | 百张图片吞吐、误识率、单任务资源耗用 | 批任务 |
| **视频/三维计算** | Upscale、插帧、3DGS、生成模型基准 | 合格成片分钟、视频参数与成本 | 批任务 |
| **模型微调与实验** | 小型开源模型 LoRA/QLoRA、embedding、排序器 | 学习曲线、任务集表现、资源消耗 | 针对具体价值再做 |

X 帖主 **@muihbb** 报告曾在 Colab 上以 88GB 权重测试 Qwen 177B 量化方案，并自述约 120 tok/s [X1]。这只是特定量化/加载/上下文的个人实测陈述，并**不能证明任意 177B 模型能在一张 96GB GPU 上稳定满上下文运行**。最值得先做是小规模对照：7B/27B/更大量化的同题完成质量及 CU，选实际最有效配置。

### 6.2 使用官方现成工具

[O8] 官方 **google-colab-cli** 支持：
- colab run --gpu G4 task.py：一次性创建 GPU、运行代码、回收资源。
- colab usage：查询 CU 速率与余额。
- colab sessions / colab status：列出使用中的任务。
- colab download：拉取结果。
- colab stop：手动停止指定任务。

官方 **colab-mcp** 可连接部分本地 Agent 与浏览器中的 Colab session，但对客户端通知支持有前置要求 [O8b]。已有 CLI 可完成时，无需为了“用了 MCP”再套一个代理。

**部署选型：**Colab runtime 的会话生命周期与 GPU 动态分配适合按需批运算；长期公开 API 选 Cloud Run/GCP。性能指标以当前任务实测为准 [O8c]。

## 7. 深度研究、Notebook、资料生产、科学实验的高回报用途

### 7.1 直接发挥 Ultra 研究能力

Gemini app / 4 Argon 可处理大型文档、PDF、代码、数据及文件生成；2026-10-29 官方已支持在 Gemini 中直接预览编辑多类文档与 PDF [O16]。

Gemini Notebook 在 Ultra 20x 官方表格达到 **每本 Notebook 上限 600 个 sources**，且有研究报告、幻灯片、Audio/Video Overviews、Quizzes、数据表等多种输出；计算配额现在看复杂度和 5h/weekly 刷新，不机械套旧日配额表 [O10]。

比起另建一个巨型知识库，建议用 Notebook 处理**专题知识包**，现有 GitHub/Omni/Obsidian 继续当长期权威保存位置，Notebook 只承担深入研究与多格式转换。

### 7.2 可产生真实收益/节省时间的研究包

- **材料/工程知识研究**：公开材料数据、TGA/黏度/缺陷机理/供应商工艺理论，Notebook 引用→Argon 比较→技术 briefing；对正式工程结论保留原始材料证据，而不是用 AI 自评替代测试。
- **AI 软件与产品技术雷达**：每月整理新模型、API 成本、工具版本与真实用户口碑；产出能帮助 AGY 选择技术栈的结构化资料。
- **独立主题市场研究**：商业痛点、竞品功能/价格/用户反馈、潜在用户愿付费问题，输出可做一个周末 MVP 的具体需求，而不是“AI 很火”。
- **家庭/教育内容**：课文、词语、学习材料、可编辑 Flashcards、Quiz、带引用的短视频与双语解释，以已有资料为输入做个人实用成品。
- **对外知识产品**：高质量研究模板、专业解释图、代码动画、小教程、可追溯数据表。先用自己的真实工作成果验证实用性。

### 7.3 Hypothesis Generation 是一个新领域，而非影视附属

Google Labs Hypothesis Generation 官方可做文献综述、研究空白、假设候选与测试设计；Standard / Advanced research 会产生结构化研究方向，官方有并行运行数量说明 [O17]。适合材料科学、工艺优化、算法与数据实验。它不替代实际实验，但可以为技术问题提供不常规的新假设。这项权益值得单独试一次，有机会超出 AI OS 现有应用范围。

## 8. 收入机会：用已有能力选择赛道，而不是预设拍视频第一

### 8.1 推荐测试组合

| 商业假设 | 产品/内容 | 差异化来源 | 首次用户验证 | 相对投入 |
| --- | --- | --- | --- | --- |
| **B2B 工程资料工具** | 公开测试报告/PDF/质量问题资料的结构化提取、问答及对比小工具 | 实际工程问题理解 + Argon + 文档处理 | 让真实目标用户用公开/模拟数据完成一项任务并反馈价值 | 中 |
| **AI 自动化实用工具** | 商品/价格信息监控、特定信息提醒、技术情报雷达、表格清理 | 现有 AI OS/Telegram/GitHub/Cloud 能力 | 一周内 5–10 个实际用例，测节省时间与是否继续使用 | 低–中 |
| **垂直 Micro-SaaS** | 有明确受众的 PDF/表格/邮件/会议材料转换、专业领域 Agent | AGY 工程效率 + Cloud Run/Gemini API | 单页面 demo、目标客户反馈、愿付费或明确拒付原因 | 中 |
| **技术解释动画与教育内容** | AI/工程原理可视化、动画、中文/英文教程、实验演示 | Argon 生成 code animation + Notebook 研究能力 | 3 条不同题材，比较留存、点击、制作耗时 | 低–中 |
| **AI 漫剧/故事 IP** | 长期连载、竖屏短剧、角色数字资产 | 已有 H3/Flow/QA 工具 | 完整可看短集、有效复访与次集追看 | 中–高 |
| **数字资产/工具模板** | 分镜、研究模板、自动化工作流、UI 组件、音效/音乐包 | 来自实际项目复用素材，非抽象“课程” | 商品展示、下载/复用、付费意向/实际成交 | 低–中 |
| **交互展示/教育小游戏** | Three.js、Blender、Project Genie 交互世界概念 | Argon 长时编码、世界模型创意 | 用户是否愿意体验、分享、继续试玩 | 中 |

**商业排序**：最值得先测试的是“**具备具体痛点的垂直小工具 + 研究/内容分发**”。它能用现有 AGY/Cloud 能力最短 E2E，且可以产生可复制软件资产；AI 漫剧不是被取消，而是与之并行的较高制作投入路线。

### 8.2 来自最近 X Likes 的跨领域信号

- [X2] 用户点赞列表中出现 **ai-goofish-monitor** 的多模态商品筛选/提醒工具，原始 GitHub 为 Usagi-org/ai-goofish-monitor [T2]。说明“自然语言条件 + 持续检索 + 有用提醒 + 页面”是可立即验证的产品模式，但应先选受众、数据源与传播渠道。
- [X3] 一条帖子讲 Apple Watch 录音整理产品的爆发式推广，体现“把用户现有设备变成可直接解决问题的软件”这一思路；**收入数字是帖主叙述，没有独立财务凭据**，不作为投资回报预测。
- [X4] AGY 创作者文章强调 Desktop/CLI、原生浏览器、知识库/MCP、Remote Agents 和工具编排；与官方新 Remote Agent 功能相互支持，但具体体验、成本与配额需本机实践。
- [X1] 177B 量化 GPU 示范，启发“Colab 不只生产视频，还可以模型推理/ASR/研究任务”。
- [X5] 视频/代码动画作者的 **cinecode** 可把 Agent 写的 Three.js/Canvas 程序变成可发的 explainer/产品视频 [T3]；这条内容路线和 H3 完全不同，适合科技教育、软件推广。
- [X6] 一条 GDP credits 推文将 Gemini API、Cloud Run、Firebase 等组合介绍；主要机制已通过 Google 官方资料核对 [O5][O6][O7]。
- [X7] 云 VPN 教程使用 GDP credit 作为节点资金；本项目已有独立四线路 E2E 记录，不重复部署。
- [X8] 有人在 X 讨论使用 Ultra 访问 Claude 高阶模型；官方 AGY 当前型号列表确实包含 Claude Opus/Sonnet 5.5，实际对应额外配额与可用性在 AGY 设置读取 [O3]。

这批信息重点是**技术方法和商业结构**，不是靠点赞量自动选“爆款行业”。

### 8.3 YouTube/TikTok 不应垄断收入路线

媒体方向可以做：
- 连载漫剧 / 小说旁白。
- **代码动画**（科学、工程、技术概念、流程教学）。
- Google Notebook/Argon 支持的资料讲解短视频与长视频。
- 音频讲解 / Flow Music 生成的原创配乐。
- 软件产品 Demo、开发日志、工具实际使用演示。
- 多语言解释内容、交互世界原型演示。

YouTube 的 Shorts/长视频、订阅与其他收益入口分开统计。Google 当前已宣布 **2027-02-01** YPP 新广告/Premium 申请标准会改变 [P1]；短期应首先判断观众真实反应和持续生产成本。TikTok 新加坡 Creator Rewards 是否开放应以账号 Studio 实况为准；TikTok Shop affiliate 的本地通道可以独立调查 [P2]。

**衡量标准**：每条作品和每个软件产品记录**现金成本、订阅额度消耗、Owner 干预时间、实际使用者/复访、点击/留存、付费意向及已到账收入**。没有观众/客户数据之前不虚构月收入。

## 9. 30TB、家庭权益与个人生活生产力

- **30TB Drive**：大模型权重、创作素材、研究原文、音视频母版、文档存档；GitHub 保存可版本化的小文件和索引。避免重复下载，利用压缩包降低 Colab FUSE 小文件读取的延迟 [O8c]。
- **家庭分享**：Google One 官方说明最多 5 位额外成员；存储空间共享，部分 Gemini/AGY/Notebook/AI credits 亦可共享，但部分额度是全家**共享池**而非每人新获得完整 Ultra 配额。加入家庭组要求所属国家一致 [O15]。
- **家庭/学校**：Notebook Flashcards、Quizzes、Audio Overviews、短教育视频、可编辑 worksheet；先验证实际省时和适龄效果，避免重复开发已存在的成熟工具。
- **照片/内容**：Google Photos 和 Gemini 的图像/文件编辑可处理私人素材、家庭资料整理和旅行/相册创作。
- **YouTube Premium**：已有历史激活记录，直接享受消费端价值，无需额外产品工程。
- **Project Genie**：Labs 官方 FAQ 地区列表包括 Singapore [O13]，适合亲子科学场景/交互教材原型；实际资格由账号登入核实。
- **Google Health Premium**：新加坡在支持地区列表中，若实际拥有 Pixel Watch/Fitbit，可作为现成权益；不为“用上福利”额外购置硬件。
- **Google Home Premium Advanced**：官方目前支持列表未见 Singapore，可低优先。
- **Gemini Tasks / AI Inbox / Chrome Auto Browse**：有更窄的官方地区限制，先用现有 MacBook AGY Desktop/Remote Agents 解决实际自动化任务，而非因为网页广告有该产品就重建流程。

## 10. 与现有 AI OS 的联动：聚焦能产生净增益的点

| 现有 AI OS 位置 | Ultra 可补的能力 | 具体闭环 | 为什么不重建 |
| --- | --- | --- | --- |
| AGY 桌面工程执行 | Remote Agents 云端独立执行 + Argon/Claude 高级模型 | GitHub Task→Remote 实现→实际测试→本地接续 | 本地 Desktop 仍掌握 Mac 文件/GUI |
| Hermes/Kelly 持续任务 | AGY 技术探索/一次性工具；Cloud Run 小 API | 已有 Telegram/Cron 触发→API 调用→结果回执 | 不另造持久 Agent 总控 |
| GitHub Canon/Project docs | Argon 文档综述 + Notebook 来源知识包 | 文件/Issue→研究→PR/报告→可追溯版本 | GitHub 继续存标准与状态 |
| Omni/Obsidian 内容系统 | Notebook 研究、Argon 多模态理解、文件编辑 | 已抓取内容→知识提炼→可发布作品/专题 | 不复制第二套知识真相 |
| Cloudflare/现有 VPN | GDP Cloud Run/边缘接入/应用 | 验证已有网络与新服务的分工及成本 | VPN 四线路历史已完成 |
| MacBook 本地模型 | 高质量云 Argon/按需 GPU，大量低延迟本地轻任务 | 任务按质量/延时/成本选路 | 小模型不取代复杂 Agent 核心 |
| 专业工程与资料分析 | Hypothesis Generation + Notebook + Argon + 数值模型 | 公开材料研究→候选假设→测试方案/可视化 | 保留已有可靠数值处理流程 |
| 内容创业 | Flow/Music + code-animation + Notebook + Cloud SaaS | 作品/软件→分发→反馈→版本与收入数据 | 不把全部业务押注一个漫剧频道 |

**关键改进原则**：以交付效果分配执行者；“Ultra 额度多”不是要求把所有当前系统都迁入 Google。“跨平台能力提升”主要体现在独立 Remote Agent、Gemini/Cloud 的新增供给，以及能持续产生产品/作品的流程，不是在 GitHub 里多写治理文件。

## 11. 建议的 30 天实际实验计划（跨多个领域）

| 时段 | 目标 | 必须给出的实际产物 |
| --- | --- | --- |
| **第 1–3 天** | 全权益实况盘点；恢复当前 Ultra 20x/5x、AGY 模型池、Flow、Flow Music、Colab、GDP、Notebook/Genie/家庭福利的状态 | **ENTITLEMENT_INVENTORY**：已可用/尚未激活/地区不适用/已用额度与重置日；不含任何密钥 |
| **第 1–5 天** | AGY Remote Agents 与本地 Desktop 的第一轮真实 E2E | 可追溯 GitHub 任务、远程执行/恢复记录、实际测试/文件交付 |
| **第 4–10 天** | Cloud Run + Gemini API / AI Studio 构建第一个真正可用的窄工具 | 可使用的 Web Demo/API、3 个以上真实样例、错误处理与账单观察 |
| **第 6–12 天** | Notebook / Deep Research / Hypothesis Generation 独立试验 | 一份真实有来源的主题报告 + 可编辑课件/数据表/研究假设 |
| **第 10–17 天** | Colab GPU 非视频基准 2–3 类 | 批量 ASR/开源模型/视觉任务的质量、CU、耗时与资源回收记录 |
| **第 12–23 天** | 2–3 条不同商业方向的小实验：窄工具、代码动画/解释内容、漫剧/数字资产任选 | 实际软件或作品、发布/演示入口、目标用户真实反馈 |
| **第 21–30 天** | 根据真实数据选下一周期主线 | 统一的 **价值/现金贡献/Owner 时间/额度使用** 排序表；保留一两个赢家，暂停明显无需求的方向 |

建议首先由 AGY 完成**跨领域同时盘点，再选产品试验**，而不是先把漫剧下一集当成唯一硬任务。

## 12. 商业机会筛选：一套不自欺的具体比较方法

把每一个候选方向按下列维度打 1–5 分（是实验优先级的**主观初评**，不是测得的统计价值）：

1. **实际痛点/愿付费程度**：能否找到具体用户和重复需求？
2. **独特优势**：用户现有专业知识、已建工具、现有受众/流量是否构成优势？
3. **首个成品时间**：AGY 可否在 1–7 天完成可验证 MVP？
4. **额外现金成本**：Ultra 订阅已支付后，实际新增付费/API/素材/流量费用有多少？
5. **持续维护**：需要多少人力持续运营和修 Bug？
6. **可复用性**：能否把一次成功沉淀为工具、资产、模板或下个项目的基础？

**建议当前第一梯队：**(1) AGY Remote Agents 能力验证；(2) 轻量垂直软件工具；(3) Notebook 专题研究与教育/技术产品；(4) Colab 非媒体 GPU 批任务。**漫剧、其他视频创作与交互原型为并行产品实验**，不是统领全部工作的前置条件。

一个 MVP 的有效结果不必先收钱：让真实用户完成一个原本做不到/很麻烦的任务、愿意反复使用或者明确表示拒绝使用的原因，都比更多空泛“商业机会分析”有信息价值。只有已经产生现金或可归属的成本节省时才记入财务收益。

## 13. AGY 可直接执行的下一轮综合任务（非漫剧专项）

**目标：最大化 Ultra 订阅的真实价值，独立发现技术与产品机会，选择并交付最值得做的下一项实物。**

1. **先读当前 GitHub**：google-ai-ultra-lab 最新 HEAD/AGENTS/CURRENT_STATE/ROADMAP、VPN 与 Colab 文档，以及本报告；识别完成事项，不重复建设。
2. **全权益现场盘点**：逐项读取本人现有 30TB Ultra 的实际可用入口、额度、重置日、Cloud credits 领取、Project Genie、Notebook、Flow/Music、AGY Remote Agent，输出一张按价值排序的可用清单。
3. **Remote Agents E2E**：按官方 CLI/项目资源方式跑一项有真实 GitHub 交付和测试的任务，明确本地与远端的资料边界和恢复路径。
4. **一个小软件产品 E2E**：自行比较“专业文档小工具”“价格/信息监控”“AI 研究/教育工具”，选最有实际用户痛点的一项，用 AGY + AI Studio + Cloud Run/现有 GCP 最短实现、实际访问并回读使用成本。
5. **一个非视频 GPU E2E**：在 Colab 跑真实 ASR/模型或视觉任务，记录 CU、质量、吞吐、任务结束资源状态，避免 GPU 只绑定视频业务。
6. **跨领域商业发现**：至少比较 6 个不同类型机会（B2B 工具、普通 SaaS、内容/教育、数字资产、互动体验、服务自动化），给出优先级和一个可实验的具体用户需求。
7. **保留已有创作工程**：漫剧已完成的基线不需要推倒；需要时继续 AI 漫剧专项 brief，但**不能用它代替整个 Ultra 综合研究和项目机会发现**。
8. **结果交付**：核心输出是“权益实况表 + 真实 Remote E2E + 一个能用的 MVP + 一次 GPU 实验 + 面向下一个月的机会排序”，并将实际测得的新增事实写回适用的项目资料。不要用长 SOP/主观自评分数替代实际产物。

**执行分工：**AGY 继续负责本项目工程落地；本报告提供跨领域机会排序和下一轮实测任务。

## 14. 来源与可复核入口

### 官方产品、开发与地区可用性

- **[O1] Google One Ultra 2026 权益** — https://support.google.com/googleone/answer/16286513?hl=en
- **[O2] Google AI plans（5x/20x）** — https://one.google.com/about/google-ai-plans/
- **[O3] AGY Plans / Models** — https://antigravity.google/docs/plans ; https://antigravity.google/docs/models/
- **[O4] AGY Remote Agents / Features / Headless** — https://antigravity.google/docs/remote-agents/ ; https://antigravity.google/docs/features ; https://antigravity.google/docs/cli/headless/
- **[O5] GDP 福利与赠金机制** — https://developers.google.com/profile/help/benefits?hl=zh-cn
- **[O6] AI Studio Deploy / Billing** — https://ai.google.dev/gemini-api/docs/aistudio-deploying ; https://ai.google.dev/gemini-api/docs/billing
- **[O7] Google Cloud Run pricing** — https://cloud.google.com/run/pricing
- **[O8] 官方 Colab CLI** — https://github.com/googlecolab/google-colab-cli
- **[O8b] 官方 Colab MCP** — https://github.com/googlecolab/colab-mcp
- **[O8c] Google Colab FAQ** — https://research.google.com/colaboratory/faq.html
- **[O9] Flow credits/models** — https://support.google.com/flow/answer/16526234?hl=en ; https://support.google.com/flow/answer/16352836?hl=en
- **[O10] Gemini Notebook plans / usage** — https://support.google.com/gemininotebook/answer/16213268 ; https://support.google.com/gemininotebook/answer/17670842
- **[O11] Gemini Notebook study tools** — https://blog.google/innovation-and-ai/products/gemini-notebook/new-study-tools-september-2026/
- **[O12] Argon interactive/game/software examples** — https://blog.google/products-and-platforms/products/gemini/gemini-4-argon-builders/ ; https://blog.google/products-and-platforms/products/gemini/gemini-4-argon-in-action/
- **[O13] Labs fx FAQ / Project Genie regional list** — https://labs.google/fx/faq
- **[O14] Project Genie expansion** — https://blog.google/innovation-and-ai/models-and-research/google-deepmind/project-genie-expands/
- **[O15] Google One family sharing** — https://support.google.com/googleone/answer/9004015?hl=en
- **[O16] Gemini files edit & generation** — https://blog.google/innovation-and-ai/products/gemini-app/edit-files-directly/ ; https://blog.google/innovation-and-ai/products/gemini-app/generate-files-in-gemini/
- **[O17] Hypothesis Generation** — https://support.google.com/hypothesis-generation/answer/17106281?hl=en
- **[O18] Jules 官方停止计划（2026-10-29）** — https://jules.google/docs/changelog/2026-10-29
- **[O19] Gemini 4 Argon 官方发布** — https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-4-argon/

### 本项目当前 GitHub 证据（历史实测，非当前登录）

- **[G1] 当前状态与权益台账** — https://github.com/solarfans/google-ai-ultra-lab/blob/main/CURRENT_STATE.md
- **[G2] 已有私人 VPN 四线路技术与 E2E** — https://github.com/solarfans/google-ai-ultra-lab/blob/main/docs/gcp_dual_node_vpn.md
- **[G3] 本地 LLM 节点** — https://github.com/solarfans/google-ai-ultra-lab/blob/main/docs/local_uncensored_llm_node.md
- **[G4] 既有漫剧专项审计（本报告的一个领域附件）** — https://github.com/solarfans/google-ai-ultra-lab/blob/main/docs/research/GOOGLE_AI_ULTRA_VALUE_AND_CREATOR_STRATEGY_2026-11-10.md

### Bird X 原帖：跨领域用户经验

- **[X1] Colab 177B 模型尝试（社区自述）** — https://x.com/muihbb/status/2119248663432319140
- **[X2] 二手商品 AI 监控工具示例** — https://x.com/Fred834567/status/2119761926620324329
- **[X3] Apple Watch 应用创业例子（收入未经独立核实）** — https://x.com/RachidSettas/status/2118675372468293647
- **[X4] AGY 自动化与 Remote Agents 长文** — https://x.com/chasen_liao/status/2118640065714729150
- **[X5] cinecode/代码动画** — https://x.com/sarpstar/status/2119082994925211686
- **[X6] GDP Cloud credits 产品用途讨论** — https://x.com/StatsWire/status/2114751606923374886
- **[X7] GDP + 私人 VPN 研究帖** — https://x.com/RainG999/status/2118531452774314026
- **[X8] AGY 实际自动化工作方式长文** — https://x.com/KOF97AI/status/2118957099078340729

### 外部 GitHub 技术案例

- **[T1] Gemini 官方 Cookbook** — https://github.com/google-gemini/cookbook
- **[T2] ai-goofish-monitor** — https://github.com/Usagi-org/ai-goofish-monitor
- **[T3] cinecode** — https://github.com/sarpstar/cinecode
- **[T4] Colab/视频混合工作站 WorldForge** — https://github.com/designfuchen/worldforge

### 平台收入查询入口

- **[P1] YouTube 2027-02-01 YPP 变化** — https://support.google.com/youtube/answer/12843009
- **[P2] TikTok Shop Singapore creator eligibility** — https://seller-sg.tiktok.com/university/essay?knowledge_id=8818745439618817

---

**研究完成的标准**：找出 **Ultra 每个资源池最有价值的实际用途**，快速把高价值方向变成真实可用的作品、工程工具或产品，并以使用反馈、效果与成本决定继续投入的方向。