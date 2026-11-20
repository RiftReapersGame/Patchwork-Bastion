const {chromium}=require('/opt/npm-tools/node_modules/playwright');
const sizes=(process.env.SZ||'664x655,360x700,700x360,560x980,900x560,1280x800').split(',').map(s=>s.split('x').map(Number));
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const errs=[];
 for(const [w,h] of sizes){
 const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1.5});p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>localStorage.setItem('pb_tut','1'));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForFunction(()=>!document.getElementById('loading'));
 await p.click('#play');await p.locator('#hcards .hero').nth(1).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(400);
 await p.evaluate(()=>{const S=__pb();document.getElementById('draft').classList.remove('on');S.mode='play';S.gold=500;S.wave=3;for(const t of ['cannon','guard','bolt','tesla'])__g.choose({id:'t',kind:'tower',type:t,rar:0,mut:null});document.getElementById('draft').classList.remove('on');S.mode='play';S.plan.counts={grunt:9,runner:4,tank:2,brute:1}; try{__g.renderPreview&&__g.renderPreview()}catch(e){}});
 await p.addStyleTag({content:'*{font-family:"DejaVu Sans",sans-serif!important}.cat em,.up em{font-size:13px!important}.up{height:96px!important}.cat{height:64px!important}.pill{height:54px!important}'});await p.waitForTimeout(3200);
 // overlap report between the main HUD boxes
 const r=await p.evaluate(()=>{const q=s=>[...document.querySelectorAll(s)].filter(e=>e.offsetParent!==null).map(e=>{const r=e.getBoundingClientRect();return {s,l:r.left,t:r.top,r:r.right,b:r.bottom}});
   const boxes=[...q('#lefthud>*'),...q('#wavebox'),...q('#preview'),...q('#righthud>*'),...q('#dmg'),...q('#upbar'),...q('#dock>button'),...q('#dock>div:not(#upbar):not(#flyout)')];const out=[];
   for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){const a=boxes[i],c=boxes[j];if(a.l<c.r-1&&c.l<a.r-1&&a.t<c.b-1&&c.t<a.b-1)out.push(a.s+' x '+c.s)}
   const u=document.getElementById('upbar');return {over:out,upScroll:u.scrollHeight>u.clientHeight+2,off:boxes.filter(b=>b.b>innerHeight+1||b.r>innerWidth+1||b.l<-1||b.t<-1).map(b=>b.s)}});
 console.log(w+'x'+h,JSON.stringify(r));await p.screenshot({path:'uif_'+w+'x'+h+'.png'});await p.close()}
 console.log(errs);await b.close()})();
