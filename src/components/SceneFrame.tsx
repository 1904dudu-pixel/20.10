import type {ReactNode} from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {content} from '../data/content';

export const palette = {
  green: '#07533e',
  deep: '#033b2c',
  cream: '#faf6ed',
  gold: '#c0a56d',
  pink: '#ecd1cb',
};

// SVG trang trí tự tạo; mọi chuyển động đều phụ thuộc frame, không dùng CSS animation.
const Flower = ({x, y, size}: {x: number; y: number; size: number}) => (
  <g transform={`translate(${x} ${y}) scale(${size})`}>
    {Array.from({length: 7}, (_, i) => (
      <ellipse key={i} cx="0" cy="-50" rx="27" ry="61" transform={`rotate(${i * 360 / 7})`} fill={i % 2 ? '#e8bdb5' : '#f4ded6'} stroke="#c99f92" strokeWidth="0.8" />
    ))}
    <circle r="20" fill="#bba16e" />
    <circle r="11" fill="#e9d7ad" />
  </g>
);

const Botanical = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <svg viewBox="0 0 2560 1440" style={{position: 'absolute', width: '100%', height: '100%', opacity: 0.85, translate: `0 ${Math.sin(frame / fps * 0.5) * 8}px`}}>
      <g fill="none" stroke="#719585" strokeWidth="3" opacity="0.6">
        <path d="M-60 1430Q90 1050 320 1030M0 1440Q60 1210 460 1260M2560 0Q2450 230 2170 265" />
        <path d="M90 1220Q-10 1090 50 1060Q160 1100 90 1220M170 1120Q150 1000 230 970Q280 1080 170 1120M270 1250Q320 1120 400 1155Q405 1240 270 1250M2420 172Q2380 50 2300 70Q2300 160 2420 172M2335 225Q2200 180 2210 290Q2300 305 2335 225" fill="#99b5a1" />
      </g>
      <Flower x={40} y={1390} size={2} />
      <Flower x={240} y={1370} size={1.15} />
      <Flower x={2520} y={15} size={1.7} />
    </svg>
  );
};

export const Sparkles = () => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {Array.from({length: 36}, (_, i) => {
        // Công thức xác định: tua lại cùng frame luôn cho cùng kết quả.
        const phase = frame / fps * (0.6 + (i % 4) * 0.13) + i * 2.4;
        const opacity = (Math.sin(phase) + 1) * 0.27;
        const size = i % 4 === 0 ? 18 : 5;
        return (
          <div key={i} style={{position: 'absolute', left: ((i * 719 + 100) % width), top: ((i * 383 + 73) % height), width: size, height: size, background: palette.gold, opacity, borderRadius: i % 4 ? '50%' : 0, rotate: '45deg', translate: `0 ${Math.sin(phase * 0.4) * 24}px`, boxShadow: `0 0 ${size * 2}px ${palette.gold}`, clipPath: i % 4 ? undefined : 'polygon(50% 0, 60% 40%, 100% 50%, 60% 60%, 50% 100%, 40% 60%, 0 50%, 40% 40%)'}} />
        );
      })}
    </AbsoluteFill>
  );
};

export const SceneFrame = ({children, dark = false}: {children: ReactNode; dark?: boolean}) => (
  <AbsoluteFill style={{background: dark ? palette.deep : palette.cream, color: dark ? palette.cream : palette.green, fontFamily: 'Arial, "DejaVu Sans", sans-serif', overflow: 'hidden'}}>
    <AbsoluteFill style={{background: dark ? 'radial-gradient(ellipse at 60% 30%, #14725288, transparent 70%)' : 'radial-gradient(ellipse at 70% 30%, #e4eddf, transparent 70%)'}} />
    <Botanical />
    <div style={{position: 'absolute', inset: 64, border: `1px solid ${palette.gold}66`, borderRadius: 4}} />
    <div style={{position: 'absolute', left: 150, top: 114, fontSize: 32, letterSpacing: 7, fontWeight: 600}}>{content.organization}</div>
    <div style={{position: 'absolute', right: 150, bottom: 108, fontSize: 25, letterSpacing: 5, color: dark ? '#d7c69f' : '#748677'}}>20 / 10 • TRÂN TRỌNG & YÊU THƯƠNG</div>
    {children}
    <Sparkles />
  </AbsoluteFill>
);

export const Rise = ({children, delay = 0, style}: {children: ReactNode; delay?: number; style?: React.CSSProperties}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <div style={{...style, opacity: interpolate(frame, [delay * fps, (delay + 1.1) * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}), translate: `0 ${interpolate(frame, [delay * fps, (delay + 1.3) * fps], [65, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}px`}}>{children}</div>
  );
};
