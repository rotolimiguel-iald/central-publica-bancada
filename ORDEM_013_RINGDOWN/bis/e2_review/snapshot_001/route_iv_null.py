"""Null LRT at frozen E0 populations; empirical tail limits are explicit."""
import importlib.util
from pathlib import Path
import numpy as np
from registration_guard import BASE,sha
from synthetic_null import binomial_result

def load_guarded_algebra(expected_pins):
    p=BASE/'refeito/e0_mc_guarded_013bis.py'
    if sha(p)!=expected_pins['refeito/e0_mc_guarded_013bis.py']:raise ValueError('MC guard changed')
    original=BASE/'refeito/e0_route_iv_power_013bis_v2.py'
    if sha(original)!=expected_pins['refeito/e0_route_iv_power_013bis_v2.py']:raise ValueError('MC algebra changed')
    spec=importlib.util.spec_from_file_location('registered_guarded_iv',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m

def run_null(population,N,draws,seed,sigma_sys,expected_pins,time_guard,chunk=10000):
    if not isinstance(N,int) or N<2 or not isinstance(draws,int) or draws<=0:raise ValueError('Invalid null dimensions')
    if not np.isfinite(sigma_sys) or sigma_sys<0:raise ValueError('Invalid systematic null width')
    mc=load_guarded_algebra(expected_pins);frozen=mc.frozen_populations()
    if population not in frozen:raise ValueError('Population not frozen')
    sig=np.asarray(frozen[population]['sigma_df']);variances=sig*sig+sigma_sys*sigma_sys
    used=0;k=0;max_t=0.;sum_t=0.;chunks=0
    while used<draws:
        time_guard();count=min(chunk,draws-used)
        n,s,ss=mc.sufficient(N,variances,0.,count,seed+chunks)
        t,_=mc.lrt(n,s,ss,variances)
        k+=mc.count_above(t,25.);used+=count;chunks+=1
        max_t=max(max_t,float(t.max()));sum_t+=float(t.sum())
    return dict(**binomial_result(k,used),population=population,N=N,seed=seed,chunk_size=chunk,
      threshold_LRT=25.,sigma_sys_INPUT=sigma_sys,max_LRT=max_t,mean_LRT=sum_t/used,
      scope='Gaussian heterogeneous measurement-width null at prospective N; fixed declared systematic variance. Does not calibrate physical sigma_sys, waveform errors, or a non-Gaussian full-posterior null.')
