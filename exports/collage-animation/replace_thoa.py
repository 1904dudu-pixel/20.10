"""Replace one portrait using original pixels; preserve every other poster pixel."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path,default=HERE.parents[1])
parser.add_argument('--out-dir',type=Path)
args=parser.parse_args();repo=args.repo;out=args.out_dir or repo/'exports';out.mkdir(parents=True,exist_ok=True)
basepath=repo/'exports/OPPO-Bac-Ninh-32-Chan-Dung-Tieu-De-Mem-Mai-4K.png'
assert hashlib.sha256(basepath.read_bytes()).hexdigest()=='11c1cb6f5b04628426a7339696bda625a20fda362d5d03a05137a446438c4f12'
newpath=repo/'public/photos/08_NGUYỄN THỊ THOA BN.png'
assert hashlib.sha256(newpath.read_bytes()).hexdigest()=='bf37a5318de62d0e80f00110e83b91f0a9d52a5a62cadfa81a2c9008a05b8208'
base=Image.open(basepath).convert('RGB');assert base.size==(3840,2160)
box=(3306,346,3694,734);size=388;radius=85
mask=Image.new('L',(size*4,size*4));ImageDraw.Draw(mask).rounded_rectangle((0,0,size*4-1,size*4-1),radius=radius*4,fill=255)
mask=mask.resize((size,size),Image.Resampling.LANCZOS);support=np.array(mask)>0
old=Image.open(repo/'public/photos/09_NGUYỄN THỊ THOA.png').convert('RGB').crop((70,0,770,700)).resize((size,size),Image.Resampling.LANCZOS)
matte=Image.new('RGB',(size,size),'white');matte.paste(old,(0,0),mask)
original=np.array(base.crop(box))
assert np.array_equal(original[support],np.array(matte)[support])
portrait=Image.open(newpath).convert('RGB').crop((0,0,790,790)).resize((size,size),Image.Resampling.LANCZOS)
patch=Image.new('RGB',(size,size),'white');patch.paste(portrait,(0,0),mask)
pixels=original.copy();pixels[support]=np.array(patch)[support]
result=base.copy();result.paste(Image.fromarray(pixels),box)
changed=np.any(np.array(result)!=np.array(base),axis=2)
allowed=np.zeros(changed.shape,dtype=bool);allowed[box[1]:box[3],box[0]:box[2]]=support
assert not np.any(changed&~allowed)
opaque=np.array(mask)==255
assert np.array_equal(np.array(result.crop(box))[opaque],np.array(portrait)[opaque])
stem='OPPO-Bac-Ninh-32-Chan-Dung-Thoa-BN-4K'
result.save(out/(stem+'.png'),optimize=True)
result.save(out/(stem+'.jpg'),quality=97,subsampling=0,optimize=True)
report={'photoCount':32,'replacedPhotoCount':1,'replacedOrder':8,'removedFromThisCollage':'public/photos/09_NGUYỄN THỊ THOA.png',
 'replacement':'public/photos/08_NGUYỄN THỊ THOA BN.png','sourceSha256':'bf37a5318de62d0e80f00110e83b91f0a9d52a5a62cadfa81a2c9008a05b8208','sourceGitBlobSha':'009ba07d263b065e58081c9f4d0eaf3f23ae0cd1',
 'sourceCrop':[0,0,790,790],'destinationPhotoRect':list(box),'frameRadius':radius,'generativeAIUsed':False,
 'fullOpacityPortraitPixelsMatchOriginalCrop':True,'pixelsOutsideReplacedPortraitExactlyUnchanged':True,'changedPixels':int(changed.sum()),
 'basePosterSha256':hashlib.sha256(basepath.read_bytes()).hexdigest(),'outputPosterSha256':hashlib.sha256((out/(stem+'.png')).read_bytes()).hexdigest()}
(out/'replacement-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
