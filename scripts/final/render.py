import json,math,os,sys,hashlib,concurrent.futures,re
from common import *
MOTION=json.loads((ROOT/'src/data/motion.json').read_text())
# Changing layout/filter code invalidates its scenes; timeline/audio-only edits do not.
ENGINE=Path(__file__).read_text().split('def scene_fingerprint(',1)[1].split('\ndef render_all(',1)[0].encode()
TRANS=27/60
def scene_fingerprint(s,width=2560,height=1440,fps=60):
 keys=['kind','src','sha256','width','height','durationInFrames','photoNumber','number','orientationFilter','trimStartSeconds','trimEndSeconds','speed','lowerThirdStartSeconds','lowerThirdEndSeconds']
 content={k:s[k] for k in keys if k in s}
 asset_names={'photo':['shine.png'],'graphic':[s.get('asset',''),'shine.png'],'wish':[f'back-{s.get("number",0):02}.png',f'lower-{s.get("number",0):02}.png','shine.png']}.get(s['kind'],[])
 content['assets']={name:sha(GEN/'assets'/name) for name in asset_names}
 if s['kind']=='video':content['sourceSha256']=sha(ROOT/'public'/s['src'])
 return hashlib.sha256(ENGINE+json.dumps(content,sort_keys=True).encode()+json.dumps(MOTION).encode()+f'{width}:{height}:{fps}'.encode()).hexdigest()

def render_scene(s,width=2560,height=1440,fps=60,directory=None):
 scale=width/2560;n=round(s['durationInFrames']*fps/60);duration=n/fps
 directory=Path(directory or GEN/'scenes');directory.mkdir(parents=True,exist_ok=True);out=directory/f'{s["id"]}.mp4';stamp=out.with_suffix('.cache.json')
 signature=scene_fingerprint(s,width,height,fps)
 if out.exists() and stamp.exists() and json.loads(stamp.read_text()).get('signature')==signature:return str(out)
 assets=GEN/'assets';input_args=[]
 def still(name):return ['-framerate',fps,'-i',assets/name]
 kind=s['kind'];graph='';filters=[]
 if kind=='photo':
  fit=min(width/s['width'],height/s['height'])*MOTION['zoomMin'];w=math.floor(s['width']*fit/2)*2;h=math.floor(s['height']*fit/2)*2;t=f'(on/{n-1})';e=f'({t}*{t}*(3-2*{t}))';rang=(MOTION['zoomMax']-MOTION['zoomMin'])/MOTION['zoomMin'];zoom=f'1+{rang}*'+(e if s['photoNumber']%2 else f'(1-{e})')
  input_args=['-threads','1','-i',ROOT/'public'/s['src'],*still('shine.png')]
  stars=','.join(f"drawbox=x={int(((j*719+100)%2560)*scale)}:y={int(((j*383+73)%1440)*scale)}:w={max(1,int((8 if j%4==0 else 3)*scale))}:h={max(1,int((8 if j%4==0 else 3)*scale))}:color=0xc0a56d@0.12:t=fill:enable='gt(sin(t*{.6+(j%4)*.13}+{j*2.4}),0.2)'" for j in range(18))
  graph=f"[0:v]scale={w}:{h}:flags=lanczos,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0xfaf6ed,zoompan=z='{zoom}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={n}:s={width}x{height}:fps={fps},setsar=1,{stars}[card];[1:v]scale={int(400*scale)}:{height},format=rgba[shine];[card][shine]overlay=x='-{700*scale}+{3960*scale}*t/{duration}':y=0:shortest=1:format=auto,format=yuv420p[v]"
 elif kind=='wish':
  number=s['number'];input_args=['-threads','1','-ss',s['trimStartSeconds'],'-t',s['trimEndSeconds']-s['trimStartSeconds'],'-i',ROOT/'public'/s['src'],*still(f'back-{number:02}.png'),*still(f'lower-{number:02}.png'),*still('shine.png')]
  orient=(s.get('orientationFilter','')+',') if s.get('orientationFilter') else ''
  end=s['lowerThirdEndSeconds'];fgw=int(2300*scale)//2*2;fgh=int(1100*scale)//2*2
  graph=f"[0:v]{orient}setpts=(PTS-STARTPTS)/{s['speed']},fps={fps},scale={fgw}:{fgh}:force_original_aspect_ratio=decrease:flags=lanczos,setsar=1,tpad=start_duration={TRANS}:stop_duration=2:start_mode=clone:stop_mode=clone,trim=end_frame={n},setpts=N/({fps}*TB)[fg];[1:v]scale={width}:{height},setsar=1[bg];[bg][fg]overlay=x=(W-w)/2:y={80*scale}+({fgh}-h)/2:shortest=1[scene];[2:v]scale={width}:{height},format=rgba,fade=t=in:st=0.75:d=0.5:alpha=1,fade=t=out:st={end-.5}:d=0.5:alpha=1[lower];[scene][lower]overlay=x=0:y='{35*scale}*(1-min(max((t-0.75)/0.65,0),1))':enable='between(t,0.75,{end})':shortest=1[named];[3:v]crop=400:160:0:0,scale={int(400*scale)}:{int(160*scale)},format=rgba[shine];[named][shine]overlay=x='-{500*scale}+{3560*scale}*min(max((t-0.75)/3.75,0),1)':y={1210*scale}:enable='between(t,0.75,{end})':shortest=1:format=auto,format=yuv420p[v]"
 elif kind=='graphic':
  input_args=[*still(s['asset']),*still('shine.png')]
  graph=f"[0:v]scale={width}:{height},setsar=1[base];[1:v]scale={int(400*scale)}:{height},format=rgba[shine];[base][shine]overlay=x='-{600*scale}+{3760*scale}*t/{duration}':y=0:shortest=1:format=auto,format=yuv420p[v]"
 else:
  input_args=['-threads','1','-i',ROOT/'public'/s['src']]
  graph=f'[0:v]fps={fps},scale={width}:{height}:force_original_aspect_ratio=decrease:flags=lanczos,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0xfaf6ed,setsar=1,format=yuv420p[v]'
 # Decode and scale each static PNG once, then cache the frame. Keep animated
 # alpha fades after the loop so the lower third still rises and fades.
 still_indices={'photo':{1},'wish':{1,2,3},'graphic':{0,1}}.get(kind,set())
 parts=graph.split(';')
 for k,part in enumerate(parts):
  match=re.match(r'\[(\d+):v\]',part)
  if match and int(match[1]) in still_indices:
   pos=part.index(',fade=') if ',fade=' in part else part.rfind('[')
   parts[k]=part[:pos]+f',loop=loop=-1:size=1:start=0,settb=1/{fps},setpts=N'+part[pos:]
 graph=';'.join(parts)
 args=[*input_args,'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-frames:v',n,'-an','-c:v','libx264','-threads','2','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-bf','0','-g',fps*2,'-r',fps,'-video_track_timescale','15360','-force_key_frames',f'0,{TRANS},{max(TRANS,duration-TRANS)}','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',out]
 ff(args)
 p=probe(out);v=next(v for v in p['streams'] if v['codec_type']=='video');assert int(v['nb_frames'])==n,(s['id'],v['nb_frames'],n)
 dump(stamp,{'signature':signature,'frames':n,'width':width,'height':height,'fps':fps});return str(out)

def render_all():
 m=load_manifest();workers=int(os.environ.get('FINAL_RENDER_WORKERS','2'));done=0
 with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
  jobs={pool.submit(render_scene,s):s for s in m['scenes']}
  for future in concurrent.futures.as_completed(jobs):
   future.result();done+=1;print(f'STAGED {done}/{len(jobs)} {jobs[future]["id"]}',flush=True)

def join(scenes,output,width=2560,height=1440,fps=60,directory=None,audio=None):
 directory=Path(directory or GEN/'scenes');work=WORK/('join' if fps==60 and width==2560 else 'preview-join');work.mkdir(parents=True,exist_ok=True);frames=round(TRANS*fps)
 commands='\n'.join(f'{max(0,i/fps-.000001):.9f} blend@dissolve all_opacity {1-ease((i+1)/frames):.12f};' for i in range(frames-1))+'\n';(work/'fade.cmd').write_text(commands)
 segments=[]
 for index,s in enumerate(scenes):
  n=round(s['durationInFrames']*fps/60);head=0 if index==0 else frames;tail=0 if index==len(scenes)-1 else frames;part=work/f'body-{index:02}.mp4';source=directory/f'{s["id"]}.mp4'
  ff(['-ss',head/fps,'-i',source,'-map','0:v:0','-frames:v',n-head-tail,'-an','-c:v','copy','-avoid_negative_ts','make_zero',part]);segments.append(part)
  if tail:
   other=directory/f'{scenes[index+1]["id"]}.mp4';fade=work/f'fade-{index:02}.mp4';path=str(work/'fade.cmd').replace('\\','/').replace(':','\\:');graph=f"[0:v]setpts=PTS-STARTPTS,fps={fps},settb=1/{fps}[a];[1:v]setpts=PTS-STARTPTS,fps={fps},settb=1/{fps}[b];[a][b]blend@dissolve=all_mode=normal:all_opacity=1:shortest=1,sendcmd=f='{path}',format=yuv420p[v]"
   ff(['-threads','1','-ss',(n-frames)/fps,'-i',source,'-threads','1','-i',other,'-filter_complex_threads','1','-filter_complex',graph,'-map','[v]','-frames:v',frames,'-an','-c:v','libx264','-threads','2','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-bf','0','-r',fps,'-video_track_timescale','15360','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',fade]);segments.append(fade)
  print(f'JOINED {index+1}/{len(scenes)} {s["id"]}',flush=True)
 listing=work/'concat.txt';listing.write_text('\n'.join("file '"+str(p).replace("'","'\\''")+"'" for p in segments)+'\n');output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
 total=sum(round(s['durationInFrames']*fps/60) for s in scenes)-(len(scenes)-1)*frames
 args=['-f','concat','-safe','0','-i',listing]
 if audio:args+=['-i',audio,'-map','0:v:0','-map','1:a:0','-c:a','aac','-b:a','320k','-ar','48000']
 else:args+=['-map','0:v:0','-an']
 ff([*args,'-c:v','copy','-t',total/fps,'-movflags','+faststart',output]);return total
if __name__=='__main__':
 mode=sys.argv[1] if len(sys.argv)>1 else 'all';m=load_manifest()
 if mode in ['all','stages']:render_all()
 if mode in ['all','join']:
  target=ROOT/m['outputFile'];frames=join(m['scenes'],target,audio=ROOT/'public'/m['audioSrc']);assert frames==m['totalFrames'];print(f'FINAL MP4 EXISTS: {target}, {frames} frames, {target.stat().st_size} bytes',flush=True)
