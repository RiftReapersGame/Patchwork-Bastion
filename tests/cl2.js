const {chromium}=require('/opt/npm-tools/node_modules/playwright');const FB='/home/claude/fbpkg/node_modules/firebase/';
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
for(const [w,h] of [[640,360],[360,740]]){const p=await b.newPage({viewport:{width:w,height:h}});
 await p.route('https://www.gstatic.com/**',r=>{const f=r.request().url().split('/').pop();r.fulfill({path:FB+f,contentType:'text/javascript'})});
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(3500);
 console.log(w,h,await p.evaluate(()=>{const t=document.getElementById('title'),a=document.getElementById('gin').getBoundingClientRect();return {sh:t.scrollHeight,ch:t.clientHeight,btnBottom:Math.round(a.bottom)}}));
 await p.screenshot({path:'cl_'+w+'.png'});await p.close()}
await b.close()})();
