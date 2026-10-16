import {Composition, Folder} from 'remotion';
import {OppoVideo} from './OppoVideo';
import manifest from './data/media-manifest.json';
import {Slideshow} from './scenes/Slideshow';
import {OpeningClip, ClosingClip} from './scenes/MediaClips';

export const RemotionRoot = () => (
  <>
    <Composition id="OppoBacNinh2010" component={OppoVideo} width={2560} height={1440} fps={60} durationInFrames={manifest.totalFrames} />
    <Folder name="Scenes">
      <Composition id="Intro" component={OpeningClip} width={2560} height={1440} fps={60} durationInFrames={manifest.intro.durationInFrames} />
      <Composition id="Slideshow" component={Slideshow} width={2560} height={1440} fps={60} durationInFrames={manifest.photos.reduce((sum, photo) => sum + photo.durationInFrames, 0) - (manifest.photos.length - 1) * manifest.transitionFrames} />
      <Composition id="Outro" component={ClosingClip} width={2560} height={1440} fps={60} durationInFrames={manifest.outro.durationInFrames} />
    </Folder>
  </>
);
