# repaint "Phoenix (reborn)" by Chasersgaming (CC0): gold wing tips and crest, orange wings, crimson body, a dark outline
import sys
from PIL import Image
src,OUT=sys.argv[1],sys.argv[2]
ph=Image.open(src).convert('RGBA')
def lerp(a,b,t):return tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
RAMP=[(0,(168,22,38)),(.3,(226,52,24)),(.55,(255,122,14)),(.8,(255,196,44)),(1,(255,242,150))]
def ramp(t):
    t=max(0,min(1,t))
    for i in range(len(RAMP)-1):
        a,b=RAMP[i],RAMP[i+1]
        if t<=b[0]:return lerp(a[1],b[1],(t-a[0])/(b[0]-a[0]))
    return RAMP[-1][1]
def isred(p):return p[3]>0 and p[0]>150 and p[1]<90 and p[2]<40
def frame(r,c,fly):
    f=ph.crop((c*32,r*32,c*32+32,r*32+32));px=f.load();o=Image.new('RGBA',(34,34));op=o.load()
    reds=[(x,y) for y in range(32) for x in range(32) if isred(px[x,y])]
    if reds:
        # body line: the densest row of the bird
        rows={};[rows.__setitem__(y,rows.get(y,0)+1) for x,y in reds];by=max(rows,key=rows.get) if fly else max(y for x,y in reds)
        xs=[x for x,y in reds];cx=(min(xs)+max(xs))/2;far=max(max(abs(y-by) for x,y in reds),6)
    for y in range(32):
        for x in range(32):
            p=px[x,y]
            if not p[3]:continue
            if isred(p):
                shade=(p[0]-178)/77  # 0 dark .. 1 light in the original
                d=abs(y-by)/far
                if fly:
                    t=.12+.95*d**.8+(.25 if x>cx+9 else 0)+(.3*(1-(x/5)) if x<5 else 0)  # head and tail tip run to gold
                else:t=.15+.8*d
                col=ramp(t*(.75+.25*shade)+.05*shade)
                op[x+1,y+1]=col+(255,)
            elif p[:3]==(255,255,0):op[x+1,y+1]=(255,236,120,255)
            elif p[0]>200 and p[1]>120 and p[2]<80:op[x+1,y+1]=(255,214,64,255)  # beak and feet
            else:op[x+1,y+1]=p
    # dark outline around the bird itself
    src2=o.copy();sp=src2.load()
    for y in range(34):
        for x in range(34):
            if sp[x,y][3]:continue
            for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                xx,yy=x+dx,y+dy
                if 0<=xx<34 and 0<=yy<34 and sp[xx,yy][3] and sp[xx,yy][0]>150 and sp[xx,yy][:3]!=(255,236,120):op[x,y]=(74,18,34,255);break
    return o
M={}
for r,(n,ay) in enumerate((('p_fly',51),('p_death',99),('p_reborn',99))):
    st=Image.new('RGBA',(34*6,34))
    for c in range(6):st.paste(frame(r,c,r==0),(c*34,0))
    st=st.resize((102*6,102),Image.NEAREST);st.save(OUT+'/'+n+'.png',optimize=True)
    M[n]={'f':6,'w':102,'h':102,'ax':51,'ay':ay,'s':1}
import json;print(json.dumps(M))
