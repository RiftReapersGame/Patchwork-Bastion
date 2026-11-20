const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1000,height:700},deviceScaleFactor:1.5});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>{localStorage.setItem('pb_tut','1');localStorage.setItem('pb_wins',JSON.stringify({'@coast':1,'@coast/easy':1}))});
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForFunction(()=>document.getElementById('loading').classList.contains('done'));
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(2).click();
 await p.addStyleTag({content:'#banner,#upbar,#dmg{display:none!important}'});
 await p.mouse.move(500,350);for(let k=0;k<3;k++){await p.mouse.wheel(0,-300);await p.waitForTimeout(80)}
 await p.evaluate(()=>{const S=__pb();S.decor.push({cx:0,cy:0,x:[...S.base.values()].find(b=>b.core).x-2.5,y:[...S.base.values()].find(b=>b.core).y+3.6,k:'lizard',ph:0,fl:false})});
 let got=0;for(let i=0;i<40&&!got;i++){await p.waitForTimeout(500);got=i>=16?1:0}
 await p.screenshot({path:'cy4.png'});console.log('tumbleweeds',got,errs);await b.close()})();
