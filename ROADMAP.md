# Google AI Ultra Lab — 长期战略规划与工程路线图 (Project Roadmap)

> **版本**：v2.0.0 (2026-11-09 SGT — 战略升级为 **AI 漫剧工业化管线**)  
> **制定席位**：Antigravity Desktop (MacBook 本地 24/7 常驻)  
> **核心操作法典**：[**docs/AI_MANJU_AND_ULTRA_SOP.md (AI 漫剧工业化生产总纲与操作守则)**](./docs/AI_MANJU_AND_ULTRA_SOP.md)  
> **惨败教训警示**：[**LESSONS_LEARNED.md (11-08 真人短剧惨败深度复盘)**](./LESSONS_LEARNED.md)  
> **核心使命**：拒绝纸上谈兵、拒绝静态图伪造视频（严格遵循 Issue #159）。最大化利用 Google AI Ultra 顶级算力（30TB 云盘 + 2,500 CU/月 G4 96GB GPU + 25,000 Google Flow 积分 + $100/月 GCP Credits），将其转化为**可量化、高一致性、零恐怖谷的 3D 国漫 CG 级 AI 漫剧资产与自动化内容管线**。

---

## 一、 防任务漂移与防作弊黄金准则 (Anti-Drift & Anti-Cheat Principles)

1. **全面转向 AI 漫剧（非真人出镜）**：彻底放弃“家庭真人照片换脸短剧”，默认锁定红果短剧爆款率最高、一致性最稳的 **【3D 国漫 / UE5 影视 CG 风】**（对标《凡人修仙传》《画江湖之不良人》）与 **【高精 2.5D 国风厚涂漫】**。
2. **五条死刑红线**：
   - 严禁使用 `ffmpeg` 摇晃静态图（Ken Burns）冒充视频；
   - 严禁使用 OpenCV 几何贴图换脸；
   - 严禁退回 `SDXL 1.0` / `SVD-XT` / `SadTalker` 等过时模型；
   - 严禁未经本地抽帧与音轨自检就把算法半成品抛给 Owner；
   - 严禁未经 **「10 秒单镜头 MVP 验收」** 就盲目一次性批跑整集。
3. **零空跑损耗（Zero-Burn SOP）**：
   - 本地 0 CU 完成剧本、分镜、角色四联身份板（Character Sheet）与首帧审核；
   - 首次拉取大模型走免费 CPU（0 CU/h）落盘 30TB Drive；
   - G4 (96GB Blackwell) 采用双通道 75s NVMe 极速预热（`launch_g4_comfyui_fast.py`），跑完立即强杀会话并执行双轨对账（确认 `Active assignments: 0`）。
4. **双视频引擎协同（Colab G4 + Google Flow）**：
   - **Colab G4 + `MiniMax-H3 (33B Native AV-DiT)`**：专职处理角色开口说话、微表情对峙与多镜头声纹锁定（`Self-Anchor Voice`）；
   - **Google Flow (25,000 积分/月)**：0 Colab CU 专职处理宏大战争、暴风雪空难、城池全景等无需中文口型的大场面镜头。

---

## 二、 三大高价值内容与基建引擎

```
                                  ┌──────────────────────────────────────────────────────────┐
                                  │ Google AI Ultra (30TB + 2,500 CU + 25,000 Flow + $100 GCP)│
                                  │ MacBook M3 Pro 24/7 本地常驻调度与多模态审核中枢         │
                                  └────────────────────────────┬─────────────────────────────┘
                                                               │
         ┌─────────────────────────────────────────────────────┼─────────────────────────────────────────────────────┐
         ▼                                                     ▼                                                     ▼
【引擎 1：3D 国漫 CG 级 AI 漫剧管线】           【引擎 2：爆款视频逆向与纯代码动效矩阵】       【引擎 3：全球高可用基础设施与私有节点】
- 画风：3D 国漫 CG (UE5质感) / 2.5D 厚涂漫     - 逆向：omni-content-pipeline + Gemini 逐秒拆解 - 网络：GCP 台湾+美西双机接力 VPN (已上线)
- 资产：四联角色身份板 + 纯空镜 + 独立首帧      - 选品：HGhub 挖掘红果热播漫剧黄金 3 秒钩子     - 备用：Google AI Pro 独立美西节点 (已上线)
- 渲染：G4 ComfyUI H3 (关闭真人毛孔LoRA) + Flow - 代码动效：sarpstar/cinecode 零废片科普/沙盘   - 算力：本地 M3 Pro 9B Heretic 无审查节点
- 交付：10s 单镜 MVP ➡️ 60s 竖屏/横屏漫剧成片   - 广播剧：小说对话提取 + 多角色配音母带         - 护栏：250GB/35GB 流量熔断锁 + 0 CU 泄漏
```

---

## 三、 四阶段实施路径与交付门禁 (Phased Milestones)

### 阶段一：算力基建、全球 VPN 矩阵与惨败教训固化（已达成 ✅）
- [x] 安装 `google-colab-cli` + `colab-dfs-ext` 无头零浏览器挂载扩展，验证 2,500 CU 额度与 G4 96GB 瞬时分配。
- [x] 部署 MacBook M3 Pro 本地私有无审查大模型节点（`9B Heretic Uncensored`, 43.9 tok/s, 32K 上下文）。
- [x] 利用 Ultra ($100/月) 与 Pro ($10/月) Cloud Credits 建成跨台湾/美西/新加坡的全球 4 线高可用 VPN 矩阵（含 250GB/35GB 自动流量熔断锁）。
- [x] 深度复盘 11-08 真人短剧失败根因，归档 [`LESSONS_LEARNED.md`](./LESSONS_LEARNED.md)。
- [x] 精读 Owner 7 日 X 点赞（50+ 篇推文 / 11 篇万字长文）与红果漫剧行业数据，制定 [`docs/AI_MANJU_AND_ULTRA_SOP.md`](./docs/AI_MANJU_AND_ULTRA_SOP.md) 及 [`references/external_tools_audit.md`](./references/external_tools_audit.md)。

---

### 阶段二（Phase 2A）：AI 漫剧「10 秒单镜头 MVP」闭环验收（当前首要门禁 🎯）
- **核心目标**：严格遵循 Miller (`@TuyetloanP81840`) 与 jonny (`@aggs8p`) 规范，先用 **1 个角色 + 1 个场景 + 1 句台词（5~10 秒）** 跑通真正工业级质量的 **3D 国漫 CG 风漫剧单镜头**，彻底洗刷昨日耻辱。
- **执行门禁（逐级点火，未过前门不开后门）**：
  - [ ] **Gate 1（0 CU 角色与空镜资产验收）**：生成主角【16:9 3D 国漫四联角色身份板（含全身、鞋靴、三视图与表情特写）】+【无人物纯净空镜场景图】+【第 1 镜高清首帧】，经 AGY 放大自检后呈交 Owner 确认画风与人物颜值。
  - [ ] **Gate 2（Colab G4 + 真 ComfyUI H3 单镜渲染）**：在 G4 (96GB) 上通过 `launch_g4_comfyui_fast.py` 极速挂载 ComfyUI + `MiniMax-H3 (Singularity v1.3)`（关闭真人写实毛孔 LoRA），输入 `<Picture 1>`(首帧) + `<Picture 2>`(身份板) + 六段式英文动作/中文 `<d>` 台词提示词，生成 5~8 秒原生带对白、真张嘴、真动态、带环境拟音的 MP4 视频，跑完立即关机查账。
  - [ ] **Gate 3（本地抽帧质检与字幕包装）**：AGY 在本地抽帧检验确认无画面烧录乱码字、无变形、口型与语音同步，使用 `auto_subtitle.py` 压制对齐中文字幕，交付 Owner 验收。

---

### 阶段三（Phase 2B）：单集 60 秒多镜头 AI 漫剧连续剧交付
- **核心目标**：在 Gate 1–3 单镜 MVP 获 Owner 认可后，扩展为 6~10 个镜头的 60 秒完整单集漫剧。
- **关键技术动作**：
  - [ ] 提取第 1 镜主角原生干声转为 `32kHz` 立体声母本（`Self-Anchor Voice`），配合单说话人门控锁定全集跨镜头音色；
  - [ ] 启用 `MiniMaxH3MotionContext (22帧)` + `MiniMaxH3JoinMatch (manual, strength=0.35)` 手动除雾无缝续接；
  - [ ] 对不满意单镜使用 `H3SaveAVLatent` (`4.8MB`) + `--only-seg N` 3 分钟手术刀热插拔重修；
  - [ ] 结合 Google Flow 生成的宏大空镜与 2~3 段听众反应镜头（J-Cut / L-Cut 盖切），合成 60 秒成片。

---

### 阶段四：红果爆款逆向与规模化 IP 连载
- [ ] 利用 `HGhub` 与 `omni-content-pipeline` + AGY Gemini 视频逆向能力，一键拆解红果百亿级爆款漫剧（如《持械入宋》《万妖图录传》）的运镜与分镜模板。
- [ ] 建立《楚氏春秋》（严格对齐 `solarfans/novel-continuation-lab` 原著设定与 [`CHUSHI_CHUNQIU_CANON_BIBLE.md`](./pipelines/short_drama/CHUSHI_CHUNQIU_CANON_BIBLE.md)）的固定角色资产库（Character Vault），实现低 CU 成本按集连载。
