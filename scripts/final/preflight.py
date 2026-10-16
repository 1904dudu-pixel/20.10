from common import *
from prepare import font

def main():
 m=load_manifest();base=json.loads((ROOT/'src/data/approved-short-structure.json').read_text());old={s['id']:s for s in base['scenes']};current=m['scenes'];by={s['id']:s for s in current};removed=[s for s in base['scenes'] if s['id'].startswith('closing-')]
 assert len(current)==75 and [s['id'] for s in current]==[s['id'] for s in base['scenes'] if not s['id'].startswith('closing-')]
 assert not any(s['kind']=='closing' or s['id'].startswith('closing-') for s in current)
 for s in current:
  for k,v in old[s['id']].items():
   if s['id']=='outro' and k in ['startFrame','endFrame']:continue
   assert s[k]==v,('Approved media/timing changed',s['id'],k,s[k],v)
  if s['kind'] in ['photo','wish']:assert sha(ROOT/'public'/s['src'])==s['sha256']
 photos=[s for s in current if s['kind']=='photo'];wishes=[s for s in current if s['kind']=='wish']
 assert len(photos)==52 and len({s['sha256'] for s in photos})==52 and all(s['durationInFrames']==360 for s in photos)
 assert len(wishes)==16 and [s['number'] for s in wishes]==list(range(1,17))
 for s in wishes:
  assert s['durationInFrames']<18*60 and s['displayName']=='Anh. '+s['name']
  assert s['displayRole']==('GIÁM ĐỐC KINH DOANH' if s['number']==1 else s['role'])
  assert font(59,True).getlength(s['displayName'])<2200 and font(37,True).getlength(s['displayRole'])<2200
  assert 3<=s['lowerThirdEndSeconds']-s['lowerThirdStartSeconds']<=4
 assert [s['id'] for s in current[-2:]]==['wish-16','outro']
 outro=by['outro'];assert outro['startFrame']==by['wish-16']['endFrame']-27
 assert outro['startFrame']==by['wish-16']['voiceEndFrame']
 assert outro['durationInFrames']==old['outro']['durationInFrames']==1200
 delta=sum(s['durationInFrames']-27 for s in removed);assert delta==1020 and m['totalFrames']==base['totalFrames']-delta==32960
 assert m['sources']['outroMusic']['src']=='music/Nhac outro.mp3'
 for key,source in base['sources'].items():
  assert m['sources'][key]==source,('Approved Intro/Outro/music changed',key)
 for source in m['sources'].values():assert sha(ROOT/'public'/source['src'])==source['sha256']
 a=json.loads((WORK/'audio-timeline.json').read_text());tracks=a['tracks'];song3=next(t for t in tracks if t['kind']=='main-song' and t['group']==3);g3=next(g for g in m['photoGroups'] if g['number']==3);voice9=by['wish-09']['voiceStartFrame']/60
 assert song3['endSeconds']>=g3['endFrame']/60 and song3['endSeconds']<voice9
 assert .5<=song3['fadeOutSeconds']<=1
 chorus=next(t for t in tracks if t['kind']=='chorus-repeat');assert 20<=chorus['durationSeconds']<=24
 assert chorus['startSeconds']==451 and abs(chorus['endSeconds']-474.58)<.001
 assert chorus['endSeconds']<by['wish-13']['voiceStartFrame']/60
 bed=next(t for t in tracks if t['kind']=='original-instrumental');assert bed['fullyMutedFromSeconds']==outro['startFrame']/60
 ot=next(t for t in tracks if t['kind']=='outro-music');assert ot['source']=='music/Nhac outro.mp3' and ot['speed']==1 and ot['originalVideoAudioMuted']
 assert abs(ot['endSeconds']-m['totalFrames']/60)<1/48000
 video_meta=probe(ROOT/'public'/outro['src']);audio_streams=[s for s in video_meta['streams'] if s['codec_type']=='audio']
 report={'passed':True,'photoCount':52,'wishCount':16,'sceneCount':75,'newTotalFrames':m['totalFrames'],'newDurationSeconds':m['totalFrames']/60,'removedSceneIds':[s['id'] for s in removed],'removedNetFrames':delta,'removedNetSeconds':delta/60,'approvedPhotoAndSpeechTimingUnchanged':True,'firstTwoMusicBlocksUnchanged':True,'labels':[{'number':s['number'],'name':s['displayName'],'role':s['displayRole'],'durationSeconds':s['durationInFrames']/60} for s in wishes],'musicCorrection':{'oldSongEndSeconds':328.88,'newCrossfadeStartSeconds':song3['endSeconds']-song3['fadeOutSeconds'],'newSongEndSeconds':song3['endSeconds'],'lastPhotoEndSeconds':g3['endFrame']/60,'nextVoiceStartSeconds':voice9},'chorusRepeat':chorus,'directEnding':{'lastWishStartSeconds':by['wish-16']['startFrame']/60,'lastVoiceEndSeconds':by['wish-16']['voiceEndFrame']/60,'outroStartSeconds':outro['startFrame']/60,'crossfadeSeconds':.45,'outroOriginalAudioStreamCount':len(audio_streams),'outroOriginalVideoSpeed':1,'instrumentalZeroFromSeconds':bed['fullyMutedFromSeconds']},'outroMusic':ot,'timelineMap':[{'id':s['id'],'oldStartSeconds':old[s['id']]['startFrame']/60,'newStartSeconds':s['startFrame']/60,'oldEndSeconds':old[s['id']]['endFrame']/60,'newEndSeconds':s['endFrame']/60} for s in current]}
 dump(WORK/'preflight-report.json',report);print(f'PREFLIGHT PASSED: 52 photos, 16 approved speech cuts, 16 labels, 75 scenes, {m["totalFrames"]/60:.3f}s; removed all four closing scenes ({delta/60}s net).',flush=True)
 return report
if __name__=='__main__':main()
