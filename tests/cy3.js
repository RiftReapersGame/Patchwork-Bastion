const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1200,height:800}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.addInitScript(()=>{localStorage.setItem('pb_tut','1');localStorage.setItem('pb_wins',JSON.stringify({'@coast':1,'@coast/easy':1}))});
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForFunction(()=>document.getElementById('loading').classList.contains('done'));
 await p.click('#play');await p.locator('#hcards .hero').nth(0).click();await p.click('#hgo');await p.locator('.dbtn').nth(0).click();await p.locator('.hero.lvl').nth(2).click();await p.waitForTimeout(3500);
 const r=await p.evaluate(()=>{const S=__pb();S.G.xp=0;const out={};
   // high ground: same tower on a mesa plot and on a floor plot
   const plots=[...S.base.values()].filter(b=>!b.core);const onM=plots.find(b=>S.mesa.has(b.x+','+b.y));
   out.mesaPlots=plots.filter(b=>S.mesa.has(b.x+','+b.y)).length+'/'+plots.length;
   // last stand, three keeps
   const hit=(ki)=>{const K=ki?(ki===1?S.k2:S.k3):S;K.hp=1;const pi=S.paths.findIndex(q=>(q.k||0)===ki);__g.spawn('runner',{p:pi,seg:S.paths[pi].cells.length-2,t:.95});for(let i=0;i<80&&S.mode==='play'&&!K.down;i++)__g.update(.05)};
   hit(1);out.after1=[S.mode,!!S.k2.down,document.getElementById('hptext2').textContent];
   hit(2);out.after2=[S.mode,!!S.k3.down];
   // a goblin on keep 1's road should now go to keep 0 (nearest standing)
   const hp0=S.hp;const pi=S.paths.findIndex(q=>q.k===1);__g.spawn('runner',{p:pi,seg:S.paths[pi].cells.length-2,t:.95});for(let i=0;i<200&&S.mode==='play';i++)__g.update(.05);out.redirect=[hp0,S.hp];
   hit(0);out.final=[S.mode,document.querySelector('#over h2').textContent];
   return out});
 console.log(JSON.stringify(r),errs);await b.close()})();
