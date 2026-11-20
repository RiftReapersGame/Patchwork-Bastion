const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:900,height:700},deviceScaleFactor:1.5});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>{localStorage.setItem('pb_tut','1');localStorage.setItem('pb_wins',JSON.stringify({'@forest':1,'@forest/easy':1}))});
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForFunction(()=>!document.getElementById('loading'));
 await p.click('#play');await p.locator('#hcards .hero').nth(1).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(1).click();await p.waitForTimeout(3500);
 await p.addStyleTag({content:'#banner{display:none!important}'});
 await p.evaluate(()=>{const S=__pb();S.G.xp=0;S.k2.hp=1;const pi=S.paths.findIndex(q=>q.k===1);__g.spawn('runner',{p:pi,seg:S.paths[pi].cells.length-2,t:.95});for(let i=0;i<60&&!S.k2.down;i++)__g.update(.05)});
 for(const t of [250,800,1600]){await p.waitForTimeout(t===250?250:t===800?550:800);await p.screenshot({path:'col'+t+'.png'})}
 console.log(await p.evaluate(()=>[__pb().k2.down,__pb().mode]),errs);await b.close()})();
