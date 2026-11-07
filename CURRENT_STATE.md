# Google AI Ultra Lab — Current State & Ledger

**最后更新**：2026-11-07 SGT  
**项目状态**：`EP01_FULL_5_SHOTS_DELIVERED / FINAL_MP4_COMPOSED / ZERO_BURN_VERIFIED / MASTER_AUDIO_EXTRACTED`  
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
| **本地 M3 Pro 算力** | Apple Silicon M3 Pro 36GB |  **已部署运行 (43.9 tok/s)** | 本地私有无审查大模型 (9B Heretic Uncensored)，32K 上下文，配备 Telegram Ella 守护进程与 Cloudflare 全球穿透 |

---

## 2. 工程规划与执行状态

- **战略路线图**：已确立并归档至 [**ROADMAP.md**](./ROADMAP.md)，涵盖短剧工业化、TikTok/YouTube 自动化爆款矩阵、有声书长音频三大引擎。
- **G4 批量渲染通关 (5 镜全量集齐)**：
  - 首镜 Shot 02 定妆出图验证通过（2.01s，0.00 CU）；
  - 剩余 4 镜（Shot 01、03、04、05）在 G4 单容器中批量完成推理，纯 GPU 耗时仅 **4.58s**，实际扣减 **0.00 CU**，全量资产 1344x768 归档入库。
- **第 1 集成片全流程自动编排落地**：
  - 打造端到端编排脚本 [**scripts/compose_short_drama.py**](./scripts/compose_short_drama.py)；
  - 自动调度 Neural 级多角色对白配音（内侍/刘禅/诸葛亮）、动态运镜（Zoom/Pan/OTS）、高对比度中文字幕卡与雨夜氛围混音；
  - 输出首部完整 32.5 秒成品短剧 [**pipelines/short_drama/chu_shi_chun_qiu_ep01_final.mp4**](./pipelines/short_drama/chu_shi_chun_qiu_ep01_final.mp4) (5.24 MB)、独立字幕 [**chu_shi_chun_qiu_ep01.srt**](./pipelines/short_drama/chu_shi_chun_qiu_ep01.srt) 及无损音频母带 [**chu_shi_chun_qiu_ep01_master.mp3**](./pipelines/short_drama/chu_shi_chun_qiu_ep01_master.mp3)。
- **本地私有无审查大模型节点**：已完成 Ollama + Metal 部署与 32K 上下文扩容，实现按需智能收口与双轨记忆，完整架构详见 [**docs/local_uncensored_llm_node.md**](./docs/local_uncensored_llm_node.md)。
- **Cloudflare 基础设施资产库**：已梳理蒸馏全景域名与凭据规范，归档至 [**references/cloudflare_infra_knowledge.md**](./references/cloudflare_infra_knowledge.md)。
- **算力守门员 Skill**：已安装并固化 `google-ai-ultra` 算力计量与防漏跑规则。

---

## 3. 下一步行动计划

1. **测试发布渠道验证**：将生成的首集成片测试推送至 YouTube 品牌频道（yoursolar 已激活 Premium）或 TikTok，验证平台画质转码与版权机制。
2. **生成式视频动作升级**：探索在 G4 Blackwell 上接驳 Wan2.1 / CogVideoX 扩散模型，为关键帧注入更丰富的肢体与口型微动态。
3. **推进小说广播剧管线 (引擎 3)**：利用 Gemini 对白提取与本地/云端 TTS 模型，生成第一期《楚氏春秋》长篇有声广播剧。
