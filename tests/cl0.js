const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const p=await b.newPage();
p.on('pageerror',e=>console.log('ERR',e.message));p.on('console',m=>{if(m.type()==='error')console.log('CON',m.text().slice(0,200))});
await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(2500);console.log(await p.evaluate(()=>typeof __g));await b.close()})();
