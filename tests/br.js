const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1280,height:800}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(700);
 await p.click('#play');await p.waitForTimeout(400);await p.locator('.card').first().click();
 await p.evaluate(()=>{const S=__pb();S.maxHp=S.hp=300;S.level=30});
 await p.click('#next');await p.click('#spd');await p.click('#spd');
 const t0=Date.now();let lands=0;
 while(Date.now()-t0<45000){
   if(await p.locator('#over.on').count())break;
   if(await p.locator('#draft.on .card').count()){await p.waitForTimeout(150);
     const land=p.locator('#draft.on .card:has-text("land")');if(await land.count()){await land.first().click({force:true});lands++}else if(await p.locator('#reroll:not([disabled])').count()){await p.evaluate(()=>{__pb().rerolls=9});await p.click('#reroll')}else await p.locator('#draft.on .card').first().click({force:true});continue}
   if(await p.locator('#next.on').count())await p.click('#next',{force:true}).catch(()=>{});
   await p.waitForTimeout(300);
 }
 await p.screenshot({path:'br1.png'});
 console.log('errors',errs,'lands',lands,await p.evaluate(()=>{const S=__pb();let br=0;for(const c of S.base.values())if(!c.core&&S.road.has(c.x+','+c.y))br++;return{wave:S.wave,cells:S.base.size,bridges:br,landFull:!!S.landFull}}));
 await b.close();
})();
