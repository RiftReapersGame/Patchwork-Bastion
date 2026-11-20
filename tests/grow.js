const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1280,height:800}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(700);
 await p.click('#play');await p.waitForTimeout(400);await p.locator('.card').first().click();await p.click('#next');await p.click('#spd');await p.click('#spd');
 let n=0;const t0=Date.now();
 while(Date.now()-t0<75000){
   if(await p.locator('#over.on').count())break;
   if(await p.locator('#draft.on .card').count()){await p.waitForTimeout(300);
     const land=p.locator('#draft.on .card:has-text("land")');const c=(await land.count())?land.first():p.locator('#draft.on .card').nth(Math.floor(Math.random()*3));await c.click({force:true});await p.waitForTimeout(100);continue}
   if(await p.locator('#next.on').count())await p.click('#next',{force:true}).catch(()=>{});
   await p.waitForTimeout(500);
   const r=await p.evaluate(()=>__pb().base.size);
   if(r>14&&n===0){n=1;await p.waitForTimeout(1500);await p.screenshot({path:'g1.png'})}
 }
 await p.screenshot({path:'g2.png'});
 for(let i=0;i<3;i++)await p.evaluate(()=>__grow());await p.waitForTimeout(2500);await p.screenshot({path:'g3.png'});
 console.log('errors',errs,await p.evaluate(()=>{const S=__pb();return{wave:S.wave,cells:S.base.size,paths:S.paths.length,mode:S.mode,hp:S.hp}}));await b.close();
})();
