const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const ctx=await b.newContext({viewport:{width:1100,height:700}});await ctx.route('https://www.gstatic.com/**',r=>r.abort());
 await ctx.addInitScript(()=>{localStorage.setItem('pb_tut','1');localStorage.setItem('pb_crowns','420');
  const fake={onUser(cb){fake.cb=cb;setTimeout(()=>cb(localStorage.getItem('fk_user')?{uid:'U1',displayName:'Test Player'}:null),50)},
   async signIn(){localStorage.setItem('fk_user','U1');fake.cb({uid:'U1',displayName:'Test Player'})},async signOut(){localStorage.removeItem('fk_user');fake.cb(null)},
   async readT(u){const v=localStorage.getItem('fk_cloud_'+u);return v?JSON.parse(v).t:null},async read(u){const v=localStorage.getItem('fk_cloud_'+u);return v?JSON.parse(v):null},
   async write(u,r){localStorage.setItem('fk_cloud_'+u,JSON.stringify(r))},async wipe(u){localStorage.removeItem('fk_cloud_'+u)},async removeUser(){localStorage.removeItem('fk_user');fake.cb(null)}};
  const t=setInterval(()=>{if(window.__g&&__g.cloud.state==='none'){clearInterval(t);__g.cloudStart(fake)}},100)});
 const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(3200);
 await p.click('#privbtn');await p.waitForTimeout(300);await p.screenshot({path:'cl_priv.png'});await p.click('#privclose');
 await p.click('#gin');await p.waitForTimeout(800);const had=await p.evaluate(()=>!!localStorage.getItem('fk_cloud_U1'));
 await p.click('#gdel');await p.waitForTimeout(200);await p.screenshot({path:'cl_del.png'});await p.click('#cdgo');await p.waitForTimeout(600);
 const r=await p.evaluate(()=>({cloud:localStorage.getItem('fk_cloud_U1'),user:!!__g.cloud.user,local:localStorage.getItem('pb_crowns'),ui:document.getElementById('acct').innerText}));
 await p.screenshot({path:'cl_after.png'});
 const p2=await b.newPage({viewport:{width:640,height:360}});await p2.goto('file:///home/claude/bastion/index.html');await p2.waitForTimeout(2500);await p2.click('#privbtn');await p2.waitForTimeout(300);await p2.screenshot({path:'cl_priv_s.png'});
 console.log(JSON.stringify({had,r,errs}));await b.close()})();
