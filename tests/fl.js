const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1280,height:800}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(700);
 await p.click('#play');await p.waitForTimeout(400);await p.locator('.card').first().click();
 await p.evaluate(()=>{const S=__pb(),h=__hub();S.maxHp=S.hp=30;S.wave=7;S.gold=0;
   const types=['dragon','phoenix','pegasus','imp','bats','drake','angel','bolt','bolt'];let i=0;
   for(let x=-4;x<=4;x++){const X=h[0]+x,Y=h[1]-2,k=X+','+Y;if(S.base.has(k)||S.road.has(k))continue;if(i>=types.length)break;S.base.set(k,{x:X,y:Y,core:false,tower:null,born:-9});const c=S.base.get(k);c.tower={type:types[i++],rar:1,mut:null,b:c,cd:0,born:-9,anim:9,flip:false}}});
 await p.setViewportSize({width:1281,height:800});await p.waitForTimeout(300);
 await p.click('#next');await p.click('#spd');
 let shots=0,saved=false;
 for(let i=0;i<150;i++){await p.waitForTimeout(300);
   if(await p.locator('#draft.on .card').count()){await p.locator('#draft.on .card').first().click({force:true});continue}
   if(await p.locator('#next.on').count())await p.click('#next',{force:true}).catch(()=>{});
   const st=await p.evaluate(()=>{const S=__pb();return{n:S.enemies.length,pools:S.pools.length,ash:[...S.base.values()].some(c=>c.tower&&c.tower.ashes>0),hp:S.hp,mode:S.mode,wave:S.wave}});
   if(shots===0&&st.n>4){await p.waitForTimeout(2500);await p.screenshot({path:'fl1.png'});shots=1}
   if(shots===1&&st.pools>0){await p.screenshot({path:'fl2.png'});shots=2}
   if(st.ash&&!saved){saved=true;await p.screenshot({path:'fl3.png'})}
   if(shots===2&&i===60){await p.evaluate(()=>{__pb().hp=3})}
   if(st.mode==='over')break}
 await p.click('#home').catch(()=>{});
 console.log('errors',errs,'phoenix saved:',saved,await p.evaluate(()=>{const S=__pb();return{wave:S.wave,hp:S.hp,dealt:JSON.stringify(Object.fromEntries(Object.entries(S.dealt||{}).map(([k,v])=>[k,Math.round(v)])))}}));
 await b.close();
})();
