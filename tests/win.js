const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1280,800,'t'],[400,820,'u']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(800);
 await p.click('#play');await p.locator('.hero').nth(0).click();await p.click('#hgo');await p.waitForTimeout(400);
 await p.evaluate(()=>{const S=__pb();S.wave=29;S.hp=S.maxHp=5000;__g.startWave();S.spawnQ.length=1});
 await p.screenshot({path:'win_'+tag+'0.png'});
 await p.evaluate(()=>{const S=__pb();S.spawnQ.length=0;for(const e of S.enemies)e.dead=true;S.enemies.length=0});
 await p.waitForTimeout(3500);
 await p.evaluate(()=>{const S=__pb();for(const e of S.enemies)e.dead=true;S.spawnQ.length=0});await p.waitForTimeout(1500);
 await p.screenshot({path:'win_'+tag+'1.png'});
 console.log(await p.evaluate(()=>__pb().mode));
 await p.click('#wendless');await p.waitForTimeout(800);await p.screenshot({path:'win_'+tag+'2.png'});
 console.log(await p.evaluate(()=>JSON.stringify({m:__pb().mode,e:__pb().endless,w:__pb().wave})));
 console.log(tag,'errors',errs);await p.close()}
 await b.close();
})();
