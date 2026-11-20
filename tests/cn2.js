const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:900,height:700},deviceScaleFactor:1.5});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>localStorage.setItem('pb_tut','1'));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForFunction(()=>!document.getElementById('loading'));
 await p.click('#play');await p.locator('#hcards .hero').nth(1).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(3000);
 await p.evaluate(()=>{const S=__pb();const c=[...S.base.values()].find(b=>b.core);__g.coins(c.x+3,c.y+2,30);__g.coins(c.x+4.5,c.y+1,6);});
 for(const t of [150,420,700]){await p.waitForTimeout(t===150?150:t-([150,420,700][[150,420,700].indexOf(t)-1]));await p.screenshot({path:'cf'+t+'.png'})}
 console.log(errs);await b.close()})();
