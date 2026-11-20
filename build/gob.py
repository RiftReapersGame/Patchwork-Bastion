# painted goblins (original art supplied by the game's owner): each source holds four walk poses in a row,
# facing right. Cut them out, line up the heads and bodies, and lay them out as a 4-frame walk loop
# standing on its feet. Also the goblin camp, a single still image.
import sys,os,json
import numpy as np
from PIL import Image,ImageFilter
sys.path.insert(0,'/home/claude/pipe')
from flyers import alpha_of
from paint2 import cutout

K=2.5
# height in map cells each goblin is drawn at (its own in-game scale applied), close to the old sprites
HT={'grunt':1.0,'runner':.95,'swarm':.6,'tank':1.12,'brute':1.3,'shaman':1.02,'nest':1.15,'gold':.98,'boss':2.15}
SC={'grunt':.9,'runner':.85,'swarm':.58,'tank':1.35,'brute':1.2,'shaman':.9,'nest':1.3,'gold':1.1,'boss':2.1}

def split(a,n):
    cols=(a>40).sum(0)>0;runs=[];i=0;W=len(cols)
    while i<W:
        if not cols[i]:
            j=i
            while j<W and not cols[j]:j+=1
            if i>0 and j<W:runs.append((j-i,i,j))
            i=j
        else:i+=1
    runs=sorted(sorted(runs,reverse=True)[:n-1],key=lambda r:r[1])
    cuts=[0]+[(r[1]+r[2])//2 for r in runs]+[W]
    return [(cuts[k],cuts[k+1]) for k in range(n)]

def top_shift(ref,fr):
    # line up the head and upper body, which barely change between steps
    def part(a):
        ys,xs=np.nonzero(a>128);y0=ys.min();y1=ys.max();cut=y0+(y1-y0)*.5
        return np.where(np.arange(a.shape[0])[:,None]<=cut,a,0)
    A=part(ref)[::3,::3]/255.;B=part(fr)[::3,::3]/255.;best=(-1,0,0)
    for dy in range(-10,11):
        for dx in range(-14,15):
            s=(np.roll(np.roll(B,dy,0),dx,1)*A).sum()
            if s>best[0]:best=(s,dy,dx)
    return best[1]*3,best[2]*3

def build(path,name):
    im=np.asarray(Image.open(path).convert('RGB')).astype(float);a=alpha_of(im)
    parts=split(a,4);PAD=40;H0=im.shape[0];Wm=max(x1-x0 for x0,x1 in parts);canv=[]
    for x0,x1 in parts:
        c=np.zeros((H0+2*PAD,Wm+2*PAD,4));w=x1-x0
        c[PAD:PAD+H0,PAD:PAD+w,:3]=im[:,x0:x1];c[PAD:PAD+H0,PAD:PAD+w,3]=a[:,x0:x1];canv.append(c)
    ref=canv[1];out=[]
    for i,c in enumerate(canv):
        if i==1:out.append(c);continue
        dy,dx=top_shift(ref[...,3],c[...,3]);c=np.roll(np.roll(c,dy,0),dx,1)
        # keep every pose standing on the same ground line
        fb=np.nonzero(c[...,3].max(1)>60)[0].max();rb=np.nonzero(ref[...,3].max(1)>60)[0].max();c=np.roll(c,rb-fb,0);out.append(c)
    al=np.maximum.reduce([f[...,3] for f in out]);ys,xs=np.nonzero(al>10)
    y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    # stand on the middle of the feet in the passing pose
    feet=ref[...,3][y1-int((y1-y0)*.12):y1]>60;fx=np.nonzero(feet.any(0))[0];cx=(fx.min()+fx.max())/2-x0
    Hu=HT[name]*64/SC[name];Q=int(round(Hu*K));P=int(round(Q*(x1-x0)/(y1-y0)))
    s=Q/(y1-y0);tiles=[]
    for f in out:
        t=Image.fromarray(f[y0:y1,x0:x1].clip(0,255).astype('uint8'),'RGBA').resize((P,Q),Image.LANCZOS)
        rgb=t.convert('RGB').filter(ImageFilter.UnsharpMask(1.5,90,2)).convert('RGBA');rgb.putalpha(t.getchannel('A'));tiles.append(rgb)
    sheet=Image.new('RGBA',(P*4,Q),(0,0,0,0))
    for i,t in enumerate(tiles):sheet.paste(t,(i*P,0))
    return sheet,{'f':4,'w':P/K,'h':Q/K,'ax':cx*s/K,'ay':Q/K-1,'s':1,'k':K}

if __name__=='__main__':
    src,OUT=sys.argv[1],sys.argv[2];M={}
    for f in sorted(os.listdir(src)):
        if not f.endswith('.png'):continue
        n=f[:-4];sheet,m=build(os.path.join(src,f),n)
        sheet.save(os.path.join(OUT,'g_'+n+'.png'),optimize=True);M['g_'+n]=m
    camp=os.path.join(os.path.dirname(src.rstrip('/')),'camp.png')
    if os.path.exists(camp):
        im=cutout(camp);W=104;P=int(W*K);Q=round(P*im.height/im.width);im=im.resize((P,Q),Image.LANCZOS)
        rgb=im.convert('RGB').filter(ImageFilter.UnsharpMask(1.5,90,2)).convert('RGBA');rgb.putalpha(im.getchannel('A'))
        rgb.save(os.path.join(OUT,'g_camp.png'),optimize=True);M['g_camp']={'f':1,'w':W,'h':Q/K,'ax':W/2,'ay':Q/K-3,'s':1,'k':K}
    print(json.dumps(M))
