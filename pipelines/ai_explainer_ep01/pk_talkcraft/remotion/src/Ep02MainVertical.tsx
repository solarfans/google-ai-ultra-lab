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
import { CosmicStarfield } from './Ep02Main';
import { SHOTS_EP02, T_EP02 } from './theme_ep02';

const CoverPosterVertical: React.FC = () => (
  <AbsoluteFill
    style={{
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: T_EP02.sans,
      padding: '100px 64px',
      textAlign: 'center',
      zIndex: 50,
    }}
  >
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 36 }}>
      <div
        style={{
          fontFamily: T_EP02.mono,
          fontSize: 28,
          fontWeight: 700,
          padding: '12px 28px',
          borderRadius: 999,
          background: 'rgba(96, 165, 250, 0.16)',
          border: '1.5px solid rgba(96, 165, 250, 0.55)',
          color: '#93C5FD',
        }}
      >
        GEMINI TASKS · ULTRA 20X
      </div>
      <div style={{ fontSize: 122, fontWeight: 900, lineHeight: 1.0, letterSpacing: '-0.03em', color: T_EP02.ink }}>
        GOOGLE&apos;S
        <br />
        <span style={{ color: T_EP02.blue }}>FREE AI</span>
        <br />
        AGENT
      </div>
      <div style={{ fontSize: 48, fontWeight: 700, fontStyle: 'italic', color: T_EP02.lavender }}>
        vs. ChatGPT Dots
      </div>
      <div
        style={{
          padding: '28px 40px',
          borderRadius: 22,
          background: 'rgba(251, 113, 133, 0.16)',
          border: '2px solid rgba(251, 113, 133, 0.65)',
          fontSize: 40,
          fontWeight: 800,
          color: '#FDA4AF',
        }}
      >
        THE 90-MIN ULTRA CATCH
      </div>
      <div style={{ fontFamily: T_EP02.mono, fontSize: 24, color: T_EP02.muted }}>
        50 Schedules · 15 Parallel · Hybrid Playbook
      </div>
    </div>
  </AbsoluteFill>
);

const TopBarV: React.FC<{ pill: string; chapter: string }> = ({ pill, chapter }) => (
  <div
    style={{
      position: 'absolute',
      top: 72,
      left: 56,
      right: 56,
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
        fontSize: 17,
        color: T_EP02.ink,
      }}
    >
      <span style={{ width: 9, height: 9, borderRadius: 999, background: T_EP02.emerald }} />
      <span>{pill}</span>
    </div>
    <div style={{ fontSize: 17, color: '#DDD6FE', fontWeight: 700 }}>{chapter}</div>
  </div>
);

const CaptionBarV: React.FC<{ text: string }> = ({ text }) => (
  <div
    style={{
      position: 'absolute',
      left: 48,
      right: 96,
      bottom: 235,
      display: 'flex',
      justifyContent: 'center',
      zIndex: 40,
      fontFamily: T_EP02.sans,
    }}
  >
    <span
      style={{
        display: 'inline-block',
        maxWidth: 920,
        padding: '12px 24px',
        borderRadius: 14,
        background: 'rgba(9, 11, 26, 0.88)',
        border: '1px solid rgba(248, 250, 252, 0.16)',
        fontSize: 30,
        lineHeight: 1.32,
        fontWeight: 700,
        color: T_EP02.ink,
        textAlign: 'center',
      }}
    >
      {text}
    </span>
  </div>
);

const S1HookV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const f = Math.max(0, frame - 12);
  const titleSp = spring({ frame: f, fps, config: { damping: 16, stiffness: 130 } });
  const cardSp = spring({ frame: Math.max(0, f - 16), fps, config: { damping: 15, stiffness: 140 } });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: '0 96px 140px 56px', fontFamily: T_EP02.sans, color: T_EP02.ink }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 34, opacity: titleSp }}>
        <div
          style={{
            alignSelf: 'flex-start',
            padding: '10px 22px',
            borderRadius: 999,
            background: 'rgba(52, 211, 153, 0.14)',
            border: '1px solid rgba(52, 211, 153, 0.5)',
            color: T_EP02.emerald,
            fontFamily: T_EP02.mono,
            fontSize: 20,
            fontWeight: 700,
          }}
        >
          ● NOV 2026 REBRAND · CLOUD AGENT
        </div>
        <div style={{ fontSize: 78, fontWeight: 900, lineHeight: 1.08, letterSpacing: '-0.03em' }}>
          <span style={{ color: T_EP02.muted, textDecoration: 'line-through', textDecorationColor: T_EP02.coral }}>
            Gemini Spark
          </span>
          <br />
          <span style={{ color: T_EP02.lavender }}>➔</span> <span style={{ color: T_EP02.blue }}>Gemini Tasks</span>
        </div>
        <div
          style={{
            padding: '28px 30px',
            borderRadius: 20,
            background: T_EP02.glass,
            border: `1px solid ${T_EP02.glassBorder}`,
            fontSize: 34,
            fontWeight: 700,
            lineHeight: 1.35,
            opacity: cardSp,
          }}
        >
          Autonomous cloud agent that <span style={{ color: T_EP02.emerald }}>keeps working after you lock your phone</span>.
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S2HowItWorksV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const winSp = spring({ frame, fps, config: { damping: 16, stiffness: 120 } });
  const flipped = frame >= 24;
  const splitSp = spring({ frame: Math.max(0, frame - 40), fps, config: { damping: 16, stiffness: 130 } });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: '0 96px 140px 56px', fontFamily: T_EP02.sans, color: T_EP02.ink }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 26, opacity: winSp }}>
        <div
          style={{
            borderRadius: 22,
            background: T_EP02.glass,
            border: '1.5px solid rgba(167, 139, 250, 0.42)',
            overflow: 'hidden',
          }}
        >
          <div style={{ height: 46, background: 'rgba(255,255,255,0.04)', borderBottom: `1px solid ${T_EP02.glassBorder}`, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 20px' }}>
            <div style={{ display: 'flex', gap: 8 }}>
              <span style={{ width: 11, height: 11, borderRadius: 999, background: '#FB7185' }} />
              <span style={{ width: 11, height: 11, borderRadius: 999, background: '#FBBF24' }} />
              <span style={{ width: 11, height: 11, borderRadius: 999, background: '#34D399' }} />
            </div>
            <span style={{ fontFamily: T_EP02.mono, fontSize: 15, color: T_EP02.muted }}>gemini.google.com</span>
          </div>
          <div style={{ padding: '26px 28px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ fontSize: 32, fontWeight: 800 }}>Flip Mode Toggle</div>
            <div style={{ display: 'inline-flex', padding: 5, borderRadius: 999, background: '#090B1A', border: `1px solid ${T_EP02.glassBorder}`, gap: 6, fontSize: 20, fontWeight: 700 }}>
              <span style={{ padding: '8px 20px', borderRadius: 999, color: flipped ? T_EP02.muted : T_EP02.ink }}>Chat</span>
              <span style={{ padding: '8px 22px', borderRadius: 999, color: flipped ? '#090B1A' : T_EP02.muted, background: flipped ? T_EP02.blue : 'transparent' }}>✦ Task</span>
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 20, opacity: splitSp }}>
          <div style={{ padding: '26px 28px', borderRadius: 20, background: 'rgba(96, 165, 250, 0.09)', border: '1px solid rgba(96, 165, 250, 0.45)' }}>
            <div style={{ fontFamily: T_EP02.mono, fontSize: 16, color: T_EP02.blue, fontWeight: 700 }}>PATH A · CLOUD SANDBOX</div>
            <div style={{ fontSize: 32, fontWeight: 800, marginTop: 8 }}>Isolated Cloud Computer + Remote Browser</div>
          </div>
          <div style={{ padding: '26px 28px', borderRadius: 20, background: 'rgba(167, 139, 250, 0.09)', border: '1px solid rgba(167, 139, 250, 0.45)' }}>
            <div style={{ fontFamily: T_EP02.mono, fontSize: 16, color: T_EP02.lavender, fontWeight: 700 }}>PATH B · DESKTOP HANDOFF</div>
            <div style={{ fontSize: 32, fontWeight: 800, marginTop: 8 }}>Chrome Auto Browse &amp; Mac App Window</div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S3TiersV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp1 = spring({ frame, fps, config: { damping: 16, stiffness: 130 } });
  const sp2 = spring({ frame: Math.max(0, frame - 20), fps, config: { damping: 16, stiffness: 130 } });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: '0 96px 140px 56px', fontFamily: T_EP02.sans, color: T_EP02.ink }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <div style={{ fontSize: 50, fontWeight: 900 }}>
          Free Tier vs. <span style={{ color: T_EP02.amber }}>Pro &amp; Ultra</span>
        </div>

        <div style={{ background: T_EP02.glass, border: `1px solid ${T_EP02.glassBorder}`, borderRadius: 20, padding: '28px 30px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', opacity: sp1 }}>
          <div>
            <div style={{ fontFamily: T_EP02.mono, fontSize: 16, color: T_EP02.muted }}>FREE · 6 COUNTRIES</div>
            <div style={{ fontSize: 28, fontWeight: 800, marginTop: 6 }}>Daily Broad Window</div>
          </div>
          <div style={{ fontSize: 64, fontWeight: 900, fontFamily: T_EP02.mono }}>10</div>
        </div>

        <div style={{ background: 'rgba(251, 191, 36, 0.09)', border: '2px solid rgba(251, 191, 36, 0.55)', borderRadius: 20, padding: '30px 30px', opacity: sp2 }}>
          <div style={{ fontFamily: T_EP02.mono, fontSize: 17, color: T_EP02.amber, fontWeight: 700 }}>PRO &amp; ULTRA 20X · GLOBAL</div>
          <div style={{ display: 'flex', gap: 44, marginTop: 14 }}>
            <div>
              <div style={{ fontSize: 64, fontWeight: 900, fontFamily: T_EP02.mono, color: T_EP02.amber }}>50</div>
              <div style={{ fontSize: 22, fontWeight: 700 }}>Schedules</div>
            </div>
            <div>
              <div style={{ fontSize: 64, fontWeight: 900, fontFamily: T_EP02.mono, color: T_EP02.emerald }}>15</div>
              <div style={{ fontSize: 22, fontWeight: 700 }}>Parallel Tasks</div>
            </div>
          </div>
          <div style={{ marginTop: 18, fontSize: 22, color: '#FDE68A', fontWeight: 600 }}>
            + Exact Timers · Gmail Monitors · Topic Monitors
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S4VsDotsV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const b1 = spring({ frame, fps, config: { damping: 16, stiffness: 110 } });
  const b2 = spring({ frame: Math.max(0, frame - 20), fps, config: { damping: 16, stiffness: 110 } });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: '0 96px 140px 56px', fontFamily: T_EP02.sans, color: T_EP02.ink }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 26 }}>
        <div style={{ fontSize: 48, fontWeight: 900, lineHeight: 1.12 }}>
          <span style={{ color: T_EP02.blue }}>Gemini Tasks</span> vs. <span style={{ color: T_EP02.lavender }}>ChatGPT Dots</span>
        </div>

        <div style={{ background: T_EP02.glass, border: `1px solid ${T_EP02.glassBorder}`, borderRadius: 22, padding: '32px 30px', display: 'flex', flexDirection: 'column', gap: 30 }}>
          <div>
            <div style={{ fontSize: 28, fontWeight: 800 }}>✦ Gemini Tasks</div>
            <div style={{ fontFamily: T_EP02.mono, fontSize: 24, color: T_EP02.emerald, fontWeight: 800, marginTop: 6 }}>$0–$19.99 / Included in Ultra</div>
            <div style={{ height: 22, background: 'rgba(255,255,255,0.08)', borderRadius: 999, overflow: 'hidden', marginTop: 12 }}>
              <div style={{ height: '100%', width: `${30 * b1}%`, background: `linear-gradient(90deg, ${T_EP02.blue}, ${T_EP02.emerald})`, borderRadius: 999 }} />
            </div>
            <div style={{ fontSize: 20, color: T_EP02.muted, marginTop: 8 }}>Native Gmail, Drive, Calendar &amp; Chrome</div>
          </div>

          <div>
            <div style={{ fontSize: 28, fontWeight: 800 }}>◎ ChatGPT Dots</div>
            <div style={{ fontFamily: T_EP02.mono, fontSize: 24, color: T_EP02.lavender, fontWeight: 800, marginTop: 6 }}>$100/mo Pro · $150/mo Business</div>
            <div style={{ height: 22, background: 'rgba(255,255,255,0.08)', borderRadius: 999, overflow: 'hidden', marginTop: 12 }}>
              <div style={{ height: '100%', width: `${92 * b2}%`, background: 'rgba(167, 139, 250, 0.72)', borderRadius: 999 }} />
            </div>
            <div style={{ fontSize: 20, color: T_EP02.muted, marginTop: 8 }}>Slack / Teams &amp; persistent cloud projects</div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S5CatchV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const meterPct = interpolate(frame, [16, 100], [18, 100], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const strikePct = interpolate(frame, [8, 26], [0, 100], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const proofSp = spring({ frame: Math.max(0, frame - 45), fps, config: { damping: 14, stiffness: 140 } });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: '0 96px 140px 56px', fontFamily: T_EP02.sans, color: T_EP02.ink }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
        <div style={{ fontSize: 64, fontWeight: 900 }}>
          The <span style={{ color: T_EP02.coral }}>Hidden Catch</span>
        </div>
        <div style={{ position: 'relative', alignSelf: 'flex-start', fontSize: 34, fontWeight: 700, color: T_EP02.muted }}>
          <span>&ldquo;Unlimited 24/7 Cloud Agents&rdquo;</span>
          <div style={{ position: 'absolute', left: 0, top: '52%', height: 5, width: `${strikePct}%`, background: T_EP02.coral }} />
        </div>
        <div style={{ background: 'rgba(251, 113, 133, 0.09)', border: `2px solid ${T_EP02.coral}`, borderRadius: 22, padding: '30px 30px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: T_EP02.mono, fontSize: 20, fontWeight: 700, marginBottom: 14 }}>
            <span style={{ color: '#FDA4AF' }}>5H COMPUTE POOL</span>
            <span style={{ color: T_EP02.coral }}>{Math.round(meterPct)}% USED</span>
          </div>
          <div style={{ height: 24, background: 'rgba(255,255,255,0.08)', borderRadius: 999, overflow: 'hidden' }}>
            <div style={{ height: '100%', width: `${meterPct}%`, background: `linear-gradient(90deg, ${T_EP02.amber}, ${T_EP02.coral})`, borderRadius: 999 }} />
          </div>
          <div style={{ marginTop: 20, fontSize: 26, fontWeight: 700, lineHeight: 1.38, opacity: proofSp }}>
            Google Forum Ultra Report: <span style={{ color: '#FDA4AF' }}>Capped in &lt;90 min on 2 heavy jobs</span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S6LimitsV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = spring({ frame, fps, config: { damping: 16, stiffness: 130 } });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: '0 96px 140px 56px', fontFamily: T_EP02.sans, color: T_EP02.ink }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 22, opacity: sp }}>
        <div style={{ fontSize: 48, fontWeight: 900 }}>
          Two <span style={{ color: T_EP02.amber }}>Real Boundaries</span>
        </div>
        <div style={{ background: T_EP02.glass, border: '1.5px solid rgba(251, 191, 36, 0.5)', borderRadius: 20, padding: '26px 28px' }}>
          <div style={{ fontFamily: T_EP02.mono, fontSize: 16, color: T_EP02.amber, fontWeight: 700 }}>U.S. ONLY FEATURES</div>
          <div style={{ fontSize: 26, fontWeight: 700, marginTop: 8, lineHeight: 1.5 }}>
            • Duplex business phone calls
            <br />• $1,000 Google Pay auto-checkout
          </div>
        </div>
        <div style={{ background: T_EP02.glass, border: '1.5px solid rgba(251, 113, 133, 0.55)', borderRadius: 20, padding: '26px 28px' }}>
          <div style={{ fontFamily: T_EP02.mono, fontSize: 16, color: T_EP02.coral, fontWeight: 700 }}>NOT REAL-TIME</div>
          <div style={{ fontSize: 26, fontWeight: 700, marginTop: 8, lineHeight: 1.5 }}>
            Topic monitors aren&apos;t built for instant ticket drops or fast trading alerts.
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S7PlaybookV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = spring({ frame, fps, config: { damping: 16, stiffness: 130 } });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: '0 96px 140px 56px', fontFamily: T_EP02.sans, color: T_EP02.ink }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 22, opacity: sp }}>
        <div style={{ fontSize: 48, fontWeight: 900 }}>
          The <span style={{ color: T_EP02.emerald }}>Hybrid Playbook</span>
        </div>
        <div style={{ background: 'rgba(52, 211, 153, 0.09)', border: '2px solid rgba(52, 211, 153, 0.55)', borderRadius: 20, padding: '26px 28px' }}>
          <div style={{ fontFamily: T_EP02.mono, fontSize: 16, color: T_EP02.emerald, fontWeight: 800 }}>USE GEMINI TASKS ($0)</div>
          <div style={{ fontSize: 26, fontWeight: 700, marginTop: 8, lineHeight: 1.5 }}>
            ✓ Gmail monitors &amp; Workspace briefs
            <br />✓ Scoped web research sweeps
          </div>
        </div>
        <div style={{ background: 'rgba(96, 165, 250, 0.09)', border: '2px solid rgba(96, 165, 250, 0.55)', borderRadius: 20, padding: '26px 28px' }}>
          <div style={{ fontFamily: T_EP02.mono, fontSize: 16, color: T_EP02.blue, fontWeight: 800 }}>KEEP ON LOCAL STACK</div>
          <div style={{ fontSize: 26, fontWeight: 700, marginTop: 8, lineHeight: 1.5 }}>
            ✓ Heavy multi-file coding &amp; custom bots
            <br />✓ Deterministic media &amp; real-time alerts
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const SCENES_V: Record<string, React.FC> = {
  s1: S1HookV,
  s2: S2HowItWorksV,
  s3: S3TiersV,
  s4: S4VsDotsV,
  s5: S5CatchV,
  s6: S6LimitsV,
  s7: S7PlaybookV,
};

export const Ep02MainVertical: React.FC = () => {
  const frame = useCurrentFrame();
  const active = SHOTS_EP02.find((s) => frame >= s.start && frame < s.end) ?? SHOTS_EP02[SHOTS_EP02.length - 1];
  const isCover = frame < 12;

  return (
    <AbsoluteFill>
      <CosmicStarfield />
      <Audio src={staticFile('voice_ep02_mix.mp3')} />
      {isCover ? (
        <CoverPosterVertical />
      ) : (
        <>
          <TopBarV pill={active.pill} chapter={active.chapter} />
          {SHOTS_EP02.map((shot) => {
            const Scene = SCENES_V[shot.id];
            return (
              <Sequence key={shot.id} from={shot.start} durationInFrames={shot.end - shot.start}>
                <Scene />
              </Sequence>
            );
          })}
          <CaptionBarV text={active.subtitle} />
        </>
      )}
    </AbsoluteFill>
  );
};
