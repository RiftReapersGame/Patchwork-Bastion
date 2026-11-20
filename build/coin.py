# painted coin (original art supplied by the game's owner): six spin frames played forward then back as a loop,
# a four-frame sparkle for when coins land in the bank, and one glint (the sparkle's first frame) for coin trails
import sys,os,json
import numpy as np
from PIL import Image,ImageFilter
src,OUT=sys.argv[1],sys.argv[2]
def unwhite(rgb):
    mn=rgb.min(-1);a=np.clip((250-mn)/28,0,1)
    col=np.where(a[...,None]>0,(rgb-255*(1-a[...,None]))/np.maximum(a[...,None],1e-3),0)
    return np.dstack([col.clip(0,255),a*255])
def split(a,n):
    col=(a>8).sum(0).astype(float);W=len(col);cuts=[0]
    for i in range(1,n):
        c=W*i/n;lo,hi=int(c-W*.07),int(c+W*.07);cuts.append(lo+int(np.argmin(col[lo:hi]+np.abs(np.arange(lo,hi)-c)*.02)))
    cuts.append(W);return [(cuts[k],cuts[k+1]) for k in range(n)]
def frames(path,n):
    rgba=unwhite(np.asarray(Image.open(path).convert('RGB')).astype(float));out=[]
    for x0,x1 in split(rgba[...,3],n):
        f=rgba[:,x0:x1];ys,xs=np.nonzero(f[...,3]>10);out.append(Image.fromarray(f[ys.min():ys.max()+1,xs.min():xs.max()+1].clip(0,255).astype('uint8'),'RGBA'))
    return out
def sheet(fr,order,P,name,fit=1):
    cw=max(f.width for f in fr);ch=max(f.height for f in fr);s=min(P/cw,P/ch)*fit
    S=Image.new('RGBA',(P*len(order),P),(0,0,0,0))
    for i,k in enumerate(order):
        im=fr[k].resize((max(1,round(fr[k].width*s)),max(1,round(fr[k].height*s))),Image.LANCZOS)
        rgb=im.convert('RGB').filter(ImageFilter.UnsharpMask(1,70,2)).convert('RGBA');rgb.putalpha(im.getchannel('A'))
        S.paste(rgb,(i*P+(P-rgb.width)//2,(P-rgb.height)//2),rgb)
    S.save(os.path.join(OUT,name+'.png'),optimize=True);return {'f':len(order),'w':P/2,'h':P/2,'ax':P/4,'ay':P/4,'s':1,'k':2}
M={}
c=frames(os.path.join(src,'spin.png'),6);M['coin']=sheet(c,[0,1,2,3,4,5,4,3,2,1],72,'coin',.96)
sp=frames(os.path.join(src,'sparkle.png'),4);M['coin_spark']=sheet(sp,[0,1,2,2,3],96,'coin_spark',1)
M['coin_glint']=sheet([sp[0]],[0],32,'coin_glint',1)
if os.path.exists(os.path.join(src,'die.png')):
    d=frames(os.path.join(src,'die.png'),6);M['die']=sheet(d,[0,1,2,3,4,5],160,'die',1)
print(json.dumps(M))
