// CPU-friendly export of the same media manifest used by Remotion Studio.
// Original media bytes are never modified. Per-clip caching enables safe resume.
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {readFileSync, writeFileSync, existsSync, mkdirSync} from 'node:fs';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const cli = resolve(dirname(require.resolve('@remotion/cli/package.json')), 'remotion-cli.js');
const system = spawnSync('ffmpeg', ['-version'], {stdio: 'ignore'}).status === 0;
const run = (args) => {
  const result = system ? spawnSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...args], {encoding: 'utf8', maxBuffer: 8 * 1024 * 1024}) : spawnSync(process.execPath, [cli, 'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', ...args], {encoding: 'utf8', maxBuffer: 8 * 1024 * 1024});
  if (result.status !== 0) throw new Error(result.stderr || 'FFmpeg failed');
};
const m = JSON.parse(readFileSync(resolve(root, 'src/data/media-manifest.json')));
const key = createHash('sha256').update(JSON.stringify(m)).update(readFileSync(fileURLToPath(import.meta.url))).digest('hex').slice(0,12);
const work = resolve(root, 'work', `native-${key}`);
mkdirSync(work, {recursive: true});
mkdirSync(resolve(root, 'out'), {recursive: true});
const shine = resolve(work, 'shine.png');
run(['-f', 'lavfi', '-i', "nullsrc=s=400x1440,format=rgba,geq=r=255:g=245:b=217:a='20*exp(-pow((X-W/2)/(W/5),2))'", '-frames:v', '1', '-threads', '1', shine]);
const encode = (frames) => ['-frames:v', String(frames), '-an', '-c:v', 'libx264', '-threads', '2', '-preset', 'fast', '-crf', '16', '-pix_fmt', 'yuv420p', '-bf', '0', '-g', '120', '-r', String(m.fps), '-video_track_timescale', '15360', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709'];
const items = [m.intro, ...m.photos, m.outro];
const full = [];
for (let i = 0; i < items.length; i++) {
  const item = items[i], n = item.durationInFrames;
  const target = resolve(work, `clip-${String(i).padStart(2,'0')}.mp4`);
  full.push(target);
  if (existsSync(target + '.done')) {console.log(`Cached ${i+1}/54: ${item.src}`); continue;}
  const force = [0, m.transitionFrames / m.fps, (n - m.transitionFrames) / m.fps].join(',');
  if (i === 0 || i === items.length-1) {
    run(['-threads', '2', '-i', resolve(root, 'public', item.src), '-vf', 'fps=60,scale=2560:1440:force_original_aspect_ratio=decrease:flags=lanczos,pad=2560:1440:(ow-iw)/2:(oh-ih)/2:color=0xfaf6ed,setsar=1,format=yuv420p', ...encode(n), '-force_key_frames', force, target]);
  } else {
    const photoIndex = i-1;
    const fit = Math.min(m.width/item.width, m.height/item.height) * 0.95;
    const w = Math.floor(item.width*fit/2)*2, h = Math.floor(item.height*fit/2)*2;
    const zoom = photoIndex % 2 === 0 ? `1+0.0263157894736842*on/${n-1}` : `1.0263157894736842-0.0263157894736842*on/${n-1}`;
    const sparkles = Array.from({length: 18}, (_, j) => `drawbox=x=${(j*719+100)%m.width}:y=${(j*383+73)%m.height}:w=${j%4===0?9:3}:h=${j%4===0?9:3}:color=0xc0a56d@0.14:t=fill:enable='gt(sin(t*${0.6+(j%4)*0.13}+${j*2.4}),0.2)'`).join(',');
    const graph = `[0:v]scale=${w}:${h}:flags=lanczos,pad=2560:1440:(ow-iw)/2:(oh-ih)/2:color=0xfaf6ed,zoompan=z='${zoom}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=${n}:s=2560x1440:fps=60,setsar=1,${sparkles}[card];[1:v]format=rgba[shine];[card][shine]overlay=x='-700+3960*t/${n/m.fps}':y=0:shortest=1:format=auto,format=yuv420p[v]`;
    run(['-threads', '1', '-i', resolve(root, 'public', item.src), '-loop', '1', '-framerate', '60', '-i', shine, '-filter_complex_threads', '1', '-filter_complex', graph, '-map', '[v]', ...encode(n), '-force_key_frames', force, target]);
  }
  writeFileSync(target + '.done', 'ok\n');
  console.log(`Encoded ${i+1}/54: ${item.src}`);
}
const segments = [];
for (let i = 0; i < items.length; i++) {
  const n = items[i].durationInFrames;
  const head = i === 0 ? 0 : m.transitionFrames;
  const bodyFrames = n-head-(i === items.length-1 ? 0 : m.transitionFrames);
  const body = resolve(work, `body-${String(i).padStart(2,'0')}.mp4`);
  run(['-ss', String(head/m.fps), '-i', full[i], '-map', '0:v:0', '-frames:v', String(bodyFrames), '-an', '-c:v', 'copy', '-avoid_negative_ts', 'make_zero', body]);
  segments.push(body);
  if (i < items.length-1) {
    const transition = resolve(work, `fade-${String(i).padStart(2,'0')}.mp4`);
    const graph = `[0:v]setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]blend=all_expr='A*(1-T*60/${m.transitionFrames-1})+B*(T*60/${m.transitionFrames-1})':shortest=1,format=yuv420p[v]`;
    run(['-threads','1','-ss', String((n-m.transitionFrames)/m.fps), '-i', full[i], '-threads','1','-i', full[i+1], '-filter_complex_threads','1','-filter_complex', graph, '-map', '[v]', ...encode(m.transitionFrames), transition]);
    segments.push(transition);
  }
  console.log(`Joined ${i+1}/54`);
}
const concat = resolve(work, 'concat.txt');
writeFileSync(concat, segments.map((file) => `file '${file.replaceAll("'", "'\\''")}'`).join('\n')+'\n');
const output = resolve(root, 'out/oppo-bac-ninh-20-10-1440p60.mp4');
const duration = m.totalFrames/m.fps;
run(['-f','concat','-safe','0','-i',concat,'-i',resolve(root,'public',m.music.src),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',`volume=${m.music.volume},afade=t=in:st=0:d=${m.music.fadeInSeconds},afade=t=out:st=${duration-m.music.fadeOutSeconds}:d=${m.music.fadeOutSeconds}`,'-c:a','aac','-b:a','320k','-ar','48000','-t',String(duration),'-movflags','+faststart',output]);
console.log(`Export complete: ${output}`);
