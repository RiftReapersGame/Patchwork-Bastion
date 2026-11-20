const {run,S}=require('./sim.js');const t0=Date.now();
const r=run('smart','smart',+process.argv[2]||12);
console.log('ms',Date.now()-t0,'wave',r.wave,'game min',(r.t/60).toFixed(1),'lvl',r.level,'plots',r.plots,JSON.stringify(r.towers),r.log.map(l=>`${l.w}:${(l.t/60).toFixed(1)}/${Math.round(l.hp)}/${l.gold}`).join(' '));
