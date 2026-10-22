"""Initial 220-only posterior comparison with shared free 440 nuisance sector.

Exact density identity for a spin-dependent curve and uniform independent
deformation priors: B = p(df,dtau-g(spin)|d)(0,0)/p(df,dtau|d)(0,0).
The shear transformation has Jacobian one; it is not mean conditional ratios.
KDE and bootstrap approximate those densities. This does NOT set the 440
deviations to GR or to TGL; this scope is explicit in every reported ratio.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import hashlib
import json
import math
import re
import h5py
import numpy as np
from scipy.stats import gaussian_kde
from fetch_public import atomic_json
from tgl_ringdown_prediction import prediction

ROOT=Path(__file__).resolve().parent

def uniform_prior(group,name):
    key='priors/analytic/'+name
    if key in group:
        txt=group[key][0].decode()
    else:
        texts=[]
        if 'config_file' in group:
            def visit(path,item):
                if isinstance(item,h5py.Dataset) and 'prior' in path.lower():
                    texts.extend(v.decode() for v in np.atleast_1d(item[()]) if isinstance(v,bytes))
            group['config_file'].visititems(visit)
        matches=[]
        for text in texts:
            matches.extend(re.findall(r'\b'+re.escape(name)+r'\s*=\s*(Uniform\([^)]*\))',text))
        if not matches or len(set(matches))!=1:raise ValueError('Missing or ambiguous prior for '+name)
        txt=matches[0]
    if not txt.startswith('Uniform('):raise ValueError('Nonuniform prior: '+txt)
    lo=re.search(r'\bminimum=([\-\d.]+)',txt);hi=re.search(r'\bmaximum=([\-\d.]+)',txt)
    if not lo or not hi:raise ValueError('Unparsed Uniform: '+txt)
    return (float(lo[1]),float(hi[1])),txt

def ratio_pair(data,shift,bwmult=1.):
    base=gaussian_kde(data,bw_method=lambda k:k.scotts_factor()*bwmult)
    moved=data.copy();moved[1]-=shift
    alt=gaussian_kde(moved,bw_method=lambda k:k.scotts_factor()*bwmult)
    logb=float(alt.logpdf([0.,0.])[0]-base.logpdf([0.,0.])[0])
    mb=gaussian_kde(data[1],bw_method=lambda k:k.scotts_factor()*bwmult)
    ma=gaussian_kde(moved[1],bw_method=lambda k:k.scotts_factor()*bwmult)
    return logb,float(ma.logpdf([0.])[0]-mb.logpdf([0.])[0])

def main():
    regpath=ROOT/'REGISTRO_C4.json'
    reg=json.loads(regpath.read_bytes());rh=hashlib.sha256(regpath.read_bytes()).hexdigest()
    if rh not in (ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C4a_REGISTRO_POSTERIORES.md').read_text():
        raise ValueError('Registration not identical to return-tunnel receipt')
    path=ROOT/'cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr/posterior_samples.h5'
    schema=json.loads((ROOT/'C4_SCHEMA.json').read_bytes())
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    if sha!=schema['h5_sha256']:raise ValueError('Posterior source changed')
    with h5py.File(path,'r') as h:
        group=h['pSEOBNRv5PHM']
        pf,tpf=uniform_prior(group,'domega220');pt,tpt=uniform_prior(group,'dtau220')
        prior_config=group['config_file/config/prior_dict'][0].decode()
        samples=group['posterior_samples'][()]
    df,dtau=samples['domega220'],samples['dtau220']
    spin=samples['final_spin_non_evolved'];mass=samples['final_mass_non_evolved']
    data=np.vstack([df,dtau])
    assert np.all(np.isfinite(data)) and np.all((spin>=0)&(spin<1))
    seed=13042026;rng=np.random.default_rng(seed)
    out=[]
    # Primary R-B, root vacuum-to-one and linear-gap conditional readings.
    # Exact modular QNM/region and propagation mappings are separate pending work.
    for reading in ['R-B','R-RAIZ-0','R-LIN']:
        shift=np.array([prediction(float(m),float(a),reading)['delta_tau_ensemble_exact'] for m,a in zip(mass,spin)])
        if not pf[0]<0<pf[1] or not np.all((shift>pt[0])&(shift<pt[1])):
            raise ValueError('Restricted model falls outside broad-model prior support')
        central,marginal=ratio_pair(data,shift)
        medshift=float(prediction(float(np.median(mass)),float(np.median(spin)),reading)['delta_tau_ensemble_exact'])
        median_case=ratio_pair(data,np.full(len(shift),medshift))[0]
        robustness=[dict(multiplier=bw,lnB_joint=ratio_pair(data,shift,bw)[0])
                    for bw in reg['KDE']['bandwidth_robustness_multipliers']]
        boot=[]
        for _ in range(reg['KDE']['bootstrap_replicates']):
            inds=rng.integers(0,len(df),len(df))
            boot.append(ratio_pair(data[:,inds],shift[inds])[0])
        row=dict(reading=reading,lnB_joint_spin_curve=central,lnB_tau_marginal=marginal,
                 joint_minus_tau=central-marginal,lnB_fixed_median_spin=median_case,
                 shift_quantiles_05_50_95=np.quantile(shift,[.05,.5,.95]).tolist(),
                 correction_over_marginal_sigma=abs(float(np.median(shift)))/float(np.std(dtau,ddof=1)),
                 lnB_bootstrap_025_50_975=np.quantile(boot,[.025,.5,.975]).tolist(),
                 bandwidth=robustness,verdict='PRELIMINARY_DENSITY_RATIO__NOT_C4_COMPLETE',
                 hypothesis_scope='Reading220 versus GR220, with identical free 440 priors marginalized',
                 physical_scope='Only if coherence-ensemble damping is the actual observable',
                 remnant_map='PESummary final_spin_non_evolved and final_mass_non_evolved; remnant-fit robustness pending')
        out.append(row);print(json.dumps(row),flush=True)
    doc=dict(status='PARTIAL_CURRENT_POSTERIOR_COMPARISON',source_sha256=sha,
             registration_sha256=rh,N=len(df),seed=seed,posterior_equal_weight_assumption='PESummary posterior_samples',
             priors=dict(df=tpf,dtau=tpt,config_text=prior_config,point_prior_ratio=1.),
             quantiles={name:np.quantile(values,[.05,.5,.95]).tolist() for name,values in
                        [('df220',df),('dtau220',dtau),('spin_non_evolved',spin),('mass_det_non_evolved',mass)]},
             rows=out,not_done=['KDE tail/local-support calibration and 95% GR HPD check',
                   'R-MOD exact mode prediction on posterior spin grid','pyRing robustness','Catalogue combination',
                   'Free tau bounds','Full 220+440 physical hypotheses','Remnant-fit version robustness',
                   'Independent 3D density-integral oracle'])
    atomic_json(ROOT/'C4_220_INITIAL.json',doc)
    print(json.dumps({'N':len(df),'quantiles':doc['quantiles']}),flush=True)

if __name__=='__main__':main()
