"""Cetico 2: refaz o vies do estimador da C2 em RG (gamma=0), SNR20, ruido OU+branco, com N grande.
Copia fiel do estimador de trajectory_recovery.py (bancada, so leitura); so muda N e a semente."""
import os; os.environ['OPENBLAS_NUM_THREADS']='1'; os.environ['OMP_NUM_THREADS']='1'
import json,sys,numpy as np
from scipy.linalg import cholesky, solve_triangular
from scipy.optimize import least_squares
from tgl_ringdown_prediction import prediction
def fit(time,y,whitener,omega,tau):
    target=whitener@y
    def residual(p):
        angle=omega*(1+p[0])*time; env=np.exp(-time/(tau*np.exp(p[1])))
        basis=whitener@np.column_stack([env*np.cos(angle),env*np.sin(angle)])
        return target-basis@np.linalg.lstsq(basis,target,rcond=None)[0]
    c=[least_squares(residual,[s,0.],bounds=([-.5,-2.],[.5,2.]),ftol=1e-10,xtol=1e-10,gtol=1e-10,max_nfev=100) for s in (0.,-.03,.03)]
    b=min(c,key=lambda r:r.cost); return float(np.expm1(b.x[1]))
mass,spin=68.1,.68
base=prediction(mass,spin,'R-B'); omega,tau=base['omega_rad_s'],base['tau_gr_s']
times=np.arange(128)/4096.
cov=.4*np.eye(128)+.6*np.exp(-abs(times[:,None]-times[None,:])/.001)
chol=cholesky(cov,lower=True); whiten=solve_triangular(chol,np.eye(128),lower=True)
carrier=np.exp(-times/tau)*np.exp(1j*(omega*times+.37))
out={}
for snr in [float(a) for a in sys.argv[2:]] or [20.]:
    amp=snr/np.linalg.norm(whiten@carrier.real); clean=amp*carrier.real
    N=int(sys.argv[1]); seed=13042600
    rng=np.random.default_rng(seed)
    # reproduz exatamente a sequencia da bancada para N=50 (wiener e cauchy consumidos antes do ruido)
    if N==50:
        rng.normal(size=(50,128)); rng.standard_cauchy(size=(50,128))
    noise=rng.normal(size=(N,128))@chol.T
    x=np.array([fit(times,clean+n,whiten,omega,tau) for n in noise])
    r=dict(SNR=snr,N=N,seed=seed,mean=float(x.mean()),median=float(np.median(x)),sd=float(x.std(ddof=1)),
           se=float(x.std(ddof=1)/np.sqrt(N)),q05_50_95=np.quantile(x,[.05,.5,.95]).tolist(),
           z_mean=float(x.mean()/(x.std(ddof=1)/np.sqrt(N))))
    print(json.dumps(r)); out[str(snr)]=r
json.dump(out,open(f'refeito_N{sys.argv[1]}.json','w'),indent=1)
