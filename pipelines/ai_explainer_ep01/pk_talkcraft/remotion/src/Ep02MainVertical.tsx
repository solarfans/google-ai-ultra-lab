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

const CoverPosterVertical: React.FC = () => (
  <AbsoluteFill
    style={{
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: V2_TOKENS.sans,
      padding: '100px 64px',
      textAlign: 'center',
      zIndex: 50,
    }}
  >
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 36 }}>
      <div
        style={{
          fontFamily: V2_TOKENS.mono,
          fontSize: 27,
          fontWeight: 800,
          padding: '12px 28px',
          borderRadius: 999,
          background: 'rgba(79, 140, 255, 0.16)',
          border: '1.5px solid rgba(79, 140, 255, 0.55)',
          color: '#93C5FD',
        }}
      >
        GEMINI TASKS · 2026 GUIDE
      </div>
      <div style={{ fontSize: 112, fontWeight: 900, lineHeight: 1.0, letterSpacing: '-0.03em', color: V2_TOKENS.ink }}>
        GOOGLE JUST
        <br />
        DROPPED
        <br />
        <span style={{ color: V2_TOKENS.cobalt }}>GEMINI TASKS</span>
      </div>
      <div
        style={{
          padding: '26px 42px',
          borderRadius: 22,
          background: 'rgba(251, 191, 36, 0.14)',
          border: `2px solid ${V2_TOKENS.gold}`,
          fontSize: 38,
          fontWeight: 800,
          color: '#FDE68A',
        }}
      >
        FLIP ONE SWITCH · HANDS-FREE AI
      </div>
      <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 24, color: V2_TOKENS.muted }}>
        Daily Briefings · Web Research · Monitors
      </div>
    </div>
  </AbsoluteFill>
);

const STAGE_PAD = '210px 78px 360px 48px';

const S1SwitchV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const flipped = frame >= 68;
  const cursorX = interpolate(frame, [20, 62], [220, 520], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const cursorY = interpolate(frame, [20, 62], [430, 326], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const cursorOpacity = interpolate(frame, [16, 24, 150, 175], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const badgePop = spring({ frame: Math.max(0, frame - 90), fps, config: { damping: 14, stiffness: 150 } });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: STAGE_PAD, fontFamily: V2_TOKENS.sans, color: V2_TOKENS.ink }}>
      <GeminiWindowFrame badge={flipped ? 'CHAT ➔ TASK' : 'GEMINI.GOOGLE.COM'} width={954} maxWidth="100%">
        <div style={{ padding: '48px 40px 52px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 30, position: 'relative' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, fontSize: 38, fontWeight: 800, textAlign: 'center', lineHeight: 1.15 }}>
            <GeminiSparkleIcon size={32} color={flipped ? V2_TOKENS.gold : V2_TOKENS.cobalt} />
            <span>{flipped ? 'What can I get done for you?' : 'Where should we start?'}</span>
          </div>

          <div
            style={{
              width: '100%',
              borderRadius: 20,
              background: 'rgba(255, 255, 255, 0.04)',
              border: `1.5px solid ${flipped ? 'rgba(79, 140, 255, 0.55)' : 'rgba(255,255,255,0.14)'}`,
              padding: '22px 24px',
              display: 'flex',
              flexDirection: 'column',
              gap: 20,
            }}
          >
            <div style={{ fontSize: 25, color: flipped ? V2_TOKENS.ink : V2_TOKENS.muted, fontWeight: 500 }}>
              + &nbsp;{flipped ? 'Describe a task...' : 'Ask Gemini'}
            </div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 15, color: V2_TOKENS.muted }}>Tools · Hydrogen ▾</div>
              <div style={{ width: 38, height: 38, borderRadius: 999, background: flipped ? V2_TOKENS.cobalt : 'rgba(255,255,255,0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 20, fontWeight: 900 }}>
                ↑
              </div>
            </div>
          </div>

          <div style={{ position: 'relative', display: 'inline-flex', padding: 6, borderRadius: 999, background: '#090B17', border: '1px solid rgba(255,255,255,0.14)', gap: 8 }}>
            <span style={{ padding: '10px 28px', borderRadius: 999, fontSize: 21, fontWeight: 700, background: flipped ? 'transparent' : 'rgba(255,255,255,0.12)', color: flipped ? V2_TOKENS.muted : V2_TOKENS.ink }}>
              Chat
            </span>
            <span style={{ padding: '10px 28px', borderRadius: 999, fontSize: 21, fontWeight: 800, background: flipped ? V2_TOKENS.cobalt : 'transparent', color: flipped ? '#FFFFFF' : V2_TOKENS.muted, boxShadow: flipped ? '0 0 28px rgba(79, 140, 255, 0.55)' : 'none' }}>
              ✦ Task
            </span>
            <GoldenFocusBox visible={flipped} style={{ right: -4, top: -4, bottom: -4, width: 138, borderRadius: 999 }} />
          </div>

          <div style={{ opacity: badgePop, padding: '10px 20px', borderRadius: 999, background: 'rgba(52, 211, 153, 0.14)', border: '1px solid rgba(52, 211, 153, 0.5)', color: V2_TOKENS.emerald, fontFamily: V2_TOKENS.mono, fontSize: 15, fontWeight: 700, textAlign: 'center' }}>
            ● BACKGROUND AGENT READY
          </div>

          <AnimatedCursor x={cursorX} y={cursorY} clickFrame={66} opacity={cursorOpacity} />
        </div>
      </GeminiWindowFrame>
    </AbsoluteFill>
  );
};

const S2ConciergeV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const leftSp = spring({ frame, fps, config: { damping: 16, stiffness: 135 } });
  const rightSp = spring({ frame: Math.max(0, frame - 26), fps, config: { damping: 16, stiffness: 135 } });
  const step1 = frame >= 105;
  const step2 = frame >= 145;
  const step3 = frame >= 185;

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: STAGE_PAD, fontFamily: V2_TOKENS.sans }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <div
          style={{
            background: V2_TOKENS.creamBg,
            color: V2_TOKENS.creamInk,
            borderRadius: 22,
            border: `2px solid ${V2_TOKENS.creamBorder}`,
            padding: '30px 32px',
            opacity: leftSp * (frame > 100 ? 0.82 : 1),
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <span style={{ padding: '6px 14px', borderRadius: 999, background: '#E5E7EB', color: '#374151', fontFamily: V2_TOKENS.mono, fontSize: 15, fontWeight: 800 }}>
              CHAT MODE
            </span>
            <span style={{ fontSize: 28 }}>💬</span>
          </div>
          <div style={{ fontSize: 34, fontWeight: 900, lineHeight: 1.15 }}>
            Ask a question &mdash; and sit waiting.
          </div>
        </div>

        <div
          style={{
            background: 'linear-gradient(165deg, #161B30 0%, #0D101D 100%)',
            color: V2_TOKENS.ink,
            borderRadius: 22,
            border: `2px solid ${V2_TOKENS.gold}`,
            boxShadow: '0 26px 72px rgba(0, 0, 0, 0.65)',
            padding: '32px 32px',
            display: 'flex',
            flexDirection: 'column',
            gap: 18,
            opacity: rightSp,
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ padding: '6px 16px', borderRadius: 999, background: V2_TOKENS.cobalt, color: '#FFFFFF', fontFamily: V2_TOKENS.mono, fontSize: 15, fontWeight: 800 }}>
              ✦ TASK MODE
            </span>
            <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 14, color: V2_TOKENS.emerald, fontWeight: 700 }}>CLOUD VM · WALK AWAY</span>
          </div>
          <div style={{ fontSize: 36, fontWeight: 900, lineHeight: 1.15 }}>
            Hand over a real job &mdash; <span style={{ color: V2_TOKENS.gold }}>walk away.</span>
          </div>
          {[
            { label: '1. Plans workflow in cloud', done: step1 },
            { label: '2. Browses sites & gathers facts', done: step2 },
            { label: '3. Delivers finished report', done: step3 },
          ].map((row, idx) => (
            <div
              key={idx}
              style={{
                padding: '14px 18px',
                borderRadius: 12,
                background: row.done ? 'rgba(52, 211, 153, 0.12)' : 'rgba(255,255,255,0.04)',
                border: `1px solid ${row.done ? 'rgba(52, 211, 153, 0.55)' : 'rgba(255,255,255,0.1)'}`,
                display: 'flex',
                justifyContent: 'space-between',
                fontSize: 20,
                fontWeight: 700,
              }}
            >
              <span>{row.label}</span>
              <span style={{ color: row.done ? V2_TOKENS.emerald : V2_TOKENS.muted, fontFamily: V2_TOKENS.mono }}>{row.done ? '✓' : '...'}</span>
            </div>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const PROMPT_S3_V = 'Every morning at 7:00 AM, scan the biggest AI launches and send me a one-page summary.';

const S3DailyBriefV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const showResult = frame >= 186;
  const typedCount = Math.floor(interpolate(frame, [24, 152], [0, PROMPT_S3_V.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const cursorX = interpolate(frame, [130, 164], [620, 822], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const cursorY = interpolate(frame, [130, 164], [380, 314], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const cursorOpacity = interpolate(frame, [125, 134, 178, 185], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const resultPop = spring({ frame: Math.max(0, frame - 188), fps, config: { damping: 16, stiffness: 135 } });
  const focusReady = frame >= 230;

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: STAGE_PAD, fontFamily: V2_TOKENS.sans, color: V2_TOKENS.ink }}>
      <GeminiWindowFrame badge={showResult ? 'REAL RESULT · ROUTINE SET' : 'TYPING THE TASK'} width={954} maxWidth="100%">
        {!showResult ? (
          <div style={{ padding: '42px 34px 48px', display: 'flex', flexDirection: 'column', gap: 24, position: 'relative' }}>
            <div style={{ fontSize: 32, fontWeight: 800 }}>What can I check off your list?</div>
            <div style={{ minHeight: 200, borderRadius: 18, background: '#0A0D19', border: '1.5px solid rgba(79, 140, 255, 0.5)', padding: '22px 24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', gap: 18 }}>
              <div style={{ fontSize: 26, lineHeight: 1.4, fontWeight: 500 }}>
                {PROMPT_S3_V.slice(0, typedCount)}
                <span style={{ color: V2_TOKENS.cobalt, fontWeight: 900 }}>|</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 14, color: V2_TOKENS.cobalt, fontWeight: 700 }}>✦ Task Mode</span>
                <div style={{ width: 42, height: 42, borderRadius: 999, background: typedCount > 15 ? V2_TOKENS.cobalt : 'rgba(255,255,255,0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 20, fontWeight: 900 }}>
                  ↑
                </div>
              </div>
            </div>
            <AnimatedCursor x={cursorX} y={cursorY} clickFrame={168} opacity={cursorOpacity} />
          </div>
        ) : (
          <div style={{ padding: '36px 32px 42px', display: 'flex', flexDirection: 'column', gap: 22, opacity: resultPop }}>
            <div style={{ fontSize: 25, fontWeight: 700, lineHeight: 1.38 }}>
              Done. Daily AI launches briefing set for <span style={{ color: V2_TOKENS.gold }}>7:00 AM</span>.
            </div>
            <div style={{ position: 'relative', padding: '24px 24px', borderRadius: 16, background: '#0A0D19', border: '1px solid rgba(255,255,255,0.14)', display: 'flex', flexDirection: 'column', gap: 14 }}>
              <div style={{ fontSize: 24, fontWeight: 800 }}>🕒 Summarize Daily AI Launches</div>
              <div style={{ fontSize: 18, color: V2_TOKENS.muted }}>Scans official blogs &amp; returns 1-page digest</div>
              <div style={{ display: 'flex', gap: 12, marginTop: 4 }}>
                <span style={{ padding: '7px 16px', borderRadius: 999, background: V2_TOKENS.cobaltDeep, fontFamily: V2_TOKENS.mono, fontSize: 15, fontWeight: 800 }}>DAILY · 07:00 AM</span>
                <span style={{ padding: '7px 14px', fontFamily: V2_TOKENS.mono, fontSize: 15, color: V2_TOKENS.emerald, fontWeight: 800 }}>✓ ACTIVE</span>
              </div>
              <GoldenFocusBox visible={focusReady} style={{ inset: -4, borderRadius: 18 }} />
            </div>
          </div>
        )}
      </GeminiWindowFrame>
    </AbsoluteFill>
  );
};

const S4WebResearchV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const showCanvas = frame >= 172;
  const s1 = frame >= 36;
  const s2 = frame >= 84;
  const s3 = frame >= 128;
  const canvasPop = spring({ frame: Math.max(0, frame - 174), fps, config: { damping: 16, stiffness: 135 } });
  const colFocus = frame >= 224;

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: STAGE_PAD, fontFamily: V2_TOKENS.sans, color: V2_TOKENS.ink }}>
      <GeminiWindowFrame badge={showCanvas ? 'GEMINI · CANVAS' : 'LIVE STEPS'} width={954} maxWidth="100%">
        {!showCanvas ? (
          <div style={{ padding: '36px 32px 42px', display: 'flex', flexDirection: 'column', gap: 18 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 22, fontWeight: 700, color: '#CBD5E1' }}>
              <GeminiSparkleIcon size={22} color={V2_TOKENS.cobalt} />
              <span>Thinking it through...</span>
            </div>
            {[
              { icon: 'G', title: 'Search Google for Q4 launches', done: s1, showAt: 10 },
              { icon: '🌐', title: 'Visit 8 live pricing & feature sites', done: s2, showAt: 48 },
              { icon: '📊', title: 'Build editable Canvas comparison', done: s3, showAt: 96 },
            ].map((step, i) => (
              <div
                key={i}
                style={{
                  opacity: frame >= step.showAt ? 1 : 0.25,
                  padding: '18px 20px',
                  borderRadius: 14,
                  background: step.done ? 'rgba(52, 211, 153, 0.11)' : 'rgba(255,255,255,0.04)',
                  border: `1px solid ${step.done ? 'rgba(52, 211, 153, 0.48)' : 'rgba(255,255,255,0.1)'}`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: 12,
                  fontSize: 21,
                  fontWeight: 700,
                }}
              >
                <span>{step.icon} &nbsp;{step.title}</span>
                <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 15, color: step.done ? V2_TOKENS.emerald : V2_TOKENS.gold }}>
                  {step.done ? '✓ DONE' : '...'}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <div style={{ padding: '22px 24px 28px', opacity: canvasPop }}>
            <div style={{ background: '#FFFFFF', color: '#0F172A', borderRadius: 16, overflow: 'hidden' }}>
              <div style={{ height: 42, background: '#F1F5F9', borderBottom: '1px solid #E2E8F0', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 16px' }}>
                <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 14, fontWeight: 700 }}>Canvas · Matrix.md</span>
                <span style={{ padding: '3px 10px', borderRadius: 6, background: '#2563EB', color: '#FFFFFF', fontFamily: V2_TOKENS.mono, fontSize: 12, fontWeight: 700 }}>Preview</span>
              </div>
              <div style={{ padding: '20px 22px', position: 'relative' }}>
                <div style={{ fontSize: 26, fontWeight: 900, marginBottom: 14 }}>Verified Market Comparison</div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 10, fontSize: 18 }}>
                  {[
                    ['Notion AI', 'Trial Only', 'Weak live web triggers'],
                    ['Perplexity', 'Limited', 'No background schedules'],
                    ['Gemini Tasks', 'Free + Pro', 'Cloud schedules + Drive'],
                  ].map((r, ri) => (
                    <div key={ri} style={{ padding: '12px 14px', borderRadius: 10, background: ri === 2 ? '#EFF6FF' : '#F8FAFC', border: '1px solid #E2E8F0', display: 'flex', justifyContent: 'space-between', fontWeight: ri === 2 ? 800 : 600 }}>
                      <span>{r[0]}</span>
                      <span style={{ color: ri === 2 ? '#2563EB' : '#475569' }}>{r[2]}</span>
                    </div>
                  ))}
                </div>
                <GoldenFocusBox visible={colFocus} style={{ left: 18, right: 18, bottom: 16, height: 50, borderRadius: 12 }} />
              </div>
            </div>
          </div>
        )}
      </GeminiWindowFrame>
    </AbsoluteFill>
  );
};

const S5MonitorsV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const quotePop = spring({ frame: Math.max(0, frame - 150), fps, config: { damping: 14, stiffness: 140 } });
  const rows = [
    { time: 'MON 08:00', name: 'Site & SSL Health Watch', badge: 'WEEKLY', delay: 14 },
    { time: 'DAILY 09:00', name: 'Flight & Hotel Price Check', badge: 'MONITOR', delay: 62 },
    { time: 'GMAIL · LIVE', name: 'Flag Mail & Draft Replies', badge: 'GMAIL', delay: 110 },
  ];

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: STAGE_PAD, fontFamily: V2_TOKENS.sans }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 22 }}>
        <div style={{ borderRadius: 22, background: 'linear-gradient(165deg, #131A35 0%, #0A0E1F 100%)', border: `1.5px solid ${V2_TOKENS.goldBorder}`, padding: '26px 26px', color: V2_TOKENS.ink }}>
          <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 15, fontWeight: 800, color: V2_TOKENS.muted, marginBottom: 16 }}>
            🕒 YOUR ROUTINE · RUNS ON ITS OWN
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {rows.map((r, i) => {
              const sp = spring({ frame: Math.max(0, frame - r.delay), fps, config: { damping: 16, stiffness: 145 } });
              return (
                <div key={i} style={{ opacity: sp, padding: '16px 18px', borderRadius: 14, background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 14, fontWeight: 800, color: V2_TOKENS.gold }}>{r.time}</div>
                    <div style={{ fontSize: 22, fontWeight: 800, marginTop: 4 }}>{r.name}</div>
                  </div>
                  <span style={{ padding: '6px 14px', borderRadius: 8, background: V2_TOKENS.cobaltDeep, fontFamily: V2_TOKENS.mono, fontSize: 14, fontWeight: 800 }}>{r.badge}</span>
                </div>
              );
            })}
          </div>
        </div>

        <div style={{ background: V2_TOKENS.creamBg, color: V2_TOKENS.creamInk, borderRadius: 18, border: `2px solid ${V2_TOKENS.cobalt}`, padding: '22px 26px', opacity: quotePop, transform: 'rotate(-1deg)' }}>
          <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 13, fontWeight: 800, color: V2_TOKENS.cobaltDeep, marginBottom: 6 }}>BEFORE MONDAY MORNING</div>
          <div style={{ fontSize: 24, fontWeight: 800, lineHeight: 1.3 }}>
            &ldquo;Flags urgent emails, price drops, and drafts replies before Monday morning.&rdquo;
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S6PermissionV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const connected = frame >= 184;
  const cursorX = interpolate(frame, [115, 178], [320, 745], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const cursorY = interpolate(frame, [115, 178], [410, 336], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const cursorOpacity = interpolate(frame, [110, 120, 225, 240], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const quotePop = spring({ frame: Math.max(0, frame - 205), fps, config: { damping: 14, stiffness: 150 } });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: STAGE_PAD, fontFamily: V2_TOKENS.sans, color: V2_TOKENS.ink }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <GeminiWindowFrame badge={connected ? 'ACCESS GRANTED' : 'WAITING FOR INPUT'} width={954} maxWidth="100%">
          <div style={{ padding: '32px 30px 36px', display: 'flex', flexDirection: 'column', gap: 20, position: 'relative' }}>
            <div style={{ fontSize: 25, fontWeight: 700, lineHeight: 1.38 }}>
              Sure. First, I&apos;ll need your permission to turn on Google Drive.
            </div>
            <div style={{ borderRadius: 16, background: '#0A0D19', border: `1.5px solid ${connected ? V2_TOKENS.emerald : 'rgba(255,255,255,0.16)'}`, padding: '22px 24px', display: 'flex', flexDirection: 'column', gap: 18 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                <GoogleDriveTriangleIcon size={38} />
                <div>
                  <div style={{ fontSize: 24, fontWeight: 800 }}>Google Drive</div>
                  <div style={{ fontSize: 16, color: V2_TOKENS.muted }}>Connect only when you approve</div>
                </div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 12, position: 'relative' }}>
                {!connected && (
                  <span style={{ padding: '10px 18px', borderRadius: 999, background: 'rgba(255,255,255,0.08)', fontSize: 18, fontWeight: 700, color: V2_TOKENS.muted }}>
                    No thanks
                  </span>
                )}
                <span style={{ padding: '10px 24px', borderRadius: 999, background: connected ? V2_TOKENS.emerald : V2_TOKENS.cobalt, color: connected ? '#062016' : '#FFFFFF', fontSize: 19, fontWeight: 900 }}>
                  {connected ? '✓ Connected' : 'Connect'}
                </span>
                <GoldenFocusBox visible={!connected && frame >= 75} style={{ right: -4, top: -4, bottom: -4, width: 136, borderRadius: 999 }} />
              </div>
            </div>
            <AnimatedCursor x={cursorX} y={cursorY} clickFrame={182} opacity={cursorOpacity} />
          </div>
        </GeminiWindowFrame>

        <div style={{ opacity: quotePop, alignSelf: 'center', background: V2_TOKENS.creamBg, color: V2_TOKENS.creamInk, borderRadius: 16, border: `2px solid ${V2_TOKENS.gold}`, padding: '18px 34px', fontSize: 30, fontWeight: 900, fontStyle: 'italic' }}>
          &ldquo;Nothing leaves without a <span style={{ color: V2_TOKENS.cobaltDeep }}>yes</span>.&rdquo;
        </div>
      </div>
    </AbsoluteFill>
  );
};

const S7AvailabilityV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const proSp = spring({ frame: Math.max(0, frame - 210), fps, config: { damping: 16, stiffness: 135 } });
  const countries = ['THE US', 'CANADA', 'JAPAN', 'SOUTH KOREA', 'AUSTRALIA', 'INDIA'];

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: STAGE_PAD, fontFamily: V2_TOKENS.sans }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          {countries.map((name, idx) => {
            const sp = spring({ frame: Math.max(0, frame - (10 + idx * 14)), fps, config: { damping: 15, stiffness: 150 } });
            return (
              <div key={name} style={{ background: V2_TOKENS.creamBg, color: V2_TOKENS.creamInk, borderRadius: 16, border: `2px solid ${V2_TOKENS.creamBorder}`, padding: '20px 22px', opacity: sp }}>
                <div style={{ fontSize: 26, fontWeight: 900 }}>{name}</div>
                <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 13, fontWeight: 800, color: V2_TOKENS.cobaltDeep, marginTop: 6 }}>
                  FREE · 10 SCHEDULES
                </div>
              </div>
            );
          })}
        </div>

        <div style={{ opacity: proSp, borderRadius: 20, background: 'linear-gradient(165deg, #1A1738 0%, #0D1020 100%)', border: `2px solid ${V2_TOKENS.gold}`, padding: '24px 28px', color: V2_TOKENS.ink, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 14, fontWeight: 800, color: V2_TOKENS.gold }}>PRO &amp; ULTRA · GLOBAL</div>
            <div style={{ fontSize: 24, fontWeight: 800, marginTop: 4 }}>Full Automation Unlock</div>
          </div>
          <div style={{ display: 'flex', gap: 28 }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 44, fontWeight: 900, color: V2_TOKENS.gold }}>50</div>
              <div style={{ fontSize: 14, color: '#FDE68A' }}>Schedules</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontFamily: V2_TOKENS.mono, fontSize: 44, fontWeight: 900, color: V2_TOKENS.emerald }}>15</div>
              <div style={{ fontSize: 14, color: '#A7F3D0' }}>Parallel</div>
            </div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const SKILL_TYPED_V = '/weekly-brief';

const S8ProTipsV: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const showSkillBeat = frame >= 248;
  const barPct = interpolate(frame, [20, 150], [18, 92], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const typedLen = Math.floor(interpolate(frame, [260, 325], [0, SKILL_TYPED_V.length], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const skillChosen = frame >= 390;
  const tip2Pop = spring({ frame: Math.max(0, frame - 252), fps, config: { damping: 16, stiffness: 135 } });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: STAGE_PAD, fontFamily: V2_TOKENS.sans, color: V2_TOKENS.ink }}>
      {!showSkillBeat ? (
        <GeminiWindowFrame badge="TIP 1 · COMPUTE BUDGET" width={954} maxWidth="100%">
          <div style={{ padding: '34px 30px 38px', display: 'flex', flexDirection: 'column', gap: 22 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ fontSize: 28, fontWeight: 900 }}>5-Hour Rolling Budget</div>
              <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 20, fontWeight: 800, color: V2_TOKENS.coral }}>{Math.round(barPct)}%</span>
            </div>
            <div style={{ height: 22, borderRadius: 999, background: 'rgba(255,255,255,0.08)', overflow: 'hidden' }}>
              <div style={{ height: '100%', width: `${barPct}%`, background: `linear-gradient(90deg, ${V2_TOKENS.cobalt}, ${V2_TOKENS.gold}, ${V2_TOKENS.coral})`, borderRadius: 999 }} />
            </div>
            <div style={{ padding: '20px 22px', borderRadius: 16, background: 'rgba(251, 113, 133, 0.10)', border: `1.5px solid ${V2_TOKENS.coral}`, fontSize: 23, fontWeight: 800, textDecoration: 'line-through', textDecorationColor: V2_TOKENS.coral }}>
              ✗ Dumping 10 jobs into 1 prompt
            </div>
            <div style={{ padding: '20px 22px', borderRadius: 16, background: 'rgba(52, 211, 153, 0.12)', border: `2px solid ${V2_TOKENS.emerald}`, fontSize: 24, fontWeight: 800 }}>
              ✓ Keep each prompt tightly scoped
            </div>
          </div>
        </GeminiWindowFrame>
      ) : (
        <div style={{ opacity: tip2Pop }}>
          <GeminiWindowFrame badge="TIP 2 · SLASH SKILLS" width={954} maxWidth="100%">
            <div style={{ padding: '34px 30px 38px', display: 'flex', flexDirection: 'column', gap: 20 }}>
              <div style={{ fontSize: 29, fontWeight: 900 }}>
                Save Repeat Flows as <span style={{ color: V2_TOKENS.cobalt }}>/Skills</span>
              </div>
              <div style={{ borderRadius: 16, background: '#0A0D19', border: `1.5px solid ${V2_TOKENS.cobalt}`, padding: '18px 22px', fontFamily: V2_TOKENS.mono, fontSize: 24, fontWeight: 800 }}>
                {skillChosen ? (
                  <span style={{ padding: '6px 16px', borderRadius: 999, background: V2_TOKENS.cobaltDeep, color: '#FFFFFF' }}>
                    /weekly-brief · 1-Click Reuse
                  </span>
                ) : (
                  <span>
                    {SKILL_TYPED_V.slice(0, typedLen)}
                    <span style={{ color: V2_TOKENS.cobalt }}>|</span>
                  </span>
                )}
              </div>
              <div style={{ borderRadius: 14, background: '#171C30', border: '1px solid rgba(255,255,255,0.14)', padding: 10, display: 'flex', flexDirection: 'column', gap: 8 }}>
                {['/weekly-brief', '/inbox-triage', '/price-watch'].map((cmd, ci) => (
                  <div key={cmd} style={{ padding: '12px 16px', borderRadius: 10, background: ci === 0 ? 'rgba(79, 140, 255, 0.18)' : 'transparent', border: `1.5px solid ${ci === 0 ? V2_TOKENS.gold : 'transparent'}`, fontFamily: V2_TOKENS.mono, fontSize: 20, fontWeight: 800, color: ci === 0 ? '#93C5FD' : V2_TOKENS.ink }}>
                    {cmd}
                  </div>
                ))}
              </div>
            </div>
          </GeminiWindowFrame>
        </div>
      )}
    </AbsoluteFill>
  );
};

const S9FiveStepsV: React.FC = () => {
  const frame = useCurrentFrame();
  const steps = [
    { num: '1', label: 'OPEN GEMINI', tag: 'APP', activeAt: 16 },
    { num: '2', label: 'CLICK TASK', tag: 'TOGGLE', activeAt: 58 },
    { num: '3', label: 'DESCRIBE ONE JOB', tag: 'SCOPE', activeAt: 102 },
    { num: '4', label: 'PUT TIMING FIRST', tag: '7 AM', activeAt: 152 },
    { num: '5', label: 'REVIEW FIRST RUN', tag: 'FOLLOW', activeAt: 204 },
  ];

  return (
    <AbsoluteFill style={{ justifyContent: 'center', padding: STAGE_PAD, fontFamily: V2_TOKENS.sans, color: V2_TOKENS.ink }}>
      <GeminiWindowFrame badge="STEP BY STEP" width={954} maxWidth="100%">
        <div style={{ padding: '28px 26px 32px', display: 'flex', flexDirection: 'column', gap: 14 }}>
          {steps.map((s) => {
            const lit = frame >= s.activeAt;
            return (
              <div key={s.num} style={{ padding: '16px 20px', borderRadius: 14, background: lit ? 'rgba(79, 140, 255, 0.16)' : 'rgba(255,255,255,0.04)', border: `1.5px solid ${lit ? V2_TOKENS.gold : 'rgba(255,255,255,0.1)'}`, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
                  <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 24, fontWeight: 900, color: lit ? V2_TOKENS.gold : V2_TOKENS.muted }}>{s.num}</span>
                  <span style={{ fontSize: 25, fontWeight: 900 }}>{s.label}</span>
                </div>
                <span style={{ padding: '5px 12px', borderRadius: 8, background: lit ? V2_TOKENS.cobaltDeep : 'rgba(255,255,255,0.08)', fontFamily: V2_TOKENS.mono, fontSize: 13, fontWeight: 800 }}>
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

const SCENES_V: Record<string, React.FC> = {
  s1: S1SwitchV,
  s2: S2ConciergeV,
  s3: S3DailyBriefV,
  s4: S4WebResearchV,
  s5: S5MonitorsV,
  s6: S6PermissionV,
  s7: S7AvailabilityV,
  s8: S8ProTipsV,
  s9: S9FiveStepsV,
};

export const Ep02MainVertical: React.FC = () => {
  const frame = useCurrentFrame();
  const active = SHOTS_EP02.find((s) => frame >= s.start && frame < s.end) ?? SHOTS_EP02[SHOTS_EP02.length - 1];
  const isCover = frame < 12;

  return (
    <AbsoluteFill>
      <AtmosphericStudioBackdrop />
      <Audio src={staticFile('voice_ep02_mix.mp3')} />
      {isCover ? (
        <CoverPosterVertical />
      ) : (
        <>
          <TopLeftKicker tag={active.tag} headline={active.headline} accentWord={active.accentWord} top={92} left={48} fontSize={27} />
          {SHOTS_EP02.map((shot) => {
            const Scene = SCENES_V[shot.id];
            return (
              <Sequence key={shot.id} from={shot.start} durationInFrames={shot.end - shot.start}>
                <Scene />
              </Sequence>
            );
          })}
          <WhitePillCaption bottom={245} fontSize={33} maxWidth={860} />
        </>
      )}
    </AbsoluteFill>
  );
};
