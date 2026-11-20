# painted towers: cut from white, sharpen, outline; scaled so the stone plinth each one stands on is one plot wide
import sys,os,json
from PIL import Image
sys.path.insert(0,'/home/claude/pipe')
from paint2 import cutout,finish
src,OUT=sys.argv[1],sys.argv[2];M={};K=2;W=70
for f in sorted(os.listdir(src)):
    if not f.endswith('.png'):continue
    n='pt_'+f[:-4];big,H=finish(cutout(os.path.join(src,f)),W,K)
    big.quantize(255,method=2,dither=Image.Dither.FLOYDSTEINBERG).save(os.path.join(OUT,n+'.png'),optimize=True)
    M[n]={'f':1,'w':W,'h':H,'ax':W/2,'ay':H-6,'s':1,'k':K}
print(json.dumps(M))
