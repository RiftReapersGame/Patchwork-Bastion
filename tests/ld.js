const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1200,height:800}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 let n=0;await p.route('**/assets/*.png',async r=>{n++;await new Promise(z=>setTimeout(z,300+n*20));await r.continue()});
 await p.addInitScript(()=>localStorage.setItem('pb_tut','1'));
 const t0=Date.now();p.goto('file:///home/claude/bastion/index.html').catch(()=>{});await p.waitForTimeout(1500);await p.screenshot({path:'ld1.png'});
 await p.waitForFunction(()=>!document.getElementById('loading'),null,{timeout:20000});console.log('loaded in',Date.now()-t0,'ms; images fetched',n);
 await p.click('#play');await p.locator('#hcards .hero').nth(2).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(500);
 await p.screenshot({path:'ld2.png'});
 await p.evaluate(()=>{const S=__pb();document.getElementById('draft').classList.remove('on');S.mode='play';for(const t of ['dragon','bats','angel','imp','phoenix']){const free=[...S.base.values()].find(b=>!b.core&&!b.tower);if(free)free.tower={type:t,rar:0,mut:null,b:free,cd:0,born:-9,anim:9,flip:false}}
   for(const t of ['grunt','runner','swarm','tank','brute','shaman','nest','goldie','boss'])__g.spawn(t,{p:0,seg:2,t:.5});for(let i=0;i<200;i++)__g.update(.05)});
 await p.waitForTimeout(800);await p.screenshot({path:'ld3.png'});console.log(errs);await b.close()})();
