---
name: google-ai-ultra
description: >-
  Google AI Ultra (30TB + 2500 CU + 25000 Flow) compute workstation, Colab G4 (96GB Blackwell) GPU orchestrator,
  and 3D Guoman CG AI Manju (AI 漫剧) production skill for Antigravity (AGY). Use this skill whenever the user asks to
  check Colab compute units (CU), run tasks on Colab G4/A100 GPUs, produce AI Manju / animated short dramas, generate
  novel audiobooks, manage 30TB Google Drive assets, or execute cloud GPU workloads safely.
---

# Google AI Ultra — Compute Workstation, Zero-Burn SOP & AI 漫剧总纲 (v4.0)

This skill equips Antigravity (AGY) with zero-leak operational command over the **Google AI Ultra (30 TB + 2,500 CU + 25,000 Flow credits)** subscription, **Colab G4 (96GB RTX PRO 6000 Blackwell)** hardware, and the **3-Layer Deterministic + 5-Gate Self-Auditing 3D Guoman CG AI Manju (AI 漫剧)** production pipeline.

Full repository playbook: `/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/docs/AI_MANJU_AND_ULTRA_SOP.md`
Lessons Learned ledger: `/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/LESSONS_LEARNED.md`

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
6. **铁律 6（5 道自动化门禁 `manju_qa_gate.py` + 多模态视听双检闭环）**：
   - **编译前**：必须运行 `python3 scripts/manju_qa_gate.py <manifest.json>`，自动完成原著原文核对、常识分镜检查、声学失真检测（ZCR < 0.20）与口语词长检测（单分句 $\le 16$ 字）；
   - **出片后 / 交付前（自主发现缺陷铁律）**：严禁只看 `ffprobe` 元数据就交付！AGY **必须同时使用 `read_file` 查看抽帧图像（`.jpg`）并亲耳聆听音频文件（`.wav`）**，自主检查：(a) 是否有鬼叫/杂音/机械念书感，(b) 画面动作与台词语义是否 100% 吻合，(c) 内心独白时人物是否保持闭嘴。发现瑕疵立即在本地或单镜重修，绝不把半成品抛给用户充当质检员。
7. **铁律 7（强制生命周期自毁 + Finder 即点即播交付）**：
   - 渲染结束必定销毁会话并确认 `Active assignments: 0` (`0.00 CU/h`)；
   - 所有交付 MP4 必须经 [`scripts/subtitle_manju.py`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/scripts/subtitle_manju.py) 去除 `【角色名】` 框、注入 `-movflags +faststart` 并在 macOS Finder 高亮呈现。

---

## 2. Deterministic AI Manju Production Commands (v4.0)

### Step 1: 生成高表现力 Neural TTS 音色种子（0 CU 本地完成）
```bash
cd "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab"
uv run --with edge-tts python3 scripts/generate_neural_voice_seeds.py
```

### Step 2: 运行 5 道自动化质量门禁并编译分集工作流（0 CU 本地完成）
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

### Step 5: 查看算力台账与紧急止损
```bash
python3 /Users/kaykel/.gemini/config/skills/google-ai-ultra/scripts/ultra_meter.py usage
python3 /Users/kaykel/.gemini/config/skills/google-ai-ultra/scripts/ultra_meter.py stop-all
```
