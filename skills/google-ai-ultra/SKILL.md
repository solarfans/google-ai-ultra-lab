---
name: google-ai-ultra
description: >-
  Google AI Ultra 20x (25,000 Flow Video credits + 30,000 Flow Music credits + 30TB Drive + 2,500 Colab CU + GCP Credits)
  Hollywood AI Cinema production (`flow.google.com` Omni 1.2 Flash / Veo 3.1 + Lyria-002), GCP Credit Ledger manager,
  Colab G4 (96GB Blackwell) GPU orchestrator, and 3D Guoman AI Manju skill for Antigravity (AGY). Activate whenever the
  user asks to produce movie-grade AI videos / YouTube or TikTok narrative shorts (e.g. Warcraft, dark fantasy, sci-fi),
  use Google Flow / Veo 3.1 / Omni 1.2, check or log Google Cloud credits, check Colab compute units (CU), run Colab G4
  workloads, or produce AI Manju / audiobooks.
---

# Google AI Ultra — Hollywood AI Cinema, GCP Credit Ledger & Compute Workstation (v5.0)

This skill equips Antigravity (AGY) with zero-waste operational command over the **Google AI Ultra 20x** ecosystem:
1. **Hollywood Photorealistic AI Cinema Pipeline (Channel A Primary)**: Persistent logged-in `flow.google.com` (`25,050` monthly Flow Video credits -> **`Omni 1.2 Flash` / `Veo 3.1 Quality` `1080p · x1`**) + `Lyria-002` / `Flow Music` orchestral scoring. Detailed playbook: [references/cinema_flow_veo_sop.md](./references/cinema_flow_veo_sop.md).
2. **Deterministic GCP Credit Ledger (`SGD 513.11` Protected Pool)**: Mandatory line-item tracking of the 90-day Free Trial (`SGD 384.83`, expires `2027-02-07`) + GDP Monthly Credits (`SGD 128.28/mo`) via [`scripts/gcp_credit_ledger.py`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/scripts/gcp_credit_ledger.py) and [`docs/GCP_CREDIT_LEDGER.md`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/docs/GCP_CREDIT_LEDGER.md).
3. **Colab G4 (`96GB Blackwell`) Zero-Burn Compute & Hobby 3D Manju**: Guarded by `scripts/ultra_meter.py` and [references/zero_burn_sop.md](./references/zero_burn_sop.md) (`LL-001` through `LL-014` in [`LESSONS_LEARNED.md`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/pipelines/short_drama/LESSONS_LEARNED.md)).

---

## Dual-Host Execution Routing (MacBook Direct vs Corporate Win11 MCP-Relay)

Because personal Google OAuth tokens (`~/.config/colab-cli/token.json`) and the persistent `flow.google.com` ULTRA browser session live on the Home MacBook (and personal Google accounts must NEVER be logged into on the corporate Win11 PC):
1. **On Home MacBook (Direct Host)**:
   - Run `browser` subagent (`flow.google.com`), `gcp_credit_ledger.py`, and `ultra_meter.py` directly.
2. **On Office Corporate Windows 11 (MCP-Relay Client)**:
   - **NEVER** ask the Owner to sign into personal Google accounts on Win11; transparently route `ultra_meter.py`, `gcp_credit_ledger.py`, and `google-ai-ultra-lab` commands to Home MacBook via `macbook-track-b` MCP (`run_shell`).

---

## 0. Six-Pool Quota Router & Strict Anti-Slop Architecture (v5.0 Ground Truth)

严禁混淆不同配额池，严禁放着顶配闭源电影大模型不用而去跑落后的量化开源假人模型（`LL-010` 惨痛教训）：

| 独立权益池 | 2026-11 实测额度与刷新规则 | 唯一正确生产定位与路由死规 |
| :--- | :--- | :--- |
| **1. Flow Video (`flow.google.com`) — 通道 A（默认视频主力）** | **`25,050` credits**（每账期 7 日刷新清零，不结转；内置浏览器已持久化登录 `ULTRA`） | **所有电影级短片、魔兽/暗黑奇幻真人剧、YouTube/TikTok 叙事视频的唯一默认引擎（`$0.00` GCP 赠金消耗）**。主力调用 **`Omni 1.2 Flash`** 与 **`Veo 3.1 - Quality`**（12-05 交棒给 Omni 系列）；空镜预演可用 `0 积分` 的 `Veo 3.1 - Lite [Lower Priority]`。**提交前必须把默认 `720p · x2` 改为 `1080p · x1`！** |
| **2. Flow Music (`Credits`)** | **`30,000` credits/月**（含商业发行授权） | 商用级主题曲、情绪铺底音床（`$0.00` GCP 赠金消耗）。 |
| **3. GCP Credits (`Vertex AI` — 通道 B，严格受控）** | 初始 `SGD 513.11`（Free Trial `SGD 384.83` `2027-02-07` 到期 + GDP `SGD 128.28/月`；当前余约 `SGD 487.72`） | **视频 API (`veo-3.1-generate-001` `$0.40/s`) 默认上锁**，未经 Owner 当面批准严禁私自调用烧赠金！日常仅开放 **`lyria-002` 电影交响配乐 API（`$0.06`/首，单集约 `SGD 0.15`）** 及双机 VPN（`~SGD 9.75/月`）。**任何消费必须当场运行 `gcp_credit_ledger.py log` 记入 GitHub 账本！** |
| **4. Colab GPU (`CU`)** | 实测余额 **`2,477.54 CU`**（活跃实例 `0`，`0.0 CU/h`） | **严禁再用于拼凑无脸塑料假人或低精度 `int8` 视频充当商业成片！** 专用于：`kto-oat`/`BTA` 十万组量化张量寻优、大批量离线计算，以及个人兴趣试验田《楚氏春秋》3D 国漫特定实验。强制受 `ultra_meter.py` 超时自毁保护。 |
| **5. 30TB Google Drive** | 30 TB 云端存储 | 归档 `>50 MB` 的无损电影母带（`CRF 17` `.mp4`）与原始分轨，严禁将大体积 `.mp4` 塞入 Git 仓库触发 GitHub `100 MB` 拒推。 |
| **6. AGY / Gemini 4 Argon** | Ultra 20x 档位 + 本地 Apple Silicon M3 Pro | 总导演、分镜编剧、`image-generator` 角色定妆锁脸、FFmpeg 宽银幕暗夜调色混音、以及交付前全片 `read_file` 原生视听冷读终审。 |

---

## 1. Four Ironclad Cinema Rules (彻底根除“图省事”与低质 AI 垃圾片铁律)

凡制作任何电影短片或对外发布视频（详见 [references/cinema_flow_veo_sop.md](./references/cinema_flow_veo_sop.md)），必须无条件执行以下 4 道硬门禁：

1. **铁律 1（无定妆不渲染 — Stage-1 Visual Sign-Off Gate）**：
   - 开拍前必须先用 `image-generator` 生成 **`ARRI Alexa 65` 真人实拍级角色定妆三视图（Turnaround Sheet）与核心分镜首帧图（Keyframes）**，整理成审片单呈现给 Owner 点头确认。**未经视觉签字，严禁提交任何视频渲染任务！** 永久禁用无五官假人、详情页白底截图拼贴与静态图 `zoompan` 平移冒充视频。
2. **铁律 2（`2.5s–5.5s` 好莱坞正反打快切 + 画内原生口型表演）**：
   - 单镜头严格控制在 `3.0–6.0s`（微距特写 ➔ 正打说话近景 ➔ 反打眼神特写 ➔ 越肩高潮对峙），严禁 >8 秒呆滞长镜头；
   - 视频 Prompt 末尾强制附加 `zero background music, no subtitles, no text`，由模型原生输出 `48kHz` 情绪人声口型（Native Lip-Sync）与环境物理音效（暴雨/金属/火焰），再叠加独立的 `Lyria-002` / `Flow Music` 贯穿式交响配乐。
3. **铁律 3（通道 A `flow.google.com` 沙盒上传与 `1080p · x1` 锁死）**：
   - 驱动 `browser` 子智能体（`Model: "flash"`）操作已登录的 `flow.google.com` 时，先将参考图复制至 `<Artifact Directory>/browser_sandbox/uploads/<filename>`；
   - 提交前强制检查右下角生成参数已从默认 `720p · x2` 切换为 **`1080p` + `x1`**，杜绝双倍吞积分与低清废片。
4. **铁律 4（跨镜色调对齐 + `<90 MB` 全片 `read_file` 原生视听终审）**：
   - 对多参考图模式可能出现的起势停顿与曝光偏亮（`LL-013`），使用 FFmpeg 裁剪起势缓冲（`-ss 1.6`）并挂载暗夜电影 LUT 对齐色调，压制 `2.35:1` 变形宽银幕遮幅与安全区字幕；
   - 导出 `<90 MB` 的 `CRF 22 -movflags +faststart` 成片，**必须调用 `read_file` 完整观看并聆听全片每一秒**，以陌生挑剔观众视角确认达到电影预告片水准后方可交付。

---

## 2. Standard Operational Commands

### 2.1 GCP 赠金账本查询、预估与消费记账（每次涉及 GCP/Vertex 必跑）
```bash
cd "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab"
python3 scripts/gcp_credit_ledger.py status
python3 scripts/gcp_credit_ledger.py estimate --lyria-clips 2
python3 scripts/gcp_credit_ledger.py log --category VERTEX_AI_SCORE --pipeline warcraft_illidan_ep02 \
  --service "Vertex AI lyria-002" --detail "2 stems @ $0.06" --usd 0.12 --notes "Ep02 orchestral score"
```

### 2.2 Colab G4 算力巡检与紧急归零止损
```bash
python3 ~/.gemini/config/skills/google-ai-ultra/scripts/ultra_meter.py usage
python3 ~/.gemini/config/skills/google-ai-ultra/scripts/ultra_meter.py stop-all
```

### 2.3 《楚氏春秋》个人兴趣试验田专用门禁（保留兼容）
《楚氏春秋》仅作为个人兴趣与技术验证（非商业化），其原著锚定与 6 道声学门禁详见 [`docs/AI_MANJU_AND_ULTRA_SOP.md`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/docs/AI_MANJU_AND_ULTRA_SOP.md)（`manju_qa_gate.py` & `manju_compiler.py`）。
