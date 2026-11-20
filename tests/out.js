const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1280,height:800}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(800);
 await p.click('#play');await p.locator('.hero').nth(0).click();await p.click('#hgo');await p.waitForTimeout(400);
 await p.evaluate(()=>{const LAND=[[[0,0],[1,0]],[[0,0],[1,0],[0,1]],[[0,0],[1,0],[0,1],[1,1]],[[0,0]]];
   for(let i=0;i<14;i++){const cells=LAND[i%4];__g.choose({id:'land',kind:'chunk',cells,sp:cells.map(()=>null),rar:1,mut:null})}
   for(let i=0;i<10;i++)__g.choose({id:'t',kind:'tower',type:['bolt','cannon','frost','glaive'][i%4],rar:0,mut:null});
   __pb().hp=__pb().maxHp=200;__pb().wave=7});
 for(let i=0;i<8;i++)await p.mouse.wheel(0,300);
 await p.waitForTimeout(600);await p.screenshot({path:'out1.png'});
 await p.click('#next');await p.click('#spd');await p.click('#spd');await p.waitForTimeout(14000);
 const c=p.locator('#draft.on .card');if(await c.count())await c.first().click();
 await p.screenshot({path:'out2.png'});
 console.log(await p.evaluate(()=>JSON.stringify({w:__pb().wave,hp:__pb().hp,paths:__pb().paths.length})),'errors',errs);await b.close();
})();
