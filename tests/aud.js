const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox','--autoplay-policy=no-user-gesture-required']});
 const p=await b.newPage({viewport:{width:1280,height:800}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('requestfailed',r=>{if(r.url().includes('8765'))errs.push('FAIL '+r.url())});
 const got=[];p.on('response',r=>{if(r.url().includes('/audio/'))got.push(r.url().split('/').pop()+':'+r.status())});
 await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(800);
 await p.click('#play');await p.waitForTimeout(600);await p.locator('.card').first().click();await p.click('#next');await p.click('#spd');await p.click('#spd');
 const t0=Date.now();const seen=new Set();
 while(Date.now()-t0<45000){
   if(await p.locator('#over.on').count())break;
   if(await p.locator('#draft.on .card').count()){await p.waitForTimeout(250);await p.locator('#draft.on .card').nth(Math.floor(Math.random()*3)).click({force:true});continue}
   if(await p.locator('#next.on').count())await p.click('#next',{force:true}).catch(()=>{});
   await p.waitForTimeout(600);
   (await p.evaluate(()=>[...document.querySelectorAll('audio')].length)); 
 }
 console.log('audio responses',got.join(' '));console.log('errors',errs);await b.close();
})();
