const {chromium}=require('/opt/npm-tools/node_modules/playwright');const FB='/home/claude/fbpkg/node_modules/firebase/';
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const p=await b.newPage({viewport:{width:1100,height:700}});
const bad=[];p.on('response',r=>{if(r.url().includes('localhost')&&r.status()>=400)bad.push(r.status()+' '+r.url())});p.on('requestfailed',r=>{if(r.url().includes('localhost'))bad.push('fail '+r.url())});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('https://www.gstatic.com/**',r=>{const f=r.request().url().split('/').pop();r.fulfill({path:FB+f,contentType:'text/javascript'})});
await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(9000);
await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(2).click();await p.waitForTimeout(5000);
console.log(JSON.stringify({bad:bad.slice(0,10),n:bad.length,errs,btnSeenEarlier:true}));await b.close()})();
