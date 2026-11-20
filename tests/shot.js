const {chromium}=require('/opt/npm-tools/node_modules/playwright');
const vw=+process.argv[2]||1280,vh=+process.argv[3]||800,tag=process.argv[4]||'d',secs=+process.argv[5]||45;
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:vw,height:vh}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');
 await p.waitForTimeout(900);await p.screenshot({path:tag+'_title.png'});
 await p.click('#play');await p.waitForTimeout(700);await p.screenshot({path:tag+'_draft.png'});
 let shots=0,sped=false;const t0=Date.now();
 while(Date.now()-t0<secs*1000){
   if(await p.locator('#over.on').count())break;
   if(await p.locator('#draft.on .card').count()){await p.waitForTimeout(350);if(shots===2)await p.screenshot({path:tag+'_draft2.png'});await p.locator('#draft.on .card').nth(Math.floor(Math.random()*3)).click({force:true});await p.waitForTimeout(120);continue}
   if(await p.locator('#next.on').count())await p.click('#next',{force:true}).catch(()=>{});
   if(!sped){sped=true;await p.click('#spd');await p.click('#spd')}
   await p.waitForTimeout(700);
   const el=(Date.now()-t0)/1000;
   if(shots<6&&el>4+shots*7){await p.screenshot({path:tag+'_play'+shots+'.png'});shots++}
 }
 await p.waitForTimeout(1600);await p.screenshot({path:tag+'_end.png'});
 console.log('errors',errs,await p.evaluate(()=>{const S=__pb();return{wave:S.wave,lvl:S.level,cells:S.base.size,paths:S.paths.length,mode:S.mode}}));await b.close();
})();
