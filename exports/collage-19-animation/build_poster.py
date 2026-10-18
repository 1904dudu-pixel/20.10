"""Original portrait crops only; same approved background, type and soft frames."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFilter,ImageFont,ImageOps

HERE=Path(__file__).parent
parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2])
parser.add_argument('--out-dir',type=Path)
args=parser.parse_args()
OUT=args.out_dir or args.repo/'exports';OUT.mkdir(parents=True,exist_ok=True)
records=json.loads((HERE/'portraits.json').read_text())
assert len(records)==19 and len({r['path'] for r in records})==19
assert records[8]['path']=='public/photos/09_NGUYỄN THỊ THOA.png'
W,H=3840,2160
bg=args.repo/'public/photos/ẢNH NỀN.png'
assert hashlib.sha256(bg.read_bytes()).hexdigest()=='602116209d81e85460405910fb1098a161333296ea29742b723f9ef26b83b15b'
background=ImageOps.fit(Image.open(bg).convert('RGB'),(W,H),Image.Resampling.LANCZOS,centering=(.5,.5))
shadows=Image.new('RGBA',(W,H));photos=Image.new('RGBA',(W,H));manifest=[];boxes=[]
def rounded(size,radius):
 mask=Image.new('L',(size*4,size*4));ImageDraw.Draw(mask).rounded_rectangle((0,0,size*4-1,size*4-1),radius=radius*4,fill=255)
 return mask.resize((size,size),Image.Resampling.LANCZOS)
for r in records:
 p=args.repo/r['path'];raw=p.read_bytes()
 assert hashlib.sha256(raw).hexdigest()==r['sha256']
 assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==r['githubBlobSha']
 crop=r['sourceCrop'];assert crop[2]-crop[0]==crop[3]-crop[1]
 size=r['size'];x=r['center'][0]-size//2;y=r['center'][1]-size//2;radius=round(size*.22)
 portrait=Image.open(p).convert('RGB').crop(crop).resize((size,size),Image.Resampling.LANCZOS)
 shadow=Image.new('RGBA',(size+104,size+104));ImageDraw.Draw(shadow).rounded_rectangle((45,48,size+59,size+62),radius=radius+7,fill=(35,74,100,47))
 shadows.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(15)),(x-52,y-45))
 card=Image.new('RGBA',(size+14,size+14),'white');card.putalpha(rounded(size+14,radius+7));photos.alpha_composite(card,(x-7,y-7))
 picture=portrait.convert('RGBA');picture.putalpha(rounded(size,radius));photos.alpha_composite(picture,(x,y))
 boxes.append((x-7,y-7,x+size+7,y+size+7))
 manifest.append({**r,'destinationPhotoRect':[x,y,x+size,y+size],'frameRadius':radius,'individualNameLabel':False})
for i,a in enumerate(boxes):
 assert 40<=a[0] and a[2]<=W-40 and 320<a[1] and a[3]<=H-10,a
 for b in boxes[i+1:]:assert min(a[2],b[2])<=max(a[0],b[0]) or min(a[3],b[3])<=max(a[1],b[1]),(a,b)
image=Image.alpha_composite(Image.alpha_composite(background.convert('RGBA'),shadows),photos)

# Exactly the approved Great Vibes lettering, coordinates, colours and swashes.
title=Image.new('RGBA',(W,320));td=ImageDraw.Draw(title);font=HERE/'fonts/GreatVibes-Regular.ttf'
main=ImageFont.truetype(str(font),156);wish=ImageFont.truetype(str(font),118);date=ImageFont.truetype(str(font),133)
def paint(text,left,top,f,c1,c2):
 box=td.textbbox((0,0),text,font=f);width,height=box[2]-box[0],box[3]-box[1]
 mask=Image.new('L',(width+12,height+12));ImageDraw.Draw(mask).text((6-box[0],6-box[1]),text,font=f,fill=255)
 yy=np.linspace(0,1,mask.height)[:,None,None];a=np.array(c1)[None,None,:];b=np.array(c2)[None,None,:]
 pixels=np.broadcast_to(np.round(a*(1-yy)+b*yy).astype('uint8'),(mask.height,mask.width,3)).copy()
 ink=Image.fromarray(pixels).convert('RGBA');ink.putalpha(mask);title.alpha_composite(ink,(round(left)-6,top-6))
 return width
box=td.textbbox((0,0),'OPPO Bắc Ninh',font=main)
paint('OPPO Bắc Ninh',(W-(box[2]-box[0]))/2,36,main,(22,91,106),(48,116,137))
box1=td.textbbox((0,0),'chúc mừng',font=wish);box2=td.textbbox((0,0),'20/10',font=date)
width=box1[2]-box1[0];start=(W-width-34-(box2[2]-box2[0]))/2
paint('chúc mừng',start,203,wish,(37,102,119),(56,118,134))
paint('20/10',start+width+34,198,date,(176,143,87),(133,94,45))
def bezier(points):
 out=[]
 for t in np.linspace(0,1,100):
  x=(1-t)**3*points[0][0]+3*(1-t)**2*t*points[1][0]+3*(1-t)*t*t*points[2][0]+t**3*points[3][0]
  y=(1-t)**3*points[0][1]+3*(1-t)**2*t*points[1][1]+3*(1-t)*t*t*points[2][1]+t**3*points[3][1]
  out.append((round(x),round(y)))
 return out
curve=[(1320,277),(1394,294),(1457,251),(1516,263)]
for points in [curve,[(W-x,y) for x,y in curve]]:td.line(bezier(points),fill=(169,140,94,155),width=3,joint='curve')
image.alpha_composite(title,(0,0));result=image.convert('RGB')
for r in manifest:
 box=r['destinationPhotoRect'];size=box[2]-box[0]
 original=Image.open(args.repo/r['path']).convert('RGB').crop(r['sourceCrop']).resize((size,size),Image.Resampling.LANCZOS)
 mask=np.array(rounded(size,r['frameRadius']))==255
 assert np.array_equal(np.array(result.crop(box))[mask],np.array(original)[mask]),r['name']
stem='OPPO-Bac-Ninh-19-Chan-Dung-Tieu-De-Mem-Mai-4K'
result.save(OUT/(stem+'.png'),optimize=True)
result.save(OUT/(stem+'.jpg'),quality=97,subsampling=0,optimize=True)
result.resize((1920,1080),Image.Resampling.LANCZOS).save(OUT/(stem+'-preview.jpg'),quality=95,subsampling=0)
audit={'width':W,'height':H,'photoCount':19,'uniquePhotos':19,'rows':[6,7,6],'title':'OPPO Bắc Ninh chúc mừng 20/10',
 'generativeAIUsed':False,'allOriginalPortraitPixelsVerified':True,'backgroundSha256':hashlib.sha256(bg.read_bytes()).hexdigest(),'portraits':manifest}
(HERE/'poster-manifest.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'photoCount':19,'allOriginalPortraitPixelsVerified':True,'files':[{'name':p.name,'bytes':p.stat().st_size} for p in OUT.iterdir()]},ensure_ascii=False))
