const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:900,height:700},deviceScaleFactor:1.5});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>localStorage.setItem('pb_tut','1'));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForFunction(()=>!document.getElementById('loading'));
 await p.click('#play');await p.locator('#hcards .hero').nth(1).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(4500);
 await p.evaluate(()=>{const S=__pb();for(const t of ['goldie','grunt','tank','boss']){__g.spawn(t,{p:0,seg:6,t:.5});}for(const e of S.enemies)e.hp=.01;S.G.xp=0;});
 const g0=await p.evaluate(()=>[__pb().gold,document.getElementById('goldtext').textContent]);
 // hit each of them once
 await p.evaluate(()=>{const S=__pb();for(const e of S.enemies.slice())__g.hurt?__g.hurt(e,99,null):(e.hp=-1)});
 await p.waitForTimeout(250);await p.screenshot({path:'cn0.png'});await p.waitForTimeout(350);await p.screenshot({path:'cn1.png'});
 const g1=await p.evaluate(()=>[__pb().gold,document.getElementById('goldtext').textContent,__pb().fx.filter(f=>f.k==='coin').length]);
 await p.waitForTimeout(1600);const g2=await p.evaluate(()=>[__pb().gold,document.getElementById('goldtext').textContent,__pb().fx.filter(f=>f.k==='coin').length]);
 console.log(g0,g1,g2,errs);await b.close()})();
