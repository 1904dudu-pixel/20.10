import json,math,wave
import numpy as np
from common import *
RATE=48000

def wav(path,data):
 Path(path).parent.mkdir(parents=True,exist_ok=True)
 with wave.open(str(path),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(RATE);f.writeframes((np.clip(data,-1,1)*32767).astype('<i2').tobytes())

def infer_key(mono):
 x=mono[::6];chroma=np.zeros(12)
 for start in range(0,len(x)-4096,8000):
  power=abs(np.fft.rfft(x[start:start+4096]*np.hanning(4096)))**2;freq=np.fft.rfftfreq(4096,1/8000);mask=(freq>70)&(freq<1800);midi=np.rint(69+12*np.log2(freq[mask]/440)).astype(int);np.add.at(chroma,midi%12,np.sqrt(power[mask]))
 major=np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88]);minor=np.array([6.33,2.68,3.52,5.38,2.6,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
 return max((float(np.corrcoef(chroma,np.roll(template,key))[0,1]),key,mode) for mode,template in [('major',major),('minor',minor)] for key in range(12))[1:]

def synth(root,mode):
 n=96*RATE;out=np.zeros((n,2),np.float32);rng=np.random.default_rng(2010)
 major=[(0,[0,4,7,11]),(9,[0,3,7,10]),(5,[0,4,7,11]),(7,[0,4,7,9])];minor=[(0,[0,3,7,10]),(8,[0,4,7,11]),(3,[0,4,7,11]),(10,[0,4,7,9])]
 progression=major if mode=='major' else minor
 def note(at,midi,duration,amplitude,pan,pad=False):
  start=int(at*RATE);length=min(n-start,int(duration*RATE));t=np.arange(length)/RATE;freq=440*2**((midi-69)/12)
  if pad:signal=(np.sin(2*np.pi*freq*t)+.19*np.sin(4*np.pi*freq*t))*np.sin(np.pi*t/duration)**2
  else:
   signal=sum(amp*np.sin(2*np.pi*freq*(harmonic+1)*t)*np.exp(-t*(.7+harmonic*.6)) for harmonic,amp in enumerate([1,.34,.15,.065,.025,.01]))
   signal*=1-np.exp(-t/.012);signal*=np.minimum(1,(duration-t)/.12)
  signal=(signal*amplitude).astype(np.float32);out[start:start+length,0]+=signal*np.sqrt((1-pan)/2);out[start:start+length,1]+=signal*np.sqrt((1+pan)/2)
 for bar in range(16):
  degree,intervals=progression[bar%4];base=48+root+degree
  for k,interval in enumerate(intervals):note(bar*6,base+interval,8,.027,(-.55+k*.36),True)
  note(bar*6,base-12,5.8,.045,-.12)
  for step in range(8):note(bar*6+step*.75,base+intervals[step%4]+12,3.7,.055 if step%4==0 else .039,(-.4+.8*((step%4)/3)))
 original=out.copy()
 for delay,gain in [(.11,.16),(.23,.12),(.37,.09),(.61,.065),(.83,.04)]:
  offset=int(delay*RATE);out[offset:]+=original[:-offset]*gain
 fade=int(1.2*RATE);out[:fade]*=np.linspace(0,1,fade)[:,None];out[-fade:]*=np.linspace(1,0,fade)[:,None]
 return out

def loop_bed(loop,length):
 fade=2*RATE;step=len(loop)-fade;out=np.zeros((length,2),np.float32)
 for start in range(0,length,step):
  n=min(len(loop),length-start);part=loop[:n].copy()
  if start:part[:min(fade,n)]*=np.linspace(0,1,min(fade,n))[:,None]
  if start+n<length:part[-fade:]*=np.linspace(1,0,fade)[:,None]
  out[start:start+n]+=part
 return out

def apply_fade(a,fade_in=.4,fade_out=.5):
 a=a.copy();n=min(int(fade_in*RATE),len(a)//2);k=min(int(fade_out*RATE),len(a)//2)
 if n:a[:n]*=np.linspace(0,1,n)[:,None]
 if k:a[-k:]*=np.linspace(1,0,k)[:,None]
 return a

def main():
 m=load_manifest();dest=GEN/'audio';dest.mkdir(exist_ok=True);n=math.ceil(m['totalFrames']/60*RATE)
 main_audio=pcm(ROOT/'public'/m['sources']['mainMusic']['src']);intro=pcm(ROOT/'public'/m['sources']['cinematic']['src']);key,mode=infer_key(main_audio.mean(1));ambient=synth(key,mode);wav(dest/'original-piano-ambient.wav',ambient)
 bed=loop_bed(ambient,n);voice=np.zeros((n,2),np.float32);song=np.zeros_like(voice);tracks=[];cursor=0
 def add(target,data,start_seconds):
  st=round(start_seconds*RATE);length=min(len(data),n-st)
  if length>0:target[st:st+length]+=data[:length]
 # Normalize and apply pitch-preserving atempo to the reviewed complete sentence excerpt.
 for s in [s for s in m['scenes'] if s['kind']=='wish']:
  out=dest/f'voice-{s["number"]:02}.wav';cache=out.with_suffix('.json');identity={'sha':s['sha256'],'start':s['trimStartSeconds'],'end':s['trimEndSeconds'],'speed':s['speed'],'filter':'hp70-lp12k-afftdn4-loudnorm-17-TP-3-v1'}
  if not out.exists() or not cache.exists() or json.loads(cache.read_text())!=identity:
   ff(['-ss',s['trimStartSeconds'],'-t',s['trimEndSeconds']-s['trimStartSeconds'],'-i',ROOT/'public'/s['src'],'-vn','-af',f"atempo={s['speed']},highpass=f=70,lowpass=f=12000,afftdn=nr=4:nf=-55,loudnorm=I=-17:TP=-3:LRA=11",'-ar',RATE,'-ac','2','-c:a','pcm_s16le',out]);dump(cache,identity)
  a=pcm(out);a=apply_fade(a,.012,.025);start=s['voiceStartFrame']/60;add(voice,a,start)
  tracks.append({'kind':'voice','number':s['number'],'name':s['name'],'source':s['src'],'sourceStartSeconds':s['trimStartSeconds'],'sourceEndSeconds':s['trimEndSeconds'],'startSeconds':start,'endSeconds':start+len(a)/RATE,'processedSrc':str(out.relative_to(ROOT/'public')),'targetLufs':-17,'targetTruePeakDb':-3})
  print(f'Normalized voice {s["number"]:02}: {len(a)/RATE:.3f}s',flush=True)
 # Use reviewed sung-phrase boundaries, never an arbitrary time or RMS minimum.
 edits=json.loads((ROOT/'src/data/music-edits.json').read_text());assert edits['sourceSha256']==m['sources']['mainMusic']['sha256']
 for group in m['photoGroups']:
  if cursor>=len(main_audio):break
  start=group['startFrame']/60+.25;available=(group['endFrame']-group['startFrame'])/60-.75;max_end=min(len(main_audio),cursor+int(available*RATE))
  end=round(edits['pauseSourceSeconds'][group['number']-1]*RATE) if group['number']<4 else len(main_audio)
  assert cursor<end<=max_end,('Phrase does not fit fixed photo duration',group,end,max_end)
  a=apply_fade(main_audio[cursor:end]*.70,.65,.65);add(song,a,start)
  tracks.append({'kind':'main-song','source':m['sources']['mainMusic']['src'],'group':group['number'],'sourceStartSeconds':cursor/RATE,'sourceEndSeconds':end/RATE,'startSeconds':start,'endSeconds':start+len(a)/RATE,'fadeSeconds':.65,'boundaryPolicy':'Continuous source cursor, no repeated or omitted samples; pause/resume at reviewed complete sung-phrase boundary, crossfade to original instrumental.'})
  cursor=end
 # Continuous ambient: louder between tracks; duck under voice and the sung track.
 step=960;count=(n+step-1)//step
 vr=np.zeros(count);sr=np.zeros(count)
 for i in range(count):
  aa=voice[i*step:min(n,(i+1)*step)];bb=song[i*step:min(n,(i+1)*step)];vr[i]=np.sqrt(np.mean(aa*aa));sr[i]=np.sqrt(np.mean(bb*bb))
 target=np.where(vr>.012,.18,np.where(sr>.008,.22,.78));envelope=np.zeros(count);state=.78
 for i,t in enumerate(target):state+=((1-np.exp(-.02/(.06 if t<state else .45)))*(t-state));envelope[i]=state
 # Incremental interpolation avoids allocating multiple full-length envelope arrays.
 for start in range(0,n,10*RATE):
  end=min(n,start+10*RATE);gain=np.interp(np.arange(start,end),np.arange(count)*step,envelope).astype(np.float32);bed[start:end]*=gain[:,None]
 # Cinematic keeps all decoded samples, with natural crossfade into the first photo block.
 add(song,apply_fade(intro*.80,.1,.8),0)
 mix=voice+song+bed;fade=int(3*RATE);mix[-fade:]*=np.linspace(1,0,fade)[:,None]
 peak=float(np.max(np.abs(mix)));master=min(1,.92/max(peak,1e-9));mix*=master;wav(dest/'final-mix.wav',mix)
 tracks.append({'kind':'cinematic','source':m['sources']['cinematic']['src'],'startSeconds':0,'endSeconds':len(intro)/RATE,'fadeOutSeconds':.8})
 tracks.append({'kind':'original-instrumental','source':'Project procedural piano/ambient, original composition','startSeconds':0,'endSeconds':n/RATE,'keyPitchClass':int(key),'mode':mode,'duckAttackSeconds':.06,'duckReleaseSeconds':.45,'voiceDuckGain':.18,'mainSongDuckGain':.22,'silenceBetweenSections':False})
 report={'sampleRate':RATE,'channels':2,'totalSeconds':n/RATE,'originalInstrumental':True,'mainSongSourceConsumedSeconds':cursor/RATE,'mainSongSourceDecodedSeconds':len(main_audio)/RATE,'allMainSongSamplesUsedOnce':cursor==len(main_audio),'masterGain':master,'stereoSamplePeak':float(np.max(np.abs(mix))),'tracks':tracks}
 assert cursor==len(main_audio),'Main song not fully consumed'
 dump(WORK/'audio-timeline.json',report);dump(GEN/'audio/audio-timeline.json',report)
 print(f'AUDIO: {n/RATE:.3f}s, stereo peak {report["stereoSamplePeak"]:.4f}, {len(tracks)} tracks, entire main song used once',flush=True)
if __name__=='__main__':main()
