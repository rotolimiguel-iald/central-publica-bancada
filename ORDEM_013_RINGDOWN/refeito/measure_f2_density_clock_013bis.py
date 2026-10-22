"""Nonblind density controls and extended source-clock prior, existing samples only."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import sys,json,hashlib,math,time
import numpy as np,h5py
from scipy.interpolate import CubicSpline
from scipy.integrate import cumulative_trapezoid
from scipy.stats import multivariate_normal
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from posterior_220_readout import uniform_prior
from tgl_ringdown_prediction import prediction
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(name,doc):
    p=ROOT/'bis'/name
    if p.exists():raise FileExistsError(p)
    raw=(json.dumps(doc,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode();tmp=p.with_suffix('.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise ValueError('Write mismatch')
    tmp.replace(p);print(name,sha(p),flush=True)
def normal_zero(x):
    if not np.isfinite(x).all():raise ValueError('Nonfinite')
    mu=np.mean(x,axis=1);cov=np.cov(x);sign,ld=np.linalg.slogdet(cov)
    if sign!=1 or np.linalg.eigvalsh(cov).min()<=0:raise ValueError('Singular covariance')
    logpdf=-math.log(2*math.pi)-.5*(ld+mu@np.linalg.solve(cov,mu))
    residual=abs(logpdf-multivariate_normal.logpdf([0,0],mean=mu,cov=cov))
    if residual>1e-10:raise ValueError('Gaussian control disagreement')
    return float(logpdf),dict(mean=mu.tolist(),covariance=cov.tolist(),formula_error=residual)
def kernel_at_zero(x,bwmult):
    covariance=np.cov(x)*(x.shape[1]**(-1/3))*bwmult**2
    inv=np.linalg.inv(covariance)
    exponent=-.5*(inv[0,0]*x[0]**2+2*inv[0,1]*x[0]*x[1]+inv[1,1]*x[1]**2)
    peak=np.max(exponent)
    return float(peak+np.log(np.exp(exponent-peak).mean())-math.log(2*math.pi)-.5*np.linalg.slogdet(covariance)[1])
def main():
    start=time.perf_counter();amend=ROOT/'bis/REGISTRO_C4_EMENDA_013BIS.json'
    registration=json.loads(amend.read_bytes())
    if sha(amend) not in (ROOT/'C4_EMENDA_TECNICA_013BIS.md').read_text():raise ValueError('Amendment witness mismatch')
    path=ROOT/'cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr/posterior_samples.h5'
    if sha(path)!=json.loads((ROOT/'C4_SCHEMA.json').read_bytes())['h5_sha256']:raise ValueError('Source changed')
    with h5py.File(path,'r') as h:
        g=h['pSEOBNRv5PHM'];s=g['posterior_samples'][()]
        pf,tpf=uniform_prior(g,'domega220');pt,tpt=uniform_prior(g,'dtau220')
    x=np.vstack([s['domega220'],s['dtau220']]);a=s['final_spin_non_evolved'];m=s['final_mass_non_evolved'];z=s['redshift']
    grid=json.loads((ROOT/'QNM_GRID.json').read_bytes())['modes']['220']
    qnm=CubicSpline(grid['spins'],np.array(grid['real'])+1j*np.array(grid['imag']),extrapolate=False)(a)
    if not np.isfinite(qnm).all() or not pf[0]<0<pf[1]:raise ValueError('QNM/prior')
    base,basediag=normal_zero(x);rows=[];xb=None;ratios=None
    for reading in registration['independent_density']['readings']:
        pred=[prediction(float(mm),float(aa),reading,redshift=float(zz),qnm_dimensionless=complex(ww) if reading=='R-MOD' else None) for mm,aa,zz,ww in zip(m,a,z,qnm)]
        shift=np.array([p['delta_tau_ensemble_exact'] for p in pred])
        if np.any((shift<=pt[0])|(shift>=pt[1])):raise ValueError('Outside prior')
        moved=x.copy();moved[1]-=shift
        logpdf,diag=normal_zero(moved)
        row=dict(reading=reading,lnB_gaussian2D=logpdf-base,shift_05_50_95=np.quantile(shift,[.05,.5,.95]).tolist(),density=diag)
        rows.append(row);print(reading,row['lnB_gaussian2D'],flush=True)
        if reading=='R-B':
            xb=np.array([p['x'] for p in pred]);ratios=np.array([p['t_planck_s']/(p['t_mass_s']/(1+p['redshift'])) for p in pred])
    dependencies={n:sha(ROOT/n) for n in ['tgl_ringdown_prediction.py','QNM_GRID.json','posterior_220_readout.py','C4_FREE_CLOCK.json','C4_220_INITIAL.json']}
    common=dict(status='NONBLIND_DENSITY_APPROXIMATION_CONTROL__NOT_CALIBRATED_EXCLUSION',N=len(s),source_sha256=sha(path),amendment_sha256=sha(amend),code_sha256=sha(Path(__file__)),dependencies=dependencies,priors=[tpf,tpt],scope='GW250114 220 sector with identical free-440 nuisance priors in both hypotheses')
    new('F2_INDEPENDENT_GAUSSIAN_DENSITY.json',dict(**common,rows=rows,GR_density=basediag,method='Full sample covariance, no KDE bandwidth; spin-dependent unit-Jacobian shear; Gaussian approximation may miss tails/skewness',sampling='Equal-weight released samples; no new PE'))
    q=np.linspace(0,40,801);curves=[]
    if ratios.max()>1e-30:raise ValueError('Planck lower endpoint no longer negligible')
    for bw in registration['free_clock']['density_bandwidth_multipliers']:
        null=kernel_at_zero(x,bw);ln=[]
        for v in q:
            shift=-xb*v/(1+xb*v)
            if np.any((shift<=pt[0])|(shift>=pt[1])):raise ValueError('Clock curve leaves broad prior')
            moved=x.copy();moved[1]-=shift;ln.append(kernel_at_zero(moved,bw)-null)
        ln=np.array(ln);posterior=[]
        for ceiling in registration['free_clock']['ceiling_robustness_INPUT']:
            mask=q<=ceiling;qq=q[mask];vv=ln[mask];w=np.exp(vv)
            cdf=cumulative_trapezoid(w,qq,initial=0);norm=cdf[-1];cdf/=norm
            cdf2=cumulative_trapezoid(w[::2],qq[::2],initial=0);norm2=cdf2[-1];cdf2/=norm2
            q95=float(np.interp(.95,cdf,qq));q95coarse=float(np.interp(.95,cdf2,qq[::2]));err=abs(q95/q95coarse-1)
            dz=abs(math.log(norm/norm2));converged=err<.005 and dz<.001
            posterior.append(dict(ceiling_in_tM=ceiling,prior='Uniform tau_source conditional on source mass',q_quantiles={str(k):float(np.interp(k,cdf,qq)) for k in [.5,.9,.95]},lnB_integrated=float(math.log(norm/ceiling)),q95_relative_grid_change=err,ln_integral_grid_change=dz,converged=converged))
        cross=np.flatnonzero(ln<=-math.log(100))
        cutoff=None
        if len(cross) and cross[0]>0:
            i=cross[0];cutoff=float(q[i-1]+(-math.log(100)-ln[i-1])*(q[i]-q[i-1])/(ln[i]-ln[i-1]))
        curves.append(dict(bandwidth_multiplier=bw,q=q.tolist(),lnB=ln.tolist(),reported_points={str(v):float(ln[np.argmin(abs(q-v))]) for v in registration['free_clock']['reported_points']},conditional_posteriors=posterior,first_lnB_minus_log100_crossing_q=cutoff))
        print('clock',bw,curves[-1]['reported_points'],flush=True)
    old=json.loads((ROOT/'C4_FREE_CLOCK.json').read_bytes())
    new('F2_FREE_CLOCK_EXTENDED.json',dict(**common,curves=curves,original_priors=[{k:r[k] for k in ['prior','quantiles','ln_evidence_free_clock_over_GR','bandwidth_controls']} for r in old['rows']],lower_endpoint_approximation=dict(exact_q_lower_max=float(ratios.max()),used_zero=True,reason='Sub floating-point effect at measured q; not a changed physical lower prior'),limitations=registration['free_clock']['limitations']+['Relative density crossing is not a posterior bound and is not physical exclusion while systematics gate fails'],elapsed_seconds=time.perf_counter()-start))
if __name__=='__main__':main()
