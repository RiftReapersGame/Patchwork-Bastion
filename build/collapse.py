# castle collapse (original art supplied by the game's owner): three stages per hero castle, damaged,
# half crumbled and a ruin. All three are scaled by the same factor, taken from the first stage, so they
# stand on the same spot as the castle and line up with each other. The ruin replaces the old made-up one.
import sys,os,json
import numpy as np
from PIL import Image
sys.path.insert(0,'/home/claude/pipe')
from flyers import alpha_of
from paint2 import finish
src,OUT=sys.argv[1],sys.argv[2];M={};K=1.5;W=292
def split3(a):
    col=(a>40).sum(0);Wd=len(col);cuts=[0]
    for i in (1,2):
        c=Wd*i/3;lo,hi=int(c-Wd*.1),int(c+Wd*.1);cuts.append(lo+int(np.argmin(col[lo:hi])))
    cuts.append(Wd);return [(cuts[k],cuts[k+1]) for k in range(3)]
for hero in ('ranger','marshal','warden','archmage'):
    p=os.path.join(src,hero+'.png')
    if not os.path.exists(p):continue
    rgb=np.asarray(Image.open(p).convert('RGB')).astype(float);a=alpha_of(rgb)
    fr=[]
    for x0,x1 in split3(a):
        sub=a[:,x0:x1].copy()
        from scipy import ndimage as ndi
        lab,n=ndi.label(sub>40);sz=ndi.sum(sub>40,lab,range(1,n+1));keep=np.isin(lab,[i+1 for i,v in enumerate(sz) if v>=max(300,sz.max()*.004)])
        sub=np.where(ndi.binary_dilation(keep,iterations=2),sub,0)   # drop stray specks and the neighbour's edge
        im=Image.fromarray(np.dstack([rgb[:,x0:x1],sub]).clip(0,255).astype('uint8'),'RGBA');fr.append(im.crop(Image.fromarray((sub>40).astype('uint8')*255).getbbox()))
    s=W/fr[0].width   # castle width on the map, from the undamaged first stage
    for i,im in enumerate(fr):
        w=im.width*s;big,H=finish(im,w,K)
        n='hcastle_'+hero+('_c1','_c2','_ruin')[i]
        big.quantize(255,method=2,dither=Image.Dither.FLOYDSTEINBERG).save(os.path.join(OUT,n+'.png'),optimize=True)
        M[n]={'f':1,'w':round(w,2),'h':H,'ax':w/2,'ay':H-4,'s':1,'k':K}
print(json.dumps(M))
