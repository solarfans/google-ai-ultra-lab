# Google AI Ultra Lab

> **定位**：Google AI Ultra 30 TB 订阅算力与高阶权益最大化工程实战库。由 Antigravity (AGY) 独立执行，拒绝形式主义跑分，以**“高品质 AI 短剧与小说广播剧资产化、探索被动收入”**为核心交付目标。

---

## 一、订阅基线与已确认事实（2026-11-07）

- **订阅方案**：Google AI Ultra 30 TB（土区 Apple 订阅渠道，₺2,949.99/月，约合 $65~$85/月）。
- **确认状态**：
  -  Google One 首页确认生效：`Google AI Ultra`，云存储容量 `30 TB`（已验证）。
  -  YouTube Premium（个人与品牌频道）已确认激活。
  -  MacBook 本地已安装 Google 官方 `google-colab-cli`（v0.7.5），支持终端直连 G4 (96GB RTX 6000 Ada/Blackwell)。
  -  OAuth 认证已握手成功，实测 `colab usage` 回读可用算力 **2,500.00 CU**。
  -  G4 硬件分配成功验证：分配 NVIDIA RTX PRO 6000 Blackwell Server Edition (97,887 MiB ~96GB 显存，176GB 内存)，测试后自动销毁会话（0 损耗）。
- **核心算力资源**：
  - **Colab 计算单元**：满额 **2,500.00 CU/月**（调度 G4 96GB 费率约 10.05 CU/小时，相当于每月约 248 小时 96GB 顶级 GPU 算力）。
  - **Google Cloud Credits**：约 $100/月（Google Developer Program 渠道）。
  - **Google Flow / Flow Music**：约 25,000 ~ 30,000 credits/月。
  - **Antigravity 顶级配额**：Gemini 4 Argon、Claude Opus、Gemini 3.8 Flash 及云端 Remote Agents。
  - **本地混合算力底座**：MacBook M3 Pro 承载私有无审查大模型 (`uncensored`, 32K 上下文, 43.9 tok/s, Metal GPU 加速)，配备 Telegram Bot Ella (v2.1 按需智能收口) 与 Cloudflare 穿透网关。详见 [**docs/local_uncensored_llm_node.md**](./docs/local_uncensored_llm_node.md)。

---

## 二、核心落地战略：三大商业变现与内容产出引擎

严格遵循 **Issue #159 戒律**：彻底砍掉无意义的横向模型跑分与纸上谈兵，将算力全量聚焦在“能沉淀真实内容资产、具备被动收入潜力”的三大引擎上。详细分阶段规划请参阅完整文档：[**ROADMAP.md (长期战略规划与工程路线图)**](./ROADMAP.md)。

```
                                  ┌──────────────────────────────────────────┐
                                  │ Google AI Ultra (30 TB + 2,500 CU / 月) │
                                  │ MacBook 24/7 本地自动化常驻调度中枢       │
                                  └─────────────────────┬────────────────────┘
                                                        │
         ┌──────────────────────────────────────────────┼──────────────────────────────────────────────┐
         ▼                                              ▼                                              ▼
【引擎 1：AI 影视级短剧工业化】             【引擎 2：TikTok / YouTube 自动爆款矩阵】     【引擎 3：小说长音频与多角色广播剧】
- 目标：精品 IP 视觉化与短剧出海             - 目标：轻量高频起号，赚取平台流量分成与广告   - 目标：长尾睡前沉浸音频与长视频合集
- 素材：《楚氏春秋》等长篇优质小说           - 题材：历史奇闻/悬疑反转/哲学故事/冷知识     - 特性：Gemini 对话提取 + Qwen3-TTS
- 核心：Qwen-Image 定妆 + MiniMax 动态       - 特性：全自动脚本 ➡️ 批量分镜 ➡️ 自动剪辑     - 平台：YouTube Long-form / 喜马拉雅 / 播客
- 交付：30s-60s 竖屏单集连续剧              - 交付：每日定时自动推送至海外社媒账号         - 交付：10-30 分钟带环境声与配乐成品
```

---

## 三、推进路线图概览（详见 ROADMAP.md）

- **阶段 1：算力基线验证与首镜画格实测（已达成）**
  - [x] 安装官方 `google-colab-cli` 命令行工具与 OAuth 本地自动握手。
  - [x] 成功开机 G4 96GB 容器验证硬件参数与自动安全关机（0 算力漏扣）。
  - [x] 建立 `google-ai-ultra` 算力计量与防漏扣专属 Skill。
  - [x] 审计社区前沿开源项目（`HGhub` 短剧客户端、`9B Uncensored` 恶斗剧本模型），归档至 [`references/external_tools_audit.md`](./references/external_tools_audit.md)。
  - [x] 提取《楚氏春秋》外传章 5 镜短剧规范（`pipelines/short_drama/chu_shi_chun_qiu_ep01.json`）。
  - [x] **基准测试**：Colab G4 运行 Shot 02 定妆出图（1344x768），实测推理 2.01s，单镜扣减 0.00 CU。
- **阶段 2：MVP 成片交付与海外发布渠道打通（已完成重构）**
  - [x] 批量跑通《楚氏春秋》第一集全量 5 镜视效画格（Colab G4 单容器批跑 4.58s，0.00 CU 扣减）。
  - [x] 研发端到端短剧合成编排引擎（`scripts/compose_short_drama.py`），整合多角色 Neural 配音、动态运镜、中文字幕卡与雨夜氛围混音。
  - [x] 交付首部 32.5 秒完整短剧成品视频 `chu_shi_chun_qiu_ep01_final.mp4` (5.24 MB)、`chu_shi_chun_qiu_ep01.srt` 及母带音频。
  - [x] **重构工业级渲染核心**：淘汰 SDXL 1.0 + SVD-XT，全面升级为 `Qwen-Image-2.1`（参考图垫图锁脸）+ `MiniMax-H3`（33B Native AV-DiT 带口型台词拟声），引入 FreedomAIG 六段式标准语法与 `colab-ultra-workstation` 75 秒 NVMe 极速预热与防烧卡工作流。
  - [x] 交付 52.42 秒母带成片 `chu_shi_chun_qiu_ep01_qwen_minimax_master.mp4` (10.45 MB) 与外挂字幕。
  - [ ] 试水海外 TikTok 与 YouTube Shorts 自动排期发布测试。
- **阶段 3：自动化内容管线与 24/7 无人值守发布（Day 9 - 18）**
  - [ ] 充分发挥 MacBook 24 小时开机中枢优势，打通热点选题到视频自动上架全流程。
- **阶段 4：商业化 ROI 结算与规模化决策（Day 19 - 30）**
  - [ ] 核算全周期算力与被动收入表现，制定续订与放大方案。

---

## 四、免责与安全红线

1. **零账单意外**：绝不擅自开通额外付费项或升级付费 API，严格控制在每月 Ultra 赠送额度内。
2. **防空转关机机制**：所有在 Colab 运行的脚本均挂载 `try...finally` 自动保存至 Google Drive 并主动停止会话，杜绝挂机浪费 CU。
3. **独立治理**：不依赖 ChatGPT 中介，由 AGY 本地终端与 GitHub 形成直接闭环。
