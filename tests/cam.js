const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1280,800,'c'],[400,820,'cm']]){
 const p=await b.newPage({viewport:{width:w,height:h},hasTouch:false});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(700);
 await p.click('#play');await p.waitForTimeout(400);await p.locator('.card').first().click();await p.click('#next');await p.click('#spd');await p.click('#spd');
 await p.waitForTimeout(5000);await p.screenshot({path:tag+'1.png'});
 const c0=await p.evaluate(()=>__cam());
 await p.mouse.move(w/2,h/2);await p.mouse.down();await p.mouse.move(w/2-250,h/2-60,{steps:6});await p.mouse.up();
 const c1=await p.evaluate(()=>__cam());await p.waitForTimeout(300);await p.screenshot({path:tag+'2.png'});
 for(let i=0;i<14;i++)await p.mouse.wheel(0,200);await p.waitForTimeout(400);await p.screenshot({path:tag+'3.png'});
 const c2=await p.evaluate(()=>__cam());
 await p.click('#home');await p.waitForTimeout(300);const c3=await p.evaluate(()=>__cam());
 // tap still selects a tower
 const pos=await p.evaluate(()=>{const S=__pb(),k=__cam();const b=[...S.base.values()].find(b=>b.tower&&!b.core);return[k.ox+(b.x+.5)*k.cs,k.oy+(b.y+.5)*k.cs]});
 await p.mouse.click(pos[0],pos[1]);await p.waitForTimeout(200);const sel=await p.locator('#info.on').count();
 // long play for stability
 const t0=Date.now();while(Date.now()-t0<20000){if(await p.locator('#over.on').count())break;if(await p.locator('#draft.on .card').count()){await p.waitForTimeout(250);await p.locator('#draft.on .card').nth(Math.floor(Math.random()*3)).click({force:true});continue}if(await p.locator('#next.on').count())await p.click('#next',{force:true}).catch(()=>{});await p.waitForTimeout(500)}
 const c4=await p.evaluate(()=>__cam());
 console.log(tag,'errors',errs,'cs',c0.cs.toFixed(1),'panned',Math.round(c1.ox-c0.ox),'zoomed cs',c2.cs.toFixed(1),'home cs',c3.cs.toFixed(1),'tap selects',sel,'cam unchanged after play',Math.abs(c4.cs-c3.cs)<.01&&Math.abs(c4.ox-c3.ox)<.5,await p.evaluate(()=>{const S=__pb();return{wave:S.wave,cells:S.base.size,paths:S.paths.map(p=>p.cells.length).join()}}));
 await p.close()}
 await b.close();
})();
