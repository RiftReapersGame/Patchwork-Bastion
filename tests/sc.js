const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const errs=[];
 for(const lv of [0,1]){
 const p=await b.newPage({viewport:{width:1200,height:800},deviceScaleFactor:1.5});p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>{localStorage.setItem('pb_tut','1');localStorage.setItem('pb_wins',JSON.stringify({'@forest':1,'@forest/easy':1,'@forest/normal':1}))});
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(1200);
 await p.click('#play');await p.locator('#hcards .hero').nth(1).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.waitForTimeout(300);if(lv==0)await p.screenshot({path:'sc_lv.png'});await p.locator('.hero.lvl').nth(lv).click();await p.waitForTimeout(600);
 await p.evaluate(()=>{document.getElementById('draft').classList.remove('on');__pb().mode='play'});
 await p.addStyleTag({content:'#hud,#dock,#upbar,#flyout,#dmg,#tip,#banner,#preview,#info,#draft,#mtools{display:none!important}'});
 await p.mouse.move(600,400);for(let k=0;k<3;k++){await p.mouse.wheel(0,300);await p.waitForTimeout(80)}
 await p.waitForTimeout(700);await p.screenshot({path:'sc'+lv+'.png'});
 for(let k=0;k<5;k++){await p.mouse.wheel(0,-300);await p.waitForTimeout(80)}await p.waitForTimeout(500);await p.screenshot({path:'sc'+lv+'z.png'});await p.close()}
 console.log(errs);await b.close()})();
