const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1280,height:800}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(700);
 await p.click('#play');await p.waitForTimeout(400);await p.locator('.card').first().click();
 await p.evaluate(()=>{const S=__pb();S.maxHp=S.hp=500;
   const cs=S.paths[0].cells,n=cs.length;const add=(c,t)=>{const k=c[0]+','+c[1];S.base.set(k,{x:c[0],y:c[1],core:false,tower:null,born:-9});const cell=S.base.get(k);if(t)cell.tower={type:t,rar:0,mut:null,b:cell,cd:0,born:-9,anim:9,flip:false}};
   const m=Math.floor(n/2);add(cs[m],null);add(cs[m+1],'bolt');add(cs[m+3],null);S.gold=0;
   // a plain plot beside the road so the bridge joins something
   const c=cs[m];for(const d of[[0,-1],[0,1],[1,0],[-1,0]]){const k=(c[0]+d[0])+','+(c[1]+d[1]);if(!S.base.has(k)&&!S.road.has(k)){S.base.set(k,{x:c[0]+d[0],y:c[1]+d[1],core:false,tower:null,born:-9});break}}
   window.__bx=cs[m+1]});
 await p.setViewportSize({width:1281,height:800});await p.waitForTimeout(200);await p.click('#next');await p.click('#spd');
 const k=await p.evaluate(()=>{const k=__cam(),c=window.__bx;return[k.ox+(c[0]+.5)*k.cs,k.oy+(c[1]+.5)*k.cs]});
 const clip={x:Math.max(0,Math.min(620,k[0]-330)),y:Math.max(0,Math.min(320,k[1]-250)),width:660,height:480};
 for(let i=0;i<60;i++){await p.waitForTimeout(300);if(await p.locator('#draft.on .card').count()){await p.locator('#draft.on .card').first().click({force:true});continue}
   const near=await p.evaluate(()=>{const S=__pb(),c=window.__bx;return S.enemies.some(e=>Math.hypot(e.x-c[0]-.5,e.y-c[1]-.5)<1.6)});if(near)break}
 await p.screenshot({path:'br2.png',clip});
 console.log('errors',errs);await b.close();
})();
