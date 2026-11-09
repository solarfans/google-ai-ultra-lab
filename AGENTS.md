# Google AI Ultra Lab — Antigravity Engineering Guidelines

Scope: Repository `solarfans/google-ai-ultra-lab`.
Role: Independent Antigravity Desktop engineering executor for Google AI Ultra compute workflows & AI Manju (AI 漫剧) production.
Canonical Playbook: [`docs/AI_MANJU_AND_ULTRA_SOP.md`](./docs/AI_MANJU_AND_ULTRA_SOP.md)

## Core Rules & Zero-Burn SOP (零浪费、防烧卡与防作弊铁律)

1. **铁律 1（全面聚焦 AI 漫剧，严禁真人换脸与静态图伪装）**：
   - 默认采用红果短剧最高成功率的 **【3D 国漫 / UE5 影视 CG 风】**（或 2.5D 高精国风厚涂漫），**严禁使用家庭真人照片，严禁使用 OpenCV (`seamlessClone`) 2D 抠图换脸**；
   - **严禁使用 `ffmpeg` 平移缩放静态图（Ken Burns）冒充动态视频**，严禁退回 `SDXL 1.0 / SVD-XT / SadTalker` 等过时模型。
2. **铁律 2（0 CU 本地备料 + 三类母本资产先行）**：
   - 开机前必须在本地完成剧本动作外显化、生成【16:9 角色四联身份板（必写鞋子、白底）】+【无人物纯净空镜场景图】+【镜头独立首帧】；
   - **10 秒单镜头 MVP 门禁**：新角色/新流程必须先跑通「1 角色 + 1 场景 + 1 句台词（5~10 秒）」单镜头并经 Owner 验收，严禁一上来盲目批跑整集。
3. **铁律 3（90 秒 NVMe 极速预热 + 0 CU CPU 下载）**：
   - 首次下载几十 GB 模型权重必须走 0.00 CU 免费 CPU 实例落盘 30TB Drive；
   - 在 G4 (96GB Blackwell，保持「高 RAM」关闭) 上运行 ComfyUI 时，严禁直接 `ln -s` 软链读取 Google Drive FUSE（会卡死 28 分钟）；必须先用双通道预热脚本（`463 MB/s`）75 秒内将权重拉入本地 NVMe SSD (`/content/fast_models`)，并以 `--highvram --disable-mmap --fast` 锁死显存。
4. **铁律 4（MiniMax-H3 漫剧六大必配参数）**：
   - **关闭写实毛孔 LoRA**：跑漫剧时必须旁路/关闭 `h3-realism-people` 与 `Facial-Realism-CloseUp`；
   - **结构化提示词**：英文写镜头与动作（单段只写 1 个贯穿运镜）+ 中文写 `<d>[Mandarin] 台词</d> He closes his mouth after speaking` + 中文场景白名单 + 末尾强制追加 `No subtitles, no text, watermark, 不要出现任何字幕`；
   - **声纹锁定**：从第 1 镜剥离 H3 原生干声转 `32kHz` 立体声 WAV 作为后续镜头的 `<Audio 1>`（`Self-Anchor Voice`），每镜只挂当前说话人的 1 路音频（单说话人门控）；
   - **手动除雾**：多段续接时 `MiniMaxH3JoinMatch` 必须设为 `tuning="manual", strength=0.35, min_excess=2.5, match_spread=False, match_detail=False`；
   - **单镜热插拔**：保存 `4.8MB` `AV_LATENT` 断点，局部返修使用 `--only-seg N`。
5. **铁律 5（强制生命周期自毁 + 交付前抽帧自检）**：
   - 每次点火前后必须运行 `colab usage` 打点，任务结束在 `finally` 中强杀实例并确认 `Active assignments: 0` (`0.00 CU/h`)；
   - 视频拉回本地后，AGY 必须先抽帧放大自检（确认真张嘴、无烧录乱码字、无黑线撕裂）并完成字幕对齐后，方可呈交 Owner。
