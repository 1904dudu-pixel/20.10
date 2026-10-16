import {AbsoluteFill, CanvasImage, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Sparkles} from '../components/SceneFrame';
import type manifest from '../data/media-manifest.json';

type Photo = (typeof manifest.photos)[number];

// Keep each complete greeting card: no crop, masks, rewritten names or captions.
export const PhotoScene = ({photo, index}: {photo: Photo; index: number}) => {
  const frame = useCurrentFrame();
  const {width, height, fps} = useVideoConfig();
  const progress = Math.max(0, Math.min(1, frame / (photo.durationInFrames - 1)));
  const scale = index % 2 === 0 ? 0.95 + progress * 0.025 : 0.975 - progress * 0.025;
  const sweep = interpolate(frame, [0.6 * fps, photo.durationInFrames - 0.6 * fps], [-55, 155], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: '#faf6ed', overflow: 'hidden'}}>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 15% 80%, #dce7d6, transparent 65%), radial-gradient(ellipse at 85% 20%, #ecd1cb70, transparent 60%)'}} />
      <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <CanvasImage src={staticFile(photo.src)} premountFor={fps} style={{width, height, objectFit: 'contain', scale, boxShadow: '0 6px 28px #173e2718'}} />
      </div>
      <AbsoluteFill style={{opacity: 0.12, pointerEvents: 'none'}}>
        <div style={{position: 'absolute', top: '-35%', height: '170%', width: '16%', left: `${sweep}%`, rotate: '-18deg', background: 'linear-gradient(90deg, transparent, #fff5d9 50%, transparent)'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{opacity: 0.35, pointerEvents: 'none'}}><Sparkles /></AbsoluteFill>
    </AbsoluteFill>
  );
};
