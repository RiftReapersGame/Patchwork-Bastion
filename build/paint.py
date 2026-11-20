# cut painted pieces (white background) out for the game: remove the background, turn the pale ground shadow into a real shadow, trim, scale
import sys,os,json,numpy as np
from PIL import Image
from scipy import ndimage as ndi
def cutout(path):
    im=np.asarray(Image.open(path).convert('RGB')).astype(float);h,w,_=im.shape
    mx=im.max(-1);mn=im.min(-1);lum=(im*[.3,.59,.11]).sum(-1);sat=(mx-mn)/np.maximum(mx,1)
    near=(mn>232)                                         # paper white
    lab,n=ndi.label(near);edge=set(lab[0,:])|set(lab[-1,:])|set(lab[:,0])|set(lab[:,-1]);edge.discard(0)
    bg=np.isin(lab,list(edge))
    # pale grey pencil shadow that touches the background
    pale=(lum>150)&(sat<.11)&~bg
    grow=ndi.binary_dilation(bg,iterations=3)
    lab2,n2=ndi.label(pale|bg);keep=set(np.unique(lab2[bg]));keep.discard(0)
    sh=np.isin(lab2,list(keep))&pale
    sh=ndi.binary_opening(sh,iterations=1)|(sh&grow)
    alpha=np.where(bg,0,255).astype(float)
    alpha=ndi.gaussian_filter(alpha,.8);alpha[bg]=np.minimum(alpha[bg],0)
    out=im.copy()
    a_sh=np.clip((255-lum)*1.6,0,150);out[sh]=[40,36,60];alpha[sh]=a_sh[sh]
    # pull white fringe off the edge pixels
    rim=ndi.binary_dilation(bg,iterations=2)&~bg&~sh;alpha[rim]*=np.clip((255-mn[rim])/40,0,1)
    lab3,n3=ndi.label(((mn>198)&(sat<.1))|bg);k3=set(np.unique(lab3[bg]));k3.discard(0);haze=np.isin(lab3,list(k3))&~bg&~sh;alpha[haze]*=np.clip((232-mn[haze])/34,0,1)
    rgba=np.dstack([out,alpha]).clip(0,255).astype('uint8');res=Image.fromarray(rgba);return res.crop(res.getbbox())
def ruin(im):
    a=np.asarray(im).astype(float);l=(a[...,:3]*[.3,.59,.11]).sum(-1,keepdims=True);a[...,:3]=(l*.55+a[...,:3]*.15)*[1,.96,1.05];return Image.fromarray(a.clip(0,255).astype('uint8'))
if __name__=='__main__':
    src,OUT=sys.argv[1],sys.argv[2];M={};K=1.5
    for f in sorted(os.listdir(src)):
        if not f.startswith('castle_'):continue
        n='h'+f[:-4];fp=os.path.join(src,'front',f);front=os.path.exists(fp)
        if front:                                   # front-on version: keep the building, drop its own strip of floor and wall
            tmp=Image.open(fp).convert('RGB');tmp=tmp.crop((0,0,tmp.width,1046));tmp.save('/tmp/_front.png');im=cutout('/tmp/_front.png');W=262
        else:im=cutout(os.path.join(src,f));W=300
        H=round(im.height*W/im.width)
        big=im.resize((int(W*K),int(H*K)),Image.LANCZOS);big.quantize(255,method=2,dither=Image.Dither.FLOYDSTEINBERG).save(os.path.join(OUT,n+'.png'),optimize=True);ruin(big).quantize(96,method=2).save(os.path.join(OUT,n+'_ruin.png'),optimize=True)
        M[n]={'f':1,'w':W,'h':H,'ax':W/2,'ay':(H+11 if front else round(H*.95)),'s':1,'k':K};M[n+'_ruin']=dict(M[n])
    print(json.dumps(M))
