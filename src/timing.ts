export const timing = {
  introSeconds: 7,
  photoSeconds: 7,
  outroSeconds: 7,
  transitionSeconds: 0.8,
};

export const getSlideshowFrames = (count: number, fps: number) => {
  // Giữ một cảnh lời chúc nếu danh sách ảnh rỗng.
  const scenes = Math.max(1, count);
  return Math.round(scenes * timing.photoSeconds * fps) -
    (scenes - 1) * Math.round(timing.transitionSeconds * fps);
};

export const getVideoFrames = (count: number, fps: number) =>
  Math.round((timing.introSeconds + timing.outroSeconds) * fps) +
  getSlideshowFrames(count, fps) - 2 * Math.round(timing.transitionSeconds * fps);
