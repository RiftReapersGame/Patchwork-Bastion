const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1200,height:800},deviceScaleFactor:1.5});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(1500);
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(500);
 const pos=await p.evaluate(()=>{const e=document.querySelector('#tipskip');e&&e.click();const S=__pb();
   // put bridge plots on road cells: one on a vertical stretch, one on a horizontal stretch, away from the castle
   const out=[];
   for(const pth of S.paths){const c=pth.cells;let nh=0,nv=0;for(let i=4;i<c.length-8;i++){const [x,y]=c[i],[px2,py2]=c[i-1],[nx,ny]=c[i+1];const k=x+','+y;if(S.base.has(k))continue;
     const horiz=py2===y&&ny===y,vert=px2===x&&nx===x;if(horiz&&nh<2){nh++}else if(vert&&nv<2){nv++}else continue;S.base.set(k,{x,y,core:false,tower:null,born:-9});out.push([x,y]);i+=3}}
   out.forEach(([x,y],i)=>{const c=S.base.get(x+','+y);if(i%2===0)c.tower={type:['bolt','cannon'][i>>1&1],rar:0,mut:null,b:c,cd:0,born:-9,anim:9,flip:false}});
   S.hp=S.maxHp=900;S.wave=6;return out});
 await p.addStyleTag({content:'#hud,#dock,#upbar,#flyout,#dmg,#tip,#banner,#preview,#info{display:none!important}'});
 await p.evaluate(()=>{__g.startWave()});
 await p.evaluate(a=>{const c=__cam?__cam():null},0);await p.mouse.move(600,400);for(let k=0;k<2;k++){await p.mouse.wheel(0,300);await p.waitForTimeout(100)}
 await p.waitForTimeout(6500);await p.screenshot({path:'brg1.png'});await p.waitForTimeout(2500);await p.screenshot({path:'brg2.png'});
 console.log(JSON.stringify(pos),'errors',errs);await b.close();
})();
