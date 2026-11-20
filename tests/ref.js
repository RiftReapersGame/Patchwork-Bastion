const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1500,height:900},deviceScaleFactor:1});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///tmp/refb/index.html');await p.waitForTimeout(1500);
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(400);
 await p.evaluate(()=>{
  const {HEROES,HERO,TOWERS,T,E,M,IMG,drawArt,drawHeroCard}=__x;
  const root=document.createElement('div');root.id='ref';root.style.cssText='position:fixed;inset:0;z-index:9999;background:#f4ecd6;overflow:auto;padding:14px;font:700 13px sans-serif;color:#2b2233';
  const sec=(title)=>{const h=document.createElement('h2');h.textContent=title;h.style.cssText='margin:10px 0 6px;font:800 20px sans-serif;width:100%';root.appendChild(h);const d=document.createElement('div');d.style.cssText='display:flex;flex-wrap:wrap;gap:8px';root.appendChild(d);return d};
  const cell=(box,label,w=128)=>{const c=document.createElement('div');c.style.cssText='width:'+w+'px;text-align:center;background:#fff8e4;border:2px solid #2b2233;border-radius:8px;padding:4px';const cv=document.createElement('canvas');cv.style.cssText='width:'+(w-8)+'px;height:'+(w-8)+'px;image-rendering:pixelated';c.appendChild(cv);const l=document.createElement('div');l.textContent=label;c.appendChild(l);box.appendChild(c);return cv};
  let s=sec('Hero castles (4)');for(const h of HEROES){const cv=cell(s,HERO[h].name+' castle',190);drawHeroCard(cv,h);cv.style.height='146px'}
  s=sec('Towers (33)');for(const t of TOWERS){const fam=HEROES.find(h=>HERO[h].fam.includes(t));drawArt(cell(s,T[t].name),{kind:'tower',type:t,rar:0,mut:null})}
  s=sec('Goblins (9)');for(const k of Object.keys(E)){const cv=cell(s,E[k].name);cv.width=cv.height=160;const c=cv.getContext('2d');c.imageSmoothingEnabled=false;const m=M[E[k].spr],im=IMG[E[k].spr],sc=Math.min(150/m.w,150/m.h);c.drawImage(im,0,0,m.w,m.h,80-m.w*sc/2,80-m.h*sc/2,m.w*sc,m.h*sc)}
  s=sec('Flying creatures (8)');const fl=TOWERS.filter(t=>T[t].fly).map(t=>[T[t].name,T[t].fly.spr]);fl.push(['Sky wyrm (Warden)','f_wyrm']);
  for(const [n,sp] of fl){const cv=cell(s,n);cv.width=cv.height=160;const c=cv.getContext('2d');c.imageSmoothingEnabled=false;const im=IMG[sp],m=M[sp];let sx=0,sy=0,w,h;if(m){w=m.w;h=m.h}else{w=im.naturalWidth/3;h=im.naturalHeight/4;sy=h*2}const sc=Math.min(150/w,150/h);c.drawImage(im,sx,sy,w,h,80-w*sc/2,80-h*sc/2,w*sc,h*sc)}
  s=sec('Scenery and ground');for(const n of ['tree1','tree2','tree3','bush','rock1','rock3','wrock1','camp','sheep','grass','road','sand','base','wall']){if(!IMG[n])continue;const cv=cell(s,n);cv.width=cv.height=160;const c=cv.getContext('2d');c.imageSmoothingEnabled=false;const im=IMG[n],m=M[n]||{w:im.naturalWidth,h:im.naturalHeight};const w=Math.min(m.w,im.naturalWidth),h=Math.min(m.h,im.naturalHeight),sc=Math.min(150/w,150/h);c.drawImage(im,0,0,w,h,80-w*sc/2,80-h*sc/2,w*sc,h*sc)}
  document.body.appendChild(root);
 });
 await p.waitForTimeout(500);
 const h=await p.evaluate(()=>document.querySelector('#ref').scrollHeight);await p.setViewportSize({width:1500,height:Math.min(h+10,4000)});await p.waitForTimeout(300);
 await p.screenshot({path:'reference_sheet.png'});console.log(h,errs);await b.close();
})();
