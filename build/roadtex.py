# a painted dirt-and-cobble road texture made from the owner's painted floor art, so roads match the fortress stonework
import sys,numpy as np
from PIL import Image,ImageFilter
SRC,OUT=sys.argv[1],sys.argv[2];T=256
im=Image.open(SRC).convert('RGB');a=np.asarray(im).astype(int);nz=np.argwhere(a.min(-1)<225);y0,x0=nz.min(0);y1,x1=nz.max(0);W=x1-x0;H=y1-y0
fs=int(W*.74);t=im.crop((x0+int(W*.13),y0+int(H*.06),x0+int(W*.13)+fs,y0+int(H*.06)+fs)).resize((T,T),Image.LANCZOS)
# make it tile: mirror into a 2x2 block so every edge meets itself
m=Image.new('RGB',(T*2,T*2));m.paste(t,(0,0));m.paste(t.transpose(Image.FLIP_LEFT_RIGHT),(T,0));m.paste(t.transpose(Image.FLIP_TOP_BOTTOM),(0,T));m.paste(t.transpose(Image.ROTATE_180),(T,T))
a=np.asarray(m).astype(float);l=(a*[.3,.59,.11]).sum(-1,keepdims=True)
dirt=np.array([196,150,98]);a=(l/ l.mean())*dirt*.55+dirt*.45                 # packed earth, keeping the painted stone shapes and ink joints
out=Image.fromarray(a.clip(0,255).astype('uint8')).resize((256,256),Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.5,70,2))
out.quantize(128,method=0).save(OUT+'/roadtex.png',optimize=True)
