# painted scenery and ground (original art supplied by the game's owner):
# trees, bushes, rocks, sea rocks, a walking sheep, seamless grass / water textures, and
# edge-and-corner sheets for meadow patches, island sand and island grass, built from the painted textures
# in the exact 4x4 layout the game's auto() expects (col: left edge, middle, right edge, single; same for rows).
import sys,os,json,math
import numpy as np
from PIL import Image,ImageFilter
sys.path.insert(0,'/home/claude/pipe')
from paint2 import cutout
from flyers import alpha_of
from gob import split,top_shift

K=2.5
def save(im,OUT,n):im.save(os.path.join(OUT,n+'.png'),optimize=True)
def sharpen(im):
    rgb=im.convert('RGB').filter(ImageFilter.UnsharpMask(1.5,90,2)).convert('RGBA');rgb.putalpha(im.getchannel('A'));return rgb

def prop(im,hc,sc,ay_pad=1):
    # scale a cut-out so it stands hc map cells tall when drawn at in-game scale sc
    bb=im.getbbox();im=im.crop(bb);H=hc*64/sc;Q=int(round(H*K));P=int(round(Q*im.width/im.height))
    im=sharpen(im.resize((P,Q),Image.LANCZOS));return im,{'f':1,'w':P/K,'h':Q/K,'ax':P/K/2,'ay':Q/K-ay_pad,'s':1,'k':K}

def row(path,n):
    im=np.asarray(Image.open(path).convert('RGB')).astype(float);a=alpha_of(im);out=[]
    for x0,x1 in split(a,n):
        t=Image.fromarray(np.dstack([im[:,x0:x1],a[:,x0:x1]]).clip(0,255).astype('uint8'),'RGBA');out.append(t.crop(t.getbbox()))
    return out

def seamless(arr):
    # blend the texture with itself shifted by half, so its edges wrap without a visible seam
    h,w=arr.shape[:2];B=np.roll(np.roll(arr,h//2,0),w//2,1)
    y=np.linspace(0,1,h)[:,None];x=np.linspace(0,1,w)[None,:]
    m=np.minimum(np.minimum(x,1-x),np.minimum(y,1-y))*2;m=np.clip(m*2.2,0,1)[...,None]
    return arr*m+B*(1-m)

def tex(path,size,crop=None):
    im=Image.open(path).convert('RGB')
    if crop:im=im.crop(crop)
    a=seamless(np.asarray(im).astype(float));return Image.fromarray(a.clip(0,255).astype('uint8')).resize((size,size),Image.LANCZOS)

def sheet(texture,T,ink,ink_w,inset,amp,shade=None):
    # 4x4 edge sheet; texture is a T-px seamless tile
    tx=np.asarray(texture.convert('RGB')).astype(float)
    out=np.zeros((4*T,4*T,4))
    yy,xx=np.mgrid[0:T,0:T].astype(float)+.5
    wob=lambda t,ph:inset+amp*(np.sin(2*np.pi*(2*t/T)+ph)*.6+np.sin(2*np.pi*(3*t/T)+ph*1.7)*.4)
    r=T*.32
    for cy in range(4):
        for cx in range(4):
            L=cx in(0,3);R=cx in(2,3);U=cy in(0,3);D=cy in(2,3);BIG=1e9
            dl=xx-wob(yy,.3) if L else BIG+0*xx;dr=(T-xx)-wob(yy,1.1) if R else BIG+0*xx
            du=yy-wob(xx,2.0) if U else BIG+0*xx;dd=(T-yy)-wob(xx,2.9) if D else BIG+0*xx
            eff=np.minimum.reduce([dl,dr,du,dd])
            for a,b in((dl,du),(du,dr),(dr,dd),(dd,dl)):
                c=(a<r)&(b<r);e=r-np.hypot(r-a,r-b);eff=np.where(c,np.minimum(eff,e),eff)
            al=np.clip(eff+.5,0,1)
            col=tx.copy()
            if shade is not None:
                k=np.clip(1-eff/(T*.18),0,1)[...,None];col=col*(1-shade*k)
            ik=np.clip(1-np.abs(eff-ink_w/2)/(ink_w/2),0,1)[...,None]*(eff<ink_w*1.2)[...,None]
            col=col*(1-ik)+np.array(ink)[None,None,:]*ik
            out[cy*T:(cy+1)*T,cx*T:(cx+1)*T,:3]=col;out[cy*T:(cy+1)*T,cx*T:(cx+1)*T,3]=al*255
    return Image.fromarray(out.clip(0,255).astype('uint8'),'RGBA')

if __name__=='__main__':
    src,OUT=sys.argv[1],sys.argv[2];M={};P=lambda n:os.path.join(src,n)
    # props: (file, name, height in cells, in-game scale)
    for f,n,hc,sc in[('tree1.png','tree1',1.6,.66),('tree2.png','tree2',2.4,.66),('tree3.png','tree3',1.6,.66),('bush.png','bush',.6,.72),('bush2.png','bush2',.66,.72)]:
        im,m=prop(cutout(P(f)),hc,sc,2);save(im,OUT,n);M[n]=m
    for i,(im,hc) in enumerate(zip(row(P('rocks.png'),4),(.32,.36,.26,.34))):
        im,m=prop(im,hc,.72,1);save(im,OUT,'rock%d'%(i+1));M['rock%d'%(i+1)]=m
    for i,(im,hc) in enumerate(zip(row(P('wrocks.png'),4),(.4,.42,.5,.46))):
        im,m=prop(im,hc,1,3);save(im,OUT,'wrock%d'%(i+1));M['wrock%d'%(i+1)]=m
    # sheep: four walk poses, lined up on body and feet like the goblins
    import gob
    gob.HT['sheep']=.55;gob.SC['sheep']=.75
    sh,m=gob.build(P('sheep.png'),'sheep');save(sh,OUT,'sheep');M['sheep']=m
    # ground: seamless big textures (one image covers 4x4 cells) and edge sheets (128 px a cell)
    save(tex(P('grass_tex.png'),512),OUT,'grass')
    save(tex(P('water_tex.png'),512),OUT,'water')
    T=128
    mtex=tex(P('meadow_tex.png'),T,(200,200,700,700))
    # meadows are a lighter patch of the same field, not a different colour: pull them most of the way toward the grass
    g=np.asarray(Image.open(os.path.join(OUT,'grass.png')).convert('RGB')).astype(float).mean((0,1));mt=np.asarray(mtex).astype(float)
    mtex=Image.fromarray(((mt-mt.mean((0,1)))*.8+g*1.16).clip(0,255).astype('uint8'))
    save(sheet(mtex,T,(92,112,30),5,T*.12,T*.05,.0),OUT,'meadow')
    stex=tex(P('sand_sheet.png'),T,(360,360,600,600))
    save(sheet(stex,T,(100,62,30),8,T*.06,T*.05,.08),OUT,'sand')
    gtex=tex(P('turf_sheet.png'),T,(360,360,600,600))
    save(sheet(gtex,T,(84,56,26),8,T*.2,T*.06,.0),OUT,'turf')
    print(json.dumps(M))
