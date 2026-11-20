const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1200,height:800},deviceScaleFactor:1.5});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(1500);
 await p.click('#play');await p.locator('#hcards .hero').nth(1).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(500);
 await p.evaluate(()=>{const e=document.querySelector('#tipskip');e&&e.click();
   for(let i=0;i<5;i++)__g.choose({id:'land',kind:'chunk',cells:[[0,0],[1,0],[2,0]],sp:[null,null,null],rar:1,mut:null});
   for(const t of ['cannon','tnt','oil','guard','cannon','tnt','oil','guard'])__g.choose({id:'t',kind:'tower',type:t,rar:0,mut:null});__pb().hp=__pb().maxHp=900;__pb().wave=5});
 await p.screenshot({path:'tw5_ui.png'});
 await p.addStyleTag({content:'#hud,#dock,#upbar,#flyout,#dmg,#tip,#banner,#preview,#info{display:none!important}'});
 await p.evaluate(()=>__g.startWave());await p.mouse.move(600,400);for(let k=0;k<3;k++){await p.mouse.wheel(0,-300);await p.waitForTimeout(100)}
 await p.waitForTimeout(7000);await p.screenshot({path:'tw5.png'});
 await p.evaluate(()=>{__pb().level=9;__g.openDraft(false)});
 console.log('errors',errs);await b.close();
})();
