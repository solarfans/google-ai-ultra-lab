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

const CHAPTER_LABELS: Record<number, { num: string; title: string }> = {
  1: { num: '01 / 04', title: 'Three Lanes' },
  2: { num: '02 / 04', title: 'Neon & 200K Cap' },
  3: { num: '03 / 04', title: 'Carbon & Hydrogen' },
  4: { num: '04 / 04', title: 'Cheat Sheet' },
};

/**
 * Root-mounted vertical avatar layer (never remounts across scenes -> exact lip-sync).
 * S1 uses a wide 960x540 (16:9) hero frame; S2-S6 shrinks smoothly to a 420x236 upper-left PiP.
 */
const PersistentAvatarLayerVertical: React.FC<{ badge: string }> = ({ badge }) => {
  const frame = useCurrentFrame();
  const isHero = frame < SHOTS_EN[0].end;
  const pushScale = isHero
    ? interpolate(frame, [0, SHOTS_EN[0].end], [1.0, 1.035], { extrapolateRight: 'clamp' })
    : 1.0;

  return (
    <div
      style={{
        position: 'absolute',
        left: 56,
        top: isHero ? 156 : 148,
        width: isHero ? 968 : 420,
        height: isHero ? 545 : 236,
        borderRadius: isHero ? 24 : 18,
        overflow: 'hidden',
        border: isHero ? '1.5px solid rgba(241, 245, 249, 0.16)' : '2px solid rgba(245, 158, 11, 0.58)',
        boxShadow: '0 24px 54px rgba(0, 0, 0, 0.65)',
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
          left: isHero ? 20 : 12,
          bottom: isHero ? 18 : 10,
          background: 'rgba(11, 14, 20, 0.86)',
          border: '1px solid rgba(241, 245, 249, 0.16)',
          padding: isHero ? '8px 16px' : '4px 10px',
          borderRadius: 999,
          fontSize: isHero ? 18 : 13,
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

const DotGridBackdropV: React.FC = () => {
  const frame = useCurrentFrame();
  const drift = (frame * 0.35) % 36;
  return (
    <AbsoluteFill
      style={{
        backgroundColor: T_EN.bg,
        backgroundImage: `
          radial-gradient(circle at 78% 18%, rgba(245, 158, 11, 0.095), transparent 45%),
          radial-gradient(circle at 20% 78%, rgba(34, 197, 94, 0.07), transparent 42%),
          radial-gradient(rgba(207, 224, 255, 0.14) 1.2px, transparent 1.2px)
        `,
        backgroundSize: '100% 100%, 100% 100%, 36px 36px',
        backgroundPosition: `0 0, 0 0, ${drift}px ${drift * 0.4}px`,
      }}
    />
  );
};

const TopBarVertical: React.FC<{ chapter: number }> = ({ chapter }) => {
  const ch = CHAPTER_LABELS[chapter] ?? CHAPTER_LABELS[1];
  return (
    <div
      style={{
        position: 'absolute',
        top: 56,
        left: 56,
        right: 56,
        height: 60,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        borderBottom: `1px solid ${T_EN.border}`,
        paddingBottom: 12,
        zIndex: 20,
        fontFamily: T_EN.sans,
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontFamily: T_EN.mono, fontSize: 18, color: T_EN.ink }}>
        <span style={{ width: 10, height: 10, borderRadius: 999, background: T_EN.amber, display: 'inline-block' }} />
        <span>GOOGLE GEMINI 4 · 2026-11 EVALS</span>
      </div>
      <div
        style={{
          fontFamily: T_EN.mono,
          fontSize: 17,
          fontWeight: 700,
          color: '#FCD34D',
          padding: '6px 14px',
          borderRadius: 999,
          background: 'rgba(245, 158, 11, 0.14)',
          border: '1px solid rgba(245, 158, 11, 0.45)',
        }}
      >
        {ch.num} · {ch.title}
      </div>
    </div>
  );
};

const SubtitleBarVertical: React.FC<{ text: string }> = ({ text }) => (
  <div
    style={{
      position: 'absolute',
      left: 48,
      right: 96,
      bottom: 235,
      display: 'flex',
      justifyContent: 'center',
      zIndex: 40,
      fontFamily: T_EN.sans,
    }}
  >
    <span
      style={{
        display: 'inline-block',
        maxWidth: 920,
        padding: '12px 24px',
        borderRadius: 14,
        background: 'rgba(11, 14, 20, 0.92)',
        border: '1px solid rgba(241, 245, 249, 0.18)',
        fontSize: 31,
        lineHeight: 1.32,
        fontWeight: 700,
        color: T_EN.ink,
        textAlign: 'center',
        boxShadow: '0 12px 32px rgba(0, 0, 0, 0.55)',
      }}
    >
      {text}
    </span>
  </div>
);

const TopPipAsideCard: React.FC<{ tag: string; title: string; highlight: string; color: string }> = ({
  tag,
  title,
  highlight,
  color,
}) => (
  <div
    style={{
      position: 'absolute',
      left: 500,
      top: 148,
      right: 56,
      height: 236,
      borderRadius: 18,
      background: T_EN.panel,
      border: `1px solid ${T_EN.border}`,
      padding: '22px 26px',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      fontFamily: T_EN.sans,
      color: T_EN.ink,
    }}
  >
    <div style={{ fontFamily: T_EN.mono, fontSize: 15, color, fontWeight: 700 }}>{tag}</div>
    <div style={{ fontSize: 30, fontWeight: 800, lineHeight: 1.18 }}>{title}</div>
    <div style={{ fontFamily: T_EN.mono, fontSize: 20, color: T_EN.muted }}>{highlight}</div>
  </div>
);

const S1HookV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 16, stiffness: 140 } });

  return (
    <AbsoluteFill style={{ fontFamily: T_EN.sans, color: T_EN.ink }}>
      {/* Below the 545px Hero Video (top 156..701) -> start cards at top 730 down to bottom 360 */}
      <div
        style={{
          position: 'absolute',
          top: 730,
          left: 56,
          right: 88,
          display: 'flex',
          flexDirection: 'column',
          gap: 24,
        }}
      >
        <div
          style={{
            display: 'inline-flex',
            alignSelf: 'flex-start',
            padding: '10px 18px',
            borderRadius: 12,
            background: 'rgba(245, 158, 11, 0.12)',
            border: '1px solid rgba(245, 158, 11, 0.45)',
            color: '#FCD34D',
            fontSize: 22,
            fontWeight: 600,
            opacity: enter,
          }}
        >
          Q: 3 Gemini 4 releases in 8 days — which one should you pick?
        </div>

        <div
          style={{
            fontSize: 56,
            lineHeight: 1.14,
            fontWeight: 800,
            letterSpacing: '-0.02em',
            transform: `translateY(${interpolate(enter, [0, 1], [14, 0])}px)`,
            opacity: enter,
          }}
        >
          <span style={{ color: T_EN.amber }}>Google</span> Dropped 3 <span style={{ color: T_EN.amber }}>Gemini 4</span> Models
          <br />
          Stop Guessing <span style={{ fontFamily: T_EN.mono, color: T_EN.amber }}>27</span> Tiers
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          {[
            { date: 'Nov 10', sym: 'C', name: 'Carbon', sub: 'Heavy Tank · 8%', color: T_EN.red, border: 'rgba(229, 72, 77, 0.5)', bg: T_EN.panel, delay: 8 },
            { date: 'Nov 12', sym: 'H', name: 'Hydrogen', sub: 'Speed · 15%', color: T_EN.green, border: 'rgba(34, 197, 94, 0.5)', bg: T_EN.panel, delay: 14 },
            { date: 'Nov 18', sym: 'Ne', name: 'Neon ★', sub: 'Daily · 75%', color: T_EN.amber, border: 'rgba(245, 158, 11, 0.7)', bg: 'rgba(245, 158, 11, 0.09)', delay: 20 },
          ].map((el) => {
            const sp = spring({ frame: Math.max(0, frame - el.delay), fps, config: { damping: 14, stiffness: 150 } });
            return (
              <div
                key={el.sym}
                style={{
                  padding: '20px',
                  borderRadius: 16,
                  background: el.bg,
                  border: `1px solid ${el.border}`,
                  opacity: sp,
                  transform: `translateY(${interpolate(sp, [0, 1], [18, 0])}px)`,
                }}
              >
                <div style={{ fontSize: 16, color: T_EN.muted, fontFamily: T_EN.mono }}>{el.date}</div>
                <div style={{ fontSize: 48, fontWeight: 800, color: el.color, margin: '6px 0 4px' }}>{el.sym}</div>
                <div style={{ fontSize: 24, fontWeight: 800 }}>{el.name}</div>
                <div style={{ fontSize: 18, color: el.sym === 'Ne' ? '#FCD34D' : T_EN.muted, marginTop: 6 }}>{el.sub}</div>
              </div>
            );
          })}
        </div>

        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '18px 24px',
            borderRadius: 16,
            background: '#101520',
            border: '1px solid rgba(229, 72, 77, 0.45)',
            opacity: spring({ frame: Math.max(0, frame - 24), fps, config: { damping: 16 } }),
          }}
        >
          <span style={{ fontSize: 22, fontWeight: 600 }}>Google Antigravity Live Menu</span>
          <span style={{ fontSize: 26, fontWeight: 800, color: T_EN.amber, fontFamily: T_EN.mono }}>11 Groups / 27 Tiers</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S2LanesV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ fontFamily: T_EN.sans, color: T_EN.ink }}>
      <TopPipAsideCard
        tag="WORKFLOW SPLIT"
        title="Not a Raw Ranking — 3 Distinct Work Lanes"
        highlight="Daily Quota Allocation"
        color={T_EN.amber}
      />
      <div
        style={{
          position: 'absolute',
          top: 430,
          left: 56,
          right: 96,
          display: 'flex',
          flexDirection: 'column',
          gap: 28,
        }}
      >
        <div style={{ fontSize: 44, fontWeight: 800, lineHeight: 1.18 }}>
          Where Your <span style={{ color: T_EN.amber }}>Gemini 4</span> Workload Actually Goes
        </div>
        <div style={{ background: T_EN.panel, border: `1px solid ${T_EN.border}`, borderRadius: 20, padding: '34px 32px', display: 'flex', flexDirection: 'column', gap: 36 }}>
          {[
            { label: '10 Ne · Gemini 4 Neon', sub: 'Daily coding, planning & Q&A driver', pct: 75, color: T_EN.amber, delay: 4 },
            { label: '01 H · Gemini 4 Hydrogen', sub: 'Quick scripts, unit tests & doc updates', pct: 15, color: T_EN.green, delay: 12 },
            { label: '06 C · Gemini 4 Carbon', sub: '10+ file refactors & live risk audits', pct: 8, color: T_EN.red, delay: 20 },
          ].map((r) => {
            const p = spring({ frame: Math.max(0, frame - r.delay), fps, config: { damping: 18, stiffness: 110 } });
            return (
              <div key={r.label}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                  <span style={{ fontSize: 30, fontWeight: 800 }}>{r.label}</span>
                  <span style={{ fontFamily: T_EN.mono, fontSize: 34, fontWeight: 800, color: r.color }}>{r.pct}%</span>
                </div>
                <div style={{ fontSize: 21, color: T_EN.muted, marginTop: 6 }}>{r.sub}</div>
                <div style={{ height: 22, background: 'rgba(241, 245, 249, 0.08)', borderRadius: 999, overflow: 'hidden', marginTop: 14 }}>
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

const S3NeonV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fastFill = interpolate(frame, [24, 52], [0, 39], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const slowFill = interpolate(frame, [52, 86], [0, 61], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ fontFamily: T_EN.sans, color: T_EN.ink }}>
      <TopPipAsideCard
        tag="10 Ne · 75% DAILY DRIVER"
        title="Google Gemini 4 Neon"
        highlight="Agent Arena 1336 · $2.82/task"
        color={T_EN.amber}
      />
      <div style={{ position: 'absolute', top: 422, left: 56, right: 96, display: 'flex', flexDirection: 'column', gap: 24 }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 18 }}>
          {[
            { label: 'Coding Index', val: '#1 · 58.6', sub: 'Beats Fable & Opus', color: T_EN.amber, pct: 92, delay: 4 },
            { label: 'vs. Carbon Cost', val: '-32%', sub: 'Zapier #1 (56.3%)', color: T_EN.green, pct: 68, delay: 12 },
            { label: 'Real Speedup', val: '~3.0x', sub: 'No 7–8m waits', color: T_EN.cyan, pct: 85, delay: 20 },
          ].map((m) => {
            const sp = spring({ frame: Math.max(0, frame - m.delay), fps, config: { damping: 16, stiffness: 120 } });
            return (
              <div
                key={m.label}
                style={{
                  background: T_EN.panel,
                  border: `1px solid ${T_EN.border}`,
                  borderRadius: 18,
                  padding: '24px 20px',
                  opacity: sp,
                  transform: `translateY(${interpolate(sp, [0, 1], [16, 0])}px)`,
                }}
              >
                <div style={{ fontSize: 19, color: T_EN.muted }}>{m.label}</div>
                <div style={{ fontSize: 44, fontWeight: 800, fontFamily: T_EN.mono, color: m.color, margin: '10px 0 6px' }}>{m.val}</div>
                <div style={{ fontSize: 17, color: T_EN.ink }}>{m.sub}</div>
                <div style={{ height: 10, background: 'rgba(241, 245, 249, 0.08)', borderRadius: 999, overflow: 'hidden', marginTop: 14 }}>
                  <div style={{ height: '100%', width: `${m.pct * sp}%`, background: m.color, borderRadius: 999 }} />
                </div>
              </div>
            );
          })}
        </div>

        <div
          style={{
            borderRadius: 20,
            padding: '30px 30px',
            border: '1.5px solid rgba(229, 72, 77, 0.5)',
            background: 'rgba(24, 18, 22, 0.94)',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
            <span style={{ fontSize: 28, fontWeight: 800, color: '#FCA5A5' }}>⚠ CONTEXT REDLINE</span>
            <span style={{ fontFamily: T_EN.mono, fontSize: 22, color: T_EN.muted }}>512K Hard Cap</span>
          </div>
          <div style={{ fontSize: 26, fontWeight: 700, marginBottom: 22 }}>
            Latency spikes hard once a single chat crosses <span style={{ color: T_EN.red, fontFamily: T_EN.mono }}>200K</span> tokens
          </div>
          <div style={{ position: 'relative', height: 26, background: '#1E2533', borderRadius: 999, marginBottom: 16, overflow: 'hidden' }}>
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
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 20, fontFamily: T_EN.mono }}>
            <span style={{ color: T_EN.green }}>0–200K · Fast Zone</span>
            <span style={{ color: T_EN.red, fontWeight: 700 }}>▲ Reset Chat Here</span>
            <span style={{ color: T_EN.muted }}>512K</span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S4CarbonV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = spring({ frame, fps, config: { damping: 16, stiffness: 130 } });
  const secs = Math.round(interpolate(frame, [8, 84], [0, 450], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const mm = String(Math.floor(secs / 60)).padStart(2, '0');
  const ss = String(secs % 60).padStart(2, '0');

  return (
    <AbsoluteFill style={{ fontFamily: T_EN.sans, color: T_EN.ink }}>
      <TopPipAsideCard
        tag="06 C · 8% HEAVY TANK"
        title="Google Gemini 4 Carbon"
        highlight="CursorBench 4.0 · WANDR #1"
        color={T_EN.red}
      />
      <div style={{ position: 'absolute', top: 422, left: 56, right: 96, display: 'flex', flexDirection: 'column', gap: 26, opacity: sp }}>
        <div style={{ background: T_EN.panel, border: '1.5px solid rgba(229,72,77,0.55)', borderRadius: 20, padding: '32px 32px' }}>
          <div style={{ fontSize: 42, fontWeight: 800, lineHeight: 1.18, marginBottom: 18 }}>
            Deepest Debugger — Never Use for Quick Edits
          </div>
          <div style={{ fontSize: 25, color: T_EN.muted, lineHeight: 1.65 }}>
            • CursorBench 4.0 / WANDR #1 · Text Arena 1526
            <br />• Exhaustive repo search &amp; multi-pass self-checks
            <br />• <strong style={{ color: T_EN.ink }}>Save strictly for: 10+ file refactors &amp; live risk kernels</strong>
          </div>
        </div>

        <div style={{ background: '#1C1419', border: `2px solid ${T_EN.red}`, borderRadius: 20, padding: '36px 32px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <div style={{ fontSize: 24, color: '#FCA5A5', fontWeight: 700 }}>TINY-EDIT WAIT TIME</div>
            <div style={{ fontSize: 22, color: T_EN.muted, marginTop: 8 }}>Overkill latency on small fixes</div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontFamily: T_EN.mono, fontSize: 82, fontWeight: 800, color: T_EN.red, lineHeight: 1 }}>{mm}:{ss}</div>
            <div style={{ fontSize: 20, color: T_EN.muted, marginTop: 8 }}>7–8 min baseline</div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S5HydrogenV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cardSp = spring({ frame, fps, config: { damping: 16, stiffness: 130 } });
  const lockSp = spring({ frame: Math.max(0, frame - 28), fps, config: { damping: 14, stiffness: 160 } });

  return (
    <AbsoluteFill style={{ fontFamily: T_EN.sans, color: T_EN.ink }}>
      <TopPipAsideCard
        tag="01 H · 15% SPEED RUNNER"
        title="Google Gemini 4 Hydrogen"
        highlight="2.5x Faster vs. 3.8 Flash"
        color={T_EN.green}
      />
      <div style={{ position: 'absolute', top: 422, left: 56, right: 96, display: 'flex', flexDirection: 'column', gap: 26, opacity: cardSp }}>
        <div style={{ background: T_EN.panel, border: '1.5px solid rgba(34,197,94,0.55)', borderRadius: 20, padding: '32px 32px' }}>
          <div style={{ fontSize: 42, fontWeight: 800, lineHeight: 1.18, marginBottom: 18 }}>
            <span style={{ fontFamily: T_EN.mono, color: T_EN.green }}>2.5x</span> Faster Than 3.8 Flash · Done in Seconds
          </div>
          <div style={{ fontSize: 25, color: T_EN.muted, lineHeight: 1.65 }}>
            • Use <strong style={{ color: T_EN.ink }}>High</strong> directly for scripts, unit tests &amp; docs
            <br />• Also powers the execution layer inside Orchestrator
          </div>
        </div>

        <div
          style={{
            background: '#1C1419',
            border: `2px solid ${T_EN.red}`,
            borderRadius: 20,
            padding: '32px 32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            transform: `scale(${interpolate(lockSp, [0, 1], [1.08, 1])})`,
            opacity: lockSp,
          }}
        >
          <div>
            <div style={{ fontSize: 22, color: '#FCA5A5', fontWeight: 700 }}>⛔ NEVER RUN SOLO</div>
            <div style={{ fontSize: 24, color: T_EN.ink, marginTop: 8 }}>Hits 60s Idle Stream EOF</div>
          </div>
          <div style={{ fontFamily: T_EN.mono, fontSize: 46, fontWeight: 800, color: T_EN.red }}>Extra (XHigh)</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S6FormulaV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const stampSp = spring({ frame: Math.max(0, frame - 28), fps, config: { damping: 14, stiffness: 170 } });

  return (
    <AbsoluteFill style={{ fontFamily: T_EN.sans, color: T_EN.ink }}>
      <TopPipAsideCard
        tag="ZERO-FOMO PLAYBOOK"
        title="Default Stack & Release Audit"
        highlight="Fresh Chat <200K · Pool B Guard"
        color={T_EN.amber}
      />
      <div style={{ position: 'absolute', top: 416, left: 56, right: 96, display: 'flex', flexDirection: 'column', gap: 18 }}>
        <div style={{ background: T_EN.panel, border: `1px solid ${T_EN.border}`, borderRadius: 18, padding: '22px 24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
            <span style={{ fontSize: 26, fontWeight: 800 }}>
              Gold Formula: <span style={{ color: T_EN.amber }}>Orchestrator (Neon)</span>
            </span>
            <span style={{ fontFamily: T_EN.mono, fontSize: 16, color: T_EN.green, padding: '4px 12px', borderRadius: 999, border: `1px solid ${T_EN.green}`, background: 'rgba(34,197,94,0.12)' }}>
              &lt;200K Reset
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <div style={{ flex: 1, padding: '14px 18px', borderRadius: 12, background: T_EN.panel2, border: '1px solid rgba(245, 158, 11, 0.5)' }}>
              <div style={{ fontFamily: T_EN.mono, fontSize: 14, color: T_EN.amber }}>1 · PLANNER</div>
              <div style={{ fontSize: 24, fontWeight: 800, marginTop: 4 }}>Neon (High)</div>
            </div>
            <div style={{ fontSize: 30, color: T_EN.amber, fontWeight: 800 }}>➔</div>
            <div style={{ flex: 1, padding: '14px 18px', borderRadius: 12, background: T_EN.panel2, border: '1px solid rgba(34, 197, 94, 0.5)' }}>
              <div style={{ fontFamily: T_EN.mono, fontSize: 14, color: T_EN.green }}>2 · EXECUTOR</div>
              <div style={{ fontSize: 24, fontWeight: 800, marginTop: 4 }}>Hydrogen (High)</div>
            </div>
          </div>
        </div>

        <div
          style={{
            borderRadius: 18,
            padding: '18px 24px',
            border: `2px solid ${T_EN.red}`,
            background: 'rgba(229, 72, 77, 0.10)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            opacity: stampSp,
          }}
        >
          <div>
            <div style={{ fontFamily: T_EN.mono, fontSize: 14, color: '#FCA5A5' }}>POOL B · ISOLATED QUOTA</div>
            <div style={{ fontSize: 28, fontWeight: 800, marginTop: 2 }}>Claude Opus 5.5</div>
          </div>
          <div style={{ fontSize: 19, textAlign: 'right', lineHeight: 1.35 }}>
            Final release
            <br />
            <strong style={{ color: T_EN.red }}>Opus Audit</strong>
          </div>
        </div>

        <div style={{ background: T_EN.panel, border: `1px solid ${T_EN.border}`, borderRadius: 18, padding: '18px 22px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 18 }}>
            <thead>
              <tr>
                {['Model Tier', 'Share', 'Role', 'Redline'].map((h) => (
                  <th key={h} style={{ textAlign: 'left', color: T_EN.muted, fontSize: 14, fontWeight: 600, paddingBottom: 10, borderBottom: `1px solid ${T_EN.border}` }}>
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[
                { name: 'Neon', color: T_EN.amber, pct: '75%', role: 'Coding #1 · ~3x', red: '>200K slows' },
                { name: 'Hydrogen', color: T_EN.green, pct: '15%', role: '2.5x quick scripts', red: 'No solo Extra' },
                { name: 'Carbon', color: T_EN.red, pct: '8%', role: '10+ file / risk', red: '7–8m min wait' },
                { name: 'Argon', color: T_EN.cyan, pct: '2%', role: '1M repo overview', red: 'Use Neon daily' },
              ].map((row, idx) => (
                <tr key={row.name}>
                  <td style={{ padding: '10px 8px 10px 0', borderBottom: idx < 3 ? '1px solid rgba(241,245,249,0.06)' : 'none', fontWeight: 800, color: row.color }}>{row.name}</td>
                  <td style={{ padding: '10px 8px 10px 0', borderBottom: idx < 3 ? '1px solid rgba(241,245,249,0.06)' : 'none', fontFamily: T_EN.mono, fontWeight: 700, color: row.color }}>{row.pct}</td>
                  <td style={{ padding: '10px 8px 10px 0', borderBottom: idx < 3 ? '1px solid rgba(241,245,249,0.06)' : 'none' }}>{row.role}</td>
                  <td style={{ padding: '10px 0', borderBottom: idx < 3 ? '1px solid rgba(241,245,249,0.06)' : 'none', color: idx < 3 ? '#FCA5A5' : T_EN.muted }}>{row.red}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const SCENES_V: Record<string, React.FC> = {
  s1: S1HookV,
  s2: S2LanesV,
  s3: S3NeonV,
  s4: S4CarbonV,
  s5: S5HydrogenV,
  s6: S6FormulaV,
};

export const MainENVertical: React.FC = () => {
  const frame = useCurrentFrame();
  const active = SHOTS_EN.find((s) => frame >= s.start && frame < s.end) ?? SHOTS_EN[SHOTS_EN.length - 1];

  return (
    <AbsoluteFill>
      <DotGridBackdropV />
      <Audio src={staticFile('voice_en_brian_mix.mp3')} />
      <TopBarVertical chapter={active.chapter} />
      {SHOTS_EN.map((shot) => {
        const Scene = SCENES_V[shot.id];
        return (
          <Sequence key={shot.id} from={shot.start} durationInFrames={shot.end - shot.start}>
            <Scene />
          </Sequence>
        );
      })}
      <PersistentAvatarLayerVertical badge={active.badge} />
      <SubtitleBarVertical text={active.subtitle} />
    </AbsoluteFill>
  );
};
