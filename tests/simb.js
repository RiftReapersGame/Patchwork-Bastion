globalThis.MutationObserver=class{observe(){}};globalThis.addEventListener=globalThis.addEventListener||(()=>{});
// headless balance sim: runs the real game code with a stub page and a bot making the choices
const fs=require('fs');const h=fs.readFileSync('/tmp/base.html','utf8');
const js=h.split('<script>')[1].split('</script>')[0];
const mk=()=>new Proxy(function(){}, {get:(t,k)=>{if(k==='clientWidth')return 1280;if(k==='clientHeight')return 800;if(k===Symbol.toPrimitive)return()=>0;if(k==='children')return[];if(k==='length')return 0;if(k===Symbol.iterator)return function*(){};return mk()},set:()=>true,apply:()=>mk(),construct:()=>mk()});
const els={};global.document={getElementById:id=>els[id]||(els[id]=mk()),createElement:()=>mk(),body:mk(),documentElement:mk(),hidden:false};
global.addEventListener=()=>{};global.devicePixelRatio=1;global.localStorage={getItem(){return null},setItem(){},removeItem(){}};
global.performance={now:()=>0};global.requestAnimationFrame=()=>{};global.Image=function(){return{set onload(f){},set onerror(f){},naturalWidth:0}};
global.DOMMatrix=function(){return mk()};global.Audio=function(){return mk()};global.setTimeout=()=>{};
eval(js);
const G=global.__g,S=()=>global.__pb();
function pickCard(policy){const s=S(),cs=s.cards;
  if(policy==='random')return cs[Math.floor(Math.random()*cs.length)];
  const free=[...s.base.values()].filter(b=>!b.core&&!b.tower).length;
  const score=c=>{let v=c.rar*2+(c.mut?1.5:0)+Math.random();
    if(c.kind==='tower'){if(c.full)v-=3;else v+=free>0?3:0;if(G.T[c.type].support&&[...s.base.values()].filter(b=>b.tower&&!b.core).length<3)v-=4}
    else v+=free<=1?4:free>=4?-2:1;return v};
  return cs.slice().sort((a,b)=>score(b)-score(a))[0]}
function spend(policy){const s=S();if(policy==='none')return;
  for(let guard=0;guard<6;guard++){
    const count={};for(const b of s.base.values())if(b.tower)count[b.tower.type]=(count[b.tower.type]||0)+1;
    const opts=Object.keys(count).filter(t=>!(G.T[t].support&&t!=='mint'&&t!=='chapel'&&t!=='bell')||true).map(t=>({t,c:G.upCost(t),n:count[t]})).filter(o=>o.c<=s.gold);
    if(policy==='smart'){const sh=G.SHOP.find(it=>it.id==='gold'&&G.shopCost(it)<=s.gold&&s.shop.gold<3&&s.wave<14);if(sh){s.gold-=G.shopCost(sh);s.shop.gold++;sh.f();continue}}
    if(!opts.length)return;
    const o=policy==='smart'?opts.sort((a,b)=>b.n/b.c-a.n/a.c)[0]:opts[Math.floor(Math.random()*opts.length)];
    G.upgradeType(o.t)}}
function run(policy,spendPol,cap){
  G.newRun(process.env.HERO||G.HEROES[Math.floor(Math.random()*4)]);let t=0,guard=0;const dt=.05,log=[];let lastW=0;
  while(guard++<4e6){const s=S();
    if(s.mode==='draft'){G.choose(pickCard(policy));continue}
    if(s.mode==='over')break;
    if(s.mode==='title'){s.mode='play'}
    if(!s.started){G.startWave()}
    if(s.between&&s.started){s.countdown=0}
    spend(spendPol);
    G.update(dt);t+=dt;s.fx.length=0;
    if(s.wave!==lastW){lastW=s.wave;log.push({w:s.wave,t,hp:s.hp,gold:Math.floor(s.gold),lvl:s.level})}
    if(s.wave>cap||t>5400)break}
  const s=S();const towers={};for(const b of s.base.values())if(b.tower&&!b.core)towers[b.tower.type]=(towers[b.tower.type]||0)+1;
  return{wave:s.wave,t,level:s.level,dealt:s.dealt||{},leak:s.leak||{},towers,plots:[...s.base.values()].filter(b=>!b.core).length,tl:Object.assign({},s.tl),log,kills:s.kills,landFull:!!s.landFull}}
module.exports={run,G,S};
if(require.main===module){
  const N=+process.argv[2]||30,pol=process.argv[3]||'smart',sp=process.argv[4]||'smart',cap=+process.argv[5]||60;
  const rs=[];for(let i=0;i<N;i++)rs.push(run(pol,sp,cap));
  const ws=rs.map(r=>r.wave).sort((a,b)=>a-b),q=p=>ws[Math.floor((ws.length-1)*p)];
  console.log(`policy ${pol}/${sp} runs ${N}: death wave min ${ws[0]} q25 ${q(.25)} median ${q(.5)} q75 ${q(.75)} max ${ws[ws.length-1]}; mean game minutes ${(rs.reduce((a,r)=>a+r.t,0)/N/60).toFixed(1)}; mean level ${(rs.reduce((a,r)=>a+r.level,0)/N).toFixed(1)}; mean plots ${(rs.reduce((a,r)=>a+r.plots,0)/N).toFixed(1)}`);
  // damage per tower-wave owned, by type
  const dmg={},own={},leak={};for(const r of rs){for(const k in r.dealt)dmg[k]=(dmg[k]||0)+r.dealt[k];for(const k in r.towers)own[k]=(own[k]||0)+r.towers[k]*r.wave;own.core=(own.core||0)+r.wave;for(const k in r.leak)leak[k]=(leak[k]||0)+r.leak[k]}
  const rows=Object.keys(G.T).map(k=>[k,Math.round(dmg[k]||0),(own[k]?(dmg[k]||0)/own[k]:0)]).sort((a,b)=>b[2]-a[2]);
  console.log('damage per tower per wave owned:');for(const r of rows)console.log('  '+r[0].padEnd(9)+String(r[1]).padStart(9)+'  '+r[2].toFixed(1));
  console.log('castle damage taken by goblin kind:',JSON.stringify(leak));
  const mid=rs.slice().sort((a,b)=>a.wave-b.wave)[Math.floor(N/2)];console.log('median run timeline (wave:minute/hp/gold/level):',mid.log.filter((_,i)=>i%3===0).map(l=>`${l.w}:${(l.t/60).toFixed(1)}/${Math.round(l.hp)}/${l.gold}/${l.lvl}`).join('  '));
}
