const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1000,height:700}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 const fs=require('fs');let bytes=0,n=0;
 // fake a slow connection: about 1 MB a second shared by all downloads
 let clock=0;await p.route('**/*.{webp,png}',async r=>{n++;const f=decodeURIComponent(new URL(r.request().url()).pathname);let sz=0;try{sz=fs.statSync(f).size}catch(e){}bytes+=sz;clock=Math.max(clock,Date.now())+sz/1000;await new Promise(z=>setTimeout(z,clock-Date.now()));await r.continue()});
 await p.addInitScript(()=>localStorage.setItem('pb_tut','1'));
 const t0=Date.now();p.goto('file:///home/claude/bastion/index.html').catch(()=>{});
 await p.waitForFunction(()=>document.getElementById('loading')&&document.getElementById('loading').classList.contains('done'),null,{timeout:60000});
 console.log('title shows after',((Date.now()-t0)/1000).toFixed(1),'s; images so far',n,'MB',(bytes/1e6).toFixed(2));
 await p.click('#play');await p.locator('#hcards .hero').nth(2).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();
 await p.waitForTimeout(200);console.log('overlay while waiting:',await p.evaluate(()=>[document.getElementById('loading').classList.contains('done'),document.getElementById('ldtxt').textContent]));
 await p.screenshot({path:'ld_wait.png'});
 await p.waitForFunction(()=>__pb().mode==='play'||__pb().mode==='draft',null,{timeout:60000});
 console.log('run starts after',((Date.now()-t0)/1000).toFixed(1),'s; total images',n,'MB',(bytes/1e6).toFixed(2));
 await p.waitForTimeout(1500);await p.screenshot({path:'ld_game.png'});console.log(errs);await b.close()})();
