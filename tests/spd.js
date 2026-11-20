const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1000,height:700}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>localStorage.setItem('pb_tut','1'));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForFunction(()=>document.getElementById('loading').classList.contains('done'));
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();
 await p.waitForFunction(()=>__pb().wave===1,null,{timeout:15000});
 // how far one goblin walks in one real second
 const d=async()=>{const a=await p.evaluate(()=>{const e=__pb().enemies[0];return e?e.seg+e.t:null});await p.waitForTimeout(1000);const c=await p.evaluate(()=>{const e=__pb().enemies[0];return e?e.seg+e.t:null});return (c-a).toFixed(2)};
 await p.waitForTimeout(1500);console.log('cells per second at 1x',await d());
 console.log(errs);await b.close()})();
