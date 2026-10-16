import motion from './data/motion.json';

// Zero velocity at both ends avoids a sudden start/stop during each crossfade.
export const easeProgress = (value: number) => {
  const t = Math.max(0, Math.min(1, value));
  return t * t * (3 - 2 * t);
};

export const photoScale = (index: number, frame: number, frames: number) => {
  const eased = easeProgress(frame / Math.max(1, frames - 1));
  return motion.zoomMin + (motion.zoomMax - motion.zoomMin) * (index % 2 === 0 ? eased : 1 - eased);
};
