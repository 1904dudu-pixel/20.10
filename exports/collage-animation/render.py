"""Animate only the background of the approved poster; original CRF-17 H.264 pipeline."""
from pathlib import Path
from functools import lru_cache
import argparse,hashlib,json,math,subprocess,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter,ImageChops

HERE=Path(__file__).parent
spec=json.loads((HERE/'spec.json').read_text())
W,H,FPS,N=spec['width'],spec['height'],spec['fps'],spec['durationFrames']
parser=argparse.ArgumentParser()
parser.add_argument('--poster',type=Path,default=HERE.parent/spec['posterFile'])
parser.add_argument('--out',type=Path,default=HERE/'out/OPPO-Bac-Ninh-32-Chan-Dung-Sparkles-1440p60.mp4')
parser.add_argument('--preview-only',action='store_true')
args=parser.parse_args()
assert hashlib.sha256(args.poster.read_bytes()).hexdigest()==spec['posterSha256']
base=Image.open(args.poster).convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
allowed=Image.new('L',(W,H),255)
draw=ImageDraw.Draw(allowed)
for r in [*spec['protectedPhotos'],spec['protectedTitle']]:
 draw.rounded_rectangle((r['x'],r['y'],r['x']+r['width'],r['y']+r['height']),radius=r['radius'],fill=0)
protected=np.array(allowed)==0;base_array=np.array(base)

def star_polygon(cx,cy,r):
 points=[]
 for k in range(16):
  angle=-math.pi/2+k*math.pi/8
  length=(r if k%4==0 else r*.5) if k%2==0 else r*.105
  points.append((cx+math.cos(angle)*length,cy+math.sin(angle)*length))
 return points

AA=3
seed=Image.new('RGBA',(128*AA,128*AA))
sd=ImageDraw.Draw(seed)
sd.polygon(star_polygon(64*AA,64*AA,33*AA),fill=(212,159,63,255))
glow=seed.filter(ImageFilter.GaussianBlur(8*AA))
glow.alpha_composite(seed)
gd=ImageDraw.Draw(glow)
gd.polygon(star_polygon(64*AA,64*AA,29*AA),fill=(255,245,207,255))
gd.polygon(star_polygon(64*AA,64*AA,22*AA),fill=(255,255,252,255))
gd.ellipse((61*AA,61*AA,67*AA,67*AA),fill=(255,255,255,255))
seed=glow.resize((128,128),Image.Resampling.LANCZOS)

@lru_cache(maxsize=4096)
def sprite(size,angle):
 return seed.rotate(angle,resample=Image.Resampling.BICUBIC).resize((size,size),Image.Resampling.LANCZOS)

@lru_cache(maxsize=32)
def dust_sprite(size):
 im=Image.new('RGBA',(size,size))
 d=ImageDraw.Draw(im);c=size/2;r=max(.8,size/5)
 d.ellipse((c-r,c-r,c+r,c+r),fill=(242,211,143,225))
 return im.filter(ImageFilter.GaussianBlur(.65))

def state(p,frame):
 t=(frame%N)/FPS
 angle=2*math.pi*(t/spec['durationSeconds']*p['cycles']+p['phase'])
 pulse=(1+math.cos(2*math.pi*(t/p['period']+p['phase'])))/2
 return p['x']+p['dx']*math.sin(angle),p['y']+p['dy']*math.cos(angle),pulse,angle

def composite(frame,source,x,y,opacity):
 opacity=max(0,min(1,opacity))
 if opacity<.018:return
 left=round(x-source.width/2);top=round(y-source.height/2)
 alpha=source.getchannel('A').point([round(i*opacity) for i in range(256)])
 alpha=ImageChops.multiply(alpha,allowed.crop((left,top,left+source.width,top+source.height)))
 frame.paste(source,(left,top),alpha)

def make_frame(frame):
 result=base.copy()
 for p in spec['dust']:
  x,y,pulse,angle=state(p,frame)
  composite(result,dust_sprite(max(5,round(p['radius']*7))),x,y,.22+.62*pulse)
 for p in spec['stars']:
  x,y,pulse,angle=state(p,frame)
  opacity=pulse**1.6
  size=max(12,round(p['radius']*4*(.5+.5*pulse**.5)))
  rotation=round((p['rotation']+20*math.sin(angle))/2)*2
  composite(result,sprite(size,rotation),x,y,opacity)
 return result

args.out.parent.mkdir(parents=True,exist_ok=True)
previews=args.out.parent/'previews';previews.mkdir(exist_ok=True)
samples=[0,45,90,150,300,597,1199,1799]
frames=[]
for f in samples:
 im=make_frame(f)
 assert np.array_equal(np.array(im)[protected],base_array[protected])
 if f in [0,90,300]:im.save(previews/f'frame-{f:04}.png')
 frames.append(im)
assert np.array_equal(np.array(make_frame(0)),np.array(make_frame(N)))
motion_pixels=int(np.count_nonzero(np.any(np.array(frames[0])!=np.array(frames[3]),axis=2)))
assert motion_pixels>5000,motion_pixels
thumbs=Image.new('RGB',(1280,720*2))
thumbs.paste(frames[0].resize((1280,720),Image.Resampling.LANCZOS),(0,0))
thumbs.paste(frames[3].resize((1280,720),Image.Resampling.LANCZOS),(0,720))
thumbs.save(previews/'motion-contact.jpg',quality=94)
report={'posterSha256':spec['posterSha256'],'width':W,'height':H,'fps':FPS,'durationSeconds':spec['durationSeconds'],'expectedFrames':N,
 'stars':len(spec['stars']),'dust':len(spec['dust']),'protectedPhotos':32,'protectedTitle':True,'protectedPixelsExactlyUnchangedInSampledFrames':True,
 'loopFirstFrameEqualsFrameAtDuration':True,'movingPixelsBetween0And2Point5Seconds':motion_pixels,'generativeAIUsed':False,'encoding':spec['encoding']}
if args.preview_only:
 (args.out.parent/'preview-qa.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report),flush=True)
 raise SystemExit(0)

enc=spec['encoding']
command=['ffmpeg','-hide_banner','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0',
 '-vf','scale=in_color_matrix=bt709:out_color_matrix=bt709:out_range=tv,format=yuv420p','-an','-frames:v',str(N),
 '-c:v',enc['codec'],'-threads','2','-preset',enc['preset'],'-crf',str(enc['crf']),'-pix_fmt',enc['pixFmt'],'-bf',str(enc['bFrames']),
 '-g',str(enc['gop']),'-r',str(FPS),'-video_track_timescale',str(enc['videoTrackTimescale']),'-force_key_frames',f'0,0.45,{spec["durationSeconds"]-.45}',
 '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-movflags','+faststart',str(args.out)]
started=time.monotonic()
with (args.out.parent/'ffmpeg.log').open('w') as log:
 process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
 try:
  for n in range(N):
   process.stdin.write(make_frame(n).tobytes())
   if (n+1)%120==0:print(f'RENDERED {n+1}/{N} frames ({time.monotonic()-started:.1f}s)',flush=True)
  process.stdin.close()
  if process.wait()!=0:raise RuntimeError('FFmpeg failed; see ffmpeg.log')
 except BaseException:
  process.kill();process.wait();raise
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(args.out)]))
video=next(s for s in probe['streams'] if s['codec_type']=='video')
assert video['codec_name']=='h264' and video['width']==W and video['height']==H
assert video['avg_frame_rate']=='60/1' and int(video['nb_frames'])==N
assert abs(float(probe['format']['duration'])-spec['durationSeconds'])<1/FPS
assert video['pix_fmt']=='yuv420p' and video['color_space']=='bt709'
report.update({'renderedFrames':int(video['nb_frames']),'outputBytes':args.out.stat().st_size,'outputSha256':hashlib.sha256(args.out.read_bytes()).hexdigest(),
 'actualVideoBitrate':int(video['bit_rate']),'codec':video['codec_name'],'pixFmt':video['pix_fmt'],'renderSeconds':round(time.monotonic()-started,2),'ffmpegCommand':command})
(args.out.parent/'qa-render.json').write_text(json.dumps(report,indent=2)+'\n')
print('ACTUAL MP4 RENDERED: '+json.dumps({k:v for k,v in report.items() if k!='ffmpegCommand'}),flush=True)
