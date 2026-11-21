# Phase A 双引擎同题 PK 实测记分牌（HyperFrames vs video-talkcraft）

> **评测标的**：《Google 密集发布 Gemini 4 Carbon / Neon / Hydrogen，到底怎么选？》（`28.20s` · `1920×1080` · `30fps` · `846 帧`）  
> **测试环境**：Home MacBook Apple M3 Pro (`11` 核 · `18GB` 统一内存) · 全程 **`0 Colab CU / $0.00 GCP`**  
> **共享资产**：`anchor_v1_charcoal_shirt.png`（炭黑衬衫定妆照）+ `Voice C`（Mac 本地 `VoxCPM2 Voice Design` `27.53s` 48kHz）+ `Flow Music hmb_02_data_analysis.wav`（`-20 dB` 商业免版权底乐）

---

## 1. 实测硬指标对照表（均经本机计时渲染 + `ffprobe` + 全片 `read_file` 视听核验）

| 评估维度 | **引擎 1：`HyperFrames` (`v0.9.75`)** | **引擎 2：`video-talkcraft` (`Remotion v4.0.519`)** |
| :--- | :--- | :--- |
| **工程形态** | 单页原生 HTML + CSS + GSAP 时间轴（亦可拆 `compositions/`） | React + TypeScript 组件化（共享 `runtime/node_modules` 软链） |
| **前端静态检查** | `hyperframes lint .`：**`0 error(s), 9 warning(s)`**（首轮捕获 `<audio>` 缺 `id` 与中文字体需 `@font-face` / `Noto Sans SC` 映射） | `./node_modules/.bin/tsc --noEmit`：**`0` 错误**（首轮需改 `tsconfig.json` `include` 路径从 `smoke` 到 `src`） |
| **实测渲染耗时** | 墙上总耗时 **`30.56s`**（CLI 内部 **`19.9s`**：编译 `3.6s` + 音频 `1.7s` + 截图 `9.9s` + 编码 `2.1s`；开启 `static-dedup` 自动复用 **`57%`** 静帧） | 墙上总耗时 **`19.05s`**（`Concurrency 6x`，Webpack bundle 已预热） |
| **成片文件体积** | **`3.3 MB`**（`CRF 16`, H.264 + AAC `48kHz`） | **`9.4 MB`**（H.264 + AAC `48kHz`，因背景点阵持续微飘移无静帧复用） |
| **动效质感与能力实测** | ✅ GSAP 缓动曲线（`back.out` / `power3.out`）与 `scaleX` 进度条极跟手；<br>⚠️ 纯 GSAP 时间轴偏“CSS/属性补间”，动态跳表数字（如 `01:59 → 07:30` 滚动）不如 React 组件直觉 | ✅ **`spring()` 物理弹性更润**，且 **React 帧驱动动态文本（如 S4 `00:00 → 07:30` 实时跳秒）与连续飘移点阵底纹**天然丝滑；<br>✅ 自带 `108` 张动效配方卡与 `voice_trim.py` / 透明通道工作台 |
| **云端并行扩展性** | ✅ 原生内置 `hyperframes cloudrun`（适配每月 `$100` GCP 赠金） | ⚠️ 需自行容器化 Remotion Lambda / Cloud Run；本地短片快，长片吃内存 |
| **本轮排错/Bug 次数** | `2` 次（`audio` 必须显式 `id`；`PingFang SC` 需切 `Noto Sans SC` 过静态字体闸） | `1` 次（`tsconfig.json` `include` 目录调整） |

---

## 2. 实测结论与推荐定位

1. **短平快日常科普主产线（1–3 分钟以内）➔ 推荐 `video-talkcraft / Remotion`**：
   - 实测 `19.05s` 渲完 28s 1080p 成片，React `useCurrentFrame()` 写动态数据表、跳秒计时器、K 线/回测曲线、物理弹簧曲线比手写 GSAP 更稳更易复用组件库（且直接继承其 `108` 张反 PPT 卡片和 `voice_trim.py` 剪气口工具）。
2. **长片/低依赖网页特效或云端 Cloud Run 并发渲染 ➔ 保留 `HyperFrames`**：
   - 成片体积小（`3.3 MB` vs `9.4 MB`）、`hyperframes snapshot` 与 `lint` 护栏极强，且自带 `Cloud Run` 一键分布式渲染通道，适合 5–15 分钟长视频零占用 Mac 本地 CPU。
3. **阶段 B 数字分身小窗衔接（已完全就绪）**：
   - 两套引擎左下角 PiP 框均已精确预留 **`396×223`（16:9，占宽 20.6%）**；只要您选定主力底座，进入阶段 B 时仅需拉起一次 Colab G4 `InfiniteTalk`（约 `2–3 CU`）把 `anchor.png` 驱动为口型同步小窗 `anchor_talk.mp4` 直接替换即可！
