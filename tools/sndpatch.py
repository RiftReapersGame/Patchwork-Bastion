p='/home/claude/pipe/index.src.html';s=open(p).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a));s=s.replace(a,b)
# 1. sound table: arrays mean "pick one at random"
i=s.index('const REC={');j=s.index('};',i)+2
s=s[:i]+r"""const V=(p,n)=>Array.from({length:n},(_,i)=>p+(i+1));
const REC={bolt:['bow',.3,1.08,80],core:['bow',.2,1.25,110],sniper:['bow',.55,.8,90],repeater:['bow',.22,1.4,60],
  ballista:['s_thunk',.42,.85,120],lancer:[['s_lance1','s_lance2'],.3,1,100],glaive:['s_twirl',.3,1.15,110],blowpipe:['s_puff',.22,1.5,90],
  cannon:[V('s_cannon',4),.32,1,90],tnt:['throw',.45,.95,110],oil:['throw',.45,.8,200],catapult:['s_creak',.4,1.1,300],exec:['s_chop',.38,1,120],guard:[V('s_blade',3),.24,1,120],
  bell:['s_bell',.5,1,400],flame:['fire',.22,1,650],tesla:['magichit',.32,1.5,110],frost:[V('s_ice',3),.26,1,110],hex:['s_spell2',.24,.85,120],gale:['s_gust',.42,1,300],
  quake:[['s_rock1','s_rock2'],.42,1,200],obelisk:[['s_gem1','s_gem2'],.14,1.1,300],star:['s_spell1',.42,.7,300],
  dragon:['s_breath',.4,1,500],dragonroar:[V('s_roar',3),.32,1.15,2500],phoenix:[['s_fire1','s_fire2'],.3,1.25,250],pegasus:[['s_punch','s_stomp'],.3,1.1,140],imp:[['s_imp','s_imp2'],.22,1.35,120],bats:[['s_squeak1','s_squeak2'],.16,1.5,90],drake:['magichit',.32,1.2,140],
  boom:[V('s_boom',4),.5,1,90],splash:[['s_splash1','s_splash2'],.32,1,150],
  die:[V('s_die',4),.2,1.35,70],diebig:['diebig',.7,1,200],brutedie:[['s_troll2','s_troll1'],.42,.9,200],barrel:[['s_boom1','s_boom2'],.6,.9,150],nestbreak:[['s_wood2','s_wood1'],.5,1,150],jackpot:['s_jackpot',.4,1,300],
  ehit:[[...V('s_grunt',4),...V('s_hurt',3)],.09,1.45,150],bhit:[V('s_troll',3),.14,1,260],
  hub:['castlehit',.75,1,120],collapse:[V('s_fall',3),.75,.8,600],warroar:[['s_roar2','s_roar4'],.8,.8,900],
  level:['levelup',.55,1,300],pick:['tap',.7,1,40],deny:['s_deny',.25,1,120],build:['build',.6,1,120],upgrade:[['s_hammer1','s_hammer2'],.4,1,120],land:['land',.7,1,120],
  wave:['wave',.55,1,400],boss:['boss',.8,1,900],rift:['growl',.6,1,400],over:['lose',.8,1,900],cleared:['cleared',.6,1,300],gong:['s_gong',.5,1,900],
  coin:[V('s_coin',3),.16,1.15,55],purse:['s_purse',.4,1,150],
  dshuf:['s_dshuf',.5,1,600],dthrow:['s_dthrow',.55,1,300],deal:['s_cfan',.42,1,300],cpick:[['s_cplace1','s_cplace2'],.45,1,120],banish:['s_cshove',.5,1,200],lock:['s_latch',.4,1,120]};
""".lstrip('\n')+s[j:]
rep("for(const f of new Set(Object.values(REC).map(r=>r[0])))","for(const f of new Set(Object.values(REC).flatMap(r=>[].concat(r[0]))))")
rep("if(r&&BUF[r[0]]){const src=AC.createBufferSource(),ga=AC.createGain();src.buffer=BUF[r[0]];",
    "const fn=r?(Array.isArray(r[0])?r[0][Math.random()*r[0].length|0]:r[0]):null;\n  if(r&&BUF[fn]){if(voices>=22&&r[3]<200)return;voices++;const src=AC.createBufferSource(),ga=AC.createGain();src.buffer=BUF[fn];src.onended=()=>voices--;")
rep("const BUF={};let sfxAsked=false;","const BUF={};let sfxAsked=false,voices=0;")
# 2. music per level + ambience
rep("const TRACKS={calm:['calm.ogg',.5],battle:['battle.ogg',.5],march:['march.ogg',.5],epic:['epic.mp3',.2]};",
    "const TRACKS={calm:['calm.ogg',.5],battle:['battle.ogg',.5],march:['march.ogg',.5],epic:['epic.mp3',.2],\n  coast_calm:['mus_coast_calm.ogg',.28],coast_battle:['mus_coast_battle.ogg',.42],canyon_calm:['mus_canyon_calm.ogg',.28],canyon_battle:['mus_canyon_battle.ogg',.28],\n  amb_forest:['amb_forest.ogg',.32],amb_coast:['amb_coast.ogg',.3],amb_canyon:['amb_canyon.ogg',.3]};\nconst LMUS={coast:{calm:'coast_calm',battle:'coast_battle'},canyon:{calm:'canyon_calm',battle:'canyon_battle'}};")
rep("  else want=S.wave%5===0?'epic':S.wave%2?'battle':'march';\n  if(S.mode==='draft'&&musWant)want=musWant;\n  musWant=want;",
    "  else want=S.wave%5===0?'epic':S.wave%2?'battle':'march';\n  if(S.mode==='draft'&&musWant)want=musWant;\n  musWant=want;\n  const lm=S.mode!=='title'&&LMUS[S.map];if(lm&&want){if(want==='calm')want=lm.calm;else if(want!=='epic')want=S.wave%2||!lm.march?lm.battle:lm.march}\n  const amb=S.mode!=='title'&&S.mode!=='over'&&S.map?'amb_'+S.map:null;")
rep("  for(const k in MUS){const a=MUS[k],tv=(k===want&&!muted&&!document.hidden)?TRACKS[k][1]:0;",
    "  if(amb&&TRACKS[amb]&&!MUS[amb]){const a=new Audio('audio/'+TRACKS[amb][0]);a.loop=true;a.volume=0;a.preload='auto';MUS[amb]=a}\n  for(const k in MUS){const a=MUS[k],tv=((k===want||k===amb)&&!muted&&!document.hidden)?TRACKS[k][1]:0;")
# 3. events
rep("if(!quiet){e.flash=.1;","if(!quiet){e.flash=.1;if(src&&e.hp-d>0)sfx(e.type==='brute'||e.type==='boss'?'bhit':'ehit');")
# careful: e.hp already reduced above; fix condition after
rep("if(src&&e.hp-d>0)sfx(","if(src&&e.hp>0)sfx(")
rep("else sfx(e.type==='tank'||e.type==='nest'||e.type==='brute'?'diebig':'die');",
    "else sfx(e.type==='tank'?'barrel':e.type==='nest'?'nestbreak':e.type==='brute'?'brutedie':e.type==='goldie'?'jackpot':'die');")
rep("sfx(boss?'boss':'wave');","sfx(boss?'boss':'wave');if(boss)setTimeout(()=>sfx('warroar'),700);")
rep("  if(t.type==='dragon'){const cs2=S.paths[tg.p].cells;sfx('flame');","  if(t.type==='dragon'){const cs2=S.paths[tg.p].cells;sfx('dragon');if(Math.random()<.3)sfx('dragonroar');")
rep("if(t.type==='drake'){const pts=[[f.x,f.y-1.1]],hit=new Set();let cur=tg,n=d.chain+L(t)-1;sfx('tesla');","if(t.type==='drake'){const pts=[[f.x,f.y-1.1]],hit=new Set();let cur=tg,n=d.chain+L(t)-1;sfx('drake');")
rep("  hurt(tg,dmg,t);\n  if(t.type==='phoenix')","  hurt(tg,dmg,t);if(t.type!=='pegasus')sfx(t.type);\n  if(t.type==='phoenix')")
rep("sfx('guard')}\n  else emit(","sfx('pegasus')}\n  else emit(")
rep("S.pools.push({x:s.tx,y:s.ty,r:.85,life:8,dmg:s.dmg,src:s.src,tk:0});sfx('flame');continue}","S.pools.push({x:s.tx,y:s.ty,r:.85,life:8,dmg:s.dmg,src:s.src,tk:0});sfx('splash');continue}")
# die roll: shake once, then the throw
rep("if(S.dieT>DIE_T-.95&&k!==S.dieTick){S.dieTick=k;sfx('pick')}if(S.dieT<=DIE_T-.95&&S.dieTick>=0){S.dieTick=-1;sfx('land')}",
    "if(S.dieT>DIE_T-.95&&k!==S.dieTick){if(S.dieTick==null||S.dieTick<0)sfx('dshuf');S.dieTick=k}if(S.dieT<=DIE_T-.95&&S.dieTick>=0){S.dieTick=-1;sfx('dthrow')}")
# keeps and castles
rep("if(standing().length>1){K.down=true;keepFall(ki);S.shake=Math.max(S.shake,.6);sfx('boss');","if(standing().length>1){K.down=true;keepFall(ki);S.shake=Math.max(S.shake,.6);sfx('collapse');sfx('barrel');")
rep("function victory(){\n  S.won=true;S.mode='won';sfx('level');","function victory(){\n  S.won=true;S.mode='won';sfx('level');sfx('gong');")
rep("S.gold-=c;S.tl[type]=(S.tl[type]||1)+1;sfx('build');","S.gold-=c;S.tl[type]=(S.tl[type]||1)+1;sfx('upgrade');")
rep("S.shop[it.id]++;it.f();sfx('level');renderShop()","S.shop[it.id]++;it.f();sfx('purse');renderShop()")
rep("if(S.gold<cc){sfx('pick');return}S.gold-=cc;S.shop[it.id]++;it.f();sfx('level');","if(S.gold<cc){sfx('deny');return}S.gold-=cc;S.shop[it.id]++;it.f();sfx('purse');")
rep("crowns-=price;arm[a.id]=l+1;crSave();sfx('build');","crowns-=price;arm[a.id]=l+1;crSave();sfx('purse');")
open(p,'w').write(s)
