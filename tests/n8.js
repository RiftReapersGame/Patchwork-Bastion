const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1280,height:800}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(700);
 await p.click('#play');await p.waitForTimeout(400);
 await p.evaluate(()=>{const S=__pb();const types=['repeater','ballista','glaive','blowpipe','gale','quake','obelisk','star'];
   let i=0;for(let y=0;y<2;y++)for(let x=0;x<4;x++){const X=__hub()[0]+(y?-5+x:2+x),Y=__hub()[1]-1;const k=X+','+Y;S.base.set(k,{x:X,y:Y,core:false,tower:null,born:-9});const c=S.base.get(k);c.tower={type:types[i],rar:0,mut:null,b:c,cd:0,born:-9,anim:9,flip:false};i++}
   S.wave=11;S.hp=S.maxHp=400;
 });
 await p.locator('.card').first().click();await p.waitForTimeout(500);
 await p.screenshot({path:'n8_0.png'});await p.click('#next');await p.click('#spd');
 for(let i=1;i<=4;i++){await p.waitForTimeout(i==1?7000:4000);
   await p.evaluate(()=>{const d=document.querySelector('#draft.on,.draft.on');});
   const c=p.locator('.card');if(await c.count()&&await c.first().isVisible().catch(()=>0))await c.first().click().catch(()=>{});
   await p.screenshot({path:'n8_'+i+'.png'})}
 console.log(await p.evaluate(()=>JSON.stringify({d:__pb().dealt,w:__pb().wave,hp:__pb().hp})));
 const tb=p.locator('#upbar');await tb.screenshot({path:'n8_bar.png'});
 console.log('errors',errs);await b.close();
})();
