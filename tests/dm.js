const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1280,800,'t'],[400,820,'u']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(800);
 await p.click('#play');await p.locator('.hero').nth(0).click();await p.click('#hgo');await p.waitForTimeout(400);
 await p.evaluate(()=>{for(let i=0;i<4;i++)__g.choose({id:'land',kind:'chunk',cells:[[0,0],[1,0],[0,1]],sp:[null,null,null],rar:1,mut:null});
   for(const t of ['bolt','cannon','frost','glaive','tesla','flame','sniper','lancer'])__g.choose({id:'t',kind:'tower',type:t,rar:0,mut:null});__pb().hp=__pb().maxHp=200;__pb().wave=6});
 await p.screenshot({path:'dm_'+tag+'0.png'});
 await p.click('#next');await p.click('#spd');await p.click('#spd');await p.waitForTimeout(9000);
 const c=p.locator('#draft.on .card');if(await c.count())await c.first().click();await p.waitForTimeout(500);
 await p.screenshot({path:'dm_'+tag+'1.png'});
 await p.click('#dmghead');await p.waitForTimeout(500);await p.screenshot({path:'dm_'+tag+'2.png'});
 console.log(tag,'errors',errs);await p.close()}
 await b.close();
})();
