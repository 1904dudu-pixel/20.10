import {Fragment} from 'react';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {useVideoConfig} from 'remotion';
import {photos} from '../data/content';
import {timing} from '../timing';
import {PhotoScene} from './PhotoScene';
import {Rise, SceneFrame} from '../components/SceneFrame';

export const Slideshow = () => {
  const {fps} = useVideoConfig();
  if (photos.length === 0) {
    return <SceneFrame><Rise style={{position: 'absolute', inset: 250, display: 'flex', justifyContent: 'center', alignItems: 'center', textAlign: 'center', fontSize: 110, fontFamily: 'Georgia, serif'}}>Chúc bạn luôn hạnh phúc<br />và rạng rỡ mỗi ngày.</Rise></SceneFrame>;
  }
  return (
    <TransitionSeries>
      {/* Các ảnh dùng chung một template; thêm ảnh tại data/content.ts. */}
      {photos.map((photo, index) => (
        <Fragment key={`${photo.src}-${index}`}>
          {index > 0 ? <TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames: Math.round(timing.transitionSeconds * fps)})} /> : null}
          <TransitionSeries.Sequence name={photo.name} durationInFrames={Math.round(timing.photoSeconds * fps)} premountFor={fps}>
            <PhotoScene photo={photo} index={index} total={photos.length} />
          </TransitionSeries.Sequence>
        </Fragment>
      ))}
    </TransitionSeries>
  );
};
