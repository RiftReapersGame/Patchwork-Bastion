const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const ctx=await b.newContext({viewport:{width:1280,height:800}});const p=await ctx.newPage();
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 require('child_process').spawn('python3',['-m','http.server','8767'],{cwd:'/home/claude/bastion',stdio:'ignore',detached:true}).unref();
 await new Promise(r=>setTimeout(r,900));
 await p.goto('http://localhost:8767/index.html');await p.waitForTimeout(800);
 await p.click('#play');await p.locator('.hero').nth(3).click();await p.click('#hgo');await p.locator('.hero.lvl').nth(1).click();await p.waitForTimeout(2600);
 await p.mouse.click(640,350);await p.waitForTimeout(300);
 await p.evaluate(()=>{__pb().gold=500});await p.locator('.up[data-type=core]').click();await p.waitForTimeout(300);
 await p.screenshot({path:'h2_info.png'});
 await p.click('#next');await p.click('#spd');await p.waitForTimeout(12000);
 const c=p.locator('#draft.on .card');if(await c.count()){await p.screenshot({path:'h2_draft.png'});await c.first().click()}
 await p.click('#pause');await p.click('#psavex');await p.waitForTimeout(300);
 console.log(await p.textContent('#cont'));
 await p.click('#cont');await p.waitForTimeout(500);
 console.log(await p.evaluate(()=>JSON.stringify({hero:__pb().hero,core:__g.T.core.name,map:__pb().map,land:__pb().land&&__pb().land.size,lv:__pb().tl.core,wave:__pb().wave})));
 await p.screenshot({path:'h2_loaded.png'});
 console.log('errors',errs);await b.close();process.exit(0);
})();
