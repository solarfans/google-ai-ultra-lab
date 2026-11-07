# Google AI Ultra Lab — Antigravity Engineering Guidelines

Scope: Repository `solarfans/google-ai-ultra-lab`.
Role: Independent Antigravity Desktop engineering executor for Google AI Ultra compute workflows.

## Core Rules & Zero-Burn SOP (零浪费与防烧卡黄金铁律)

1. **铁律 1（0 CU 本地备料）**：
   - 剧本、分镜、中英双语提示词、角色定义、负向提示词必须在本地 MacBook（0 CU 消耗）编排校验完毕后，方可申请开机。
   - 严禁开着按小时计费的 G4 (10.05 CU/h) 或 A100 显卡去现场想剧本或调试提示词。
2. **铁律 2（0 CU 预备环境）**：
   - Colab CPU 实例扣费为 0.00 CU 免费；
   - 大模型权重拉取与环境预热优先在 0 CU CPU 容器中运行，并持久化到 30TB Google Drive（`/content/drive/MyDrive/AI_Workstation/`）；
   - G4 显卡开机只负责纯推理，严禁在贵价 GPU 上耗时拉取大文件。
3. **铁律 3（强制生命周期自毁）**：
   - 单次批处理任务优先使用 `colab run --gpu G4 ...`，执行完毕后容器由底层驱动自动安全销毁；
   - 若使用会话模式（`colab new`），脚本代码必须包裹在 `try...finally` 块中，在退出或发生异常时必定调用 `colab stop`；
   - 每次点火前后必须运行 `colab usage` 打点，记录开机前余额、关机后余额与实际扣费。
4. **铁律 4（防翻车提示词门禁）**：
   - 视频生成必须在提示词末尾强制包含负向门禁约束：`"不要出现任何字幕、水印或英文乱码，text, watermark, subtitles, English letters, blurry, deformed limbs"`，防止因字幕烧录导致废片重跑。
5. **铁律 5（以可消费作品为唯一交付标准）**：
   - 遵循 Issue #159 戒律，拒绝脱离实际业务的学术跑分；
   - 每次点火必须以输出实际可观看的 MP4 视频、可听的广播剧音频或训练好的权重为交付物。
