import React from 'react';
import { Composition } from 'remotion';
import { Main } from './Main';
import { MainEN } from './MainEN';
import { MainENVertical } from './MainENVertical';
import { Ep02Main } from './Ep02Main';
import { Ep02MainVertical } from './Ep02MainVertical';
import { FPS, TOTAL_FRAMES } from './theme';
import { TOTAL_FRAMES_EN } from './theme_en';
import { TOTAL_FRAMES_EP02 } from './theme_ep02';

export const Root: React.FC = () => (
  <>
    <Composition
      id="Ep01Gemini4"
      component={Main}
      durationInFrames={TOTAL_FRAMES}
      fps={FPS}
      width={1920}
      height={1080}
    />
    <Composition
      id="Ep01Gemini4EN"
      component={MainEN}
      durationInFrames={TOTAL_FRAMES_EN}
      fps={FPS}
      width={1920}
      height={1080}
    />
    <Composition
      id="Ep01Gemini4ENVertical"
      component={MainENVertical}
      durationInFrames={TOTAL_FRAMES_EN}
      fps={FPS}
      width={1080}
      height={1920}
    />
    <Composition
      id="Ep02GeminiTasks"
      component={Ep02Main}
      durationInFrames={TOTAL_FRAMES_EP02}
      fps={FPS}
      width={1920}
      height={1080}
    />
    <Composition
      id="Ep02GeminiTasksVertical"
      component={Ep02MainVertical}
      durationInFrames={TOTAL_FRAMES_EP02}
      fps={FPS}
      width={1080}
      height={1920}
    />
  </>
);
