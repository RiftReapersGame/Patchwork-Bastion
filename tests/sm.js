const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1050,500,'a'],[1210,756,'b'],[400,820,'c']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(900);
 await p.click('#play');await p.locator('#hcards .hero').nth(2).click();await p.click('#hgo');await p.locator('.hero.lvl').nth(1).click();await p.waitForTimeout(400);
 await p.evaluate(()=>{for(const t of ['phoenix','hex','bolt','cannon'])__g.choose({id:'t',kind:'tower',type:t,rar:0,mut:null});__pb().hp=__pb().maxHp=200;__pb().k2.hp=__pb().k2.maxHp=200;__pb().wave=2});
 await p.click('#next');await p.click('#spd');await p.click('#spd');await p.waitForTimeout(5000);await p.screenshot({path:'sm_'+tag+'1.png'});
 await p.waitForTimeout(9000);await p.screenshot({path:'sm_'+tag+'2.png'});
 console.log(tag,errs);await p.close()}
 await b.close();
})();
