---
name: google-ai-ultra
description: >-
  Google AI Ultra (30TB + 2500 CU + 25000 Flow) compute workstation, Colab G4 (96GB Blackwell) GPU orchestrator,
  and 3D Guoman CG AI Manju (AI 漫剧) production skill for Antigravity (AGY). Use this skill whenever the user asks to
  check Colab compute units (CU), run tasks on Colab G4/A100 GPUs, produce AI Manju / animated short dramas, generate
  novel audiobooks, manage 30TB Google Drive assets, or execute cloud GPU workloads safely.
---

# Google AI Ultra — Compute Workstation, Zero-Burn SOP & AI 漫剧总纲 (v4.5)

This skill equips Antigravity (AGY) with zero-leak operational command over the **Google AI Ultra 20x (30 TB + Colab CU + 25,000 Flow Video credits + 30,000 Flow Music credits + $100/mo GDP Cloud credits)** subscription, **Colab G4 (96GB RTX PRO 6000 Blackwell)** hardware, and the **6-Gate Self-Auditing + Hybrid Multi-Model (`MiniMax-H3` + `Flow Veo 3.1 Lite / Omni 1.2` + `Flow Music`) 3D Guoman CG AI Manju (AI 漫剧)** production pipeline.

Full repository playbook: `/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/docs/AI_MANJU_AND_ULTRA_SOP.md`
Creator & Ultra Value Strategy: `/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/docs/research/GOOGLE_AI_ULTRA_VALUE_AND_CREATOR_STRATEGY_2026-11-10.md`
Lessons Learned ledger: `/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/LESSONS_LEARNED.md`

---

## 0. Five-Pool Quota Ledger & Hybrid Model Routing (2026-11-10 官方口径与混合生产矩阵)

严禁将不同产品的额度混为一谈。每次规划与生产按以下 **5 类独立成本池** 与 **镜头路由表** 分配资源：

| 权益池 | Ultra 20x 官方额度與规则 | 漫剧生产定位与路由策略 |
| :--- | :--- | :--- |
| **1. AGY / Gemini 4 Argon** | 20x 档位（Owner 推理余量充裕） | **常驻总导演、连续性编剧与冷读 QA**。负责剧情因果设计、分镜阻塞预检、多模态抽帧/音频冷读审查与故障最小实验归因；正则、时长、SHA-256 指纹与 FFmpeg 混音全部交由确定性 Python 脚本执行。 |
| **2. Colab GPU (`CU`)** | 标准发放 2,000 CU/月（当前实测余额 `2,484.46 CU`） | **主力角色演出与口型渲染 (`MiniMax-H3`)** + 批量后期。用于固定国漫角色身份、双人交锋对白、微表情与声纹驱动；强制受 `ultra_meter.py` 单任务硬超时与 `try...finally` 进程级释放保护。 |
| **3. Flow Video (`Credits`)** | 25,000 credits/月（按账单月刷新，不结转） | **空镜、大场面转场与 A/B 候选镜头补充**。`Veo Extend` 已于 11-05 退役，`Veo 3.1 Fast/Quality` 与 `Omni 1.1` 将于 12-05 退役。当前主力：**`Veo 3.1 Lite`**（4/6/8s，**Ultra 20x Lower Priority 档为 `0 credits`**）用于空镜/氛围候选；**`Omni Flash 1.2`**（前 10s 为 `3 credits/s`=30 credits）用于高冲击力大场面或局部视频修改。 |
| **4. Flow Music (`Credits`)** | 30,000 credits/月（**含 Member 商业使用授权**） | **商用级主题曲、古风配乐与情绪铺底（BGM）**。独立于视频积分池，替代单调合成音床，生成带商业版权的专属国漫主题曲与悬疑转场音乐轨。 |
| **5. GDP Cloud & 30TB Drive** | US$100/月 Cloud Credits（有效期 1 年）+ 30TB Drive | **Cloud** 用于已验证的小型常驻网络/API 服务；**30TB Drive** 归档大容量无损母带（Clean Master）、角色母本与分轨工程，避免把几十 MB 的原始渲染中间片无限塞入 Git 仓库。 |

---

## 1. Seven Golden Rules (防烧卡、原著高还原、自然声学与自主闭环质检铁律)

Whenever planning or executing tasks with Google AI Ultra, AGY must strictly adhere to [Zero-Burn & Anti-Cheat SOP](./references/zero_burn_sop.md) and [`LESSONS_LEARNED.md`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/LESSONS_LEARNED.md):

1. **铁律 1（全面锁定 3D 国漫 CG，严禁真人换脸与静态图伪装）**：
   - 默认采用红果短剧最高成功率的 **【3D 国漫 / UE5 影视 CG 风】**（对标《凡人修仙传》《剑来》《画江湖之不良人》）；
   - **绝对禁止**使用真人生活照、OpenCV (`seamlessClone`) 2D 抠图换脸、或 `ffmpeg` 平移缩放静态图（Ken Burns）冒充视频；禁止退回 `SDXL 1.0 / SVD-XT / SadTalker`。
2. **铁律 2（原著逐景精读锚定，严禁跨章记流水账）**：
   - 开工前必须逐段精读原著章节切片（`/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/novel-continuation-lab/books/chushi-chunqiu/source/raw/chapters/`）与 [`CHUSHI_CHUNQIU_CANON_BIBLE.md`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/CHUSHI_CHUNQIU_CANON_BIBLE.md)；
   - **一集（6~8 镜）只精做一章的核心戏剧冲突**，严禁把两章内容粗暴压缩成 5 个干瘪的流水账镜头；
   - 每个分镜必须在 `epXX_<name>_manifest.json` 中填写 `canonical_anchor`（包含原著章节文件名、行号与原文原句 `source_quote`），由 [`scripts/manju_qa_gate.py`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/scripts/manju_qa_gate.py) 自动做原文子串核验，杜绝篡改人物动机（如吴安然逃亡平原郡、回味豆花店按铜钱入木桌毛遂自荐、暗施大搜魂手等关键细节）。
3. **铁律 3（打破死板双人站桩：四模态镜头路由与“魂穿双轨声音法则”）**：
   - **严禁所有镜头都用“两人面对面站桩轮流念 4.5 秒课文”的死板模板**！必须根据剧情合理选择 [`scripts/manju_compiler.py`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/scripts/manju_compiler.py) (v3.0) 的 4 种镜头模式：
     - `offscreen_pa_and_os`（画内单人表演 + 画外广播/OS）：如客机失事镜头，画面仅展示现代男主在座位上惊恐发短信，空姐广播通过后期航空带通滤波（`highpass=400,lowpass=3200`）作为画外音播放，**严禁让空姐拿电话站在乘客座位旁广播**；
     - `single_inner_monologue_os`（画内闭嘴演眼神 + 成年人灵魂混响独白 OS）：表现“六岁幼童身体 + 成年人灵魂”时，画面上小楚铮**必须紧闭双唇**通过眼神和动作演戏，音轨播放带混响（`aecho`）的 **28 岁成年男声（`zh-CN-YunxiNeural`）内心独白**；
     - `os_plus_short_spoken`（哭腔诉说 + 闭嘴流泪内心独白 + 最终短促开口）：如王秀荷磕头滴血认母镜头；
     - `natural_dialogue`（带肢体动作交锋的短句对白）：每个呼吸分句 **$\le 16$ 个汉字**，多用口语停顿（`……`、`，`、`！`），彻底消除“拿着书照着念”的机械感。
4. **铁律 4（永久禁用 `say` 机械音与 `asetrate` 变调，强制使用高表现力 Neural TTS）**：
   - **绝对禁止**使用 macOS `say -v Tingting` 或 `ffmpeg asetrate` 硬拉音高制作参考音色（会产生高频金属鬼叫失真与机器人朗读腔）；
   - 所有音色种子与后期画外音必须由 [`scripts/generate_neural_voice_seeds.py`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/scripts/generate_neural_voice_seeds.py) 基于 `edge-tts` / `CosyVoice2` 生成，并写入 `voice_seeds_manifest.json` 供门禁校验。
5. **铁律 5（G4 单会话批量热显存复用 + 6-Step Turbo 极速采样）**：
   - 选 G4 (96GB Blackwell) 时**保持「高 RAM」关闭**，通过 `aria2c -x 16 -s 16` 从 HuggingFace CDN 直拉权重至 `/content/ComfyUI/models`；
   - `MiniMaxH3ReferenceToVideo` 仅挂载 2 张角色设定卡，首帧通过 `MiniMaxH3AddGuide (frame_idx=0)` 注入一次；采用 `steps=6, tail_steps=2` 在单会话内批量渲染整集。
6. **铁律 6（6 道自动化门禁 `manju_qa_gate.py` + 指纹断点续跑 + 冷读视听双检闭环）**：
   - **指纹校验断点续跑（`manju_compiler.py` v3.2）**：严禁仅凭 `status == "completed"` 盲目跳过！编译器自动计算每个镜头的 `input_fingerprint`（SHA-256 覆盖 `shot_mode`、角色、台词、首帧 PNG 内容哈希）并检查输出 MP4 是否存在且 $>100\text{ KB}$；任何台词或首帧修改都会自动触发该镜重编译。
   - **渲染前预检（Gates 1–5）**：运行 `python3 scripts/manju_qa_gate.py <manifest.json>`，自动完成原著原文核对、常识分镜检查、声学失真检测（ZCR < 0.20）、口语词长检测（单分句 $\le 16$ 字）与双轨时间戳零重叠检测。
   - **出片后验闭环（Gate 6 `--post-render` + 多模态视听冷读）**：运行 `python3 scripts/manju_qa_gate.py <manifest.json> --post-render` 校验每个实际渲染 MP4 的流完整性与对白时间窗声学能量（dBFS > -36 dBFS）；随后 AGY **必须同时使用 `read_file` 查看抽帧图像（`.jpg`）并亲耳聆听音频文件（`.wav`）**，以“冷读观众视角”检查：(a) 是否有鬼叫/杂音/尾句截断，(b) 画面动作与台词语义是否 100% 吻合，(c) 内心独白/广播时人物是否保持闭嘴。
7. **铁律 7（强制生命周期自毁 + 双画幅母带与发行规范）**：
   - 渲染结束必定销毁会话并确认 `Active assignments: 0` (`0.00 CU/h`)；
   - 保留无字幕 `Clean Master` 与独立分轨（对白/OS/PA/BGM），按平台需求导出 `16:9` 横屏版与 `9:16` 竖屏安全区版；应对 **YouTube 2027-02-01 YPP 新规**（广告分成需 1,000 订阅 + 8,000 长视频观看小时/365 天或 2,000 万 Shorts/90 天），采用“单集短剧引流 + 多集合集长片/幕后解析沉淀长视频时长”的双轨发行策略。

---

## 2. Deterministic AI Manju Production Commands (v4.5)

### Step 1: 生成高表现力 Neural TTS 音色种子（0 CU 本地完成）
```bash
cd "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab"
uv run --with edge-tts python3 scripts/generate_neural_voice_seeds.py
```

### Step 2: 运行 Pre-Flight 5 道门禁并基于 SHA-256 指纹增量编译工作流（0 CU 本地完成）
```bash
cd "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab"
python3 scripts/manju_qa_gate.py pipelines/short_drama/ep02_zhuanshi_chongsheng_manifest.json
python3 scripts/manju_compiler.py pipelines/short_drama/ep02_zhuanshi_chongsheng_manifest.json
```

### Step 3: 本地合成双轨预告音轨（OS 混响 + 航空 PA 滤波 + 对白）并用 `read_file` 实听自检
```bash
cd "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab"
uv run --with edge-tts python3 scripts/synthesize_episode_audio_preview.py pipelines/short_drama/ep02_zhuanshi_chongsheng_manifest.json
```

### Step 4: 单会话 G4 批量渲染整集镜头（自动计费对账 + 自动释放 G4）
```bash
python3 /Users/kaykel/.gemini/config/skills/google-ai-ultra/scripts/ultra_meter.py run --gpu G4 --timeout 2400 scripts/run_ep02_batch_g4.py > /tmp/colab_ep02_batch.log 2>&1
```

### Step 5: Post-Render 第 6 道成片门禁校验与混音母带压制
```bash
cd "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab"
python3 scripts/master_ep02_v2_audio.py
python3 scripts/manju_qa_gate.py pipelines/short_drama/ep02_zhuanshi_chongsheng_manifest.json --post-render
```

### Step 6: 查看算力台账与紧急止损
```bash
python3 /Users/kaykel/.gemini/config/skills/google-ai-ultra/scripts/ultra_meter.py usage
python3 /Users/kaykel/.gemini/config/skills/google-ai-ultra/scripts/ultra_meter.py stop-all
```
