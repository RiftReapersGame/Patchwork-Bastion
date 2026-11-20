# overpass: an arched stone bridge. The space under the main arch is cut clear so the game's road and the goblins on it show through.
import sys,json,numpy as np
from PIL import Image,ImageFilter,ImageDraw
from scipy import ndimage as ndi
SRC,OUT=sys.argv[1],sys.argv[2]
im=Image.open(SRC).convert('RGB');a=np.asarray(im).astype(float);mn=a.min(-1);H,W=mn.shape
lab,n=ndi.label(mn>236);sz=ndi.sum(np.ones_like(lab),lab,range(1,n+1));white=np.isin(lab,[i+1 for i,v in enumerate(sz) if v>500])
# the opening: start from the white hole under the main arch and take everything below it between the front piers
hole=np.zeros_like(white);cl,cn=ndi.label(white)
cid=cl[int(H*.63),W//2]
if cid:hole=cl==cid
ys,xs=np.nonzero(hole);m=Image.new('L',(W,H),0);d=ImageDraw.Draw(m)
if len(ys):
    top=ys.min();cx=W//2;rx=int(W*.225);ry=int((H*.70-top)+H*.012)
    d.pieslice([cx-rx,top-int(H*.012),cx+rx,top-int(H*.012)+2*ry],180,360,fill=255);d.rectangle([cx-rx,top-int(H*.012)+ry,cx+rx,int(H*.83)],fill=255)
clear=white|(np.asarray(m)>0)
solid=~clear;solid=ndi.binary_opening(solid,iterations=2)
al=ndi.gaussian_filter(np.where(solid,255.,0.),1.0)
res=Image.fromarray(np.dstack([a,al]).astype('uint8'));bb=res.getbbox();res=res.crop(bb)
UW=68;K=2.4;UH=round(res.height*UW/res.width);big=res.resize((int(UW*K),int(UH*K)),Image.LANCZOS)
core=big.getchannel('A').point(lambda v:255 if v>128 else 0);ring=core.filter(ImageFilter.MaxFilter(5));out=Image.new('RGBA',big.size,(44,32,40,0));out.putalpha(ring);out.paste(big.convert('RGB').filter(ImageFilter.UnsharpMask(1.5,90,2)),(0,0),core)
out.quantize(255,method=2).save(OUT+'/bridge.png',optimize=True)
print(json.dumps({'bridge':{'f':1,'w':UW,'h':UH,'ax':UW/2,'ay':UH,'s':1,'k':K}}))
