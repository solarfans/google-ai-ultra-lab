# Google AI Ultra Lab — Current State & Ledger

**最后更新**：2026-11-07 SGT  
**项目状态**：`V1_0_0_INITIATED / AGY_TAKEOVER / REPO_CREATED / COLAB_CLI_INSTALLED`  
**负责席位**：Antigravity Desktop (MacBook)  

---

## 1. 订阅与权益状态清单

| 权益项目 | 官方标称/社区数据 | 当前实测状态 | 验证方式/凭据 |
| :--- | :--- | :--- | :--- |
| **会员级别** | Google AI Ultra 30 TB |  **已确认** | Google One 首页已显示 "Google AI Ultra, 30 TB" (Melvin Guo) |
| **订阅成本** | ₺2,949.99 / 月 |  **已确认** | Apple 订阅页面截图证实，12 月 7 日自动续费 |
| **YouTube Premium** | 个人与品牌频道会员 |  **已确认** | 个人身份与 yoursolar 品牌频道均显示 Premium 标识 |
| **Colab 算力** | 约 2,000 ~ 2,500 CU/月 | ⏳ 待握手回读 | 本地 `google-colab-cli` v0.7.5 已安装就绪，待单次 OAuth 激活 |
| **G4 96GB GPU** | NVIDIA RTX PRO 6000 Ada | ⏳ 待开机测试 | `colab new --gpu G4` 待验证分配延迟与 CU 扣费率 |
| **Cloud Credits** | 约 $100 / 月 | ⏳ 待激活 | 待注册 Google Cloud Developer Program 绑定账单 |
| **Google Flow** | 约 25,000 点 / 月 | ⏳ 待使用 | 网页后台已确认包含，待短剧音画生成时调用 |
| **Antigravity** | Gemini 4 Argon + Claude Opus |  **已就绪** | 顶级模型池在 AGY 中可用，云端 Remote Agents 已灰度放量 |

---

## 2. 下一步行动计划

1. **终端 OAuth 单次授权**：在已登录 Ultra 账号的 Chrome 中完成 `colab usage` 的单次点击放行。
2. **G4 开机短跑测试**：运行 5 分钟测试脚本，回读实际 GPU 硬件参数、显存与扣费速率后立即关机。
3. **第一部分镜脚本起草**：为 30 秒 MVP 短剧选定剧本框架并开始出定妆首帧。
