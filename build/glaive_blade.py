# the Glaive thrower's spinning blade, taken from the tower painting itself: the lower points are hidden
# by the frame, so one clean point is copied round the hub five times and the brass hub is laid back on top.
import sys,os,json,math
import numpy as np
from PIL import Image,ImageFilter
sys.path.insert(0,'/home/claude/pipe')
from flyers import alpha_of
src,OUT=sys.argv[1],sys.argv[2]
raw=Image.open(src).convert('RGB');R=np.asarray(raw).astype(float);A=alpha_of(R)
rgba=Image.fromarray(np.dstack([R,A]).clip(0,255).astype('uint8'),'RGBA')
cx,cy=624,375;a0=-131
H,W=A.shape;yy,xx=np.mgrid[0:H,0:W];ang=(np.degrees(np.arctan2(yy-cy,xx-cx))-a0)%360;rad=np.hypot(xx-cx,yy-cy)
sect=np.asarray(rgba).copy();sect[...,3]=np.where((ang<72.5)&(rad<450),sect[...,3],0)
S=Image.fromarray(sect,'RGBA');big=Image.new('RGBA',(W,H),(0,0,0,0))
for k in range(5):big=Image.alpha_composite(big,S.rotate(-72*k,resample=Image.BICUBIC,center=(cx,cy)))
hub=np.asarray(rgba).copy();hub[...,3]=np.where(rad<104,hub[...,3],0);big=Image.alpha_composite(big,Image.fromarray(hub,'RGBA'))
from scipy import ndimage as ndi
al=np.asarray(big)[...,3]>40;lab,n=ndi.label(al);sz=ndi.sum(al,lab,range(1,n+1));keep=lab==(1+int(np.argmax(sz)))
keep=ndi.binary_dilation(keep,iterations=2);arr=np.asarray(big).copy();arr[...,3]=np.where(keep,arr[...,3],0);big=Image.fromarray(arr,'RGBA')
big=big.crop(big.getbbox());K=4;D=.55;P=int(D*64*K);big=big.resize((P,round(P*big.height/big.width)),Image.LANCZOS)
rgb=big.convert('RGB').filter(ImageFilter.UnsharpMask(1.2,80,2)).convert('RGBA');rgb.putalpha(big.getchannel('A'))
rgb.save(os.path.join(OUT,'pj_glaive.png'),optimize=True)
w,h=rgb.width/K,rgb.height/K
print(json.dumps({'pj_glaive':{'f':1,'w':w,'h':h,'ax':w/2,'ay':h/2,'s':1,'k':K}}))
