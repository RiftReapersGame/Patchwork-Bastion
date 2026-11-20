# front-on painted hero castles: cut from white, drop the pale ground shadow, sharpen, add a firm dark outline so they sit with the pixel art
import sys,os,json,numpy as np
from PIL import Image,ImageFilter
from scipy import ndimage as ndi
def cutout(path,blank_top=0):
    im=np.asarray(Image.open(path).convert('RGB')).astype(float)
    if blank_top:im[:blank_top]=255
    mx=im.max(-1);mn=im.min(-1);lum=(im*[.3,.59,.11]).sum(-1);sat=(mx-mn)/np.maximum(mx,1)
    def edge_connected(mask):
        lab,_=ndi.label(mask);e=set(lab[0,:])|set(lab[-1,:])|set(lab[:,0])|set(lab[:,-1]);e.discard(0);return np.isin(lab,list(e))
    bg=edge_connected(mn>232)
    core=((sat>.22)|(lum<165))&~bg                     # real paint: coloured or dark; the hatched ground shadow is pale and grey
    core=ndi.binary_opening(core,iterations=2);core=ndi.binary_closing(core,iterations=6);solid=ndi.binary_fill_holes(core)
    solid=ndi.binary_opening(solid,iterations=3)
    lab,n=ndi.label(solid);sizes=ndi.sum(solid,lab,range(1,n+1));solid=lab==(1+int(np.argmax(sizes)))
    wl,wn=ndi.label((mn>236)&solid)
    if wn:
        ws=ndi.sum(np.ones_like(wl),wl,range(1,wn+1));solid&=~np.isin(wl,[i+1 for i,v in enumerate(ws) if v>260])
    a=ndi.gaussian_filter(np.where(solid,255.,0.),.9)
    res=Image.fromarray(np.dstack([im,a]).clip(0,255).astype('uint8'));return res.crop(res.getbbox())
def finish(im,W,K):
    H=round(im.height*W/im.width);big=im.resize((int(W*K),int(H*K)),Image.LANCZOS)
    rgb=big.convert('RGB').filter(ImageFilter.UnsharpMask(2,120,2));al=big.getchannel('A')
    core=al.point(lambda v:255 if v>128 else 0);ring=core.filter(ImageFilter.MaxFilter(7))
    out=Image.new('RGBA',big.size,(44,32,40,0));out.putalpha(ring);out.paste(rgb,(0,0),core);return out,H
def ruin(im):
    a=np.asarray(im).astype(float);l=(a[...,:3]*[.3,.59,.11]).sum(-1,keepdims=True);a[...,:3]=(l*.55+a[...,:3]*.15)*[1,.96,1.05];return Image.fromarray(a.clip(0,255).astype('uint8'))
if __name__=='__main__':
    src,OUT=sys.argv[1],sys.argv[2];M={};K=1.5;W=292
    for f in sorted(os.listdir(src)):
        if not f.startswith('castle_'):continue
        n='h'+f[:-4];im=cutout(os.path.join(src,f),208 if 'warden' in f else 0);big,H=finish(im,W,K)
        big.quantize(255,method=2,dither=Image.Dither.FLOYDSTEINBERG).save(os.path.join(OUT,n+'.png'),optimize=True);ruin(big).quantize(96,method=2).save(os.path.join(OUT,n+'_ruin.png'),optimize=True)
        M[n]={'f':1,'w':W,'h':H,'ax':W/2,'ay':H-4,'s':1,'k':K};M[n+'_ruin']=dict(M[n])
    print(json.dumps(M))
