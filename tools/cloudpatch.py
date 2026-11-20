import sys
p='/home/claude/pipe/index.src.html';s=open(p).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:60],s.count(a));s=s.replace(a,b)
G='<svg class="gg" viewBox="0 0 48 48" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>'
# markup: account area on title, and the keep-which dialog
rep('Credits</button></div></div>','Credits</button></div><div id="acct"></div></div>\n  <div class="screen" id="cloudq"><div class="panel"><h2>Which progress do you want to keep?</h2><p style="margin:4px 0 6px;color:var(--ink);text-shadow:none;font-size:15px">This device and your Google account have different progress. The one you don\'t keep is replaced.</p><button class="big alt cq" id="cqdev"></button><button class="big alt cq" id="cqacc"></button></div></div>')
# styles
rep('  .screen{position:absolute;','  #acct{margin-top:16px;display:flex;flex-direction:column;align-items:center;gap:6px;min-height:0}#acct:empty{display:none}\n  #acct .gbtn{display:inline-flex;align-items:center;gap:10px;background:#fff;font-size:16px;padding:7px 16px 10px;box-shadow:0 5px 0 var(--navy),inset 0 -5px 0 #dfe3ea}\n  .gg{width:20px;height:20px;flex:none}\n  #acct .anote{font-size:13.5px;font-weight:800;max-width:340px;line-height:1.35}\n  #acct .alink{background:none;border:0;padding:2px 6px;color:inherit;font:inherit;font-size:13.5px;font-weight:900;text-decoration:underline;cursor:pointer}\n  #cloudq{z-index:45}#cloudq .panel{gap:10px}.cq{width:100%;text-align:left;font-size:15px!important;line-height:1.3;padding:9px 14px 12px!important}.cq b{display:block;font-size:17px}\n  .screen{position:absolute;')
JS=r'''
/* ---------- cloud save: Google sign-in with Firebase. The device save stays the main save; the account holds a copy. ---------- */
const FBV='13.4.0',FBC={apiKey:"AIzaSyAqO2KcVfim5mhrrXNth2-2XbuulMZzj20",authDomain:"patchwork-bastion.firebaseapp.com",databaseURL:"https://patchwork-bastion-default-rtdb.firebaseio.com",projectId:"patchwork-bastion",storageBucket:"patchwork-bastion.firebasestorage.app",messagingSenderId:"794433346508",appId:"1:794433346508:web:c5563008630423139a9b69"};
const SYNC=['pb_save','pb_crowns','pb_arm','pb_bank','pb_best','pb_wins','pb_tut','pb_diff','pb_mute','pb_dmg'];
const cloud={api:null,user:null,state:'off',msg:'',hold:false,pend:undefined,timer:0,saving:false};
const SP=Storage.prototype,rawSet=SP.setItem,rawDel=SP.removeItem;
function lsGet(k){try{return localStorage.getItem(k)}catch(e){return null}}
function lsRaw(k,v){try{v==null?rawDel.call(localStorage,k):rawSet.call(localStorage,k,String(v))}catch(e){}}
function touched(k,old,v){if(SYNC.includes(k)&&old!==v){lsRaw('pb_mt',Date.now());cloudSoon()}}
SP.setItem=function(k,v){const old=this===localStorage?this.getItem(k):null;rawSet.call(this,k,v);if(this===localStorage)touched(k,old,String(v))};
SP.removeItem=function(k){const old=this===localStorage?this.getItem(k):null;rawDel.call(this,k);if(this===localStorage)touched(k,old,null)};
function localData(){const d={};for(const k of SYNC){const v=lsGet(k);if(v!=null)d[k]=v}return d}
function syncInfo(){try{return JSON.parse(lsGet('pb_sync'))||{}}catch(e){return{}}}
function markSynced(t){lsRaw('pb_sync',JSON.stringify({u:cloud.user.uid,t}));if((+lsGet('pb_mt')||0)<=t)lsRaw('pb_mt',t)}
const sameData=(a,b)=>SYNC.every(k=>(a[k]??null)===((b||{})[k]??null));
function sumUp(d){let c=0,a=0,b=0,w=0,run='';try{c=Math.floor(+d.pb_crowns||0);a=Object.values(JSON.parse(d.pb_arm||'{}')).filter(Boolean).length;b=+d.pb_best||0;w=Object.keys(JSON.parse(d.pb_wins||'{}')).length;const o=JSON.parse(d.pb_save||'null');if(o&&o.S)run='a run at wave '+o.S.wave}catch(e){}
  return {c,a,b,w,run,empty:!c&&!a&&!b&&!w&&!run}}
function sumText(d){const s=sumUp(d);if(s.empty)return 'No progress yet';return [s.c+' Crowns',s.a+' Armory item'+(s.a==1?'':'s'),s.b?'best run wave '+s.b:'',s.run].filter(Boolean).join(', ')}
const onTitle=()=>$('title').classList.contains('on')&&!$('heroes').classList.contains('on')&&!$('levels').classList.contains('on');
function cloudSoon(){if(!cloud.user||cloud.hold||cloud.pend!==undefined)return;clearTimeout(cloud.timer);cloud.timer=setTimeout(cloudUp,2500)}
async function cloudUp(){
  clearTimeout(cloud.timer);if(!cloud.user||cloud.hold||cloud.pend!==undefined)return;
  if(cloud.saving){cloud.timer=setTimeout(cloudUp,1500);return}
  const sy=syncInfo(),mt=+lsGet('pb_mt')||0;if(sy.u===cloud.user.uid&&mt<=sy.t&&cloud.msg!=='fail')return;
  const t=Date.now(),uid=cloud.user.uid;cloud.saving=true;
  try{await cloud.api.write(uid,{v:1,t,d:localData()});if(cloud.user&&cloud.user.uid===uid)markSynced(t);cloud.msg='ok'}catch(e){cloud.msg='fail'}
  cloud.saving=false;acctUI();
}
function cloudDecide(rec){
  if(!onTitle()){cloud.pend=rec;return}
  cloud.pend=undefined;const uid=cloud.user.uid,sy=syncInfo(),mt=+lsGet('pb_mt')||0,loc=localData(),known=sy.u===uid;
  if(!rec||!rec.d)return cloudUp();
  if(sameData(loc,rec.d)){markSynced(rec.t);cloud.msg='ok';acctUI();return}
  const locCh=!known||mt>sy.t,clCh=!known||rec.t>sy.t;
  if(!clCh)return cloudUp();
  if(!locCh||sumUp(loc).empty)return cloudTake(rec);
  if(sumUp(rec.d).empty)return cloudUp();
  cloud.hold=true;$('cqdev').innerHTML='<b>Keep this device\'s progress</b>'+sumText(loc);$('cqacc').innerHTML='<b>Keep your account\'s progress</b>'+sumText(rec.d);
  $('cqdev').onclick=()=>{$('cloudq').classList.remove('on');cloud.hold=false;lsRaw('pb_mt',Date.now());cloudUp()};
  $('cqacc').onclick=()=>{$('cloudq').classList.remove('on');cloud.hold=false;cloudTake(rec)};
  $('cloudq').classList.add('on');
}
function cloudTake(rec){for(const k of SYNC)lsRaw(k,rec.d[k]);markSynced(rec.t);lsRaw('pb_mt',rec.t);cloud.hold=true;location.reload()}
async function cloudCheck(){if(!cloud.user)return;const uid=cloud.user.uid;cloud.msg='load';acctUI();
  let rec;try{rec=await cloud.api.read(uid)}catch(e){cloud.msg='fail';acctUI();return}
  if(cloud.user&&cloud.user.uid===uid){cloud.msg='ok';acctUI();cloudDecide(rec)}}
function acctUI(){
  const el=$('acct');if(!el)return;
  if(cloud.state==='off'||cloud.state==='none'){el.innerHTML='';return}
  if(!cloud.user){
    el.innerHTML='<button class="big gbtn" id="gin"'+(cloud.state==='busy'?' disabled':'')+'>'+GLOGO+(cloud.state==='busy'?'Signing in':'Sign in with Google')+'</button><div class="anote outline">'+(cloud.err||'Optional. Keeps a copy of your progress so you can carry on from any device.')+'</div>';
    $('gin').onclick=cloudSignIn;return}
  const who=cloud.user.displayName||cloud.user.email||'your Google account';
  const st=cloud.msg==='fail'?'Can\'t reach your account right now. Your progress is still saved on this device.':cloud.msg==='load'?'Checking your account':'Your progress is saved to '+esc(who)+'.';
  el.innerHTML='<div class="anote outline">'+st+'</div><button class="alink outline" id="gout">Sign out</button>';
  $('gout').onclick=async()=>{clearTimeout(cloud.timer);try{await cloudUp()}catch(e){}try{await cloud.api.signOut()}catch(e){}};
}
const esc=t=>String(t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const GLOGO='__GLOGO__';
async function cloudSignIn(){
  if(cloud.state!=='ready')return;cloud.state='busy';cloud.err='';acctUI();
  try{await cloud.api.signIn()}catch(e){const c=e&&e.code||'';
    cloud.err=c==='auth/popup-closed-by-user'||c==='auth/cancelled-popup-request'?'':c==='auth/popup-blocked'?'Your browser blocked the sign-in window. Allow pop-ups for this page, then try again.':c==='auth/unauthorized-domain'?'Google sign-in isn\'t switched on for this website yet.':c==='auth/network-request-failed'?'Couldn\'t connect. Check your internet and try again.':'Sign-in didn\'t work this time. Try again in a moment.'}
  cloud.state='ready';acctUI();
}
async function cloudStart(api){
  cloud.api=api;cloud.state='ready';acctUI();
  api.onUser(u=>{const was=cloud.user&&cloud.user.uid;cloud.user=u||null;cloud.err='';cloud.msg='';cloud.pend=undefined;acctUI();if(u&&u.uid!==was)cloudCheck()});
}
async function cloudInit(){
  if(/crazygames/i.test(location.hostname))return;
  const base='https://www.gstatic.com/firebasejs/'+FBV+'/',im=f=>import(base+f);
  try{
    const [A,Au,D]=await Promise.race([Promise.all([im('firebase-app.js'),im('firebase-auth.js'),im('firebase-database.js')]),new Promise((_,r)=>setTimeout(()=>r(0),15000))]);
    const app=A.initializeApp(FBC),auth=Au.getAuth(app),db=D.getDatabase(app),R=uid=>D.ref(db,'saves/'+uid);
    cloudStart({onUser:cb=>Au.onAuthStateChanged(auth,cb),signIn:()=>Au.signInWithPopup(auth,new Au.GoogleAuthProvider()),signOut:()=>Au.signOut(auth),
      read:async uid=>{const s=await D.get(R(uid));return s.exists()?s.val():null},write:(uid,rec)=>D.set(R(uid),rec)});
  }catch(e){cloud.state='none';acctUI()}
}
document.addEventListener('visibilitychange',()=>{if(document.hidden&&cloud.user)cloudUp()});
setTimeout(cloudInit,1200);
'''.replace("'__GLOGO__'",repr(G).replace("\\'","'"))
rep("$('credbtn').onclick=",JS+"$('credbtn').onclick=")
# showTitle: run a postponed cloud check once the player is back on the title
rep("{const sv=savedInfo(),cb=$('cont');if(sv){cb.style.display='';cb.textContent='Continue (wave '+sv.wave+', level '+sv.level+')'}}\n}","{const sv=savedInfo(),cb=$('cont');if(sv){cb.style.display='';cb.textContent='Continue (wave '+sv.wave+', level '+sv.level+')'}}\n  if(typeof cloud!=='undefined'&&cloud.user&&cloud.pend!==undefined)setTimeout(()=>{if(cloud.pend!==undefined)cloudDecide(cloud.pend)},0);\n}")
rep("globalThis.__g={","globalThis.__g={cloudStart,cloud,")
open(p,'w').write(s)
