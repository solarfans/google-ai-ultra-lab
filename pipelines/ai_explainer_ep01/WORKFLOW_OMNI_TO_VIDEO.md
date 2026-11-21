# Omni 知识库 → AI 科普蒸馏长期工作流（Phase A / Zero-Burn 底座）

> **定位**：将本地沉淀的一手实测知识资产转化为高信息密度代码动效科普成片（杜绝泛化新闻复述与 AI Slop 空镜拼贴）。

---

## 1. 四源知识底座（Single Source of Truth）

1. **Obsidian 个人知识库**：`/Users/kaykel/Library/Mobile Documents/iCloud~md~obsidian/Documents/Iris/98_Melvin_Notes/`
   - 存放由 `omni-content-pipeline` 自动提炼入库的 X 深度文章、技术长帖、抖音拆解笔记。
2. **抖音 AGY 数据库**：`/Users/kaykel/AI_PROJECTS/douyin-fav-study/data/library.db`
   - 存放收藏夹视频转录文本（`transcript`）、结构化笔记（`note_json`）与本地原片路径（`local_path`），用于提取痛点话术与爆款节奏参考（可配合 `rea-video` 拆解）。
3. **Canon 专题研究报告**：`/Users/kaykel/ai-agent-bridges/ai-agent-lab-canon/docs/research/`
   - 存放已交叉核验的工程手册与实时探针基线（如 `AGY_PRACTICAL_PLAYBOOK_AND_MULTI_AGENT_GUIDE_2026-11-14.md` v3.1）。
4. **第三方 GitHub 仓库台账**：`/Users/kaykel/ai-agent-bridges/ai-agent-lab-canon/docs/research/THIRD_PARTY_GITHUB_REPOSITORY_LEDGER.md`
   - 存放每个开源项目的 Stars / License / 实读局限 / 选型结论，避免被营销帖误导。

---

## 2. 去水蒸馏 3 条硬门禁（Anti-Slop Gate）

1. **拒绝新闻腔与空话**：禁止“最近 AI 圈炸锅了/震撼发布”类废话；第 1 句直接抛真实冲突或具体数字。
2. **密度硬指标**：每支 30–60 秒短视频脚本必须同时包含：
   - 至少 **3 个可核验基准数字或实测耗时/成本**；
   - 至少 **1 条真实踩坑红线（What NOT to do）**；
   - 至少 **1 套观众立刻能抄走的配置公式**。
3. **口语化与视觉动作绑定**：口播文本必须提前切分成短句（`script_lines.txt`），并同步产出逐句对应的视觉动作词（挤压、抽出、高亮、进度轴、对比卡）与结构化对比表数据，直接喂给 `HyperFrames` / `video-talkcraft`。

---

## 3. 五步标准生产流水线（阶段 A 本机 0 CU → 阶段 B 按需 G4）

1. **Step 1 · 知识蒸馏**：多源检索验证 → 输出 `SCRIPT_<LANG>_V1.md` + `script_lines.txt`（含对比表数据与物理动效节拍）。
2. **Step 2 · 本地声纹配音（`0 CU / $0`）**：
   - 使用固定锚点参考音频 `assets/digital_twin/voice_samples/seed_zh_clean.wav`；
   - 运行 `scripts/synth_voxcpm2_voice.py` 在 Mac Apple Silicon 上生成 48kHz 主干声与逐句时间戳 `manifest.json`（或使用路线 A 真人口播 + `WhisperX`/`voice_trim.py`）。
3. **Step 3 · 3 张关键帧静态样图确认**：
   - 在写全片长动画前，先渲染 **开场标题 + 人像小窗占比 + 核心对比卡片** 3 张静态样图人工快审。
4. **Step 4 · 代码动效渲染（`0 CU`）**：
   - 由 `HyperFrames`（HTML/GSAP + 本地预览/Cloud Run）或 `video-talkcraft`（Remotion）渲染 60fps 深色机构风（`#0B0E14` + `#F1F5F9` + 强调色 `<=3`）矢量动效画布，叠加人物小窗与 `assets/music_library/` 商用底乐。
5. **Step 5 · 数字分身角标小窗（阶段 B 按需拉起 Colab G4）**：
   - 确认音画与动效定稿后，仅针对需要人物口播的段落拉起 Colab G4 `Wan2.1-I2V-14B + InfiniteTalk`（`--highvram --disable-mmap`），生成 `832×480` 驱动人像并缩放入 1080p 画布 22% 角落圆角 PiP，跑完立即 `ultra_meter.py stop-all`。
