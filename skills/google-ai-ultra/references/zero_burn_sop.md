# Google AI Ultra — 零浪费、防烧卡与 AI 漫剧防翻车铁律 (Zero-Burn & Anti-Cheat SOP v2.1)

完整细节请参阅仓库主法典：`/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/docs/AI_MANJU_AND_ULTRA_SOP.md`

---

### 铁律 1：锁定【3D 国漫 CG 风 AI 漫剧】，严禁真人换脸与静态图伪造
* 默认采用 **3D 国漫 / UE5 影视 CG 风**（对标《凡人修仙传》《画江湖之不良人》）或 **2.5D 国风厚涂漫**，规避真人恐怖谷效应。
* **五条死刑红线**：
  1. 严禁用 `ffmpeg` 平移缩放静态图（Ken Burns）冒充动态视频；
  2. 严禁用 OpenCV (`seamlessClone`) 传统几何贴图换脸；
  3. 严禁退回 `SDXL 1.0 / SVD-XT / SadTalker` 等过时模型；
  4. 严禁未经本地抽帧与音轨自检就将残次半成品抛给用户；
  5. 严禁未经「10 秒单镜头 MVP 验收」就盲目一次性批跑整集。

### 铁律 2：0 CU 本地备料与三类前置母本资产
* 开机前在本地（0 CU）完成：
  1. **剧本视觉化改编**：心理活动全部转为外显动作，区分「当面说 / 内心独白 / 画外音」，5 秒镜头台词 $\le 25$ 字；
  2. **16:9 角色四联身份板（Character Sheet）**：纯白底、正面半身特写 + 全身正/侧/背面 A-Pose，**必须写鞋子**；
  3. **纯净无人物空镜场景图**：对话戏出「正打 + 反打 + 站位全景」，绝不混入人物；
  4. **高清独立首帧**：用 `Qwen-Image-2.1` 垫图或九宫格拆图生成，冷读审核无误后再上云端。

### 铁律 3：0 CU CPU 下权重 + G4 75s 双通道 NVMe 预热
* 首次下载大模型权重走 **0.00 CU 免费 CPU 实例** 存入 30TB Google Drive。
* 选 G4 (96GB Blackwell) 时**保持「高 RAM」关闭**。
* 严禁直接 `ln -s` 软链读取 Google Drive FUSE（PyTorch `mmap` 随机读会掉速至 `25 MB/s` 卡死 28 分钟）；必须通过双通道预热脚本（`463 MB/s`）在 **75 秒内**拉入本地 NVMe SSD (`/content/fast_models`)，插件打包为单文件 `custom_nodes_bundle.tar.gz`（解压 1.5 秒），并以 `--highvram --disable-mmap --fast` 启动 ComfyUI。

### 铁律 4：MiniMax-H3 漫剧渲染六大核心参数
1. **关闭真人写实毛孔 LoRA**：旁路或设 `h3-realism-people` / `Facial-Realism-CloseUp` 权重为 `0.0`。
2. **黄金帧数公式**：$F(k) = 17k + 5$（主力档 `124` 帧 = 5.17s，`141` 帧 = 5.88s）。
3. **结构化提示词**：英文写动作与单一运镜（严禁单镜写多个运镜防闪切）+ `<d>[Mandarin] 台词</d> He closes his mouth after speaking` + 段尾 1.3s 闭嘴静音缓冲 + 中文场景白名单 + 末尾 `No subtitles, no text, no watermark, 不要出现任何字幕`。
4. **原生自锚定声纹 (`Self-Anchor Voice`)**：剥离第 1 镜原生人声转 `32kHz` 立体声 WAV 作为后续 `<Audio 1>`，单镜只挂当前说话人 1 路音频（单说话人门控）。
5. **手动除雾 (`MiniMaxH3JoinMatch`)**：`tuning="manual", strength=0.35, min_excess=2.5, match_spread=False, match_detail=False`。
6. **5MB 潜变量断点热插拔**：通过 `H3SaveAVLatent` 保存 `.pt`，局部返修用 `--only-seg N`（3 分钟 / `0.48 CU`）。

### 铁律 5：强制生命周期自毁、配额轮询确认与内存/盘防爆线 (`ultra_meter.py v2.1`)
* **点火前与停机后双轨查账**：必须执行 `colab usage` 对账，任务结束在 `finally` 中强制停止会话，二次确认 `Active assignments: 0` 与 `0.00 CU/h`。
* **配额账本轮询注销 + `504` 孤儿反查**：`ultra_meter.py` v2.1 在 `unassign` 后轮询 `list_assignments()` 最长 `8s` 确认配额释放，自动清扫未写入本地 store 的云端孤儿实例（防 `504/ReadTimeout` 后台静默扣费），并强制 `python -E -s` + 清洗 `PYTHONPATH`/`VIRTUAL_ENV`（`LL-AGY-008`）。
* **G4 Cgroup 感知 `/dev/shm` OOM 防线**：G4（`176 GB RAM`）大张量占满内存时 `/dev/shm` 仍可能虚报 `80+ GB` 空闲，重型 PyTorch/多进程任务必须用 `min(shm_free, MemAvailable - 32 GB)` 控流（可通过 `ultra_meter.py shm-guard --emit-snippet` 一键输出远程脚本片段）。
* **Drive 大文件写入防爆盘与停机刷盘**：严禁向 `/content/drive` FUSE 无节流写入 `100GB+` 模型撑爆 `235 GB` 根盘（大文件持久化走 `rclone copy --vfs-cache-mode off --bwlimit 80M`）；凡涉及向 Drive 落盘的批处理，运行 `ultra_meter.py run --flush-drive` 在停机前执行 `os.sync()` + `drive.flush_and_unmount()`（量化侧车优先走 `colab download` 直传本机）。
