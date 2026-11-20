const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const ctx=await b.newContext({viewport:{width:1280,height:800}});
 (async()=>{})();
 const p=await ctx.newPage();
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 require('child_process').spawn('python3',['-m','http.server','8766'],{cwd:'/home/claude/bastion',stdio:'ignore',detached:true}).unref();
 await new Promise(r=>setTimeout(r,1200));
 await p.goto('http://localhost:8766/index.html');await p.waitForTimeout(800);
 await p.click('#play');await p.waitForTimeout(400);await p.locator('.card').first().click();await p.click('#next');await p.click('#spd');await p.click('#spd');
 const t0=Date.now();while(Date.now()-t0<22000){if(await p.locator('#draft.on .card').count()){await p.waitForTimeout(200);await p.locator('#draft.on .card').nth(Math.floor(Math.random()*3)).click({force:true});continue}if(await p.locator('#next.on').count())await p.click('#next',{force:true}).catch(()=>{});await p.waitForTimeout(400);
   if(Date.now()-t0>14000&&await p.evaluate(()=>__pb().enemies.length>2&&__pb().mode==='play'))break}
 const snap=()=>p.evaluate(()=>{const S=__pb();return{wave:S.wave,level:S.level,gold:Math.floor(S.gold),hp:S.hp,cells:S.base.size,towers:[...S.base.values()].filter(c=>c.tower).map(c=>c.tower.type+c.tower.rar).sort().join(),paths:S.paths.length,enemies:S.enemies.length,road:S.road.size}});
 await p.click('#pause');await p.waitForTimeout(200);await p.screenshot({path:'sv_pause.png'});
 const before=await snap();
 await p.click('#psavex');await p.waitForTimeout(500);await p.screenshot({path:'sv_title.png'});
 const contText=await p.locator('#cont').textContent();
 await p.reload();await p.waitForTimeout(900);
 await p.click('#cont');await p.waitForTimeout(600);const after=await snap();await p.screenshot({path:'sv_loaded.png'});
 // keeps running after a load
 const t1=Date.now();while(Date.now()-t1<10000){if(await p.locator('#draft.on .card').count()){await p.locator('#draft.on .card').first().click({force:true});continue}if(await p.locator('#next.on').count())await p.click('#next',{force:true}).catch(()=>{});await p.waitForTimeout(400)}
 const later=await snap();
 await p.click('#pause').catch(()=>{});await p.waitForTimeout(200);if(await p.locator('#pausescr.on').count()){await p.click('#pexit');await p.waitForTimeout(300)}
 const backAtTitle=await p.locator('#title.on').count();
 console.log('errors',errs,'\nbefore',JSON.stringify(before),'\nafter ',JSON.stringify(after),'\nlater ',JSON.stringify(later),'\ncont:',contText,'exit->title',backAtTitle);
 await b.close();require('child_process').execSync('pkill -f "http.server 8766" || true');
})();
