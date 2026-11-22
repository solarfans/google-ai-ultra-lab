# Global EN AI Explainer Dual-Track Production SOP (`v5.2`)

Standard repeatable operating procedures for producing **Global English** YouTube (`16:9`, `1920x1080`) + TikTok / YouTube Shorts (`9:16`, `1080x1920`) AI Explainer videos in `/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab`.

Choose **Track A** as the default daily driver (`$0.00 / 0 CU`), or **Track B** on demand when an episode requires a talking-head digital twin (`InfiniteTalk` lip-sync). For cinematic dark-fantasy/narrative shorts (e.g., *Warcraft Illidan*), use **Track C** ([`cinema_flow_veo_sop.md`](./cinema_flow_veo_sop.md)).

---

## Track A — Default `$0 / 0 CU` Pure Kinetic UI + WordBoundary White-Pill (Ep02 v2 Standard)

Best for product launches, workflow walkthroughs, and high-retention explainers with 0% face-cam overhead.

### 1. Script & Audio / WordBoundary Generation
- Voice standard: **`V2_Brian_CasualCreator`** (`edge-tts` `en-US-BrianMultilingualNeural`, `RATE = "+1%"`, natural pacing, no `atempo` distortion).
- Background music: Shared local Flow Music asset `assets/music_library/how_markets_break/hmb_02_data_analysis.wav` mixed at **`-22 dB`** (`amix` + `alimiter=limit=0.95`).
- Procedural UI SFX (`pop.wav`, `whoosh.wav`, `tick.wav` at `48 kHz`) are synthesized automatically and overlaid at scene/beat transitions.
- Reference generator: [`scripts/synth_ep02_v2_en_brian.py`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/scripts/synth_ep02_v2_en_brian.py)
  - Reads `pipelines/ai_explainer_ep02/script_lines_en.txt` (adapt path or parameterize for Ep03+).
  - Captures exact `edge-tts` `WordBoundary` timestamps, groups 2–4 words per caption pill, outputs `pipelines/ai_explainer_ep01/pk_talkcraft/remotion/public/voice_ep02_mix.mp3` and auto-generates `pipelines/ai_explainer_ep01/pk_talkcraft/remotion/src/captions_ep02.ts`.
  ```bash
  cd "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab"
  python3 scripts/synth_ep02_v2_en_brian.py
  ```

### 2. Remotion Kinetic UI Primitives (`video-talkcraft`)
- Remotion workspace: `pipelines/ai_explainer_ep01/pk_talkcraft/remotion` (backed by `tools_runtime/video-talkcraft/runtime/node_modules`).
- Reusable kinetic components in `src/ep02_components.tsx`:
  - `AtmosphericStudioBackdrop`: Warm-indigo studio bokeh + subtle horizon glow + parallax micro-stars.
  - `TopLeftKicker`: Compact pill kicker (no heavy full-width top header bar).
  - `GeminiWindowFrame`: Floating golden-trimmed UI shell.
  - `AnimatedCursor`, `GoldenFocusBox`, `WhitePillCaption`, `GeminiSparkleIcon`, `GoogleDriveTriangleIcon`.
- Compositions registered in `src/Root.tsx`:
  - `Ep02GeminiTasks` (`Ep02Main.tsx`, `1920x1080 @ 30fps`)
  - `Ep02GeminiTasksVertical` (`Ep02MainVertical.tsx`, `1080x1920 @ 30fps`)

### 3. Dual-Aspect Render & Visual Gate
```bash
cd "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/ai_explainer_ep01/pk_talkcraft/remotion"
npx remotion render src/index.ts Ep02GeminiTasks out/ep02_16x9.mp4 --codec=h264 --crf=20 --pixel-format=yuv420p --concurrency=4
npx remotion render src/index.ts Ep02GeminiTasksVertical out/ep02_9x16.mp4 --codec=h264 --crf=20 --pixel-format=yuv420p --concurrency=4
```
- Deliver final `.mp4` masters + mix `.mp3` + script `.md` into `~/Downloads/<YYYY-MM-DD>_<Episode_Name>/` and verify key frames & playback via `read_file` before reporting `COMPLETED`.

---

## Track B — On-Demand Colab G4 `InfiniteTalk` Lip-Sync Explainer (Ep01 Final LipSync Standard)

Use on demand when a talking-head digital twin presenter is desired (~`2.92 CU`, ~`18.5 min` on Colab G4 96GB Blackwell; keep Shorts/TikTok cut under `58s`).

### 1. Dry Voice Mix & 832x480 Anchor Portrait Prep
- Reference generator: [`scripts/synth_en_v2_brian.py`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/scripts/synth_en_v2_brian.py)
  - Reads `pipelines/ai_explainer_ep01/script_lines_en.txt`, synthesizes `en-US-BrianMultilingualNeural` (`+0%`), trims silence, applies `loudnorm=I=-18:TP=-1.5:LRA=9`.
  - Tightens pauses (`0.45s -> 0.25s`) if total duration exceeds `57.5s`.
  - Mixes `assets/music_library/how_markets_break/hmb_02_data_analysis.wav` at `-21 dB` -> `remotion/public/voice_en_brian_mix.mp3`.
  - Crops `assets/digital_twin/portraits/anchor_v1_charcoal_shirt.png` to Lanczos `832x480` -> `anchor_832x480.png`.
  ```bash
  cd "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab"
  python3 scripts/synth_en_v2_brian.py
  ```

### 2. Colab G4 `InfiniteTalk` Talking-Head Render (Zero-Burn Guarded)
- Scripts: [`scripts/run_phase_b_infinitetalk_g4.py`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/scripts/run_phase_b_infinitetalk_g4.py) + [`scripts/g4_infinitetalk_worker.py`](/Users/kaykel/AI_PROJECTS/AI%20OS%20Backup_Mac/google-ai-ultra-lab/scripts/g4_infinitetalk_worker.py).
- Runs ComfyUI + `ComfyUI-WanVideoWrapper` (`fp8`/`bf16`, LightX2V 6-step, `colormatch="mkl"`, `transformers 5.x` Wav2Vec hook) at `832x480 @ 25fps`, protected by `ultra_meter.py` `finally: stop-all` auto-teardown.
- Copy the returned raw lip-sync video into `pipelines/ai_explainer_ep01/pk_talkcraft/remotion/public/avatar_en_v2_brian.mp4`.

### 3. Remotion Zero-Reset Composite & Render
- **Critical invariant**: Place `<OffthreadVideo>` once at root level **outside** `<Sequence>` (`MainEN.tsx` / `MainENVertical.tsx`) so scene transitions never reset lip-sync playback.
```bash
cd "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/ai_explainer_ep01/pk_talkcraft/remotion"
npx remotion render src/index.ts Ep01Gemini4EN out/ep01_16x9.mp4 --codec=h264 --crf=20 --pixel-format=yuv420p --concurrency=4
npx remotion render src/index.ts Ep01Gemini4ENVertical out/ep01_9x16.mp4 --codec=h264 --crf=20 --pixel-format=yuv420p --concurrency=4
```
- Deliver `01_YouTube_16x9_*.mp4`, `02_TikTok_Shorts_9x16_*.mp4`, raw avatar `.mp4`, and dry `48kHz` `.mp3` to `~/Downloads/<YYYY-MM-DD>_<Episode_Name>/`.
