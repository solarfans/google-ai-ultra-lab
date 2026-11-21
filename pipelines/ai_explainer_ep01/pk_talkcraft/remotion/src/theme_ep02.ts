import { CAPTIONS_EP02 } from './captions_ep02';
import { V2_TOKENS } from './ep02_components';

export const T_EP02 = V2_TOKENS;
export const FPS = CAPTIONS_EP02.fps;
export const TOTAL_FRAMES_EP02 = CAPTIONS_EP02.totalFrames;

const SHOT_META = [
  { id: 's1', tag: 'THE SWITCH', headline: 'FROM CHAT TO', accentWord: 'TASK' },
  { id: 's2', tag: 'THE DIFFERENCE', headline: 'CHAT VS', accentWord: 'TASK' },
  { id: 's3', tag: 'USE CASE 1', headline: 'DAILY', accentWord: 'BRIEFING' },
  { id: 's4', tag: 'USE CASE 2', headline: 'LIVE WEB', accentWord: 'RESEARCH' },
  { id: 's5', tag: 'USE CASE 3', headline: 'RECURRING', accentWord: 'MONITORS' },
  { id: 's6', tag: 'CONTROL', headline: 'NOTHING WITHOUT', accentWord: 'A YES' },
  { id: 's7', tag: 'WHO GETS IT', headline: 'FREE IN SIX', accentWord: 'COUNTRIES' },
  { id: 's8', tag: 'REAL-USER TIPS', headline: 'SCOPE &', accentWord: '/SKILLS' },
  { id: 's9', tag: 'START TODAY', headline: 'YOUR FIRST', accentWord: 'TASK' },
] as const;

export const SHOTS_EP02 = SHOT_META.map((meta, idx) => {
  const seg = CAPTIONS_EP02.segments[idx];
  return {
    ...meta,
    start: seg ? seg.startFrame : 0,
    end: seg ? seg.endFrame : TOTAL_FRAMES_EP02,
  };
});
