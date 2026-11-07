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
| **Colab 算力** | 约 2,000 ~ 2,500 CU/月 |  **已确认 (2,500.00 CU)** | `colab usage` 回读当前满额余额：2,500.00 计算单元 |
| **G4 96GB GPU** | NVIDIA RTX PRO 6000 Ada/Blackwell |  **实测开机验证成功** | `colab run --gpu G4` 秒级分配：NVIDIA RTX PRO 6000 Blackwell Server Edition (97,887 MiB ~96GB 显存，176GB 内存，236GB 磁盘，CUDA 13.0)；执行完毕后已自动安全终止 |
| **Cloud Credits** | 约 $100 / 月 | ⏳ 待激活 | 待注册 Google Cloud Developer Program 绑定账单 |
| **Google Flow** | 约 25,000 点 / 月 | ⏳ 待使用 | 网页后台已确认包含，待短剧音画生成时调用 |
| **Antigravity** | Gemini 4 Argon + Claude Opus |  **已就绪** | 顶级模型池在 AGY 中可用，云端 Remote Agents 已灰度放量 |

---

## 2. 工程规划与执行状态

- **战略路线图**：已确立并归档至 [**ROADMAP.md**](./ROADMAP.md)，涵盖短剧工业化、TikTok/YouTube 自动化爆款矩阵、有声书长音频三大引擎。
- **外部工具审计**：已完成 `Minireel/HGhub` 与 `DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED` 评估并归档至 [`references/external_tools_audit.md`](./references/external_tools_audit.md)。
- **算力守门员 Skill**：已安装并固化 `google-ai-ultra` 算力计量与防漏跑规则。

---

## 3. 下一步行动计划

1. **G4 容器实跑验证**：通过 `ultra_meter.py run` 启动 G4 容器，渲染《楚氏春秋》第 2 镜（刘禅御书房定妆出图，1344x768），验证单镜耗时与实际 CU 扣减。
2. **生成物回传与质检**：拉取图像至本地资产库 `pipelines/short_drama/assets/` 进行人物特征与画质确认。
3. **推进第 1 集全量 5 镜视效**：定妆确认后批量出图并接驳 MiniMax H3 进行 5 秒动态转绘。
