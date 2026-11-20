const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1280,800,'t'],[400,820,'u']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(800);
 await p.click('#play');await p.waitForTimeout(700);
 await p.screenshot({path:'h_'+tag+'_sel.png',fullPage:false});
 if(tag==='t')for(const i of [0,1,2,3]){
   if(i){await p.evaluate(()=>{document.querySelector('#pause').click()});await p.click('#pexit');await p.click('#play');await p.waitForTimeout(300)}
   await p.locator('.hero').nth(i).click();if(i==0)await p.screenshot({path:'h_t_picked.png'});await p.click('#hgo');await p.waitForTimeout(300);
   await p.evaluate(()=>{const S=__pb();S.hp=S.maxHp=300;S.wave=5});
   await p.click('#next');await p.click('#spd');await p.waitForTimeout(9000);
   const c=p.locator('#draft.on .card');if(await c.count())await c.first().click();
   await p.evaluate(()=>{const S=__pb();S.sel=S.base.get(__hub()[0]+','+__hub()[1])});
   await p.mouse.click(w/2,h/2-10);await p.waitForTimeout(400);
   await p.screenshot({path:'h_t_run'+i+'.png'});
   console.log(i,await p.evaluate(()=>JSON.stringify({hero:__pb().hero,d:__pb().dealt,hp:__pb().hp,w:__pb().wave})));
 }
 console.log(tag,'errors',errs);await p.close()}
 await b.close();
})();
