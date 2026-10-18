"""Remove one approved photo while stream-copying every other video frame."""
from common import *
from audio_sync import approved_source
from preflight import main as preflight
from render import render_scene,join

def hashes(path):
 data=json.loads(run(['ffprobe','-v','error','-select_streams','v:0','-show_packets','-show_entries','packet=data_hash','-show_data_hash','sha256','-of','json',path],True))
 return [p['data_hash'] for p in data['packets']]

def main():
 preflight();m=load_manifest();base=json.loads((ROOT/'src/data/approved-polished-structure.json').read_text());source,digest=approved_source(base)
 by={s['id']:s for s in m['scenes']}
 left=by['photo-48'];right=by['photo-50'];cut=right['startFrame'];fade=m['transitionFrames'];delta=333;resume=cut+fade+delta
 # Reuse the exact approved scene filters, zoom/effects, smoothstep dissolve,
 # libx264 CRF 17 and existing 15360Hz video track time base.
 for scene in [left,right]:render_scene(scene)
 pair=WORK/'photo-48-to-50.mp4';join([left,right],pair)
 dest=WORK/'minimal-join';dest.mkdir(exist_ok=True)
 prefix=dest/'before.mp4';transition=dest/'transition.mp4';suffix=dest/'after.mp4'
 ff(['-i',source,'-map','0:v:0','-frames:v',cut,'-an','-c:v','copy','-video_track_timescale','15360',prefix])
 ff(['-i',pair,'-ss',(left['durationInFrames']-fade)/60,'-map','0:v:0','-frames:v',fade,'-an','-c:v','copy','-avoid_negative_ts','make_zero','-video_track_timescale','15360',transition])
 # Output seeking retains the keyframe exactly at the body of photo-50. No
 # frames from either old dissolve containing photo-49 may enter the suffix.
 ff(['-i',source,'-ss',resume/60,'-map','0:v:0','-frames:v',base['manifest']['totalFrames']-resume,'-an','-c:v','copy','-avoid_negative_ts','make_zero','-video_track_timescale','15360',suffix])
 original=hashes(source);first=hashes(prefix);last=hashes(suffix);middle=hashes(transition)
 assert first==original[:cut] and last==original[resume:] and len(middle)==fade
 listing=dest/'concat.txt';listing.write_text('\n'.join("file '"+str(p).replace("'","'\\''")+"'" for p in [prefix,transition,suffix])+'\n')
 target=ROOT/m['outputFile'];target.parent.mkdir(exist_ok=True)
 # Disable automatic Annex-B header insertion: the already muxed segments
 # contain their original parameter sets. This preserves packet bytes exactly.
 ff(['-f','concat','-safe','0','-auto_convert','0','-i',listing,'-i',ROOT/'public'/m['audioSrc'],'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','320k','-ar','48000','-t',m['totalFrames']/60,'-movflags','+faststart',target])
 actual=hashes(target);assert len(actual)==m['totalFrames']
 assert actual[:cut]==original[:cut] and actual[cut+fade:]==original[resume:] and actual[cut:cut+fade]==middle
 report={'passed':True,'approvedSourceSha256':digest,'framesCopiedWithoutReencoding':len(actual)-fade,'newCrossfadeFrames':fade,'removedFrames':delta,'outputFrames':len(actual),'newCrossfadeStartFrame':cut,'allOtherCompressedVideoFramesIdentical':True}
 dump(WORK/'minimal-render-report.json',report)
 print('MINIMAL VIDEO EXPORT PASSED: '+json.dumps(report),flush=True)
 print(f'FINAL MP4 EXISTS: {target}, {len(actual)} frames, {target.stat().st_size} bytes',flush=True)

if __name__=='__main__':main()
