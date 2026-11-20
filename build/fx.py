# painted effects (original art supplied by the game's owner): five frames each on white, start to finish.
# Watercolour glows are kept soft by lifting the white out as transparency. Frames keep their relative sizes
# and are laid out to the same frame count, box size and anchor the old effects used, so timing is unchanged.
import sys,os,json
import numpy as np
from PIL import Image,ImageFilter
sys.path.insert(0,'/home/claude/pipe')
def split(a,n):
    # cut near the n evenly spaced boundaries, at the emptiest column close to each
    col=(a>8).sum(0).astype(float);W=len(col);cuts=[0]
    for i in range(1,n):
        c=W*i/n;lo,hi=int(c-W*.07),int(c+W*.07);cuts.append(lo+int(np.argmin(col[lo:hi]+np.abs(np.arange(lo,hi)-c)*.02)))
    cuts.append(W);return [(cuts[k],cuts[k+1]) for k in range(n)]
K=2.5
# name: (old frame count, box w, box h, ax, ay, frame order, bottom-aligned)
SPEC={'explosion':(9,64,64,33,36,[0,1,2,2,3,3,3,4,4],0),'dust':(10,64,57,32,28,[0,1,1,2,2,3,3,3,4,4],0),
 'fire':(12,55,55,28,55,[1,2,3,3,2,1,1,2,3,3,2,1],1),'heal':(11,98,128,49,78,[0,1,1,2,2,2,3,3,4,4,4],0),
 'fexp':(9,100,78,51,39,[0,1,2,2,3,3,3,4,4],0),'mexp':(9,100,78,51,39,[0,1,2,2,3,3,3,4,4],0),
 'slash':(7,90,60,45,30,[0,1,2,2,3,3,4],0),'zap':(7,50,80,25,40,[0,1,2,2,3,3,4],0),
 'fire_s':(8,22,24,11,24,[1,1,1,1,1,1,1,1],1,'explosion')}
def unwhite(rgb):
    mn=rgb.min(-1);a=np.clip((250-mn)/28,0,1)
    col=np.where(a[...,None]>0,(rgb-255*(1-a[...,None]))/np.maximum(a[...,None],1e-3),0)
    return np.dstack([col.clip(0,255),a*255])
src,OUT=sys.argv[1],sys.argv[2];M={}
for n,sp in SPEC.items():
    F,W,H,AX,AY,order,bottom=sp[:7];p=os.path.join(src,(sp[7] if len(sp)>7 else n)+'.png')
    if not os.path.exists(p):continue
    rgb=np.asarray(Image.open(p).convert('RGB')).astype(float);rgba=unwhite(rgb);al=rgba[...,3]
    frames=[]
    for x0,x1 in split(al,5):
        f=rgba[:,x0:x1];ys,xs=np.nonzero(f[...,3]>8)
        frames.append(f[ys.min():ys.max()+1,xs.min():xs.max()+1] if len(ys) else f[:2,:2])
    used=[frames[k] for k in set(order)];cw=max(f.shape[1] for f in used);ch=max(f.shape[0] for f in used)
    s=min(W*.96/cw,H*.96/ch)*K;P,Q=int(round(W*K)),int(round(H*K))
    cells=[]
    for f in frames:
        im=Image.fromarray(f.clip(0,255).astype('uint8'),'RGBA');im=im.resize((max(1,round(im.width*s)),max(1,round(im.height*s))),Image.LANCZOS)
        c=Image.new('RGBA',(P,Q),(0,0,0,0))
        x=round(AX*K-im.width/2);y=(Q-im.height-1) if bottom else round(AY*K-im.height/2)
        c.paste(im,(x,max(0,y)),im);cells.append(c)
    sheet=Image.new('RGBA',(P*F,Q),(0,0,0,0))
    for i,k in enumerate(order):
        c=cells[k]
        if n=='fire_s':
            sy=[1,.86,1.06,.92,1.1,.88,1,.95][i];sx=[1,1.08,.94,1.05,.9,1.07,.98,1.02][i];im=c.resize((max(1,round(P*sx)),max(1,round(Q*sy))),Image.LANCZOS)
            c=Image.new('RGBA',(P,Q),(0,0,0,0));c.paste(im,((P-im.width)//2,Q-im.height),im)
        sheet.paste(c,(i*P,0))
    sheet.save(os.path.join(OUT,'fx_'+n+'.png'),optimize=True)
    M['fx_'+n]={'f':F,'w':W,'h':H,'ax':AX,'ay':AY,'s':1,'k':K}
print(json.dumps(M))
