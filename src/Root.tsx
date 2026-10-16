import {Composition, Folder} from 'remotion';
import {OppoVideo} from './OppoVideo';
import {photos} from './data/content';
import {getSlideshowFrames, getVideoFrames, timing} from './timing';
import {Intro} from './scenes/Intro';
import {Slideshow} from './scenes/Slideshow';
import {Outro} from './scenes/Outro';

export const RemotionRoot = () => (
  <>
    <Composition
      id="OppoBacNinh2010"
      component={OppoVideo}
      width={2560}
      height={1440}
      fps={30}
      durationInFrames={getVideoFrames(photos.length, 30)}
    />
    <Folder name="Scenes">
      <Composition id="Intro" component={Intro} width={2560} height={1440} fps={30} durationInFrames={Math.round(timing.introSeconds * 30)} />
      <Composition id="Slideshow" component={Slideshow} width={2560} height={1440} fps={30} durationInFrames={getSlideshowFrames(photos.length, 30)} />
      <Composition id="Outro" component={Outro} width={2560} height={1440} fps={30} durationInFrames={Math.round(timing.outroSeconds * 30)} />
    </Folder>
  </>
);
