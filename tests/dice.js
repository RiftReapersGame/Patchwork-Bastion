const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:900,height:700},deviceScaleFactor:1.5});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>localStorage.setItem('pb_tut','1'));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForFunction(()=>document.getElementById('loading').classList.contains('done'));
 await p.click('#play');await p.locator('#hcards .hero').nth(1).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(4200);
 await p.evaluate(()=>{const S=__pb();S.G.xp=0;S.spawnQ.length=0;for(const e of S.enemies)__g.hurt(e,1e9,null)});
 const shots=[];for(const t of [300,900,1500,2200]){await p.waitForTimeout(t-(shots.length?[300,900,1500,2200][shots.length-1]:0));await p.screenshot({path:'dice'+t+'.png'});shots.push(t);
   console.log(t,await p.evaluate(()=>{const S=__pb();return [S.mode,S.dieN,S.dieT&&S.dieT.toFixed(2),S.pending,document.getElementById('dtitle').textContent]}))}
 for(let i=0;i<4;i++){const m=await p.evaluate(()=>__pb().mode);if(m!=='draft')break;console.log(await p.evaluate(()=>document.getElementById('dtitle').textContent));await p.locator('#cards .card').first().click();await p.waitForTimeout(500)}
 console.log(errs);await b.close()})();
