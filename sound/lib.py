import subprocess, numpy as np
SR=44100
def load(p,sr=SR,ch=1):
    r=subprocess.run(['ffmpeg','-v','error','-i',p,'-f','f32le','-ac',str(ch),'-ar',str(sr),'-'],capture_output=True,check=True)
    a=np.frombuffer(r.stdout,np.float32).copy()
    return a.reshape(-1,ch) if ch>1 else a
def save(p,a,q=4,sr=SR):
    ch=1 if a.ndim==1 else a.shape[1]
    subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ac',str(ch),'-ar',str(sr),'-i','-','-c:a','libvorbis','-q:a',str(q),p],input=a.astype(np.float32).tobytes(),check=True)
def db(x):return 20*np.log10(max(x,1e-9))
def stats(a):
    m=a if a.ndim==1 else a.mean(1)
    w=int(.05*SR);n=max(1,len(m)//w);r=np.sqrt((m[:n*w].reshape(n,w)**2).mean(1)) if len(m)>=w else np.array([np.sqrt((m**2).mean())])
    return len(m)/SR, db(np.abs(m).max()), db(r.max())
def trim(a,th=-45,pad=.01):
    m=np.abs(a if a.ndim==1 else a.mean(1));t=10**(th/20)
    idx=np.where(m>t)[0]
    if not len(idx):return a
    s=max(0,idx[0]-int(pad*SR));e=min(len(m),idx[-1]+int(pad*SR))
    return a[s:e]
def fade(a,fi=.003,fo=.03):
    n=len(a);a=a.copy();i=min(n,int(fi*SR));o=min(n,int(fo*SR))
    if i:a[:i]*=np.linspace(0,1,i)[:,None] if a.ndim>1 else np.linspace(0,1,i)
    if o:a[-o:]*=np.linspace(1,0,o)[:,None] if a.ndim>1 else np.linspace(1,0,o)
    return a
def norm(a,rms=-14,peak=-1):
    _,pk,r=stats(a);g=min(rms-r,peak-pk);return a*10**(g/20)
def loop(a,L,X=2.0,start=0):
    s=int(start*SR);n=int(L*SR);x=int(X*SR)
    seg=a[s:s+n+x].copy()
    head=seg[:x];tail=seg[n:n+x]
    r=np.linspace(0,1,x);r=r[:,None] if seg.ndim>1 else r
    out=seg[:n].copy();out[:x]=head*np.sqrt(r)+tail*np.sqrt(1-r)
    return out
