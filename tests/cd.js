const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1210,756,'t'],[400,820,'u']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(900);
 await p.click('#play');await p.locator('.hero').nth(0).click();await p.click('#hgo');await p.waitForTimeout(300);
 const names=new Set();
 for(let i=0;i<40;i++){await p.evaluate(()=>{__pb().level=12;__g.openDraft(false)});(await p.locator('.card .name').allTextContents()).forEach(n=>names.add(n));
   if(i===0||i===1)await p.screenshot({path:'cd_'+tag+i+'.png'})}
 console.log([...names].filter(n=>/plot|Line|Corner|Square|shape|Plus|Long/.test(n)).join(', '));
 console.log(tag,'errors',errs);await p.close()}
 await b.close();
})();
