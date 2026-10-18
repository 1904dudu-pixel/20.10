from common import *

EXCLUDED='photos/10_ĐINH THỊ THU TRANG.png'

def main():
 m=load_manifest();baseline=json.loads((ROOT/'src/data/approved-polished-structure.json').read_text());base=baseline['manifest']
 old={s['id']:s for s in base['scenes']};by={s['id']:s for s in m['scenes']};removed=old['photo-49'];delta=removed['durationInFrames']-base['transitionFrames']
 assert removed['src']==EXCLUDED and delta==333
 assert len(m['scenes'])==74 and [s['id'] for s in m['scenes']]==[s['id'] for s in base['scenes'] if s['id']!='photo-49']
 assert m['excludedPhotos']==[EXCLUDED] and (ROOT/'public'/EXCLUDED).is_file()
 assert m['photos']==[p for p in base['photos'] if p['src']!=EXCLUDED]
 assert m['wishes']==base['wishes'] and m['sources']==base['sources']
 assert all(m[k]==base[k] for k in ['fps','width','height','transitionFrames','audioSrc','removedSceneIds','outroOriginalAudioMuted','instrumentalOrigin'])
 timing={'startFrame','endFrame','voiceStartFrame','voiceEndFrame'}
 for s in m['scenes']:
  shift=delta if old[s['id']]['startFrame']>removed['startFrame'] else 0
  for key,value in old[s['id']].items():
   assert s[key]==(value-shift if key in timing else value),('Unrequested scene change',s['id'],key,s[key],value)
  if s['kind'] in ['photo','wish']:assert sha(ROOT/'public'/s['src'])==s['sha256']
 for source in m['sources'].values():assert sha(ROOT/'public'/source['src'])==source['sha256']
 photos=[s for s in m['scenes'] if s['kind']=='photo'];wishes=[s for s in m['scenes'] if s['kind']=='wish']
 assert len(photos)==m['photoCount']==51 and len({s['sha256'] for s in photos})==51
 assert [s['src'] for s in photos]==sorted(s['src'] for s in photos)
 assert all(s['durationInFrames']==360 and s['src']!=EXCLUDED for s in photos)
 assert [s['photoNumber'] for s in photos]==[i for i in range(1,53) if i!=49]
 assert len(wishes)==m['wishCount']==16 and [s['number'] for s in wishes]==list(range(1,17))
 assert all(s['durationInFrames']<1080 for s in wishes)
 assert m['totalFrames']==base['totalFrames']-delta==32627
 for left,right in zip(m['scenes'],m['scenes'][1:]):assert right['startFrame']==left['endFrame']-27
 assert by['photo-50']['startFrame']==by['photo-48']['endFrame']-27
 assert [s['id'] for s in m['scenes'][-2:]]==['wish-16','outro']
 assert by['outro']['startFrame']==by['wish-16']['voiceEndFrame']
 a=json.loads((WORK/'audio-timeline.json').read_text());old_audio=baseline['audio'];sync=a['synchronization']
 assert sync['removedFrames']==333 and sync['allGainsAndSpeedsUnchanged'] and sync['fullApprovedChorusPreserved']
 for previous,current in zip(old_audio['tracks'],a['tracks']):
  for key,value in previous.items():
   expected=value-delta/60 if key in ['startSeconds','endSeconds','videoStartSeconds','fullyMutedFromSeconds','timelineStartSeconds'] and value>=sync['oldCutEndSeconds'] else value
   if key=='boundaryPolicy' and previous['kind']=='main-song' and previous['group']==4:continue
   assert current[key]==expected,('Unrequested music change',current['kind'],key)
 chorus=next(t for t in a['tracks'] if t['kind']=='chorus-repeat')
 assert abs(chorus['startSeconds']-445.45)<1e-6 and abs(chorus['endSeconds']-469.03)<1e-6
 assert chorus['durationSeconds']==23.58 and chorus['endSeconds']<by['wish-13']['voiceStartFrame']/60
 assert sync['sampleIdenticalShiftedPcmFromSeconds']<chorus['startSeconds']
 bed=next(t for t in a['tracks'] if t['kind']=='original-instrumental');assert abs(bed['fullyMutedFromSeconds']-by['outro']['startFrame']/60)<1e-6
 assert abs(a['totalSeconds']-m['totalFrames']/60)<1/48000
 report={'passed':True,'approvedBaseCommit':baseline['approvedCommit'],'photoCount':51,'wishCount':16,'sceneCount':74,'excludedPhoto':EXCLUDED,'excludedScene':'photo-49','originalPhotoFileRetained':True,'removedNetFrames':delta,'removedNetSeconds':delta/60,'newTotalFrames':m['totalFrames'],'newDurationSeconds':m['totalFrames']/60,'allOtherScenesAndEffectsUnchanged':True,'allNamesRolesSpeechCutsAndSpeedsUnchanged':True,'renderSettingsUnchanged':True,'chorusRepeat':chorus,'audioSynchronization':sync,'newPhoto48To50CrossfadeSeconds':[by['photo-50']['startFrame']/60,(by['photo-50']['startFrame']+27)/60],'nextMaleGroupStartSeconds':by['wish-13']['voiceStartFrame']/60,'outroStartSeconds':by['outro']['startFrame']/60,'timelineMap':[{'id':s['id'],'oldStartSeconds':old[s['id']]['startFrame']/60,'newStartSeconds':s['startFrame']/60,'oldEndSeconds':old[s['id']]['endFrame']/60,'newEndSeconds':s['endFrame']/60} for s in m['scenes']]}
 dump(WORK/'preflight-report.json',report)
 print(f'PREFLIGHT PASSED: only photo-49 removed; 51 photos, 16 unchanged wishes, 74 scenes, {m["totalFrames"]/60:.3f}s; all other scene data and settings match Final Polished.',flush=True)
 return report

if __name__=='__main__':main()
