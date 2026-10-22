"""Bounded C2 audit: independent spectral geometry and selected fits only.

No builder or project module is imported. No full trajectory experiment or PE.
"""
import os
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import ast
import hashlib
import json
import math
import time
import numpy as np
import scipy
from scipy.linalg import cholesky, solve_triangular, qr, null_space
from scipy.interpolate import CubicSpline
from scipy.optimize import least_squares
from scipy.stats import poisson

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent

def write_new(path, data):
    if path.exists():raise FileExistsError(path)
    raw=(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    tmp=path.with_name(path.name+'.tmp')
    with tmp.open('xb') as handle:handle.write(raw)
    assert tmp.read_bytes()==raw
    tmp.replace(path)

def main():
    start=time.monotonic()
    d=json.loads((ROOT/'bis/C2_TRAJECTORY_expanded_1000.json').read_bytes())
    meta=json.loads((ROOT/'C5_RECOLORED_NOISE.json').read_bytes())
    scenario=next(r for r in meta['scenarios'] if r['psd']=='O4')
    with np.load(ROOT/scenario['cache_path'],allow_pickle=False) as f:
        arrays={k:f[k].copy() for k in ('frequency_hz','psd_scaled',
            'projected_covariance_scaled','H1_strain_scaled','H1_original_GPS')}
    freq=arrays['frequency_hz'];psd=arrays['psd_scaled'];noise=arrays['H1_strain_scaled'][:,:128]
    t=np.arange(128)/2048.;poly=np.column_stack([np.ones(128),np.linspace(-1,1,128),np.linspace(-1,1,128)**2])
    # Independent SVD complement and explicit trigonometric quadrature; no FFT.
    p=null_space(poly.T).T
    phase=2*np.pi*np.outer(t,freq)
    cs=p@np.cos(phase);sn=p@np.sin(phase)
    cs[:,0]=0.;sn[:,0]=0.
    weights=psd*(freq[1]-freq[0]);weights=weights.copy();weights[[0,-1]]*=.5
    cov=(cs*weights)@cs.T+(sn*weights)@sn.T
    inverse=solve_triangular(cholesky(cov,lower=True),np.eye(125),lower=True)
    w=inverse@p
    # Extract only the already-read pure whitener function for comparison.
    source=ROOT/'prepare_empirical_noise.py'
    tree=ast.parse(source.read_text(encoding='utf-8'))
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='polynomial_whitener')
    namespace=dict(np=np,qr=qr,cholesky=cholesky,solve_triangular=solve_triangular,STRIDE=2)
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),namespace)
    w0,c0,i0=namespace['polynomial_whitener'](psd,4096,128)
    q0=qr(np.polynomial.legendre.legvander(np.linspace(-1,1,128),2),mode='full')[0][:,3:].T
    rotate=q0@p.T
    cov0_independent=rotate@cov@rotate.T
    nlong=arrays['H1_strain_scaled'].shape[1]
    plong=qr(np.polynomial.legendre.legvander(np.linspace(-1,1,nlong),2),mode='full')[0][:,3:].T
    restrict=p@plong.T[:128,:]
    transported=restrict@arrays['projected_covariance_scaled']@restrict.T
    raw=np.loadtxt(ROOT/'cache/psd'/scenario['curve']['filename'])
    raw=raw[(raw[:,0]>0)&(raw[:,1]>0)&np.isfinite(raw[:,1])]
    predicted=np.zeros_like(psd);positive=freq>0
    predicted[positive]=np.exp(np.interp(np.log(freq[positive]),np.log(raw[:,0]),2*np.log(raw[:,1])))
    below=positive&(freq<raw[0,0]);predicted[below]=raw[0,1]**2*(freq[below]/raw[0,0])**(-4)
    predicted*=1e42
    geometry=dict(array_shapes={k:list(v.shape) for k,v in arrays.items()},
        times_first_last=[float(t[0]),float(t[-1])],sample_duration=128/2048,
        input_fs=4096,retained_fs=2048,stride=2,frequency_last=float(freq[-1]),
        frequency_step=float(freq[1]-freq[0]),polynomial_rank=3,quotient_dimension=125,
        polynomial_annihilation=float(np.max(abs(p@poly))),
        orthonormality=float(np.max(abs(p@p.T-np.eye(125)))),
        independent_whitening_residual=float(np.max(abs(inverse@cov@inverse.T-np.eye(125)))),
        recorded_algorithm_residual=float(np.max(abs(i0@c0@i0.T-np.eye(125)))),
        recorded_residual=d['whitening_residual'],
        independent_covariance_relative_error=float(np.linalg.norm(cov0_independent-c0)/np.linalg.norm(c0)),
        metric_relative_error=float(np.linalg.norm(w.T@w-w0.T@w0)/np.linalg.norm(w0.T@w0)),
        long_to_short_covariance_relative_error=float(np.linalg.norm(transported-cov)/np.linalg.norm(cov)),
        long_to_short_whitened_residual=float(np.max(abs(inverse@transported@inverse.T-np.eye(125)))),
        psd_max_relative_difference=float(np.max(abs(predicted[positive]/psd[positive]-1))),
        gps_exact_match=bool(np.array_equal(arrays['H1_original_GPS'],d['original_noise_GPS'])),
        short_empirical_mean_chisquare=float(np.mean((noise@w.T)**2)))
    # Regenerate just RNG base arrays (no fits here) to recover selected records.
    dt=np.diff(np.r_[0.,t]);rng=np.random.default_rng(d['seed']);n=d['N_per_cell']
    brownian=np.cumsum(rng.normal(size=(n,128))*np.sqrt(dt),axis=1)
    cauchy=np.cumsum(rng.standard_cauchy(size=(n,128))*dt,axis=1)
    indices=rng.integers(0,len(noise),size=n)
    assert indices.tolist()==d['noise_indices']
    beta=7.2973525693e-3*math.sqrt(math.e)
    tm=68.1*1.3271244e20/299792458.**3
    tp=math.sqrt((6.62607015e-34/(2*math.pi))*6.67430e-11/299792458.**5)
    spin=.68;wr=1.5251-1.1568*(1-spin)**.1292;q=.7+1.4187*(1-spin)**(-.499)
    wbcw=wr/tm;taubcw=2*q/wbcw
    grid=json.loads((ROOT/'QNM_GRID.json').read_bytes())['modes']['220']
    exact=complex(CubicSpline(grid['spins'],np.array(grid['real'])+1j*np.array(grid['imag']))(spin))
    result_rows=[];selected=[];refits=[]
    for row in d['rows']:
        reading=row['reading'];occupation=row.get('occupation')
        omega,tau=(exact.real/tm,-tm/exact.imag) if reading=='R-MOD' else (wbcw,taubcw)
        carrier=np.exp(-t/tau+1j*(omega*t+.37));amp=20/np.linalg.norm(w@carrier.real)
        if occupation:
            lo,hi=row['poisson_meta']['support'];support=np.arange(lo,hi+1)
            probabilities=poisson.pmf(support,occupation)
            gaps=np.sqrt(beta*omega)/(np.sqrt(support+1)+np.sqrt(support))
            ensemble=np.exp(-.5*t[:,None]*gaps*gaps)@probabilities
            gamma=None
        else:
            if reading=='R-A':gamma=beta*tp*omega**2/2
            elif reading=='R-B':gamma=beta*tm*omega**2/2
            elif reading=='R-RAIZ-0':gamma=beta*omega/2
            elif reading=='R-RAIZ-EP4':
                base=1/(4*tp);gamma=beta*omega**2/(2*(math.sqrt(base+omega)+math.sqrt(base))**2)
            elif reading=='R-RAIZ-REST':
                base=(tm*299792458.**3/6.67430e-11)*299792458.**2/(6.62607015e-34/(2*math.pi))
                gamma=beta*omega**2/(2*(math.sqrt(base+omega)+math.sqrt(base))**2)
            elif reading=='R-LIN':gamma=beta*omega
            elif reading=='R-MOD':
                root=math.sqrt(1-spin*spin);oh=spin/(2*tm*(1+root));kap=root/(2*tm*(1+root))
                gamma=beta*(2*math.pi/kap)*(omega-2*oh)**2/2
            elif reading=='R-GLOBAL':gamma=0.
            else:raise ValueError(reading)
            ensemble=np.exp(-gamma*t)
        gr=w@np.column_stack([np.exp(-t/tau)*np.cos(omega*t),np.exp(-t/tau)*np.sin(omega*t)])
        grq=np.linalg.svd(gr,full_matrices=False)[0]
        def residual(params, target):
            env=np.exp(-t/(tau*np.exp(params[1])))
            angle=omega*(1+params[0])*t
            design=w@np.column_stack([env*np.cos(angle),env*np.sin(angle)])
            uq=np.linalg.qr(design,mode='reduced')[0]
            return target-uq@(uq.T@target)
        target_ensemble=w@(amp*(carrier*ensemble).real)
        saved=row['ensemble_fit'];r=residual([saved['df'],math.log1p(saved['dtau'])],target_ensemble)
        report=dict(reading=reading,occupation=occupation,omega=omega,tau=tau,gamma=gamma,
            ensemble_saved_cost=saved['cost'],ensemble_cost_recalculated=float(r@r/2),
            analytic_ensemble_dtau=None if gamma is None else -gamma*tau/(1+gamma*tau),
            saved_ensemble_dtau=saved['dtau'],snr=float(np.linalg.norm(w@(amp*carrier.real))))
        if occupation:
            report['poisson_sum']=float(probabilities.sum())
            report['poisson_tail']=float(poisson.cdf(lo-1,occupation)+poisson.sf(hi,occupation))
        result_rows.append(report)
        picks={0}
        if reading=='R-LIN':picks.update([149,284,596,766])
        for i in sorted(picks):
            factor=(np.exp(1j*brownian[i,:,None]*gaps)@probabilities if occupation else
                np.exp(1j*(gamma*cauchy[i] if reading=='R-LIN' else math.sqrt(2*gamma)*brownian[i])))
            clean=amp*(carrier*factor).real;white=w@clean
            projection=grq@(grq.T@white)
            loss=1-np.linalg.norm(projection)/np.linalg.norm(white)
            projection_pythagorean=abs(float(white@white-projection@projection-(white-projection)@(white-projection)))
            for kind in ('noise_free','recolored'):
                target=w@(clean+(noise[indices[i]] if kind=='recolored' else 0.))
                saved=row[kind]['fits'][i];params=[saved['df'],math.log1p(saved['dtau'])]
                residual0=residual(params,target);cost=float(residual0@residual0/2)
                record=dict(reading=reading,occupation=occupation,kind=kind,index=i,
                    saved_cost=saved['cost'],cost_recalculated=cost,cost_difference=cost-saved['cost'],
                    phase_projection_loss=float(loss),pythagorean_residual=projection_pythagorean,
                    factor_modulus_range=[float(abs(factor).min()),float(abs(factor).max())])
                selected.append(record)
                # 11 reoptimizations: 7 boundary records plus 4 ordinary controls.
                do_refit=saved['boundary'] or (i==0 and (
                    reading=='R-B' or (reading=='R-MOD' and kind=='recolored') or
                    (occupation==4 and kind=='noise_free')))
                if do_refit:
                    candidates=[least_squares(residual,[a,0.],args=(target,),bounds=([-.5,-2.],[.5,2.]),
                        ftol=1e-11,xtol=1e-11,gtol=1e-11,max_nfev=200) for a in (-.45,-.2,0.,.2,.45)]
                    candidate=least_squares(residual,params,args=(target,),bounds=([-.5,-2.],[.5,2.]),
                        ftol=1e-11,xtol=1e-11,gtol=1e-11,max_nfev=200)
                    best=min(candidates+[candidate],key=lambda z:z.cost)
                    refits.append(dict(reading=reading,occupation=occupation,kind=kind,index=i,
                        saved_df=saved['df'],saved_dtau=saved['dtau'],saved_cost=saved['cost'],
                        df=float(best.x[0]),dtau=float(np.expm1(best.x[1])),cost=float(best.cost),
                        cost_improvement=float(cost-best.cost),success=bool(best.success)))
    output=dict(scope='Direct spectral quadrature; 30 selected cost checks, only 11 reoptimizations; no full experiment',
        numpy_version=np.__version__,scipy_version=scipy.__version__,geometry=geometry,
        seed_indices_match=True,beta_runtime=beta,ensemble_checks=result_rows,
        selected_costs=selected,refits=refits,seconds=time.monotonic()-start)
    write_new(OUT/'numerics.json',output)
    print(json.dumps(dict(geometry=geometry,selected_cost_count=len(selected),refit_count=len(refits),
        maximum_cost_discrepancy=max(abs(r['cost_difference']) for r in selected),
        maximum_refit_improvement=max(r['cost_improvement'] for r in refits),seconds=output['seconds']),indent=2))
    for r in refits:print(json.dumps(r))

if __name__=='__main__':main()
