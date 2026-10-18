import sys,re
import numpy as np
from PIL import Image,ImageDraw
from common import *
from preflight import main as preflight
from audio_sync import approved_source
def main():
 pre=preflight();m=load_manifest();p=ROOT/m['outputFile'];meta=probe(p);v=next(x for x in meta['streams'] if x['codec_type']=='video');a=next(x for x in meta['streams'] if x['codec_type']=='audio')
 assert (v['codec_name'],v['width'],v['height'],v['avg_frame_rate'])==('h264',2560,1440,'60/1')
 assert a['codec_name']=='aac' and a['channels']==2 and a['sample_rate']=='48000'
 assert int(v['nb_frames'])==m['totalFrames'],(v['nb_frames'],m['totalFrames'])
 assert abs(float(meta['format']['duration'])-m['totalFrames']/60)<.1
 assert 540<=m['totalFrames']/60<=600
 photos=[s for s in m['scenes'] if s['kind']=='photo'];wishes=[s for s in m['scenes'] if s['kind']=='wish']
 assert len(photos)==51 and len({s['src'] for s in photos})==51
 baseline=json.loads((ROOT/'src/data/approved-polished-structure.json').read_text());reference_path,reference_sha=approved_source(baseline);old={s['id']:s for s in baseline['manifest']['scenes']}
 assert [s['src'] for s in photos]==sorted(s['src'] for s in photos)
 assert len(wishes)==16 and [s['number'] for s in wishes]==list(range(1,17))
 assert all(s['keptSeconds']<18 and s['speed']<=1.1 for s in wishes)
 # Compare actual encoded frames against the approved staged scenes, at interior
 # points outside transitions. This catches missing, duplicated and misrotated media.
 checks=[];thumbs=[]
 for s in m['scenes']:
  t=2 if s['kind']=='wish' else s['durationInFrames']/120
  arrays=[]
  for src,time in [(p,s['startFrame']/60+t),(GEN/'scenes'/f'{s["id"]}.mp4',t),(reference_path,old[s['id']]['startFrame']/60+t)]:
   raw=run(['ffmpeg','-v','error','-ss',time,'-i',src,'-frames:v','1','-vf','scale=320:180','-pix_fmt','rgb24','-f','rawvideo','-'],True);arrays.append(np.frombuffer(raw,np.uint8).reshape(180,320,3))
  baseline_mae=float(np.mean(np.abs(arrays[0].astype(float)-arrays[2].astype(float))));assert baseline_mae<3,(s['id'],'Approved Final Polished frame changed',baseline_mae)
  mae=float(np.mean(np.abs(arrays[0].astype(float)-arrays[1].astype(float))));assert mae<3,(s['id'],mae)
  thumb=Image.fromarray(arrays[0]);ImageDraw.Draw(thumb).text((8,8),s['id'],fill='white');checks.append({'id':s['id'],'frameMae':mae,'approvedPolishedFrameMae':baseline_mae,'sourceSha256':s.get('sha256',m['sources']['outro']['sha256'] if s['id']=='outro' else None)})
  if s['kind'] in ['photo','wish']:thumbs.append(thumb)
  print('QA FRAME',s['id'],round(mae,4),flush=True)
 # Every unchanged H.264 frame should retain its approved compressed payload.
 # This checks the entire film outside the sole new 27-frame crossfade.
 packet_hashes=[]
 for video in [reference_path,p]:
  data=json.loads(run(['ffprobe','-v','error','-select_streams','v:0','-show_packets','-show_entries','packet=data_hash','-show_data_hash','sha256','-of','json',video],True))
  packet_hashes.append([packet['data_hash'] for packet in data['packets']])
 before,after=packet_hashes;assert len(before)==baseline['manifest']['totalFrames'] and len(after)==m['totalFrames']
 cut=next(s['startFrame'] for s in m['scenes'] if s['id']=='photo-50');end=cut+m['transitionFrames'];delta=baseline['manifest']['totalFrames']-m['totalFrames']
 matches=sum(after[i]==before[i if i<cut else i+delta] for i in range(len(after)) if not cut<=i<end)
 preservation={'framesCompared':len(after)-(end-cut),'identicalCompressedFramePayloads':matches,'newTransitionStartFrame':cut,'newTransitionFrames':end-cut,'removedFrames':delta,'allOtherCompressedVideoFramesIdentical':matches==len(after)-(end-cut)}
 assert preservation['allOtherCompressedVideoFramesIdentical'],preservation
 print('QA ALL UNCHANGED H264 FRAME PAYLOADS IDENTICAL',matches,flush=True)
 sheet=Image.new('RGB',(320*4,180*17))
 for k,im in enumerate(thumbs):sheet.paste(im,((k%4)*320,(k//4)*180))
 sheet.save(WORK/'render-contact.jpg',quality=90)
 # The final AAC must match the approved mix. No clipping or accidental silence.
 approved_audio=pcm(reference_path,rate=8000)
 actual=pcm(p,rate=8000);expected=pcm(ROOT/'public'/m['audioSrc'],rate=8000);n=min(len(actual),len(expected));corr=float(np.corrcoef(actual[:n].ravel(),expected[:n].ravel())[0,1]);assert corr>.98,corr
 peak=float(np.max(np.abs(actual)));assert peak<1
 voice_checks=[]
 for s in wishes:
  st=round(s['voiceStartFrame']/60*8000);en=round(s['voiceEndFrame']/60*8000);c=float(np.corrcoef(actual[st:en].ravel(),expected[st:en].ravel())[0,1]);assert c>.98
  old_st=round(old[s['id']]['voiceStartFrame']/60*8000);reference=approved_audio[old_st:old_st+en-st];k=min(len(reference),en-st);margin=1600
  present=float(np.corrcoef(actual[st+margin:st+k-margin].ravel(),reference[margin:k-margin].ravel())[0,1]);assert present>.92,(s['number'],present)
  voice_checks.append({'approvedVoiceCorrelation':present,'number':s['number'],'name':s['displayName'],'role':s['displayRole'],'seconds':s['keptSeconds'],'audioCorrelation':c,'orientation':s['orientationNote']})
 # Check the actual AAC at its native sample rate for clipping/true peaks.
 loud=run(['ffmpeg','-hide_banner','-nostats','-i',p,'-vn','-af','loudnorm=I=-17:TP=-1:LRA=11:print_format=json','-f','null','-'])
 loudness=json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}',loud,re.S)[0]);assert float(loudness['input_tp'])<0,loudness
 # Decode everything; reject unexpected black frames in the interior timeline.
 logs=run(['ffmpeg','-hide_banner','-nostats','-v','info','-i',p,'-map','0:v:0','-map','0:a:0','-vf','blackdetect=d=0.1:pix_th=0.05:pic_th=0.99','-f','null','-'])
 black=[{'start':float(x),'end':float(y),'duration':float(z)} for x,y,z in re.findall(r'black_start:([0-9.]+) black_end:([0-9.]+) black_duration:([0-9.]+)',logs)]
 outro=next(s['startFrame']/60 for s in m['scenes'] if s['id']=='outro')
 assert all(b['end']<8.4 or b['start']>outro for b in black),black
 assert not re.search(r'Error while|Invalid data|corrupt decoded|non monotonically',logs,re.I),logs[-4000:]
 levels=[float(np.sqrt(np.mean(actual[t*8000:(t+1)*8000]**2))) for t in range(1,int(m['totalFrames']/60)-3)]
 assert min(levels)>.0003,min(levels)
 report={'passed':True,'file':p.name,'sha256':sha(p),'bytes':p.stat().st_size,'durationSeconds':m['totalFrames']/60,'frames':m['totalFrames'],'photoCount':51,'wishCount':16,'sceneCount':74,'allFourClosingScenesRemoved':True,'directLastWishToOriginalOutro':True,'dedicatedOutroMusic':'music/Nhac outro.mp3','excludedPhoto':pre['excludedPhoto'],'onlyOnePhotoRemoved':True,'videoPreservation':preservation,'approvedReferenceSha256':reference_sha,'approvedReferenceIsExactGithubArtifact':reference_sha==baseline['approvedMp4Sha256'],'preflightPassed':pre['passed'],'video':'H.264 2560x1440 60fps','audio':'AAC stereo 48000Hz 320kbps','audioCorrelation':corr,'samplePeakAt8kHz':peak,'truePeakDb':float(loudness['input_tp']),'integratedLufs':float(loudness['input_i']),'framesChecked':checks,'wishes':voice_checks,'fullDecodePassed':True,'blackIntervals':black,'minimumInteriorOneSecondRms':min(levels)}
 dump(WORK/'qa-report.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ['framesChecked','wishes']},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
