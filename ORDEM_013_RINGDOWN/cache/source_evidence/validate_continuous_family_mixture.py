"""Independent finite-sum oracle for continuous axes, priors and covariance."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
from datetime import datetime, timezone
import json
import numpy as np
import source_evidence as se
from continuous_source_calibration import curve_statistics
from continuous_family_mixture import mix_curves

STAGE = se.ROOT/'continuous_family_mixture_validation'


def main():
    STAGE.mkdir(exist_ok=False)
    names = ['continuous_family_mixture.py', 'validate_continuous_family_mixture.py',
        'continuous_source_calibration.py', 'source_family_mixture.py',
        'source_family_mixture_validation/RESULT.json']
    se.write(STAGE/'REGISTRATION.json',dict(date_utc=datetime.now(timezone.utc).isoformat(),
        seed=131031, source_counts=[257,389], strengths=17, targets=3,
        scope='Finite sample arithmetic oracle; no additional stochastic coverage claim',
        hashes={n:se.sha(se.ROOT/n) for n in names}))
    if json.loads((se.ROOT/'source_family_mixture_validation/RESULT.json').read_bytes())['status']!='PASS_FAMILY_MIXTURE_ARITHMETIC':
        raise ValueError('Inherited binary mixture is unvalidated')
    rng=np.random.default_rng(131031); grid=np.arange(-4.,4.25,.5); ref=8
    values=[]; qs=[]; stats=[]
    for f,n in enumerate((257,389)):
        source=rng.normal(size=(n,1,3))
        v=(.1*source*(1+grid[None,:,None]/8.)-.05*grid[None,:,None]**2+
            (2*f-1)*.3*grid[None,:,None]+np.array([.1,.7,-.4])[None,None,:]+f)
        q=.02*rng.normal(size=n)
        values.append(v);qs.append(q);stats.append(curve_statistics(grid,v,q,target_batch=2))
    prior=np.array([.35,.65])
    result=mix_curves(grid,values,qs,stats,prior,target_batch=2)
    integrands=[np.exp(v.astype(np.longdouble)-q[:,None,None]) for v,q in zip(values,qs)]
    means=[v.mean(axis=0) for v in integrands]
    exact_mean=sum(np.longdouble(p)*m for p,m in zip(prior,means))
    exact_log=np.log(exact_mean)
    exact_relative=exact_log-exact_log[ref]
    expected_variance=np.zeros_like(exact_mean)
    for f,(weight,array) in enumerate(zip(prior,integrands)):
        n=len(array)
        influence=weight*(array/exact_mean[None,:,:]-array[:,ref:ref+1,:]/exact_mean[None,ref:ref+1,:])/n
        influence-=influence.mean(axis=0)
        expected_variance+=np.longdouble(n)/(n-1)*np.sum(influence**2,axis=0)
    errors=dict(logz=float(np.max(np.abs(result['logz']-exact_log))),
        relative_logz=float(np.max(np.abs(result['relative_logz']-exact_relative))),
        paired_MC_sd=float(np.max(np.abs(result['relative_MC_sd']-np.sqrt(expected_variance)))))
    if max(errors.values())>1e-12:
        raise ValueError('Independent continuous mixture arithmetic differs')
    wrong=prior[0]*stats[0]['relative_logz']+prior[1]*stats[1]['relative_logz']
    wrong_error=float(np.max(np.abs(wrong-result['relative_logz'])))
    if wrong_error<.1:
        raise ValueError('Oracle does not detect averaging log evidences')
    # Exact constants can have changing family probabilities while MC error=0.
    constant=[np.broadcast_to(s['logz'],v.shape).copy() for s,v in zip(stats,values)]
    zeroq=[np.zeros(len(v)) for v in values]
    exact_stats=[curve_statistics(grid,v,q) for v,q in zip(constant,zeroq)]
    exact_mix=mix_curves(grid,constant,zeroq,exact_stats,prior)
    constant_mc=float(exact_mix['relative_MC_sd'].max())
    if constant_mc>1e-14:
        raise ValueError('Spurious error for exact constant integrands')
    # Deliberately fail the numerically subdominant family; averaging cannot
    # promote this cell even with vanishingly small prior weight.
    failing=[{k:v.copy() for k,v in s.items()} for s in stats]
    failing[0]['ESS'][0,0]=2.; failing[0]['local_precision'][0,0]=False
    guard=mix_curves(grid,values,qs,failing,[1e-10,1-1e-10])
    if guard['local_precision'][0,0]:
        raise ValueError('Subdominant imprecise family hidden')
    failing[0]['local_precision'][0,0]=True
    try:
        mix_curves(grid,values,qs,failing,prior)
    except ValueError as error:
        if str(error)!='Family precision mask contradicts its diagnostics':
            raise
    else:
        raise ValueError('Optimistic stored precision flag accepted')
    output=dict(status='PASS_CONTINUOUS_FAMILY_MIXTURE_ARITHMETIC', errors=errors,
        incorrect_log_average_max_error=wrong_error,exact_constant_max_MC_sd=constant_mc,
        weak_family_precision_preserved=True,optimistic_mask_refused=True,
        existing_binary_repeat_oracle_reused=True,physical_calibration_completed=False,
        scientific_acceptance=False,registration_sha256=se.sha(STAGE/'REGISTRATION.json'))
    se.write(STAGE/'RESULT.json',output)
    print(json.dumps(output),flush=True)


if __name__=='__main__':
    main()
