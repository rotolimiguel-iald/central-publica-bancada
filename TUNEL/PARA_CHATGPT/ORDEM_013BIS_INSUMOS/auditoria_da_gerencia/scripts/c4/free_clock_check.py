import numpy as np, math
from scipy.stats import gaussian_kde
ALPHA=7.2973525693e-3; BETA=ALPHA*math.sqrt(math.e)
d=np.load('post_GW250114_17018009__pSEOBNRv5PHM.npz'); df,dt,chi=d['domega220'],d['dtau220'],d['final_spin_non_evolved']
wr=1.5251-1.1568*(1-chi)**0.1292; Q=0.7+1.4187*(1-chi)**(-0.499); xB=BETA*wr*Q
k0=gaussian_kde(np.vstack([df,dt])); f0=k0.pdf([[0.],[0.]])[0]
us=np.linspace(0,1,41); Bs=[]
for u in us:
    s=-(u*xB)/(1+u*xB)
    Bs.append(gaussian_kde(np.vstack([df,dt-s])).pdf([[0.],[0.]])[0]/f0)
Bs=np.array(Bs)
print('lnB(u) at u=0,0.5,1:',np.log(Bs[[0,20,40]]))
print('uniform-prior ln evidence ratio:', math.log(np.trapezoid(Bs,us)))
# posterior CDF in u (uniform prior)
post=Bs/np.trapezoid(Bs,us); cdf=np.concatenate([[0],np.cumsum((post[1:]+post[:-1])/2*np.diff(us))])
print('u quantiles 0.5,0.9,0.95:',[float(np.interp(q,cdf,us)) for q in (0.5,0.9,0.95)])
# data-only likelihood extension: how far beyond t_M before lnB<-2 ? (u>1 means tau_star > GM/c^3)
for u in [1,2,3,5,8,10]:
    s=-(u*xB)/(1+u*xB)
    print('u=',u,'lnB=',float(np.log(gaussian_kde(np.vstack([df,dt-s])).pdf([[0.],[0.]])[0]/f0)))
