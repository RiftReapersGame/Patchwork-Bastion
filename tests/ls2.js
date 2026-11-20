const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1100,height:700}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>{localStorage.setItem('pb_tut','1');localStorage.setItem('pb_wins',JSON.stringify({'@forest':1,'@forest/easy':1,'@forest/normal':1}))});
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForFunction(()=>!document.getElementById('loading'));
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(1).click();await p.waitForTimeout(4200);
 // knock the second keep to 1 hp and send a goblin down one of its roads
 const r=await p.evaluate(()=>{const S=__pb();S.G.xp=0;S.k2.hp=1;const pi=S.paths.findIndex(q=>q.k===1);const pj=S.paths.findIndex(q=>q.k!==1);
   __g.spawn('runner',{p:pi,seg:S.paths[pi].cells.length-2,t:.9});for(let i=0;i<200&&S.mode==='play';i++)__g.update(.05);
   await 0;const after1={k2down:!!S.k2.down,mode:S.mode,hp:S.hp,txt:document.getElementById('hptext2').textContent};
   // another goblin down the fallen keep's road should now hit the west keep
   return after1;const hp0=S.hp;__g.spawn('runner',{p:pi,seg:S.paths[pi].cells.length-2,t:.9});for(let i=0;i<200;i++)__g.update(.05);
   const after2={hpBefore:hp0,hpAfter:S.hp,mode:S.mode};
   S.hp=1;__g.spawn('runner',{p:pj,seg:S.paths[pj].cells.length-2,t:.9});for(let i=0;i<200&&S.mode==='play';i++)__g.update(.05);
   return {after1,after2,final:S.mode,head:document.querySelector('#over h2').textContent}});
 console.log(JSON.stringify(r));await p.evaluate(()=>{const S=__pb();S.mode='play';});await p.waitForTimeout(3600);await p.screenshot({path:'ls.png'});console.log(errs);await b.close()})();
