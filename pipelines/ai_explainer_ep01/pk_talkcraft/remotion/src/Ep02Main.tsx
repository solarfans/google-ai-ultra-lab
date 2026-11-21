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
import {
  AnimatedCursor,
  AtmosphericStudioBackdrop,
  GeminiSparkleIcon,
  GeminiWindowFrame,
  GoldenFocusBox,
  GoogleDriveTriangleIcon,
  TopLeftKicker,
  V2_TOKENS,
  WhitePillCaption,
} from './ep02_components';
import { SHOTS_EP02 } from './theme_ep02';

const CoverPoster16x9: React.FC = () => (
  <AbsoluteFill
    style={{
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: V2_TOKENS.sans,
      zIndex: 50,
    }}
  >
    <div
      style={{
        width: 540,
        height: 940,
        borderRadius: 28,
        background: 'linear-gradient(165deg, #161A33 0%, #090B1A 100%)',
        border: `2px solid ${V2_TOKENS.goldBorder}`,
        boxShadow: '0 36px 96px rgba(0, 0, 0, 0.85)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '44px 36px',
        textAlign: 'center',
        gap: 26,
      }}
    >
      <div
        style={{
          fontFamily: V2_TOKENS.mono,
          fontSize: 19,
          fontWeight: 800,
          padding: '8px 20px',
          borderRadius: 999,
          background: 'rgba(79, 140, 255, 0.16)',
          border: '1.5px solid rgba(79, 140, 255, 0.55)',
          color: '#93C5FD',
        }}
      >
        GEMINI TASKS · 2026 GUIDE
      </div>
      <div style={{ fontSize: 74, fontWeight: 900, lineHeight: 1.02, letterSpacing: '-0.03em', color: V2_TOKENS.ink }}>
        GOOGLE JUST
        <br />
        DROPPED
        <br />
        <span style={{ color: V2_TOKENS.cobalt }}>GEMINI TASKS</span>
      </div>
      <div
        style={{
          width: '100%',
          padding: '20px 22px',
          borderRadius: 18,
          background: 'rgba(251, 191, 36, 0.14)',
          border: `2px solid ${V2_TOKENS.gold}`,
          fontSize: 27,
          fontWeight: 800,
          color: '#FDE68A',
        }}
      >
        FLIP ONE SWITCH · HANDS-FREE AI
      </div>
      <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 18, color: V2_TOKENS.muted }}>
        Daily Briefings · Web Research · Monitors
      </div>
    </div>
  </AbsoluteFill>
);

const S1Switch: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const flipped = frame >= 68;
  const cursorX = interpolate(frame, [20, 62], [320, 692], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const cursorY = interpolate(frame, [20, 62], [440, 326], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const cursorOpacity = interpolate(frame, [16, 24, 150, 175], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const badgePop = spring({ frame: Math.max(0, frame - 90), fps, config: { damping: 14, stiffness: 150 } });

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: V2_TOKENS.sans, color: V2_TOKENS.ink }}>
      <div style={{ position: 'relative', marginTop: 12 }}>
        <GeminiWindowFrame badge={flipped ? 'CHAT ➔ TASK' : 'GEMINI.GOOGLE.COM'} width={1260}>
          <div style={{ padding: '72px 84px 66px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 34, position: 'relative' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 14, fontSize: 44, fontWeight: 800, letterSpacing: '-0.02em' }}>
              <GeminiSparkleIcon size={36} color={flipped ? V2_TOKENS.gold : V2_TOKENS.cobalt} />
              <span>{flipped ? 'What can I get done for you?' : 'Where should we start?'}</span>
            </div>

            <div
              style={{
                width: '100%',
                borderRadius: 22,
                background: 'rgba(255, 255, 255, 0.04)',
                border: `1.5px solid ${flipped ? 'rgba(79, 140, 255, 0.55)' : 'rgba(255,255,255,0.14)'}`,
                padding: '24px 28px',
                display: 'flex',
                flexDirection: 'column',
                gap: 24,
              }}
            >
              <div style={{ fontSize: 26, color: flipped ? V2_TOKENS.ink : V2_TOKENS.muted, fontWeight: 500 }}>
                + &nbsp;{flipped ? 'Describe a task...' : 'Ask Gemini'}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 16, color: V2_TOKENS.muted }}>
                  Tools &nbsp;·&nbsp; Hydrogen ▾
                </div>
                <div
                  style={{
                    width: 40,
                    height: 40,
                    borderRadius: 999,
                    background: flipped ? V2_TOKENS.cobalt : 'rgba(255,255,255,0.12)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 20,
                    fontWeight: 900,
                    color: '#FFFFFF',
                  }}
                >
                  ↑
                </div>
              </div>
            </div>

            <div style={{ position: 'relative', display: 'inline-flex', padding: 6, borderRadius: 999, background: '#090B17', border: '1px solid rgba(255,255,255,0.14)', gap: 8 }}>
              <span
                style={{
                  padding: '10px 30px',
                  borderRadius: 999,
                  fontSize: 21,
                  fontWeight: 700,
                  background: flipped ? 'transparent' : 'rgba(255,255,255,0.12)',
                  color: flipped ? V2_TOKENS.muted : V2_TOKENS.ink,
                }}
              >
                Chat
              </span>
              <span
                style={{
                  padding: '10px 32px',
                  borderRadius: 999,
                  fontSize: 21,
                  fontWeight: 800,
                  background: flipped ? V2_TOKENS.cobalt : 'transparent',
                  color: flipped ? '#FFFFFF' : V2_TOKENS.muted,
                  boxShadow: flipped ? '0 0 28px rgba(79, 140, 255, 0.55)' : 'none',
                }}
              >
                ✦ Task
              </span>
              <GoldenFocusBox visible={flipped} style={{ right: -4, top: -4, bottom: -4, width: 146, borderRadius: 999 }} />
            </div>

            <div
              style={{
                opacity: badgePop,
                transform: `translateY(${interpolate(badgePop, [0, 1], [12, 0])}px)`,
                padding: '10px 24px',
                borderRadius: 999,
                background: 'rgba(52, 211, 153, 0.14)',
                border: '1px solid rgba(52, 211, 153, 0.5)',
                color: V2_TOKENS.emerald,
                fontFamily: V2_TOKENS.mono,
                fontSize: 18,
                fontWeight: 700,
              }}
            >
              ● BACKGROUND ASSISTANT READY · ACTUALLY FINISHES THE JOB
            </div>

            <AnimatedCursor x={cursorX} y={cursorY} clickFrame={66} opacity={cursorOpacity} />
          </div>
        </GeminiWindowFrame>
      </div>
    </AbsoluteFill>
  );
};

const S2Concierge: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const leftSp = spring({ frame, fps, config: { damping: 16, stiffness: 135 } });
  const rightSp = spring({ frame: Math.max(0, frame - 26), fps, config: { damping: 16, stiffness: 135 } });
  const step1 = frame >= 105;
  const step2 = frame >= 145;
  const step3 = frame >= 185;

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: V2_TOKENS.sans }}>
      <div style={{ width: 1420, display: 'grid', gridTemplateColumns: '1fr 1.15fr', gap: 36, alignItems: 'stretch', marginTop: 12 }}>
        {/* Left: Crisp Cream Editorial Card */}
        <div
          style={{
            background: V2_TOKENS.creamBg,
            color: V2_TOKENS.creamInk,
            borderRadius: 24,
            border: `2px solid ${V2_TOKENS.creamBorder}`,
            boxShadow: '0 28px 70px rgba(0, 0, 0, 0.45)',
            padding: '44px 42px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            opacity: leftSp * (frame > 100 ? 0.82 : 1),
            transform: `translateY(${interpolate(leftSp, [0, 1], [24, 0])}px)`,
          }}
        >
          <div style={{ display: 'flex', flexDirection: 'column', gap: 22 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span
                style={{
                  padding: '6px 16px',
                  borderRadius: 999,
                  background: '#E5E7EB',
                  color: '#374151',
                  fontFamily: V2_TOKENS.mono,
                  fontSize: 16,
                  fontWeight: 800,
                }}
              >
                CHAT MODE
              </span>
              <span style={{ fontSize: 32 }}>💬</span>
            </div>
            <div style={{ fontSize: 44, fontWeight: 900, lineHeight: 1.12, letterSpacing: '-0.02em' }}>
              You ask a question &mdash; and wait.
            </div>
            <div style={{ fontSize: 23, color: V2_TOKENS.creamMuted, lineHeight: 1.5 }}>
              Great for quick answers at your keyboard, but stops the moment you close the tab.
            </div>
          </div>
          <div style={{ marginTop: 28, paddingTop: 20, borderTop: `1px solid ${V2_TOKENS.creamBorder}`, fontFamily: V2_TOKENS.mono, fontSize: 16, color: '#6B7280', fontWeight: 700 }}>
            SYNCHRONOUS · WAITS ON YOU
          </div>
        </div>

        {/* Right: Elevated Gold-Trimmed Dark Cloud Agent Card */}
        <div
          style={{
            background: 'linear-gradient(165deg, #161B30 0%, #0D101D 100%)',
            color: V2_TOKENS.ink,
            borderRadius: 24,
            border: `2px solid ${V2_TOKENS.gold}`,
            boxShadow: '0 32px 86px rgba(0, 0, 0, 0.65), 0 0 40px rgba(251, 191, 36, 0.16)',
            padding: '44px 44px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            opacity: rightSp,
            transform: `translateY(${interpolate(rightSp, [0, 1], [28, 0])}px)`,
          }}
        >
          <div style={{ display: 'flex', flexDirection: 'column', gap: 22 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span
                style={{
                  padding: '7px 18px',
                  borderRadius: 999,
                  background: V2_TOKENS.cobalt,
                  color: '#FFFFFF',
                  fontFamily: V2_TOKENS.mono,
                  fontSize: 16,
                  fontWeight: 800,
                }}
              >
                ✦ TASK MODE
              </span>
              <span
                style={{
                  padding: '6px 14px',
                  borderRadius: 999,
                  background: 'rgba(52, 211, 153, 0.14)',
                  border: '1px solid rgba(52, 211, 153, 0.5)',
                  color: V2_TOKENS.emerald,
                  fontFamily: V2_TOKENS.mono,
                  fontSize: 14,
                  fontWeight: 700,
                }}
              >
                CLOUD VM · WALK AWAY
              </span>
            </div>

            <div style={{ fontSize: 44, fontWeight: 900, lineHeight: 1.12, letterSpacing: '-0.02em' }}>
              Hand over a job &mdash; <span style={{ color: V2_TOKENS.gold }}>walk away.</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginTop: 6 }}>
              {[
                { label: '1. Plans multi-step workflow in Google cloud', done: step1 },
                { label: '2. Browses sites & gathers live facts', done: step2 },
                { label: '3. Delivers finished report when you return', done: step3 },
              ].map((row, idx) => (
                <div
                  key={idx}
                  style={{
                    padding: '14px 18px',
                    borderRadius: 12,
                    background: row.done ? 'rgba(52, 211, 153, 0.12)' : 'rgba(255,255,255,0.04)',
                    border: `1px solid ${row.done ? 'rgba(52, 211, 153, 0.55)' : 'rgba(255,255,255,0.10)'}`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    fontSize: 20,
                    fontWeight: 600,
                  }}
                >
                  <span>{row.label}</span>
                  <span style={{ color: row.done ? V2_TOKENS.emerald : V2_TOKENS.muted, fontFamily: V2_TOKENS.mono, fontWeight: 800 }}>
                    {row.done ? '✓ DONE' : '...'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const PROMPT_S3 = 'Every morning at 7:00 AM, scan the biggest AI launches and send me a one-page summary.';

const S3DailyBrief: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const showResult = frame >= 186;
  const typedCount = Math.floor(interpolate(frame, [24, 152], [0, PROMPT_S3.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const cursorX = interpolate(frame, [130, 164], [960, 1146], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const cursorY = interpolate(frame, [130, 164], [380, 294], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const cursorOpacity = interpolate(frame, [125, 134, 178, 185], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const resultPop = spring({ frame: Math.max(0, frame - 188), fps, config: { damping: 16, stiffness: 135 } });
  const focusReady = frame >= 230;

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: V2_TOKENS.sans, color: V2_TOKENS.ink }}>
      <GeminiWindowFrame badge={showResult ? 'REAL RESULT · ROUTINE SET' : 'TYPING THE TASK'} width={1280}>
        {!showResult ? (
          <div style={{ padding: '68px 72px 72px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 30, position: 'relative' }}>
            <div style={{ fontSize: 40, fontWeight: 800, letterSpacing: '-0.02em' }}>
              What can I check off your list?
            </div>
            <div
              style={{
                width: '100%',
                minHeight: 170,
                borderRadius: 20,
                background: '#0A0D19',
                border: '1.5px solid rgba(79, 140, 255, 0.5)',
                padding: '26px 30px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                gap: 20,
              }}
            >
              <div style={{ fontSize: 28, lineHeight: 1.45, fontWeight: 500, color: V2_TOKENS.ink }}>
                {PROMPT_S3.slice(0, typedCount)}
                <span style={{ color: V2_TOKENS.cobalt, fontWeight: 900 }}>|</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ padding: '6px 16px', borderRadius: 999, background: 'rgba(79,140,255,0.16)', color: V2_TOKENS.cobalt, fontFamily: V2_TOKENS.mono, fontSize: 15, fontWeight: 700 }}>
                  ✦ Task Mode · Hydrogen
                </span>
                <div
                  style={{
                    width: 44,
                    height: 44,
                    borderRadius: 999,
                    background: typedCount > 15 ? V2_TOKENS.cobalt : 'rgba(255,255,255,0.12)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 22,
                    fontWeight: 900,
                  }}
                >
                  ↑
                </div>
              </div>
            </div>
            <AnimatedCursor x={cursorX} y={cursorY} clickFrame={168} opacity={cursorOpacity} />
          </div>
        ) : (
          <div style={{ padding: '50px 64px 58px', display: 'flex', flexDirection: 'column', gap: 26, opacity: resultPop }}>
            <div style={{ alignSelf: 'flex-end', maxWidth: 820, padding: '16px 22px', borderRadius: 16, background: 'rgba(255,255,255,0.06)', fontSize: 20, color: '#CBD5E1' }}>
              {PROMPT_S3}
            </div>
            <div style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
              <GeminiSparkleIcon size={28} color={V2_TOKENS.cobalt} />
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 18 }}>
                <div style={{ fontSize: 26, fontWeight: 700, lineHeight: 1.4 }}>
                  Done. I&apos;ve scheduled your daily AI launches briefing every morning at <span style={{ color: V2_TOKENS.gold }}>7:00 AM</span>.
                </div>
                <div
                  style={{
                    position: 'relative',
                    padding: '22px 26px',
                    borderRadius: 16,
                    background: '#0A0D19',
                    border: '1px solid rgba(255,255,255,0.14)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                    <span style={{ fontSize: 26 }}>🕒</span>
                    <div>
                      <div style={{ fontSize: 24, fontWeight: 800 }}>Summarize Daily AI Launches</div>
                      <div style={{ fontSize: 17, color: V2_TOKENS.muted, marginTop: 4 }}>Scans official blogs + web · One-page brief</div>
                    </div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                    <span style={{ padding: '8px 18px', borderRadius: 999, background: V2_TOKENS.cobaltDeep, fontFamily: V2_TOKENS.mono, fontSize: 17, fontWeight: 800 }}>
                      DAILY · 07:00 AM
                    </span>
                    <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 15, color: V2_TOKENS.emerald, fontWeight: 700 }}>
                      ✓ ACTIVE
                    </span>
                  </div>
                  <GoldenFocusBox visible={focusReady} style={{ inset: -4, borderRadius: 18 }} />
                </div>
              </div>
            </div>
          </div>
        )}
      </GeminiWindowFrame>
    </AbsoluteFill>
  );
};

const S4WebResearch: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const showCanvas = frame >= 172;
  const s1 = frame >= 36;
  const s2 = frame >= 84;
  const s3 = frame >= 128;
  const canvasPop = spring({ frame: Math.max(0, frame - 174), fps, config: { damping: 16, stiffness: 135 } });
  const colFocus = frame >= 224;

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: V2_TOKENS.sans, color: V2_TOKENS.ink }}>
      <GeminiWindowFrame badge={showCanvas ? 'GEMINI · CANVAS REPORT' : 'GEMINI · LIVE STEPS'} width={1320}>
        {!showCanvas ? (
          <div style={{ padding: '48px 64px 56px', display: 'flex', flexDirection: 'column', gap: 22 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, fontSize: 22, fontWeight: 700, color: '#CBD5E1' }}>
              <GeminiSparkleIcon size={24} color={V2_TOKENS.cobalt} />
              <span>Thinking it through...</span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 16, paddingLeft: 18, borderLeft: '2px solid rgba(79, 140, 255, 0.35)' }}>
              {[
                { icon: 'G', title: 'Searching Google for Q4 launch announcements & pricing', done: s1, showAt: 10 },
                { icon: '🌐', title: 'Visiting 8 live product websites & changelog pages', done: s2, showAt: 48 },
                { icon: '📊', title: 'Extracting feature gaps into structured Canvas report', done: s3, showAt: 96 },
              ].map((step, i) => {
                const visible = frame >= step.showAt;
                return (
                  <div
                    key={i}
                    style={{
                      opacity: visible ? 1 : 0.22,
                      padding: '20px 24px',
                      borderRadius: 14,
                      background: step.done ? 'rgba(52, 211, 153, 0.10)' : 'rgba(255,255,255,0.04)',
                      border: `1px solid ${step.done ? 'rgba(52, 211, 153, 0.45)' : 'rgba(255,255,255,0.1)'}`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      fontSize: 23,
                      fontWeight: 600,
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                      <span style={{ fontFamily: V2_TOKENS.mono, fontWeight: 900, color: V2_TOKENS.cobalt }}>{step.icon}</span>
                      <span>{step.title}</span>
                    </div>
                    <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 16, color: step.done ? V2_TOKENS.emerald : V2_TOKENS.gold, fontWeight: 800 }}>
                      {step.done ? '✓ VERIFIED' : 'RUNNING...'}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        ) : (
          <div style={{ padding: '24px 36px 36px', opacity: canvasPop }}>
            <div style={{ background: '#FFFFFF', color: '#0F172A', borderRadius: 16, overflow: 'hidden', boxShadow: '0 16px 40px rgba(0,0,0,0.4)' }}>
              <div style={{ height: 46, background: '#F1F5F9', borderBottom: '1px solid #E2E8F0', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 22px' }}>
                <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 15, fontWeight: 700, color: '#334155' }}>
                  Canvas · Competitive Launch Brief.md
                </span>
                <div style={{ display: 'flex', gap: 10, fontFamily: V2_TOKENS.mono, fontSize: 13, fontWeight: 700 }}>
                  <span style={{ padding: '4px 12px', borderRadius: 6, background: '#E2E8F0', color: '#475569' }}>Code</span>
                  <span style={{ padding: '4px 12px', borderRadius: 6, background: '#2563EB', color: '#FFFFFF' }}>Preview</span>
                  <span style={{ padding: '4px 12px', borderRadius: 6, background: '#0F172A', color: '#FFFFFF' }}>Export ▾</span>
                </div>
              </div>
              <div style={{ padding: '26px 34px', position: 'relative' }}>
                <div style={{ fontSize: 32, fontWeight: 900, letterSpacing: '-0.02em', marginBottom: 18 }}>
                  Verified Market Table &amp; Editable Summary
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1.1fr 1fr 1.4fr', border: '1px solid #CBD5E1', borderRadius: 12, overflow: 'hidden', fontSize: 19 }}>
                  {['Company', 'Free Tier', 'Verified Finding'].map((h) => (
                    <div key={h} style={{ background: '#F8FAFC', padding: '12px 16px', fontWeight: 800, borderBottom: '1px solid #CBD5E1' }}>
                      {h}
                    </div>
                  ))}
                  {[
                    ['Notion AI', 'Trial Only', 'Strong workspace wikis, weak live web actions'],
                    ['Perplexity', 'Limited', 'Fast citations, no multi-step background routines'],
                    ['Gemini Tasks', '6 Countries', 'Runs cloud schedules + Drive/Gmail workflows'],
                  ].map((r, ri) => (
                    <React.Fragment key={ri}>
                      <div style={{ padding: '12px 16px', fontWeight: 800, borderBottom: ri < 2 ? '1px solid #E2E8F0' : 'none', background: ri === 2 ? '#EFF6FF' : '#FFFFFF' }}>{r[0]}</div>
                      <div style={{ padding: '12px 16px', fontFamily: V2_TOKENS.mono, fontWeight: 700, borderBottom: ri < 2 ? '1px solid #E2E8F0' : 'none', background: ri === 2 ? '#EFF6FF' : '#FFFFFF' }}>{r[1]}</div>
                      <div style={{ padding: '12px 16px', color: '#334155', borderBottom: ri < 2 ? '1px solid #E2E8F0' : 'none', background: ri === 2 ? '#EFF6FF' : '#FFFFFF' }}>{r[2]}</div>
                    </React.Fragment>
                  ))}
                </div>
                <GoldenFocusBox visible={colFocus} style={{ left: 30, right: 30, bottom: 22, height: 54, borderRadius: 10 }} />
              </div>
            </div>
          </div>
        )}
      </GeminiWindowFrame>
    </AbsoluteFill>
  );
};

const S5Monitors: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const quotePop = spring({ frame: Math.max(0, frame - 150), fps, config: { damping: 14, stiffness: 140 } });

  const rows = [
    { time: 'MON 08:00', name: 'Site Health, SSL & Broken Links Check', badge: 'WEEKLY', delay: 14 },
    { time: 'DAILY 09:00', name: 'Flight & Hotel Price Drop Watcher', badge: 'MONITOR', delay: 62 },
    { time: 'GMAIL · LIVE', name: 'Flag Urgent Emails & Draft Monday Replies', badge: 'GMAIL', delay: 110 },
  ];

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: V2_TOKENS.sans }}>
      <div style={{ width: 1300, display: 'flex', flexDirection: 'column', gap: 26, position: 'relative', marginTop: 10 }}>
        {/* Dark Navy Routine Board */}
        <div
          style={{
            borderRadius: 22,
            background: 'linear-gradient(165deg, #131A35 0%, #0A0E1F 100%)',
            border: `1.5px solid ${V2_TOKENS.goldBorder}`,
            boxShadow: '0 32px 84px rgba(0,0,0,0.65)',
            padding: '32px 38px',
            color: V2_TOKENS.ink,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 22 }}>
            <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 18, fontWeight: 800, color: V2_TOKENS.muted }}>
              🕒 YOUR ROUTINE · RUNS ON ITS OWN
            </div>
            <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 15, color: V2_TOKENS.emerald, fontWeight: 700 }}>
              ● CLOUD SCHEDULER ARMED
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            {rows.map((r, i) => {
              const sp = spring({ frame: Math.max(0, frame - r.delay), fps, config: { damping: 16, stiffness: 145 } });
              return (
                <div
                  key={i}
                  style={{
                    opacity: sp,
                    transform: `translateX(${interpolate(sp, [0, 1], [-22, 0])}px)`,
                    padding: '18px 24px',
                    borderRadius: 14,
                    background: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255,255,255,0.10)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: 26 }}>
                    <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 19, fontWeight: 800, color: V2_TOKENS.gold, minWidth: 145 }}>
                      {r.time}
                    </span>
                    <span style={{ fontSize: 26, fontWeight: 800 }}>{r.name}</span>
                  </div>
                  <span style={{ padding: '7px 18px', borderRadius: 8, background: V2_TOKENS.cobaltDeep, fontFamily: V2_TOKENS.mono, fontSize: 16, fontWeight: 800 }}>
                    {r.badge}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Contrast Cream Editorial Quote Card */}
        <div
          style={{
            alignSelf: 'flex-end',
            maxWidth: 880,
            background: V2_TOKENS.creamBg,
            color: V2_TOKENS.creamInk,
            borderRadius: 18,
            border: `2px solid ${V2_TOKENS.cobalt}`,
            padding: '24px 32px',
            boxShadow: '0 24px 60px rgba(0,0,0,0.55)',
            opacity: quotePop,
            transform: `rotate(-1.2deg) scale(${interpolate(quotePop, [0, 1], [0.92, 1])})`,
          }}
        >
          <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 14, fontWeight: 800, color: V2_TOKENS.cobaltDeep, marginBottom: 6 }}>
            BEFORE MONDAY MORNING
          </div>
          <div style={{ fontSize: 27, fontWeight: 800, lineHeight: 1.3 }}>
            &ldquo;Flags urgent emails, tracks price drops, and drafts replies before you even open Gmail.&rdquo;
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S6Permission: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const connected = frame >= 184;
  const cursorX = interpolate(frame, [115, 178], [420, 998], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const cursorY = interpolate(frame, [115, 178], [390, 294], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const cursorOpacity = interpolate(frame, [110, 120, 225, 240], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const quotePop = spring({ frame: Math.max(0, frame - 205), fps, config: { damping: 14, stiffness: 150 } });

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: V2_TOKENS.sans, color: V2_TOKENS.ink }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 26, position: 'relative' }}>
        <GeminiWindowFrame badge={connected ? 'ACCESS GRANTED BY YOU' : 'WAITING FOR YOUR INPUT'} width={1180}>
          <div style={{ padding: '44px 54px 48px', display: 'flex', flexDirection: 'column', gap: 24, position: 'relative' }}>
            <div style={{ fontSize: 27, fontWeight: 700, lineHeight: 1.4 }}>
              Sure. First, I&apos;ll need your permission to turn on the Google Drive app.
            </div>
            <div
              style={{
                borderRadius: 18,
                background: '#0A0D19',
                border: `1.5px solid ${connected ? V2_TOKENS.emerald : 'rgba(255,255,255,0.16)'}`,
                padding: '28px 32px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                gap: 24,
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
                <GoogleDriveTriangleIcon size={44} />
                <div>
                  <div style={{ fontSize: 26, fontWeight: 800 }}>Google Drive</div>
                  <div style={{ fontSize: 18, color: V2_TOKENS.muted, marginTop: 4 }}>
                    Read docs, organize summaries &amp; export drafts only when approved
                  </div>
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 14, position: 'relative' }}>
                {!connected && (
                  <span style={{ padding: '12px 22px', borderRadius: 999, background: 'rgba(255,255,255,0.08)', fontSize: 19, fontWeight: 700, color: V2_TOKENS.muted }}>
                    No thanks
                  </span>
                )}
                <span
                  style={{
                    padding: '12px 28px',
                    borderRadius: 999,
                    background: connected ? V2_TOKENS.emerald : V2_TOKENS.cobalt,
                    color: connected ? '#062016' : '#FFFFFF',
                    fontSize: 20,
                    fontWeight: 900,
                  }}
                >
                  {connected ? '✓ Connected' : 'Connect'}
                </span>
                <GoldenFocusBox visible={!connected && frame >= 75} style={{ right: -6, top: -6, bottom: -6, width: 150, borderRadius: 999 }} />
              </div>
            </div>
            <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 16, color: connected ? V2_TOKENS.emerald : V2_TOKENS.cobalt, fontWeight: 700 }}>
              {connected ? '● RESUMING TASK SAFELY' : '⏸ PAUSED · WAITING FOR YOUR INPUT'}
            </div>
            <AnimatedCursor x={cursorX} y={cursorY} clickFrame={182} opacity={cursorOpacity} />
          </div>
        </GeminiWindowFrame>

        <div
          style={{
            opacity: quotePop,
            transform: `translateY(${interpolate(quotePop, [0, 1], [16, 0])}px)`,
            background: V2_TOKENS.creamBg,
            color: V2_TOKENS.creamInk,
            borderRadius: 16,
            border: `2px solid ${V2_TOKENS.gold}`,
            padding: '18px 38px',
            fontSize: 34,
            fontWeight: 900,
            fontStyle: 'italic',
            boxShadow: '0 22px 54px rgba(0,0,0,0.5)',
          }}
        >
          &ldquo;Nothing leaves without a <span style={{ color: V2_TOKENS.cobaltDeep }}>yes</span>.&rdquo;
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S7Availability: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const proSp = spring({ frame: Math.max(0, frame - 210), fps, config: { damping: 16, stiffness: 135 } });
  const countries = [
    { name: 'THE US', sub: 'Free Tier Live' },
    { name: 'CANADA', sub: 'Free Tier Live' },
    { name: 'JAPAN', sub: 'Free Tier Live' },
    { name: 'SOUTH KOREA', sub: 'Free Tier Live' },
    { name: 'AUSTRALIA', sub: 'Free Tier Live' },
    { name: 'INDIA', sub: 'Free Tier Live' },
  ];

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: V2_TOKENS.sans }}>
      <div style={{ width: 1360, display: 'flex', flexDirection: 'column', gap: 28, marginTop: 14 }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 22 }}>
          {countries.map((c, idx) => {
            const sp = spring({ frame: Math.max(0, frame - (10 + idx * 16)), fps, config: { damping: 15, stiffness: 150 } });
            return (
              <div
                key={c.name}
                style={{
                  background: V2_TOKENS.creamBg,
                  color: V2_TOKENS.creamInk,
                  borderRadius: 18,
                  border: `2px solid ${V2_TOKENS.creamBorder}`,
                  padding: '26px 30px',
                  boxShadow: '0 20px 50px rgba(0,0,0,0.42)',
                  opacity: sp,
                  transform: `translateY(${interpolate(sp, [0, 1], [18, 0])}px)`,
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10 }}>
                  <span style={{ fontSize: 34, fontWeight: 900, letterSpacing: '-0.02em' }}>{c.name}</span>
                  <span style={{ padding: '4px 12px', borderRadius: 999, background: '#DBEAFE', color: V2_TOKENS.cobaltDeep, fontFamily: V2_TOKENS.mono, fontSize: 13, fontWeight: 800 }}>
                    FREE · 10/DAY
                  </span>
                </div>
                <div style={{ fontSize: 18, color: V2_TOKENS.creamMuted, fontWeight: 600 }}>
                  {c.sub} · Standard Google Account
                </div>
              </div>
            );
          })}
        </div>

        {/* Pro & Ultra Unlock Strip */}
        <div
          style={{
            opacity: proSp,
            transform: `translateY(${interpolate(proSp, [0, 1], [24, 0])}px)`,
            borderRadius: 22,
            background: 'linear-gradient(165deg, #1A1738 0%, #0D1020 100%)',
            border: `2px solid ${V2_TOKENS.gold}`,
            boxShadow: '0 28px 72px rgba(0,0,0,0.6), 0 0 38px rgba(251,191,36,0.16)',
            padding: '28px 42px',
            color: V2_TOKENS.ink,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <div>
            <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 16, fontWeight: 800, color: V2_TOKENS.gold }}>
              PRO &amp; ULTRA PLANS · GLOBAL ACCESS
            </div>
            <div style={{ fontSize: 30, fontWeight: 800, marginTop: 6 }}>
              Full Automation &amp; Event Monitors
            </div>
          </div>
          <div style={{ display: 'flex', gap: 52, alignItems: 'center' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 56, fontWeight: 900, color: V2_TOKENS.gold, lineHeight: 1 }}>50</div>
              <div style={{ fontSize: 17, color: '#FDE68A', fontWeight: 700, marginTop: 4 }}>Schedules</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 56, fontWeight: 900, color: V2_TOKENS.emerald, lineHeight: 1 }}>15</div>
              <div style={{ fontSize: 17, color: '#A7F3D0', fontWeight: 700, marginTop: 4 }}>Parallel Tasks</div>
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const SKILL_TYPED = '/weekly-brief';

const S8ProTips: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const showSkillBeat = frame >= 248;
  const barPct = interpolate(frame, [20, 150], [18, 92], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const typedLen = Math.floor(interpolate(frame, [260, 325], [0, SKILL_TYPED.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const skillChosen = frame >= 390;
  const cursorX = interpolate(frame, [335, 385], [880, 420], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const cursorY = interpolate(frame, [335, 385], [370, 290], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const cursorOpacity = interpolate(frame, [330, 340, 420, 438], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const tip2Pop = spring({ frame: Math.max(0, frame - 252), fps, config: { damping: 16, stiffness: 135 } });

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: V2_TOKENS.sans, color: V2_TOKENS.ink }}>
      {!showSkillBeat ? (
        <GeminiWindowFrame badge="TIP 1 · COMPUTE BUDGET" width={1220}>
          <div style={{ padding: '48px 56px 54px', display: 'flex', flexDirection: 'column', gap: 28 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ fontSize: 36, fontWeight: 900 }}>5-Hour Rolling Compute Budget</div>
              <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 24, fontWeight: 800, color: V2_TOKENS.coral }}>
                {Math.round(barPct)}% WINDOW
              </span>
            </div>
            <div style={{ height: 24, borderRadius: 999, background: 'rgba(255,255,255,0.08)', overflow: 'hidden' }}>
              <div style={{ height: '100%', width: `${barPct}%`, background: `linear-gradient(90deg, ${V2_TOKENS.cobalt}, ${V2_TOKENS.gold}, ${V2_TOKENS.coral})`, borderRadius: 999 }} />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, marginTop: 8 }}>
              <div style={{ padding: '24px 28px', borderRadius: 16, background: 'rgba(251, 113, 133, 0.10)', border: `1.5px solid ${V2_TOKENS.coral}` }}>
                <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 15, color: V2_TOKENS.coral, fontWeight: 800 }}>✗ AVOID THIS</div>
                <div style={{ fontSize: 27, fontWeight: 800, marginTop: 8, textDecoration: 'line-through', textDecorationColor: V2_TOKENS.coral }}>
                  Dumping 10 jobs into 1 huge prompt
                </div>
              </div>
              <div style={{ padding: '24px 28px', borderRadius: 16, background: 'rgba(52, 211, 153, 0.12)', border: `2px solid ${V2_TOKENS.emerald}` }}>
                <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 15, color: V2_TOKENS.emerald, fontWeight: 800 }}>✓ DO THIS INSTEAD</div>
                <div style={{ fontSize: 27, fontWeight: 800, marginTop: 8 }}>
                  Keep each task tightly scoped
                </div>
              </div>
            </div>
          </div>
        </GeminiWindowFrame>
      ) : (
        <div style={{ opacity: tip2Pop }}>
          <GeminiWindowFrame badge="TIP 2 · SLASH SKILLS" width={1220}>
            <div style={{ padding: '44px 56px 56px', display: 'flex', flexDirection: 'column', gap: 24, position: 'relative' }}>
              <div style={{ fontSize: 34, fontWeight: 900 }}>
                Save Repeat Workflows as <span style={{ color: V2_TOKENS.cobalt }}>/Skills</span>
              </div>

              <div style={{ borderRadius: 18, background: '#0A0D19', border: `1.5px solid ${V2_TOKENS.cobalt}`, padding: '20px 26px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 14, fontFamily: V2_TOKENS.mono, fontSize: 26, fontWeight: 700 }}>
                  {skillChosen ? (
                    <span style={{ padding: '6px 18px', borderRadius: 999, background: V2_TOKENS.cobaltDeep, color: '#FFFFFF' }}>
                      /weekly-brief
                    </span>
                  ) : (
                    <span>
                      {SKILL_TYPED.slice(0, typedLen)}
                      <span style={{ color: V2_TOKENS.cobalt }}>|</span>
                    </span>
                  )}
                  <span style={{ fontFamily: V2_TOKENS.sans, fontSize: 22, color: V2_TOKENS.muted }}>
                    {skillChosen ? 'Run Monday briefing & save summary to Drive' : ''}
                  </span>
                </div>
                <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 15, color: V2_TOKENS.emerald, fontWeight: 700 }}>
                  {skillChosen ? '✓ 1-CLICK REUSE' : 'SLASH MENU'}
                </span>
              </div>

              {/* Slash Autocomplete Menu */}
              <div style={{ borderRadius: 16, background: '#171C30', border: '1px solid rgba(255,255,255,0.14)', padding: 10, display: 'flex', flexDirection: 'column', gap: 8 }}>
                {[
                  { cmd: '/weekly-brief', desc: 'Scan AI launches -> format 1-page Canvas brief', active: true },
                  { cmd: '/inbox-triage', desc: 'Flag urgent Gmail threads & prepare Monday drafts', active: false },
                  { cmd: '/price-watch', desc: 'Compare flight & hotel fares and alert on drops', active: false },
                ].map((s) => (
                  <div
                    key={s.cmd}
                    style={{
                      padding: '14px 20px',
                      borderRadius: 12,
                      background: s.active ? 'rgba(79, 140, 255, 0.18)' : 'transparent',
                      border: `1.5px solid ${s.active ? V2_TOKENS.gold : 'transparent'}`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                    }}
                  >
                    <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 22, fontWeight: 800, color: s.active ? '#93C5FD' : V2_TOKENS.ink }}>
                      {s.cmd}
                    </span>
                    <span style={{ fontSize: 19, color: V2_TOKENS.muted }}>{s.desc}</span>
                  </div>
                ))}
              </div>
              <AnimatedCursor x={cursorX} y={cursorY} clickFrame={388} opacity={cursorOpacity} />
            </div>
          </GeminiWindowFrame>
        </div>
      )}
    </AbsoluteFill>
  );
};

const S9FiveSteps: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const steps = [
    { num: '1', label: 'OPEN GEMINI', tag: 'WEB OR APP', activeAt: 16 },
    { num: '2', label: 'CLICK TASK', tag: 'TOGGLE', activeAt: 58 },
    { num: '3', label: 'DESCRIBE ONE CLEAR JOB', tag: 'SCOPE', activeAt: 102 },
    { num: '4', label: 'PUT THE TIMING FIRST', tag: 'SCHEDULE', activeAt: 152 },
    { num: '5', label: 'REVIEW THE FIRST RUN', tag: 'FOLLOW FOR MORE', activeAt: 204 },
  ];

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', fontFamily: V2_TOKENS.sans, color: V2_TOKENS.ink }}>
      <GeminiWindowFrame badge="STEP BY STEP" width={1140}>
        <div style={{ padding: '36px 46px 42px', display: 'flex', flexDirection: 'column', gap: 14 }}>
          {steps.map((s, idx) => {
            const lit = frame >= s.activeAt;
            const pop = spring({ frame: Math.max(0, frame - idx * 8), fps, config: { damping: 16, stiffness: 145 } });
            return (
              <div
                key={s.num}
                style={{
                  opacity: pop,
                  padding: '18px 26px',
                  borderRadius: 14,
                  background: lit ? 'rgba(79, 140, 255, 0.14)' : 'rgba(255, 255, 255, 0.04)',
                  border: `1.5px solid ${lit ? V2_TOKENS.gold : 'rgba(255,255,255,0.10)'}`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
                  <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 28, fontWeight: 900, color: lit ? V2_TOKENS.gold : V2_TOKENS.muted }}>
                    {s.num}
                  </span>
                  <span style={{ fontSize: 29, fontWeight: 900, letterSpacing: '-0.01em', color: lit ? V2_TOKENS.ink : '#CBD5E1' }}>
                    {s.label}
                  </span>
                </div>
                <span
                  style={{
                    padding: '6px 16px',
                    borderRadius: 8,
                    background: lit ? V2_TOKENS.cobaltDeep : 'rgba(255,255,255,0.08)',
                    fontFamily: V2_TOKENS.mono,
                    fontSize: 15,
                    fontWeight: 800,
                    color: '#FFFFFF',
                  }}
                >
                  {s.tag}
                </span>
              </div>
            );
          })}
        </div>
      </GeminiWindowFrame>
    </AbsoluteFill>
  );
};

const SCENES_EP02: Record<string, React.FC> = {
  s1: S1Switch,
  s2: S2Concierge,
  s3: S3DailyBrief,
  s4: S4WebResearch,
  s5: S5Monitors,
  s6: S6Permission,
  s7: S7Availability,
  s8: S8ProTips,
  s9: S9FiveSteps,
};

export const Ep02Main: React.FC = () => {
  const frame = useCurrentFrame();
  const active = SHOTS_EP02.find((s) => frame >= s.start && frame < s.end) ?? SHOTS_EP02[SHOTS_EP02.length - 1];
  const isCover = frame < 12;

  return (
    <AbsoluteFill>
      <AtmosphericStudioBackdrop />
      <Audio src={staticFile('voice_ep02_mix.mp3')} />
      {isCover ? (
        <CoverPoster16x9 />
      ) : (
        <>
          <TopLeftKicker tag={active.tag} headline={active.headline} accentWord={active.accentWord} top={28} left={48} fontSize={30} />
          {SHOTS_EP02.map((shot) => {
            const Scene = SCENES_EP02[shot.id];
            return (
              <Sequence key={shot.id} from={shot.start} durationInFrames={shot.end - shot.start}>
                <Scene />
              </Sequence>
            );
          })}
          <WhitePillCaption bottom={36} fontSize={30} maxWidth={920} />
        </>
      )}
    </AbsoluteFill>
  );
};
