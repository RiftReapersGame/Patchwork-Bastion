import sys,json,colorsys,os
from PIL import Image
SRC=sys.argv[1];OUT=sys.argv[2];M={}
def load(p):return Image.open(os.path.join(SRC,p)).convert('RGBA')
def anim(name,path,frames,center=False,scale=1,tint=None):
    im=load(path);fw=im.width//frames;fh=im.height
    fr=[im.crop((i*fw,0,(i+1)*fw,fh)) for i in range(frames)]
    l,t,r,b=fw,fh,0,0
    for f in fr:
        bb=f.split()[3].point(lambda a:255 if a>10 else 0).getbbox()
        if bb:l=min(l,bb[0]);t=min(t,bb[1]);r=max(r,bb[2]);b=max(b,bb[3])
    w,h=r-l,b-t;out=Image.new('RGBA',(w*frames,h))
    for i,f in enumerate(fr):out.paste(f.crop((l,t,r,b)),(i*w,0))
    if tint:out=recolor(out,tint)
    ax,ay=(fw/2-l,(fh/2-t) if center else h)
    if scale!=1:
        out=out.resize((max(1,round(w*scale))*frames,max(1,round(h*scale))),Image.LANCZOS);w,h=out.width//frames,out.height;ax*=scale;ay*=scale
    out.save(os.path.join(OUT,name+'.png'),optimize=True)
    M[name]={'f':frames,'w':w,'h':h,'ax':round(ax,1),'ay':round(ay,1),'s':scale}
def recolor(im,fn):
    px=im.load()
    for y in range(im.height):
        for x in range(im.width):
            r,g,b,a=px[x,y]
            if a:px[x,y]=fn(r,g,b)+(a,)
    return im
def lerp(a,b,t):t=max(0,min(1,t));return tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
def dirt(r,g,b):
    h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
    if v<.3:return (66,46,44)
    if s<.32 and v>.75:return (104,158,88)
    if .36<h<.62:return lerp((104,76,60),(150,112,78),(v-.3)/.4)
    return lerp((168,126,84),(228,192,134),(v-.5)/.28)
def stone(r,g,b):
    h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
    if v<.3:return (r,g,b)
    if .36<h<.62:return (r,g,b)
    return lerp((136,142,140),(212,212,196),(v-.5)/.28)
def frost(r,g,b):
    h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
    if v<.25:return (r,g,b)
    c=colorsys.hsv_to_rgb(.54,min(1,s*.9),min(1,v*1.05));return tuple(round(k*255) for k in c)
def tile(name,im):im.save(os.path.join(OUT,name+'.png'),optimize=True)
t1=load('map/images/tiles/Tilemap_color1.png');t3=load('map/images/tiles/Tilemap_color3.png');t2=load('map/images/tiles/Tilemap_color2.png')
tile('grass',t3.crop((64,64,128,128)))
def rim(r,g,b):
    h,s_,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
    return (98,160,84) if (s_<.32 and v>.75) else (r,g,b)
tile('meadow',recolor(t2.crop((0,0,256,256)),rim))
tile('road',recolor(t1.crop((0,0,256,256)),dirt))
tile('base',recolor(t1.crop((320,0,576,256)),stone))
tile('wall',t1.crop((320,256,576,320)))
U='images/units/'
GOB=sys.argv[3]
def gob(name,path,cell,row,frames):
    im=Image.open(os.path.join(GOB,path)).convert('RGBA').crop((0,row*cell,frames*cell,(row+1)*cell))
    tmp=os.path.join(OUT,'_tmp.png');im.save(tmp);anim(name,tmp,frames);os.remove(tmp)
_load=load
def load(p):return Image.open(p).convert('RGBA') if os.path.isabs(p) else _load(p)
gob('e_grunt','Troops/Torch/Red/Torch_Red.png',192,1,6);gob('e_runner','Troops/TNT/Red/TNT_Red.png',192,1,6)
gob('e_swarm','Troops/Torch/Yellow/Torch_Yellow.png',192,1,6);gob('e_tank','Troops/Barrel/Red/Barrel_Red.png',128,3,6)
gob('e_boss','Troops/Torch/Purple/Torch_Purple.png',192,1,6)
def gfile(name,path,frames,center=False,crop=None):
    im=Image.open(os.path.join(GOB,path)).convert('RGBA')
    if crop:im=im.crop(crop)
    tmp=os.path.join(OUT,'_tmp.png');im.save(tmp);anim(name,tmp,frames,center);os.remove(tmp)
gfile('b_perch','Buildings/Wood_Tower/Wood_Tower_Purple.png',4);gfile('b_gobtower','Buildings/Wood_Tower/Wood_Tower_Blue.png',4);gfile('b_catapult','Buildings/Wood_Tower/Wood_Tower_InConstruction.png',1,crop=(0,0,256,192));gfile('dynamite','Troops/TNT/Dynamite/Dynamite.png',6,True)
gob('e_brute','Troops/Torch/Blue/Torch_Blue.png',192,1,6);gob('e_nest','Troops/Barrel/Blue/Barrel_Blue.png',128,3,6);gob('e_gold','Troops/Barrel/Yellow/Barrel_Yellow.png',128,3,6)
tmp=os.path.join(OUT,'_c.png');Image.open(os.path.join(GOB,'Buildings/Wood_House/Goblin_House.png')).save(tmp);anim('camp',tmp,1);os.remove(tmp)
anim('u_archer_idle',U+'Blue/Archer_Idle.png',6);anim('u_archer_atk',U+'Blue/Archer_Attack.png',8)
anim('u_priest_idle',U+'Blue/Priest_Idle.png',6);anim('u_priest_cast',U+'Blue/Priest_Heal.png',11)
anim('u_warrior_idle',U+'Yellow/Warrior_Idle.png',8);anim('u_warrior_atk',U+'Yellow/Warrior_Attack1.png',4)
anim('u_lancer_idle',U+'Black/Lancer_Idle.png',12);anim('u_lancer_atk',U+'Black/Lancer_Attack.png',9)
anim('u_rwarrior_idle',U+'Red/Warrior_Idle.png',8);anim('u_rwarrior_atk',U+'Red/Warrior_Attack1.png',4)
anim('u_hex_idle',U+'Purple/Priest_Idle.png',6);anim('u_hex_cast',U+'Purple/Priest_Heal.png',11)
B='images/buildings/'
for n,p in (('castle','Blue/Castle'),('b_tower','Blue/Tower'),('b_barracks','Blue/Barracks'),('b_archery','Blue/Archery'),('b_monastery','Blue/Monastery'),('b_house','Red/House1'),('b_tower_k','Black/Tower'),('b_barracks_k','Black/Barracks'),('b_tower_y','Yellow/Tower'),('b_tower_p','Purple/Tower'),('b_treasury','Yellow/House3'),('b_chapel','Blue/House2'),('b_hall','Red/Barracks'),('b_bell','Yellow/Monastery'),('b_echo','Purple/Monastery'),('b_tower_r','Red/Tower'),('b_drums','Purple/House1'),('b_bounty','Yellow/House2'),('b_roost','Black/Monastery'),('b_pyre','Red/Monastery'),('b_stable','Yellow/Archery'),('b_batcave','Black/House3'),('b_drake','Purple/House2'),('b_shrine','Blue/House1'),('castle_ruin','Black/Castle')):
    anim(n,B+p+'.png',1)
F='images/effects/'
anim('fx_explosion',F+'explosion1.png',9,True);anim('fx_fire',F+'fire3.png',12);anim('fx_fire_s',F+'fire1.png',8);anim('fx_dust',F+'dust2.png',10,True)
anim('fx_heal',F+'heal.png',11,True);anim('b_tower_ice',B+'Blue/Tower.png',1,tint=frost);anim('fx_magic',U+'magic.png',3,True);anim('fx_mexp',U+'magic explosion.png',9,True)
anim('fx_frost',U+'magic.png',3,True,tint=frost);anim('fx_fexp',U+'magic explosion.png',9,True,tint=frost)
anim('arrow',U+'arrow.png',1,True)
D='map/images/decorations/'
anim('tree1',D+'Tree1.png',8);anim('tree2',D+'Tree2.png',8);anim('tree3',D+'Tree3.png',8);anim('bush',D+'Bushe1.png',8);anim('bush2',D+'Bushe3.png',8)
for i in (1,2,3,4):anim('rock%d'%i,D+'Rock%d.png'%i,1)
anim('sheep',D+'Sheep_Idle.png',6)
sc=load('images/ui/banner.png');sc=sc.resize((sc.width//2,sc.height//2),Image.LANCZOS);sc.save(os.path.join(OUT,'scroll.png'),optimize=True)
rb=load('images/ui/large ribbons.png')
for i,c in enumerate(('blue','red','yellow','purple','gray')):
    row=rb.crop((0,i*128,448,(i+1)*128));o=Image.new('RGBA',(320,128))
    o.paste(row.crop((0,0,128,128)),(0,0));o.paste(row.crop((192,0,256,128)),(128,0));o.paste(row.crop((320,0,448,128)),(192,0))
    bb=o.getbbox();o=o.crop((0,bb[1],320,bb[3]));o.save(os.path.join(OUT,'ribbon_%s.png'%c),optimize=True);M['ribbon_'+c]={'w':o.width,'h':o.height}
# new towers: recolours of the blue buildings and units
def swap(h0,sm=1,vm=1,lo=.5,hi=.72):
    def fn(r,g,b):
        h,s_,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
        if s_<.2 or v<.18 or not(lo<=h<=hi):return (r,g,b)
        c=colorsys.hsv_to_rgb(h0,min(1,s_*sm),min(1,v*vm));return tuple(round(k*255) for k in c)
    return fn
anim('b_repeater',B+'Red/Archery.png',1);anim('b_ballista',B+'Black/Archery.png',1);anim('b_glaive',B+'Yellow/Barracks.png',1);anim('b_star',B+'Purple/Barracks.png',1)
anim('b_tower_g',B+'Blue/Tower.png',1,tint=swap(.3,1,.95));anim('b_tower_e',B+'Blue/Tower.png',1,tint=swap(.075,.8,.8))
anim('b_gale',B+'Blue/Monastery.png',1,tint=swap(.46,.3,1.35));anim('b_obelisk',B+'Blue/Monastery.png',1,tint=swap(.9,.95,1.1))
anim('u_hunter_idle',U+'Blue/Archer_Idle.png',6,tint=swap(.3,1,.9));anim('u_hunter_atk',U+'Blue/Archer_Attack.png',8,tint=swap(.3,1,.9))
anim('u_shaker_idle',U+'Black/Warrior_Idle.png',8);anim('u_shaker_atk',U+'Black/Warrior_Attack1.png',4)
hp=load(U+'harpoon.png').rotate(-45,expand=True,resample=Image.BICUBIC);hp=hp.crop(hp.getbbox());hp.save(os.path.join(OUT,'harpoon.png'),optimize=True)
M['harpoon']={'f':1,'w':hp.width,'h':hp.height,'ax':hp.width/2,'ay':hp.height/2,'s':1}
# heroes: a castle per hero, the warden's lancer and sky wyrm
for n,c in (('castle_r','Red'),('castle_y','Yellow'),('castle_p','Purple')):anim(n,B+c+'/Castle.png',1)
anim('u_ylancer_idle',U+'Yellow/Lancer_Idle.png',12);anim('u_ylancer_atk',U+'Yellow/Lancer_Attack.png',9)
# the phoenix: "Phoenix (reborn)" by Chasersgaming (CC0), repainted by phoenix.py
PH='/home/claude/dl/phoenix/unboxed.png'
if os.path.exists(PH):
    import subprocess
    M.update(json.loads(subprocess.check_output([sys.executable,'-I','/home/claude/pipe/phoenix.py',PH,OUT]).decode()))
# hero figures: palette swaps so each hero is a one-off (gold-helmed ranger, steel-clad marshal, white-haired archmage)
def pal(d):
    return lambda r,g,b:d.get((r,g,b),(r,g,b))
RANGER=pal({(156,190,170):(246,198,74),(104,140,138):(196,134,40),(212,237,194):(255,238,160),(70,151,172):(244,244,236)})
MARSHAL=pal({(239,225,171):(104,118,150),(232,206,145):(74,86,116),(148,116,103):(52,60,84)})
ARCH=pal({(151,123,107):(238,238,244),(94,84,85):(170,176,198),(171,110,156):(126,92,224),(92,84,126):(60,48,138)})
anim('u_hranger_idle',U+'Blue/Archer_Idle.png',6,tint=RANGER);anim('u_hranger_atk',U+'Blue/Archer_Attack.png',8,tint=RANGER)
anim('u_hmarshal_idle',U+'Red/Warrior_Idle.png',8,tint=MARSHAL);anim('u_hmarshal_atk',U+'Red/Warrior_Attack1.png',4,tint=MARSHAL)
anim('u_harch_idle',U+'Purple/Priest_Idle.png',6,tint=ARCH);anim('u_harch_cast',U+'Purple/Priest_Heal.png',11,tint=ARCH)
# flying creatures: sheets of 3 frames across, 4 facings down (up, right, down, left)
if len(sys.argv)>4:
    ST=sys.argv[4]
    def ember(r,g,b):
        h,s_,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
        if v<.16 or s_<.12:return (r,g,b)
        c=colorsys.hsv_to_rgb(.03+.09*v,min(1,s_*1.25+.15),min(1,v*1.45+.1));return tuple(round(k*255) for k in c)
    def sky(r,g,b):
        h,s_,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
        if v<.16 or s_<.12:return (r,g,b)
        c=colorsys.hsv_to_rgb(.56,min(1,s_*.75),min(1,v*1.15+.05));return tuple(round(k*255) for k in c)
    for name,path,tint in (('f_wyrm','dragon/flying_golden_dragon.png',sky),('f_dragon','dragon/flying_golden_dragon.png',None),('f_drake','dragon/twin_head_dragon.png',None),
                           ('f_bat','animal/bat.png',None),('f_pegasus','mythical_being/pegasus.png',None),('f_angel','angel/angel.png',None),('f_imp','demon/winged_blue_imp.png',None)):
        im=Image.open(os.path.join(ST,path)).convert('RGBA')
        if tint:im=recolor(im,tint)
        im.save(os.path.join(OUT,name+'.png'),optimize=True)
json.dump(M,open(os.path.join(OUT,'manifest.json'),'w'))
print(json.dumps(M))
