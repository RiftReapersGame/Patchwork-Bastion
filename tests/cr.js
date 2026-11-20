const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1280,height:800}});await p.goto('file:///home/claude/bastion/index.html');await p.waitForTimeout(700);
 await p.click('#credbtn');await p.waitForTimeout(300);await p.screenshot({path:'cr.png'});await p.click('#credclose');console.log('closed ok',await p.locator('#play').isVisible());await b.close()})();
