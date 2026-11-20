const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1200,height:800}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>localStorage.setItem('pb_tut','1'));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(1200);
 await p.click('#play');await p.locator('#hcards .hero').nth(3).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(500);
 const r=await p.evaluate(()=>{const S=__pb();document.getElementById('draft').classList.remove('on');S.mode='play';S.wave=24;
   // a gale spire right beside the start of road 0, and nothing else that can hurt
   for(const b of S.base.values())if(b.tower&&!b.core)b.tower=null;
   const path=S.paths[0].cells;__g.spawn('brute',{p:0,seg:2,t:0});const e=S.enemies[S.enemies.length-1];e.hp=e.max=1e9;
   const c=path[4];const T=__g.T||null;
   // place the gale on any free plot by teleporting a plot next to the road start
   const k=(c[0])+','+(c[1]+1);const plot={x:c[0],y:c[1]+1,tower:null};S.base.set(k,plot);plot.tower={type:'gale',rar:3,mut:null,b:plot,cd:0,born:-9,anim:9,flip:false};
   const log=[];let last=-1;for(let i=0;i<20*90;i++){__g.update(.05);if(i%100===0)log.push((e.seg+e.t).toFixed(1)+'/'+(e.gusts||0))}return log});
 console.log(r.join(' '));console.log(errs);await b.close()})();
