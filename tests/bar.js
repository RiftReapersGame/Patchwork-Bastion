const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1280,800,'bd'],[400,820,'bm']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(700);
 await p.click('#play');await p.waitForTimeout(400);await p.locator('.card').first().click();await p.click('#next');await p.click('#spd');await p.click('#spd');
 const t0=Date.now();let ups=0,shot=0;
 while(Date.now()-t0<36000){
   if(await p.locator('#over.on').count())break;
   if(await p.locator('#draft.on .card').count()){await p.waitForTimeout(250);await p.locator('#draft.on .card').nth(Math.floor(Math.random()*3)).click({force:true});continue}
   if(await p.locator('#next.on').count())await p.click('#next',{force:true}).catch(()=>{});
   await p.waitForTimeout(500);
   if(await p.locator('.up.can').count()){if(shot<1){shot++;const c=await p.evaluate(()=>{const S=__pb(),k=__cam();const b=[...S.base.values()].find(b=>b.tower&&!b.core);return[k.ox+(b.x+.5)*k.cs,k.oy+(b.y+.5)*k.cs]});await p.mouse.click(c[0],c[1]);await p.waitForTimeout(200);await p.screenshot({path:tag+'_bar.png'})}
     await p.locator('.up.can').last().click({force:true});ups++}
 }
 await p.screenshot({path:tag+'_end.png'});
 console.log(tag,'errors',errs,'upgrades',ups,await p.evaluate(()=>{const S=__pb();return{wave:S.wave,gold:Math.floor(S.gold),tl:JSON.stringify(S.tl),hp:S.hp}}));
 await p.close()}
 await b.close();
})();
