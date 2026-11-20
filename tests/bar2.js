const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1280,800,'t'],[400,820,'u']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(800);
 await p.click('#play');await p.locator('.hero').nth(1).click();await p.click('#hgo');await p.waitForTimeout(400);
 await p.evaluate(()=>{const S=__pb();const types=['bolt','cannon','frost','sniper','tesla','oil','guard','dragon','bats','mint','hall','glaive'];
   let i=0;for(let y=0;y<2;y++)for(let x=0;x<6;x++){const X=__hub()[0]+2+x,Y=__hub()[1]-2-y*2;const k=X+','+Y;S.base.set(k,{x:X,y:Y,core:false,tower:null,born:-9});const c=S.base.get(k);c.tower={type:types[i],rar:0,mut:null,b:c,cd:0,born:-9,anim:9,flip:false};i++}
   S.gold=130;__g.upgradeType('core')});
 await p.waitForTimeout(400);await p.screenshot({path:'bar_'+tag+'1.png'});
 await p.locator('.cat').nth(0).click();await p.waitForTimeout(300);await p.screenshot({path:'bar_'+tag+'2.png'});
 await p.locator('.cat').nth(3).click();await p.waitForTimeout(300);await p.mouse.click(tag==='t'?640:200,tag==='t'?330:330);await p.waitForTimeout(300);await p.screenshot({path:'bar_'+tag+'3.png'});
 await p.locator('#flyout .up').first().click();await p.locator('.cat').nth(3).click();await p.waitForTimeout(200);console.log('closed',await p.locator('#flyout').isVisible(),await p.evaluate(()=>JSON.stringify(__pb().tl)));
 console.log(tag,'errors',errs);await p.close()}
 await b.close();
})();
