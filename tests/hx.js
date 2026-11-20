const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1210,height:756}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(1500);
 await p.click('#play');await p.evaluate(()=>{document.querySelector('#heroes').scrollTop=200});
 await p.locator('.hero').nth(1).click();await p.click('#hgo');await p.waitForTimeout(400);
 await p.click('#pause');await p.click('#pexit');await p.click('#play');await p.waitForTimeout(500);
 await p.screenshot({path:'hx.png'});
 console.log(await p.evaluate(()=>{const h=document.querySelector('#heroes');return JSON.stringify({st:h.scrollTop,sh:h.scrollHeight,ch:h.clientHeight})}),errs);await b.close();
})();
