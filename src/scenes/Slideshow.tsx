import {Fragment} from 'react';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {useVideoConfig} from 'remotion';
import manifest from '../data/media-manifest.json';
import {PhotoScene} from './PhotoScene';

// All cards intentionally share one presentation template and sorted manifest.
export const Slideshow = () => {
  const {fps} = useVideoConfig();
  return (
    <TransitionSeries>
      {manifest.photos.map((photo, index) => (
        <Fragment key={photo.src}>
          {index > 0 ? <TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames: manifest.transitionFrames})} /> : null}
          <TransitionSeries.Sequence name={photo.src.slice('photos/'.length)} durationInFrames={photo.durationInFrames} premountFor={fps}>
            <PhotoScene photo={photo} index={index} />
          </TransitionSeries.Sequence>
        </Fragment>
      ))}
    </TransitionSeries>
  );
};
