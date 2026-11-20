const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1200,height:800},deviceScaleFactor:1.5});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(1500);
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(500);
 await p.evaluate(()=>{const e=document.querySelector('#tipskip');e&&e.click();
   const L=[[[0,0],[1,0],[0,1],[1,1]],[[0,0],[1,0],[2,0]],[[0,0],[1,0],[0,1]],[[0,0],[1,0]],[[0,0],[0,1],[1,1]]];const SPS=['power','reach','haste',null];let n=0;
   for(let i=0;i<9;i++){const cells=L[i%5];__g.choose({id:'land',kind:'chunk',cells,sp:cells.map(()=>SPS[(n++)%4]),rar:1,mut:null})}
   for(const t of ['bolt','frost'])__g.choose({id:'t',kind:'tower',type:t,rar:0,mut:null})});
 await p.addStyleTag({content:'#hud,#dock,#upbar,#flyout,#dmg,#tip,#banner,#preview,#info{display:none!important}'});
 await p.mouse.move(600,400);for(let k=0;k<4;k++){await p.mouse.wheel(0,-300);await p.waitForTimeout(100)}
 await p.waitForTimeout(3500);await p.screenshot({path:'found_raw.png'});
 console.log('errors',errs);await b.close();
})();
