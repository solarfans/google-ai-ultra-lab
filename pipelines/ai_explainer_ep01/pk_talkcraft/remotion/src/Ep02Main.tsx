import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { SHOTS_EP02, T_EP02 } from './theme_ep02';

const STARS = Array.from({ length: 48 }, (_, i) => ({
  x: ((i * 197 + 31) % 100),
  y: ((i * 293 + 17) % 100),
  r: (i % 3) + 1.2,
  phase: i * 0.65,
}));

export const CosmicStarfield: React.FC = () => {
  const frame = useCurrentFrame();
  const driftY = (frame * 0.14) % 1080;

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 22% 18%, rgba(167, 139, 250, 0.16), transparent 46%),
                     radial-gradient(circle at 82% 76%, rgba(96, 165, 250, 0.12), transparent 44%),
                     linear-gradient(155deg, ${T_EP02.bg0} 0%, ${T_EP02.bg1} 55%, #070916 100%)`,
      }}
    >
      {STARS.map((s, idx) => {
        const twinkle = 0.25 + 0.55 * (0.5 + 0.5 * Math.sin(frame * 0.08 + s.phase));
        const yPct = (s.y + (driftY / 1080) * 18) % 100;
        return (
          <div
            key={idx}
            style={{
              position: 'absolute',
              left: `${s.x}%`,
              top: `${yPct}%`,
              width: s.r * 2,
              height: s.r * 2,
              borderRadius: 999,
              background: idx % 5 === 0 ? '#DDD6FE' : '#E2E8F0',
              opacity: twinkle,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

const CoverPoster16x9: React.FC = () => (
  <AbsoluteFill
    style={{
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: T_EP02.sans,
      zIndex: 50,
    }}
  >
    <div
      style={{
        width: 560,
        height: 960,
        borderRadius: 28,
        background: 'linear-gradient(165deg, #131636 0%, #090B1A 100%)',
        border: '2px solid rgba(167, 139, 250, 0.5)',
        boxShadow: '0 32px 90px rgba(0, 0, 0, 0.85)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '44px 36px',
        textAlign: 'center',
        gap: 24,
      }}
    >
      <div
        style={{
          fontFamily: T_EP02.mono,
          fontSize: 20,
          fontWeight: 700,
          padding: '8px 20px',
          borderRadius: 999,
          background: 'rgba(96, 165, 250, 0.16)',
          border: '1px solid rgba(96, 165, 250, 0.5)',
          color: '#93C5FD',
        }}
      >
        GEMINI TASKS · ULTRA 20X
      </div>
      <div style={{ fontSize: 78, fontWeight: 900, lineHeight: 1.02, letterSpacing: '-0.03em', color: T_EP02.ink }}>
        GOOGLE&apos;S
        <br />
        <span style={{ color: T_EP02.blue }}>FREE AI</span>
        <br />
        AGENT
      </div>
      <div style={{ fontSize: 32, fontWeight: 700, fontStyle: 'italic', color: T_EP02.lavender }}>
        vs. ChatGPT Dots
      </div>
      <div
        style={{
          width: '100%',
          padding: '22px 24px',
          borderRadius: 18,
          background: 'rgba(251, 113, 133, 0.14)',
          border: '2px solid rgba(251, 113, 133, 0.65)',
          fontSize: 28,
          fontWeight: 800,
          color: '#FDA4AF',
        }}
      >
        THE 90-MIN ULTRA CATCH
      </div>
      <div style={{ fontFamily: T_EP02.mono, fontSize: 19, color: T_EP02.muted }}>
        50 Schedules · 15 Parallel · Hybrid Playbook
      </div>
    </div>
  </AbsoluteFill>
);

const TopBreadCrumb: React.FC<{ pill: string; chapter: string }> = ({ pill, chapter }) => (
  <div
    style={{
      position: 'absolute',
      top: 36,
      left: 72,
      right: 72,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      zIndex: 20,
      fontFamily: T_EP02.mono,
    }}
  >
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 10,
        padding: '8px 18px',
        borderRadius: 999,
        background: T_EP02.glass,
        border: `1px solid ${T_EP02.glassBorder}`,
        fontSize: 16,
        color: T_EP02.ink,
      }}
    >
      <span style={{ width: 9, height: 9, borderRadius: 999, background: T_EP02.emerald, display: 'inline-block' }} />
      <span>{pill}</span>
    </div>
    <div style={{ fontSize: 16, color: T_EP02.muted }}>{chapter}</div>
  </div>
);

const CaptionBar: React.FC<{ text: string }> = ({ text }) => (
  <div
    style={{
      position: 'absolute',
      left: 96,
      right: 96,
      bottom: 36,
      display: 'flex',
      justifyContent: 'center',
      zIndex: 40,
      fontFamily: T_EP02.sans,
    }}
  >
    <span
      style={{
        display: 'inline-block',
        maxWidth: 1500,
        padding: '10px 24px',
        borderRadius: 12,
        background: 'rgba(9, 11, 26, 0.84)',
        border: '1px solid rgba(248, 250, 252, 0.14)',
        fontSize: 23,
        fontWeight: 600,
        color: T_EP02.ink,
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
  const f = Math.max(0, frame - 12);
  const titleSp = spring({ frame: f, fps, config: { damping: 16, stiffness: 130 } });
  const cardSp = spring({ frame: Math.max(0, f - 18), fps, config: { damping: 15, stiffness: 140 } });

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: T_EP02.sans, color: T_EP02.ink }}>
      <div style={{ textAlign: 'center', maxWidth: 1380, padding: '0 64px', opacity: titleSp }}>
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 10,
            padding: '10px 22px',
            borderRadius: 999,
            background: 'rgba(52, 211, 153, 0.14)',
            border: '1px solid rgba(52, 211, 153, 0.5)',
            color: T_EP02.emerald,
            fontFamily: T_EP02.mono,
            fontSize: 20,
            fontWeight: 700,
            marginBottom: 28,
          }}
        >
          <span>●</span>
          <span>NOV 2026 REBRAND · CLOUD AGENT ACTIVE</span>
        </div>

        <div
          style={{
            fontSize: 82,
            fontWeight: 900,
            lineHeight: 1.1,
            letterSpacing: '-0.03em',
            transform: `translateY(${interpolate(titleSp, [0, 1], [24, 0])}px)`,
          }}
        >
          <span style={{ color: T_EP02.muted, textDecoration: 'line-through', textDecorationColor: T_EP02.coral }}>
            Gemini Spark
          </span>{' '}
          <span style={{ color: T_EP02.lavender }}>➔</span>{' '}
          <span style={{ color: T_EP02.blue }}>Gemini Tasks</span>
        </div>

        <div
          style={{
            marginTop: 34,
            display: 'inline-block',
            padding: '22px 40px',
            borderRadius: 20,
            background: T_EP02.glass,
            border: `1px solid ${T_EP02.glassBorder}`,
            fontSize: 34,
            fontWeight: 700,
            transform: `scale(${interpolate(cardSp, [0, 1], [0.92, 1])})`,
            opacity: cardSp,
          }}
        >
          Autonomous Cloud Agent · <span style={{ color: T_EP02.emerald }}>Works While Your Phone Is Locked</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S2HowItWorks: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const winSp = spring({ frame, fps, config: { damping: 16, stiffness: 120 } });
  const flipped = frame >= 24;
  const splitSp = spring({ frame: Math.max(0, frame - 42), fps, config: { damping: 16, stiffness: 130 } });

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: T_EP02.sans, color: T_EP02.ink }}>
      <div
        style={{
          width: 1480,
          borderRadius: 24,
          background: T_EP02.glass,
          border: '1.5px solid rgba(167, 139, 250, 0.38)',
          boxShadow: '0 30px 80px rgba(0,0,0,0.6)',
          overflow: 'hidden',
          transform: `translateY(${interpolate(winSp, [0, 1], [28, 0])}px)`,
          opacity: winSp,
        }}
      >
        <div
          style={{
            height: 52,
            background: 'rgba(255,255,255,0.04)',
            borderBottom: `1px solid ${T_EP02.glassBorder}`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '0 24px',
          }}
        >
          <div style={{ display: 'flex', gap: 10 }}>
            <span style={{ width: 13, height: 13, borderRadius: 999, background: '#FB7185' }} />
            <span style={{ width: 13, height: 13, borderRadius: 999, background: '#FBBF24' }} />
            <span style={{ width: 13, height: 13, borderRadius: 999, background: '#34D399' }} />
          </div>
          <span style={{ fontFamily: T_EP02.mono, fontSize: 16, color: T_EP02.muted }}>gemini.google.com · Mode Switch</span>
          <span style={{ fontFamily: T_EP02.mono, fontSize: 14, color: T_EP02.emerald }}>GEMINI 4 HYDROGEN</span>
        </div>

        <div style={{ padding: '38px 48px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 34 }}>
            <div style={{ fontSize: 40, fontWeight: 800 }}>
              One Toggle Turns <span style={{ color: T_EP02.muted }}>Chat</span> Into <span style={{ color: T_EP02.blue }}>Execution</span>
            </div>
            <div
              style={{
                display: 'inline-flex',
                padding: 6,
                borderRadius: 999,
                background: '#090B1A',
                border: `1px solid ${T_EP02.glassBorder}`,
                gap: 6,
                fontSize: 20,
                fontWeight: 700,
              }}
            >
              <span style={{ padding: '10px 26px', borderRadius: 999, color: flipped ? T_EP02.muted : T_EP02.ink, background: flipped ? 'transparent' : 'rgba(255,255,255,0.1)' }}>
                Chat
              </span>
              <span
                style={{
                  padding: '10px 28px',
                  borderRadius: 999,
                  color: flipped ? '#090B1A' : T_EP02.muted,
                  background: flipped ? T_EP02.blue : 'transparent',
                  boxShadow: flipped ? '0 0 28px rgba(96, 165, 250, 0.55)' : 'none',
                }}
              >
                ✦ Task
              </span>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 28, opacity: splitSp }}>
            <div style={{ padding: '30px 32px', borderRadius: 18, background: 'rgba(96, 165, 250, 0.08)', border: '1px solid rgba(96, 165, 250, 0.4)' }}>
              <div style={{ fontFamily: T_EP02.mono, fontSize: 16, color: T_EP02.blue, fontWeight: 700 }}>PATH A · CLOUD SANDBOX</div>
              <div style={{ fontSize: 32, fontWeight: 800, margin: '10px 0 12px' }}>Isolated Cloud VM + Remote Browser</div>
              <div style={{ fontSize: 21, color: T_EP02.muted, lineHeight: 1.55 }}>
                Runs research, code, files, and multi-step browsing in Google&apos;s cloud even when your laptop is shut.
              </div>
            </div>

            <div style={{ padding: '30px 32px', borderRadius: 18, background: 'rgba(167, 139, 250, 0.08)', border: '1px solid rgba(167, 139, 250, 0.4)' }}>
              <div style={{ fontFamily: T_EP02.mono, fontSize: 16, color: T_EP02.lavender, fontWeight: 700 }}>PATH B · DESKTOP HANDOFF</div>
              <div style={{ fontSize: 32, fontWeight: 800, margin: '10px 0 12px' }}>Chrome Auto Browse + Mac App</div>
              <div style={{ fontSize: 21, color: T_EP02.muted, lineHeight: 1.55 }}>
                Operates your signed-in Chrome tabs or Apple Silicon Mac background windows while leaving your cursor free.
              </div>
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S3Tiers: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const leftSp = spring({ frame, fps, config: { damping: 16, stiffness: 130 } });
  const rightSp = spring({ frame: Math.max(0, frame - 18), fps, config: { damping: 16, stiffness: 130 } });
  const pillSp = spring({ frame: Math.max(0, frame - 48), fps, config: { damping: 16, stiffness: 130 } });

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: T_EP02.sans, color: T_EP02.ink }}>
      <div style={{ width: 1480, display: 'flex', flexDirection: 'column', gap: 28 }}>
        <div style={{ fontSize: 54, fontWeight: 900, textAlign: 'center' }}>
          Free Tier vs. <span style={{ color: T_EP02.amber }}>Google AI Pro &amp; Ultra</span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.25fr', gap: 28 }}>
          <div style={{ background: T_EP02.glass, border: `1px solid ${T_EP02.glassBorder}`, borderRadius: 20, padding: '34px 36px', opacity: leftSp }}>
            <div style={{ fontFamily: T_EP02.mono, fontSize: 17, color: T_EP02.muted }}>FREE · 6 COUNTRIES ONLY</div>
            <div style={{ fontSize: 20, color: T_EP02.muted, marginTop: 6 }}>US, Canada, India, Japan, Korea, Australia</div>
            <div style={{ fontSize: 74, fontWeight: 900, fontFamily: T_EP02.mono, color: T_EP02.ink, margin: '18px 0 8px' }}>10</div>
            <div style={{ fontSize: 26, fontWeight: 700 }}>Active Daily Schedules</div>
            <div style={{ fontSize: 20, color: T_EP02.muted, marginTop: 10 }}>Once per day · Broad morning/day/evening window</div>
          </div>

          <div
            style={{
              background: 'rgba(251, 191, 36, 0.08)',
              border: '2px solid rgba(251, 191, 36, 0.55)',
              borderRadius: 20,
              padding: '34px 36px',
              opacity: rightSp,
            }}
          >
            <div style={{ fontFamily: T_EP02.mono, fontSize: 17, color: T_EP02.amber, fontWeight: 700 }}>PRO &amp; ULTRA 20X · GLOBAL ELIGIBLE</div>
            <div style={{ display: 'flex', gap: 48, margin: '18px 0 10px' }}>
              <div>
                <div style={{ fontSize: 74, fontWeight: 900, fontFamily: T_EP02.mono, color: T_EP02.amber }}>50</div>
                <div style={{ fontSize: 24, fontWeight: 700 }}>Active Schedules</div>
              </div>
              <div>
                <div style={{ fontSize: 74, fontWeight: 900, fontFamily: T_EP02.mono, color: T_EP02.emerald }}>15</div>
                <div style={{ fontSize: 24, fontWeight: 700 }}>Parallel Tasks</div>
              </div>
            </div>
            <div style={{ fontSize: 20, color: '#FDE68A' }}>Included in Singapore &amp; most non-EEA/UK markets</div>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 20, opacity: pillSp }}>
          {[
            { tag: 'TRIGGER 1', name: 'Exact & Hourly Timers', color: T_EP02.blue },
            { tag: 'TRIGGER 2', name: 'Gmail Event Monitors', color: T_EP02.emerald },
            { tag: 'TRIGGER 3', name: 'Topic & News Monitors', color: T_EP02.lavender },
          ].map((t) => (
            <div
              key={t.tag}
              style={{
                background: T_EP02.glass,
                border: `1px solid ${T_EP02.glassBorder}`,
                borderRadius: 16,
                padding: '20px 24px',
                display: 'flex',
                flexDirection: 'column',
                gap: 6,
              }}
            >
              <span style={{ fontFamily: T_EP02.mono, fontSize: 15, color: t.color, fontWeight: 700 }}>{t.tag}</span>
              <span style={{ fontSize: 24, fontWeight: 800 }}>{t.name}</span>
            </div>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S4VsDots: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const b1 = spring({ frame, fps, config: { damping: 16, stiffness: 110 } });
  const b2 = spring({ frame: Math.max(0, frame - 20), fps, config: { damping: 16, stiffness: 110 } });
  const badgeSp = spring({ frame: Math.max(0, frame - 42), fps, config: { damping: 14, stiffness: 150 } });

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: T_EP02.sans, color: T_EP02.ink }}>
      <div style={{ width: 1460, display: 'flex', flexDirection: 'column', gap: 28 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ fontSize: 52, fontWeight: 900 }}>
            <span style={{ color: T_EP02.blue }}>Gemini Tasks</span> vs. <span style={{ color: T_EP02.lavender }}>ChatGPT Dots</span>
          </div>
          <span
            style={{
              fontFamily: T_EP02.mono,
              fontSize: 19,
              fontWeight: 800,
              padding: '10px 20px',
              borderRadius: 999,
              background: 'rgba(52, 211, 153, 0.16)',
              border: `1px solid ${T_EP02.emerald}`,
              color: T_EP02.emerald,
              opacity: badgeSp,
            }}
          >
            $0 EXTRA IF ON PRO / ULTRA
          </span>
        </div>

        <div style={{ background: T_EP02.glass, border: `1px solid ${T_EP02.glassBorder}`, borderRadius: 22, padding: '36px 40px', display: 'flex', flexDirection: 'column', gap: 32 }}>
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 28, fontWeight: 800, marginBottom: 12 }}>
              <span>✦ Google Gemini Tasks</span>
              <span style={{ fontFamily: T_EP02.mono, color: T_EP02.emerald }}>$0–$19.99/mo · Gmail + Drive + Chrome</span>
            </div>
            <div style={{ height: 26, background: 'rgba(255,255,255,0.08)', borderRadius: 999, overflow: 'hidden' }}>
              <div style={{ height: '100%', width: `${30 * b1}%`, background: `linear-gradient(90deg, ${T_EP02.blue}, ${T_EP02.emerald})`, borderRadius: 999 }} />
            </div>
            <div style={{ fontSize: 19, color: T_EP02.muted, marginTop: 8 }}>Best for Google Workspace triggers, Sheets/Docs output, and single-account workflows</div>
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 28, fontWeight: 800, marginBottom: 12 }}>
              <span>◎ OpenAI ChatGPT Dots</span>
              <span style={{ fontFamily: T_EP02.mono, color: T_EP02.lavender }}>$100/mo Pro · $150/mo Business Min</span>
            </div>
            <div style={{ height: 26, background: 'rgba(255,255,255,0.08)', borderRadius: 999, overflow: 'hidden' }}>
              <div style={{ height: '100%', width: `${92 * b2}%`, background: 'rgba(167, 139, 250, 0.72)', borderRadius: 999 }} />
            </div>
            <div style={{ fontSize: 19, color: T_EP02.muted, marginTop: 8 }}>Stronger for Slack / Teams collaboration and persistent cross-app cloud projects</div>
          </div>
        </div>

        <div style={{ alignSelf: 'center', fontFamily: T_EP02.mono, fontSize: 17, padding: '8px 20px', borderRadius: 999, background: T_EP02.glass, border: `1px solid ${T_EP02.glassBorder}`, color: T_EP02.muted }}>
          Verified against Google Support &amp; OpenAI Pricing · Nov 2026
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S5Catch: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const meterPct = interpolate(frame, [16, 110], [18, 100], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const strikePct = interpolate(frame, [8, 28], [0, 100], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const proofSp = spring({ frame: Math.max(0, frame - 55), fps, config: { damping: 14, stiffness: 140 } });

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: T_EP02.sans, color: T_EP02.ink }}>
      <div style={{ width: 1380, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 30, textAlign: 'center' }}>
        <div style={{ fontSize: 72, fontWeight: 900, lineHeight: 1.08 }}>
          The <span style={{ color: T_EP02.coral }}>Hidden Catch</span>
        </div>

        <div style={{ position: 'relative', display: 'inline-block', fontSize: 42, fontWeight: 700, color: T_EP02.muted }}>
          <span>&ldquo;Unlimited 24/7 Cloud Agents&rdquo;</span>
          <div
            style={{
              position: 'absolute',
              left: 0,
              top: '52%',
              height: 6,
              width: `${strikePct}%`,
              background: T_EP02.coral,
              borderRadius: 999,
            }}
          />
        </div>

        <div style={{ width: '100%', background: 'rgba(251, 113, 133, 0.08)', border: `2px solid ${T_EP02.coral}`, borderRadius: 22, padding: '32px 40px', textAlign: 'left' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: T_EP02.mono, fontSize: 22, fontWeight: 700, marginBottom: 14 }}>
            <span style={{ color: '#FDA4AF' }}>5-HOUR ROLLING COMPUTE WEIGHT POOL</span>
            <span style={{ color: T_EP02.coral }}>{Math.round(meterPct)}% USED</span>
          </div>
          <div style={{ height: 28, background: 'rgba(255,255,255,0.08)', borderRadius: 999, overflow: 'hidden' }}>
            <div style={{ height: '100%', width: `${meterPct}%`, background: `linear-gradient(90deg, ${T_EP02.amber}, ${T_EP02.coral})`, borderRadius: 999 }} />
          </div>
          <div style={{ marginTop: 22, fontSize: 28, fontWeight: 700, opacity: proofSp }}>
            Real Ultra User Report (Google AI Forum):{' '}
            <span style={{ color: '#FDA4AF' }}>Hit the wall in &lt;90 minutes on just 2 heavy tasks</span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S6Limits: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const c1 = spring({ frame, fps, config: { damping: 16, stiffness: 130 } });
  const c2 = spring({ frame: Math.max(0, frame - 26), fps, config: { damping: 16, stiffness: 130 } });

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: T_EP02.sans, color: T_EP02.ink }}>
      <div style={{ width: 1420, display: 'flex', flexDirection: 'column', gap: 30 }}>
        <div style={{ fontSize: 54, fontWeight: 900, textAlign: 'center' }}>
          Two More <span style={{ color: T_EP02.amber }}>Real-World Boundaries</span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 28 }}>
          <div style={{ background: T_EP02.glass, border: '1.5px solid rgba(251, 191, 36, 0.5)', borderRadius: 22, padding: '36px 38px', opacity: c1 }}>
            <div style={{ fontFamily: T_EP02.mono, fontSize: 17, color: T_EP02.amber, fontWeight: 700 }}>REGION GATE · U.S. ONLY</div>
            <div style={{ fontSize: 36, fontWeight: 800, margin: '12px 0 18px' }}>Locked Outside the U.S.</div>
            <div style={{ fontSize: 23, color: T_EP02.muted, lineHeight: 1.65 }}>
              • Google Duplex live business phone calls
              <br />• Google Pay auto-checkout ($1,000 cap)
              <br />• SMS &amp; email forwarding dispatch
            </div>
          </div>

          <div style={{ background: T_EP02.glass, border: '1.5px solid rgba(251, 113, 133, 0.55)', borderRadius: 22, padding: '36px 38px', opacity: c2 }}>
            <div style={{ fontFamily: T_EP02.mono, fontSize: 17, color: T_EP02.coral, fontWeight: 700 }}>LATENCY DISCLAIMER</div>
            <div style={{ fontSize: 36, fontWeight: 800, margin: '12px 0 18px' }}>Not Built for Instant Drops</div>
            <div style={{ fontSize: 23, color: T_EP02.muted, lineHeight: 1.65 }}>
              • Topic monitors check periodically — never millisecond-fast
              <br />• Google warns against instant ticket drops or trading alerts
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S7Playbook: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp1 = spring({ frame, fps, config: { damping: 16, stiffness: 130 } });
  const sp2 = spring({ frame: Math.max(0, frame - 22), fps, config: { damping: 16, stiffness: 130 } });

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: T_EP02.sans, color: T_EP02.ink }}>
      <div style={{ width: 1440, display: 'flex', flexDirection: 'column', gap: 28 }}>
        <div style={{ fontSize: 56, fontWeight: 900, textAlign: 'center' }}>
          The Winning <span style={{ color: T_EP02.emerald }}>Hybrid Playbook</span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 28 }}>
          <div style={{ background: 'rgba(52, 211, 153, 0.08)', border: '2px solid rgba(52, 211, 153, 0.55)', borderRadius: 22, padding: '36px 38px', opacity: sp1 }}>
            <div style={{ fontFamily: T_EP02.mono, fontSize: 17, color: T_EP02.emerald, fontWeight: 800 }}>SEND TO GEMINI TASKS ($0)</div>
            <div style={{ fontSize: 36, fontWeight: 800, margin: '12px 0 18px' }}>Workspace &amp; Web Sweeps</div>
            <div style={{ fontSize: 23, color: T_EP02.ink, lineHeight: 1.65 }}>
              ✓ Gmail monitors &amp; draft replies
              <br />✓ Topic news digests into Google Sheets
              <br />✓ Scoped travel &amp; Docs packaging
            </div>
          </div>

          <div style={{ background: 'rgba(96, 165, 250, 0.08)', border: '2px solid rgba(96, 165, 250, 0.55)', borderRadius: 22, padding: '36px 38px', opacity: sp2 }}>
            <div style={{ fontFamily: T_EP02.mono, fontSize: 17, color: T_EP02.blue, fontWeight: 800 }}>KEEP ON LOCAL STACK (NO LIMITS)</div>
            <div style={{ fontSize: 36, fontWeight: 800, margin: '12px 0 18px' }}>Code, Bots &amp; Production</div>
            <div style={{ fontSize: 23, color: T_EP02.ink, lineHeight: 1.65 }}>
              ✓ Multi-file engineering &amp; local SQLite
              <br />✓ High-frequency monitors &amp; custom bots
              <br />✓ Deterministic video &amp; media pipelines
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const SCENES_EP02: Record<string, React.FC> = {
  s1: S1Hook,
  s2: S2HowItWorks,
  s3: S3Tiers,
  s4: S4VsDots,
  s5: S5Catch,
  s6: S6Limits,
  s7: S7Playbook,
};

export const Ep02Main: React.FC = () => {
  const frame = useCurrentFrame();
  const active = SHOTS_EP02.find((s) => frame >= s.start && frame < s.end) ?? SHOTS_EP02[SHOTS_EP02.length - 1];
  const isCover = frame < 12;

  return (
    <AbsoluteFill>
      <CosmicStarfield />
      <Audio src={staticFile('voice_ep02_mix.mp3')} />
      {isCover ? (
        <CoverPoster16x9 />
      ) : (
        <>
          <TopBreadCrumb pill={active.pill} chapter={active.chapter} />
          {SHOTS_EP02.map((shot) => {
            const Scene = SCENES_EP02[shot.id];
            return (
              <Sequence key={shot.id} from={shot.start} durationInFrames={shot.end - shot.start}>
                <Scene />
              </Sequence>
            );
          })}
          <CaptionBar text={active.subtitle} />
        </>
      )}
    </AbsoluteFill>
  );
};
