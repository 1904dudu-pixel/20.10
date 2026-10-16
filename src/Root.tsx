import {Composition} from 'remotion';
import {FinalVideo} from './FinalVideo';
import manifest from './data/final-manifest.json';
export const RemotionRoot = () => <Composition id="OppoBacNinh2010" component={FinalVideo} width={2560} height={1440} fps={60} durationInFrames={manifest.totalFrames} />;
