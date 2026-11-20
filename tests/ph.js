const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1280,height:800}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(800);
 await p.click('#play');await p.locator('.hero').nth(2).click();await p.click('#hgo');await p.waitForTimeout(400);
 await p.evaluate(()=>{__g.choose({id:'t',kind:'tower',type:'phoenix',rar:0,mut:null});__pb().wave=4;__pb().hp=__pb().maxHp=60});
 for(let i=0;i<3;i++)await p.mouse.wheel(0,-300);
 await p.click('#next');await p.waitForTimeout(7000);await p.screenshot({path:'ph1.png'});
 await p.evaluate(()=>{__pb().hp=3;const S=__pb();for(const e of S.enemies){e.seg=S.paths[e.p].cells.length-2;e.t=.9}});
 await p.waitForTimeout(450);await p.screenshot({path:'ph2.png'});
 await p.waitForTimeout(1500);await p.screenshot({path:'ph3.png'});
 await p.evaluate(()=>{const S=__pb();for(const c of S.base.values())if(c.tower&&c.tower.type==='phoenix'){c.tower.ashes=1}S.spawnQ.length=0;for(const e of S.enemies)e.dead=true});
 await p.waitForTimeout(700);const c=p.locator('#draft.on .card');if(await c.count())await c.first().click();await p.waitForTimeout(250);
 await p.screenshot({path:'ph4.png'});
 console.log(await p.evaluate(()=>JSON.stringify({hp:__pb().hp})),'errors',errs);await b.close();
})();
