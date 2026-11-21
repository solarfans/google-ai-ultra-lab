import React from 'react';
import {
  AbsoluteFill,
  Audio,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { SHOTS_EN, T_EN } from './theme_en';

const CHAPTERS_EN = [
  { id: 1, label: '01 Three Lanes' },
  { id: 2, label: '02 Neon & 200K Cap' },
  { id: 3, label: '03 Carbon & Hydrogen' },
  { id: 4, label: '04 Cheat Sheet' },
];

/**
 * Mounted once at root level outside <Sequence> so InfiniteTalk lip-sync
 * plays continuously across every scene without frame resets.
 */
const PersistentAvatarLayer: React.FC<{ badge: string }> = ({ badge }) => {
  const frame = useCurrentFrame();
  const isHero = frame < SHOTS_EN[0].end;
  const pushScale = isHero
    ? interpolate(frame, [0, SHOTS_EN[0].end], [1.0, 1.04], { extrapolateRight: 'clamp' })
    : 1.0;

  return (
    <div
      style={{
        position: 'absolute',
        left: 64,
        top: isHero ? 225 : 731,
        width: isHero ? 740 : 396,
        height: isHero ? 610 : 223,
        borderRadius: isHero ? 24 : 20,
        overflow: 'hidden',
        border: isHero ? '1.5px solid rgba(241, 245, 249, 0.16)' : '2px solid rgba(245, 158, 11, 0.55)',
        boxShadow: isHero ? '0 28px 64px rgba(0, 0, 0, 0.6)' : '0 20px 50px rgba(0, 0, 0, 0.65)',
        background: '#0F131B',
        zIndex: 30,
      }}
    >
      <OffthreadVideo
        src={staticFile('avatar_en_v2_brian.mp4')}
        muted
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          objectPosition: 'center 20%',
          transform: `scale(${pushScale})`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: isHero ? 24 : 14,
          bottom: isHero ? 24 : 12,
          background: 'rgba(11, 14, 20, 0.85)',
          border: '1px solid rgba(241, 245, 249, 0.16)',
          padding: isHero ? '10px 18px' : '4px 12px',
          borderRadius: isHero ? 12 : 999,
          fontSize: isHero ? 19 : 14,
          fontWeight: 600,
          color: T_EN.ink,
          fontFamily: T_EN.sans,
        }}
      >
        {badge}
      </div>
    </div>
  );
};

const DotGridBackdrop: React.FC = () => {
  const frame = useCurrentFrame();
  const drift = (frame * 0.35) % 36;
  return (
    <AbsoluteFill
      style={{
        backgroundColor: T_EN.bg,
        backgroundImage: `
          radial-gradient(circle at 76% 24%, rgba(245, 158, 11, 0.085), transparent 44%),
          radial-gradient(circle at 22% 80%, rgba(34, 197, 94, 0.065), transparent 40%),
          radial-gradient(rgba(207, 224, 255, 0.14) 1.2px, transparent 1.2px)
        `,
        backgroundSize: '100% 100%, 100% 100%, 36px 36px',
        backgroundPosition: `0 0, 0 0, ${drift}px ${drift * 0.4}px`,
      }}
    />
  );
};

const TopBar: React.FC<{ activeChapter: number }> = ({ activeChapter }) => (
  <div
    style={{
      position: 'absolute',
      top: 30,
      left: 64,
      right: 64,
      height: 52,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      borderBottom: `1px solid ${T_EN.border}`,
      paddingBottom: 14,
      zIndex: 20,
      fontFamily: T_EN.sans,
    }}
  >
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 12,
        fontFamily: T_EN.mono,
        fontSize: 17,
        letterSpacing: '0.05em',
        color: T_EN.ink,
      }}
    >
      <span style={{ width: 10, height: 10, borderRadius: 999, background: T_EN.amber, display: 'inline-block' }} />
      <span>GOOGLE GEMINI 4 · 2026-11 BENCHMARK GUIDE</span>
    </div>
    <div style={{ display: 'flex', gap: 26, fontSize: 17, fontWeight: 600 }}>
      {CHAPTERS_EN.map((ch) => {
        const active = ch.id === activeChapter;
        return (
          <span
            key={ch.id}
            style={{
              color: active ? T_EN.ink : '#64748B',
              borderBottom: active ? `2px solid ${T_EN.amber}` : '2px solid transparent',
              paddingBottom: 12,
            }}
          >
            {ch.label}
          </span>
        );
      })}
    </div>
  </div>
);

const SubtitleBar: React.FC<{ text: string }> = ({ text }) => (
  <div
    style={{
      position: 'absolute',
      left: 64,
      right: 64,
      bottom: 44,
      display: 'flex',
      justifyContent: 'center',
      zIndex: 40,
      fontFamily: T_EN.sans,
    }}
  >
    <span
      style={{
        display: 'inline-block',
        maxWidth: 1640,
        padding: '10px 26px',
        borderRadius: 12,
        background: 'rgba(11, 14, 20, 0.90)',
        border: '1px solid rgba(241, 245, 249, 0.15)',
        fontSize: 25,
        lineHeight: 1.35,
        fontWeight: 600,
        color: T_EN.ink,
        textAlign: 'center',
      }}
    >
      {text}
    </span>
  </div>
);

const S1Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 16, stiffness: 140 } });

  return (
    <AbsoluteFill style={{ fontFamily: T_EN.sans, color: T_EN.ink }}>
      <div
        style={{
          position: 'absolute',
          top: 112,
          left: 64,
          right: 64,
          bottom: 132,
          display: 'grid',
          gridTemplateColumns: '740px 1fr',
          gap: 44,
          alignItems: 'center',
        }}
      >
        <div style={{ width: 740, height: 610 }} />

        <div>
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              padding: '12px 22px',
              borderRadius: 14,
              background: 'rgba(245, 158, 11, 0.12)',
              border: '1px solid rgba(245, 158, 11, 0.45)',
              color: '#FCD34D',
              fontSize: 22,
              fontWeight: 600,
              marginBottom: 22,
              transform: `translateX(${interpolate(enter, [0, 1], [24, 0])}px)`,
              opacity: enter,
            }}
          >
            Q: Google dropped 3 Gemini 4 models in 8 days — which one should you pick?
          </div>
          <div
            style={{
              fontSize: 52,
              lineHeight: 1.18,
              fontWeight: 800,
              letterSpacing: '-0.02em',
              marginBottom: 26,
              transform: `translateY(${interpolate(enter, [0, 1], [16, 0])}px)`,
              opacity: enter,
            }}
          >
            <span style={{ color: T_EN.amber }}>Google</span> Dropped 3 <span style={{ color: T_EN.amber }}>Gemini 4</span> Models
            <br />
            Stop Guessing <span style={{ fontFamily: T_EN.mono, color: T_EN.amber }}>27</span> Tiers — Lock 3 Lanes
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 18, marginBottom: 24 }}>
            {[
              { date: 'Nov 10', sym: 'C', name: 'Gemini 4 Carbon', sub: 'Heavy Tank · 8%', color: T_EN.red, border: 'rgba(229, 72, 77, 0.5)', bg: T_EN.panel, delay: 8 },
              { date: 'Nov 12', sym: 'H', name: 'Gemini 4 Hydrogen', sub: 'Speed Runner · 15%', color: T_EN.green, border: 'rgba(34, 197, 94, 0.5)', bg: T_EN.panel, delay: 14 },
              { date: 'Nov 18', sym: 'Ne', name: 'Gemini 4 Neon ★', sub: 'Daily Driver · 75%', color: T_EN.amber, border: 'rgba(245, 158, 11, 0.7)', bg: 'rgba(245, 158, 11, 0.08)', delay: 20 },
            ].map((el) => {
              const cardSp = spring({ frame: Math.max(0, frame - el.delay), fps, config: { damping: 14, stiffness: 150 } });
              return (
                <div
                  key={el.sym}
                  style={{
                    padding: '20px',
                    borderRadius: 16,
                    background: el.bg,
                    border: `1px solid ${el.border}`,
                    transform: `translateY(${interpolate(cardSp, [0, 1], [20, 0])}px) scale(${interpolate(cardSp, [0, 1], [0.92, 1])})`,
                    opacity: cardSp,
                  }}
                >
                  <div style={{ fontSize: 16, color: T_EN.muted, fontFamily: T_EN.mono }}>{el.date}</div>
                  <div style={{ fontSize: 44, fontWeight: 800, color: el.color, margin: '6px 0 4px' }}>{el.sym}</div>
                  <div style={{ fontSize: 20, fontWeight: 700 }}>{el.name}</div>
                  <div style={{ fontSize: 16, color: el.sym === 'Ne' ? '#FCD34D' : T_EN.muted, marginTop: 6 }}>{el.sub}</div>
                </div>
              );
            })}
          </div>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '18px 26px',
              borderRadius: 16,
              background: '#101520',
              border: '1px solid rgba(229, 72, 77, 0.45)',
              opacity: spring({ frame: Math.max(0, frame - 24), fps, config: { damping: 16 } }),
            }}
          >
            <span style={{ fontSize: 21, fontWeight: 600 }}>Google Antigravity Live Model Menu</span>
            <span style={{ fontSize: 25, fontWeight: 800, color: T_EN.amber, fontFamily: T_EN.mono }}>11 Groups / 27 Tiers</span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S2Lanes: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ fontFamily: T_EN.sans, color: T_EN.ink }}>
      <div style={{ position: 'absolute', top: 110, left: 500, right: 64, bottom: 126, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 22 }}>
        <div style={{ fontSize: 42, fontWeight: 800 }}>
          <span style={{ color: T_EN.amber }}>Google Gemini 4</span> Isn&apos;t a Ranking — It&apos;s <span style={{ color: T_EN.amber }}>3 Work Lanes</span>
        </div>
        <div style={{ background: T_EN.panel, border: `1px solid ${T_EN.border}`, borderRadius: 18, padding: '28px 34px', display: 'flex', flexDirection: 'column', gap: 24 }}>
          {[
            { label: '10 Ne · Gemini 4 Neon (Daily Coding & Q&A)', pct: 75, color: T_EN.amber, delay: 4 },
            { label: '01 H · Gemini 4 Hydrogen (Quick Scripts & Unit Tests)', pct: 15, color: T_EN.green, delay: 12 },
            { label: '06 C · Gemini 4 Carbon (10+ File Refactors & Risk Audits)', pct: 8, color: T_EN.red, delay: 20 },
          ].map((r) => {
            const p = spring({ frame: Math.max(0, frame - r.delay), fps, config: { damping: 18, stiffness: 110 } });
            return (
              <div key={r.label}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 23, fontWeight: 700 }}>
                  <span>{r.label}</span>
                  <span style={{ fontFamily: T_EN.mono, color: r.color }}>{r.pct}%</span>
                </div>
                <div style={{ height: 18, background: 'rgba(241, 245, 249, 0.08)', borderRadius: 999, overflow: 'hidden', marginTop: 12 }}>
                  <div style={{ height: '100%', width: `${r.pct * p}%`, background: r.color, borderRadius: 999 }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S3Neon: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fastFill = interpolate(frame, [24, 52], [0, 39], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const slowFill = interpolate(frame, [52, 86], [0, 61], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ fontFamily: T_EN.sans, color: T_EN.ink }}>
      <div style={{ position: 'absolute', top: 110, left: 500, right: 64, bottom: 126, display: 'flex', flexDirection: 'column', gap: 22 }}>
        <div
          style={{
            background: T_EN.panel,
            border: `1px solid ${T_EN.border}`,
            borderRadius: 18,
            padding: '24px 32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
            <div
              style={{
                width: 92,
                height: 92,
                borderRadius: 16,
                background: T_EN.amberSoft,
                border: `2px solid ${T_EN.amber}`,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
              }}
            >
              <span style={{ fontFamily: T_EN.mono, fontSize: 15, color: T_EN.amber }}>10</span>
              <span style={{ fontSize: 34, fontWeight: 800 }}>Ne</span>
            </div>
            <div>
              <div style={{ fontSize: 38, fontWeight: 800 }}>Google Gemini 4 Neon</div>
              <div style={{ fontSize: 20, color: T_EN.muted, marginTop: 4 }}>Agent Arena 1336 · $2.82 median/task</div>
            </div>
          </div>
          <div
            style={{
              padding: '12px 24px',
              borderRadius: 12,
              background: 'rgba(245, 158, 11, 0.16)',
              border: `1px solid ${T_EN.amber}`,
              fontSize: 23,
              fontWeight: 800,
              color: '#FCD34D',
              fontFamily: T_EN.mono,
            }}
          >
            75% DAILY DRIVER
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 22 }}>
          {[
            { label: 'AA Coding Agent Index', val: '#1 · 58.6', sub: 'Beats Fable 58.47 & Opus 58.16', subColor: T_EN.green, pct: 92, color: T_EN.amber, delay: 4 },
            { label: 'Cost vs. Carbon', val: '-32%', sub: 'Zapier Automation #1 (56.3%)', subColor: T_EN.muted, pct: 68, color: T_EN.green, delay: 12 },
            { label: 'Avg. Real-World Speed', val: '~3.0x', sub: 'No more 7–8 min waits', subColor: T_EN.muted, pct: 85, color: T_EN.cyan, delay: 20 },
          ].map((m) => {
            const sp = spring({ frame: Math.max(0, frame - m.delay), fps, config: { damping: 16, stiffness: 120 } });
            return (
              <div
                key={m.label}
                style={{
                  background: T_EN.panel,
                  border: `1px solid ${T_EN.border}`,
                  borderRadius: 18,
                  padding: '24px 28px',
                  transform: `translateY(${interpolate(sp, [0, 1], [18, 0])}px)`,
                  opacity: sp,
                }}
              >
                <div style={{ fontSize: 19, color: T_EN.muted }}>{m.label}</div>
                <div style={{ fontSize: 52, fontWeight: 800, fontFamily: T_EN.mono, color: m.color, margin: '10px 0 6px' }}>{m.val}</div>
                <div style={{ fontSize: 18, color: m.subColor }}>{m.sub}</div>
                <div style={{ height: 12, background: 'rgba(241, 245, 249, 0.08)', borderRadius: 999, overflow: 'hidden', marginTop: 14 }}>
                  <div style={{ height: '100%', width: `${m.pct * sp}%`, background: m.color, borderRadius: 999 }} />
                </div>
              </div>
            );
          })}
        </div>

        <div
          style={{
            borderRadius: 18,
            padding: '24px 32px',
            border: '1px solid rgba(229, 72, 77, 0.42)',
            background: 'rgba(24, 18, 22, 0.92)',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: 25, fontWeight: 700, color: '#FCA5A5' }}>⚠ REAL-WORLD REDLINE: Latency spikes past 200K context</span>
            <span style={{ fontFamily: T_EN.mono, fontSize: 21, color: T_EN.muted }}>512K Hard Cap</span>
          </div>
          <div style={{ position: 'relative', height: 22, background: '#1E2533', borderRadius: 999, margin: '18px 0 12px', overflow: 'hidden' }}>
            <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: `${fastFill}%`, background: T_EN.green }} />
            <div
              style={{
                position: 'absolute',
                left: '39%',
                top: 0,
                bottom: 0,
                width: `${slowFill}%`,
                background: 'repeating-linear-gradient(-45deg, rgba(229,72,77,0.72), rgba(229,72,77,0.72) 12px, rgba(229,72,77,0.35) 12px, rgba(229,72,77,0.35) 24px)',
              }}
            />
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 18, fontFamily: T_EN.mono }}>
            <span style={{ color: T_EN.green }}>0–200K · Sweet Spot</span>
            <span style={{ color: T_EN.red, fontWeight: 700 }}>▲ 200K Slowdown (Start a new chat)</span>
            <span style={{ color: T_EN.muted }}>512K Cap</span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S4Carbon: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = spring({ frame, fps, config: { damping: 16, stiffness: 130 } });
  const secs = Math.round(interpolate(frame, [8, 84], [0, 450], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const mm = String(Math.floor(secs / 60)).padStart(2, '0');
  const ss = String(secs % 60).padStart(2, '0');
  return (
    <AbsoluteFill style={{ fontFamily: T_EN.sans, color: T_EN.ink }}>
      <div style={{ position: 'absolute', top: 110, left: 500, right: 64, bottom: 126, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <div
          style={{
            background: T_EN.panel,
            border: '1px solid rgba(229,72,77,0.55)',
            borderRadius: 18,
            padding: 38,
            display: 'grid',
            gridTemplateColumns: '1fr 380px',
            gap: 32,
            alignItems: 'center',
            transform: `translateY(${interpolate(sp, [0, 1], [16, 0])}px)`,
            opacity: sp,
          }}
        >
          <div>
            <div style={{ fontSize: 21, color: T_EN.red, fontWeight: 700 }}>06 C · GOOGLE GEMINI 4 CARBON (8% SHARE)</div>
            <div style={{ fontSize: 44, fontWeight: 800, lineHeight: 1.18, margin: '12px 0 18px' }}>Deepest Debugger — Never Use for Quick Edits</div>
            <div style={{ fontSize: 22, color: T_EN.muted, lineHeight: 1.65 }}>
              • CursorBench 4.0 / WANDR #1 · Text Arena 1526
              <br />• Built for exhaustive search &amp; multi-pass self-checks
              <br />• <strong style={{ color: T_EN.ink }}>Only use for: 10+ file cross-module refactors &amp; live trading kernels</strong>
            </div>
          </div>
          <div style={{ background: '#1C1419', border: `2px solid ${T_EN.red}`, borderRadius: 18, padding: 32, textAlign: 'center' }}>
            <div style={{ fontSize: 20, color: '#FCA5A5' }}>Quick-Edit Wait Time</div>
            <div style={{ fontFamily: T_EN.mono, fontSize: 74, fontWeight: 800, color: T_EN.red, margin: '10px 0' }}>
              {mm}:{ss}
            </div>
            <div style={{ fontSize: 19, color: T_EN.muted }}>7–8 min baseline</div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S5Hydrogen: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cardSp = spring({ frame, fps, config: { damping: 16, stiffness: 130 } });
  const lockSp = spring({ frame: Math.max(0, frame - 32), fps, config: { damping: 14, stiffness: 160 } });
  return (
    <AbsoluteFill style={{ fontFamily: T_EN.sans, color: T_EN.ink }}>
      <div style={{ position: 'absolute', top: 110, left: 500, right: 64, bottom: 126, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <div
          style={{
            background: T_EN.panel,
            border: '1px solid rgba(34,197,94,0.55)',
            borderRadius: 18,
            padding: 38,
            display: 'grid',
            gridTemplateColumns: '1fr 400px',
            gap: 32,
            alignItems: 'center',
            opacity: cardSp,
          }}
        >
          <div>
            <div style={{ fontSize: 21, color: T_EN.green, fontWeight: 700 }}>01 H · GOOGLE GEMINI 4 HYDROGEN (15% SHARE)</div>
            <div style={{ fontSize: 44, fontWeight: 800, lineHeight: 1.18, margin: '12px 0 18px' }}>
              <span style={{ fontFamily: T_EN.mono, color: T_EN.green }}>2.5x</span> Faster Than 3.8 Flash · Done in Seconds
            </div>
            <div style={{ fontSize: 22, color: T_EN.muted, lineHeight: 1.65 }}>
              • Use <strong style={{ color: T_EN.ink }}>High</strong> directly for quick scripts, tests, and doc updates
              <br />• Also powers the execution layer inside Orchestrator
            </div>
          </div>
          <div
            style={{
              background: '#1C1419',
              border: `2px solid ${T_EN.red}`,
              borderRadius: 18,
              padding: 28,
              textAlign: 'center',
              transform: `scale(${interpolate(lockSp, [0, 1], [1.14, 1])})`,
              opacity: lockSp,
            }}
          >
            <div style={{ fontSize: 20, color: '#FCA5A5', fontWeight: 700 }}>⛔ NEVER RUN SOLO</div>
            <div style={{ fontFamily: T_EN.mono, fontSize: 44, fontWeight: 800, color: T_EN.red, margin: '14px 0' }}>Extra (XHigh)</div>
            <div style={{ fontSize: 20, color: T_EN.ink }}>Hits 60s Idle Stream EOF</div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S6Formula: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const stampSp = spring({ frame: Math.max(0, frame - 34), fps, config: { damping: 14, stiffness: 170 } });
  return (
    <AbsoluteFill style={{ fontFamily: T_EN.sans, color: T_EN.ink }}>
      <div style={{ position: 'absolute', top: 110, left: 500, right: 64, bottom: 126, display: 'flex', flexDirection: 'column', gap: 22 }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 390px', gap: 24 }}>
          <div style={{ background: T_EN.panel, border: `1px solid ${T_EN.border}`, borderRadius: 18, padding: '26px 32px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 12 }}>
              <span style={{ fontSize: 27, fontWeight: 800 }}>
                Daily Gold Formula: <span style={{ color: T_EN.amber }}>Orchestrator (Neon)</span>
              </span>
              <span
                style={{
                  fontFamily: T_EN.mono,
                  padding: '6px 14px',
                  borderRadius: 999,
                  background: 'rgba(34,197,94,0.14)',
                  border: `1px solid ${T_EN.green}`,
                  color: T_EN.green,
                  fontSize: 16,
                  whiteSpace: 'nowrap',
                }}
              >
                Fresh Chat &lt;200K
              </span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 18, marginTop: 18 }}>
              <div style={{ flex: 1, padding: '18px 22px', borderRadius: 14, background: T_EN.panel2, border: '1px solid rgba(245, 158, 11, 0.5)' }}>
                <div style={{ fontFamily: T_EN.mono, fontSize: 15, color: T_EN.amber }}>STEP 1 · PLANNER</div>
                <div style={{ fontSize: 25, fontWeight: 800, marginTop: 6 }}>Neon (High)</div>
                <div style={{ fontSize: 17, color: T_EN.muted, marginTop: 4 }}>Read-only plan · -32% cost</div>
              </div>
              <div style={{ fontSize: 34, color: T_EN.amber, fontWeight: 800 }}>➔</div>
              <div style={{ flex: 1, padding: '18px 22px', borderRadius: 14, background: T_EN.panel2, border: '1px solid rgba(34, 197, 94, 0.5)' }}>
                <div style={{ fontFamily: T_EN.mono, fontSize: 15, color: T_EN.green }}>STEP 2 · EXECUTOR</div>
                <div style={{ fontSize: 25, fontWeight: 800, marginTop: 6 }}>Hydrogen (High)</div>
                <div style={{ fontSize: 17, color: T_EN.muted, marginTop: 4 }}>2.5x fast edits · auto-escalates</div>
              </div>
            </div>
          </div>

          <div
            style={{
              borderRadius: 18,
              padding: 24,
              border: `2px solid ${T_EN.red}`,
              background: 'rgba(229, 72, 77, 0.08)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              transform: `scale(${interpolate(stampSp, [0, 1], [1.18, 1])})`,
              opacity: stampSp,
            }}
          >
            <div>
              <div style={{ fontFamily: T_EN.mono, fontSize: 15, color: '#FCA5A5' }}>POOL B · ISOLATED QUOTA</div>
              <div style={{ fontSize: 31, fontWeight: 800, marginTop: 8 }}>Claude Opus 5.5</div>
            </div>
            <div style={{ fontSize: 18, color: T_EN.ink, lineHeight: 1.45 }}>
              Stay idle daily · Call{' '}
              <strong style={{ color: T_EN.red }}>Opus Audit</strong> for final release sign-off
            </div>
          </div>
        </div>

        <div style={{ background: T_EN.panel, border: `1px solid ${T_EN.border}`, borderRadius: 18, padding: '22px 30px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 19 }}>
            <thead>
              <tr>
                {['Google Model Tier', 'Daily Share', 'Core Benchmark / Role', 'Hard Redline'].map((h) => (
                  <th key={h} style={{ textAlign: 'left', color: T_EN.muted, fontSize: 15, fontWeight: 600, paddingBottom: 12, borderBottom: `1px solid ${T_EN.border}` }}>
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[
                { name: 'Gemini 4 Neon', color: T_EN.amber, pct: '75%', bench: 'Coding #1 (58.6) · ~3x speed / -32% cost', red: 'Slows >200K (512K cap)', redColor: '#FCA5A5' },
                { name: 'Gemini 4 Hydrogen', color: T_EN.green, pct: '15%', bench: '2.5x vs 3.8 Flash · Scripts done in seconds', red: 'Never run Extra solo (60s EOF)', redColor: '#FCA5A5' },
                { name: 'Gemini 4 Carbon', color: T_EN.red, pct: '8%', bench: 'CursorBench #1 · Deep bugs & risk kernels', red: '7–8 min wait even on tiny edits', redColor: '#FCA5A5' },
                { name: 'Gemini 4 Argon', color: T_EN.cyan, pct: '2%', bench: 'Unified 1M window · Massive repo overviews', red: 'Use Neon for daily coding', redColor: T_EN.muted },
              ].map((row, idx) => {
                const rowSp = spring({ frame: Math.max(0, frame - (12 + idx * 6)), fps, config: { damping: 18 } });
                return (
                  <tr key={row.name} style={{ opacity: rowSp }}>
                    <td style={{ padding: '12px 10px 12px 0', borderBottom: idx < 3 ? '1px solid rgba(241,245,249,0.06)' : 'none', fontWeight: 700, color: row.color, whiteSpace: 'nowrap' }}>{row.name}</td>
                    <td style={{ padding: '12px 10px 12px 0', borderBottom: idx < 3 ? '1px solid rgba(241,245,249,0.06)' : 'none', fontFamily: T_EN.mono, color: row.color, fontWeight: 700 }}>{row.pct}</td>
                    <td style={{ padding: '12px 10px 12px 0', borderBottom: idx < 3 ? '1px solid rgba(241,245,249,0.06)' : 'none' }}>{row.bench}</td>
                    <td style={{ padding: '12px 0', borderBottom: idx < 3 ? '1px solid rgba(241,245,249,0.06)' : 'none', color: row.redColor }}>{row.red}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const SCENES_EN: Record<string, React.FC> = {
  s1: S1Hook,
  s2: S2Lanes,
  s3: S3Neon,
  s4: S4Carbon,
  s5: S5Hydrogen,
  s6: S6Formula,
};

export const MainEN: React.FC = () => {
  const frame = useCurrentFrame();
  const active = SHOTS_EN.find((s) => frame >= s.start && frame < s.end) ?? SHOTS_EN[SHOTS_EN.length - 1];

  return (
    <AbsoluteFill>
      <DotGridBackdrop />
      <Audio src={staticFile('voice_en_brian_mix.mp3')} />
      <TopBar activeChapter={active.chapter} />
      {SHOTS_EN.map((shot) => {
        const Scene = SCENES_EN[shot.id];
        return (
          <Sequence key={shot.id} from={shot.start} durationInFrames={shot.end - shot.start}>
            <Scene />
          </Sequence>
        );
      })}
      <PersistentAvatarLayer badge={active.badge} />
      <SubtitleBar text={active.subtitle} />
    </AbsoluteFill>
  );
};
