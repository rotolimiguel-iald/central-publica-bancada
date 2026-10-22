"""Independent quadrature oracle with a fixed remnant and correlated mock posterior.

For a constant shift the KDE covariance does not change. Directly integrate
the original joint KDE evaluated along the nonlinear clock curve; compare
to the sample-kernel cumulative integration used on actual release samples.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import hashlib
import json
import math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import gaussian_kde
from free_clock_posterior import integrate
from fetch_public import atomic_json
from tgl_ringdown_prediction import scales

ROOT=Path(__file__).resolve().parent

def main():
    rng=np.random.default_rng(13042500)
    data=rng.multivariate_normal([.02,.08],[[.08**2,.3*.08*.12],[.3*.08*.12,.12**2]],10000).T
    x=.025;tm=.0003;tp=scales(68.,'CODATA2018_IAU2015')[1]
    kde=gaussian_kde(data)
    rows=[]
    for prior in ('uniform','log_uniform'):
        result=integrate(data,np.full(data.shape[1],x),np.full(data.shape[1],tm),tp,prior,1.,1025)
        def clock(u):
            return tp+u*(tm-tp) if prior=='uniform' else tp*math.exp(u*math.log(tm/tp))
        def likelihood(u):
            xx=x*clock(u)/tm
            return float(kde([0.,-xx/(1+xx)])[0])
        z,error=quad(likelihood,0,1,epsabs=1e-9,epsrel=1e-9,limit=100)
        logb=math.log(z/likelihood(0.))
        delta=abs(logb-result['ln_evidence_free_clock_over_GR'])
        checks=[]
        for q in (.9,.95):
            u=brentq(lambda cut:quad(likelihood,0,cut,epsabs=1e-9,epsrel=1e-9)[0]/z-q,0,1,xtol=1e-12)
            value=clock(u)
            relative=abs(result['quantiles'][str(q)]['tau_source_s']/value-1.)
            checks.append(dict(quantile=q,oracle_tau=value,relative_error=relative))
            assert relative<2e-4
        assert delta<1e-5
        rows.append(dict(prior=prior,logB_oracle=logb,logB_absolute_error=delta,
                         integration_error_estimate=error,limits=checks))
    out=dict(status='PASS',mock_seed=13042500,mock_samples=data.shape[1],rows=rows,
             oracle='Direct original joint scipy KDE integrated along nonlinear clock curve with adaptive QUADPACK; separate from per-sample trapezoidal CDF implementation',
             tested_sha256=hashlib.sha256((ROOT/'free_clock_posterior.py').read_bytes()).hexdigest())
    atomic_json(ROOT/'C4_FREE_CLOCK_ORACLE.json',out)
    print(json.dumps(out),flush=True)

if __name__=='__main__':main()
