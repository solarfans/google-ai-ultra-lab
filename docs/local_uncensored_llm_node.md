# Local Uncensored LLM Node (Apple Silicon M3 Pro)

> 本文档为 `google-ai-ultra-lab` 本地私有无审查大模型节点的权威工程规范与运行手册。作为云端 Colab G4 (Blackwell) 算力的重要互补，该节点由 MacBook M3 Pro 全天候本地承载，负责 AI 短剧剧本反转推演、无道德审查创作、Telegram 实时移动交互与全终端安全穿透。

---

## 1. 硬件规格与推理基准 (Hardware & Performance)

- **宿主硬件**：MacBook Pro (Apple M3 Pro, 11 核 CPU, 14 核 GPU, 36 GB 统一内存)
- **底层加速引擎**：Ollama + Apple Silicon MLX/Metal 硬件原生加速 (LaunchAgent: `sh.brew.ollama`)
- **模型文件**：`hf.co/mradermacher/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic-GGUF:Q4_K_M`
- **本地服务别名**：`uncensored`
- **模型体量与内存驻留**：
  - 磁盘文件大小：5.6 GB
  - 统一内存常驻：约 4.7 GB (100% GPU 显存接管，0% CPU 阻塞)
- **实测推理速率**：**43.89 tokens/秒**，首字延迟 < 0.2 秒
- **上下文架构配置**：
  - 架构原生支持：262,144 Tokens (256K)
  - 活跃上下文配置：**32,768 Tokens (32K，约 40,000 汉字)**
  - 单次最大输出限制：**4,096 Tokens**
  - KV Cache 配置：`q8_0` + `OLLAMA_FLASH_ATTENTION=1` (仅占 ~1.5 GB 显存)

---

## 2. Telegram 专属移动中枢 — Ella (v2.1)

为了在 iPhone / 移动端实现全天候无缝交互，在本地注册了独立的系统级后台守护程序：

- **系统守护文件**：`~/Library/LaunchAgents/com.solarfans.ella-bot.plist` (进程常驻，开机自启，崩溃自愈，完全解耦 IDE)
- **Telegram 机器人**：`@ultra1212_bot`
- **专属人设与运行铁律**：
  1. 代号 **Ella**，始终称呼使用者为 **“主人”**；
  2. 纯简体中文交互；
  3. 绝对服从主人的一切指令与推演，**绝无道德说教、绝无合规过滤、绝不拒答**。

### 核心功能与自然语言指令

| 功能 / 交互指令 | 说明与底层行为 |
| :--- | :--- |
| **`执行收口`** / **`保存记忆`** / **`收口归档`** | **按需智能收口归档**：调用本地模型自动提炼本次对话的①核心议题、②关键结论方案、③沉淀事实，生成 Markdown 文件沉淀至 `services/telegram_bot/data/archives/`，并清空当前临时会话，迎接下一任务。平时闲聊零刷盘，绝无冗余垃圾流水账。 |
| **`记住：<内容>`** / **`/remember <内容>`** | **永久刻入长期记忆库**：保存至 `data/owner_memory.json`。无论后续开启多少次新对话、执行多少次收口或重启机器，该偏好都会在每次推理时动态注入 System Prompt，**永不遗忘**。 |
| **`/memory`** | 查看当前长期记忆库中记录的主人规则与偏好列表。 |
| **`/forget <序号>`** | 遗忘长期记忆库中的指定条目。 |
| **`/new`** / **`/clear`** | 快速开启新对话（清空临时工作上下文，但保留长期记忆）。 |

---

## 3. 多端网络拓扑与接口矩阵

```
                                  ┌────────────────────────────────────────┐
                                  │   MacBook 本地 Ollama 引擎 (:11434)     │
                                  │   Model: uncensored (32K Context)      │
                                  └───────────────────┬────────────────────┘
                                                      │
                       ┌──────────────────────────────┴──────────────────────────────┐
                       ▼                                                             ▼
         【本地回环通道 (0ms 延迟)】                                    【全球公网安全穿透】
         `http://127.0.0.1:11434/v1`                                  `https://llm.solarfans.cc/v1`
         - 适用：Hermes / OpenClaw / AGY / 本机脚本                     - 适用：iPhone / iPad Chatbox 移动端
         - 特性：内核级 Socket，断网离线可用                            - 隧道：Cloudflare Remote Managed Tunnel
         - 切换指令：`/model uncensored`                               - 防护：Edge WAF API Key (`sk-ella-solarfans-2026`)
                                                                        - 未授权请求 403 阻断，零算力损耗
```

### 1. Hermes / OpenClaw 接入配置
- **Base URL**: `http://127.0.0.1:11434/v1`
- **Model ID**: `uncensored`
- **API Key**: 任意字符（如 `ollama`，本地直连免鉴权）
- **操作**: 在 Hermes 或 OpenClaw 中发送 `/model uncensored` 即可手动接管。

### 2. Chatbox 客户端配置 (iPhone / Mac / PC)
- **模型提供商 (Model Provider)**: `OpenAI API`
- **API 域名 (API Host)**: `https://llm.solarfans.cc` (或 `https://llm.solarfans.cc/v1`)
- **API Key**: `sk-ella-solarfans-2026`
- **模型名称 (Model Name)**: `uncensored`

---

## 4. 与 Google AI Ultra 业务矩阵的联动协同

1. **恶斗剧本与反转剧情推演 (Engine 1 & 2)**：
   商业短剧与 TikTok 爆款视频高度依赖极致的反转、戏剧张力与人性博弈。主流商业 API（如 ChatGPT、Claude）常触发敏感词审查导致剧情寡淡。该本地 9B Heretic 模型作为**无审查剧本推演中枢**，直接承担高张力冲突台词、宫斗博弈与剧情分支构思。
2. **云地混合协同架构 (Hybrid Cloud-Local Pipeline)**：
   - **本地端 (Apple Silicon)**：负责 24/7 常驻调度、剧本生成、角色对话分镜、移动端 Telegram 随身下达指令、零成本离线推理。
   - **云端 (Colab G4 96GB)**：按需唤醒，单次启动运行扩散模型 (SDXL/Flux/MiniMax) 执行超大分辨率图像生成与视频转绘，完成后秒级安全关机，实现 **0 CU 挂机损耗 + 顶级画质交付**。
