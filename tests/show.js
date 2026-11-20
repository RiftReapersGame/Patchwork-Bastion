const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1280,height:800}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(700);
 await p.click('#play');await p.waitForTimeout(400);await p.locator('.card').first().click();
 await p.evaluate(()=>{const S=__pb();S.level=40;S.gold=900;S.wave=5;
   const types=['guard','lancer','hex','mint','hall','chapel','tesla','bolt'],muts=[null,'twin','venom','blessed',null,null,'far','gilded'];let i=0;
   const cells=[...S.base.values()].filter(b=>!b.core);
   const sps=['power','reach','haste',null];
   for(const c of cells){c.sp=sps[i%4];c.tower={type:types[i%8],rar:i%5,mut:muts[i%8],b:c,cd:0,born:-9,anim:9,flip:false};i++}
 });
 await p.click('#next');await p.waitForTimeout(6500);await p.screenshot({path:'sh1.png'});
 const c=await p.evaluate(()=>{const S=__pb(),k=__cam();const b=[...S.base.values()].find(b=>b.tower&&b.tower.mut);return[k.ox+(b.x+.5)*k.cs,k.oy+(b.y+.5)*k.cs]});await p.mouse.click(c[0],c[1]);await p.waitForTimeout(300);
 await p.screenshot({path:'sh2.png',clip:{x:0,y:440,width:700,height:360}});
 await p.click('#spd');await p.click('#spd');
 for(let i=0;i<60;i++){if(await p.locator('#draft.on .card').count()){await p.waitForTimeout(500);await p.screenshot({path:'sh3.png'});break}await p.waitForTimeout(500)}
 await p.click('#reroll').catch(()=>{});await p.waitForTimeout(500);await p.screenshot({path:'sh4.png'});
 console.log('errors',errs);await b.close();
})();
