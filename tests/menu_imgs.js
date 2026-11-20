const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1000,height:700}});
 await p.addInitScript(()=>{window.__used=new Set();const o=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(im,...a){if(im&&im.src)__used.add(im.src.split('/').pop().replace('.png',''));return o.call(this,im,...a)};localStorage.setItem('pb_tut','1');localStorage.setItem('pb_wins',JSON.stringify({'@forest':1,'@forest/easy':1,'@forest/normal':1,'@coast/easy':1,'@coast/normal':1}))});
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForFunction(()=>!document.getElementById('loading'));await p.waitForTimeout(800);
 await p.click('#armbtn');await p.waitForTimeout(300);await p.click('#aback');
 await p.click('#play');await p.waitForTimeout(500);for(let i=0;i<4;i++){await p.locator('#hcards .hero').nth(i).click();await p.waitForTimeout(150)}
 await p.locator('#hcards .more').first().click().catch(()=>{});
 await p.click('#hgo');await p.waitForTimeout(500);for(let i=0;i<3;i++){await p.locator('.dbtn').nth(i).click().catch(()=>{});await p.waitForTimeout(200)}
 console.log(JSON.stringify([...await p.evaluate(()=>[...__used])].sort()));await b.close()})();
