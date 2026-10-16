import {Audio} from '@remotion/media';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {AbsoluteFill, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import manifest from './data/media-manifest.json';
import {OpeningClip, ClosingClip} from './scenes/MediaClips';
import {Slideshow} from './scenes/Slideshow';

export const OppoVideo = () => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const slideshowFrames = manifest.photos.reduce((sum, photo) => sum + photo.durationInFrames, 0) - (manifest.photos.length - 1) * manifest.transitionFrames;
  return (
    <AbsoluteFill style={{background: '#faf6ed'}}>
      <TransitionSeries>
        <TransitionSeries.Sequence name="Intro.mp4" durationInFrames={manifest.intro.durationInFrames} premountFor={fps}>
          <OpeningClip />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames: manifest.transitionFrames})} />
        <TransitionSeries.Sequence name="52 ảnh nhân sự — nguyên thiết kế" durationInFrames={slideshowFrames} premountFor={fps}>
          <Slideshow />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames: manifest.transitionFrames})} />
        <TransitionSeries.Sequence name="Outro_20-10_OPPO_Bac_Ninh.mp4" durationInFrames={manifest.outro.durationInFrames} premountFor={fps}>
          <ClosingClip />
        </TransitionSeries.Sequence>
      </TransitionSeries>
      <Audio name="NHẠC 20.10.mp3 — một lượt trọn bài" src={staticFile(manifest.music.src)} premountFor={fps} volume={manifest.music.volume * Math.min(
        interpolate(frame, [0, manifest.music.fadeInSeconds * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
        interpolate(frame, [durationInFrames - manifest.music.fadeOutSeconds * fps, durationInFrames - 1], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
      )} />
    </AbsoluteFill>
  );
};
