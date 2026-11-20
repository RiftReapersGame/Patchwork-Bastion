# painted foundation pieces supplied by the game's owner: floor block, wall block, three plot medallions
import sys,os,json,random,numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage as ndi
SRC,OUT=sys.argv[1],sys.argv[2];T=128;INK=(70,50,44,255)
FR=Image.open(SRC+'/../front/castle_marshal.png').convert('RGB')      # the front-on castle sets the stone colours
def tint(im,target):
    a=np.asarray(im.convert('RGB')).astype(float);m=a.reshape(-1,3).mean(0);a=a*(np.array(target)/m);return Image.fromarray(a.clip(0,255).astype('uint8'))
fl=tint(Image.open(SRC+'/floor.png'),(238,206,158)).resize((T,T),Image.LANCZOS)
base=Image.new('RGBA',(T*4,T*4));r=random.Random(3)
def edge(d,p0,p1,w=5):
    n=9;pts=[(p0[0]+(p1[0]-p0[0])*i/n+r.uniform(-.8,.8),p0[1]+(p1[1]-p0[1])*i/n+r.uniform(-.8,.8)) for i in range(n+1)];d.line(pts,fill=INK,width=w,joint='curve')
for ty in range(4):
    for tx in range(4):
        t=fl.copy().convert('RGBA');d=ImageDraw.Draw(t)
        if tx in(0,3):edge(d,(2,0),(2,T))
        if tx in(2,3):edge(d,(T-3,0),(T-3,T))
        if ty in(0,3):edge(d,(0,2),(T,2))
        if ty in(2,3):edge(d,(0,T-3),(T,T-3))
        base.paste(t,(tx*T,ty*T))
base.convert('RGB').quantize(200,method=0).save(OUT+'/base.png',optimize=True)
wall=Image.new('RGBA',(T*4,T*28//64))
for i,x0 in enumerate((49,451,853,451)):wall.paste(FR.crop((x0,1099,x0+402,1181)).resize((T,T*28//64),Image.LANCZOS),(i*T,0))
wall.convert('RGB').quantize(200,method=0).save(OUT+'/wall.png',optimize=True)
M={}
for n in('power','reach','haste'):
    a=np.asarray(Image.open(SRC+'/sp_%s.png'%n).convert('RGB')).astype(float);mn=a.min(-1)
    lab,_=ndi.label(mn>236);e=set(lab[0,:])|set(lab[-1,:])|set(lab[:,0])|set(lab[:,-1]);e.discard(0);bg=np.isin(lab,list(e))
    al=ndi.gaussian_filter(np.where(bg,0.,255.),1.2);im=Image.fromarray(np.dstack([a,al]).astype('uint8'));im=im.crop(im.getbbox()).resize((176,176),Image.LANCZOS)
    im.quantize(200,method=2).save(OUT+'/sp_%s.png'%n,optimize=True);M['sp_'+n]={'f':1,'w':88,'h':88,'ax':44,'ay':44,'s':1,'k':2}
print(json.dumps(M))
