const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1280,800,'s'],[400,820,'sm']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(700);
 await p.click('#play');await p.waitForTimeout(400);await p.locator('.card').first().click();
 await p.evaluate(()=>{__pb().gold=1200});await p.waitForTimeout(200);
 await p.click('#kd');await p.waitForTimeout(250);await p.screenshot({path:tag+'_shop.png'});
 await p.locator('.srow .big').nth(0).click();await p.locator('.srow .big').nth(2).click();await p.locator('.srow .big').nth(3).click();
 const st=await p.evaluate(()=>{const S=__pb();return{gold:S.gold,shop:S.shop,G:S.G.gold,maxHp:S.maxHp}});
 await p.click('#shopclose');await p.click('#next');await p.click('#spd');await p.click('#spd');
 const kinds=new Set();const t0=Date.now();
 while(Date.now()-t0<25000){if(await p.locator('#over.on').count())break;
   if(await p.locator('#draft.on .card').count()){await p.waitForTimeout(200);for(const t of await p.locator('#draft.on .ribbon span').allTextContents())kinds.add(t.split(' ').pop());await p.locator('#draft.on .card').nth(Math.floor(Math.random()*3)).click({force:true});continue}
   if(await p.locator('#next.on').count())await p.click('#next',{force:true}).catch(()=>{});await p.waitForTimeout(400)}
 console.log(tag,'errors',errs,JSON.stringify(st),'card kinds',[...kinds].join());
 await p.close()}
 await b.close();
})();
