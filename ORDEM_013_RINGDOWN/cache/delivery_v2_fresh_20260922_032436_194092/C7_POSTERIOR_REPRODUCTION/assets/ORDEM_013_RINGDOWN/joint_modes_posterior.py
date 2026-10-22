"""GW250114 joint 220+440 constrained-model evidence, conditional ensemble reading.

No product of marginal tests on the same event. Four deformation coordinates
are constrained together. Remaining IMR modes retain the release's treatment;
this is still not an all-mode theory likelihood. The mode-wise extension is
an explicit physical hypothesis, not a consequence of naming the generator.
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
from scipy.interpolate import CubicSpline
from scipy.stats import gaussian_kde
from fetch_public import atomic_json
from posterior_220_readout import uniform_prior, ratio_pair
from catalog_220_readout import local_support, READINGS
from tgl_ringdown_prediction import prediction

ROOT=Path(__file__).resolve().parent

def log_ratio(data,shift,bw=1.):
    null=gaussian_kde(data,bw_method=lambda k:k.scotts_factor()*bw)
    alt=gaussian_kde(data-shift,bw_method=lambda k:k.scotts_factor()*bw)
    return float(alt.logpdf(np.zeros(data.shape[0]))[0]-null.logpdf(np.zeros(data.shape[0]))[0])

def main():
    regpath=ROOT/'REGISTRO_C4.json';reg=json.loads(regpath.read_bytes())
    regsha=hashlib.sha256(regpath.read_bytes()).hexdigest()
    if regsha not in (ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C4a_REGISTRO_POSTERIORES.md').read_text():
        raise ValueError('C4 registration changed')
    path=ROOT/'cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr/posterior_samples.h5'
    source_sha=hashlib.sha256(path.read_bytes()).hexdigest()
    if source_sha!=json.loads((ROOT/'C4_SCHEMA.json').read_bytes())['h5_sha256']:
        raise ValueError('Posterior source changed')
    names=('domega220','dtau220','domega440','dtau440')
    with h5py.File(path,'r') as h:
        g=h['pSEOBNRv5PHM'];s=g['posterior_samples'][()]
        priors={n:uniform_prior(g,n) for n in names}
    data=np.vstack([s[n] for n in names]);spin=s['final_spin_non_evolved']
    mass=s['final_mass_non_evolved'];redshift=s['redshift']
    if not np.all(np.isfinite(data)):raise ValueError('Non-finite posterior')
    grid=json.loads((ROOT/'QNM_GRID.json').read_bytes())
    interps={}
    for mode in ('220','440'):
        q=grid['modes'][mode]
        interps[mode]=CubicSpline(q['spins'],np.array(q['real'])+1j*np.array(q['imag']),extrapolate=False)
    values={m:f(spin) for m,f in interps.items()}
    if any(not np.all(np.isfinite(v)) for v in values.values()):raise ValueError('Uncovered spin')
    rng=np.random.default_rng(13042700)
    test=rng.choice(len(s),min(5000,len(s)//5),replace=False)
    train=np.setdiff1d(np.arange(len(s)),test)
    hpd_controls=[]
    for bw in (.7,1.,1.4):
        kd=gaussian_kde(data[:,train],bw_method=lambda k:k.scotts_factor()*bw)
        hpd=float(np.mean(kd.logpdf(data[:,test])>=kd.logpdf(np.zeros(4))[0]))
        hpd_controls.append(dict(bandwidth=bw,GR_HPD_content=hpd,
                                 MC_standard_error=math.sqrt(hpd*(1-hpd)/len(test))))
    null_support=local_support(data)
    rows=[];shifts={}
    for reading in READINGS:
        shifted=np.zeros_like(data)
        for j,mode in enumerate(('220','440')):
            ell=int(mode[0]);tuple_mode=(ell,ell,0)
            for i,(m,a,z,w) in enumerate(zip(mass,spin,redshift,values[mode])):
                p=prediction(float(m),float(a),reading,redshift=float(z),mode=tuple_mode,
                             qnm_dimensionless=complex(w) if reading=='R-MOD' or ell==4 else None)
                shifted[2*j+1,i]=p['delta_tau_ensemble_exact']
        for coordinate,name in enumerate(names):
            lo,hi=priors[name][0]
            if not lo<0<hi or np.any((shifted[coordinate]<=lo)|(shifted[coordinate]>=hi)):
                raise ValueError('Restricted model leaves broad prior support')
        shifts[reading]=shifted
        central=log_ratio(data,shifted)
        robust=[log_ratio(data,shifted,bw) for bw in reg['KDE']['bandwidth_robustness_multipliers']]
        boot=[]
        if np.max(abs(shifted))>1e-12:
            for _ in range(reg['KDE']['bootstrap_replicates']):
                ix=rng.integers(0,len(s),len(s));boot.append(log_ratio(data[:,ix],shifted[:,ix]))
        else:boot=[0.]*reg['KDE']['bootstrap_replicates']
        support=local_support(data-shifted)
        resolved=min(null_support['kernel_effective_samples'],support['kernel_effective_samples'])>=100
        gr_inside=all(r['GR_HPD_content']+3*r['MC_standard_error']<.95 for r in hpd_controls)
        verdict='EXCLUDED_IN_READING' if all(r<=-math.log(100) for r in robust) and gr_inside else 'NOT_EXCLUDED'
        if not gr_inside:verdict='INCONCLUSIVE_SYSTEMATICS'
        if not resolved:verdict='INCONCLUSIVE_DENSITY_SUPPORT'
        marginals=[ratio_pair(data[2*j:2*j+2],shifted[2*j+1])[0] for j in (0,1)]
        result=dict(reading=reading,lnB_joint_220_440=central,lnB_bandwidth=robust,
             lnB_bootstrap_025_50_975=np.quantile(boot,[.025,.5,.975]).tolist(),
             lnB_product_of_two_marginals_DIAGNOSTIC_ONLY=sum(marginals),
             joint_minus_marginal_product=central-sum(marginals),
             shift_220_05_50_95=np.quantile(shifted[1],[.05,.5,.95]).tolist(),
             shift_440_05_50_95=np.quantile(shifted[3],[.05,.5,.95]).tolist(),
             support=support,verdict=verdict)
        rows.append(result);print(json.dumps(result),flush=True)
    # Independent 5D KDE integral over spin; same bandwidth exponent as 4D KDE.
    factor=len(s)**(-1/8)
    kd5=gaussian_kde(np.vstack([data,spin]),bw_method=factor)
    kd4=gaussian_kde(data,bw_method=factor)
    lower=max(0,float(spin.min()-8*np.sqrt(kd5.covariance[4,4])))
    upper=min(.98,float(spin.max()+8*np.sqrt(kd5.covariance[4,4])))
    quadratures=[]
    for size in (128,256):
        nodes,weights=np.polynomial.legendre.leggauss(size)
        points=(nodes+1)*(upper-lower)/2+lower
        curve=np.zeros((5,size));curve[-1]=points
        for j,mode in enumerate(('220','440')):
            ell=int(mode[0])
            curve[2*j+1]=[prediction(68.1,float(a),'R-B',mode=(ell,ell,0),
                    qnm_dimensionless=complex(interps[mode](a)) if ell==4 else None)
                    ['delta_tau_ensemble_exact'] for a in points]
        null=curve.copy();null[:4]=0
        z0=float(np.sum(weights*kd5(null))*(upper-lower)/2)
        z1=float(np.sum(weights*kd5(curve))*(upper-lower)/2)
        quadratures.append(dict(nodes=size,lnB=math.log(z1/z0),
            relative_GR_marginal_error=abs(z0/float(kd4(np.zeros(4))[0])-1)))
    if abs(quadratures[-1]['lnB']-quadratures[-2]['lnB'])>1e-5:
        raise ValueError('Independent joint-mode quadrature unresolved')
    estimated=next(r for r in rows if r['reading']=='R-B')['lnB_joint_220_440']
    difference=quadratures[-1]['lnB']-estimated
    if abs(difference)>.02:raise ValueError('Residual-KDE approximation fails independent curve integral')
    out=dict(status='JOINT_220_440_CONDITIONAL_COMPARISON',event='GW250114',N=len(s),
        source_sha256=source_sha,registration_sha256=regsha,priors=priors,
        uniform_independent_prior_density_ratio=1.,GR_HPD_controls=hpd_controls,GR_support=null_support,
        posterior_correlation_matrix=np.corrcoef(data).tolist(),rows=rows,
        independent_five_dimensional_KDE_quadrature=quadratures,
        quadrature_minus_residual_KDE_logB=difference,
        scope='Mode-wise ensemble extension imposed simultaneously on 220 and 440. All other IMR modes retain the source analysis treatment. Not a complete all-mode TGL/GR likelihood.',
        hypothesis_status='CONJECTURE: the same physical clock law governs both effective oscillator modes; no identification of classical unraveling is proved',
        no_double_count='Do not multiply this by 220-only, 440-only, or pyRing evidence from the same event',
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        dependencies={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in
                      ('tgl_ringdown_prediction.py','QNM_GRID.json','posterior_220_readout.py')})
    atomic_json(ROOT/'C4_JOINT_MODES.json',out)
    print(json.dumps(dict(GR_HPD=hpd_controls,GR_support=null_support,quadrature_difference=difference)),flush=True)

if __name__=='__main__':main()
