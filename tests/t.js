const fs=require('fs');const h=fs.readFileSync(process.argv[2],'utf8');
let js=h.split('<script>')[1].split('</script>')[0];
const mk=()=>new Proxy(function(){}, {get:(t,k)=>{if(k==='classList')return{add(){},remove(){},toggle(){}};if(k==='style')return{};if(k==='getContext')return()=>mk();if(k==='clientWidth'||k==='clientHeight')return 600;if(k==='getBoundingClientRect')return()=>({left:0,top:0});if(k===Symbol.toPrimitive)return()=>0;return mk()},set:()=>true,apply:()=>mk()});
const els={};global.document={getElementById:id=>els[id]||(els[id]={classList:{add(){},remove(){},toggle(){}},style:{},addEventListener(){},appendChild(c){(this.kids=this.kids||[]).push(c)},set innerHTML(v){this.kids=[]},getContext:()=>mk(),clientWidth:600,clientHeight:600,getBoundingClientRect:()=>({left:0,top:0})}),createElement:()=>({addEventListener(e,f){this.click=f},set innerHTML(v){},className:''})};
global.addEventListener=()=>{};global.devicePixelRatio=1;global.localStorage={getItem(){},setItem(){}};
global.performance={now:()=>0};let raf=null;global.requestAnimationFrame=f=>{raf=f};
js=js.replace("newRun();resize();","global.__S=()=>S;global.__u=update;global.__tap=tap;global.__sw=startWave;newRun();resize();");
eval(js);
let now=0,maxW=0;
for(let i=0;i<200000;i++){
  const S=__S();
  if(S.mode==='draft'){const k=els.cards.kids;k[Math.floor(Math.random()*k.length)].click();continue}
  if(S.mode==='placeTower'){const bs=[...S.base.values()].filter(b=>!b.core);const e=bs.find(b=>!b.tower)||bs[0];__tap(e.x,e.y);if(S.mode==='placeTower')__tap(e.x,e.y);continue}
  if(S.mode==='placeChunk'){els.confirm.onclick();if(S.mode==='placeChunk')throw 'chunk stuck';continue}
  if(S.mode==='over'){console.log('over wave',S.wave,'lvl',S.level,'cells',S.base.size,'paths',S.paths.length);break}
  if(!S.started)__sw();
  now+=50;raf&&raf(now);
}
