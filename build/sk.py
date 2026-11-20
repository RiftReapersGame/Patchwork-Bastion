# original hand-sketched art, drawn from scratch: wobbly ink lines, loose colour wash, pencil hatching
import math,random
from PIL import Image,ImageDraw,ImageFilter
S=4;INK=(52,46,60);PAPER=(244,236,214)
class Sk:
    def __init__(s,w=256,h=256,seed=1):
        s.w,s.h=w,h;s.im=Image.new('RGBA',(w*S,h*S),(0,0,0,0));s.r=random.Random(seed)
    def wob(s,pts,amp=1.2,closed=False,step=7):
        if closed:pts=list(pts)+[pts[0]]
        out=[]
        for (x0,y0),(x1,y1) in zip(pts,pts[1:]):
            n=max(1,int(math.hypot(x1-x0,y1-y0)/step))
            for i in range(n):
                t=i/n;out.append(((x0+(x1-x0)*t+s.r.uniform(-amp,amp))*S,(y0+(y1-y0)*t+s.r.uniform(-amp,amp))*S))
        out.append((pts[-1][0]*S,pts[-1][1]*S));return out
    def wash(s,pts,col,a=215,amp=2.2):
        L=Image.new('RGBA',s.im.size,(0,0,0,0));d=ImageDraw.Draw(L)
        d.polygon(s.wob([(x+s.r.uniform(-1.5,1.5),y+s.r.uniform(-1.5,1.5)) for x,y in pts],amp,True),fill=col+(a,))
        s.im=Image.alpha_composite(s.im,L.filter(ImageFilter.GaussianBlur(S*.6)))
    def line(s,pts,w=2.2,closed=False,amp=1.1,col=INK,twice=True):
        d=ImageDraw.Draw(s.im)
        for k in range(2 if twice else 1):
            d.line(s.wob(pts,amp if k==0 else amp*1.5,closed),fill=col+(235 if k==0 else 120,),width=int((w if k==0 else w*.55)*S),joint='curve')
    def shape(s,pts,col,w=2.2,a=215):s.wash(pts,col,a);s.line(pts,w,True)
    def hatch(s,pts,ang=-50,gap=5,w=1,a=150):
        M=Image.new('L',s.im.size,0);ImageDraw.Draw(M).polygon([(x*S,y*S) for x,y in pts],fill=255)
        L=Image.new('RGBA',s.im.size,(0,0,0,0));d=ImageDraw.Draw(L);c,sn=math.cos(math.radians(ang)),math.sin(math.radians(ang))
        for i in range(int(900/gap)):
            o=-450+i*gap
            p0=(160+o*-sn-400*c,128+o*c-400*sn);p1=(160+o*-sn+400*c,128+o*c+400*sn)
            d.line(s.wob([p0,p1],.8,step=14),fill=INK+(a,),width=int(w*S))
        L.putalpha(Image.composite(L.getchannel('A'),Image.new('L',s.im.size,0),M));s.im=Image.alpha_composite(s.im,L)
    def ell(s,cx,cy,rx,ry,n=22,a0=0,a1=360):return [(cx+rx*math.cos(math.radians(a0+(a1-a0)*i/n)),cy+ry*math.sin(math.radians(a0+(a1-a0)*i/n))) for i in range(n+(0 if a1-a0>=360 else 1))]
    def out(s):return s.im.resize((s.w,s.h),Image.LANCZOS)
def ground(k,cx,y,rx):
    for i in range(3):k.line(k.ell(cx,y+i*1.5,rx-i*6,7,16,10,170),1.2,amp=1.6,twice=False)
def tower(seed=3):
    k=Sk(seed=seed);STONE=(206,200,190);ROOF=(92,138,196);WOOD=(170,124,84)
    ground(k,128,226,62)
    body=[(92,104),(164,104),(172,222),(84,222)];k.shape(body,STONE)
    k.hatch([(140,104),(164,104),(172,222),(146,222)],-55,5)
    for x,y in[(100,130),(124,150),(104,176),(132,196),(112,206),(128,120)]:k.line([(x,y),(x+14,y),(x+14,y+7)],1.1,twice=False,amp=.8)
    k.shape([(74,84),(182,84),(178,108),(78,108)],WOOD)                       # timber gallery
    for x in range(86,178,14):k.line([(x,86),(x,107)],1.1,twice=False)
    k.shape([(70,84),(128,30),(186,84)],ROOF);k.hatch([(128,30),(186,84),(140,84)],60,6)
    for i in range(1,4):k.line([(128-i*15,84-i*13.5+13.5*0),(128+i*15,84-i*13.5+13.5*0)][:0] or [(86+i*8,84-i*10),(170-i*8,84-i*10)],1,twice=False,amp=1.4)
    k.line([(128,30),(128,8)],2);k.shape([(128,9),(156,15),(128,23)],(214,74,66),1.8)
    door=[(114,222),(114,196)]+k.ell(128,196,14,14,8,180,360)+[(142,222)];k.shape(door,(96,70,58));k.line([(128,186),(128,222)],1,twice=False)
    k.shape([(124,134),(132,134),(132,154),(124,154)],(60,54,70),1.5)
    return k.out()
def goblin(seed=5):
    k=Sk(seed=seed);G=(128,176,96);TUN=(150,96,70);ground(k,128,226,44)
    k.shape([(108,214),(106,228),(124,228),(124,214)],(96,70,58),1.8);k.shape([(134,214),(134,228),(152,228),(150,214)],(96,70,58),1.8)
    k.shape([(100,150),(158,150),(164,216),(94,216)],TUN);k.hatch([(136,150),(158,150),(164,216),(140,216)],-55,5)
    k.line([(96,186),(162,186)],2.4);k.shape([(123,181),(135,181),(135,192),(123,192)],(226,190,90),1.6)
    k.shape([(160,160),(186,150),(192,162),(166,174)],G,1.9)                  # arm
    k.shape([(184,160),(194,96),(214,90),(222,104),(200,166)],(170,124,84));  # club
    for p in[(204,104),(212,118),(200,130)]:k.line(k.ell(p[0],p[1],3,3,6),1,twice=False)
    k.shape([(98,160),(74,172),(80,184),(100,176)],G,1.9)
    k.shape([(84,96),(40,74),(72,118)],G);k.shape([(172,96),(216,74),(184,118)],G)   # ears
    k.line([(60,88),(76,104)],1,twice=False);k.line([(196,88),(180,104)],1,twice=False)
    k.shape(k.ell(128,108,48,44,20),G);k.hatch(k.ell(150,116,24,34,12),-55,5,a=110)
    for cx in(110,146):k.shape(k.ell(cx,100,10,11,10),(250,244,220),1.6);k.shape(k.ell(cx+2,102,4,5,8),INK,1,255)
    k.line([(96,84),(120,92)],2.6);k.line([(160,84),(136,92)],2.6)
    k.line([(104,128)]+k.ell(128,124,24,14,8,160,20)[::-1][0:0]+[(112,138),(128,141),(144,138),(152,128)],2.2)
    for x in(114,126,138):k.shape([(x,136),(x+8,136),(x+4,146)],(250,244,220),1.3)
    k.line([(124,112),(128,118),(133,112)],1.4,twice=False)
    return k.out()
def castle(seed=9):
    k=Sk(320,256,seed);STONE=(206,200,190);ROOF=(92,138,196)
    for i in range(3):k.line(k.ell(160,228+i*1.5,140-i*8,8,20,10,170),1.2,amp=1.6,twice=False)
    def merlons(x0,x1,y,n):
        w=(x1-x0)/(2*n-1)
        for i in range(n):k.shape([(x0+i*2*w,y-12),(x0+i*2*w+w,y-12),(x0+i*2*w+w,y+2),(x0+i*2*w,y+2)],STONE,1.8)
    k.shape([(60,130),(260,130),(264,224),(56,224)],STONE);merlons(64,256,130,7)
    for x,y in[(84,150),(112,180),(206,156),(228,190),(90,200),(196,204)]:k.line([(x,y),(x+16,y),(x+16,y+8)],1.1,twice=False,amp=.8)
    for x0 in(22,238):
        k.shape([(x0+4,96),(x0+56,96),(x0+60,224),(x0,224)],STONE);k.hatch([(x0+38,96),(x0+56,96),(x0+60,224),(x0+40,224)],-55,5)
        merlons(x0,x0+60,96,3);k.shape([(x0+25,130),(x0+35,130),(x0+35,154),(x0+25,154)],(60,54,70),1.5)
    k.shape([(120,84),(200,84),(204,224),(116,224)],STONE);k.hatch([(176,84),(200,84),(204,224),(180,224)],-55,5)
    k.shape([(110,84),(160,34),(210,84)],ROOF);k.hatch([(160,34),(210,84),(172,84)],60,6)
    k.line([(160,34),(160,10)],2);k.shape([(160,11),(192,18),(160,26)],(214,74,66),1.8)
    gate=[(138,224),(138,176)]+k.ell(160,176,22,22,10,180,360)+[(182,224)];k.shape(gate,(96,70,58))
    for x in(149,160,171):k.line([(x,160),(x,224)],1.1,twice=False)
    for y in(186,204):k.line([(139,y),(181,y)],1.1,twice=False)
    k.shape([(152,108),(168,108),(168,132),(152,132)],(60,54,70),1.5)
    return k.out()
if __name__=='__main__':
    sheet=Image.new('RGBA',(900,300),PAPER+(255,))
    for i,(im,x) in enumerate(((castle(),10),(tower(),340),(goblin(),620))):sheet.alpha_composite(im,(x,24))
    sheet.save('/home/claude/t/sketch_sample.png')
