import sys,re
import numpy as np
from PIL import Image,ImageDraw
from common import *
def main():
 m=load_manifest();p=ROOT/'out/oppo-bac-ninh-20-10-final-short-1440p60.mp4';meta=probe(p);v=next(x for x in meta['streams'] if x['codec_type']=='video');a=next(x for x in meta['streams'] if x['codec_type']=='audio')
 assert (v['codec_name'],v['width'],v['height'],v['avg_frame_rate'])==('h264',2560,1440,'60/1')
 assert a['codec_name']=='aac' and a['channels']==2 and a['sample_rate']=='48000'
 assert int(v['nb_frames'])==m['totalFrames'],(v['nb_frames'],m['totalFrames'])
 assert abs(float(meta['format']['duration'])-m['totalFrames']/60)<.1
 assert 540<=m['totalFrames']/60<=600
 photos=[s for s in m['scenes'] if s['kind']=='photo'];wishes=[s for s in m['scenes'] if s['kind']=='wish']
 assert len(photos)==52 and len({s['src'] for s in photos})==52
 assert [s['src'] for s in photos]==sorted(s['src'] for s in photos)
 assert len(wishes)==16 and [s['number'] for s in wishes]==list(range(1,17))
 assert all(s['keptSeconds']<18 and s['speed']<=1.1 for s in wishes)
 # Compare actual encoded frames against the approved staged scenes, at interior
 # points outside transitions. This catches missing, duplicated and misrotated media.
 checks=[];thumbs=[]
 for s in photos+wishes:
  t=2 if s['kind']=='wish' else s['durationInFrames']/120
  arrays=[]
  for src,time in [(p,s['startFrame']/60+t),(GEN/'scenes'/f'{s["id"]}.mp4',t)]:
   raw=run(['ffmpeg','-v','error','-ss',time,'-i',src,'-frames:v','1','-vf','scale=320:180','-pix_fmt','rgb24','-f','rawvideo','-'],True);arrays.append(np.frombuffer(raw,np.uint8).reshape(180,320,3))
  mae=float(np.mean(np.abs(arrays[0].astype(float)-arrays[1].astype(float))));assert mae<3,(s['id'],mae)
  thumb=Image.fromarray(arrays[0]);ImageDraw.Draw(thumb).text((8,8),s['id'],fill='white');thumbs.append(thumb);checks.append({'id':s['id'],'frameMae':mae,'sourceSha256':s['sha256']})
  print('QA FRAME',s['id'],round(mae,4),flush=True)
 sheet=Image.new('RGB',(320*4,180*17))
 for k,im in enumerate(thumbs):sheet.paste(im,((k%4)*320,(k//4)*180))
 sheet.save(WORK/'render-contact.jpg',quality=90)
 # The final AAC must match the approved mix. No clipping or accidental silence.
 actual=pcm(p,rate=8000);expected=pcm(ROOT/'public'/m['audioSrc'],rate=8000);n=min(len(actual),len(expected));corr=float(np.corrcoef(actual[:n].ravel(),expected[:n].ravel())[0,1]);assert corr>.98,corr
 peak=float(np.max(np.abs(actual)));assert peak<1
 voice_checks=[]
 for s in wishes:
  st=round(s['voiceStartFrame']/60*8000);en=round(s['voiceEndFrame']/60*8000);c=float(np.corrcoef(actual[st:en].ravel(),expected[st:en].ravel())[0,1]);assert c>.98
  reference=pcm(GEN/'audio'/f'voice-{s["number"]:02}.wav',rate=8000);k=min(len(reference),en-st);margin=1600
  present=float(np.corrcoef(actual[st+margin:st+k-margin].ravel(),reference[margin:k-margin].ravel())[0,1]);assert present>.92,(s['number'],present)
  voice_checks.append({'normalizedVoiceCorrelation':present,'number':s['number'],'name':s['name'],'role':s['role'],'seconds':s['keptSeconds'],'audioCorrelation':c,'orientation':s['orientationNote']})
 # Decode everything; reject unexpected black frames in the interior timeline.
 logs=run(['ffmpeg','-hide_banner','-nostats','-v','info','-i',p,'-map','0:v:0','-map','0:a:0','-vf','blackdetect=d=0.1:pix_th=0.05:pic_th=0.99','-f','null','-'])
 black=[{'start':float(x),'end':float(y),'duration':float(z)} for x,y,z in re.findall(r'black_start:([0-9.]+) black_end:([0-9.]+) black_duration:([0-9.]+)',logs)]
 outro=next(s['startFrame']/60 for s in m['scenes'] if s['id']=='outro')
 assert all(b['end']<8.4 or b['start']>outro for b in black),black
 assert not re.search(r'Error while|Invalid data|corrupt decoded|non monotonically',logs,re.I),logs[-4000:]
 levels=[float(np.sqrt(np.mean(actual[t*8000:(t+1)*8000]**2))) for t in range(1,int(m['totalFrames']/60)-3)]
 assert min(levels)>.0003,min(levels)
 report={'passed':True,'file':p.name,'sha256':sha(p),'bytes':p.stat().st_size,'durationSeconds':m['totalFrames']/60,'frames':m['totalFrames'],'photoCount':52,'wishCount':16,'video':'H.264 2560x1440 60fps','audio':'AAC stereo 48000Hz 320kbps','audioCorrelation':corr,'samplePeak':peak,'framesChecked':checks,'wishes':voice_checks,'fullDecodePassed':True,'blackIntervals':black,'minimumInteriorOneSecondRms':min(levels)}
 dump(WORK/'qa-report.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ['framesChecked','wishes']},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
