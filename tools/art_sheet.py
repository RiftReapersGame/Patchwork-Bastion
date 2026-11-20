import json
from PIL import Image,ImageDraw,ImageFont
A='/home/claude/bastion/assets/';M=json.load(open('/home/claude/pipe/manifest.json'))
F='/usr/share/fonts/truetype/dejavu/'
fH=ImageFont.truetype(F+'DejaVuSans-Bold.ttf',40);fS=ImageFont.truetype(F+'DejaVuSans-Bold.ttf',22);fL=ImageFont.truetype(F+'DejaVuSans-Bold.ttf',19);fN=ImageFont.truetype(F+'DejaVuSans.ttf',16);fT=ImageFont.truetype(F+'DejaVuSans-Bold.ttf',58)
INK=(44,32,40);PAR=(244,232,206);CARD=(255,249,236);RED=(178,58,52);MUTE=(110,88,72)
def frame(n,i=0,flip=False):
    im=Image.open(A+n+'.png').convert('RGBA');m=M.get(n)
    if m and m.get('f',1)>1:
        fw=im.width//m['f'];im=im.crop((i*fw,0,(i+1)*fw,im.height))
    if n in('sand','turf'):im=im.crop((0,0,192,192))
    bb=im.getbbox();im=im.crop(bb) if bb else im
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
CW,CH=230,272
def card(name,img,note,tag=None,big=False,ph='new'):
    w=CW*(2 if big else 1)+(18 if big else 0);c=Image.new('RGBA',(w,CH),CARD+(255,));d=ImageDraw.Draw(c)
    d.rounded_rectangle((0,0,w-1,CH-1),14,outline=INK,width=3)
    box=(w-24,140)
    if img is not None:
        im=img.copy();s=min(box[0]/im.width,box[1]/im.height,4 if im.width<80 else 2.2);im=im.resize((max(1,int(im.width*s)),max(1,int(im.height*s))),Image.NEAREST if s>1.5 else Image.LANCZOS)
        bg=Image.new('RGBA',(w-16,150),(120,170,100,255));c.paste(bg,(8,8));c.paste(im,((w-im.width)//2,8+150-im.height-5 if im.height<140 else 13),im)
    else:
        d.rectangle((8,8,w-9,157),fill=(232,222,200));d.multiline_text((w//2,82),ph,font=fS,fill=MUTE,anchor='mm',align='center')
    d.text((12,166),name,font=fL,fill=INK)
    y=192
    for line in wrap(note,fN,w-24):
        d.text((12,y),line,font=fN,fill=MUTE);y+=19
    if tag:
        tw=d.textlength(tag,font=fN)+16;d.rounded_rectangle((w-tw-8,14,w-8,38),9,fill=RED);d.text((w-8-tw/2,26),tag,font=fN,fill='white',anchor='mm')
    return c
def wrap(t,f,W):
    out=[];cur=''
    for wd in t.split():
        if f.getlength(cur+' '+wd)>W and cur:out.append(cur);cur=wd
        else:cur=(cur+' '+wd).strip()
    return out+([cur] if cur else [])
import sys;sys.path.insert(0,'/home/claude/pipe')
from paint2 import cutout
def nowhite(n):return cutout('/home/claude/dl/paint/found/'+n+'.png')
SECT=[];CODE='drawn in\ncode now'
def sect(title,sub,cards):SECT.append((title,sub,cards))
G=lambda n,i=0:frame(n,i)
sect('1. Goblins — both levels','Each needs a 4-pose walk loop facing right (step, pass, step, pass), same style as the towers. Shown at the size they appear now.',[
 card('Torch goblin',G('e_grunt'),'Basic goblin with a torch.','walk ×4'),
 card('Sapper',G('e_runner'),'Fast goblin with a big pack of dynamite.','walk ×4'),
 card('Goblin pack',G('e_swarm'),'Small goblin that comes in groups. Must read when tiny.','walk ×4'),
 card('Powder barrel',G('e_tank'),'Goblin inside an armoured powder barrel. Slow and tough.','walk ×4'),
 card('Brute',G('e_brute'),'Big, muscly goblin that heals as it walks.','walk ×4'),
 card('Shaman',G('e_boss'),'Goblin magic-user with a staff. Now shares the Warlord look.','walk ×4'),
 card('Goblin nest',G('e_nest'),'Barrel crammed with little goblins that burst out when it breaks.','walk ×4'),
 card('Gold barrel',G('e_gold'),'Barrel of gold carried by a running goblin.','walk ×4'),
 card('Warlord (boss)',G('e_boss'),'Huge armoured goblin chief, drawn twice normal size.','walk ×4'),
 card('Goblin camp',G('camp'),'Hut at the start of each road where goblins come from. Still image.'),
])
sect('2. The Greenwood (level 1)','Ground and scenery around the map. Trees and bushes sway in the wind now; a single still image is fine for each.',[
 card('Grass tile',frame('grass'),'Seamless square tile that repeats across the whole map.','tiles'),
 card('Meadow patch',frame('meadow'),'Lighter grass patches scattered on the grass. Seamless tile.','tiles'),
 card('Pine',G('tree1'),'Medium pine tree.'),
 card('Tall pine',G('tree2'),'Tall, thin pine.'),
 card('Birch',G('tree3'),'Small leafy tree with a pale trunk.'),
 card('Bush',G('bush'),'Low round bush.'),
 card('Flowering bush',G('bush2'),'Second bush with a bit of colour.'),
 card('Rocks ×4',frame('rock2'),'Four small grey rocks of different shapes.'),
 card('Sheep',G('sheep'),'Wanders the meadow. 4-pose walk loop if possible.','walk ×4'),
])
sect('3. The Twin Keeps (level 2)','Island in open water. The shore tiles join up like puzzle pieces; ask for one sheet and I will cut it.',[
 card('Sand shore',frame('sand'),'Beach edge between land and water: a 4×4 sheet of matching edge and corner pieces.','tile set',big=True),
 card('Island grass',frame('turf'),'Grass on the island, same 4×4 edge-and-corner layout so it sits inside the sand.','tile set',big=True),
 card('Water',None,'Seamless water tile with gentle ripples (now drawn in code).','tiles'),
 card('Sea rocks ×4',G('wrock2'),'Rocks sticking out of the water with a foam ring.'),
])
sect('4. Projectiles — what every tower fires','One still image each, pointing RIGHT, plain white background. I rotate and spin them in code, so one angle is enough. Keep them small and bold.',[
 card('Arrow',G('arrow'),'Archer tower and the Ranger castle.','Ranger'),
 card('Longbow arrow',G('arrow'),'Longbow range. Longer, white fletching.','Ranger'),
 card('Crossbow bolt',None,'Repeater crossbow. Short and stubby.','Ranger',ph=CODE),
 card('Spear',G('harpoon'),'Spear thrower. Wooden shaft, iron tip.','Ranger'),
 card('Ballista bolt',G('harpoon'),'Ballista. Huge iron-tipped bolt.','Ranger'),
 card('Glaive blade',None,'Glaive thrower. Five-pointed spinning blade, seen face-on.','Ranger',ph=CODE),
 card('Poison dart',None,'Blowpipe hunter. Tiny dart, green tip.','Ranger',ph=CODE),
 card('Powder keg',None,'Bombard and the Marshal castle. Small keg with a lit fuse.','Marshal',ph=CODE),
 card('Dynamite',G('dynamite'),'Goblin tower. Bundle of red sticks, lit fuse.','Marshal'),
 card('Oil pot',None,'Oil gallery. Clay pot with flames at the mouth.','Marshal',ph=CODE),
 card('Boulder',None,'Catapult. Big round grey rock.','Marshal',ph=CODE),
 card('Frost shard',G('fx_frost'),'Frost mage and the Archmage castle. Glowing ice crystal.','Archmage'),
 card('Hex orb',G('fx_magic'),'Hex mage and the Archmage castle. Purple curse orb.','Archmage'),
 card('Meteor',None,'Star tower. Flaming rock falling at an angle.','Archmage',ph=CODE),
 card('Stone spikes',None,'Earthshaker. A cluster of spikes bursting out of the road.','Archmage',ph=CODE),
])
sect('5. Effects — optional, lower priority','Short bursts. These can stay as they are; repaint them if they look out of place next to the new art. Ask for 4–6 frames in a row, like the flyers.',[
 card('Explosion',G('fx_explosion',3),'Bombard, Goblin tower, Catapult, Meteor.','frames'),
 card('Burning ground',G('fx_fire',2),'Oil pools, Fire forge, Dragon fire.','frames'),
 card('Dust puff',G('fx_dust',3),'Building, landing, Pegasus dive.','frames'),
 card('Healing sparkle',G('fx_heal',4),'Chapel and Phoenix.','frames'),
 card('Frost burst',G('fx_fexp',3),'When a frost shard hits.','frames'),
 card('Magic burst',G('fx_mexp',3),'Hex orb hits, Storm chapel sparks.','frames'),
 card('Sword slash',None,'Knight post and Executioner swings. Curved white arc.','frames',ph=CODE),
 card('Lightning',None,'Storm chapel, Storm drake, Thunder bell. Can stay in code.','optional',ph=CODE),
])
sect('6. Level 3 — new set, theme not chosen yet','The same kinds of pieces as levels 1 and 2, in the new theme. Once we pick the theme I will write the exact list.',[
 card('Ground tile',None,'Seamless main ground.','tiles'),
 card('Second ground',None,'Patches or edges (like meadow or shore).','tiles'),
 card('Large prop ×3',None,'Tree-sized scenery, three shapes.'),
 card('Small prop ×2',None,'Bush-sized scenery.'),
 card('Rocks ×4',None,'Small scatter pieces.'),
 card('Critter',None,'Something that wanders, like the sheep.','walk ×4'),
 card('Level feature',None,'The thing that makes the level unique (like the Twin Keeps water).'),
 card('Road look',None,'Only if the roads should look different here.'),
])
# layout
W=1920;M0=50;GAP=18;cols=(W-2*M0+GAP)//(CW+GAP)
rows=[]
y=0;blocks=[]
for t,s,cs in SECT:
    # flow cards
    x=0;r=0;pos=[]
    for c in cs:
        if x+c.width>W-2*M0:x=0;r+=1
        pos.append((x,r));x+=c.width+GAP
    h=110+(r+1)*(CH+GAP)
    blocks.append((t,s,cs,pos,h))
H=190+sum(b[4] for b in blocks)+40
sh=Image.new('RGBA',(W,H),PAR+(255,));d=ImageDraw.Draw(sh)
d.text((M0,40),'Patchwork Bastion — art still to paint',font=fT,fill=INK)
d.text((M0,118),'Everything below still uses old pixel art or simple shapes. Done: towers, castles, foundations, bridges, flying creatures and plot markers.',font=fS,fill=MUTE)
y=190
for t,s,cs,pos,h in blocks:
    d.text((M0,y),t,font=fH,fill=INK);d.text((M0,y+52),s,font=fN,fill=MUTE)
    for c,(x,r) in zip(cs,pos):sh.paste(c,(M0+x,y+100+r*(CH+GAP)),c)
    y+=h
sh.convert('RGB').save('/home/claude/sheet/art_still_needed.png',optimize=True);print(sh.size)
