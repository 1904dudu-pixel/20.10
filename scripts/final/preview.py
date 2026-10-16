from common import *
from render import render_scene,join
m=load_manifest();scenes=[next(s for s in m['scenes'] if s['id']==id).copy() for id in ['photo-01','wish-02']]
path=WORK/'preview-scenes'
for s in scenes:render_scene(s,960,540,30,path)
# Extract their original timeline audio, respecting the same overlap as the full export.
from audio import wav
import numpy as np
parts=[pcm(ROOT/'public'/m['audioSrc'],extra=['-ss',s['startFrame']/60,'-t',s['durationInFrames']/60]) for s in scenes]
fade=round(m['transitionFrames']/60*48000);r=np.linspace(0,1,fade)[:,None]
a=np.concatenate([parts[0][:-fade],parts[0][-fade:]*(1-r)+parts[1][:fade]*r,parts[1][fade:]])
wav(WORK/'preview-audio.wav',a)
join(scenes,WORK/'preview.mp4',960,540,30,path,WORK/'preview-audio.wav')
print('Preview written',flush=True)
