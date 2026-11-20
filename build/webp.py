# WebP copies of every image the game loads: painted art (manifest entries with a k resolution factor, and the
# ground textures) as high-quality lossy WebP, pixel art as lossless WebP so its hard edges stay exact
import os,json,sys
from PIL import Image
A='/home/claude/bastion/assets';M=json.load(open('/home/claude/pipe/manifest.json'))
PAINT={'grass','water','meadow','sand','turf','base','wall','roadtex','road'}
n=0;t0=t1=0
for f in os.listdir(A):
    if not f.endswith('.png'):continue
    k=f[:-4];src=os.path.join(A,f);dst=os.path.join(A,k+'.webp')
    if os.path.exists(dst) and os.path.getmtime(dst)>=os.path.getmtime(src):continue
    im=Image.open(src).convert('RGBA')
    if k in PAINT or (M.get(k) or {}).get('k'):im.save(dst,'WEBP',quality=88,method=6,alpha_quality=92)
    else:im.save(dst,'WEBP',lossless=True,method=6)
    n+=1
print('converted',n)
