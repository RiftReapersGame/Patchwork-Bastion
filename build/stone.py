# painted-style fortress floor and wall, drawn to sit with the hand-painted castles: cream flagstones, warm brown ink, grey rock footing
import sys,random
from sk import Sk
from PIL import Image
INK=(96,66,48);CREAM=(222,203,162);CREAM2=(204,183,142);ROCK=(178,166,158);ROCK2=(150,138,134);MOSS=(150,160,84)
def base():
    k=Sk(256,256,11);r=random.Random(4)
    for ty in range(4):
        for tx in range(4):
            oL=tx in(0,3);oR=tx in(2,3);oU=ty in(0,3);oD=ty in(2,3);x0,y0=tx*64,ty*64
            l=x0+(4 if oL else 0);rr=x0+64-(4 if oR else 0);t=y0+(4 if oU else 0);b=y0+64-(3 if oD else 0)
            mx=x0+r.randint(26,38);my=y0+r.randint(26,38)
            for (a,c,d,e) in((l,t,mx,my),(mx,t,rr,my),(l,my,mx,b),(mx,my,rr,b)):
                col=tuple(v+r.randint(-9,7) for v in (CREAM if r.random()<.7 else CREAM2))
                k.wash([(a+.5,c+.5),(d-.5,c+.5),(d-.5,e-.5),(a+.5,e-.5)],col,255,.6)
            k.line([(mx+r.uniform(-2,2),t),(mx,my),(mx+r.uniform(-2,2),b)],1.5,amp=.7,col=INK,twice=False)
            k.line([(l,my+r.uniform(-2,2)),(mx,my),(rr,my+r.uniform(-2,2))],1.5,amp=.7,col=INK,twice=False)
            for i in range(3):                                         # chips and cracks
                px,py=x0+r.randint(10,54),y0+r.randint(10,54);k.line([(px,py),(px+r.randint(3,7),py+r.randint(-2,3))],.7,amp=.4,col=(150,120,92),twice=False)
            k.hatch([(mx+3,my+3),(rr-3,my+3),(rr-3,b-3),(mx+3,b-3)],-55,5,a=38)
            if not oL:k.line([(x0,t),(x0,b)],1.3,amp=.5,col=(120,90,66),twice=False)
            if not oU:k.line([(l,y0),(rr,y0)],1.3,amp=.5,col=(120,90,66),twice=False)
            edge=[]
            if oU:k.line([(l,t),(rr,t)],3.2,amp=.8,col=INK)
            if oD:k.line([(l,b),(rr,b)],3.2,amp=.8,col=INK)
            if oL:k.line([(l,t),(l,b)],3.2,amp=.8,col=INK)
            if oR:k.line([(rr,t),(rr,b)],3.2,amp=.8,col=INK)
    im=k.out()
    # keep each tile's paint inside its own cell on open sides (the wash blurs a little)
    return im
def wall():
    k=Sk(256,64,23);r=random.Random(9)
    for tx in range(4):
        oL=tx in(0,3);oR=tx in(2,3);x0=tx*64;l=x0+(3 if oL else 0);rr=x0+64-(3 if oR else 0)
        k.wash([(l,0),(rr,0),(rr,27),(l,27)],ROCK2,255,.4)
        xs=[l,x0+r.randint(18,26),x0+r.randint(38,46),rr]
        for i in range(3):
            a,b=xs[i],xs[i+1];top=[(a+1,1),(b-1,1+r.uniform(0,2)),(b-1-r.uniform(0,3),14),(a+1+r.uniform(0,2),13)]
            k.wash(top,tuple(v+r.randint(-8,8) for v in ROCK),255,.5);k.line(top,1,True,amp=.5,col=INK,twice=False)
        xs2=[l,x0+r.randint(28,36),rr]
        for i in range(2):
            a,b=xs2[i],xs2[i+1];bl=[(a+1+r.uniform(0,2),15),(b-1,15+r.uniform(0,1.5)),(b-1,26),(a+1,26)]
            k.wash(bl,tuple(v+r.randint(-8,6) for v in ROCK2),255,.5);k.line(bl,1,True,amp=.5,col=INK,twice=False);k.hatch(bl,-55,4,a=70)
        k.line([(l,0.8),(rr,0.8)],1.6,amp=.5,col=INK);k.line([(l,27),(rr,27)],1.6,amp=.6,col=INK)
        if oL:k.line([(l,0),(l,27)],1.8,amp=.5,col=INK)
        if oR:k.line([(rr,0),(rr,27)],1.8,amp=.5,col=INK)
        for i in range(2):
            mxp=x0+r.randint(8,52);k.wash([(mxp,24),(mxp+6,22),(mxp+11,25),(mxp+7,28),(mxp+1,28)],MOSS,230,.5)
    im=k.out();im.paste((0,0,0,0),(0,29,256,64));return im
if __name__=='__main__':
    OUT=sys.argv[1];base().save(OUT+'/base.png',optimize=True);wall().save(OUT+'/wall.png',optimize=True)
