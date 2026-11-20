const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1210,575,'t'],[400,820,'u']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(1200);
 await p.click('#play');await p.waitForTimeout(600);await p.screenshot({path:'hd_'+tag+'0.png'});
 await p.locator('.hero .more').nth(1).click();await p.waitForTimeout(300);await p.screenshot({path:'hd_'+tag+'1.png'});
 console.log(tag,'selected by details click?',await p.locator('.hero.sel').count(),errs);await p.close()}
 await b.close();
})();
