const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1280,800,'e'],[400,820,'em']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(700);
 await p.click('#play');await p.waitForTimeout(400);await p.locator('.card').first().click();
 // jump ahead so every goblin kind is unlocked, with a strong base so the run lasts
 await p.evaluate(()=>{const S=__pb();S.wave=9;S.maxHp=S.hp=400;S.tl={bolt:9,tesla:6,cannon:6,flame:6,core:8};const ts=['bolt','tesla','cannon','flame'];let i=0;for(const c of S.base.values())if(!c.core){c.tower={type:ts[i++%4],rar:2,mut:null,b:c,cd:0,born:-9,anim:9,flip:false}}});
 await p.click('#next');await p.click('#spd');await p.click('#spd');
 const seen=new Set();let shots=0;const t0=Date.now();
 while(Date.now()-t0<42000){
   if(await p.locator('#over.on').count())break;
   if(await p.locator('#draft.on .card').count()){await p.waitForTimeout(200);await p.locator('#draft.on .card').nth(Math.floor(Math.random()*3)).click({force:true});continue}
   if(await p.locator('#next.on').count()){if(shots<1){shots++;await p.locator('.chip').first().click();await p.waitForTimeout(150);await p.screenshot({path:tag+'_pv.png'})}await p.click('#next',{force:true}).catch(()=>{})}
   await p.waitForTimeout(400);
   for(const t of await p.evaluate(()=>__pb().enemies.map(e=>e.type)))seen.add(t);
   if(shots===1&&seen.size>=4){shots++;await p.mouse.move(w/2,h/2);for(let i=0;i<5;i++)await p.mouse.wheel(0,200);await p.waitForTimeout(300);await p.screenshot({path:tag+'_mix.png'})}
 }
 console.log(tag,'errors',errs,'seen',[...seen].join(),await p.evaluate(()=>{const S=__pb();return{wave:S.wave,hp:Math.round(S.hp),plan:JSON.stringify(S.plan.counts)}}));
 await p.close()}
 await b.close();
})();
