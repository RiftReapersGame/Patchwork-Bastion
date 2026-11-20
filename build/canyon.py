# Red Canyon art (original art supplied by the game's owner): desert sand, mesa-top edge sheet, a cliff band
# that hangs under the front edge of every mesa, cacti, a dry bush, red rocks, a skull, a tumbleweed and a lizard
import sys,os,json
import numpy as np
from PIL import Image,ImageFilter
from scipy import ndimage as ndi
sys.path.insert(0,'/home/claude/pipe')
from paint2 import cutout
from flyers import alpha_of
from terrain import tex,sheet,prop,sharpen,K,save
import gob
src,OUT=sys.argv[1],sys.argv[2];M={};P=lambda n:os.path.join(src,n)

# ground
save(tex(P('sand_tex.png'),512),OUT,'dsand')
T=128;mt=tex(P('mesa_tex.png'),T,(300,300,800,800))
from PIL import ImageEnhance
mt=ImageEnhance.Color(ImageEnhance.Brightness(mt).enhance(1.12)).enhance(1.12)   # lift the plateau tops so they read against the sand
save(sheet(mt,T,(62,24,16),11,T*.05,T*.045,.0),OUT,'mesa')

# cliff bands: cut the rock strip off the white, keep its lower part (the top is hidden under the mesa edge),
# make it wrap left to right, and fit it to three cells wide and 0.7 of a cell tall. Two variants, one per row.
def band(path):
    rgb=np.asarray(Image.open(path).convert('RGB')).astype(float);a=alpha_of(rgb);ys,xs=np.nonzero(a>128)
    y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min()+6,xs.max()-5
    im=Image.fromarray(np.dstack([rgb,a]).clip(0,255).astype('uint8'),'RGBA').crop((x0,y0+int((y1-y0)*.18),x1,y1))
    W,H=3*T,int(T*1.0);im=im.resize((W+60,H),Image.LANCZOS);arr=np.asarray(im).astype(float)
    o=60;w=np.linspace(0,1,o)[None,:,None];arr[:,:o]=arr[:,:o]*w+arr[:,W:W+o]*(1-w)   # blend the ends so it wraps
    return Image.fromarray(arr[:,:W].clip(0,255).astype('uint8'),'RGBA')
b1,b2=band(P('cliff2.png')),band(P('cliff1.png'))
cl=Image.new('RGBA',(b1.width,b1.height*2),(0,0,0,0));cl.paste(b1,(0,0));cl.paste(b2,(0,b1.height));save(cl,OUT,'cliff')

# scenery: (file, name, height in cells, in-game scale)
for f,n,hc,sc in[('saguaro.png','cac_sag',1.35,.72),('barrel.png','cac_bar',.5,.72),('pear.png','cac_pear',.62,.72),('drybush.png','dbush',.62,.72),('tumble.png','tumble',.5,1)]:
    im,m=prop(cutout(P(f)),hc,sc,2);save(im,OUT,n);M[n]=m
# the four red rocks sit in a 2 x 2 grid: take the four biggest pieces, left to right, top to bottom
rgb=np.asarray(Image.open(P('rocks.png')).convert('RGB')).astype(float);a=alpha_of(rgb);lab,n=ndi.label(a>128)
sz=ndi.sum(a>128,lab,range(1,n+1));big=sorted(range(n),key=lambda i:-sz[i])[:4]
boxes=sorted([ndi.find_objects((lab==i+1).astype(int))[0] for i in big],key=lambda s:(s[0].start//300,s[1].start))
for i,(sy,sx) in enumerate(boxes):
    m_=ndi.binary_dilation(lab[sy,sx]>0,iterations=3)
    piece=Image.fromarray(np.dstack([rgb[sy,sx],np.where(m_,a[sy,sx],0)]).clip(0,255).astype('uint8'),'RGBA')
    im,m=prop(piece,(.42,.26,.3,.36)[i],.8,1);save(im,OUT,'rrock%d'%(i+1));M['rrock%d'%(i+1)]=m
im,m=prop(cutout(P('skull.png')),.36,.8,1);save(im,OUT,'rskull');M['rskull']=m
# the lizard walks with four poses, lined up like the goblins
gob.HT['lizard']=.24;gob.SC['lizard']=.75
sh,m=gob.build(P('lizard.png'),'lizard');save(sh,OUT,'lizard');M['lizard']=m
print(json.dumps(M))
