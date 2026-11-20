const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1280,height:800}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(800);
 await p.click('#msnd');await p.screenshot({path:'mt_title.png'});
 console.log('muted class',await p.evaluate(()=>[document.querySelector('#msnd').className,document.querySelector('#snd').className]));
 await p.click('#mfs');await p.waitForTimeout(300);
 await p.click('#play');await p.waitForTimeout(400);await p.click('#msnd');await p.screenshot({path:'mt_hero.png'});
 await p.locator('.hero').nth(0).click();await p.click('#hgo');await p.waitForTimeout(400);
 console.log('in game visible',await p.locator('#mtools').isVisible(),await p.evaluate(()=>document.querySelector('#snd').className));
 console.log('errors',errs);await b.close();
})();
