# turn a sprite into a pencil-and-wash sketch: soft shapes, pale colour, graphite outline, hatching in the shadows
import sys,os,numpy as np
from PIL import Image,ImageFilter
PAPER=np.array([244,236,214],float);INK=np.array([58,52,66],float)
def sketch(im,ground=False):
    im=im.convert('RGBA');w,h=im.size;k=3
    big=im.resize((w*k,h*k),Image.BICUBIC).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(.8))
    a=np.asarray(big).astype(float);rgb=a[...,:3];al=a[...,3]/255
    lum=(rgb*[.3,.59,.11]).sum(-1)/255
    grey=np.repeat((lum*255)[...,None],3,-1)
    sat=.55 if not ground else .4
    col=grey+(rgb-grey)*sat
    col=col+(PAPER-col)*(.42 if not ground else .55)          # wash it out toward the paper
    yy,xx=np.mgrid[0:h*k,0:w*k]
    rng=np.random.default_rng(7);noise=rng.random((h*k,w*k))
    hatch=((xx+yy)%7<1.6)&(lum<.42);hatch2=((xx-yy)%7<1.4)&(lum<.24)
    col[hatch|hatch2]=col[hatch|hatch2]*.55+INK*.45
    g=Image.fromarray((lum*255).astype('uint8'))
    e=np.asarray(g.filter(ImageFilter.FIND_EDGES)).astype(float)/255
    ae=np.asarray(Image.fromarray((al*255).astype('uint8')).filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))).astype(float)/255
    line=np.clip(e*(2.2 if not ground else .9)+ae*1.6,0,1)*(.65+.35*noise)
    line=np.asarray(Image.fromarray((line*255).astype('uint8')).filter(ImageFilter.GaussianBlur(.6))).astype(float)/255
    line=np.clip(line*1.5,0,1)[...,None]
    col=col*(1-line)+INK*line
    col*= (.97+.06*noise)[...,None]                              # paper grain
    al2=np.clip(np.maximum(al,ae*.9),0,1)
    out=np.dstack([np.clip(col,0,255),al2*255]).astype('uint8')
    return Image.fromarray(out).resize((w,h),Image.LANCZOS)
if __name__=='__main__':
    d=sys.argv[1]
    for f in sorted(os.listdir(d)):
        if not f.endswith('.png'):continue
        p=os.path.join(d,f);g=f.split('.')[0] in('grass','meadow','road','sand','turf','base')
        sketch(Image.open(p),g).save(p)
