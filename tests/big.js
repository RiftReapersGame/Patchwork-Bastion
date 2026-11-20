const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 for(const [w,h,tag] of [[1210,575,'t'],[400,820,'u']]){
 const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(900);
 let all=[];
 for(let r=0;r<6;r++){
  await p.click('#play');await p.locator('#hcards .hero').nth(r%4).click();await p.click('#hgo');await p.locator('.hero.lvl').nth(1).click();await p.waitForTimeout(250);
  const L=await p.evaluate(()=>{const S=__pb();for(let i=0;i<6;i++){S.wave=[3,5,8,11,14,18][i];}return 0});
  // open all later paths by playing the wave counter forward through the game's own hook
  const lens=await p.evaluate(()=>{const S=__pb();return S.paths.map(q=>q.cells.length)});all=all.concat(lens);
  if(r===0){await p.screenshot({path:'big_'+tag+'.png'})}
  await p.click('#pause');await p.click('#pexit');}
 console.log(tag,'start path lengths',all.join(' '),'min',Math.min(...all),errs);await p.close()}
 await b.close();
})();
