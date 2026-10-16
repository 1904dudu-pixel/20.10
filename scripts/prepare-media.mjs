import {createHash} from 'node:crypto';
import {readdirSync, readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {spawnSync} from 'node:child_process';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const cli = resolve(dirname(require.resolve('@remotion/cli/package.json')), 'remotion-cli.js');
const systemProbe = spawnSync('ffprobe', ['-version'], {stdio: 'ignore'}).status === 0;
const probe = (src) => {
  const args = ['-v', 'error', '-show_entries', 'format=duration:stream=codec_type,codec_name,width,height,duration,sample_rate,channels,r_frame_rate', '-of', 'json', resolve(root, 'public', src)];
  const result = systemProbe ? spawnSync('ffprobe', args, {encoding: 'utf8'}) : spawnSync(process.execPath, [cli, 'ffprobe', ...args], {encoding: 'utf8'});
  if (result.status !== 0) throw new Error(`Cannot read ${src}: ${result.stderr}`);
  return JSON.parse(result.stdout);
};
const fingerprint = (src) => createHash('sha256').update(readFileSync(resolve(root, 'public', src))).digest('hex');
// Deterministic ascending filename order, identical on Windows/macOS/Linux.
// Only raster images are allowed; SVG placeholders and .gitkeep never enter the timeline.
const names = readdirSync(resolve(root, 'public/photos')).filter((name) => /\.(png|jpe?g|webp)$/i.test(name)).sort();
if (names.length !== 52) throw new Error(`Expected 52 real photos, found ${names.length}`);
const tracks = readdirSync(resolve(root, 'public/music')).filter((name) => /\.mp3$/i.test(name));
if (tracks.length !== 1 || tracks[0] !== 'NHẠC 20.10.mp3') throw new Error(`Unexpected music files: ${tracks.join(', ')}`);
const fps = 60;
const musicSrc = `music/${tracks[0]}`;
const introSrc = 'videos/Intro.mp4';
const outroSrc = 'videos/Outro_20-10_OPPO_Bac_Ninh.mp4';
const musicMetadata = probe(musicSrc);
const introMetadata = probe(introSrc);
const outroMetadata = probe(outroSrc);
const musicSeconds = Number(musicMetadata.streams.find((s) => s.codec_type === 'audio').duration ?? musicMetadata.format.duration);
const introSeconds = Number(introMetadata.streams.find((s) => s.codec_type === 'video').duration);
const outroSeconds = Number(outroMetadata.streams.find((s) => s.codec_type === 'video').duration);
const totalFrames = Math.floor(musicSeconds * fps);
const introFrames = Math.round(introSeconds * fps);
const outroFrames = Math.round(outroSeconds * fps);
const transitionFrames = Math.round(0.7 * fps);
const photoBudget = totalFrames - introFrames - outroFrames + (names.length + 1) * transitionFrames;
const baseFrames = Math.floor(photoBudget / names.length);
const extraFrames = photoBudget % names.length;
if (baseFrames < 4 * fps || transitionFrames * 2 >= baseFrames) throw new Error('Music is too short for readable photo scenes');
let startFrame = introFrames - transitionFrames;
const photos = names.map((name, index) => {
  const src = `photos/${name}`;
  const metadata = probe(src).streams.find((s) => s.codec_type === 'video');
  if (!metadata?.width || !metadata?.height) throw new Error(`Unreadable image: ${src}`);
  const durationInFrames = baseFrames + (index < extraFrames ? 1 : 0);
  const photo = {src, sha256: fingerprint(src), width: metadata.width, height: metadata.height, startFrame, durationInFrames};
  startFrame += durationInFrames - transitionFrames;
  return photo;
});
if (new Set(photos.map((photo) => photo.sha256)).size !== 52) throw new Error('Duplicate image contents detected');
if (startFrame + outroFrames !== totalFrames) throw new Error('Timeline duration mismatch');
const manifest = {
  fps, width: 2560, height: 1440, totalFrames, transitionFrames,
  filenameOrder: 'Ascending filename (Unicode), with extension; SVG excluded',
  music: {src: musicSrc, sha256: fingerprint(musicSrc), durationSeconds: musicSeconds, volume: 0.85, fadeInSeconds: 1.5, fadeOutSeconds: 3},
  intro: {src: introSrc, sha256: fingerprint(introSrc), durationSeconds: introSeconds, durationInFrames: introFrames},
  outro: {src: outroSrc, sha256: fingerprint(outroSrc), durationSeconds: outroSeconds, durationInFrames: outroFrames, startFrame},
  photos,
};
writeFileSync(resolve(root, 'src/data/media-manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
mkdirSync(resolve(root, 'work'), {recursive: true});
writeFileSync(resolve(root, 'work/photo-timeline.csv'), '\ufeffindex,filename,start_seconds,end_seconds,duration_seconds,sha256\n' + photos.map((photo, i) => [i + 1, JSON.stringify(photo.src), (photo.startFrame / fps).toFixed(3), ((photo.startFrame + photo.durationInFrames) / fps).toFixed(3), (photo.durationInFrames / fps).toFixed(3), photo.sha256].join(',')).join('\n') + '\n');
console.log(`Verified ${photos.length} unique photos; music: ${musicSrc}; ${totalFrames} frames / ${(totalFrames / fps).toFixed(3)} s at ${fps} fps.`);
