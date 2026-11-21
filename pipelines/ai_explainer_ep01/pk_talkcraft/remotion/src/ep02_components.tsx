import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { CAPTIONS_EP02 } from './captions_ep02';

export const V2_TOKENS = {
  bg0: '#080A18',
  bg1: '#151232',
  windowBg: '#121626',
  windowBgDeep: '#0B0E1A',
  gold: '#FBBF24',
  goldBorder: 'rgba(251, 191, 36, 0.48)',
  cobalt: '#4F8CFF',
  cobaltDeep: '#2563EB',
  emerald: '#34D399',
  coral: '#FB7185',
  coralText: '#EA580C',
  lavender: '#A78BFA',
  ink: '#F8FAFC',
  muted: '#94A3B8',
  creamBg: '#F8F6F1',
  creamBorder: '#E5DEC9',
  creamInk: '#111827',
  creamMuted: '#4B5563',
  sans: '"SF Pro Display", "Inter", -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif',
  mono: '"SF Mono", "JetBrains Mono", Menlo, monospace',
} as const;

const STARS = Array.from({ length: 44 }, (_, i) => ({
  x: (i * 197 + 31) % 100,
  y: (i * 293 + 17) % 100,
  r: (i % 3) + 1.1,
  phase: i * 0.72,
}));

export const AtmosphericStudioBackdrop: React.FC = () => {
  const frame = useCurrentFrame();
  const driftY = (frame * 0.12) % 1080;
  const breathe = 0.5 + 0.5 * Math.sin(frame * 0.03);

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 76% 24%, rgba(245, 158, 11, ${0.11 + 0.04 * breathe}), transparent 42%),
                     radial-gradient(circle at 20% 22%, rgba(79, 140, 255, ${0.15 + 0.04 * breathe}), transparent 46%),
                     radial-gradient(circle at 52% 84%, rgba(167, 139, 250, 0.12), transparent 50%),
                     linear-gradient(155deg, ${V2_TOKENS.bg0} 0%, ${V2_TOKENS.bg1} 58%, #070916 100%)`,
      }}
    >
      {/* Subtle studio desk perspective horizon glow */}
      <div
        style={{
          position: 'absolute',
          left: '10%',
          right: '10%',
          bottom: '-18%',
          height: '44%',
          borderRadius: '50%',
          background: 'radial-gradient(ellipse at center, rgba(251, 191, 36, 0.09) 0%, transparent 72%)',
          filter: 'blur(26px)',
        }}
      />
      {STARS.map((s, idx) => {
        const twinkle = 0.22 + 0.55 * (0.5 + 0.5 * Math.sin(frame * 0.075 + s.phase));
        const yPct = (s.y + (driftY / 1080) * 16) % 100;
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
              background: idx % 6 === 0 ? '#FDE68A' : idx % 3 === 0 ? '#DDD6FE' : '#E2E8F0',
              opacity: twinkle,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

export const TopLeftKicker: React.FC<{
  tag: string;
  headline: string;
  accentWord: string;
  top?: number;
  left?: number;
  fontSize?: number;
}> = ({ tag, headline, accentWord, top = 28, left = 48, fontSize = 30 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = spring({ frame, fps, config: { damping: 18, stiffness: 150 } });

  return (
    <div
      style={{
        position: 'absolute',
        top,
        left,
        zIndex: 30,
        display: 'flex',
        alignItems: 'center',
        gap: 14,
        fontFamily: V2_TOKENS.sans,
        opacity: sp,
        transform: `translateY(${interpolate(sp, [0, 1], [-8, 0])}px)`,
      }}
    >
      <div
        style={{
          padding: '6px 14px',
          borderRadius: 6,
          background: 'rgba(248, 250, 252, 0.94)',
          color: '#0F172A',
          fontFamily: V2_TOKENS.mono,
          fontSize: Math.max(13, Math.round(fontSize * 0.48)),
          fontWeight: 800,
          letterSpacing: '0.06em',
          textTransform: 'uppercase',
          boxShadow: '0 6px 18px rgba(0,0,0,0.35)',
        }}
      >
        {tag}
      </div>
      <div
        style={{
          fontSize,
          fontWeight: 900,
          letterSpacing: '-0.02em',
          textTransform: 'uppercase',
          color: V2_TOKENS.ink,
          textShadow: '0 2px 14px rgba(0,0,0,0.65)',
        }}
      >
        {headline}{' '}
        <span style={{ color: V2_TOKENS.cobalt }}>{accentWord}</span>
      </div>
    </div>
  );
};

export const GeminiSparkleIcon: React.FC<{ size?: number; color?: string }> = ({
  size = 24,
  color = V2_TOKENS.cobalt,
}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <path
      d="M12 2C12.7 7.2 16.8 11.3 22 12C16.8 12.7 12.7 16.8 12 22C11.3 16.8 7.2 12.7 2 12C7.2 11.3 11.3 7.2 12 2Z"
      fill={color}
    />
  </svg>
);

export const GeminiWindowFrame: React.FC<{
  badge: string;
  width: number;
  maxWidth?: string;
  subtitleRight?: string;
  children: React.ReactNode;
}> = ({ badge, width, maxWidth = '92%', subtitleRight = 'gemini.google.com', children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame, fps, config: { damping: 17, stiffness: 135 } });

  return (
    <div
      style={{
        width,
        maxWidth,
        borderRadius: 22,
        background: `linear-gradient(170deg, rgba(20, 24, 42, 0.96) 0%, rgba(11, 14, 26, 0.98) 100%)`,
        border: `1.5px solid ${V2_TOKENS.goldBorder}`,
        boxShadow: '0 36px 96px rgba(0, 0, 0, 0.68), 0 0 42px rgba(251, 191, 36, 0.10)',
        overflow: 'hidden',
        transform: `translateY(${interpolate(enter, [0, 1], [18, 0])}px) scale(${interpolate(enter, [0, 1], [0.97, 1])})`,
        opacity: enter,
      }}
    >
      <div
        style={{
          height: 46,
          background: 'rgba(255, 255, 255, 0.03)',
          borderBottom: '1px solid rgba(251, 191, 36, 0.16)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 20px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <div style={{ display: 'flex', gap: 7 }}>
            <span style={{ width: 11, height: 11, borderRadius: 999, background: '#FB7185' }} />
            <span style={{ width: 11, height: 11, borderRadius: 999, background: '#FBBF24' }} />
            <span style={{ width: 11, height: 11, borderRadius: 999, background: '#34D399' }} />
          </div>
          <span style={{ fontFamily: V2_TOKENS.mono, fontSize: 13, color: V2_TOKENS.muted }}>
            {subtitleRight}
          </span>
        </div>
        <div
          style={{
            padding: '4px 12px',
            borderRadius: 999,
            background: 'rgba(251, 191, 36, 0.14)',
            border: '1px solid rgba(251, 191, 36, 0.45)',
            color: '#FDE68A',
            fontFamily: V2_TOKENS.mono,
            fontSize: 12,
            fontWeight: 700,
            letterSpacing: '0.05em',
          }}
        >
          {badge}
        </div>
      </div>
      {children}
    </div>
  );
};

export const AnimatedCursor: React.FC<{
  x: number;
  y: number;
  clickFrame?: number;
  opacity?: number;
}> = ({ x, y, clickFrame = -1, opacity = 1 }) => {
  const frame = useCurrentFrame();
  const sinceClick = clickFrame >= 0 ? frame - clickFrame : -1;
  const isClicking = sinceClick >= 0 && sinceClick <= 12;
  const pressScale =
    sinceClick >= 0 && sinceClick <= 6
      ? interpolate(sinceClick, [0, 3, 6], [1, 0.82, 1])
      : 1;
  const rippleProgress = isClicking ? interpolate(sinceClick, [0, 12], [0, 1]) : 0;

  if (opacity <= 0.01) return null;

  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        zIndex: 60,
        pointerEvents: 'none',
        opacity,
        transform: `translate(-4px, -4px) scale(${pressScale})`,
      }}
    >
      {isClicking && (
        <div
          style={{
            position: 'absolute',
            left: -18,
            top: -18,
            width: 44,
            height: 44,
            borderRadius: 999,
            border: `2.5px solid ${V2_TOKENS.gold}`,
            transform: `scale(${0.4 + rippleProgress * 1.4})`,
            opacity: 1 - rippleProgress,
          }}
        />
      )}
      <svg width={32} height={32} viewBox="0 0 28 28" fill="none" style={{ filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.55))' }}>
        <path
          d="M5 3L21 13.5L13.5 15.3L10.3 22.5L5 3Z"
          fill="#FFFFFF"
          stroke="#0F172A"
          strokeWidth="2"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
};

export const GoldenFocusBox: React.FC<{
  visible: boolean;
  style?: React.CSSProperties;
}> = ({ visible, style }) => {
  if (!visible) return null;
  return (
    <div
      style={{
        position: 'absolute',
        borderRadius: 12,
        border: `2.5px solid ${V2_TOKENS.gold}`,
        background: 'rgba(251, 191, 36, 0.08)',
        boxShadow: '0 0 26px rgba(251, 191, 36, 0.34), inset 0 0 14px rgba(251, 191, 36, 0.12)',
        pointerEvents: 'none',
        zIndex: 25,
        ...style,
      }}
    />
  );
};

export const WhitePillCaption: React.FC<{
  bottom?: number;
  fontSize?: number;
  maxWidth?: number;
}> = ({ bottom = 36, fontSize = 30, maxWidth = 900 }) => {
  const frame = useCurrentFrame();
  if (frame < 12) return null;

  const pill = CAPTIONS_EP02.pills.find((p) => frame >= p.startFrame && frame < p.endFrame);
  if (!pill) return null;

  const localF = frame - pill.startFrame;
  const pop = interpolate(localF, [0, 3], [0.95, 1], { extrapolateRight: 'clamp' });
  const highlight = pill.accentColor === 'coral' ? V2_TOKENS.coralText : V2_TOKENS.cobaltDeep;

  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        bottom,
        display: 'flex',
        justifyContent: 'center',
        zIndex: 70,
        pointerEvents: 'none',
        fontFamily: V2_TOKENS.sans,
      }}
    >
      <div
        style={{
          maxWidth,
          padding: '10px 26px',
          borderRadius: 12,
          background: '#FFFFFF',
          boxShadow: '0 12px 32px rgba(0, 0, 0, 0.52)',
          display: 'inline-flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: '0 9px',
          transform: `scale(${pop})`,
        }}
      >
        {pill.words.map((w, idx) => (
          <span
            key={idx}
            style={{
              fontSize,
              fontWeight: 900,
              letterSpacing: '-0.02em',
              color: w.accent ? highlight : '#0F172A',
            }}
          >
            {w.text}
          </span>
        ))}
      </div>
    </div>
  );
};

export const GoogleDriveTriangleIcon: React.FC<{ size?: number }> = ({ size = 28 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <path d="M8.5 3.5H15.5L21 13L17.5 19H6.5L3 13L8.5 3.5Z" fill="none" />
    <path d="M9 4L15 4L21 14L18 19L12 9L9 4Z" fill="#FBBC05" />
    <path d="M9 4L3 14L6 19L12 9L9 4Z" fill="#0F9D58" />
    <path d="M6 19H18L21 14H9L6 19Z" fill="#4285F4" />
  </svg>
);
