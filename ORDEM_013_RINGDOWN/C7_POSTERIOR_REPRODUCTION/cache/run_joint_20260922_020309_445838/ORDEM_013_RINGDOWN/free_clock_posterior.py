"""Integrate the registered free source clock, retaining joint remnant samples.

The auxiliary coordinate u is uniform on [0,1] under either conditional prior:
tau=tP+u*(tM_source-tP), or tau=tP*exp(u*log(tM_source/tP)).
KDE density at the constrained surface supplies sample-wise nuisance weights.
Integrate those weights before normalizing. This is not a point Bayes factor,
nor an average of conditional point ratios. All results are 220-sector only.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import hashlib
import json
import math
import h5py
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import brentq
from scipy.stats import gaussian_kde
from fetch_public import atomic_json
from posterior_220_readout import uniform_prior
from tgl_ringdown_prediction import prediction

ROOT=Path(__file__).resolve().parent

def kernel_weights(data, bandwidth):
    kde=gaussian_kde(data,bw_method=lambda k:k.scotts_factor()*bandwidth)
    quadratic=np.einsum('in,ij,jn->n',data,kde.inv_cov,data)
    weights=np.exp(-quadratic/2)/(len(data.T)*2*math.pi*math.sqrt(np.linalg.det(kde.covariance)))
    residual=abs(weights.sum()/float(kde([0,0])[0])-1)
    if residual>1e-12:
        raise ValueError('Independent covariance density disagrees with scipy KDE')
    return weights,residual

def integrate(data,x_b,tm_source,tp,prior,bandwidth,size):
    u=np.linspace(0,1,size)
    log_span=np.log(tm_source/tp)
    all_weights=np.empty((size,len(tm_source)))
    residuals=[]
    for index,coordinate in enumerate(u):
        tau=(tp+coordinate*(tm_source-tp) if prior=='uniform'
             else tp*np.exp(coordinate*log_span))
        x=x_b*tau/tm_source
        shift=-x/(1+x)
        moved=data.copy();moved[1]-=shift
        all_weights[index],residual=kernel_weights(moved,bandwidth)
        residuals.append(residual)
    integrated=cumulative_trapezoid(all_weights,u,axis=0,initial=0.)
    z=float(integrated[-1].sum())
    z_gr=float(all_weights[0].sum()) # Planck endpoint is numerically GR at this resolution.
    columns=np.arange(len(tm_source));du=u[1]-u[0]
    def cdf_from_coordinates(cuts):
        cuts=np.broadcast_to(np.clip(cuts,0,1),tm_source.shape)
        lo=np.minimum((cuts/du).astype(int),size-2)
        delta=cuts-u[lo]
        wl=all_weights[lo,columns];wr=all_weights[lo+1,columns]
        pieces=integrated[lo,columns]+delta*(wl+.5*delta/du*(wr-wl))
        return float(pieces.sum()/z)
    def physical_cdf(log_tau):
        cuts=((math.exp(log_tau)-tp)/(tm_source-tp) if prior=='uniform'
              else (log_tau-math.log(tp))/log_span)
        return cdf_from_coordinates(cuts)
    quantiles={}
    for q in (.5,.9,.95):
        coord=brentq(lambda a:cdf_from_coordinates(a)-q,0,1,xtol=1e-12)
        log_tau=brentq(lambda a:physical_cdf(a)-q,math.log(tp),math.log(float(max(tm_source))),xtol=1e-11)
        quantiles[str(q)]=dict(prior_coordinate=coord,tau_source_s=math.exp(log_tau))
    if abs(cdf_from_coordinates(0.))>1e-14 or abs(cdf_from_coordinates(1.)-1)>1e-12:
        raise ValueError('Integrated CDF not normalized')
    return dict(prior=prior,bandwidth=bandwidth,grid_size=size,
        ln_evidence_free_clock_over_GR=math.log(z/z_gr),quantiles=quantiles,
        density_oracle_max_relative_error=max(residuals),
        log_likelihood_ratio_range=[float(np.log(all_weights.sum(axis=1)/z_gr).min()),
                                    float(np.log(all_weights.sum(axis=1)/z_gr).max())],
        prior_coordinate=u.tolist(),log_marginal_likelihood=np.log(all_weights.sum(axis=1)/z_gr).tolist(),
        posterior_coordinate_cdf=(integrated.sum(axis=1)/z).tolist(),
        interpretation='Uniform u prior in both cases; physical clock upper limits are conditional on chosen mass-dependent bounds')

def main():
    regpath=ROOT/'REGISTRO_C4.json';reg=json.loads(regpath.read_bytes())
    regsha=hashlib.sha256(regpath.read_bytes()).hexdigest()
    if regsha not in (ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C4a_REGISTRO_POSTERIORES.md').read_text():
        raise ValueError('C4 registration mismatch')
    path=ROOT/'cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr/posterior_samples.h5'
    source_sha=hashlib.sha256(path.read_bytes()).hexdigest()
    if source_sha!=json.loads((ROOT/'C4_SCHEMA.json').read_bytes())['h5_sha256']:
        raise ValueError('Posterior source changed')
    with h5py.File(path,'r') as h:
        group=h['pSEOBNRv5PHM'];s=group['posterior_samples'][()]
        pf,tpf=uniform_prior(group,'domega220');pt,tpt=uniform_prior(group,'dtau220')
    data=np.vstack([s['domega220'],s['dtau220']])
    predicted=[prediction(float(m),float(a),'R-B',redshift=float(z)) for m,a,z in
               zip(s['final_mass_non_evolved'],s['final_spin_non_evolved'],s['redshift'])]
    tm_source=np.array([p['t_mass_s']/(1+p['redshift']) for p in predicted])
    tp=predicted[0]['t_planck_s'];xb=np.array([p['x'] for p in predicted])
    if not pf[0]<0<pf[1] or np.any(-xb/(1+xb)<=pt[0]) or pt[1]<=0:
        raise ValueError('Continuous prior curve leaves broad-model prior support')
    rows=[]
    for prior in ('uniform','log_uniform'):
        attempts=[]
        previous=None
        for size in (129,257,513,1025):
            result=integrate(data,xb,tm_source,tp,prior,1.,size)
            metrics=dict(grid_size=size,ln_evidence=result['ln_evidence_free_clock_over_GR'],quantiles=result['quantiles'])
            if previous is not None:
                err=max(abs(result['quantiles'][q]['tau_source_s']/previous['quantiles'][q]['tau_source_s']-1) for q in ('0.9','0.95'))
                dz=abs(result['ln_evidence_free_clock_over_GR']-previous['ln_evidence_free_clock_over_GR'])
                metrics.update(upper_limit_relative_change=err,ln_evidence_change=dz)
                attempts.append(metrics)
                if err<1e-3 and dz<1e-5:
                    break
            else:attempts.append(metrics)
            previous=result
        else:
            atomic_json(ROOT/'C4_FREE_CLOCK_UNRESOLVED.json',dict(prior=prior,attempts=attempts))
            raise ValueError('Clock quadrature unresolved; preserve attempted result')
        controls=[]
        for bw in (.7,1.4):
            control=integrate(data,xb,tm_source,tp,prior,bw,size)
            controls.append({k:control[k] for k in ('bandwidth','grid_size','quantiles','ln_evidence_free_clock_over_GR')})
        result.update(convergence=attempts,bandwidth_controls=controls)
        rows.append(result)
        print(json.dumps({k:result[k] for k in ('prior','grid_size','quantiles','ln_evidence_free_clock_over_GR','convergence','bandwidth_controls')}),flush=True)
    out=dict(status='CONDITIONAL_FREE_CLOCK_MARGINALIZATION__NOT_POINT_BAYES_FACTOR',
        event='GW250114',N=len(s),source_sha256=source_sha,registration_sha256=regsha,
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        prediction_sha256=hashlib.sha256((ROOT/'tgl_ringdown_prediction.py').read_bytes()).hexdigest(),
        broad_priors=[tpf,tpt],point_prior_ratio=1.,
        physical_clock_bounds=dict(lower_s=tp,upper='tM_source for each nuisance sample',
                                   tM_source_05_50_95=np.quantile(tm_source,[.05,.5,.95]).tolist()),
        scope='220 ensemble amplitude under quadratic generator; 440 is free nuisance in both hypotheses',
        method='Joint spin/mass/redshift samples; integrate individual residual-KDE kernel weights in prior coordinate before normalizing; source-clock CDF integrates each sample only to its own clock threshold',
        rows=rows,not_done=['Shared universal clock across catalogue', 'Full multi-mode clock likelihood'])
    atomic_json(ROOT/'C4_FREE_CLOCK.json',out)

if __name__=='__main__':main()
