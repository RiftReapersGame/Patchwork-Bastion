const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1210,575,'t'],[400,820,'u']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(900);
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.waitForTimeout(300);
 await p.locator('.dbtn').nth(0).click();await p.waitForTimeout(300);await p.screenshot({path:'df_'+tag+'.png'});
 const fit=await p.evaluate(()=>{const l=document.querySelector('#levels');return [l.scrollHeight,l.clientHeight]});
 await p.locator('.hero.lvl').nth(1).click();await p.waitForTimeout(300);
 console.log(tag,fit,await p.evaluate(()=>JSON.stringify({diff:__pb().diff,hp:__pb().hp,hp2:__pb().k2.hp})),errs);await p.close()}
 await b.close();
})();
