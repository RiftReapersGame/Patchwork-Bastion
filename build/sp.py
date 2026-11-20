# painted special-plot medallions (original art supplied by the game's owner): cut from white, scaled to sit inside one plot
import sys,os,json
from PIL import Image,ImageFilter
sys.path.insert(0,'/home/claude/pipe')
from paint2 import cutout
src,OUT=sys.argv[1],sys.argv[2];M={};K=2.5;W=70
for k in('power','reach','haste'):
    im=cutout(os.path.join(src,'sp_'+k+'.png'));P=int(W*K)
    im=im.resize((P,round(P*im.height/im.width)),Image.LANCZOS)
    rgb=im.convert('RGB').filter(ImageFilter.UnsharpMask(1.5,80,2)).convert('RGBA');rgb.putalpha(im.getchannel('A'))
    rgb.save(os.path.join(OUT,'sp_'+k+'.png'),optimize=True)
    M['sp_'+k]={'f':1,'w':W,'h':rgb.height/K,'ax':W/2,'ay':rgb.height/K/2,'s':1,'k':K}
print(json.dumps(M))
