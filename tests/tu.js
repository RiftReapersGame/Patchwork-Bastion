const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1210,575,'t'],[400,820,'u']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(900);
 await p.screenshot({path:'tu_'+tag+'m.png'});
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(600);
 await p.screenshot({path:'tu_'+tag+'0.png'});console.log(await p.textContent('#tiptext'));
 await p.click('#tipok');await p.evaluate(()=>{__pb().hp=__pb().maxHp=500});await p.click('#next');await p.click('#spd');await p.click('#spd');
 await p.waitForSelector('#draft.on',{timeout:40000});await p.waitForTimeout(500);await p.screenshot({path:'tu_'+tag+'1.png'});
 await p.locator('#draft.on .card').first().click();await p.waitForTimeout(600);
 while(await p.locator('#draft.on').count()){await p.locator('#draft.on .card').first().click();await p.waitForTimeout(400)}
 await p.waitForTimeout(600);await p.screenshot({path:'tu_'+tag+'2.png'});
 console.log(tag,await p.locator('#tip.on').count(),await p.textContent('#tiptext'),errs);await p.close()}
 await b.close();
})();
