const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox','--autoplay-policy=no-user-gesture-required']});
const p=await b.newPage({viewport:{width:390,height:800}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///home/claude/coin/picker.html');
for(const el of await p.locator('button[data-f]').all()){await el.click();await p.waitForTimeout(60)}
await p.waitForTimeout(800);const bad=await p.locator('text=Can\'t play').count();
await p.screenshot({path:'/home/claude/t/coinp.png'});console.log({errs,bad});await b.close()})();
