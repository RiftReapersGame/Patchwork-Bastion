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
# fit the bridge to the grid: exactly one plot wide, its deck flush with the floor beside it and its feet level with the bottom of the walls
W0,H0=res.size;split=int(H0*.47);deck=res.crop((0,0,W0,split));arch=res.crop((0,split,W0,H0))
da=np.asarray(deck);rows=[]
for y in range(da.shape[0]):                       # square the deck up: every row runs the full width (the drawing tapers toward the back)
    xs=np.nonzero(da[y,:,3]>128)[0]
    if len(xs)>W0*.5:rows.append(np.asarray(Image.fromarray(da[y:y+1,xs[0]:xs[-1]+1]).resize((W0,1),Image.BILINEAR))[0])
deck=Image.fromarray(np.array(rows)) if rows else deck
aa=np.asarray(arch);xs=np.nonzero(aa[...,3].max(0)>128)[0];arch=arch.crop((int(xs[0]),0,int(xs[-1])+1,arch.height))
UW=64;K=2.4;DH=34;AH=58;UH=DH+AH
big=Image.new('RGBA',(int(UW*K),int(UH*K)),(0,0,0,0))
big.paste(deck.resize((int(UW*K),int(DH*K)),Image.LANCZOS),(0,0));ar=arch.resize((int(UW*K),int(UH*K)-int(DH*K)),Image.LANCZOS);big.paste(ar,(0,int(DH*K)))
core=big.getchannel('A').point(lambda v:255 if v>128 else 0);ring=core.filter(ImageFilter.MaxFilter(5));out=Image.new('RGBA',big.size,(44,32,40,0));out.putalpha(ring);out.paste(big.convert('RGB').filter(ImageFilter.UnsharpMask(1.5,90,2)),(0,0),core)
out.quantize(255,method=2).save(OUT+'/bridge.png',optimize=True)
print(json.dumps({'bridge':{'f':1,'w':UW,'h':UH,'ax':UW/2,'ay':UH,'s':1,'k':K}}))
