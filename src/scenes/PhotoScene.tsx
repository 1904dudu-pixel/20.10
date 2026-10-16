import {CanvasImage, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {palette, Rise, SceneFrame} from '../components/SceneFrame';
import type {Photo} from '../data/content';
import {timing} from '../timing';

type PhotoSceneProps = {photo: Photo; index: number; total: number};

export const PhotoScene = ({photo, index, total}: PhotoSceneProps) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <SceneFrame>
      <div style={{position: 'absolute', left: 230, top: 245, width: 850, height: 965, borderRadius: '425px 425px 12px 12px', overflow: 'hidden', border: '12px solid #fffdf8', boxShadow: '0 30px 70px #173e2725'}}>
        <CanvasImage src={staticFile(photo.src)} premountFor={fps} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: photo.objectPosition ?? 'center', scale: interpolate(frame, [0, timing.photoSeconds * fps], [1.02, 1.08], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}} />
      </div>
      <div style={{position: 'absolute', left: 1250, top: 365, width: 1050}}>
        <Rise style={{fontSize: 27, letterSpacing: 6, color: '#7a8b77'}}>NHỮNG ĐÓA HOA CỦA OPPO</Rise>
        <Rise delay={0.25} style={{marginTop: 55, fontFamily: 'Georgia, "DejaVu Serif", serif', fontSize: 111, lineHeight: 1.22}}>{photo.name}</Rise>
        <Rise delay={0.5} style={{width: 120, height: 3, background: palette.gold, marginTop: 50}}><span /></Rise>
        <Rise delay={0.75} style={{marginTop: 47, fontSize: 45, lineHeight: 1.65, whiteSpace: 'pre-line', color: '#52725f'}}>{photo.caption}</Rise>
        <Rise delay={1.1} style={{marginTop: 65, fontSize: 28, letterSpacing: 6, color: '#9b855b'}}>{String(index + 1).padStart(2, '0')} / {String(total).padStart(2, '0')}</Rise>
      </div>
    </SceneFrame>
  );
};
