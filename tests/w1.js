const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const errs=[];
 for(const tut of ['1','0']){
 const p=await b.newPage({viewport:{width:900,height:700}});p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(v=>localStorage.setItem('pb_tut',v),tut);
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForFunction(()=>document.getElementById('loading').classList.contains('done'));
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();
 const log=[];for(let i=0;i<10;i++){await p.waitForTimeout(500);log.push(await p.evaluate(()=>__pb().wave+':'+document.getElementById('next').textContent.replace('Next wave','N').replace('Wave 1 in','W1')))}
 console.log('tips '+(tut==='0'?'on':'off'),log.join(' '));
 if(tut==='0'){await p.click('#tipok');const l2=[];for(let i=0;i<10;i++){await p.waitForTimeout(500);l2.push(await p.evaluate(()=>__pb().wave))}console.log(' after closing tip',l2.join(' '))}
 await p.close()}
 console.log(errs);await b.close()})();
