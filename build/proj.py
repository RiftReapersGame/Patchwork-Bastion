# painted projectiles (original art supplied by the game's owner): each points right; cut out and scaled by
# its length in map cells. The game rotates them in flight. Earthshaker spikes are turned to point up.
import sys,os,json
from PIL import Image,ImageFilter
sys.path.insert(0,'/home/claude/pipe')
from paint2 import cutout
K=4
L={'arrow':.6,'bolt':.36,'longbow':.85,'spear':.9,'ballista':1.05,'dart':.42,'keg':.4,'frost':.55,'oil':.4,'boulder':.46,'hex':.42,'spikes':.78,'meteor':.95,'dynamite':.3}
src,OUT=sys.argv[1],sys.argv[2];M={}
for f in sorted(os.listdir(src)):
    n=f[:-4]
    if n not in L:continue
    im=cutout(os.path.join(src,f));im=im.crop(im.getbbox())
    if n=='spikes':im=im.rotate(90,expand=True)
    if n=='dynamite':im=im.rotate(-55,expand=True,resample=Image.BICUBIC);im=im.crop(im.getbbox())
    long=im.height if n=='spikes' else im.width
    s=L[n]*64*K/long;im=im.resize((max(1,round(im.width*s)),max(1,round(im.height*s))),Image.LANCZOS)
    rgb=im.convert('RGB').filter(ImageFilter.UnsharpMask(1.2,80,2)).convert('RGBA');rgb.putalpha(im.getchannel('A'))
    rgb.save(os.path.join(OUT,'pj_'+n+'.png'),optimize=True)
    w,h=rgb.width/K,rgb.height/K
    M['pj_'+n]={'f':1,'w':w,'h':h,'ax':w/2 if n!='spikes' else w/2,'ay':h/2 if n!='spikes' else h-1,'s':1,'k':K}
print(json.dumps(M))
