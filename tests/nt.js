const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1280,height:800}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(700);
 await p.click('#play');await p.waitForTimeout(400);await p.locator('.card').first().click();
 const info=await p.evaluate(()=>{const S=__pb(),h=__hub();S.maxHp=S.hp=500;S.wave=6;
   // put the new towers on plots hugging the first road so they all get work
   const road=S.paths[0].cells.slice(-14,-3);const types=['tnt','echo','exec','catapult','bell','bounty','drums','bolt','cannon'];let i=0,placed=[];
   for(const c of road){for(const d of [[0,-1],[0,1],[1,0],[-1,0]]){const x=c[0]+d[0],y=c[1]+d[1],k=x+','+y;if(S.base.has(k)||S.road.has(k)||(x===h[0]&&y===h[1]+1))continue;if(i>=types.length)break;
     S.base.set(k,{x,y,core:false,tower:null,born:-9});const cell=S.base.get(k);cell.tower={type:types[i++],rar:1,mut:null,b:cell,cd:0,born:-9,anim:9,flip:false};placed.push(k);break}}
   // a bridge plot with an oil gallery
   const rc=S.paths[1].cells[S.paths[1].cells.length-5],rk=rc[0]+','+rc[1];S.base.set(rk,{x:rc[0],y:rc[1],core:false,tower:null,born:-9});const oc=S.base.get(rk);oc.tower={type:'oil',rar:1,mut:null,b:oc,cd:0,born:-9,anim:9,flip:false};
   return placed.length});
 await p.click('#next');await p.click('#spd');await p.click('#spd');
 const seen={fly:0,stun:0,bounty:0,echo:0};
 for(let i=0;i<150;i++){await p.waitForTimeout(300);
   if(await p.locator('#draft.on .card').count()){await p.locator('#draft.on .card').first().click({force:true});continue}
   if(await p.locator('#next.on').count())await p.click('#next',{force:true}).catch(()=>{});
   const r=await p.evaluate(()=>{const S=__pb();return{fly:S.enemies.some(e=>e.fly),stun:S.enemies.some(e=>e.stun>0),bounty:S.enemies.some(e=>e.bounty),echo:[...S.base.values()].some(b=>b.tower&&b.tower.type==='echo'&&b.tower.bind)}});
   for(const k in r)if(r[k])seen[k]++;
   if(i===14)await p.screenshot({path:'nt1.png'});if(i===30)await p.screenshot({path:'nt2.png'})}
 console.log('errors',errs,'placed',info,JSON.stringify(seen),await p.evaluate(()=>{const S=__pb();return{wave:S.wave,gold:Math.floor(S.gold),kills:S.kills}}));
 await b.close();
})();
