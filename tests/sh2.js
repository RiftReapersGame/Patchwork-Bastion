const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1210,height:756}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(900);
 await p.click('#play');await p.locator('.hero').nth(3).click();await p.click('#hgo');await p.waitForTimeout(300);
 await p.evaluate(()=>{__pb().gold=500});await p.click('#kd');await p.waitForTimeout(400);await p.screenshot({path:'sh2.png'});
 const bt=p.locator('#shop button, .shop button').filter({hasText:'80'});console.log('buttons',await bt.count());
 if(await bt.count())await bt.first().click();
 console.log(await p.evaluate(()=>JSON.stringify({rr:__pb().rerolls,gold:__pb().gold,shop:__pb().shop})),errs);await b.close();
})();
