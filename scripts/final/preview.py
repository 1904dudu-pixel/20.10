from common import *
from render import render_scene,join
from audio import wav
from preflight import main as preflight
from PIL import Image,ImageDraw
import numpy as np

m=load_manifest();preflight();dest=WORK/'previews';dest.mkdir(exist_ok=True);path=WORK/'preview-scenes';fps=60;catalog=[]
# All coordinates refer to the approved short film until the removal point.
first=next(s for s in m['scenes'] if s['id']=='wish-01');last=next(s for s in m['scenes'] if s['id']=='wish-16')
ranges=[('01-labels',first['startFrame'],first['endFrame']),('02-music-transition',325*60,342*60),('03-chorus-reprise',449*60,478*60),('04-direct-outro',last['startFrame'],m['totalFrames'])]
for id,start,end in ranges:
 scenes=[s for s in m['scenes'] if s['startFrame']<end and s['endFrame']>start]
 for s in scenes:render_scene(s,960,540,fps,path)
 total=scenes[-1]['endFrame']-scenes[0]['startFrame'];audio=pcm(ROOT/'public'/m['audioSrc'],extra=['-ss',scenes[0]['startFrame']/60,'-t',total/60]);wav(WORK/'preview-audio.wav',audio)
 assembled=WORK/'preview-assembled.mp4';frames=join(scenes,assembled,960,540,fps,path,WORK/'preview-audio.wav');assert frames==total
 out=dest/f'{id}.mp4';ff(['-ss',(start-scenes[0]['startFrame'])/60,'-i',assembled,'-t',(end-start)/60,'-map','0:v:0','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf',18,'-threads',2,'-r',60,'-af',f'afade=t=in:d=0.1,afade=t=out:st={(end-start)/60-.1}:d=0.1','-c:a','aac','-b:a','320k','-movflags','+faststart',out])
 meta=probe(out);v=next(x for x in meta['streams'] if x['codec_type']=='video');assert int(v['nb_frames'])==end-start,(id,v['nb_frames'],end-start)
 audio_stream=next(x for x in meta['streams'] if x['codec_type']=='audio');assert audio_stream['codec_name']=='aac' and audio_stream['channels']==2 and audio_stream['sample_rate']=='48000'
 actual=pcm(out,rate=8000);expected=pcm(ROOT/'public'/m['audioSrc'],rate=8000,extra=['-ss',start/60,'-t',(end-start)/60]);k=min(len(actual),len(expected));margin=1600
 correlation=float(np.corrcoef(actual[margin:k-margin].ravel(),expected[margin:k-margin].ravel())[0,1]);assert correlation>.98,(id,correlation)
 assert np.max(abs(actual))<1
 run(['ffmpeg','-v','error','-i',out,'-f','null','-'])
 catalog.append({'audioCorrelation':correlation,'fullDecodePassed':True,'previewEdgeAudioFadeSeconds':.1,'id':id,'timelineStartSeconds':start/60,'timelineEndSeconds':end/60,'frames':end-start,'fps':60,'file':str(out.relative_to(ROOT)),'sha256':sha(out)});print('PREVIEW PASSED',id,flush=True)
# A readable contact sheet checks all sixteen rendered Vietnamese lower thirds.
sheet=Image.new('RGB',(1280,16*110),'#faf6ed')
for i,s in enumerate(m['wishes']):
 im=Image.open(GEN/'assets'/f'lower-{s["number"]:02}.png').crop((130,1190,2430,1390)).convert('RGBA').resize((1265,110));bg=Image.new('RGBA',im.size,'#4d6256');bg.alpha_composite(im);sheet.paste(bg.convert('RGB'),(8,i*110))
sheet.save(WORK/'labels-contact.jpg',quality=95)
dump(WORK/'preview-report.json',{'passed':True,'preflightPassed':True,'previews':catalog,'labelsContact':'work/final/labels-contact.jpg'});print('ALL FOUR POLISHED PREVIEWS EXIST AND HAVE VERIFIED VIDEO/AUDIO STREAMS',flush=True)
