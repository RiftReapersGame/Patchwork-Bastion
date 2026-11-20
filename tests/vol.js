const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox','--autoplay-policy=no-user-gesture-required']});
for(const [w,h] of [[1100,700],[640,360],[390,800]]){const p=await b.newPage({viewport:{width:w,height:h}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>localStorage.setItem('pb_tut','1'));
await p.goto('http://localhost:8766/index.html');await p.waitForTimeout(3500);
await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(2500);
await p.click('#pause');await p.waitForTimeout(400);
await p.locator('#vmus').fill('40');await p.locator('#vsfx').fill('70');await p.waitForTimeout(1500);
const r=await p.evaluate(()=>({mus:localStorage.getItem('pb_vmus'),sfx:localStorage.getItem('pb_vsfx'),vols:Object.fromEntries(Object.entries(__g.MUS).map(([k,a])=>[k,+a.volume.toFixed(3)])),txt:[document.getElementById('vmuso').textContent,document.getElementById('vsfxo').textContent]}));
await p.screenshot({path:'/home/claude/t/vol_'+w+'.png'});
console.log(w,h,JSON.stringify(r),errs);await p.close()}
await b.close()})();
