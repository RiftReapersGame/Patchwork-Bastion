const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[400,820,'gm']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(700);
 await p.click('#play');await p.waitForTimeout(400);await p.locator('.card').first().click();await p.click('#next');await p.click('#spd');await p.click('#spd');
 const t0=Date.now();let ups=0,shot=false;
 while(Date.now()-t0<16000){
   if(await p.locator('#over.on').count())break;
   if(await p.locator('#draft.on .card').count()){await p.waitForTimeout(250);await p.locator('#draft.on .card').nth(Math.floor(Math.random()*3)).click({force:true});continue}
   if(await p.locator('#next.on').count())await p.click('#next',{force:true}).catch(()=>{});
   await p.waitForTimeout(500);
   const pos=await p.evaluate(()=>{const S=__pb();const b=[...S.base.values()].find(b=>b.tower&&!b.core);if(!b)return null;const cv=document.getElementById('cv');return{gold:S.gold,sel:!!S.sel,b:[b.x,b.y]}});
   if(pos&&pos.gold>=45&&!pos.sel){const c=await p.evaluate(()=>__cam());await p.mouse.click(c.ox+(pos.b[0]+.5)*c.cs,c.oy+(pos.b[1]+.5)*c.cs);await p.waitForTimeout(150)}
   if(await p.locator('#upg:not([disabled])').count()){if(!shot){shot=true;await p.screenshot({path:tag+'_up.png'})}await p.click('#upg',{force:true});ups++}
 }
 await p.screenshot({path:tag+'_end.png'});
 console.log(tag,'errors',errs,'upgrades',ups,await p.evaluate(()=>{const S=__pb();return{wave:S.wave,gold:Math.floor(S.gold),lv:[...S.base.values()].filter(b=>b.tower).map(b=>b.tower.type+b.tower.lvl).join(',')}}));
 await p.close()}
 await b.close();
})();
