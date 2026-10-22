"""Negative tests before RNG and dense algebra controls; zero Monte Carlo draws."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
from pathlib import Path
import importlib.util,json,hashlib,time,sys
import numpy as np
B=Path(__file__).resolve().parents[1];CODE=B/'bis/e2_code'
sys.path.insert(0,str(CODE))
import synthetic_null as m
import route_iv_null as iv


def main():
    out=B/'bis/E2_NULL_GUARD_CONTROLS.json'
    if out.exists():raise FileExistsError(out)
    start=time.perf_counter();checks=[]
    def forbidden(*a,**k):raise RuntimeError('RNG_OR_ALGEBRA_REACHED_IN_NEGATIVE_TEST')
    old=m.np.random.default_rng;old_iv=iv.load_guarded_algebra
    m.np.random.default_rng=forbidden;iv.load_guarded_algebra=forbidden
    base={'components':{'noise_variance_fraction':.6,'nuisance_variance_fraction':.4},'draws':10,'seed':12,'model':'gaussian','time_guard':lambda:None,'chunk':3}
    bad=[('draws',True),('draws',1),('draws',2.2),('seed',None),('seed',False),('seed',-1),('chunk',0),('chunk',-1),('chunk',.5),('time_guard',None),('model','elliptical_student5'),('components',{'noise_variance_fraction':float('nan'),'nuisance_variance_fraction':0.})]
    try:
        for key,value in bad:
            args=dict(base);args[key]=value
            try:m.simulate_projection(**args)
            except ValueError:checks.append('REJECT_'+key+'_'+str(value))
            else:raise AssertionError('Invalid null input accepted')
        for key,value in [('N',True),('draws',1),('seed',None),('chunk',0),('sigma_sys',float('nan')),('time_guard',None)]:
            args={'population':'unused','N':10,'draws':10,'seed':12,'sigma_sys':0.,'expected_pins':{},'time_guard':lambda:None,'chunk':3};args[key]=value
            try:iv.run_null(**args)
            except ValueError:checks.append('IV_REJECT_'+key)
            else:raise AssertionError('Invalid IV input accepted')
    finally:m.np.random.default_rng=old;iv.load_guarded_algebra=old_iv
    for k,n,a in [(True,10,.05),(0,True,.05),(0,10,float('nan')),(0,10,0),(0,10,1)]:
        try:m.binomial_result(k,n,a)
        except ValueError:checks.append('BINOMIAL_REJECT_'+str((k,n,a)))
        else:raise AssertionError('Invalid confidence input accepted')
    algebra=[]
    for V in [np.zeros((2,2)),np.array([[.01,.002],[.002,.003]]),np.array([[.01,0],[0,0]])]:
        sigma=np.array([.05,.1,.2,.4]);delta=np.array([-.02,-.025,-.03,-.035]);X=np.column_stack((np.ones(4),sigma))
        r=m.projected_components(delta,sigma,X,V);C=np.diag(sigma*sigma)+X@V@X.T
        I=float(delta@np.linalg.solve(C,delta));error=abs(r['signal_information_with_nuisance']-I)
        if not np.isclose(I,r['signal_information_with_nuisance'],rtol=1e-10,atol=1e-12):raise AssertionError('Dense covariance disagrees')
        algebra.append({'dense_information':I,'absolute_error':error})
    value={'status':'PASS_ZERO_DRAWS_NEGATIVES_AND_DENSE_ALGEBRA','checks':checks,'algebra':algebra,
      'wall_seconds':time.perf_counter()-start,'python_optimized':not __debug__,
      'source_pins':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [CODE/'synthetic_null.py',CODE/'route_iv_null.py',Path(__file__)]}}
    with out.open('x') as f:json.dump(value,f,indent=2,allow_nan=False)
    print(json.dumps({'status':value['status'],'negative_checks':len(checks),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))


if __name__=='__main__':main()
