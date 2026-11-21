# How Markets Break — 100% Free-Credit Zero-Confirmation Production Runbook (`v1.0` Baseline Archive)

> **Status:** `ARCHIVED_VERIFIED_BASELINE` (Promoted as supporting B-roll / BGM asset module; primary channel creative engine pivoting to Real-Face / Digital-Twin Talking-Head + Code-Driven Motion Graphics per `2026-11-21` research).  
> **Verified Commit:** `solarfans/google-ai-ultra-lab` `main` @ `4373fd8`  
> **Related Skill:** `google-ai-ultra` `v5.1` (`solarfans/ai-agent-lab-canon` @ `33d5a69`)

---

## 1. Verified Baseline & Deliverables

- **Pipeline Factory:** [`scripts/hmb_episode_factory.py`](../scripts/hmb_episode_factory.py) (`prepare` + `master` subcommands)
- **Unit Tests:** [`tests/test_hmb_episode_factory.py`](../tests/test_hmb_episode_factory.py) + [`tests/test_ypp_pilot_gate.py`](../tests/test_ypp_pilot_gate.py) (`7/7` PASS on both system `python3` and `.venv/bin/python`)
- **Compliance Gate:** [`scripts/ypp_pilot_gate.py`](../scripts/ypp_pilot_gate.py) enforces `manifest.json` (`track == "A"`, `language == "en"`, `gcp_usd_budget == 0`, IP disclosure rules) before synthesis or mastering runs.
- **Reusable Flow Music Library:** [`assets/music_library/how_markets_break/CATALOG.json`](../assets/music_library/how_markets_break/CATALOG.json) (`4` audited `48kHz` stereo `pcm_s16le` instrumental WAV tracks, `152s–177s`, generated on `https://www.flowmusic.app/` `Lyria 3.5` with Instrumental Mode ON; `5` Flow Music credits spent once-off, `0` ongoing credits, `$0.00` GCP).
- **Verified Production Outputs (Ep01, `117.27s`, mirrored to `~/Downloads/2026-11-20_HowMarketsBreak_Ep01_Master/`):**
  - `HowMarketsBreak_Ep01_Three_Liquidity_Signals_16x9_1080p_Clean.mp4` (`30.92 MB`)
  - `HowMarketsBreak_Ep01_Three_Liquidity_Signals_16x9_1080p_Subtitled.mp4` (`23.66 MB`)
  - `HowMarketsBreak_Ep01_Three_Liquidity_Signals_9x16_Shorts.mp4` (`22.09 MB`)

---

## 2. 4-Stage Zero-Confirmation Workflow

```text
[Stage 1: prepare] ─▶ [Stage 2: Flow T2V (browser)] ─▶ [Stage 3: master] ─▶ [Stage 4: Deliver]
   ~41s (Mac)              ~5.5 min (flow.google.com)       ~71s (Mac)         ~/Downloads/
```

### Stage 1 — `prepare <episode_spec.json>` (`~41s` on Mac)
```bash
"/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/.venv/bin/python" \
  "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/scripts/hmb_episode_factory.py" \
  prepare pipelines/<ep_dir>/episode_spec.json
```
1. Enforces `ypp_pilot_gate.py` compliance on sibling `manifest.json` (`gcp_usd_budget == 0`).
2. Fetches live Yahoo Finance daily closes (`^IXIC`, `GC=F`, `BTC-USD`, `HYG`, `IEF`, `^TNX`, `DX-Y.NYB`, `^VIX`, `^VIX3M`) -> `data/market_snapshot.json`.
3. Synthesizes 7 `edge-tts` narration beats (`20s` `asyncio.wait_for` timeout, em-dash sanitization for speech only, 4-tier prosody fallback resolving `NoAudioReceived` hangs) -> `audio/voiceover_timeline.json`.
4. Builds `audio/flow_music_score.wav` by crossfading segments from local `CATALOG.json` (`$0.00` GCP, `0` new Flow Music credits).
5. Renders headless-Chrome `1920×1080` SVG->PNG base charts (`charts/*.png`) and 30fps progressive wipe cards (`motion_assets/*.mp4`) using native `ffmpeg` `crop + fade + overlay` (`~2s` per card instead of `geq`).
6. Generates overflow-safe, sentence-boundary-guarded word-wrapped PNG subtitles and writes `flow_prompts.json`.

### Stage 2 — Zero-Confirmation Flow Text-to-Video (`~5.5 min` in AGY `webview_browser`)
- **Host Surface:** `https://flow.google.com` inside AGY built-in `webview_browser` (Chrome external CDP remote debugging stays unchecked to avoid Chrome 144+ per-session popups).
- **Mandatory Zero-Confirm Setting:** Use pure **Text-to-Video (`Omni 1.2 Flash · Ingredients · 16:9 · 720p · 8s · x1`)** — **never** call `setInputFiles` (local file upload triggers a hard AGY human confirmation dialog even in Turbo mode).
- Generates `5` cinematic clips (`24` Flow credits × `5` = `120` Flow credits) saved directly to `pipelines/<ep_dir>/renders/shot01_flow.mp4..shot05_flow.mp4`.

### Stage 3 — `master <episode_spec.json>` (`~71s` on Mac)
```bash
"/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/.venv/bin/python" \
  "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/scripts/hmb_episode_factory.py" \
  master pipelines/<ep_dir>/episode_spec.json
```
- Probes `renders/shot01_flow.mp4..shot05_flow.mp4` via `ffprobe`.
- Normalizes narration loudness, sidechain-ducks local Flow Music score, blends native Flow audio/Foley, and composites progressive charts + PNG subtitles (without relying on `libass`/`drawtext`, which Homebrew `ffmpeg` lacks on this host) into `output/` (`16x9 Clean`, `16x9 Subtitled`, `9x16 Shorts`).

### Stage 4 — Delivery Mirror
- Copies all three masters directly to `spec["downloads_dir"]` (`~/Downloads/YYYY-MM-DD_<Episode>_Master/`).

---

## 3. Exact Measured Timing & Resource Accounting

| Metric | Ep01 Actual (`2026-11-20` Total Wall-Clock) | Ep01 Post-Fix Steady-State Run (`20:23–20:32` mtime Verified) |
|---|---|---|
| **Stage 1 (`prepare`)** | ~45 min (first-time factory scripting + `edge-tts` 16m hang fix + `geq`->`crop` rewrite + `chart02_vix` overflow fix + Flow Music 4-track setup) | **`~41s`** (`20:23:26` -> `20:24:07`) |
| **Stage 2 (Flow 5-Clip T2V)** | `~5.5 min` | **`~5.5 min`** (`20:24:59` -> `20:30:33`, saved `20:30:52`) |
| **Stage 3 (`master` x3 MP4s)** | `~1 min 11s` | **`~1 min 11s`** (`20:31:00` -> `20:32:11`) |
| **End-to-End Elapsed** | `> 1 hr` (dev + debug included) | **`~7–8 minutes / ~2-min episode`** |
| **GCP Cash/Credit Spend** | `$0.00` (remaining `$380.09` / `SGD 487.57`) | **`$0.00`** |
| **Flow Video Credits** | `120` credits (`24,930 -> 24,810`) | **`120` credits / 5 clips** |
| **Flow Music Credits** | `5` credits one-time library build (`30,530 -> 30,525`) | **`0` credits** (local `CATALOG.json` reuse) |
| **Colab G4 Compute Units** | `0 CU` (remaining `2,477.54 CU`) | **`0 CU`** |
| **Human Confirmations** | `0` during Ep01 production (after Flow Music one-time Google OAuth) | **`0`** |

---

## 4. Known Constraints & Strategic Role Going Forward

1. **Key Technical Guards Retained:**
   - Never rely on Flow Music UI WAV blob export (`dl.path() === null` in `webview_browser`); download generated lossless audio via `https://storage.googleapis.com/producer-app-public/clips/<song_uuid>.wav`.
   - Always sanitize em-dashes (`—`) in `edge-tts` speech input (`pitch="+0Hz"` fallback), while preserving formal punctuation in rendered subtitle PNGs.
2. **Why This Pipeline Is Demoted from Main Format to Supporting Module:**
   - While steady-state execution is fast (`~7–8 min`), two structural weaknesses make **pure faceless Flow T2V + `edge-tts` + static SVG wipes** unsuitable as the main channel product:
     1. **Automation Fragility:** Stage 2 depends on automating `flow.google.com`'s Web UI DOM via browser subagent rather than deterministic CLI/code.
     2. **Content & Trust Ceiling ("AI Slop"):** Generic T2V stock B-roll + robotic TTS + wipe-revealed slides without a real human / high-craft talking-head presenter feels synthetic and fails audience trust & retention.
   - **Updated Role:** Retain [`assets/music_library/how_markets_break/CATALOG.json`](../assets/music_library/how_markets_break/CATALOG.json) as the copyright-safe instrumental BGM bed and reserve `flow.google.com` (`24,810` monthly credits) selectively for high-craft atmospheric opener B-roll, while shifting primary video production to **Real-Face / Digital-Twin Talking-Head + Code-Driven Motion Graphics (`HyperFrames` / `video-use`)**.
