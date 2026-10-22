"""Independent density-curve quadrature and Leaver/qnm cross-checks."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import hashlib
import json
import h5py
import numpy as np
from scipy.stats import gaussian_kde
from fetch_public import atomic_json
from tgl_ringdown_prediction import prediction

ROOT=Path(__file__).resolve().parent

def main():
    direct=json.loads((ROOT/'refeito/leaver_kerr_result.json').read_bytes())
    qnm=json.loads((ROOT/'FISHER_INPUTS.json').read_bytes())
    comparisons=[]
    for row in qnm['mode_220']:
        # Manager oracle used spin .671219, not .6712194217379245.
        if abs(row['spin']-.6712194217379245)<1e-14:continue
        other=direct[f"{row['spin']:.6f}"]
        error=abs(complex(row['omega_real'],row['omega_imag'])-
                  complex(other['M_omega_R'],other['M_omega_I']))
        assert error<1e-9
        comparisons.append(dict(spin=row['spin'],absolute_difference=error,leaver_residual=other['resid']))
    base=ROOT/'cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr'
    path=base/'posterior_samples.h5'
    with h5py.File(path,'r') as h:samples=h['pSEOBNRv5PHM/posterior_samples'][()]
    df,dtau,spin=[samples[k] for k in ['domega220','dtau220','final_spin_non_evolved']]
    n=len(df);factor=n**(-1/6)
    density3=gaussian_kde(np.vstack([df,dtau,spin]),bw_method=factor)
    density2=gaussian_kde(np.vstack([df,dtau]),bw_method=factor)
    lower=max(0,float(spin.min()-8*np.sqrt(density3.covariance[2,2])))
    upper=min(.999,float(spin.max()+8*np.sqrt(density3.covariance[2,2])))
    quadratures=[]
    for count in [128,256]:
        points,weights=np.polynomial.legendre.leggauss(count)
        sg=(points+1)*(upper-lower)/2+lower
        shift=np.array([prediction(68.1,float(a),'R-B')['delta_tau_ensemble_exact'] for a in sg])
        alt=np.sum(weights*density3(np.vstack([np.zeros(count),shift,sg])))*(upper-lower)/2
        null=np.sum(weights*density3(np.vstack([np.zeros(count),np.zeros(count),sg])))*(upper-lower)/2
        exact_null=float(density2([0,0])[0])
        quadratures.append(dict(nodes=count,lnB=float(np.log(alt/null)),
                            relative_null_marginal_error=float(abs(null-exact_null)/exact_null)))
    assert abs(quadratures[-1]['lnB']-quadratures[-2]['lnB'])<1e-5
    initial=json.loads((ROOT/'C4_220_INITIAL.json').read_bytes())
    approx=next(r['lnB_joint_spin_curve'] for r in initial['rows'] if r['reading']=='R-B')
    difference=quadratures[-1]['lnB']-approx
    assert abs(difference)<.02
    # Held-out posterior draws estimate enclosed HPD content through the GR
    # point. This is a Monte Carlo credible-region check, not a p-value.
    rng=np.random.default_rng(213041)
    ids=rng.permutation(n);train=ids[:int(.8*n)];test=ids[int(.8*n):]
    p=gaussian_kde(np.vstack([df[train],dtau[train]]))
    pgr=float(p([0,0])[0]);pred=p(np.vstack([df[test],dtau[test]]))
    content=float(np.mean(pred>pgr));se=float(np.sqrt(content*(1-content)/len(test)))
    mahal=np.einsum('in,ij,jn->n',np.vstack([df,dtau]),np.linalg.inv(density2.covariance),np.vstack([df,dtau]))
    weights=np.exp(-mahal/2);ess=float(weights.sum()**2/(weights@weights))
    report=dict(status='INDEPENDENT_ORACLES_PASS__C4_STILL_PARTIAL',
        posterior_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        qnm_vs_leaver=comparisons,spin_curve_quadrature=quadratures,
        quadrature_minus_residual_KDE_logB=difference,
        GR_220_95_region=dict(hpd_content_through_GR=content,MC_standard_error=se,
               inside_95=bool(content+3*se<.95),held_out_samples=len(test),
               interpretation='GR220 point with the free-440 nuisance sector; not a full-GR test'),
        local_GR_KDE_support=dict(kernel_weight_ESS=ess,within_two_kernel_sigmas=int(np.sum(mahal<=4))),
        not_done=['pyRing and remnant-fit robustness','R-MOD full posterior','Catalogue','Full 220+440 hypotheses'])
    atomic_json(ROOT/'C4_VALIDATION.json',report)
    print(json.dumps(report),flush=True)

if __name__=='__main__':main()
