const {chromium}=require('/opt/npm-tools/node_modules/playwright');
const FB='/home/claude/fbpkg/node_modules/firebase/';
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const out={};
 // 1. real Firebase files served locally: the button should appear
 {const p=await b.newPage({viewport:{width:1100,height:700}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.route('https://www.gstatic.com/**',r=>{const f=r.request().url().split('/').pop();r.fulfill({path:FB+f,contentType:'text/javascript',headers:{'access-control-allow-origin':'*'}})});
  await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(4000);
  out.real={state:await p.evaluate(()=>__g.cloud.state),btn:await p.locator('#gin').count(),errs};
  await p.screenshot({path:'cl_title.png'});await p.close()}
 // 2. Firebase blocked (like the claude.ai page): nothing shows, no errors
 {const p=await b.newPage({viewport:{width:1100,height:700}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.route('https://www.gstatic.com/**',r=>r.abort());
  await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(3000);
  out.blocked={state:await p.evaluate(()=>__g.cloud.state),html:await p.evaluate(()=>document.getElementById('acct').innerHTML),errs};await p.close()}
 // 3. sync logic with a stand-in account
 const ctx=await b.newContext({viewport:{width:1100,height:700}});
 await ctx.route('https://www.gstatic.com/**',r=>r.abort());
 await ctx.addInitScript(()=>{localStorage.setItem('pb_tut','1');
  const fake={onUser(cb){setTimeout(()=>cb(localStorage.getItem('fk_user')?{uid:localStorage.getItem('fk_user'),displayName:'Test Player'}:null),50);fake.cb=cb},
   async signIn(){localStorage.setItem('fk_user','U1');fake.cb({uid:'U1',displayName:'Test Player'})},async signOut(){localStorage.removeItem('fk_user');fake.cb(null)},
   async readT(uid){const v=localStorage.getItem('fk_cloud_'+uid);return v?JSON.parse(v).t:null},async read(uid){const v=localStorage.getItem('fk_cloud_'+uid);return v?JSON.parse(v):null},async write(uid,rec){localStorage.setItem('fk_cloud_'+uid,JSON.stringify(rec));fake.writes=(fake.writes||0)+1}};
  window.__fake=fake;const t=setInterval(()=>{if(window.__g&&__g.cloud.state==='none'){clearInterval(t);__g.cloudStart(fake)}},100)});
 const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 const go=async()=>{await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(3200)};
 await go();try{
 // a) device has progress, account empty -> sign in uploads it
 await p.evaluate(()=>{localStorage.setItem('pb_crowns','250');localStorage.setItem('pb_best','12')});
 await p.click('#gin');await p.waitForTimeout(800);
 out.a={cloud:await p.evaluate(()=>JSON.parse(localStorage.getItem('fk_cloud_U1')).d),ui:await p.locator('#acct').innerText()};
 await p.screenshot({path:'cl_signed.png'});
 // b) a change on the device uploads a few seconds later
 await p.evaluate(()=>localStorage.setItem('pb_crowns','300'));await p.waitForTimeout(3500);
 out.b=await p.evaluate(()=>JSON.parse(localStorage.getItem('fk_cloud_U1')).d.pb_crowns);
 // c) another device moved ahead (account newer, device unchanged) -> device takes the account's progress after reload
 await p.evaluate(()=>{const r=JSON.parse(localStorage.getItem('fk_cloud_U1'));r.t=Date.now()-3;r.d.pb_crowns='900';localStorage.setItem('fk_cloud_U1',JSON.stringify(r))});
 await go();await p.waitForTimeout(1500);
 out.c={crowns:await p.evaluate(()=>localStorage.getItem('pb_crowns')),shown:await p.locator('#armn').innerText()};
 // d) both changed -> the keep-which question
 await p.evaluate(()=>{const r=JSON.parse(localStorage.getItem('fk_cloud_U1'));r.t=Date.now()-7;r.d.pb_crowns='1500';localStorage.setItem('fk_cloud_U1',JSON.stringify(r));localStorage.setItem('pb_crowns','950')});
 await go();await p.waitForTimeout(800);
 out.d={dialog:await p.locator('#cloudq.on').count(),dev:await p.locator('#cqdev').innerText(),acc:await p.locator('#cqacc').innerText()};
 out.dbg=await p.evaluate(()=>({sync:localStorage.getItem('pb_sync'),mt:localStorage.getItem('pb_mt'),cr:localStorage.getItem('pb_crowns'),rec:JSON.parse(localStorage.getItem('fk_cloud_U1')).t,st:__g.cloud.state,user:!!__g.cloud.user,msg:__g.cloud.msg,pend:__g.cloud.pend!==undefined,title:document.getElementById('title').className}));console.log(JSON.stringify(out,null,1));
 await p.screenshot({path:'cl_q.png'});
 await p.click('#cqdev');await p.waitForTimeout(600);
 out.d.after=await p.evaluate(()=>JSON.parse(localStorage.getItem('fk_cloud_U1')).d.pb_crowns);
 // e) sign out keeps the device save
 await p.click('#gout');await p.waitForTimeout(400);
 out.e={crowns:await p.evaluate(()=>localStorage.getItem('pb_crowns')),btn:await p.locator('#gin').count()};
 // f) play a run while signed in: no errors, run save reaches the account
 await p.click('#gin');await p.waitForTimeout(600);
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(3000);
 await p.evaluate(()=>{for(let i=0;i<2500&&__pb().mode==='play';i++)__g.update(.05)});await p.evaluate(()=>{document.getElementById('psave').click()});out.pmsg=await p.locator('#pmsg').innerText();await p.waitForTimeout(3500);
 out.f=await p.evaluate(()=>{const r=JSON.parse(localStorage.getItem('fk_cloud_U1'));return {hasRun:!!r.d.pb_save,localRun:!!localStorage.getItem('pb_save'),wave:__pb().wave,mode:__pb().mode,sync:localStorage.getItem('pb_sync'),mt:localStorage.getItem('pb_mt'),msg:__g.cloud.msg,hold:__g.cloud.hold,pend:__g.cloud.pend!==undefined,kb:Math.round(JSON.stringify(r).length/1024)}});
 }catch(e){out.fail=e.message.slice(0,200)}
 out.errs=errs;console.log(JSON.stringify(out,null,1));await b.close()})();
