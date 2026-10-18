"""Splice the approved soundtrack; never regenerate, normalize or remix its stems."""
import copy
import os
import numpy as np
from common import *

RATE=48000
CUT_START=445.0
FADE=.65

def approved_source(base):
 path=Path(os.environ.get('APPROVED_POLISHED_MP4',ROOT/'out/oppo-bac-ninh-20-10-final-polished-1440p60.mp4'))
 if not path.is_file():raise FileNotFoundError('Supply the approved Final Polished MP4 through APPROVED_POLISHED_MP4. No soundtrack will be regenerated.')
 digest=sha(path);allowed=[base['approvedMp4Sha256']]
 if not os.environ.get('GITHUB_ACTIONS'):allowed.append(base['localEquivalentMp4Sha256'])
 assert digest in allowed,('Not the approved Final Polished file',digest)
 return path,digest

def main():
 m=load_manifest();base=json.loads((ROOT/'src/data/approved-polished-structure.json').read_text());old=base['manifest'];source,digest=approved_source(base)
 delta_frames=old['totalFrames']-m['totalFrames'];assert delta_frames==333
 delta=delta_frames/m['fps'];cut_end=CUT_START+delta
 # These windows are in the approved instrumental coda before the chorus at
 # 451s. The full chorus and all later decoded PCM samples remain unchanged.
 left=CUT_START-FADE/2;right=CUT_START+FADE/2;assert right+delta<451
 raw=WORK/'approved-source-audio.f32';ff(['-i',source,'-vn','-ac','2','-ar',RATE,'-f','f32le',raw])
 reference=np.memmap(raw,dtype='<f4',mode='r').reshape(-1,2)
 old_n=old['totalFrames']*RATE//m['fps'];new_n=m['totalFrames']*RATE//m['fps'];assert len(reference)>=old_n
 reference=reference[:old_n];lo=round(left*RATE);hi=round(right*RATE);offset=round(delta*RATE)
 result=np.empty((new_n,2),dtype='<f4');result[:lo]=reference[:lo]
 t=np.linspace(0,1,hi-lo,dtype=np.float32);t=t*t*(3-2*t)
 result[lo:hi]=reference[lo:hi]*(1-t[:,None])+reference[lo+offset:hi+offset]*t[:,None]
 result[hi:]=reference[hi+offset:]
 assert np.array_equal(result[:lo],reference[:lo]) and np.array_equal(result[hi:],reference[hi+offset:])
 target_raw=WORK/'synchronized-audio.f32';result.tofile(target_raw);dest=GEN/'audio';dest.mkdir(exist_ok=True)
 # Float WAV avoids normalization or requantization outside the splice. Final
 # output keeps the existing AAC stereo 48kHz 320kbps settings in render.py.
 ff(['-f','f32le','-ar',RATE,'-ac','2','-i',target_raw,'-c:a','pcm_f32le',dest/'final-mix.wav'])
 report=copy.deepcopy(base['audio']);report['totalSeconds']=new_n/RATE
 for track in report['tracks']:
  for field in ['startSeconds','endSeconds','videoStartSeconds','fullyMutedFromSeconds','timelineStartSeconds']:
   if field in track and track[field]>=cut_end:track[field]-=delta
  if track['kind']=='main-song' and track['group']==4:
   track['technicalCodaSplice']={'oldTimelineCutStartSeconds':CUT_START,'oldTimelineCutEndSeconds':cut_end,'crossfadeSeconds':FADE}
   track['boundaryPolicy']='Approved mixed soundtrack; only instrumental coda shortened, complete sung phrases and full chorus unchanged.'
 report.update({'stereoSamplePeak':float(np.max(np.abs(result))),'soundtrackMode':'Technical splice of approved MP4 soundtrack; no synthesis, stem processing, remix, normalization or speed change','approvedSourceSha256':digest,'approvedSourceCommit':base['approvedCommit'],'synchronization':{'removedFrames':delta_frames,'removedSeconds':delta,'oldCutStartSeconds':CUT_START,'oldCutEndSeconds':cut_end,'crossfadeSeconds':FADE,'newCrossfadeStartSeconds':left,'newCrossfadeEndSeconds':right,'unchangedPcmBeforeSeconds':left,'sampleIdenticalShiftedPcmFromSeconds':right,'allGainsAndSpeedsUnchanged':True,'fullApprovedChorusPreserved':True,'sourceIsExactGithubArtifact':digest==base['approvedMp4Sha256']}})
 dump(WORK/'audio-timeline.json',report);dump(dest/'audio-timeline.json',report)
 print(f'APPROVED AUDIO SYNCHRONIZED: removed {delta:.2f}s of instrumental coda; complete chorus 445.450–469.030s; all other decoded PCM unchanged outside {left:.3f}–{right:.3f}s.',flush=True)

if __name__=='__main__':main()
