const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const errs=[];
 for(const [w,h] of (process.env.SZ||'1200x800,700x1000').split(',').map(s=>s.split('x').map(Number))){
 const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});p.on('pageerror',e=>errs.push(w+' '+e.message));
 await p.addInitScript(()=>{localStorage.setItem('pb_tut','1');localStorage.setItem('pb_wins',JSON.stringify({'@forest':1,'@forest/easy':1,'@forest/normal':1,'@coast':1,'@coast/easy':1}))});
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForFunction(()=>document.getElementById('loading').classList.contains('done'));
 await p.click('#play');await p.locator('#hcards .hero').nth(+(process.env.HERO||1)).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.waitForTimeout(500);
 if(w===1200)await p.screenshot({path:'cy_lv.png'});
 await p.locator('.hero.lvl').nth(2).click();await p.waitForTimeout(4000);
 const info=await p.evaluate(()=>{const S=__pb();return {map:S.map,keeps:S.k2&&S.k3?3:0,mesa:S.mesa?S.mesa.size:0,paths:S.paths.map(q=>q.cells.length+'→'+q.k),hp:document.getElementById('hptext').textContent+' | '+document.getElementById('hptext2').textContent+' | '+document.getElementById('hptext3').textContent}});
 console.log(w+'x'+h,JSON.stringify(info));
 await p.screenshot({path:'cy_'+w+'.png'});await p.close()}
 console.log(errs);await b.close()})();
