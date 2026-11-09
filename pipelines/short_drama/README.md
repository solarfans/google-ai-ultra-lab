# 主线 A：Colab G4 96GB 3D 国漫影视 CG 风 AI 漫剧生产流水线 (v2.0)

> **规范主文档**：[`docs/AI_MANJU_AND_ULTRA_SOP.md`](../../docs/AI_MANJU_AND_ULTRA_SOP.md)
> **事故复盘与红线**：[`LESSONS_LEARNED.md`](../../LESSONS_LEARNED.md)

## 核心设计理念 (v2.0 3D 国漫 CG 漫剧)

针对 2026-11-08 真人全家福短剧试错中暴露的“真人恐怖谷”、“OpenCV 贴图换脸假面感”与“Ken Burns 静态图晃动伪造视频”问题，本流水线全面升级为**全非真人角色出镜的 3D 国漫影视 CG 风（UE5 级《凡人修仙传》《剑来》风格）AI 漫剧工业化管线**：

1. **视觉画风锁定**：`3D Chinese animation style, Unreal Engine 5 cinematic render, Donghua CG style, subsurface scattering translucent jade skin, delicate 3D modeled silk clothing, blindbox/high-precision 3D character proportions`。
2. **三件套前置定妆资产（0 CU 本地/工作台锁定，Gate 1）**：
   * `16:9` 1344×768 三视图角色设定卡（正面/侧面/半身，纯灰底 `#808080`，无文字水印）；
   * `16:9` 1344×768 纯空景锚点图（固定机位、光源与景深）；
   * `16:9` 1344×768 分镜首帧定妆图 + 15~30s 纯净干声参考音频（`Qwen3-TTS` / `IndexTTS-2.5`）。
3. **Colab G4 96GB + MiniMax-H3 (`Singularity v1.3 INT8`) 单镜 10s 音画同出（Gate 2）**：
   * 禁用真人皮肤毛孔 LoRA（`h3-realism-people` 与 `minimax-h3-facial-realism-closeup` 权重强制为 `0.0`）；
   * 启用 `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors`（8 步极速，`steps=8, cfg=1.0, res_multistep`）+ `BunnyH3ConditioningBridge` (`alpha=0.10`)；
   * 6 段式精准时间轴 Prompt + `<d>[Mandarin]...</d>` 原生音画口型同步（24fps × 10s = `241` 帧）。
4. **跨镜头接力与双轨剪辑（Gate 3）**：
   * 多镜头使用 `MiniMaxH3MotionContext` (`context_length="22"`, `audio_context_length=18`) + `MiniMaxH3JoinMatch` (`strength=0.35`)；
   * 彻底禁止 `ffmpeg zoompan / sin(t)` 静态图平移缩放伪造视频、禁止 `SDXL 1.0 / SVD-XT` 降级、禁止 `OpenCV / InsightFace` 贴图换脸。

## 目录工作流说明

* [`workflows/minimax_h3_manju_mvp_10s.json`](./workflows/minimax_h3_manju_mvp_10s.json)：**v2.0 标准 10 秒单镜 3D 国漫 CG 音画一体工作流**（`241` 帧，8 步 Turbo + `minimax_h3_latent_upscaler_3d_conv_v1_bf16` 二段式 3D 潜空间超分，写实毛孔 LoRA 已剔除）。
* [`workflows/minimax_h3_dialogue_v9.json`](./workflows/minimax_h3_dialogue_v9.json)：多段连续对白接力参考工作流（`MotionContext` + `JoinMatch` + `AddGuide`，已将两个真人皮肤毛孔 LoRA 默认权重归零 `0.0`）。
