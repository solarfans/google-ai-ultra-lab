# YouTube YPP (`Y0`) Original English Pilot Decision Brief (`2026-11-20`)

> **Policy Baseline**: Respects YouTube Partner Program **`2027-02-01`** full-ad monetization threshold (**500 -> 1,000+ subs / 3,000h -> 8,000h** long-form watch hours) and strict `Inauthentic Content` / Fake-Trailer rules.  
> **Hard IP Redline**: **100% original English IP only**. *Warcraft (Illidan/Arthas)* and *《楚氏春秋》* remain strictly non-commercial benchmark sandboxes and are banned from any YPP channel.  
> **Compute Budget (`$0` Cash / `$0` GCP Credit Burn)**: Consume November **`25,050` Flow Video credits** (resetting `2026-12-07`, `Omni 1.2 Flash` `1080p · x1`) + **`30,000` Commercial Flow Music credits** (plus optional zero-cash self-recorded or synthetic original narration with explicit YouTube AI content disclosure).

---

## Owner Decision Prompt: Pick ONE Track (`A` / `B` / `C`)

Per `GOALS.yaml` (`goal_youtube_ypp_en`) and strict `WIP = 1` sequencing (launching `Y1` monthly 2x long-form + retention cadence after `OmniExtract` distribution), pick **exactly 1** track below for the `60–90s` `Y0` Pilot before `2026-12-07`:

### Option A (**Recommended**): High-RPM Dark-Tech & Quantitative Finance Visual Documentary (`ColdLedger` / `Silent Alpha`)
- **Target Audience & RPM**: Tier-1 English audience (`US / UK / SG / AU`), estimated **`$12–$24` RPM** (finance, market crashes, quantitative systems, tech history).
- **Day-1 Monetization (Pre-YPP)**: Relevant developer/quant/cloud tool SaaS affiliates in description (`Stripe SG` / partner payouts) + zero-copyright sponsorship hook.
- **60–90s `Y0` Pilot Beat Sheet**:
  1. `0–8s` Cold Hook: *"Why 94% of retail trading bots fail within 14 days — the microstructure trap nobody plots."*
  2. `8–30s` Cinema Establish (`Omni 1.2 Flash` `1080p · x1`, original obsidian/wireframe server-vault visual shots + `Flow Music` dark ambient pulse).
  3. `30–65s` Visual Mechanism Breakdown: Clean English narration + animated order-book cascade & stop-clustering schematic (zero stolen clips).
  4. `65–85s` Resolution + Open Loop for `12-min` Ep01 long-form feature (`how to prove positive expectancy out-of-sample`).
- **Flow Budget**: `<= 1,200` Flow Video credits (`8–10` scenes @ `1080p · x1`) + `<= 300` Flow Music credits; **`$0.00` GCP Credits**.

### Option B: Original Cosmic-Sci-Fi Visual Lore + `<11.5h` Ambient Retention Live Streams (`Aether Archive`)
- **Target Audience & RPM**: English sci-fi lore, AI cinema enthusiasts, and study/focus ambient listeners (**`$4–$9` RPM**, huge watch-hour compounding via `<11.5h` looping ambient live archives synced with original `Flow Music`).
- **Day-1 Monetization (Pre-YPP)**: Gumroad/Stripe digital lore wallpaper & soundtrack packs + AI cinema workflow tool affiliates.
- **60–90s `Y0` Pilot Beat Sheet**:
  1. `0–10s` First-person ship log entering an abandoned Dyson megastructure (100% original worldbuilding & character names).
  2. `10–60s` Multi-shot dark orbital cinema (`Omni 1.2 Flash` `1080p · x1`) scored with seamless commercial `Flow Music`.
  3. `60–85s` Signal transmission cliffhanger teasing Episode 1 (`10-min` documentary lore) + linked 8h ambient Focus Stream for watch-hour accumulation (`3,000h -> 8,000h`).
- **Flow Budget**: `<= 1,500` Flow Video credits + `<= 600` Flow Music credits; **`$0.00` GCP Credits**.

### Option C: Autonomous AI Engineering Breakdown (`Zero-Hype Agent Systems`, Cross-Promoting `OmniExtract MCP`)
- **Target Audience & RPM**: AI engineers, MCP builders, indie hackers (`US / EU / SG`, **`$10–$20` RPM**).
- **Day-1 Monetization (Pre-YPP)**: Direct organic funnel to **`poweragy/omni-extract-mcp`** (`$5 / 1k` Apify PPE + developer tool affiliates).
- **60–90s `Y0` Pilot Beat Sheet**:
  1. `0–8s` Hook: *"Stop feeding 403 errors and raw JS shells into your AI agent — here is the zero-cookie extraction pipeline."*
  2. `8–65s` Visual architecture diagrams + real side-by-side terminal comparison + dark minimal motion shots (`Omni 1.2 Flash` + `Flow Music`).
  3. `65–85s` Call-to-action pointing to `solarfans/omni-extract-mcp` & Apify hosted MCP, setting up a `10-min` deep-dive series on autonomous agent sandboxes.
- **Flow Budget**: `<= 900` Flow Video credits + `<= 250` Flow Music credits; **`$0.00` GCP Credits**.

---

## Execution Gate & `kill_if` Discipline (`GOALS.yaml`)
- **Pre-Production Gate**: Run `python3 scripts/ypp_pilot_gate.py <manifest.json>` — must verify `language == "en"`, `original_ip == True`, `ai_disclosure_required == True`, `gcp_usd_budget == 0`, `flow_credit_budget <= 2000`, and zero banned IP keywords before any video generation runs.
- **`kill_if` Hard Stop (`2027-02-01` discipline)**: After publishing `6` original English long-form videos in `Y1`, **pivot or stop** if median CTR `< 3%`, median AVD `< 25%`, AND subscriber growth `< 100`.
