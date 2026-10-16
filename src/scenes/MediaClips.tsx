import {Video} from '@remotion/media';
import {staticFile, useVideoConfig} from 'remotion';
import manifest from '../data/media-manifest.json';

export const OpeningClip = () => {
  const {fps} = useVideoConfig();
  return <Video src={staticFile(manifest.intro.src)} muted premountFor={fps} style={{width: '100%', height: '100%', objectFit: 'contain', background: '#faf6ed'}} />;
};

export const ClosingClip = () => {
  const {fps} = useVideoConfig();
  return <Video src={staticFile(manifest.outro.src)} muted premountFor={fps} style={{width: '100%', height: '100%', objectFit: 'contain', background: '#faf6ed'}} />;
};
