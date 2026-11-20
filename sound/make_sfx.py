import sys,json,os;sys.path.insert(0,'/home/claude/snd')
from lib import *
P=json.load(open('P.json'))
OUT='/home/claude/snd/out';os.makedirs(OUT,exist_ok=True)
# name: (source key, max seconds, start offset)
S={
 's_lance1':('lance',.5,0),'s_lance2':('lance2',.4,0),'s_thunk':('thunk',.35,0),'s_twirl':('twirl',.8,0),'s_puff':('gust3',.3,0),'s_gust':('gust',1.0,0),
 's_cannon1':('cannon1',1.0,0),'s_cannon2':('cannon3',.9,0),'s_cannon3':('cannon4',.9,0),'s_cannon4':('cannon5',.9,0),
 's_boom1':('bang1',1.0,0),'s_boom2':('bang3',1.0,0),'s_boom3':('bang5',1.0,0),'s_boom4':('expl',.6,0),
 's_splash1':('splash1',.6,0),'s_splash2':('splash2',.7,0),
 's_blade1':('blade1',.35,0),'s_blade2':('blade2',.35,0),'s_blade3':('blade3',.4,0),'s_chop':('chop',.3,0),
 's_creak':('creak',.6,0),'s_plank':('plank',.7,0),'s_bell':('bell',1.5,0),'s_bell2':('bell2',.8,0),
 's_fire1':('fire6',.9,0),'s_fire2':('fire7',.65,0),'s_fire3':('fire1',.9,0),'s_breath':('fire3',1.4,0),
 's_spell1':('spell1',.6,0),'s_spell2':('spell2',.55,0),
 's_ice1':('ice1',.25,0),'s_ice2':('ice2',.25,0),'s_ice3':('ice3',.15,0),
 's_gem1':('gem',.3,0),'s_gem2':('gem2',.3,0),
 's_rock1':('rock1',1.0,0),'s_rock2':('rock2',.9,0),'s_mining':('mining',.8,0),
 's_fall1':('rockfall1',.95,0),'s_fall2':('rockfall2',.9,0),'s_fall3':('rockfall3',.6,0),
 's_wood1':('woodbreak',.35,0),'s_wood2':('woodbreak2',.6,0),
 's_stomp':('stomp',.45,0),'s_punch':('punch',.6,0),
 's_roar1':('roar1',.7,0),'s_roar2':('roar3',1.2,0),'s_roar3':('roar4',.95,0),'s_roar4':('roar2',1.05,0),
 's_grunt1':('grunt2',.5,0),'s_grunt2':('grunt3',.6,0),'s_grunt3':('grunt4',.6,0),'s_grunt4':('grunt5',.6,0),
 's_hurt1':('hurt1',.45,0),'s_hurt2':('hurt2',.45,0),'s_hurt3':('hurt5',.45,0),
 's_die1':('cdie1',.5,0),'s_die2':('cdie2',.65,0),'s_die3':('cdie3',.65,0),'s_die4':('cdie4',.75,0),
 's_troll1':('troll1',.6,0),'s_troll2':('troll2',.8,0),'s_troll3':('troll3',.45,0),
 's_squeak1':('bug2',.4,0),'s_squeak2':('bug5',.33,0),'s_imp':('cmisc2',.2,0),'s_imp2':('att1',.2,0),'s_wing':('wing',.5,0),
 's_dshuf':('dshuf2',1.2,0),'s_dthrow':('dthrow',.6,0),'s_dthrow2':('dthrow2',.4,0),
 's_cfan':('cfan',.7,0),'s_cslide1':('cslide',.5,0),'s_cslide2':('cslide2',.5,0),'s_cplace1':('cplace',.5,0),'s_cplace2':('cplace2',.6,0),'s_cshove':('cshove',.7,0),
 's_latch':('latch',.3,0),'s_purse':('coins',.85,0),
 's_coin1':('coin1',.4,0),'s_coin2':('coin2',.5,0),'s_coin3':('coin3',.45,0),'s_jackpot':('coin4',1.6,0),
 's_chip':('chip2',.25,0),
 's_select':('select',.1,0),'s_confirm':('confirm',.55,0),'s_back':('back',.1,0),'s_deny':('err',.12,0),
 's_gong':('gong',1.4,0),'s_bellA':('bellA',1.3,0),'s_chime':('chime',.15,0),'s_hammer1':('hammer',.5,0),'s_hammer2':('hammer2',.3,0),
 's_metalfall':('metalfall',1.1,0),'s_glitch':('glitch',.05,0),
}
tot=0
for n,(k,mx,st) in S.items():
    a=load(P[k])[int(st*SR):]
    pk=np.abs(a).max();a=trim(a,th=db(pk)-42)
    a=a[:int(mx*SR)];a=fade(a,.002,min(.06,len(a)/SR*.3))
    a=norm(a,-14,-1)
    save(f'{OUT}/{n}.ogg',a,q=3);tot+=os.path.getsize(f'{OUT}/{n}.ogg')
print(len(S),'files',round(tot/1024),'KB')
