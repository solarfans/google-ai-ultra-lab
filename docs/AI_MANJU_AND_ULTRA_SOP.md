# Google AI Ultra × AI 漫剧工业化生产总纲与操作守则 (Master SOP & Playbook)

> **版本**：v2.0.0 (2026-11-09 SGT)  
> **适用范围**：`solarfans/google-ai-ultra-lab` 及全局 `google-ai-ultra` Skill  
> **信息源基座**：Owner 过去 7 日 X (Twitter) 点赞精选（50+ 篇推文 / 11 篇万字长文全量展开）、X 定向高赞检索、红果免费短剧 2025–2026 行业大盘数据、以及 [LESSONS_LEARNED.md](../LESSONS_LEARNED.md) 惨败复盘。  
> **核心使命**：将 Google AI Ultra（30TB 云盘 + 2,500 Colab CU + 25,000 Google Flow 积分 + AGY Gemini 4）转化为**零算力泄漏、零欺骗性半成品、高一致性的 AI 漫剧工业化生产工作站**。

---

## 一、 战略方向锁定：为什么放弃“真人短剧”，全面聚焦【3D 国漫 CG 风 AI 漫剧】？

### 1.1 历史惨败根因与物理边界
在 2026-11-08 的测试中，试图用家庭真人生活照制作古装短剧遭遇彻底失败（详见 [LESSONS_LEARNED.md](../LESSONS_LEARNED.md)）。结合一线创作者（如 Miller `@TuyetloanP81840`）的实战铁律与底层视觉扩散原理，核心原因在于：
1. **真人恐怖谷效应（Uncanny Valley）**：人类视觉对熟人/真人面孔的识别精度达亚毫米级。生活照平光与影视侧逆光不兼容，任何 2D 换脸或扩散重绘哪怕出现 1% 的五官/肤色偏移，都会立即呈现“丧尸感”或“塑料假人感”。
2. **真人跨镜头锁脸极难**：真人缺乏夸张的色彩与造型符号，跨镜头极易变成另一个人。
3. **合规与平台风控**：各主流短剧平台严厉拦截未经授权的真人/明星面部参考。

### 1.2 红果短剧外部数据与【画风唯一最优解】
根据 2025–2026 红果免费短剧（日活 1.68 亿，人均单日使用 151 分钟）与 DataEye 行业监测数据：
* **完播率优势**：红果将漫剧与真人剧合榜后，**AI 漫剧平均完播率、分享率比同类真人短剧高出约 30%**（代表作《持械入宋》全网播放破 66～120 亿、收藏 1,141 万；《万妖图录传》多季连载破十亿级）。
* **画风冷热分化（关键避坑）**：早期纯 2D 简笔画、沙雕表情包漫在红果大盘占比已萎缩至 **<1%**。
* **本实验室默认锁定最高成功率画风 —— 【3D 国漫 / UE5 影视 CG 风】**（对标《凡人修仙传》《画江湖之不良人》《吞噬星空》）：
  1. **规避恐怖谷**：明确的高精 3D 建模国漫俊美五官，观众对口型微瑕与夸张表演容忍度高出真人 10 倍；
  2. **造型锚点极稳**：高马尾、玄铁重铠、暗金龙纹、眉心印记等强视觉符号，在 `Qwen-Image-2.1` 与 `MiniMax-H3 (Ref2VA)` 中跨镜头一致性可达 **95%+**；
  3. **特效浑然一体**：刀光剑影、风雪漫天、战火硝烟在 3D CG 画风下天然融合，绝无真人剧的“五毛塑料感”；
  4. **备选画风**：若涉及现代悬疑/规则怪谈/女频情感，切换为 **【高精 2.5D 国风厚涂 + 新海诚电影光影漫】**。

---

## 二、 五条死刑红线与双线程审核门禁 (Zero-Tolerance Guardrails)

任何 AGY 会话在执行漫剧生产任务时，**一旦触犯以下任意一条红线，视为严重工程违纪**：

1. 🚫 **严禁静态图晃动冒充视频**：绝对禁止使用 `ffmpeg` 的 `scale+crop+sin(t)`（Ken Burns 平移缩放）将静态图片包装成“动态视频”交付。所有镜头必须由 `MiniMax-H3` 或 `Google Flow` 原生生成像素级人物动作与口型。
2. 🚫 **严禁传统几何贴图换脸**：绝对禁止使用 OpenCV (`seamlessClone`, `grabCut`, `warpAffine`) 进行抠图拼贴，禁止使用真人家庭照片作为漫剧输入。
3. 🚫 **严禁模型倒退**：禁止在 96GB Blackwell G4 上退回使用 `SDXL 1.0`、`SVD-XT`、`SadTalker` 等 2022–2023 年过时模型。
4. 🚫 **严禁将算法调试残次品直抛给用户**：任何首帧图或视频片段生成后，必须先经过 **Agent 本地抽帧自检**（检查是否张嘴、有无画面烧录乱码字幕、有无黑线撕裂、有无多手多脚），确认 100% 合格后方可交付 Owner 审阅。
5. 🚫 **严禁一次性盲目批跑整集**：初次测试新角色或新工作流时，必须严格执行 **「10 秒单镜头 MVP 门禁」**（1 个角色 + 1 个场景 + 1 句台词），单镜经 Owner 验收通过后，方可串行扩展至整集。

---

## 三、 Google AI Ultra 全权益最大化架构与 Colab G4 极速基建

基于 `@Delroy715`（码农暖爸 `yuanyang749/colab-ultra-workstation`）、`@yangleiocx3`（阿磊 `designfuchen/worldforge`）与 `@ox40404` 实战验证：

### 3.1 四大算力层分工矩阵
| 资源层级 | 规格与额度 | 专属职责与最佳实践 |
| :--- | :--- | :--- |
| **本地 MacBook M3 Pro** | 0 CU · 24/7 常驻 | 剧本打磨、分镜拆解、`omni-content-pipeline` + Gemini 逆向爆款视频、冷读审核、`auto_subtitle.py` 声学包络对齐字幕（3秒/0 CU）、多轨混音压制。 |
| **Colab CPU 实例** | 0.00 CU/h · 免费 | 首次从 HuggingFace 拉取几十 GB 模型权重并持久化至 30TB Google Drive（`/content/drive/MyDrive/AI_Workstation/`）。**铁律：严禁开着 G4 首次慢速下模型！** |
| **Colab G4 GPU 实例** | 96GB Blackwell · ~8.71–10.05 CU/h | **主力对白与角色表演渲染引擎**。运行 ComfyUI + `Qwen-Image-2.1` (32GB) + `MiniMax-H3 Singularity v1.3` (42.3GB)。**注意：选 G4 时保持「高 RAM」关闭**，默认已给满 `95.6GB 显存 + 176.9GB 内存 + 235GB 本地 NVMe SSD`！ |
| **Google Flow (Veo/Omni)** | 25,000 积分/月（Ultra 附赠） | **0 Colab CU 宏大空镜与特效引擎**。720p/15s 视频仅耗 60 积分（每月可出 ~400 条）。专职生成“暴风雪空难、十万铁骑冲锋、城池远景、山河空镜”等无需精细中文口型的大场面镜头，与 G4 人物镜头剪辑合流。 |

### 3.2 零浏览器无头连接 (`colab-cli + colab-dfs-ext`)
抛弃易断连的网页版 `colab-mcp`，统一采用终端无头架构：
```bash
# 1. 安装官方 CLI（注入 socksio 防代理崩溃）
uv tool install --with socksio google-colab-cli

# 2. 注入零浏览器 Google Drive 静默挂载扩展
curl -fsSL https://raw.githubusercontent.com/deluxebear/colab-dfs-ext/main/install.sh | sh

# 3. 首次 OAuth 授权（⚠️ 必看避坑：网页弹窗中「查看、编辑、创建和删除您的所有 Google 云端硬盘文件」右侧复选框默认未勾选，必须手动勾上再点继续，否则报 403 SCOPE_INSUFFICIENT）
colab dfs consent
```

### 3.3 破解 Google Drive FUSE 28 分钟假死黑洞（90 秒极速冷启动法）
* **深坑原因**：若直接用 `ln -s` 软链读取 `/content/drive` 中的 `42.33GB` H3 权重，PyTorch 的 `mmap` 4KB 随机分片读会把 FUSE 打进 `25 MB/s` 假死状态（耗时 28 分钟，白烧 3~4 CU）；且跨 FUSE 遍历 `custom_nodes` 3,000+ 小文件会卡顿 60 秒。
* **标准解法（`launch_g4_comfyui_fast.py` 架构）**：
  1. **双通道并发预热至本地 NVMe SSD (`/content/fast_models`)**：利用 G4 自带的 `235GB` 本地高速 NVMe SSD，通过 Google Drive v3 API（64 并发流拉中小模型，~150 MB/s）+ HF CDN 多线程分片（拉主干大权重，~400 MB/s），实测 `463 MB/s` 均速，**75.4 秒内将 42.3GB 权重落盘本地 NVMe**。
  2. **插件单包秒级解压**：将 13 套 ComfyUI 插件预打包为 `custom_nodes_bundle.tar.gz`，开机拷入本地 NVMe 解压仅需 **1.5 秒**。
  3. **显存常驻焊死 + 内存盘加速**：以 `--highvram --disable-mmap --fast` 启动 ComfyUI，16 秒内（2.5 GB/s）将模型全量灌入 96GB 显存并永久常驻（第 2 镜起 **0 秒加载**）；利用 `177GB 系统内存` 承载 CPU 配音模型，利用 `/dev/shm`（88GB 内存盘）处理临时帧读写。
  4. **强制双轨查账与强杀守门员（`colab_meter.py` / `ultra_meter.py`）**：开机打点记录余额，任务结束或异常退出在 `finally` 块中强制销毁实例，二次核验 `Active assignments: 0` 与 `0.00 CU/h`。

---

## 四、 AI 漫剧标准化生产六步流水线 (Six-Step Production Pipeline)

融合 `@aggs8p`（jonny 漫剧保姆全流程）、`@TuyetloanP81840`（Miller 独人剧组 SOP）与 `@EianLu`（导演审核制）最佳实践：

### 第一步：剧本视觉化改编与去 AI 味（0 CU 本地）
* **只写镜头拍得到的东西**：AI 视频模型看不懂“他心里很难过/很愤怒”，必须全部翻译为**具体外显动作与生理信号**（如“眼眶泛红、下颌绷紧、五指猛地攥紧剑柄指节发白”）。
* **声音三分法标记**：在剧本阶段严格区分：
  1. 当面开口：`角色名：（动作/语气）台词`
  2. 心理活动：`角色名（内心独白）：台词`（画面中人物闭嘴只做眼神微表情，杜绝张嘴念心声）
  3. 画外音：`角色名（画外音）：台词`
* **节奏与字数控制**：开头 3 秒必出核心冲突，结尾停在悬念；按每 10 个汉字约 2 秒计算，5 秒镜头最多安排 1～1.5 句台词（15～25 字），严禁塞长句导致口型崩坏。
* **去 AI 味过滤**：结合 `@lieflat_3` 去 AI 味规范与本地 `9B Heretic Uncensored` 模型，剔除公文腔、排比句与道德说教，强化权谋交锋或爽剧短促张力。

### 第二步：三类核心母本资产预制（0 CU / 极速生图）
**铁律：先选角定场，再开拍！绝不在生成视频时临时凑图。**
1. **主角四联设定板（Character Identity Sheet）**：
   * 使用 `Qwen-Image-2.1` 或 GPT Image 生成 16:9 纯白/中性灰底设定板：左侧为 2:3 正面半身面部特写，右侧并排全身正面、侧面、背面 A-Pose + 3 个表情特写。
   * **必写细节**：必须明确写出**鞋子样式**（否则 AI 极易只画半身），锁死发色、发型、标志性服饰纹理（如“银冠束发、玄色暗金龙纹窄袖锦袍、黑色云纹战靴”）。
2. **纯净空镜场景图（Empty Scene Plates）**：
   * **画面里绝对不能有人！**
   * 对话场景一次性生成 3 张同画风空镜：**正打**（拍角色 A 方向）、**反打**（拍角色 B 方向，左右陈设互换）、**站位大全景**。
3. **白底关键道具图（Props）**：
   * 纯白底无人物，**必须标注真实物理尺寸**（如“青铜虎符长约 12 厘米，单手可握”），防止视频中道具忽大忽小。

### 第三步：分镜拆解与高清首帧生成（First-Frame Anchoring）
* **切镜黄金法则**：
  1. 换人说话就切（说话人 → 听众反应 1~2 秒 → 说话人）；
  2. 情绪每变一次切一镜；
  3. 复杂大动作拆成「准备 → 执行 → 结果」三镜，单镜只干一件事；
  4. 连续 3 个镜头严禁使用同一种景别（远/中/近/特写交替），平视正面全片不超过 2 次，多用仰拍、俯拍、过肩（OTS）机位。
* **首帧生成两法**：
  * **方法 A（`Qwen-Image-2.1` 参考图垫图法）**：将【角色身份板】+【对应场景空镜】作为参考图喂给 `Qwen-Image-2.1`，叠加光学镜头预设（如 `3D Chinese animation CG style, Unreal Engine 5 render, ARRI Alexa Mini LF, 50mm lens, dramatic volumetric rim lighting`），生成 `1344×768`（横屏）或 `768×1344`（竖屏 9:16）的镜头首帧。
  * **方法 B（九宫格/六宫格同源拆图法，`@aggs8p` 推荐）**：一次性生成 3×3 九宫格或 3×2 六宫格连续分镜图，确保整场戏色调光影 100% 同源，再用脚本自动裁切为独立首帧 `shot_001.png ~ shot_006.png`。
* **提交前冷读审核（`@EianLu` 审核门禁）**：逐张检查首帧——后续动作要用到的道具（如酒杯、佩剑）是否已在首帧中画出？人物左右站位是否与分镜表一致？有无多指或畸变？

### 第四步：编写 MiniMax-H3 工业级结构化提示词
MiniMax-H3 极度依赖提示词结构，统一采用 **「英文写镜头/动作/环境 + 中文 `<d>` 标签写台词 + 中文白名单防漂移」** 的六段式规范：

1. **`subject_definitions`（主体与参考图绑定）**：
   * `<Picture 1>`：当前镜头首帧图（控制开场构图、人物位置与光影状态）；
   * `<Picture 2>`：主角 A 角色设定板（`<Subject 1>`）；
   * `<Picture 3>`：主角 B 角色设定板（`<Subject 2>`）或场景参考图；
   * **附中文白名单防漂移**：`"场景与案几物品以上述参考图为准，全程不得添加、移动或凭空产生其他物件。"`
2. **`summary`（镜头概述）**：仅用英文简述景别与画面核心动作，**严禁在此处重复台词**（否则会导致角色抢话或念两遍）。
3. **`retention_analysis`（一致性锁定）**：声明完全保留 3D 国漫 CG 画风、面部特征、服装纹理与主光源方向。
4. **`detailed_description`（逐秒动作与内嵌台词）**：
   * **单镜单运镜原则**：5 秒内只写 **1 个贯穿首尾的运镜指令**（如 `Camera slowly tracks in from medium shot to tight close-up and holds steady`），严禁写两个时间段的不同运镜，防止 Qwen3-VL 编码器误触发段内闪切！
   * **空间轴线锁死**：开篇显式声明 `<Subject 1> on screen-left facing right, <Subject 2> on screen-right facing left`。
   * **中近景防削头顶**：中近景严禁写 `rises/stands up from chair`，一律改写为 `leans sharply forward across the table`（大幅前倾撑桌）。
   * **台词与闭嘴锚点标准写法**：
     ```text
     At 00:00.500, <Subject 1> (S1, <Audio 1>) narrows his eyes, leans forward slightly, and speaks in a cold, commanding voice: <d>[Mandarin] 从今日起，这平原城的十万铁骑，由本世子接管！</d> He closes his mouth firmly after speaking. From 00:04.500 to 00:05.875, he holds a tense, silent glare with his mouth completely closed.
     ```
5. **`overall_soundscape`（物理拟声音效）**：
   * 只写画面看得见原因的真实动作拟音（如 `Heavy rain pattering outside the window, a sharp metallic sword unsheathing clang at 00:00.400, followed by S1's resonant voice`）。
   * 若需后段情绪咆哮爆发，利用 **T8mars 双重声学破锁协议**：在 `00:00.400` 注入拍桌/拔剑等高能量瞬态音效，直接拉高音频潜空间声强包络（`+7 ~ +10 dB`）。
6. **`non_diegetic_music` & 【强制负向门禁】**：
   * 配乐固定写：`None. Leave background music for post-production.`（严禁模型自带混乱 BGM）。
   * 末尾强制追加：`No subtitles, no text, no watermark, no English letters, no blurry face, no extra limbs, no camera cut. 不要出现任何字幕、文字或水印。`

### 第五步：Colab G4 + ComfyUI 渲染与六大深坑调优参数
在 Colab G4 上调用 `MiniMax-H3 (Singularity v1.3 + Qwen3-VL-32B-Heretic NVFP4)` 时，严格固化以下工业级参数：

1. **漫剧画风去写实 LoRA**：
   * 跑 3D 国漫 / 2.5D 漫剧时，**必须旁路（Bypass）或将 `minimax-h3-realism-people` 与 `facial-realism-closeup` 两个真人毛孔 LoRA 权重设为 `0.0`**，防止动漫建模脸被强行染上真人法令纹与糙皮！
2. **黄金帧数定律（$F(k) = 17k + 5$）**：
   * 快切/反应镜头：`length = 90` (3.75s)；
   * 标准单句台词主力档：`length = 124` (5.17s) 或 `141` (5.88s)；
   * 双句长对白/走位档：`length = 192` (8.00s)。
3. **跨镜头音色 100% 锁死（`Self-Anchor Voice` + 单说话人门控）**：
   * **第 1 镜生成后**：用 `ffmpeg` 将主角最满意的原生干声剥离并转为 `32kHz` 双声道立体声母本（`aresample=32000,pan=stereo|c0=c0|c1=c0`）；
   * **后续所有镜头**：将该 `.wav` 传入 `<Audio 1>` 作为声纹锚点；
   * **单说话人门控（Speech-Active Gating）**：哪一段是谁开口说话，就**只挂载那 1 个人的 `<Audio 1>`**，绝不同时挂男女双声纹，彻底杜绝串音与抢话。
4. **多段无缝续接与手动除雾（`MiniMaxH3JoinMatch`）**：
   * 续接段采用 `MiniMaxH3MotionContext (context_frames = 22)`；
   * `MiniMaxH3JoinMatch` **严禁使用默认 `auto`**（会压缩 31.8% 对比度导致画面起雾发灰），强制设为：
     `tuning = "manual"`, `strength = 0.35`, `min_excess = 2.5`, `match_spread = False`, `match_detail = False`。
5. **防侧脸转头看镜头（`V9_TailLock`）**：
   * 侧脸对峙镜头严禁出现复数五官词（`eyes`, `brows`）与否定句（`without turning toward camera`）；必要时在尾部串联 `MiniMaxH3AddGuide` 锚定静态侧脸帧。
6. **5MB 潜变量断点存档与单段热插拔（`--only-seg`）**：
   * 每段跑完自动通过 `H3SaveAVLatent` 保存 `~4.8MB` 的 `.pt` 原生潜变量至云盘；若第 3 镜有瑕疵，仅执行 `--only-seg 3` 单独重修（耗时 3 分钟 / `0.48 CU`），无需重跑全片。

### 第六步：本地 0 CU 后期精修、反应镜头盖切与字幕压制
1. **反应镜头盖切法（J-Cut / L-Cut）**：
   * 对白较长时，顺手生成 2~3 段 3 秒的“听众反应镜头”（不说话，仅眼神震惊/冷笑/握拳），在后期合成时保留说话人音频不断，画面切入 1.5 秒听众反应，彻底消除站桩对话感。
2. **声学包络自动对齐字幕（`auto_subtitle_video.py`）**：
   * 在本地 Mac（0 CU）滤除拍桌/拔剑等瞬态脉冲，提取 `130Hz ~ 3600Hz` 人声包络，以 10ms 精度自动对齐中文字幕，并在首段嵌入呼吸滑入式角色铭牌（Lower-Third Callout）。
3. **三层音轨混音与响度统一**：
   * 音量层级：**角色对白（主轨最大，-14 LUFS 响度统一） > 物理动作环境音效（SFX） > 情绪背景配乐（BGM，有人说话时自动 Ducking 压低 -8dB）**。
   * 画面统一挂载 LUT 滤镜调平色温，并使用 Lanczos / Real-ESRGAN 超分至 1080P/2K 交付。

---

## 五、 全景开源工具与模型选型矩阵 (Curated Ecosystem Matrix)

基于过去 7 日 X 点赞与全网检索验证，按实战价值分级归档：

### 5.1 核心生产底座（已纳入主干管线）
| 名称 | 类型 / 开源地址 | 核心用途与配置要点 | 推荐等级 |
| :--- | :--- | :--- | :--- |
| **`colab-ultra-workstation`** | GitHub: `yuanyang749/colab-ultra-workstation` | Colab G4 96GB 工业级 ComfyUI 无头工作站。含 `launch_g4_comfyui_fast.py` (75s NVMe 预热)、`colab_meter.py` (双轨查账强杀)、`workflow_v9_final.json` (H3 多段续接) 与 `auto_subtitle.py`。 | ⭐⭐⭐⭐⭐ |
| **`google-colab-cli` + `colab-dfs-ext`** | GitHub: `googlecolab/google-colab-cli` + `deluxebear/colab-dfs-ext` | 零浏览器终端拉起 G4 实例、静默挂载 30TB Google Drive、后台执行渲染脚本。 | ⭐⭐⭐⭐⭐ |
| **`MiniMax-H3` (`Singularity v1.3`)** | HF: `WarmBloodAban/Minimax-h3_Singularity` + `Comfy-Org/MiniMax-H3` | 33B 原生音视频联合大模型（42.3GB）。音画口型同生，配合 `Qwen3-VL-32B-Heretic NVFP4` 编码器在 G4 上满血常驻。 | ⭐⭐⭐⭐⭐ |
| **`Qwen-Image-2.1`** | HF: `Comfy-Org/Qwen-Image-2.1` (32GB) | 漫剧角色四联身份板生成、场景空镜生成、以及基于 I2I 参考图垫图的跨镜头首帧锁脸。 | ⭐⭐⭐⭐⭐ |
| **Google Flow (Veo / Omni 1.2)** | Google AI Ultra 内置权益 (25,000 积分/月) | 0 Colab CU 辅助视频通道，专门生成宏大战争、自然灾难、城市空镜与特效转场。 | ⭐⭐⭐⭐⭐ |

### 5.2 爆款逆向、剧本去 AI 味与辅助工具库（按需调用）
| 名称 | 类型 / 开源地址 | 核心用途与借鉴价值 | 推荐等级 |
| :--- | :--- | :--- | :--- |
| **Antigravity 视频逆向 + `rea-video`** | Gemini 原生多模态 + GitHub: `rea-video` (`@leaf_sanren` / `@grgerwcwetwet`) | 输入红果/抖音爆款漫剧视频，直接由 Gemini 逐秒逆向出机位、运镜、动作方向与分镜提示词（配合设定图垫图 1:1 复刻高燃镜头）。 | ⭐⭐⭐⭐⭐ |
| **`Minireel/HGhub`** | GitHub: `Minireel/HGhub` (Rust + Tauri 2) | 红果免费短剧跨平台免广告桌面客户端（支持 macOS）。用于检索红果热播漫剧榜、拆解黄金 3 秒钩子与人物造型参考。 | ⭐⭐⭐⭐ |
| **`去 AI 味 Skill` + `9B/27B Heretic Uncensored`** | `@lieflat_3` 规范 + HF: `DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic` | 本地 M3 Pro (43.9 tok/s) 零成本常驻。消除剧本 AI 味，生成权谋死斗、反派狠话等不被商业道德锁拒答的高冲突台词。 | ⭐⭐⭐⭐⭐ |
| **`WorldForge` (世界工坊)** | GitHub: `designfuchen/worldforge` (`@yangleiocx3`) | 借鉴其 **6 套电影摄影机光学预设**（ARRI Alexa / 新海诚暮光云海镜头等）与 **177GB 内存跑 CPU TTS + `/dev/shm` 内存盘加速**；不直接用其单图 GUI 跑多镜漫剧。 | ⭐⭐⭐ |
| **`sarpstar/cinecode`** | GitHub: `sarpstar/cinecode` (`@Yooeec3`) | 纯代码（Canvas / Three.js / WebGL）生成数据可视化、历史沙盘推演、科普动效视频（0 抽卡废片率），适合【引擎 2】知识类短视频。 | ⭐⭐⭐⭐ |
| **`Wakeloom`** | GitHub: `a3974892-cmd/wakeloom` (`@gaoyy9`) | Windows 桌面端 Colab 算力管理与 ComfyUI API 面板化参考，供公司 Win11 电脑备选参考。 | ⭐⭐⭐ |

---

## 六、 标准执行检查清单 (Pre-Flight & Post-Flight Checklist)

每次启动漫剧制作任务时，AGY 必须按以下顺序逐项打勾执行：

- [ ] **Step 1（本地 0 CU）**：确认剧本已完成“动作外显化”，单镜时长 5~8 秒，台词 $\le 25$ 字，画风明确锁定为 **3D 国漫影视 CG 风（UE5 质感）**。
- [ ] **Step 2（资产准备）**：主角【16:9 四联角色身份板（含鞋）】与【无人物空镜场景图】已生成并通过视觉检查，Owner 已确认人物造型过关。
- [ ] **Step 3（首帧检查）**：镜头首帧（`1344×768` 或 `768×1344`）已生成，放大核验无多指、无畸变、左右站位正确。
- [ ] **Step 4（提示词门禁）**：H3 六段式提示词已就绪（英文动作运镜 + 单一运镜指令 + `<d>[Mandarin] 台词</d> He closes his mouth` + 中文场景白名单 + 末尾 `No subtitles, no text, 不要出现任何字幕`）。
- [ ] **Step 5（云端渲染与查账）**：运行 `colab usage` 记录初始 CU ➡️ 预热挂载 G4 96GB 运行 ComfyUI H3（关闭写实毛孔 LoRA，启用手动 `JoinMatch` 除雾） ➡️ 先跑 **1 个镜头（5~10 秒 MVP）** 拉回本地 ➡️ 立即关机并核验 `Active assignments: 0`。
- [ ] **Step 6（本地自检与包装）**：AGY 在本地对生成的 MP4 抽帧并检测音轨（确认真动态、真张嘴、无乱码字、声音清晰），压制对齐外挂/内嵌字幕后交付 Owner 验收。
