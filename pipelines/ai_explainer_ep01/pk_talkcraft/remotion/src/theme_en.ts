export const T_EN = {
  bg: '#0B0E14',
  panel: 'rgba(19, 24, 35, 0.92)',
  panel2: '#181F2E',
  border: 'rgba(241, 245, 249, 0.12)',
  ink: '#F1F5F9',
  muted: '#94A3B8',
  amber: '#F59E0B',
  amberSoft: 'rgba(245, 158, 11, 0.14)',
  green: '#22C55E',
  red: '#E5484D',
  cyan: '#38BDF8',
  sans: '"SF Pro Display", "Inter", -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif',
  mono: '"SF Mono", "JetBrains Mono", Menlo, monospace',
} as const;

export const FPS = 30;
export const TOTAL_FRAMES_EN = 1726; // 57.550s * 30fps (synced to manifest_en_v2_brian.json)

export const SHOTS_EN = [
  {
    id: 's1',
    start: 0,
    end: 221,
    chapter: 1,
    badge: 'Studio · Real-World Evals',
    subtitle: 'Google dropped Carbon, Hydrogen, and Neon in 8 days — 27 Gemini 4 tiers.',
  },
  {
    id: 's2',
    start: 221,
    end: 374,
    chapter: 1,
    badge: '22% PiP · Real-World Split',
    subtitle: 'Stop comparing them by raw rank. They are 3 completely different work lanes.',
  },
  {
    id: 's3',
    start: 374,
    end: 772,
    chapter: 2,
    badge: 'Daily Driver · Neon',
    subtitle: 'Lock 75% of daily work on Neon: #1 coding (58.6), 3x faster & 32% cheaper — watch the 200K cap.',
  },
  {
    id: 's4',
    start: 772,
    end: 1070,
    chapter: 3,
    badge: 'Heavy Tank · Carbon',
    subtitle: 'Carbon digs deepest, but even tiny edits wait 7–8 min. Save it for 10+ file refactors & risk audits.',
  },
  {
    id: 's5',
    start: 1070,
    end: 1390,
    chapter: 3,
    badge: 'Speed Runner · Hydrogen',
    subtitle: 'Hydrogen runs 2.5x faster than 3.8 Flash in seconds. Never run Extra solo or hit 60s stream EOF.',
  },
  {
    id: 's6',
    start: 1390,
    end: 1726,
    chapter: 4,
    badge: 'Cheat Sheet · Zero-FOMO',
    subtitle: 'Cheat sheet: Orchestrator (Neon plans, Hydrogen executes), fresh chat per task, Opus release audit.',
  },
] as const;
