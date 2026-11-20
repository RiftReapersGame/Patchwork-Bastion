const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1210,height:756}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(900);
 // forest sanity
 await p.click('#play');await p.locator('.hero').nth(0).click();await p.click('#hgo');await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(400);
 await p.click('#next');await p.click('#spd');await p.click('#spd');await p.waitForTimeout(8000);
 console.log('forest',await p.evaluate(()=>JSON.stringify({map:__pb().map,k2:__pb().k2,hp:__pb().hp,d:__pb().wd})));
 const c=p.locator('#draft.on .card');if(await c.count())await c.first().click();
 await p.click('#pause');await p.click('#pexit');
 // twin: lose the east keep
 await p.click('#play');await p.locator('#hcards .hero').nth(1).click();await p.click('#hgo');await p.locator('.hero.lvl').nth(1).click();await p.waitForTimeout(400);
 await p.click('#next');await p.waitForTimeout(3000);
 await p.evaluate(()=>{const S=__pb();S.k2.hp=1;for(const e of S.enemies){const pt=S.paths.findIndex(q=>q.k===1);e.p=pt;e.seg=S.paths[pt].cells.length-2;e.t=.5}});
 await p.waitForTimeout(2500);await p.screenshot({path:'tw_over.png'});
 console.log('twin',await p.evaluate(()=>JSON.stringify({mode:__pb().mode,hp:__pb().hp,hp2:__pb().k2.hp,fell:__pb().fellK})),'errors',errs);await b.close();
})();
