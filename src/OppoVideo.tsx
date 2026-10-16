import {Audio} from '@remotion/media';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {AbsoluteFill, interpolate, staticFile, useVideoConfig} from 'remotion';
import {music, photos} from './data/content';
import {getSlideshowFrames, timing} from './timing';
import {Intro} from './scenes/Intro';
import {Slideshow} from './scenes/Slideshow';
import {Outro} from './scenes/Outro';

export const OppoVideo = () => {
  const {fps, durationInFrames} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: '#faf6ed'}}>
      <TransitionSeries>
        <TransitionSeries.Sequence name="Intro — Tôn vinh nét đẹp" durationInFrames={Math.round(timing.introSeconds * fps)} premountFor={fps}>
          <Intro />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames: Math.round(timing.transitionSeconds * fps)})} />
        <TransitionSeries.Sequence name="Ảnh nhân sự & lời chúc" durationInFrames={getSlideshowFrames(photos.length, fps)} premountFor={fps}>
          <Slideshow />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames: Math.round(timing.transitionSeconds * fps)})} />
        <TransitionSeries.Sequence name="Outro — Gửi trọn yêu thương" durationInFrames={Math.round(timing.outroSeconds * fps)} premountFor={fps}>
          <Outro />
        </TransitionSeries.Sequence>
      </TransitionSeries>
      {music.src ? <Audio src={staticFile(music.src)} loop premountFor={fps} volume={(frame) => music.volume * Math.min(
        interpolate(frame, [0, 1.5 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
        interpolate(frame, [durationInFrames - 2 * fps, durationInFrames - 1], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
      )} /> : null}
    </AbsoluteFill>
  );
};
