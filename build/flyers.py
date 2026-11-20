# painted flying creatures (original art supplied by the game's owner): each source image holds three
# wing poses in a row (up, level, down) facing right. Cut them out, line the bodies up, and lay them
# out as a 4-frame flap loop: up, level, down, level.
import sys,os,json
import numpy as np
from PIL import Image,ImageFilter
from scipy import ndimage as ndi

K=2.5
# visible wingspan in map cells at the flyer's own in-game scale, so each sits at its old size
SIZE={'dragon':(1.9,1.15),'phoenix':(1.45,.9),'pegasus':(1.5,1.25),'bats':(.62,1),'wyrm':(2.0,1.2),'angel':(1.2,.8),'drake':(1.8,1.05),'imp':(1.0,1.05)}

def alpha_of(im):
    mn=im.min(-1)
    lab,_=ndi.label(mn>232);e=set(lab[0,:])|set(lab[-1,:])|set(lab[:,0])|set(lab[:,-1]);e.discard(0)
    bg=np.isin(lab,list(e))
    solid=~bg
    solid=ndi.binary_opening(solid,iterations=1)
    # holes of plain white enclosed by the figure (inside a halo, between wing and body) are background too
    wl,wn=ndi.label((mn>245)&solid)
    if wn:
        ws=ndi.sum(np.ones_like(wl),wl,range(1,wn+1));solid&=~np.isin(wl,[i+1 for i,v in enumerate(ws) if v>700])
    lab,n=ndi.label(solid)
    if n:
        sz=ndi.sum(solid,lab,range(1,n+1));solid=np.isin(lab,[i+1 for i,v in enumerate(sz) if v>=250])
    return ndi.gaussian_filter(np.where(solid,255.,0.),.8)

def split(a):
    cols=(a>40).sum(0)>0;runs=[];i=0;W=len(cols)
    while i<W:
        if not cols[i]:
            j=i
            while j<W and not cols[j]:j+=1
            if i>0 and j<W:runs.append((j-i,i,j))
            i=j
        else:i+=1
    runs=sorted(sorted(runs,reverse=True)[:2],key=lambda r:r[1])
    cuts=[0]+[(r[1]+r[2])//2 for r in runs]+[W]
    return [(cuts[k],cuts[k+1]) for k in range(3)]

def body_shift(ref,fr):
    # line up the right-hand part (head and body), which does not change between poses
    def part(a):
        ys,xs=np.nonzero(a>128);x0=xs.min();x1=xs.max();cut=x1-(x1-x0)*.45
        m=np.where(np.arange(a.shape[1])[None,:]>=cut,a,0);return m
    A=part(ref)[::3,::3]/255.;B=part(fr)[::3,::3]/255.;best=(-1,0,0)
    for dy in range(-12,13):
        for dx in range(-12,13):
            s=(np.roll(np.roll(B,dy,0),dx,1)*A).sum()
            if s>best[0]:best=(s,dy,dx)
    return best[1]*3,best[2]*3

def build(path,name):
    im=np.asarray(Image.open(path).convert('RGB')).astype(float);a=alpha_of(im)
    parts=split(a);frames=[]
    for x0,x1 in parts:frames.append((im[:,x0:x1],a[:,x0:x1]))
    Wm=max(f[0].shape[1] for f in frames);H0=im.shape[0];PAD=40
    canv=[]
    for rgb,al in frames:
        c=np.zeros((H0+2*PAD,Wm+2*PAD,4));w=rgb.shape[1]
        c[PAD:PAD+H0,PAD:PAD+w,:3]=rgb;c[PAD:PAD+H0,PAD:PAD+w,3]=al;canv.append(c)
    out=[canv[1]]
    for i in (0,2):
        dy,dx=body_shift(canv[1][...,3],canv[i][...,3]);out.append(np.roll(np.roll(canv[i],dy,0),dx,1))
    up,lev,down=out[1],out[0],out[2]
    al=np.maximum.reduce([f[...,3] for f in (up,lev,down)]);ys,xs=np.nonzero(al>10)
    y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    span,sc=SIZE[name];Wu=span*64/sc;P=int(round(Wu*K));Q=int(round(P*(y1-y0)/(x1-x0)))
    tiles=[]
    for f in (up,lev,down,lev):
        t=Image.fromarray(f[y0:y1,x0:x1].clip(0,255).astype('uint8'),'RGBA').resize((P,Q),Image.LANCZOS)
        rgb=t.convert('RGB').filter(ImageFilter.UnsharpMask(1.5,90,2));t2=rgb.convert('RGBA');t2.putalpha(t.getchannel('A'));tiles.append(t2)
    sheet=Image.new('RGBA',(P*4,Q),(0,0,0,0))
    for i,t in enumerate(tiles):sheet.paste(t,(i*P,0))
    return sheet,{'f':4,'w':P/K,'h':Q/K,'ax':P/K/2,'ay':Q/K/2,'s':1,'k':K}

if __name__=='__main__':
    src,OUT=sys.argv[1],sys.argv[2];M={}
    for f in sorted(os.listdir(src)):
        if not f.endswith('.png'):continue
        n=f[:-4];sheet,m=build(os.path.join(src,f),n)
        sheet.save(os.path.join(OUT,'pf_'+n+'.png'),optimize=True);M['pf_'+n]=m
    print(json.dumps(M))
