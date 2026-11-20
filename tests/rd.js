const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const errs=[];
 for(const [w,h,lv] of [[1200,800,0],[800,1200,0],[1200,800,1]]){const all=[];let fb=0;
 for(let r=0;r<6;r++){
 const p=await b.newPage({viewport:{width:w,height:h}});p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>{localStorage.setItem('pb_wins',JSON.stringify({'@forest':1,'@forest/easy':1,'@forest/normal':1,'@coast/easy':1}));localStorage.setItem('pb_tut','1')});
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(900);
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(lv).click();await p.waitForTimeout(400);
 const L=await p.evaluate(()=>{for(let i=0;i<6;i++)__g.addPath();const P=__pb().paths;const seen=new Set();let dup=0;for(const q of P){const k=q.cells[0]+'';if(seen.has(k))dup++;seen.add(k)}return [P.map(q=>q.cells.length),dup]});
 all.push(...L[0]);fb+=L[1];if(r==0)await p.screenshot({path:'rd'+w+lv+'.png'});await p.close()}
 all.sort((a,b)=>a-b);console.log(w,h,lv,'min',all[0],'med',all[all.length>>1],'max',all[all.length-1],'n',all.length,'fallbackDup',fb)}
 console.log(errs);await b.close()})();
