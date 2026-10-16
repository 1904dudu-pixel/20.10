import json,math,csv,re,shutil,unicodedata
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from common import *
from analyse_media import main as inspect_media
FPS=60;TRANS=27
FONT=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');BOLD=FONT.with_name('DejaVuSans-Bold.ttf')
def font(size,bold=False):return ImageFont.truetype(str(BOLD if bold else FONT),size)
def wrap(text,f,width):
 lines=[];line=''
 for w in text.split():
  candidate=(line+' '+w).strip()
  if f.getlength(candidate)>width and line:lines.append(line);line=w
  else:line=candidate
 if line:lines.append(line)
 return lines
def centered(d,text,y,f,color,width=2100):
 for line in wrap(text,f,width):
  d.text(((2560-f.getlength(line))/2,y),line,font=f,fill=color);y+=int(f.size*1.5)
 return y

def background(dark=False):
 im=Image.new('RGB',(2560,1440));a=__import__('numpy');y,x=a.mgrid[:1440,:2560];glow=a.exp(-((x-1850)/1300)**2-((y-350)/850)**2)
 base=a.array([3,48,36] if dark else [249,246,237]);delta=a.array([9,47,29] if dark else [-11,-3,-12]);arr=a.clip(base+glow[:,:,None]*delta,0,255).astype('uint8');im=Image.fromarray(arr);d=ImageDraw.Draw(im)
 d.rounded_rectangle((64,64,2496,1376),radius=10,outline='#bba16e',width=2)
 for j in range(48):
  xx=(j*719+90)%2560;yy=(j*383+64)%1440;r=3 if j%4 else 6;d.ellipse((xx-r,yy-r,xx+r,yy+r),fill='#a28e62' if dark else '#d3c398')
 return im

def assets(m):
 assets=GEN/'assets';assets.mkdir(exist_ok=True)
 # Local font prevents missing Vietnamese glyphs and cross-machine layout drift.
 shutil.copyfile(FONT,assets/'DejaVuSans.ttf');shutil.copyfile(BOLD,assets/'DejaVuSans-Bold.ttf')
 license=Path('/usr/share/doc/fonts-dejavu-core/copyright')
 if license.exists():shutil.copyfile(license,assets/'FONT-LICENSE.txt')
 im=background(True);d=ImageDraw.Draw(im);centered(d,'OPPO BẮC NINH',260,font(82,True),'#ffffff');centered(d,'GỬI MỘT NỬA',520,font(120,True),'#ffffff');centered(d,'YÊU THƯƠNG',710,font(120,True),'#dac395');centered(d,'20 / 10  •  TRÂN TRỌNG & YÊU THƯƠNG',1060,font(44),'#e6dcc8');im.save(assets/'title.png')
 for group in range(1,5):
  im=background(True);d=ImageDraw.Draw(im);centered(d,f'NHỮNG LỜI CHÚC TỪ ĐỒNG ĐỘI  •  {group:02}',290,font(40),'#d6c396');centered(d,'Và còn những lời chúc đặc biệt…',520,font(84,True),'#ffffff');centered(d,'Từ những người đồng đội',750,font(65),'#ffffff');centered(d,'luôn sát cánh bên các bạn!',860,font(65),'#e5cf9e');im.save(assets/f'bridge-{group}.png')
 for r in m['wishes']:
  im=Image.new('RGBA',(2560,1440));d=ImageDraw.Draw(im);d.rounded_rectangle((150,1210,2410,1370),radius=18,fill=(3,52,39,234),outline=(192,165,109,180),width=2)
  d.rectangle((150,1240,158,1340),fill='#dac395');d.text((208,1222),r['displayName'],font=font(59,True),fill='white');d.text((210,1302),r['displayRole'],font=font(37,True),fill='#e2ca95');im.save(assets/f'lower-{r["number"]:02}.png')
  f=ROOT/'public'/r['src'];raw=assets/f'poster-{r["number"]:02}.png'
  filt=','.join([r['orientationFilter']] if r.get('orientationFilter') else [])
  filt=(filt+',' if filt else '')+'scale=640:360:force_original_aspect_ratio=increase,crop=640:360'
  ff(['-ss',r['trimStartSeconds'],'-i',f,'-frames:v','1','-vf',filt,'-threads','1',raw])
  p=Image.open(raw).convert('RGB').resize((2560,1440)).filter(ImageFilter.GaussianBlur(48));overlay=Image.new('RGB',p.size,'#092f26');p=Image.blend(p,overlay,.36);p.save(assets/f'back-{r["number"]:02}.png');raw.unlink()
  for which,t in [('head',r['trimStartSeconds']),('tail',max(r['trimStartSeconds'],r['trimEndSeconds']-1/60))]:
   filt=(r['orientationFilter']+',' if r.get('orientationFilter') else '')+'scale=2300:1100:force_original_aspect_ratio=decrease'
   ff(['-ss',t,'-i',f,'-frames:v','1','-vf',filt,'-threads','1',assets/f'{which}-{r["number"]:02}.png'])
 # A translucent procedural champagne beam. Original photos are unchanged.
 im=Image.new('RGBA',(400,1440));import numpy as np
 arr=np.zeros((1440,400,4),dtype=np.uint8);arr[:,:,:3]=[255,245,217];arr[:,:,3]=(16*np.exp(-((np.arange(400)-200)/80)**2))[None,:].astype('uint8');Image.fromarray(arr).save(assets/'shine.png')

def main():
 # Reuse only when every wish fingerprint still matches; otherwise reinspect.
 analysis=WORK/'wishes-analysis.json';reuse=analysis.exists()
 if reuse:
  wishes=json.loads(analysis.read_text());reuse=len(wishes)==16 and all(sha(ROOT/'public'/r['src'])==r['sha256'] for r in wishes)
 if not reuse:inspect_media();wishes=json.loads(analysis.read_text())
 edits=json.loads((ROOT/'src/data/speech-edits.json').read_text())
 for r in wishes:
  e=next(e for e in edits if e['number']==r['number']);assert r['sha256']==e['sourceSha256'];r.update(e);r['trimPolicy']='Reviewed complete sentence excerpt; source intervals and excluded ranges in speech-edits.json';r['removedHeadSeconds']=r['trimStartSeconds'];r['removedTailSeconds']=r['sourceSeconds']-r['trimEndSeconds'];r['keptSeconds']=(r['trimEndSeconds']-r['trimStartSeconds'])/r['speed']
  assert r['keptSeconds']+2*TRANS/FPS<18
 # Clip 2's image itself is sideways, despite absent rotation metadata. Verified visually.
 for r in wishes:
  r['orientationFilter']='transpose=cclock' if r['number']==2 else ''
  if r['number']==2:r['displaySize']=[r['height'],r['width']];r['orientationNote']='Additional counterclockwise 90 degrees; baked sideways pixels, no metadata.'
  else:r['orientationNote']='Respect FFmpeg display matrix autorotation.'
  r['keptFrames']=math.ceil(r['keptSeconds']*FPS)
  r['displayName']='Anh. '+r['name'];r['displayRole']='GIÁM ĐỐC KINH DOANH' if r['number']==1 else r['role']
 photos=[]
 for f in sorted((ROOT/'public/photos').iterdir()):
  if f.suffix.lower() not in ['.png','.jpg','.jpeg','.webp']:continue
  with Image.open(f) as im:w,h=im.size
  photos.append({'src':str(f.relative_to(ROOT/'public')),'sha256':sha(f),'width':w,'height':h})
 assert len(photos)==52 and len({p['sha256'] for p in photos})==52
 sources={}
 for key,src in {'intro':'videos/Intro.mp4','outro':'videos/Outro_20-10_OPPO_Bac_Ninh.mp4','mainMusic':'music/NHẠC 20.10.mp3','cinematic':'music/abydos_music-opening-epic-logo-193120.mp3','outroMusic':'music/Nhac outro.mp3'}.items():
  p=ROOT/'public'/src
  if not p.exists():raise FileNotFoundError(src)
  meta=probe(p);sources[key]={'src':src,'sha256':sha(p),'durationSeconds':float(meta['format']['duration'])}
 scenes=[];cursor=0
 def add(kind,id,frames,**data):
  nonlocal cursor
  item={'kind':kind,'id':id,'durationInFrames':frames,'startFrame':cursor,'endFrame':cursor+frames,'stagedSrc':f'generated/final/scenes/{id}.mp4',**data};scenes.append(item);cursor+=frames-TRANS;return item
 add('video','intro',498,src=sources['intro']['src'])
 add('graphic','title',math.ceil(sources['cinematic']['durationSeconds']*60)-498+TRANS,asset='title.png')
 groups=[]
 for group in range(4):
  start=len(scenes)
  for n,p in enumerate(photos[group*13:(group+1)*13],group*13+1):add('photo',f'photo-{n:02}',360,photoNumber=n,**p,clearReadingSeconds=5.1)
  groups.append({'number':group+1,'startFrame':scenes[start]['startFrame'],'endFrame':scenes[-1]['endFrame']})
  add('graphic',f'bridge-{group+1}',150,asset=f'bridge-{group+1}.png')
  for r in wishes[group*4:(group+1)*4]:
   s=add('wish',f'wish-{r["number"]:02}',r['keptFrames']+2*TRANS,**r)
   s['voiceStartFrame']=s['startFrame']+TRANS;s['voiceEndFrame']=s['voiceStartFrame']+r['keptFrames'];s['lowerThirdStartSeconds']=.75;s['lowerThirdEndSeconds']=min(4.5,s['durationInFrames']/60-.9)
 add('video','outro',1200,src=sources['outro']['src'])
 m={'version':'final-polished-52-16-v3','title':'OPPO BẮC NINH – 20/10 | GỬI MỘT NỬA YÊU THƯƠNG','fps':FPS,'width':2560,'height':1440,'transitionFrames':TRANS,'totalFrames':scenes[-1]['endFrame'],'sources':sources,'photoCount':52,'wishCount':16,'photos':photos,'wishes':wishes,'photoGroups':groups,'scenes':scenes,'audioSrc':'generated/final/audio/final-mix.wav','outputFile':'out/oppo-bac-ninh-20-10-final-polished-1440p60.mp4','removedSceneIds':['closing-0','closing-1','closing-2','closing-3'],'outroOriginalAudioMuted':True,'instrumentalOrigin':'Original procedural warm piano/ambient composition created by project code; no external or commercial recording.'}
 assets(m);dump(ROOT/'src/data/final-manifest.json',m);dump(WORK/'manifest.json',m)
 with open(WORK/'timeline.csv','w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(['id','type','source','name','role','start_seconds','end_seconds','raw_seconds','clear_reading_seconds'])
  for s in scenes:w.writerow([s['id'],s['kind'],s.get('src',''),s.get('displayName',s.get('name','')),s.get('displayRole',s.get('role','')),s['startFrame']/60,s['endFrame']/60,s['durationInFrames']/60,s.get('clearReadingSeconds','')])
 dump(WORK/'trim-report.json',wishes)
 print(f'FINAL MANIFEST: {len(photos)} photos, {len(wishes)} wishes, {len(scenes)} scenes, {m["totalFrames"]/60:.3f}s; voice content {sum(r["keptSeconds"] for r in wishes):.3f}s',flush=True)
if __name__=='__main__':main()
