# Google AI Ultra Lab — Antigravity Engineering Guidelines

Scope: Repository `solarfans/google-ai-ultra-lab`.
Role: Independent Antigravity Desktop engineering executor for Google AI Ultra compute workflows.

## Core Rules
1. **Issue #159 Anti-Overengineering Codex**:
   - 严禁假大空、形式主义打卡、横向无意义跑分；
   - 每一轮研发必须以“产生可播放、可交付的实际音视频/文本资产”为交付标准。
2. **GPU 算力管理与防烧卡铁律**:
   - 任何在 Colab 启动的会话，必须在脚本尾部或 `try...finally` 块中调用自动关机指令（`colab stop`），并确保产出物已安全同步至 Google Drive。
   - 严禁挂机闲置消耗 CU。
3. **安全与授权边界**:
   - 绝不开启未经 Owner 明确批准的额外付费项目；
   - 绝不向 GitHub 提交个人账号凭据、OAuth Token 或私有 Cookie。
