const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox','--autoplay-policy=no-user-gesture-required']});
const out={};
for(const [hi,lvl] of [[1,2],[2,1],[3,0],[0,0]]){const hero=hi;
const p=await b.newPage({viewport:{width:1100,height:700}});const bad=[],errs=[];
p.on('response',r=>{if(r.status()>=400)bad.push(r.status()+' '+r.url().split('/').pop())});p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{localStorage.setItem('pb_tut','1');localStorage.setItem('pb_wins',JSON.stringify({'@forest':1,'@forest/easy':1,'@coast':1,'@coast/easy':1}))});
await p.goto('http://localhost:8766/index.html');await p.waitForTimeout(4000);
await p.click('#play');await p.waitForTimeout(300);
await p.locator('#hcards .hero').nth(Math.max(0,hi)).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.waitForTimeout(300);
await p.locator('.hero.lvl').nth(lvl).click();await p.waitForTimeout(4000);
// count sounds actually played
await p.evaluate(()=>{window.__played={};const inv=new Map(Object.entries(__g.BUF).map(([k,v])=>[v,k]));const o=AudioBufferSourceNode.prototype.start;AudioBufferSourceNode.prototype.start=function(...a){const n=inv.get(this.buffer)||'?';window.__played[n]=(window.__played[n]||0)+1;return o.apply(this,a)}});
const r=await p.evaluate(()=>{const g=__g;const S=__pb();
  // give gold and auto-build some towers via cards: just run waves
  let steps=0;for(let w=0;w<40;w++){for(let i=0;i<300&&S.mode==='play';i++){g.update(.05);steps++}if(S.mode==='draft'){const c=document.querySelector('#cards .card');if(c)c.click()}if(S.mode==='over')break}
  return {wave:S.wave,mode:S.mode,map:S.map,steps}});
await p.waitForTimeout(1500);
const st=await p.evaluate(()=>{const need=new Set(Object.values(__g.REC).flatMap(r=>[].concat(r[0])));return {played:window.__played,missing:[...need].filter(f=>!__g.BUF[f]),music:Object.keys(__g.MUS)}});
out[hero+'/'+lvl]={r,st,bad,errs};await p.close()}
console.log(JSON.stringify(out,null,1));await b.close()})();
