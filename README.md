# Google AI Ultra Lab

> **定位**：Google AI Ultra 30 TB 订阅算力与高阶权益最大化工程实战库。由 Antigravity (AGY) 独立执行，拒绝形式主义跑分，以**“高品质 AI 短剧与小说广播剧资产化、探索被动收入”**为核心交付目标。

---

## 一、订阅基线与已确认事实（2026-11-07）

- **订阅方案**：Google AI Ultra 30 TB（土区 Apple 订阅渠道，₺2,949.99/月，约合 $65~$85/月）。
- **确认状态**：
  -  Google One 首页确认生效：`Google AI Ultra`，云存储容量 `30 TB`（已验证）。
  -  YouTube Premium（个人与品牌频道）已确认激活。
  -  MacBook 本地已安装 Google 官方 `google-colab-cli`（v0.7.5），支持终端直连 G4 (96GB RTX 6000 Ada)。
- **核心算力资源**：
  - **Colab 计算单元**：约 2,000 ~ 2,500 CU/月（支持调度 G4 96GB，费率约 10.05 CU/小时，相当于每月约 200 小时 96GB 顶级 GPU 算力）。
  - **Google Cloud Credits**：约 $100/月（Google Developer Program 渠道）。
  - **Google Flow / Flow Music**：约 25,000 ~ 30,000 credits/月。
  - **Antigravity 顶级配额**：Gemini 4 Argon、Claude Opus、Gemini 3.8 Flash 及云端 Remote Agents。

---

## 二、核心落地战略：双轮驱动的商业与内容流水线

严格遵循 **Issue #159 戒律**：彻底砍掉无意义的横向模型跑分与纸上谈兵，将算力全量聚焦在“能沉淀真实内容资产、具备被动收入潜力”的双主线上：

```
                             Google AI Ultra (30TB + 2000 CU)
                                            │
                ┌───────────────────────────┴───────────────────────────┐
                ▼                                                       ▼
  【主线 A：AI 短剧 / 爆款短视频自动化流水线】              【主线 B：小说切片 ➡️ 有声广播剧自动工业化】
 1. 爆款剧情与分镜生成 (Gemini 4 / 去审查模型)             1. 原创小说分章与角色提取 (Gemini Argon)
 2. 定妆首帧与人物一致性 (Colab G4: Qwen-Image-2.1)        2. 角色多音色克隆与情感配音 (Colab: Qwen3-TTS / Fish)
 3. 首帧生视频+口型对白 (Colab G4: MiniMax H3)             3. 情绪背景音乐自动配乐 (Google Flow Music)
 4. 自动合成、字幕与防翻车成片 (ffmpeg)                  4. 交付完整有声书，分发喜马拉雅/YouTube
```

---

## 三、推进路线图与里程碑

### 阶段 1：环境极简握手与 G4 算力探测（Day 1）
- [x] 安装官方 `google-colab-cli` 命令行工具。
- [ ] 完成 Chrome 单次 OAuth 授权，实现终端免密无头调度。
- [ ] 运行 `colab new --gpu G4`，记录实际分配显存、RAM、磁盘及 CU 扣费率，验证后立即安全关机。

### 阶段 2：MVP 短剧第一作成片交付（Day 2 - 4）
- [ ] 吸收社区 `@yangleiocx3` 实测经验，编写自动化流水线：
  - 提取 5 个镜头（中景、特写、广角），每个镜头 5 秒；
  - Qwen-Image-2.1 出 1792×1024 高清首帧（利用参考图锁定人物面部、服装一致性）；
  - MiniMax H3 图生视频（1344×768 双声道，包含台词对白与环境音效）；
  - ffmpeg 自动拼接合成 30 秒带声画完整成片，自动归档至 Google Drive 30TB 盘。
- **交付目标**：第一部可直接在手机/电脑播放的 30 秒高品质短剧成片，实测单部消耗约 6.5 CU（约 $0.65）。

### 阶段 3：小说切片广播剧/有声书流水线（Day 5 - 7）
- [ ] 结合本地已有的小说续写底座（SAGA V2 / CH001-CH002）：
  - Gemini 自动提取角色对话表与旁白；
  - Colab 部署开源高表现力 TTS（Qwen3-TTS 或 CosyVoice）；
  - Flow Music 匹配情节氛围配乐，批量渲染第一集 10 分钟广播剧 Demo。

### 阶段 4：常驻与被动收入渠道铺设（Day 8 - 30）
- [ ] 结合红果短剧（HongGuo）等爆款剧本套路，建立批量剧本改写 Agent；
- [ ] 用 Google Cloud Credits 部署常驻云服务，打通自动化渲染与社交平台发布管道；
- [ ] 评估首月实际投入产出比（ROI），做出续订与商业化放大决策。

---

## 四、免责与安全红线

1. **零账单意外**：绝不擅自开通额外付费项或升级付费 API，严格控制在每月 Ultra 赠送额度内。
2. **防空转关机机制**：所有在 Colab 运行的脚本均挂载 `try...finally` 自动保存至 Google Drive 并主动停止会话，杜绝挂机浪费 CU。
3. **独立治理**：不依赖 ChatGPT 中介，由 AGY 本地终端与 GitHub 形成直接闭环。
