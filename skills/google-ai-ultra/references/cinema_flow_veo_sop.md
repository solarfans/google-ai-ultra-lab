# Hollywood AI Cinema Production Playbook — Google Flow (`Omni 1.2` / `Veo 3.1`) & `Lyria-002` SOP

> **Applicable Scope**: All photorealistic live-action dark-fantasy, sci-fi, historical epic, Warcraft, YouTube cinema shorts, and TikTok narrative films.
> **Full Benchmark & Tooling Report**: `/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/docs/research/HOLLYWOOD_AI_CINEMA_BENCHMARKS_TOOLS_AND_SOP_2026-11-12.md`
> **GCP Credit Ledger**: `/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/docs/GCP_CREDIT_LEDGER.md`

---

## 1. Dual-Channel Economics & Strict Routing Rule

| Channel | Entry Point | Model Matrix | Quota / Cost Pool | Routing Policy |
| :--- | :--- | :--- | :--- | :--- |
| **Channel A (DEFAULT PRIMARY)** | `https://flow.google.com` via AGY built-in `browser` subagent (`Model: "flash"`, persistent ULTRA login) | `Omni 1.2 Flash` (Flagship), `Veo 3.1 - Quality`, `Veo 3.1 - Fast`, `Veo 3.1 - Lite [Lower Priority]` (`0 credits`) | **Monthly `25,000` Flow Video Credits** (non-rollover, resets monthly on the 7th) — **`$0.00` GCP Credit Spend** | **100% of daily/episodic video generation MUST use Channel A.** Always switch prompt-bar settings from default `720p · x2` to **`1080p · x1`** before submitting. |
| **Channel B (SCORE & AUTHORIZED FALLBACK)** | Vertex AI (`us-central1`, `project-665ac784-237e-4a71-ad0`) via Python SDK | `lyria-002` (`$0.06`/30s stem), `veo-3.1-generate-001` (`$0.40/s`) | GCP Free Trial (`SGD 384.83`, exp `2027-02-07`) + GDP Monthly (`SGD 128.28/mo`) | **Routine auto-use permitted ONLY for `lyria-002` orchestral stems (`~$0.12/ep`)**. Calling `veo-3.1` on Channel B (`~$18.40` per 46s ep) is **LOCKED** unless explicitly approved by Owner in chat, and MUST be logged via `gcp_credit_ledger.py log`. |

---

## 2. Four-Stage Mandatory Cinema Production Pipeline (Zero Slop)

### Stage 1: Storyboard & 4-Asset Consistency Lock (Pre-Render Approval Gate)
1. Never jump straight to video generation, never use faceless mannequins, and never use FFmpeg `zoompan` on static images.
2. Invoke `image-generator` to create **photorealistic ARRI Alexa 65 (`16:9` or `9:16`) assets**:
   - **Character Turnaround Sheets** (`character_sheet_16x9.jpg` -> crop clean solo `ref_<char>_face.jpg` & `ref_<char>_front.jpg` plates);
   - **Per-Shot First-Frame Keyframe Plates** (`shot01.jpg` .. `shot08.jpg`) matching exact lighting, rain/fog atmosphere, and camera angle.
3. Present the Markdown storyboard artifact with embedded images to the Owner and **WAIT for approval** before spending a single Flow credit.

### Stage 2: Channel A (`Google Flow`) Browser Execution Protocol
1. **Stage Reference Uploads Properly**:
   - Because the `browser` subagent is sandboxed, copy single-segment filenames (`shot01.jpg`, `ref_illidan_face.jpg`, etc.) into `<Artifact Directory Path>/browser_sandbox/uploads/<filename>` and instruct the `browser` subagent to pass bare `<filename>` to `setInputFiles` / `fileChooser.setFiles`.
2. **Enforce Flow Studio Settings (Avoid `LL-014` Trap)**:
   - On `flow.google.com`, verify top-right `ULTRA` badge;
   - Open the bottom-right parameter pill (which defaults to `Video · 720p · 8s · x2`) and explicitly select:
     - **Model**: `Omni 1.2 Flash` or `Veo 3.1 - Quality` (`Veo 3.1 - Lite [Lower Priority]` for 0-credit tests)
     - **Resolution**: `1080p`
     - **Count**: `x1` (single high-precision take; do not burn 2x credits blindly)
     - **Duration**: `4s` or `6s` (`8s` only for grand finale shots).
3. **4-Part Cinema Prompt Formula**:
   - `[Camera & Lens]`: `Photorealistic live-action dark-fantasy Hollywood cinema shot on ARRI Alexa 65 anamorphic lens, shallow depth of field...`
   - `[Action & Physics]`: `Slow dramatic push-in as [Character] ... rain splashes off armor...`
   - `[Native Acting & Lip-Sync]`: `...speaks in a [voice timbre] with exact lip-sync: "<Short punchy line, 5-12 words>"`
   - `[Clean Audio Lock — MANDATORY]`: `Authentic [rain/wind/metal] Foley sound, zero background music, no subtitles, no text, no watermark.`
4. Download generated `1080p` `.mp4` clips from `browser_sandbox` downloads into `pipelines/<project>/renders/`.

### Stage 3: Orchestral Score (`Lyria-002` / `Flow Music`) & Hollywood Mastering
1. **Score Generation (`LL-012` Safe Prompting)**:
   - Never include real composer names (`Hans Zimmer`, `Russell Brower`) or vocal/choir terms in `lyria-002` prompts (triggers `400 INVALID_ARGUMENT`).
   - Use pure instrumental orchestration, key, and tempo: e.g., `"Dark epic orchestral fantasy film soundtrack in D minor, mournful solo cello, deep French horns, thunderous timpani swells, 72 bpm"`.
   - If using Vertex `lyria-002`, authenticate with `creds.refresh(Request())` + `x-goog-user-project: project-665ac784-237e-4a71-ad0` (`LL-011`) and log `$0.06/clip` via `scripts/gcp_credit_ledger.py log`.
2. **2.5s–5.5s Shot-Reverse-Shot Editing & Color Continuity (`LL-013`)**:
   - Keep shot durations tight (`3.0s–6.0s`).
   - If a multi-reference (`Ingredients`) shot exhibits a static 1–1.5s intro or brighter gamma than first-frame shots, trim `-ss 1.6` and apply matching nocturnal LUT (`eq=contrast=1.30:brightness=-0.13:gamma=0.74:saturation=1.15,colorbalance=bs=0.10:bm=0.07:bh=0.03:gs=-0.02`).
   - Apply `2.35:1` widescreen letterbox (`132px` top/bottom black bars on `1920x1080`) for horizontal cinema shorts, placing bilingual subtitles cleanly inside the lower safe zone.

### Stage 4: Dual Master Export & Cold-Viewer `read_file` Verification (`LL-014`)
1. Export two editions:
   - `Clean_1080p.mp4` & `Subtitled_1080p.mp4` with `-crf 22 -movflags +faststart` (`<90 MB`, streaming & `read_file` ready);
   - Optional `-crf 17` local archival master (keep all `.mp4` masters `.gitignore`d; archive to 30TB Google Drive when needed).
2. **Mandatory Final Gate**: Call `read_file` directly on the final `<90 MB` `.mp4` deliverable to inspect every cut, lip-sync alignment, gamma continuity, and orchestral mix before presenting to the Owner.
