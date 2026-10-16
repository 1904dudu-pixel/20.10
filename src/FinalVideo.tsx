import {AbsoluteFill, Audio, staticFile, Video} from 'remotion';
import {TransitionSeries} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import manifest from './data/final-manifest.json';
import {easeProgress} from './motion';

// Both exporters consume these same baked scenes: names, orientation, zoom,
// glitter and sweeps therefore remain identical in Studio and the fast export.
export const FinalVideo = () => (
  <AbsoluteFill style={{backgroundColor: '#faf6ed'}}>
    <TransitionSeries>
      {manifest.scenes.flatMap((scene, index) => [
        ...(index > 0 ? [<TransitionSeries.Transition key={`fade-${scene.id}`} presentation={fade()} timing={{getDurationInFrames: () => manifest.transitionFrames, getProgress: ({frame}) => easeProgress(frame / manifest.transitionFrames)}} />] : []),
        <TransitionSeries.Sequence key={scene.id} durationInFrames={scene.durationInFrames}>
          <Video src={staticFile(scene.stagedSrc)} muted style={{width: '100%', height: '100%'}} />
        </TransitionSeries.Sequence>,
      ])}
    </TransitionSeries>
    <Audio src={staticFile(manifest.audioSrc)} />
  </AbsoluteFill>
);
