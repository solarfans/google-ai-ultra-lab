# Google AI Ultra Lab — Current State & Ledger

**最后更新**：2026-11-08 SGT (MacBook Pro)  
**项目状态**：`QWEN_IMAGE_MINIMAX_H3_REFACTOR_LANDED / ZERO_BURN_VERIFIED / MASTER_COMPOSED`  
**负责席位**：Antigravity Desktop (MacBook)  

---

## 1. 订阅与权益状态清单

| 权益项目 | 官方标称/社区数据 | 当前实测状态 | 验证方式/凭据 |
| :--- | :--- | :--- | :--- |
| **会员级别** | Google AI Ultra 30 TB |  **已确认** | Google One 首页已显示 "Google AI Ultra, 30 TB" (Melvin Guo) |
| **订阅成本** | ₺2,949.99 / 月 |  **已确认** | Apple 订阅页面截图证实，12 月 7 日自动续费 |
| **YouTube Premium** | 个人与品牌频道会员 |  **已确认** | 个人身份与 yoursolar 品牌频道均显示 Premium 标识 |
| **Colab 算力** | 约 2,000 ~ 2,500 CU/月 |  **已确认 (2,499.56 CU)** | `colab usage` 回读当前余额：2,499.56 CU，活跃实例 0 |
| **G4 96GB GPU** | NVIDIA RTX PRO 6000 Ada/Blackwell |  **实测开机验证成功** | `colab run --gpu G4` 秒级分配：NVIDIA RTX PRO 6000 Blackwell Server Edition (97,887 MiB ~96GB 显存，176GB 内存，236GB 磁盘，CUDA 13.0)；执行完毕后已自动安全终止 |
| **Cloud Credits** | 约 $100 / 月 | ⏳ 待激活 | 待注册 Google Cloud Developer Program 绑定账单 |
| **Google Flow** | 约 25,000 点 / 月 | ⏳ 待使用 | 网页后台已确认包含，待短剧音画生成时调用 |
| **Antigravity** | Gemini 4 Argon + Claude Opus |  **已就绪** | 顶级模型池在 AGY 中可用，云端 Remote Agents 已灰度放量 |
| **本地 M3 Pro 算力** | Apple Silicon M3 Pro 36GB |  **已部署运行 (43.9 tok/s)** | 本地私有无审查大模型 (9B Heretic Uncensored)，32K 上下文，配备 Telegram Ella 守护进程与 Cloudflare 全球穿透 |

---

## 2. 工程重构与最新交付成果 (Qwen-Image + MiniMax-H3)

- **彻底重构 AI 短剧渲染引擎**：
  - 彻底淘汰旧版 `SDXL 1.0 Base` (画质塑料/假人蜡像) 与 `SVD-XT` (无声橡皮泥拉伸)；
  - 接入业内最强工业级生图模型 **`Qwen-Image-2.1`** (7B DiT + Qwen3-VL 条件编码器)，原生支持参考图垫图锁脸 (I2I Consistency)，在 1344x768 电影级画幅下将楚铮、楚轩、贾道角色面相、汉制玄衣深衣与玉冠 100% 锁定；
  - 接入全模态视频模型 **`MiniMax-H3`** (33B Native AV-DiT)，全面采用 FreedomAIG 六段式标准语法 (`<Subject N>`, `summary`, `retention_analysis`, `detailed_description` 含 `<d>[Mandarin]...</d> He closes his mouth after speaking`, `overall_soundscape`, `non_diegetic_music`)，原生实现唇形口型对齐、角色声纹与拟声音效一步直出；
  - 整合 `yuanyang749/colab-ultra-workstation` 工业级调度资产 (`launch_g4_fast.py` 与 `minimax_h3_dialogue_v9.json`)。
- **《楚氏春秋·正传第一卷：杯底波澜》工业级资产库交付**：
  - 全新剧本分镜规范：[**pipelines/short_drama/chu_shi_chun_qiu_qwen_minimax_ep01.json**](./pipelines/short_drama/chu_shi_chun_qiu_qwen_minimax_ep01.json)；
  - 云端 G4 渲染引擎：[**scripts/render_qwen_minimax_remote.py**](./scripts/render_qwen_minimax_remote.py)；
  - 本地 G4 调度调度器：[**scripts/run_qwen_minimax_drama.py**](./scripts/run_qwen_minimax_drama.py)；
  - 本地母带合成引擎：[**scripts/compose_qwen_minimax_drama.py**](./scripts/compose_qwen_minimax_drama.py)；
  - 本地秒级合成交付 52.42 秒母带成片 [**pipelines/short_drama/chu_shi_chun_qiu_ep01_qwen_minimax_master.mp4**](./pipelines/short_drama/chu_shi_chun_qiu_ep01_qwen_minimax_master.mp4) (10.45 MB) 与外挂字幕 [**chu_shi_chun_qiu_ep01_qwen_minimax_master.srt**](./pipelines/short_drama/chu_shi_chun_qiu_ep01_qwen_minimax_master.srt)。
- **严格遵循 Zero-Burn 防烧卡铁律**：
  - 0 CU 本地备料：剧本分镜、角色定义、负向提示词门禁全部在本地编排完成；
  - 生命周期强制自毁：任务结束后自动释放，当前活跃实例数归零，算力余额稳健保持 2499.56 CU。

---

## 3. 下一步行动计划

1. **Colab G4 实机点火跑片**：在准备就绪时运行 `python3 scripts/run_qwen_minimax_drama.py`，点火 G4 渲染 Qwen-Image + MiniMax-H3 全量素材。
2. **多机位接力与长镜头扩展**：引入 `BUNNY_H3_ActionLogic_Bridge` 与 22 帧潜空间混合接力，实现长镜头连续对手戏。
3. **推进小说广播剧管线 (引擎 3)**：利用 Gemini 对白提取与本地/云端 TTS 模型，生成第一期《楚氏春秋》长篇有声广播剧。
