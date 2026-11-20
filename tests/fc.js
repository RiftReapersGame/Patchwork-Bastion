const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1200,height:800}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>localStorage.setItem('pb_tut','1'));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(1200);
 await p.click('#play');await p.locator('#hcards .hero').nth(2).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(500);
 await p.evaluate(()=>{__pb().wave=3;__g.openDraft(false);const S=__pb();S.cards=[{id:'t_angel',kind:'tower',type:'angel',rar:0},{id:'t_imp',kind:'tower',type:'imp',rar:1},{id:'t_pegasus',kind:'tower',type:'pegasus',rar:2}];});
 await p.evaluate(()=>{document.getElementById('banbtn').click();document.getElementById('banbtn').click()});
 await p.waitForTimeout(600);await p.screenshot({path:'fc.png'});console.log(errs);await b.close()})();
