"""Auditor's independent single-realization (Brownian phase) fit, noiseless, ramo B and R-RAIZ-0/R-MOD-like x."""
import numpy as np, math, json
from scipy.optimize import least_squares
ALPHA=7.2973525693e-3; BETA=ALPHA*math.sqrt(math.e)
GMSUN_C3=1.32712440041e20/299792458.0**3
def bcw(chi):
    return 1.5251-1.1568*(1-chi)**0.1292, 0.7+1.4187*(1-chi)**(-0.4990)
M,chi=68.1,0.68
tM=M*GMSUN_C3; w,Q=bcw(chi); om=w/tM; tau=2*Q/om
fs=4096.; n=128; t=np.arange(n)/fs
def fit(h):
    def res(p):
        df,u=p; tp=tau*math.exp(u); op=om*(1+df)
        env=np.exp(-t/tp); X=np.stack([env*np.cos(op*t),env*np.sin(op*t)],1)
        c,*_=np.linalg.lstsq(X,h,rcond=None); return h-X@c
    best=None
    for s in [(0,0),(0.02,0.1),(-0.02,-0.1)]:
        r=least_squares(res,s,bounds=([-.5,-2],[.5,2]),xtol=1e-14,ftol=1e-14,gtol=1e-14)
        if best is None or r.cost<best.cost: best=r
    return best.x[0], math.exp(best.x[1])-1
rng=np.random.default_rng(20260922)
out={}
for label,Gamma in [('R-B',BETA*w*w/(2*tM)),('R-RAIZ-0_like',BETA*om/2)]:
    x=Gamma*tau
    ens=np.exp(-(1/tau+Gamma)*t)*np.cos(om*t+0.37)
    dfe,dte=fit(ens)
    dfs=[];dts=[]
    for k in range(1500):
        dW=rng.normal(scale=math.sqrt(1/fs),size=n); W=np.concatenate([[0],np.cumsum(dW)[:-1]])
        phi=rng.uniform(0,2*np.pi)
        h=np.exp(-t/tau)*np.cos(om*t+phi+math.sqrt(2*Gamma)*W)
        a,b=fit(h); dfs.append(a); dts.append(b)
    dfs=np.array(dfs); dts=np.array(dts)
    out[label]=dict(Gamma=Gamma,x=x,ensemble_exact=-x/(1+x),ensemble_fit_dtau=dte,ensemble_fit_df=dfe,
        mean_dtau=float(dts.mean()),se_mean_dtau=float(dts.std(ddof=1)/math.sqrt(len(dts))),ratio=float(dts.mean()/(-x/(1+x))),
        median_dtau=float(np.median(dts)),mean_df=float(dfs.mean()),std_df=float(dfs.std(ddof=1)),
        gerencia_std_df_estimate=0.7*math.sqrt(2*x)/(2*Q))
    print(label,json.dumps(out[label]))
json.dump(out,open('realization_out.json','w'),indent=1)
