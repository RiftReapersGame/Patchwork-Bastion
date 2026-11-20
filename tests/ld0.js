const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1200,height:800}});
 let n=0;await p.route('**/*.png',async r=>{n++;await new Promise(z=>setTimeout(z,300+n*20));await r.continue()});
 p.goto('file:///home/claude/bastion/index.html');
 for(let i=0;i<12;i++){await p.waitForTimeout(250);try{console.log(i*250,n,await p.evaluate(()=>{const t=document.getElementById('ldtxt');return t?t.textContent:'gone'}))}catch(e){console.log('x')}}
 await b.close()})();
