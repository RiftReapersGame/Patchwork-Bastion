const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1200,height:800},deviceScaleFactor:1.5});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>localStorage.setItem('pb_tut','1'));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(1200);
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(500);
 await p.evaluate(()=>{for(let i=0;i<3;i++)__g.choose({id:'land',kind:'chunk',cells:[[0,0],[1,0],[2,0]],sp:['power','reach','haste'],rar:2,mut:null});
   for(const t of ['bolt','cannon'])__g.choose({id:'t',kind:'tower',type:t,rar:0,mut:null});__pb().wave=3;__g.openDraft(false)});
 await p.waitForTimeout(500);await p.screenshot({path:'sp_draft.png'});
 await p.evaluate(()=>{document.getElementById('draft').classList.remove('on');__pb().mode='play'});
 await p.addStyleTag({content:'#hud,#dock,#upbar,#flyout,#dmg,#tip,#banner,#preview,#info,#draft{display:none!important}'});
 await p.mouse.move(600,400);for(let k=0;k<3;k++){await p.mouse.wheel(0,-300);await p.waitForTimeout(100)}
 await p.waitForTimeout(800);await p.screenshot({path:'sp.png'});console.log(errs);await b.close()})();
