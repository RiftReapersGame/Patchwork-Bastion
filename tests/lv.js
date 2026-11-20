const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1210,756,'t'],[400,820,'u']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(900);
 await p.click('#play');await p.locator('.hero').nth(2).click();await p.click('#hgo');await p.waitForTimeout(500);
 await p.screenshot({path:'lv_'+tag+'0.png'});
 await p.locator('.hero.lvl').nth(1).click();await p.waitForTimeout(600);
 for(let i=0;i<8;i++)await p.mouse.wheel(0,300);await p.waitForTimeout(500);
 await p.screenshot({path:'lv_'+tag+'1.png'});
 await p.evaluate(()=>{for(let i=0;i<6;i++)__g.choose({id:'land',kind:'chunk',cells:[[0,0],[1,0],[0,1]],sp:[null,null,null],rar:1,mut:null});
   for(const t of ['bolt','cannon','frost','glaive'])__g.choose({id:'t',kind:'tower',type:t,rar:0,mut:null});__pb().hp=__pb().maxHp=200;__pb().wave=3});
 await p.click('#next');await p.click('#spd');await p.click('#spd');await p.waitForTimeout(1500);await p.screenshot({path:'lv_'+tag+'2.png'});
 await p.waitForTimeout(9000);const c=p.locator('#draft.on .card');if(await c.count())await c.first().click();
 for(let i=0;i<5;i++)await p.mouse.wheel(0,-300);await p.waitForTimeout(500);
 await p.screenshot({path:'lv_'+tag+'3.png'});
 console.log(tag,await p.evaluate(()=>JSON.stringify({map:__pb().map,land:__pb().land.size,paths:__pb().paths.map(q=>q.cells.length),tide:__pb().tide,w:__pb().wave})),'errors',errs);await p.close()}
 await b.close();
})();
