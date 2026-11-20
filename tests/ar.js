const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const errs=[];
 for(const [w,h,tag] of [[1200,800,'d'],[412,860,'m']]){
 const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1.5});p.on('pageerror',e=>errs.push(tag+' '+e.message));
 await p.addInitScript(()=>{if(!localStorage.getItem('pb_tut')){localStorage.setItem('pb_tut','1');localStorage.setItem('pb_crowns','3300')}});
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(1200);
 await p.screenshot({path:'ar_title_'+tag+'.png'});
 await p.click('#armbtn');await p.waitForTimeout(300);await p.screenshot({path:'ar_shop0_'+tag+'.png'});
 for(let k=0;k<25;k++){const bs=p.locator('#alist .big:not([disabled])');if(!await bs.count())break;await bs.first().click()}
 await p.waitForTimeout(200);await p.screenshot({path:'ar_shop1_'+tag+'.png',fullPage:false});
 console.log(tag,'crowns after buying all',await p.evaluate(()=>__g.getCrowns()),await p.evaluate(()=>localStorage.getItem('pb_arm')));
 await p.click('#aback');await p.click('#play');await p.locator('#hcards .hero').nth(1).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(0).click();await p.waitForTimeout(500);
 const st=await p.evaluate(()=>{const S=__pb();return{gold:S.gold,plots:[...S.base.values()].filter(b=>!b.core).length,tw:[...S.base.values()].filter(b=>b.tower&&!b.core).map(b=>b.tower.type),ban:S.banLeft,lock:S.lockLeft,wind:S.wind}});console.log(tag,JSON.stringify(st));
 await p.evaluate(()=>{__pb().wave=3;__g.openDraft(false)});await p.waitForTimeout(500);await p.screenshot({path:'ar_draft_'+tag+'.png'});
 // banish first tower card
 const before=await p.evaluate(()=>__pb().cards.map(c=>c.id));
 await p.click('#banbtn');await p.waitForTimeout(100);await p.screenshot({path:'ar_ban_'+tag+'.png'});
 const ti=before.findIndex(i=>i.startsWith('t_'));await p.locator('#cards .card').nth(ti).click();await p.waitForTimeout(200);
 console.log(tag,'ban',before,await p.evaluate(()=>[__pb().cards.map(c=>c.id),__pb().ban,__pb().banLeft]));
 await p.click('#lockbtn');await p.locator('#cards .card').nth(0).click();await p.waitForTimeout(200);await p.screenshot({path:'ar_lock_'+tag+'.png'});
 const lockId=await p.evaluate(()=>__pb().mark.id);
 await p.locator('#cards .card').nth(1).click();await p.waitForTimeout(200);
 await p.evaluate(()=>__g.openDraft(false));await p.waitForTimeout(300);
 console.log(tag,'locked',lockId,'next draft',await p.evaluate(()=>[__pb().cards.map(c=>c.id),__pb().lockLeft]));await p.screenshot({path:'ar_kept_'+tag+'.png'});
 await p.locator('#cards .card').nth(0).click();
 // second wind + loss
 await p.evaluate(()=>{const S=__pb();S.hp=1;__g.startWave()});
 await p.evaluate(()=>{for(let i=0;i<4000&&__pb().wind;i++)__g.update(.05)});
 console.log(tag,'after wind',await p.evaluate(()=>({hp:__pb().hp,wind:__pb().wind,mode:__pb().mode,en:__pb().enemies.filter(e=>!e.dead).length})));
 await p.waitForTimeout(600);await p.screenshot({path:'ar_wind_'+tag+'.png'});
 await p.evaluate(()=>{const S=__pb();S.wave=12;for(let i=0;i<20000&&S.mode!=='over';i++){S.hp=Math.min(S.hp,1);if(S.mode==='draft')__g.choose(S.cards[0]);if(S.between)__g.startWave();__g.update(.05)}});
 await p.waitForTimeout(1800);await p.screenshot({path:'ar_over_'+tag+'.png'});
 console.log(tag,'end',await p.evaluate(()=>({cr:__pb().cr,cs:__pb().cs,crowns:__g.getCrowns(),line:document.getElementById('ocr').textContent})));
 await p.close()}
 console.log('errors',errs);await b.close()})();
