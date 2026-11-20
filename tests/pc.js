const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1210,height:700}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(1500);
 await p.click('#play');await p.waitForTimeout(800);await p.screenshot({path:'pc_sel.png'});
 for(const i of [0,3]){
  if(i){await p.click('#pause');await p.click('#pexit');await p.click('#play')}
  await p.locator('#hcards .hero').nth(i).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(500);
  await p.evaluate(()=>{const e=document.querySelector('#tipskip');e&&e.click();for(let k=0;k<3;k++)__g.choose({id:'land',kind:'chunk',cells:[[0,0],[1,0],[0,1]],sp:[null,null,null],rar:1,mut:null});for(const t of ['bolt','cannon','frost','glaive'])__g.choose({id:'t',kind:'tower',type:t,rar:0,mut:null});__pb().hp=__pb().maxHp=300;__pb().wave=4});
  await p.mouse.move(600,350);for(let k=0;k<3;k++)await p.mouse.wheel(0,-300);
  await p.click('#next');await p.waitForTimeout(6000);await p.screenshot({path:'pc_run'+i+'.png'});
 }
 console.log('errors',errs);await b.close();
})();
