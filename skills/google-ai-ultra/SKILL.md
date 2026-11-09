---
name: google-ai-ultra
description: >-
  Google AI Ultra (30TB + 2500 CU + 25000 Flow) compute workstation, Colab G4 (96GB Blackwell) GPU orchestrator,
  and 3D Guoman CG AI Manju (AI 漫剧) production skill for Antigravity (AGY). Use this skill whenever the user asks to
  check Colab compute units (CU), run tasks on Colab G4/A100 GPUs, produce AI Manju / animated short dramas, generate
  novel audiobooks, manage 30TB Google Drive assets, or execute cloud GPU workloads safely.
---

# Google AI Ultra — Compute Workstation, Zero-Burn SOP & AI 漫剧总纲 (v3.0)

This skill equips Antigravity (AGY) with zero-leak operational command over the **Google AI Ultra (30 TB + 2,500 CU + 25,000 Flow credits)** subscription, **Colab G4 (96GB RTX PRO 6000 Blackwell)** hardware, and the **3-Layer Deterministic 3D Guoman CG AI Manju (AI 漫剧)** production pipeline.

Full repository playbook: `/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/docs/AI_MANJU_AND_ULTRA_SOP.md`

---

## 1. Six Golden Rules (防烧卡、零浪费与防作弊铁律)

Whenever planning or executing tasks with Google AI Ultra, AGY must strictly adhere to [Zero-Burn & Anti-Cheat SOP](./references/zero_burn_sop.md):

1. **铁律 1（全面锁定 AI 漫剧，严禁真人换脸与静态图伪装）**：
   - 默认采用红果短剧最高成功率的 **【3D 国漫 / UE5 影视 CG 风】**（对标《凡人修仙传》《剑来》《画江湖之不良人》）；
   - **绝对禁止**使用真人生活照、OpenCV (`seamlessClone`) 2D 抠图换脸、或 `ffmpeg` 平移缩放静态图（Ken Burns）冒充视频；禁止退回 `SDXL 1.0 / SVD-XT / SadTalker`。
2. **铁律 2（原著剧情铁律对齐 + 三层确定性架构，严禁手写长 Prompt 漂移）**：
   - 开工前必须读取原著章节切片（如 `/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/novel-continuation-lab/books/chushi-chunqiu/source/raw/chapters/`）与设定圣经（[`CHUSHI_CHUNQIU_CANON_BIBLE.md`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/CHUSHI_CHUNQIU_CANON_BIBLE.md)）；
   - **严禁每集手写冗长 ComfyUI JSON 或散乱提示词**！必须通过三层确定性架构驱动：
     - **Layer 1（只读设定金库）**：[`character_vault.json`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/character_vault.json)（锁定世界观、角色真实姓名/年龄、1344×768 三视图定妆照、专属 WAV 声纹种子）；
     - **Layer 2（分集剧本清单）**：`epXX_<name>_manifest.json`（仅填引用角色 ID、首帧图、对白文本与运镜）；
     - **Layer 3（确定性编译器 + 单会话批量执行器）**：运行 [`scripts/manju_compiler.py`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/scripts/manju_compiler.py) 自动校验角色合法性并编译出标准工作流 JSON。
3. **铁律 3（G4 单会话批量热显存复用 + HF CDN `aria2c` 直拉）**：
   - 选 G4 (96GB Blackwell) 时**保持「高 RAM」关闭**（默认已给满 97,887 MiB 显存 + 本地 NVMe）；
   - 严禁依赖 Google Drive FUSE 挂载；优先通过 `aria2c -x 16 -s 16` 从 HuggingFace CDN 并发直拉 42.3 GB 权重至 `/content/ComfyUI/models`（实测 149s 落盘）；
   - **整集多镜头必须在同一个 G4 会话内批量排队执行**（开启 `--highvram --disable-mmap --fast`），使第 2~N 镜享受 **0 秒冷启动 + 0 秒模型重载**。
4. **铁律 4（ComfyUI + MiniMax-H3 漫剧提速与防崩核心参数）**：
   - **参考图 Token 去重（提速核心）**：`MiniMaxH3ReferenceToVideo` 只挂载 2 张角色设定卡（`ref_image_0`, `ref_image_1`），镜头首帧仅通过 `MiniMaxH3AddGuide (frame_idx=0, strength=1.0)` 注入一次，每步自注意力立省 `4,032` 个视觉 Token；
   - **6-Step Turbo 极速采样**：搭配 `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors`，采用 `steps=6, tail_steps=2`（实测单镜 10.125s 243 帧仅需 **207 秒 / 3.45 分钟**，约 **0.50 CU/镜**）；
   - **双角色音色精准路由**：`<Audio 1>` / `<Audio 2>` 搭配 `<d>[Mandarin] 台词</d> He/She closes his/her mouth after speaking`，末尾强制追加反字幕硬约束。
5. **铁律 5（Google Flow 25,000 积分协同）**：
   - 宏大空镜、战争场面、自然灾难转场优先使用 Ultra 附赠的 Google Flow 积分（0 Colab CU），Colab G4 专攻角色开口对白与对手戏。
6. **铁律 6（强制生命周期自毁 + 本地抽帧与音画质检门禁）**：
   - 点火前后运行 `ultra_meter.py` 对账，结束必定销毁会话并确认 `Active assignments: 0` (`0.00 CU/h`)；
   - 视频拉回本地后，AGY 必须用 `ffprobe` 与 `read_file` 逐镜检查画面、口型与音轨，确认无误后再执行无损拼接（`ffmpeg -f concat -c copy`）交付。

---

## 2. Deterministic AI Manju Production Commands

### Step 1: 编译并校验分集工作流（0 CU 本地瞬间完成）
```bash
cd "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab"
python3 scripts/manju_compiler.py
```

### Step 2: 单会话 G4 批量渲染整集镜头（自动计费对账 + 自动释放 G4）
```bash
python3 /Users/kaykel/.gemini/config/skills/google-ai-ultra/scripts/ultra_meter.py run --gpu G4 --timeout 2400 scripts/run_ep01_batch_g4.py > /tmp/colab_ep01_batch.log 2>&1
```

### Step 3: 查看算力台账与紧急止损
```bash
python3 /Users/kaykel/.gemini/config/skills/google-ai-ultra/scripts/ultra_meter.py usage
python3 /Users/kaykel/.gemini/config/skills/google-ai-ultra/scripts/ultra_meter.py stop-all
```
