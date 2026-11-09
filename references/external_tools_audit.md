# 外部开源工具、工作流与模型全景审计归档 (External Tools & Models Audit)

> **最后更新**：2026-11-09 SGT  
> **审计执行席位**：Antigravity Desktop (MacBook)  
> **信息源范围**：Owner 过去 7 日 X (Twitter) 点赞推文（50+ 条 / 11 篇万字长文全量展开）+ X 定向高赞搜索 + GitHub 源码核验。  
> **关联操作总纲**：[**docs/AI_MANJU_AND_ULTRA_SOP.md**](../docs/AI_MANJU_AND_ULTRA_SOP.md)

---

## 一、 Colab G4 算力调度与 AI 漫剧/短剧核心工作流

### 1. `yuanyang749/colab-ultra-workstation`（Colab G4 96GB × MiniMax-H3 工业级无头工作站）
* **信息来源**：码农暖爸 `@Delroy715` 两篇万字长文 [`2111091086349533244`](https://x.com/Delroy715/status/2111091086349533244) & [`2116130442651005028`](https://x.com/Delroy715/status/2116130442651005028)
* **开源仓库**：`https://github.com/yuanyang749/colab-ultra-workstation`
* **核心价值评级**：⭐⭐⭐⭐⭐ **（主力基建底座，直接采用）**
* **关键技术精髓**：
  1. **`colab-cli + colab-dfs-ext` 零浏览器无头架构**：摆脱网页版 `colab-mcp` 必须人工弹窗点 Allow 和切卡的痛点，终端直接拉起 G4 96GB 并静默挂载 30TB Drive（首次 `colab dfs consent` 必须手动勾选 Google Drive 复选框）。
  2. **75 秒双通道 NVMe 预热 (`launch_g4_comfyui_fast.py v2.2`)**：绕开 Google Drive FUSE 软链随机读 `25 MB/s`（卡死 28 分钟）的算力黑洞，通过 Drive v3 API + HF CDN 双通道（`463 MB/s`）在 75.4 秒内将 `42.33GB` 核心权重拉入 G4 本地 NVMe SSD (`/content/fast_models`)，并将 13 套插件打包为 `custom_nodes_bundle.tar.gz`（解压仅 1.5 秒），冷启动全流程 90 秒，96GB 显存常驻后第 2 次起 0 秒加载。
  3. **攻克 MiniMax-H3 六大深坑**：
     * **原生自锚定声纹 (`Self-Anchor Voice`) + 单说话人门控 + `T8mars` 瞬态破锁协议**：彻底解决跨镜头变声与外部 TTS 机械播音腔；
     * **`MiniMaxH3JoinMatch` 手动除雾**：`tuning="manual", strength=0.35, min_excess=2.5, match_spread=False, match_detail=False`，根治多段续接后段画面发灰起雾；
     * **`H3SaveAVLatent` (`4.8MB`) + `--only-seg N` 单段 3 分钟手术刀重修**：改单镜立省 75% CU；
     * **`auto_subtitle_video.py`**：本地 0 CU 基于 `130Hz~3600Hz` 人声能量包络以 10ms 精度自动对齐字幕 + 首段呼吸滑入人物铭牌。
  4. **漫剧适配要点**：跑 3D 国漫 / 2.5D 漫剧时，必须将工作流中的两枚真人毛孔去油 LoRA（`minimax-h3-realism-people` 与 `Facial-Realism-CloseUp`）权重设为 `0.0` 或旁路关闭。

---

### 2. `@aggs8p` (jonny) —— 《零/低成本 AI 漫剧制作保姆全流程（手动 + Codex/Agent 自动化）》
* **信息来源**：jonny `@aggs8p` [`2119348643463655427`](https://x.com/aggs8p/status/2119348643463655427)
* **核心价值评级**：⭐⭐⭐⭐⭐ **（AI 漫剧资产与提示词标准 SOP，直接采用）**
* **关键技术精髓**：
  1. **三类母本资产前置固定**：开拍前单独制作【人物四联设定图（左侧 2:3 正面大特写 + 右侧三格正面/侧面/背面全身）】、【无人物纯净场景图】、【白底三视图道具图】。
  2. **九宫格/六宫格分镜拆图法**：结合资产图一次性生成 3×3 或 3×2 宫格分镜图以锁死整场戏画风色调，再通过 `split_grid.py` 拆分为独立镜头首帧 `镜头001.png ~ 镜头009.png`。
  3. **H3 漫剧防乱说话与防漂移规范 (`minimax_h3.md`)**：
     * 画面描述、运镜、动作全部用**英文**，人物实际对白用**中文 `<d>[中文] 原文</d>`**；
     * **情绪靠动作带**：严禁写“他很悲伤/愤怒”等形容词，必须改写为视线、呼吸、下颌、手部动作与声线描述；
     * **中文白名单防漂移**：在场景 Subject 定义末尾附加上 `"桌上/环境物品以上述为准，全程不得添加、移动或碰触其他物件"`。

---

### 3. `@TuyetloanP81840` (Miller) —— 《用 Claude + H3 一个人拍 AI 短剧/漫剧实战教程》
* **信息来源**：Miller `@TuyetloanP81840` [`2119326884505043274`](https://x.com/TuyetloanP81840/status/2119326884505043274)（附 `miliagent.com/light` 光影速查与技能包）
* **核心价值评级**：⭐⭐⭐⭐⭐ **（单镜 MVP 验证法与导演剪辑节奏指南，直接采用）**
* **关键技术精髓**：
  1. **一小时 10 秒新手/MVP 铁律**：第一次跑新剧绝不一上来做 5 分钟，先用「1 个角色 + 1 个场景 + 1 句台词」跑通 5~10 秒单镜头闭环。
  2. **16:9 角色身份板（Character Identity Sheet）五规矩**：全身正面、白底、双手自然垂下不拿东西、**必须写鞋子**（不写必出半身）、**严禁用真人/明星照片当参考**。
  3. **对话戏正反打空镜法**：场景图绝不画人，对话戏固定出「正打 + 反打（左右前后互换）+ 站位大全景」三张，每段视频只喂 1 张对应场景图。
  4. **声音三分法与反应镜头盖切（J-Cut / L-Cut）**：
     * 台词严格区分「当面说 / 内心独白 / 画外音」，防止角色张嘴念心里话；
     * 顺手多跑几段 3~5 秒不说话的“听众反应镜头”，后期保留说话人声音不断，画面切 1~2 秒听众反应，彻底解决长台词画面发死。

---

### 4. `@EianLu` (Eian) —— 《Claude Code / Codex + 视频大模型：从想法到成片四线程工作流》
* **信息来源**：Eian `@EianLu` [`2118317430665613741`](https://x.com/EianLu/status/2118317430665613741)
* **核心价值评级**：⭐⭐⭐⭐☆ **（提交前冷读审核门禁与避坑清单，吸收采用）**
* **关键技术精髓**：
  1. **错误前置拦截原则**：“能在文字里发现的错，不留到图上；能在图上发现的错，不留到视频上。”
  2. **独立冷读审核 Subagent**：在提交视频渲染前，開啟一个零上下文先入为主的审核视角，放大检查首帧与提示词（左右方向、人数、道具数量、手部、机位是否 100% 匹配）。
  3. **构图与运动铁律**：全片平视正面最多 2 次，其余用俯拍、仰拍、过肩、透过前景遮挡拍；人物眼睛落在画面横向 38% 或 62% 黄金分割位；每镜必须明确写出“到底是什么在动”。

---

### 5. `designfuchen/worldforge`（WorldForge 世界工坊 —— Mac 原生 SSH 连接 Colab 工作台）
* **信息来源**：阿磊 `@yangleiocx3` [`2119328145975255371`](https://x.com/yangleiocx3/status/2119328145975255371) & [`2118950523445354988`](https://x.com/yangleiocx3/status/2118950523445354988)
* **开源仓库**：`https://github.com/designfuchen/worldforge`
* **核心价值评级**：⭐⭐⭐ **（提取光学预设与内存分层技巧，不用其单图 GUI 跑多镜漫剧）**
* **审计结论**：
  * **吸收亮点**：
    1. **6 套专业电影摄影机光学预设**（岩井俊二黄金逆光柔焦 `ARRI Alexa 65 + Canon FD 85mm f/1.2L`、王家卫暗夜霓虹变形宽银幕 `ARRI Alexa Mini LF + Cooke Anamorphic 40mm`、新海诚暮光云海星芒镜头 `Panavision DXL2 8K + Ultra Panatar 1.3x` 等），直接纳入本实验室首帧生图提示词库；
    2. **四层硬件利用法**：30TB 云盘做永久金库 + `177GB DDR5 系统内存` 跑 CPU 配音（0 显存占用）+ `/dev/shm`（88GB 内存盘）做高速合成 IO + `96GB 显存` 100% 留给生图/视频主模型。
  * **局限性**：其三栏 GUI 缺少 ComfyUI `Ref2VA` 多参考图槽位、潜空间 22 帧续接与单段断点重修能力，无法支撑多镜头连续漫剧的角色锁定。

---

## 二、 爆款逆向、剧本去 AI 味与跨端辅助工具

### 6. `Antigravity 视频逆向` + `rea-video`（爆款视频逐秒运镜与提示词反推）
* **信息来源**：Leaf Yeah! `@leaf_sanren` [`2118661246434353299`](https://x.com/leaf_sanren/status/2118661246434353299) & 周览资源 `@grgerwcwetwet` [`2118308946259874095`](https://x.com/grgerwcwetwet/status/2118308946259874095)
* **核心价值评级**：⭐⭐⭐⭐⭐ **（漫剧分镜外挂捷径，直接采用）**
* **实战用法**：
  * GPT/Claude 看视频只能抽静态截图，看不懂运镜；而 **AGY 底层的 Gemini 具备原生连续视频时空理解能力**；
  * 刷到红果/抖音高赞爆款漫剧（或二次元高燃打斗如 Koda 武士对决）➡️ 用 `omni-content-pipeline` 下载原片 ➡️ 由 AGY Gemini 逐秒逆向出「时间轴 + 景别机位 + 动作方向 + 碰撞接触 + 拟声音效」提示词 ➡️ 垫入我们自己的漫剧角色设定图，即可 1:1 复刻爆款镜头语言！

---

### 7. `Minireel/HGhub`（红果免费短剧跨平台免广告开源客户端）
* **信息来源**：`@BlackMelooo` [`2118617027732808184`](https://x.com/BlackMelooo/status/2118617027732808184)、`@grgerwcwetwet` [`2119035519611089371`](https://x.com/grgerwcwetwet/status/2119035519611089371)、`@NFT_Chen` [`2119494877230866619`](https://x.com/NFT_Chen/status/2119494877230866619)
* **开源仓库**：`https://github.com/Minireel/HGhub` (Rust + Tauri 2, 支持 macOS / Windows / Android)
* **核心价值评级**：⭐⭐⭐⭐ **（红果漫剧选品与参考样片库）**
* **实战用法**：在 Mac 上直接免广告浏览红果短剧/漫剧热播榜，筛选高赞 3D 国漫与动态漫爆款，提取前 3 秒黄金钩子与人物建模画风参考。

---

### 8. `去 AI 味 Skill` (`@lieflat_3`) + `Heretic Uncensored` 无审查大模型家族
* **信息来源**：
  * `@lieflat_3` [`2118355780474937831`](https://x.com/lieflat_3/status/2118355780474937831)（520万字样本提炼去 AI 味 Skill）& `@Lonely__MH` [`2118319043388309704`](https://x.com/Lonely__MH/status/2118319043388309704)
  * `@mingzi206` [`2118655841024753692`](https://x.com/mingzi206/status/2118655841024753692)：`DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic` (5.6GB，已部署于 MacBook 本地 43.9 tok/s)
  * `@muihbb` [`2118681685189603540`](https://x.com/muihbb/status/2118681685189603540) & [`2119248663432319140`](https://x.com/muihbb/status/2119248663432319140)：Colab G4 部署破甲 `Qwen 27B` (70 tok/s) / `Qwen3.8-Flash-Next 177B` (88GB, 120 tok/s)
* **核心价值评级**：⭐⭐⭐⭐⭐ **（剧本台词去公文腔与高冲突反派台词生成，已就绪）**

---

### 9. `sarpstar/cinecode`（纯代码驱动零抽卡视频生成 Skill）
* **信息来源**：`@Yooeec3` [`2119112059770286376`](https://x.com/Yooeec3/status/2119112059770286376) & `@sarpstar` [`2119082994925211686`](https://x.com/sarpstar/status/2119082994925211686)
* **核心价值评级**：⭐⭐⭐⭐ **（适合历史战略沙盘推演、数据可视化、科普纪录片动效，0 抽卡成本）**
* **实战用法**：在历史权谋漫剧（如《楚氏春秋》《持械入宋》）需要插入“九州兵力行军路线图、城防沙盘推演、朝堂势力关系图”时，直接用 `cinecode` 渲染丝滑高帧率代码动效，比用扩散模型盲抽地图强百倍。
