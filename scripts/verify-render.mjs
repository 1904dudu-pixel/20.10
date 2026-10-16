import {spawnSync} from 'node:child_process';
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {createHash} from 'node:crypto';
import {photoScale} from './motion.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const manifest = JSON.parse(readFileSync(resolve(root, 'src/data/media-manifest.json'), 'utf8'));
const output = resolve(root, process.argv[2] ?? 'out/oppo-bac-ninh-20-10-1440p60.mp4');
const require = createRequire(import.meta.url);
const cli = resolve(dirname(require.resolve('@remotion/cli/package.json')), 'remotion-cli.js');
const run = (tool, args) => {
  const system = spawnSync(tool, ['-version'], {stdio: 'ignore'}).status === 0;
  const result = system ? spawnSync(tool, args, {maxBuffer: 128 * 1024 * 1024}) : spawnSync(process.execPath, [cli, tool, ...args], {maxBuffer: 128 * 1024 * 1024});
  if (result.status !== 0) throw new Error(`${tool} failed: ${result.stderr?.toString()}`);
  return result.stdout;
};
const assert = (condition, message) => {if (!condition) throw new Error(message);};
const metadata = JSON.parse(run('ffprobe', ['-v', 'error', '-show_format', '-show_streams', '-of', 'json', output]).toString());
const video = metadata.streams.find((s) => s.codec_type === 'video');
const audio = metadata.streams.find((s) => s.codec_type === 'audio');
for (const media of [manifest.intro, manifest.outro, manifest.music]) {
  assert(createHash('sha256').update(readFileSync(resolve(root, 'public', media.src))).digest('hex') === media.sha256, `Source changed: ${media.src}`);
}
assert(video?.codec_name === 'h264' && video.width === 2560 && video.height === 1440 && video.avg_frame_rate === '60/1', 'Unexpected video specification');
assert(Number(video.nb_frames) === manifest.totalFrames && video.pix_fmt === 'yuv420p', 'Frame count or pixel format mismatch');
assert(audio?.codec_name === 'aac' && audio.channels === 2, 'Missing AAC stereo audio');
assert(Math.abs(Number(metadata.format.duration) - manifest.totalFrames / manifest.fps) < 0.1, 'Duration mismatch');
// Decode every encoded frame and audio packet; fail on a corrupt packet/frame.
console.log('Decoding the full MP4 to check for stream errors...');
run('ffmpeg', ['-v', 'error', '-xerror', '-threads', '2', '-i', output, '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-']);

const similarity = (a, b) => {
  assert(a.length === b.length && a.length > 0, 'Sample size mismatch');
  let sa = 0, sb = 0, saa = 0, sbb = 0, sab = 0;
  for (let i = 0; i < a.length; i++) {const x = a[i], y = b[i]; sa += x; sb += y; saa += x*x; sbb += y*y; sab += x*y;}
  return (sab - sa*sb/a.length) / Math.sqrt((saa - sa*sa/a.length)*(sbb - sb*sb/a.length));
};
const gray = (file, time, filter = '') => run('ffmpeg', ['-v', 'error', '-threads', '1', ...(time === null ? [] : ['-ss', String(time)]), '-i', file, '-frames:v', '1', '-vf', `${filter ? `${filter},` : ''}scale=240:135:flags=area,format=gray`, '-f', 'rawvideo', '-']);
const references = manifest.photos.map((photo) => gray(resolve(root, 'public', photo.src), null));
mkdirSync(resolve(root, 'work/qa'), {recursive: true});
const photos = manifest.photos.map((photo, index) => {
  assert(createHash('sha256').update(readFileSync(resolve(root, 'public', photo.src))).digest('hex') === photo.sha256, `Source changed: ${photo.src}`);
  const localFrame = Math.floor(photo.durationInFrames / 2);
  const scale = photoScale(index, localFrame, photo.durationInFrames);
  const fit = Math.min(manifest.width / photo.width, manifest.height / photo.height) * scale;
  const w = Math.floor(photo.width * fit / 2) * 2, h = Math.floor(photo.height * fit / 2) * 2;
  const time = (photo.startFrame + localFrame) / manifest.fps;
  const actual = gray(output, time, `crop=${w}:${h}:${Math.floor((manifest.width-w)/2)}:${Math.floor((manifest.height-h)/2)}`);
  const scores = references.map((reference) => similarity(actual, reference));
  const nearestIndex = scores.indexOf(Math.max(...scores));
  const score = scores[index];
  assert(nearestIndex === index && score > 0.97, `Wrong/missing photo at ${time}s: expected ${photo.src}, nearest ${manifest.photos[nearestIndex].src}, correlation ${score}`);
  writeFileSync(resolve(root, `work/qa/photo-${String(index+1).padStart(2,'0')}.pgm`), Buffer.concat([Buffer.from('P5\n240 135\n255\n'), actual]));
  console.log(`${index+1}/52 verified: ${photo.src} (${score.toFixed(5)})`);
  return {index: index + 1, src: photo.src, timeSeconds: time, correlation: score, nearestIndex: nearestIndex + 1};
});
const clips = [
  {src: manifest.intro.src, globalSeconds: 3, sourceSeconds: 3},
  {src: manifest.outro.src, globalSeconds: manifest.outro.startFrame / manifest.fps + 7, sourceSeconds: 7},
].map((clip) => {
  const score = similarity(gray(output, clip.globalSeconds), gray(resolve(root, 'public', clip.src), clip.sourceSeconds));
  assert(score > 0.97, `Incorrect intro/outro: ${clip.src} (${score})`);
  return {...clip, correlation: score};
});
const pcm = (file, channels = 1, sampleRate = 8000) => {
  const b = run('ffmpeg', ['-v', 'error', '-i', file, '-vn', '-ac', String(channels), '-ar', String(sampleRate), '-f', 'f32le', '-']);
  return new Float32Array(b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength));
};
const sourcePcm = pcm(resolve(root, 'public', manifest.music.src));
const actualPcm = pcm(output);
let bestLag = 0, bestCorrelation = -1;
for (let lag = -160; lag <= 160; lag++) {
  const start = 30 * 8000;
  const score = similarity(actualPcm.subarray(start, start + 8000), sourcePcm.subarray(start + lag, start + lag + 8000));
  if (score > bestCorrelation) {bestLag = lag; bestCorrelation = score;}
}
const measure = (seconds, length = 0.2) => {
  const start = Math.round(seconds * 8000), n = Math.round(length * 8000);
  const a = actualPcm.subarray(start, start+n), b = sourcePcm.subarray(start+bestLag, start+bestLag+n);
  let aa = 0, bb = 0;
  for (let i = 0; i < a.length; i++) {aa += a[i]*a[i]; bb += b[i]*b[i];}
  return {seconds, correlation: similarity(a,b), amplitudeRatio: Math.sqrt(aa/bb)};
};
const audioChecks = Array.from({length: Math.floor((manifest.totalFrames / manifest.fps - 5) / 5)}, (_, index) => measure((index + 1) * 5, 1));
assert(audioChecks.every((check) => check.correlation > 0.95 && Math.abs(check.amplitudeRatio - manifest.music.volume) < 0.12), 'Soundtrack mismatch, dropout, or volume error');
const fadeIn = measure(0.3), fadeOut = measure(manifest.totalFrames / manifest.fps - 0.5);
assert(fadeIn.amplitudeRatio < manifest.music.volume * 0.5 && fadeOut.amplitudeRatio < manifest.music.volume * 0.4, 'Missing audio fades');
let peak = 0;
// Check the encoded stereo channels at their native sample rate. A mono
// downmix can sum correlated channels above 1 even when neither channel clips.
for (const sample of pcm(output, 2, Number(audio.sample_rate))) peak = Math.max(peak, Math.abs(sample));
assert(peak < 1, 'Clipped stereo audio');
const report = {passed: true, output, sha256: createHash('sha256').update(readFileSync(output)).digest('hex'), video: {codec: video.codec_name, width: video.width, height: video.height, fps: video.avg_frame_rate, frames: Number(video.nb_frames), durationSeconds: Number(video.duration)}, audio: {codec: audio.codec_name, channels: audio.channels, sampleRate: Number(audio.sample_rate), source: manifest.music.src, bestLagSamplesAt8k: bestLag, checks: audioChecks, fadeIn, fadeOut, stereoPeak: peak}, fullDecodePassed: true, uniquePhotosVerified: photos.length, photos, clips};
writeFileSync(resolve(root, 'work/qa-report.json'), JSON.stringify(report, null, 2) + '\n');
console.log('PASS: 52/52 encoded photos match their sources in order, intro/outro match, soundtrack and fades match, full MP4 decodes without errors.');
