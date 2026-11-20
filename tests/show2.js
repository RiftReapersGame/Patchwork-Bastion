const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1280,800,'t'],[400,820,'u']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(700);
 await p.click('#play');await p.waitForTimeout(400);
 await p.evaluate(()=>{const S=__pb();const types=['bolt','cannon','frost','sniper','tesla','flame','guard','lancer','hex','mint','hall','chapel'];
   // lay a 6x2 block of plots to the right of the castle for a line-up
   let i=0;for(let y=0;y<2;y++)for(let x=0;x<6;x++){const cx=S.base.get([...S.base.keys()][1]);const X=__hub()[0]+2+x*1,Y=__hub()[1]-2+y*-2;const k=X+','+Y;S.base.set(k,{x:X,y:Y,core:false,tower:null,born:-9});const c=S.base.get(k);c.tower={type:types[i],rar:0,mut:null,b:c,cd:0,born:-9,anim:9,flip:false};i++}
 });
 await p.locator('.card').first().click();await p.waitForTimeout(600);
 await p.screenshot({path:tag+'_line.png'});
 console.log(tag,'errors',errs);await p.close()}
 await b.close();
})();
