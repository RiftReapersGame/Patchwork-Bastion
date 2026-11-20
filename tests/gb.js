const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1200,height:800},deviceScaleFactor:1.5});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>localStorage.setItem('pb_tut','1'));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(1200);await p.screenshot({path:'gb_title.png'});
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(500);
 await p.evaluate(()=>{const S=__pb();S.wave=6;document.getElementById('draft').classList.remove('on');S.mode='play';
   const types=['grunt','runner','swarm','tank','brute','shaman','nest','goldie','boss'];let i=0;
   for(const t of types){__g.spawn(t,{p:0,seg:2+i*2,t:.5});i++}
   for(let k=0;k<6;k++)__g.spawn(types[k],{p:Math.min(1,__pb().paths.length-1),seg:3+k*2,t:.3});});
 await p.addStyleTag({content:'#upbar,#flyout,#dmg,#tip,#banner,#info,#draft{display:none!important}'});
 await p.waitForTimeout(400);await p.screenshot({path:'gb.png'});
 await p.mouse.move(600,400);for(let k=0;k<6;k++){await p.mouse.wheel(0,400);await p.waitForTimeout(80)}await p.waitForTimeout(500);await p.screenshot({path:'gb2.png'});
 console.log(errs);await b.close()})();
