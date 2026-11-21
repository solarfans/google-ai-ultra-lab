export const T = {
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
  sans: '"PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", sans-serif',
  mono: '"SF Mono", "JetBrains Mono", Menlo, monospace',
} as const;

export const FPS = 30;
export const TOTAL_FRAMES = 1122; // 37.40s * 30fps (synced to manifest_voiceC_v2.json)

export const SHOTS = [
  { id: 's1', start: 0, end: 161, chapter: 1, subtitle: '谷歌八天连发 Carbon、Hydrogen、Neon 三款 Gemini 4，菜单多出二十七个档位' },
  { id: 's2', start: 161, end: 281, chapter: 1, subtitle: '其实不用纠结，它们不是分强弱，而是三条分工线' },
  { id: 's3', start: 281, end: 514, chapter: 2, subtitle: '日常七成五锁死 Neon：编码榜首 58.6，比 Carbon 省三成、快三倍，但过二十万上下文会掉速' },
  { id: 's4', start: 514, end: 687, chapter: 3, subtitle: 'Carbon 排雷最深，可改几行也要干等七八分钟，只留给十个文件以上的大重构和实盘风控' },
  { id: 's5', start: 687, end: 887, chapter: 3, subtitle: 'Hydrogen 速度是 3.8 Flash 的两倍半，改脚本十几秒；但别单开 Extra，容易六十秒断流' },
  { id: 's6', start: 887, end: 1122, chapter: 4, subtitle: '最后给你一套抄作业公式：日常挂 Orchestrator，Neon 规划 Hydrogen 施工，换活开新对话，上线再让 Opus 复核' },
] as const;
