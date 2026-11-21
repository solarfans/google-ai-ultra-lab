import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { SHOTS, T } from './theme';

const CHAPTERS = [
  { id: 1, label: '01 三条分工线' },
  { id: 2, label: '02 Neon 主力与红线' },
  { id: 3, label: '03 Carbon / Hydrogen 避坑' },
  { id: 4, label: '04 抄作业公式' },
];

const DotGridBackdrop: React.FC = () => {
  const frame = useCurrentFrame();
  const drift = (frame * 0.35) % 36;
  return (
    <AbsoluteFill
      style={{
        backgroundColor: T.bg,
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
      borderBottom: `1px solid ${T.border}`,
      paddingBottom: 14,
      zIndex: 20,
      fontFamily: T.sans,
    }}
  >
    <div style={{ display: 'flex', alignItems: 'center', gap: 12, fontFamily: T.mono, fontSize: 18, letterSpacing: '0.05em', color: T.ink }}>
      <span style={{ width: 10, height: 10, borderRadius: 999, background: T.amber, display: 'inline-block' }} />
      <span>GOOGLE GEMINI 4 · 2026-11 实测选型指南</span>
    </div>
    <div style={{ display: 'flex', gap: 28, fontSize: 18, fontWeight: 600 }}>
      {CHAPTERS.map((ch) => {
        const active = ch.id === activeChapter;
        return (
          <span
            key={ch.id}
            style={{
              color: active ? T.ink : '#64748B',
              borderBottom: active ? `2px solid ${T.amber}` : '2px solid transparent',
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

const HostPip: React.FC<{ badge: string }> = ({ badge }) => (
  <div
    style={{
      position: 'absolute',
      left: 64,
      bottom: 126,
      width: 396,
      height: 223,
      borderRadius: 20,
      overflow: 'hidden',
      border: '2px solid rgba(245, 158, 11, 0.55)',
      boxShadow: '0 20px 50px rgba(0, 0, 0, 0.65)',
      background: '#0F131B',
      zIndex: 30,
    }}
  >
    <Img src={staticFile('anchor.png')} style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'center 22%' }} />
    <div
      style={{
        position: 'absolute',
        left: 14,
        bottom: 12,
        background: 'rgba(11, 14, 20, 0.85)',
        border: '1px solid rgba(241, 245, 249, 0.16)',
        padding: '4px 12px',
        borderRadius: 999,
        fontSize: 15,
        fontWeight: 600,
        color: T.ink,
        fontFamily: T.sans,
      }}
    >
      {badge}
    </div>
  </div>
);

const SubtitleBar: React.FC<{ text: string }> = ({ text }) => (
  <div style={{ position: 'absolute', left: 64, right: 64, bottom: 44, textAlign: 'center', zIndex: 40, fontFamily: T.sans }}>
    <span
      style={{
        display: 'inline-block',
        padding: '10px 26px',
        borderRadius: 12,
        background: 'rgba(11, 14, 20, 0.90)',
        border: '1px solid rgba(241, 245, 249, 0.15)',
        fontSize: 28,
        fontWeight: 600,
        color: T.ink,
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
  const pushScale = interpolate(frame, [0, 161], [1.0, 1.045], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ fontFamily: T.sans, color: T.ink }}>
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
        <div
          style={{
            position: 'relative',
            width: 740,
            height: 610,
            borderRadius: 24,
            overflow: 'hidden',
            border: '1.5px solid rgba(241, 245, 249, 0.16)',
            boxShadow: '0 28px 64px rgba(0, 0, 0, 0.6)',
          }}
        >
          <Img
            src={staticFile('anchor.png')}
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
              left: 24,
              bottom: 24,
              background: 'rgba(11, 14, 20, 0.84)',
              border: `1px solid ${T.border}`,
              borderRadius: 12,
              padding: '10px 18px',
              fontSize: 20,
              fontWeight: 600,
            }}
          >
            炭黑演播室 · 硬核实测版
          </div>
        </div>

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
              fontSize: 24,
              fontWeight: 600,
              marginBottom: 22,
              transform: `translateX(${interpolate(enter, [0, 1], [24, 0])}px)`,
              opacity: enter,
            }}
          >
            Q：Google 8 天连发 3 款 Gemini 4，日常到底怎么选？
          </div>
          <div
            style={{
              fontSize: 56,
              lineHeight: 1.2,
              fontWeight: 800,
              letterSpacing: '-0.02em',
              marginBottom: 26,
              transform: `translateY(${interpolate(enter, [0, 1], [16, 0])}px)`,
              opacity: enter,
            }}
          >
            <span style={{ color: T.amber }}>Google</span> 8 天连发 <span style={{ color: T.amber }}>Gemini 4</span>
            <br />
            <span style={{ fontFamily: T.mono, color: T.amber }}>27</span> 个档位别靠猜，按分工锁死
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 18, marginBottom: 24 }}>
            {[
              { date: '11月10日', sym: 'C', name: 'Gemini 4 Carbon', sub: '重型坦克 · 8%', color: T.red, border: 'rgba(229, 72, 77, 0.5)', bg: T.panel, delay: 8 },
              { date: '11月12日', sym: 'H', name: 'Gemini 4 Hydrogen', sub: '极速工兵 · 15%', color: T.green, border: 'rgba(34, 197, 94, 0.5)', bg: T.panel, delay: 14 },
              { date: '11月18日', sym: 'Ne', name: 'Gemini 4 Neon ★', sub: '日常主力 · 75%', color: T.amber, border: 'rgba(245, 158, 11, 0.7)', bg: 'rgba(245, 158, 11, 0.08)', delay: 20 },
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
                  <div style={{ fontSize: 16, color: T.muted, fontFamily: T.mono }}>{el.date}</div>
                  <div style={{ fontSize: 44, fontWeight: 800, color: el.color, margin: '6px 0 4px' }}>{el.sym}</div>
                  <div style={{ fontSize: 20, fontWeight: 700 }}>{el.name}</div>
                  <div style={{ fontSize: 16, color: el.sym === 'Ne' ? '#FCD34D' : T.muted, marginTop: 6 }}>{el.sub}</div>
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
            <span style={{ fontSize: 22, fontWeight: 600 }}>Google Antigravity 实测模型菜单</span>
            <span style={{ fontSize: 26, fontWeight: 800, color: T.amber, fontFamily: T.mono }}>11 组 / 27 个档位</span>
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
    <AbsoluteFill style={{ fontFamily: T.sans, color: T.ink }}>
      <HostPip badge="22% PiP · 实测拆解" />
      <div style={{ position: 'absolute', top: 110, left: 500, right: 64, bottom: 126, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 22 }}>
        <div style={{ fontSize: 44, fontWeight: 800 }}>
          <span style={{ color: T.amber }}>Google Gemini 4</span> 不是排强弱，而是 <span style={{ color: T.amber }}>3 条分工线</span>
        </div>
        <div style={{ background: T.panel, border: `1px solid ${T.border}`, borderRadius: 18, padding: '28px 34px', display: 'flex', flexDirection: 'column', gap: 24 }}>
          {[
            { label: '10 Ne · Gemini 4 Neon（日常开发 / 问答主力）', pct: 75, color: T.amber, delay: 4 },
            { label: '01 H · Gemini 4 Hydrogen（改小脚本 / 单测十几秒）', pct: 15, color: T.green, delay: 12 },
            { label: '06 C · Gemini 4 Carbon（10+ 文件大重构 / 核心风控）', pct: 8, color: T.red, delay: 20 },
          ].map((r) => {
            const p = spring({ frame: Math.max(0, frame - r.delay), fps, config: { damping: 18, stiffness: 110 } });
            return (
              <div key={r.label}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 24, fontWeight: 700 }}>
                  <span>{r.label}</span>
                  <span style={{ fontFamily: T.mono, color: r.color }}>{r.pct}%</span>
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
    <AbsoluteFill style={{ fontFamily: T.sans, color: T.ink }}>
      <HostPip badge="主理人实测 · Neon 篇" />
      <div style={{ position: 'absolute', top: 110, left: 500, right: 64, bottom: 126, display: 'flex', flexDirection: 'column', gap: 22 }}>
        <div
          style={{
            background: T.panel,
            border: `1px solid ${T.border}`,
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
                background: T.amberSoft,
                border: `2px solid ${T.amber}`,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
              }}
            >
              <span style={{ fontFamily: T.mono, fontSize: 15, color: T.amber }}>10</span>
              <span style={{ fontSize: 34, fontWeight: 800 }}>Ne</span>
            </div>
            <div>
              <div style={{ fontSize: 38, fontWeight: 800 }}>Google Gemini 4 Neon</div>
              <div style={{ fontSize: 20, color: T.muted, marginTop: 4 }}>Agent Arena 1336 分 · 单任务中位仅 $2.82</div>
            </div>
          </div>
          <div
            style={{
              padding: '12px 24px',
              borderRadius: 12,
              background: 'rgba(245, 158, 11, 0.16)',
              border: `1px solid ${T.amber}`,
              fontSize: 25,
              fontWeight: 800,
              color: '#FCD34D',
              fontFamily: T.mono,
            }}
          >
            日常锁死 75% 主力
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 22 }}>
          {[
            { label: 'AA Coding Agent Index', val: '#1 · 58.6', sub: '压过 Fable 58.47 / Opus 58.16', subColor: T.green, pct: 92, color: T.amber, delay: 4 },
            { label: '对比 Carbon 任务成本', val: '-32%', sub: 'Zapier 自动化榜 #1（56.3%）', subColor: T.muted, pct: 68, color: T.green, delay: 12 },
            { label: '企业实测平均提速', val: '~3.0x', sub: '告别小改干等 7–8 分钟', subColor: T.muted, pct: 85, color: T.cyan, delay: 20 },
          ].map((m) => {
            const sp = spring({ frame: Math.max(0, frame - m.delay), fps, config: { damping: 16, stiffness: 120 } });
            return (
              <div
                key={m.label}
                style={{
                  background: T.panel,
                  border: `1px solid ${T.border}`,
                  borderRadius: 18,
                  padding: '24px 28px',
                  transform: `translateY(${interpolate(sp, [0, 1], [18, 0])}px)`,
                  opacity: sp,
                }}
              >
                <div style={{ fontSize: 20, color: T.muted }}>{m.label}</div>
                <div style={{ fontSize: 54, fontWeight: 800, fontFamily: T.mono, color: m.color, margin: '10px 0 6px' }}>{m.val}</div>
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
            <span style={{ fontSize: 26, fontWeight: 700, color: '#FCA5A5' }}>⚠ 实测避坑红线：单会话上下文过 200K 明显掉速</span>
            <span style={{ fontFamily: T.mono, fontSize: 22, color: T.muted }}>硬上限 512K</span>
          </div>
          <div style={{ position: 'relative', height: 22, background: '#1E2533', borderRadius: 999, margin: '18px 0 12px', overflow: 'hidden' }}>
            <div style={{ position: 'absolute', left: 0, top: 0, bottom: 0, width: `${fastFill}%`, background: T.green }} />
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
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 19, fontFamily: T.mono }}>
            <span style={{ color: T.green }}>0 – 200K · 极速甜蜜区</span>
            <span style={{ color: T.red, fontWeight: 700 }}>▲ 200K 减速带（换任务即开新对话）</span>
            <span style={{ color: T.muted }}>512K 封顶</span>
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
  const secs = Math.round(interpolate(frame, [8, 70], [0, 450], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }));
  const mm = String(Math.floor(secs / 60)).padStart(2, '0');
  const ss = String(secs % 60).padStart(2, '0');
  return (
    <AbsoluteFill style={{ fontFamily: T.sans, color: T.ink }}>
      <HostPip badge="重型坦克 · Carbon" />
      <div style={{ position: 'absolute', top: 110, left: 500, right: 64, bottom: 126, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <div
          style={{
            background: T.panel,
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
            <div style={{ fontSize: 22, color: T.red, fontWeight: 700 }}>06 C · GOOGLE GEMINI 4 CARBON（仅占 8%）</div>
            <div style={{ fontSize: 48, fontWeight: 800, margin: '12px 0 18px' }}>排雷最深，但别当日常买菜车</div>
            <div style={{ fontSize: 24, color: T.muted, lineHeight: 1.6 }}>
              • CursorBench 4.0 / WANDR #1，Text Arena 1526
              <br />• 天生爱穷举探索 + 多轮自检
              <br />• <strong style={{ color: T.ink }}>唯一适用场景：10+ 文件跨模块重构 / 实盘交易内核</strong>
            </div>
          </div>
          <div style={{ background: '#1C1419', border: `2px solid ${T.red}`, borderRadius: 18, padding: 32, textAlign: 'center' }}>
            <div style={{ fontSize: 20, color: '#FCA5A5' }}>小改任务实测等待</div>
            <div style={{ fontFamily: T.mono, fontSize: 74, fontWeight: 800, color: T.red, margin: '10px 0' }}>
              {mm}:{ss}
            </div>
            <div style={{ fontSize: 19, color: T.muted }}>7–8 分钟起步</div>
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
    <AbsoluteFill style={{ fontFamily: T.sans, color: T.ink }}>
      <HostPip badge="极速工兵 · Hydrogen" />
      <div style={{ position: 'absolute', top: 110, left: 500, right: 64, bottom: 126, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <div
          style={{
            background: T.panel,
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
            <div style={{ fontSize: 22, color: T.green, fontWeight: 700 }}>01 H · GOOGLE GEMINI 4 HYDROGEN（约占 15%）</div>
            <div style={{ fontSize: 48, fontWeight: 800, margin: '12px 0 18px' }}>
              3.8 Flash 的 <span style={{ fontFamily: T.mono, color: T.green }}>2.5x</span> 速度 · 十几秒交活
            </div>
            <div style={{ fontSize: 24, color: T.muted, lineHeight: 1.6 }}>
              • 改几行脚本、补单测、更新文档直接单挂 <strong style={{ color: T.ink }}>High</strong>
              <br />• 同时担任全部 Orchestrator 的底层施工员
            </div>
          </div>
          <div
            style={{
              background: '#1C1419',
              border: `2px solid ${T.red}`,
              borderRadius: 18,
              padding: 28,
              textAlign: 'center',
              transform: `scale(${interpolate(lockSp, [0, 1], [1.14, 1])})`,
              opacity: lockSp,
            }}
          >
            <div style={{ fontSize: 20, color: '#FCA5A5', fontWeight: 700 }}>⛔ 禁用单开档位</div>
            <div style={{ fontFamily: T.mono, fontSize: 44, fontWeight: 800, color: T.red, margin: '14px 0' }}>Extra (XHigh)</div>
            <div style={{ fontSize: 20, color: T.ink }}>极易撞 60s 空闲断流 EOF</div>
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
    <AbsoluteFill style={{ fontFamily: T.sans, color: T.ink }}>
      <HostPip badge="抄作业闭环 · Zero-FOMO" />
      <div style={{ position: 'absolute', top: 110, left: 500, right: 64, bottom: 126, display: 'flex', flexDirection: 'column', gap: 22 }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 390px', gap: 24 }}>
          <div style={{ background: T.panel, border: `1px solid ${T.border}`, borderRadius: 18, padding: '26px 32px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: 30, fontWeight: 800 }}>
                日常黄金公式：<span style={{ color: T.amber }}>Orchestrator (Neon)</span>
              </span>
              <span
                style={{
                  fontFamily: T.mono,
                  padding: '6px 14px',
                  borderRadius: 999,
                  background: 'rgba(34,197,94,0.14)',
                  border: `1px solid ${T.green}`,
                  color: T.green,
                  fontSize: 18,
                }}
              >
                换活即开新对话 &lt;200K
              </span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 18, marginTop: 18 }}>
              <div style={{ flex: 1, padding: '18px 22px', borderRadius: 14, background: T.panel2, border: '1px solid rgba(245, 158, 11, 0.5)' }}>
                <div style={{ fontFamily: T.mono, fontSize: 16, color: T.amber }}>STEP 1 · PLANNER</div>
                <div style={{ fontSize: 26, fontWeight: 800, marginTop: 6 }}>Neon (High)</div>
                <div style={{ fontSize: 17, color: T.muted, marginTop: 4 }}>只读规划 · 省 32% 成本</div>
              </div>
              <div style={{ fontSize: 34, color: T.amber, fontWeight: 800 }}>➔</div>
              <div style={{ flex: 1, padding: '18px 22px', borderRadius: 14, background: T.panel2, border: '1px solid rgba(34, 197, 94, 0.5)' }}>
                <div style={{ fontFamily: T.mono, fontSize: 16, color: T.green }}>STEP 2 · EXECUTOR</div>
                <div style={{ fontSize: 26, fontWeight: 800, marginTop: 6 }}>Hydrogen (High)</div>
                <div style={{ fontSize: 17, color: T.muted, marginTop: 4 }}>2.5x 极速施工 · 遇阻自动回弹</div>
              </div>
            </div>
          </div>

          <div
            style={{
              borderRadius: 18,
              padding: 24,
              border: `2px solid ${T.red}`,
              background: 'rgba(229, 72, 77, 0.08)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              transform: `scale(${interpolate(stampSp, [0, 1], [1.18, 1])})`,
              opacity: stampSp,
            }}
          >
            <div>
              <div style={{ fontFamily: T.mono, fontSize: 16, color: '#FCA5A5' }}>POOL B · 100% 独立配额</div>
              <div style={{ fontSize: 32, fontWeight: 800, marginTop: 8 }}>Claude Opus 5.5</div>
            </div>
            <div style={{ fontSize: 19, color: T.ink, lineHeight: 1.45 }}>
              平时不动 · 重大上线喊
              <br />
              <strong style={{ color: T.red }}>「Opus 审计」</strong> 异构红队复核
            </div>
          </div>
        </div>

        <div style={{ background: T.panel, border: `1px solid ${T.border}`, borderRadius: 18, padding: '22px 30px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 21 }}>
            <thead>
              <tr>
                {['Google 模型档位', '日常占比', '核心基准 / 定位', '避坑红线'].map((h) => (
                  <th key={h} style={{ textAlign: 'left', color: T.muted, fontSize: 16, fontWeight: 600, paddingBottom: 12, borderBottom: `1px solid ${T.border}` }}>
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[
                { name: 'Gemini 4 Neon', color: T.amber, pct: '75%', bench: 'Coding #1 (58.6) · 提速 ~3x / 省 32%', red: '过 200K 掉速（上限 512K）', redColor: '#FCA5A5' },
                { name: 'Gemini 4 Hydrogen', color: T.green, pct: '15%', bench: '3.8 Flash 的 2.5x 极速 · 改小脚本十秒级', red: '禁单开 Extra（60s 断流）', redColor: '#FCA5A5' },
                { name: 'Gemini 4 Carbon', color: T.red, pct: '8%', bench: 'CursorBench #1 · 深层竞态与风控重坦', red: '小改也等 7–8 分钟', redColor: '#FCA5A5' },
                { name: 'Gemini 4 Argon', color: T.cyan, pct: '2%', bench: '统一 1M 窗口 · 中文长文与超大仓概览', red: '日常代码性价比让位 Neon', redColor: T.muted },
              ].map((row, idx) => {
                const rowSp = spring({ frame: Math.max(0, frame - (12 + idx * 6)), fps, config: { damping: 18 } });
                return (
                  <tr key={row.name} style={{ opacity: rowSp }}>
                    <td style={{ padding: '12px 8px 12px 0', borderBottom: idx < 3 ? '1px solid rgba(241,245,249,0.06)' : 'none', fontWeight: 700, color: row.color }}>{row.name}</td>
                    <td style={{ padding: '12px 8px 12px 0', borderBottom: idx < 3 ? '1px solid rgba(241,245,249,0.06)' : 'none', fontFamily: T.mono, color: row.color, fontWeight: 700 }}>{row.pct}</td>
                    <td style={{ padding: '12px 8px 12px 0', borderBottom: idx < 3 ? '1px solid rgba(241,245,249,0.06)' : 'none' }}>{row.bench}</td>
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

const SCENES: Record<string, React.FC> = {
  s1: S1Hook,
  s2: S2Lanes,
  s3: S3Neon,
  s4: S4Carbon,
  s5: S5Hydrogen,
  s6: S6Formula,
};

export const Main: React.FC = () => {
  const frame = useCurrentFrame();
  const active = SHOTS.find((s) => frame >= s.start && frame < s.end) ?? SHOTS[SHOTS.length - 1];

  return (
    <AbsoluteFill>
      <DotGridBackdrop />
      <Audio src={staticFile('voice.mp3')} />
      <TopBar activeChapter={active.chapter} />
      {SHOTS.map((shot) => {
        const Scene = SCENES[shot.id];
        return (
          <Sequence key={shot.id} from={shot.start} durationInFrames={shot.end - shot.start}>
            <Scene />
          </Sequence>
        );
      })}
      <SubtitleBar text={active.subtitle} />
    </AbsoluteFill>
  );
};
