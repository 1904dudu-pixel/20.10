import {readFileSync} from 'node:fs';

export const motion = JSON.parse(readFileSync(new URL('../src/data/motion.json', import.meta.url), 'utf8'));
export const easeProgress = (value) => {
  const t = Math.max(0, Math.min(1, value));
  return t * t * (3 - 2 * t);
};
export const photoScale = (index, frame, frames) => {
  const eased = easeProgress(frame / Math.max(1, frames - 1));
  return motion.zoomMin + (motion.zoomMax - motion.zoomMin) * (index % 2 === 0 ? eased : 1 - eased);
};
export const photoZoomExpression = (index, frames) => {
  const t = `(on/${Math.max(1, frames - 1)})`;
  const eased = `(${t}*${t}*(3-2*${t}))`;
  const range = (motion.zoomMax - motion.zoomMin) / motion.zoomMin;
  return `1+${range}*${index % 2 === 0 ? eased : `(1-${eased})`}`;
};

// sendcmd is downstream of blend: after frame i, set opacity for frame i+1.
// Use blend's native pixel kernel; no slow per-pixel expression evaluation.
export const dissolveCommands = (fps, frames) => Array.from({length: frames - 1}, (_, i) => {
  const at = Math.max(0, i / fps - 0.000001);
  const opacity = 1 - easeProgress((i + 1) / frames);
  return `${at.toFixed(9)} blend@dissolve all_opacity ${opacity.toFixed(12)};`;
}).join('\n') + '\n';
