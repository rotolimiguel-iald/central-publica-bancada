# [CONJECTURE-level auditor check] the pasted text's dimensionally-fixed form Gamma = beta/t_M  (x = beta*tau/t_M = 2 beta Q / (M omega))
import numpy as np, math, glob
from scipy.stats import gaussian_kde
ALPHA=7.2973525693e-3; BETA=ALPHA*math.sqrt(math.e)
controls={'GW191109_010717','GW200208_130117'}
def lnB(df,dt,chi):
    wr=1.5251-1.1568*(1-chi)**0.1292; Q=0.7+1.4187*(1-chi)**(-0.499); x=2*BETA*Q/wr; s=-x/(1+x)
    k0=gaussian_kde(np.vstack([df,dt])); k1=gaussian_kde(np.vstack([df,dt-s]))
    return float(k1.logpdf([[0.],[0.]])[0]-k0.logpdf([[0.],[0.]])[0]), float(np.median(s))
tot=0.; tot33=0.
for f in sorted(glob.glob('post_G5_*.npz')):
    ev=f.split('post_G5_')[1].split('__')[0]; d=np.load(f)
    v,s=lnB(d['domega220'],d['dtau220'],d['final_spin_non_evolved'])
    tot33+=v
    if ev not in controls: tot+=v
    if ev.startswith('GW250114'): print('GW250114 text-fixed reading: shift',s,'lnB',v)
print('catalog31',tot,'catalog33',tot33)
