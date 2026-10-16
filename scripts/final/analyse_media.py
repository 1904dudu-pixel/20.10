import json,subprocess,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
NAMES=[('NGUYỄN CÔNG HƯNG','RM'),('TRẦN TUẤN HƯNG','SALE LEADER'),('PHAN ĐÌNH QUYỀN','SALE LEADER'),('NGUYỄN KINH TUẤN','SALE LEADER'),('LƯU VĂN BÁCH','IOT LEADER'),('NGUYỄN THẾ DUY','TRAINER'),('NGÔ VĂN THÁI','TRAINER'),('ĐÀO ĐĂNG THÙY','SALE BẮC GIANG'),('LƯƠNG VĂN TUẤN','SALE BẮC GIANG'),('NGUYỄN THẠC TÙNG','SALE BẮC NINH'),('NGUYỄN THẾ ANH','SALE LẠNG SƠN'),('NGUYỄN TRƯỜNG GIANG','SALE HƯNG YÊN'),('TRIỆU VIẾT HƯỚNG','SALE BẮC GIANG'),('VŨ THẾ DUY','SALE LẠNG SƠN'),('NGUYỄN VĂN LƯƠNG','PB BẮC NINH'),('PHẠM VĂN TÙNG','PB BẮC NINH')]
def run(args):
 p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace')[-8000:])
 return p.stdout,p.stderr.decode(errors='replace')
def probe(path):return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)])[0])
def sha(path):return hashlib.file_digest(open(path,'rb'),'sha256').hexdigest()
def normalize(s):return re.sub(r'[^\w]','',s.upper())
def main():
 work=ROOT/'work/final';work.mkdir(parents=True,exist_ok=True)
 files=list((ROOT/'public/videos/wishes').glob('*')); indexed={}
 for f in files:
  if not f.is_file() or f.suffix.lower() not in ['.mp4','.mov','.m4v']:continue
  m=re.match(r'^(\d+)[\s.,_-]*',f.stem)
  if not m:raise ValueError('Missing numeric order: '+f.name)
  index=int(m[1]);assert index not in indexed,'Duplicate wish number';indexed[index]=f
 assert sorted(indexed)==list(range(1,17)),f'Missing/excess wishes: {sorted(indexed)}'
 records=[]
 for i,(name,role) in enumerate(NAMES,1):
  f=indexed[i];assert normalize(re.sub(r'^\d+[\s.,_-]*','',f.stem))==normalize(name+' '+role),f'Wrong identity: {f.name}'
  p=probe(f);v=next(s for s in p['streams'] if s['codec_type']=='video');a=next((s for s in p['streams'] if s['codec_type']=='audio'),None);assert a,f'No voice audio: {f.name}'
  duration=float(p['format']['duration']);rot=next((s.get('rotation',0) for s in v.get('side_data_list',[]) if 'rotation'in s),0)
  _,log=run(['ffmpeg','-hide_banner','-nostats','-i',str(f),'-vn','-af','loudnorm=I=-17:TP=-3:LRA=11:print_format=json','-f','null','-'])
  loud=json.loads(re.findall(r'\{\s*"input_i".*?\}',log,re.S)[-1]);threshold=min(-40,float(loud['input_thresh'])-10)
  _,log=run(['ffmpeg','-hide_banner','-nostats','-i',str(f),'-vn','-af',f'silencedetect=noise={threshold}dB:d=0.65','-f','null','-'])
  events=[(kind,float(t)) for kind,t in re.findall(r'silence_(start|end): ([\d.]+)',log)]
  lead=0.;tail=duration
  if events and events[0][0]=='start' and events[0][1]<0.05 and len(events)>1 and events[1][0]=='end' and events[1][1]>=1.0:lead=max(0,events[1][1]-0.4)
  starts=[t for kind,t in events if kind=='start'];ends=[t for kind,t in events if kind=='end']
  if starts and ends and ends[-1]>=duration-0.08 and duration-starts[-1]>=1.0:tail=min(duration,starts[-1]+0.4)
  # Never remove ambiguous low-level speech, internal pauses, laughter or camera noise.
  lead=int(lead*60)/60;tail=min(duration,__import__('math').ceil(tail*60)/60)
  if tail-lead<2:lead=0.;tail=duration
  w,h=v['width'],v['height'];display=[h,w] if abs(rot)%180 else [w,h]
  rec={'number':i,'name':name,'role':role,'src':str(f.relative_to(ROOT/'public')),'sha256':sha(f),'sourceSeconds':duration,'width':w,'height':h,'rotation':rot,'displaySize':display,'sourceFps':v['avg_frame_rate'],'sampleRate':a['sample_rate'],'channels':a['channels'],'trimStartSeconds':lead,'trimEndSeconds':tail,'removedHeadSeconds':lead,'removedTailSeconds':duration-tail,'keptSeconds':tail-lead,'loudness':loud,'silenceThresholdDb':threshold,'silenceEvents':events,'trimPolicy':'Only continuous edge silence >=1s at conservative threshold; retain >=0.4s. Ambiguous/noisy edges and all internal pauses retained.'}
  records.append(rec);print(json.dumps({k:rec[k] for k in ['number','name','sourceSeconds','displaySize','rotation','removedHeadSeconds','removedTailSeconds','keptSeconds']},ensure_ascii=False),flush=True)
 (work/'wishes-analysis.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
 # Small contact sheet includes start, middle and end of each original clip, with autorotation.
 from PIL import Image,ImageDraw
 sheet=Image.new('RGB',(1200,16*180),'#faf6ed');d=ImageDraw.Draw(sheet)
 for row,r in enumerate(records):
  f=ROOT/'public'/r['src']
  for col,t in enumerate([min(.6,r['keptSeconds']/3),r['sourceSeconds']/2,max(0,r['sourceSeconds']-.6)]):
   pic=work/f'wish-{r["number"]:02}-{col}.png';run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(f),'-frames:v','1','-vf','scale=390:145:force_original_aspect_ratio=decrease','-threads','1',str(pic)])
   im=Image.open(pic);sheet.paste(im,(col*400+(390-im.width)//2,row*180));d.text((col*400+5,row*180+148),f'{r["number"]:02} {r["name"]} | {t:.1f}s',fill='#07533e')
 sheet.save(work/'wishes-contact.jpg')
if __name__=='__main__':main()
