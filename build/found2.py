# painted foundation block (floor on top, wall face below) supplied by the game's owner -> the game's floor and wall tiles
import sys,random,numpy as np
from PIL import Image,ImageDraw,ImageFilter
SRCS,OUT=sys.argv[1].split(','),sys.argv[2];T=128;WH=T*28//64;INK=(52,38,40,255);JOINT=(96,78,72,150)
def pieces(SRC):
    inner=SRC.endswith('!');SRC=SRC.rstrip('!')
    im=Image.open(SRC).convert('RGB');a=np.asarray(im).astype(int);nz=np.argwhere(a.min(-1)<225);y0,x0=nz.min(0);y1,x1=nz.max(0);W=x1-x0;H=y1-y0
    fx0=x0+int(W*.10);fs=int(W*.80);fy0=y0+int(H*.035)
    if inner:fx0=x0+int(W*.19);fs=int(W*.62);fy0=y0+int(H*.11)      # these have a ring of stones round the floor: keep the paving inside it
    fl=im.crop((fx0,fy0,fx0+fs,fy0+fs)).resize((T,T),Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.5,90,2))
    wl=im.crop((x0+int(W*.04),y0+int(H*.735),x1-int(W*.04),y1-int(H*.012))).resize((T,WH),Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.5,90,2))
    return fl,wl
r=random.Random(3)
def edge(d,p0,p1,col,w):
    n=9;d.line([(p0[0]+(p1[0]-p0[0])*i/n+r.uniform(-.7,.7),p0[1]+(p1[1]-p0[1])*i/n+r.uniform(-.7,.7)) for i in range(n+1)],fill=col,width=w,joint='curve')
N=len(SRCS);base=Image.new('RGBA',(T*4*N,T*4));wall=Image.new('RGBA',(T*4*N,WH))
for v,SRC in enumerate(SRCS):
    fl,wl=pieces(SRC)
    for ty in range(4):
        for tx in range(4):
            t=fl.convert('RGBA');ov=Image.new('RGBA',(T,T),(0,0,0,0));d=ImageDraw.Draw(ov)
            L,R,U,D=tx in(0,3),tx in(2,3),ty in(0,3),ty in(2,3)
            edge(d,(1,0),(1,T),INK if L else JOINT,6 if L else 2);edge(d,(T-2,0),(T-2,T),INK if R else JOINT,6 if R else 2)
            edge(d,(0,1),(T,1),INK if U else JOINT,6 if U else 2);edge(d,(0,T-2),(T,T-2),INK if D else JOINT,5 if D else 2)
            base.paste(Image.alpha_composite(t,ov),((v*4+tx)*T,ty*T))
    for tx in range(4):
        t=wl.convert('RGBA');ov=Image.new('RGBA',(T,WH),(0,0,0,0));d=ImageDraw.Draw(ov)
        if tx in(0,3):edge(d,(1,0),(1,WH),INK,6)
        if tx in(2,3):edge(d,(T-2,0),(T-2,WH),INK,6)
        edge(d,(0,WH-2),(T,WH-2),INK,5);wall.paste(Image.alpha_composite(t,ov),((v*4+tx)*T,0))
base.convert('RGB').quantize(240,method=0).save(OUT+'/base.png',optimize=True)
wall.convert('RGB').quantize(220,method=0).save(OUT+'/wall.png',optimize=True)

# a whole block with its stone rim becomes the raised slab for plots built over a road
if len(sys.argv)>3:
    from scipy import ndimage as ndi
    a=np.asarray(Image.open(sys.argv[3]).convert('RGB')).astype(float);mn=a.min(-1)
    lab,_=ndi.label(mn>232);e=set(lab[0,:])|set(lab[-1,:])|set(lab[:,0])|set(lab[:,-1]);e.discard(0);bg=np.isin(lab,list(e))
    solid=ndi.binary_opening(ndi.binary_fill_holes(~bg),iterations=3);al=ndi.gaussian_filter(np.where(solid,255.,0.),1.2)
    sl=Image.fromarray(np.dstack([a,al]).astype('uint8'));sl=sl.crop(sl.getbbox()).resize((144,150),Image.LANCZOS)
    core=sl.getchannel('A').point(lambda v:255 if v>128 else 0);ring=core.filter(ImageFilter.MaxFilter(5));out=Image.new('RGBA',sl.size,(44,32,40,0));out.putalpha(ring);out.paste(sl.convert('RGB').filter(ImageFilter.UnsharpMask(1.5,90,2)),(0,0),core)
    out.quantize(200,method=2).save(OUT+'/slab.png',optimize=True)
