import json,subprocess,hashlib,os,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
GEN=ROOT/'public/generated/final';WORK=ROOT/'work/final'
GEN.mkdir(parents=True,exist_ok=True);WORK.mkdir(parents=True,exist_ok=True)
def run(args,raw=False):
 p=subprocess.run([str(a) for a in args],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-12000:])
 return p.stdout if raw else p.stderr.decode(errors='replace')
def ff(args):return run(['ffmpeg','-hide_banner','-loglevel','error','-y',*args])
def probe(path):return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path],True))
def sha(path):return hashlib.file_digest(open(path,'rb'),'sha256').hexdigest()
def dump(path,data):Path(path).parent.mkdir(parents=True,exist_ok=True);Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def load_manifest():return json.loads((ROOT/'src/data/final-manifest.json').read_text())
def ease(p):p=max(0,min(1,p));return p*p*(3-2*p)
def pcm(path,rate=48000,channels=2,extra=[]):
 import numpy as np
 return np.frombuffer(run(['ffmpeg','-v','error',*extra,'-i',path,'-vn','-ac',channels,'-ar',rate,'-f','f32le','-'],True),dtype='<f4').reshape(-1,channels).copy()
