export const T_EP02 = {
  bg0: '#090B1A',
  bg1: '#151233',
  glass: 'rgba(15, 20, 40, 0.84)',
  glassBorder: 'rgba(248, 250, 252, 0.14)',
  ink: '#F8FAFC',
  muted: '#94A3B8',
  lavender: '#A78BFA',
  blue: '#60A5FA',
  emerald: '#34D399',
  coral: '#FB7185',
  amber: '#FBBF24',
  sans: '"SF Pro Display", "Inter", -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif',
  mono: '"SF Mono", "JetBrains Mono", Menlo, monospace',
} as const;

export const FPS = 30;
export const TOTAL_FRAMES_EP02 = 1685; // 56.164s * 30fps (synced to manifest_ep02_en.json)

export const SHOTS_EP02 = [
  {
    id: 's1',
    start: 0,
    end: 204,
    pill: 'GOOGLE GEMINI TASKS',
    chapter: '01 / 07 · Rebrand',
    subtitle: 'Gemini Spark is now Gemini Tasks — works even after you lock your phone.',
  },
  {
    id: 's2',
    start: 204,
    end: 409,
    pill: 'EXECUTION ENGINE',
    chapter: '02 / 07 · Cloud + Mac',
    subtitle: 'Flip Chat to Task: isolated cloud VM + browser, or Mac Chrome Auto Browse.',
  },
  {
    id: 's3',
    start: 409,
    end: 710,
    pill: 'PLANS & TRIGGERS',
    chapter: '03 / 07 · Free vs Ultra',
    subtitle: 'Free (6 countries): 10 schedules · Pro/Ultra: 50 schedules, 15 parallel & monitors.',
  },
  {
    id: 's4',
    start: 710,
    end: 935,
    pill: 'VS CHATGPT DOTS',
    chapter: '04 / 07 · Ecosystem',
    subtitle: 'ChatGPT Dots needs $100/mo Pro · Gemini Tasks is built into Gmail, Drive & Chrome.',
  },
  {
    id: 's5',
    start: 935,
    end: 1195,
    pill: 'QUOTA REALITY',
    chapter: '05 / 07 · The Catch',
    subtitle: 'Rolling 5-hour compute pool — one Ultra user hit the wall in <90 min on 2 jobs.',
  },
  {
    id: 's6',
    start: 1195,
    end: 1417,
    pill: 'BOUNDARIES',
    chapter: '06 / 07 · Limits',
    subtitle: 'Calls & Google Pay checkout remain U.S.-only; topic monitors are not instant.',
  },
  {
    id: 's7',
    start: 1417,
    end: 1685,
    pill: 'WINNING PLAYBOOK',
    chapter: '07 / 07 · AI OS Split',
    subtitle: 'Run Gmail monitors & web sweeps in Tasks · Keep heavy code on your local stack.',
  },
] as const;
