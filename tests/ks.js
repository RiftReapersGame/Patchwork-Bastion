const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1210,575,'t'],[400,820,'u']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(1200);
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(400);
 await p.evaluate(()=>{const e=document.querySelector('#tipskip');e&&e.click();__pb().gold=600});
 await p.click('#kd');await p.waitForTimeout(500);await p.screenshot({path:'ks_'+tag+'.png'});
 await p.locator('#flyout .shopit').nth(3).click();await p.waitForTimeout(300);
 const st=await p.evaluate(()=>JSON.stringify({g:__pb().gold,rr:__pb().rerolls,modal:document.querySelector('#shop').classList.contains('on'),n:document.querySelectorAll('#flyout .shopit').length}));
 await p.click('#kd');await p.waitForTimeout(200);console.log(tag,st,'closed',!(await p.locator('#flyout.on').count()),errs);await p.close()}
 await b.close();
})();
