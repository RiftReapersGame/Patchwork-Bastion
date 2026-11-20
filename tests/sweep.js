const {run,G}=require('./sim.js');
const N=+process.argv[2]||12,cap=+process.argv[3]||45;
const sets=JSON.parse(process.argv[4]);
for(const set of sets){Object.assign(G.TUNE,{hpLin:.22,hpExp:1.1,budA:6,budB:2.6,budExp:1,xpA:5,xpB:4},set);
  for(const pol of [['smart','smart'],['random','random']]){const t0=Date.now();const rs=[];for(let i=0;i<N;i++)rs.push(run(pol[0],pol[1],cap));
    const ws=rs.map(r=>r.wave).sort((a,b)=>a-b),q=p=>ws[Math.floor((ws.length-1)*p)];
    const firstHit=rs.map(r=>{const l=r.log.find(l=>l.hp<25);return l?l.w:99}).sort((a,b)=>a-b)[Math.floor(N/2)];
    console.log(JSON.stringify(set),pol[0],`death q25 ${q(.25)} med ${q(.5)} q75 ${q(.75)} max ${ws[N-1]} | first castle hit (med) wave ${firstHit} | min ${(rs.reduce((a,r)=>a+r.t,0)/N/60).toFixed(1)} | lvl ${(rs.reduce((a,r)=>a+r.level,0)/N).toFixed(0)} plots ${(rs.reduce((a,r)=>a+r.plots,0)/N).toFixed(0)} | ${((Date.now()-t0)/1000).toFixed(0)}s`)}}
