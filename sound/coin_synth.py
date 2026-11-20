import sys;sys.path.insert(0,'/home/claude/snd')
from lib import *
rng=np.random.default_rng(3)
def env(t,a,d):return np.minimum(t/a,1)*np.exp(-t/d)
def ring(f0,ratios,amps,dur,dec,t0=0,L=None):
    n=int((L or dur)*SR);t=np.arange(n)/SR;out=np.zeros(n)
    tt=t-t0;m=tt>=0
    for r,a,dd in zip(ratios,amps,dec):
        out[m]+=a*np.sin(2*np.pi*f0*r*tt[m]+rng.uniform(0,6))*env(tt[m],.0015,dd)
    return out
def click(L,t0,amp=.6,fc=6000):
    n=int(L*SR);out=np.zeros(n);s=int(t0*SR);k=int(.006*SR)
    nz=rng.normal(0,1,k)*np.exp(-np.arange(k)/(.0015*SR))
    # crude highpass
    nz=np.diff(np.concatenate([[0],nz]))
    out[s:s+k]+=amp*nz;return out
R=[1,2.756,5.404,8.933];A=[1,.6,.35,.2]
# 1: bright ching (one coin)
L=.6;a=ring(2093,R,A,L,[.28,.16,.09,.05],0)+click(L,0,.5)
save('out/syn_ching.ogg',fade(norm(a,-14,-1),.001,.05),q=4)
# 2: ka-ching (two strikes, second higher)
L=.75;a=ring(1568,R,A,L,[.08,.05,.04,.03],0)*.6+click(L,0,.4)+ring(2637,R,A,L,[.32,.18,.1,.06],.075)+click(L,.075,.5)
save('out/syn_kaching.ogg',fade(norm(a,-14,-1),.001,.06),q=4)
# 3: coin into a slot: two clinks then a short drop ring
L=.55;a=ring(2349,[1,2.4,3.9],[1,.5,.3],L,[.03,.02,.015],0)*.7+click(L,0,.5)+ring(2793,[1,2.4,3.9],[1,.5,.3],L,[.04,.025,.02],.055)*.6+click(L,.055,.4)+ring(1976,R,A,L,[.18,.1,.06,.04],.11)
save('out/syn_slot.ogg',fade(norm(a,-14,-1),.001,.05),q=4)
# 4: arcade coin, two notes
L=.45;t=np.arange(int(L*SR))/SR
def sq(f,t):return np.sign(np.sin(2*np.pi*f*t))*.5+.5*np.sin(2*np.pi*f*t)
a=np.where(t<.07,sq(1976,t),sq(2637,t)*np.exp(-(t-.07)/.12))*.5
save('out/syn_arcade.ogg',fade(norm(a,-16,-1),.001,.03),q=4)
print('ok')
