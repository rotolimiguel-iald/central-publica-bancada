"""Conditional 220-sector comparison across unique GWTC-5 pSEOB events.

Other modes keep each release's original treatment. In particular GW250114
marginalizes free 440 deviations, while other events fix them to zero. This
is not a joint Bayes factor for a theory modifying all radiative modes.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import argparse
import hashlib
import json
import math
import h5py
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.stats import gaussian_kde
from fetch_public import atomic_json
from posterior_220_readout import uniform_prior,ratio_pair
from tgl_ringdown_prediction import prediction

ROOT=Path(__file__).resolve().parent
READINGS=('R-A','R-B','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-LIN','R-MOD','R-GLOBAL')

def local_support(data):
    kde=gaussian_kde(data)
    w=np.exp(-.5*np.einsum('in,ij,jn->n',data,kde.inv_cov,data))
    return dict(kernel_effective_samples=float(w.sum()**2/np.sum(w*w)),
                samples_within_two_kernel_sd=int(np.sum(w>=np.exp(-2.))))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--bootstrap',type=int,default=200)
    args=parser.parse_args()
    regpath=ROOT/'REGISTRO_C4.json';reg=json.loads(regpath.read_bytes())
    regsha=hashlib.sha256(regpath.read_bytes()).hexdigest()
    if regsha not in (ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C4a_REGISTRO_POSTERIORES.md').read_text():
        raise ValueError('C4 registration mismatch')
    schema=json.loads((ROOT/'C4_CATALOG_SCHEMA.json').read_bytes())
    if schema['duplicates']:raise ValueError('Unresolved duplicate events')
    grid=json.loads((ROOT/'QNM_GRID.json').read_bytes());q=grid['modes']['220']
    interp=CubicSpline(q['spins'],np.array(q['real'])+1j*np.array(q['imag']),extrapolate=False)
    folder=ROOT/'cache/public/21454847/extracted/pSEOB/metafiles'
    cache=ROOT/'cache/catalog_220';cache.mkdir(exist_ok=True)
    codehash=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    deps={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
          ['tgl_ringdown_prediction.py','posterior_220_readout.py','QNM_GRID.json']}
    results=[]
    for index,row in enumerate(schema['rows']):
        outpath=cache/(row['event']+'.json')
        if outpath.exists():
            old=json.loads(outpath.read_bytes())
            if old['source_sha256']==row['sha256'] and old['code_sha256']==codehash and old['dependency_hashes']==deps:
                results.append(old);print(json.dumps(dict(event=row['event'],status='REUSED_VERIFIED_RESULT')),flush=True);continue
        path=folder/row['filename']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Source changed')
        with h5py.File(path,'r') as h:
            g=h[row['label']];s=g['posterior_samples'][()]
            pf,tpf=uniform_prior(g,'domega220');pt,tpt=uniform_prior(g,'dtau220')
        data=np.vstack([s['domega220'],s['dtau220']]);spin=s['final_spin_non_evolved']
        mass=s['final_mass_non_evolved'];redshift=s['redshift'];exact=interp(spin)
        if not np.all(np.isfinite(exact)):raise ValueError('Spin outside validated QNM range')
        rng=np.random.default_rng(13042026+index)
        train=rng.choice(len(s),int(.8*len(s)),replace=False);test=np.setdiff1d(np.arange(len(s)),train)
        tk=gaussian_kde(data[:,train]);density0=float(tk.logpdf([0,0])[0])
        hpd=float(np.mean(tk.logpdf(data[:,test])>=density0))
        support=local_support(data)
        readings=[]
        for reading in READINGS:
            predicted=[prediction(float(m),float(a),reading,redshift=float(z),
                         qnm_dimensionless=complex(w) if reading=='R-MOD' else None)
                       for m,a,z,w in zip(mass,spin,redshift,exact)]
            shift=np.array([p['delta_tau_ensemble_exact'] for p in predicted])
            if not pf[0]<0<pf[1] or np.any((shift<=pt[0])|(shift>=pt[1])):raise ValueError('Prior support failure')
            central,marginal=ratio_pair(data,shift)
            med=float(prediction(float(np.median(mass)),float(np.median(spin)),reading,
                 redshift=float(np.median(redshift)),
                 qnm_dimensionless=complex(interp(np.median(spin))) if reading=='R-MOD' else None)['delta_tau_ensemble_exact'])
            robust=[ratio_pair(data,shift,bw)[0] for bw in reg['KDE']['bandwidth_robustness_multipliers']]
            moved=data.copy();moved[1]-=shift;alt_support=local_support(moved)
            boot=[]
            if max(abs(shift))>1e-12:
                for _ in range(args.bootstrap):
                    inds=rng.integers(0,len(s),len(s))
                    boot.append(ratio_pair(data[:,inds],shift[inds])[0])
            else:boot=[0.]*args.bootstrap
            excluded=all(v<=-math.log(100) for v in robust) and hpd<=.95
            resolved=min(support['kernel_effective_samples'],alt_support['kernel_effective_samples'])>=100
            verdict='EXCLUDED_IN_READING' if excluded and resolved else 'NOT_EXCLUDED'
            if hpd>.95:verdict='INCONCLUSIVE_SYSTEMATICS'
            if not resolved:verdict='INCONCLUSIVE_DENSITY_SUPPORT'
            readings.append(dict(reading=reading,lnB=central,lnB_tau_marginal=marginal,
               lnB_median_spin=ratio_pair(data,np.full(len(s),med))[0],
               lnB_bandwidth=robust,bootstrap_N=len(boot),
               lnB_bootstrap_025_50_975=np.quantile(boot,[.025,.5,.975]).tolist(),
               shift_05_50_95=np.quantile(shift,[.05,.5,.95]).tolist(),
               gamma_over_omega_05_50_95=np.quantile([p['gamma_over_omega'] for p in predicted],[.05,.5,.95]).tolist(),
               median_prediction=prediction(float(np.median(mass)),float(np.median(spin)),reading,
                   redshift=float(np.median(redshift)),qnm_dimensionless=complex(interp(np.median(spin))) if reading=='R-MOD' else None),
               z_tau_gaussian_diagnostic=(float(np.median(data[1]))-med)/float(np.std(data[1],ddof=1)),
               correction_over_sigma=abs(med)/float(np.std(data[1],ddof=1)),
               support=alt_support,verdict=verdict,
               scope='CONDITIONAL_220_ENSEMBLE__OTHER_MODES_AS_IN_RELEASE__NOT_FULL_TGL'))
        result=dict(event=row['event'],N=len(s),source_sha256=row['sha256'],code_sha256=codehash,
            dependency_hashes=deps,registration_sha256=regsha,
            prior_df=tpf,prior_dtau=tpt,prior_density_ratio=1.,
            higher_modes='440_FREE_NUISANCE' if np.std(s['dtau440'])>0 else 'HIGHER_MODE_DEVIATIONS_FIXED_TO_GR',
            quantiles={k:np.quantile(v,[.05,.5,.95]).tolist() for k,v in
                       [('spin',spin),('mass_detector',mass),('redshift',redshift),('df220',data[0]),('dtau220',data[1])]},
            GR_HPD_content=hpd,GR_HPD_MC_se=math.sqrt(hpd*(1-hpd)/len(test)),
            GR_inside_95=hpd<=.95,GR_support=support,rows=readings)
        atomic_json(outpath,result);results.append(result)
        print(json.dumps(dict(event=row['event'],N=len(s),GR_HPD=hpd,
                     lnB={r['reading']:r['lnB'] for r in readings})),flush=True)
    sums=[]
    for reading in READINGS:
        selected=[next(x for x in row['rows'] if x['reading']==reading) for row in results]
        without=[x for row,x in zip(results,selected) if row['event']!='GW250114_082203']
        sums.append(dict(reading=reading,lnB_conditional_sector_sum=sum(x['lnB'] for x in selected),
              lnB_without_GW250114=sum(x['lnB'] for x in without),
              lnB_bandwidth_sums=np.sum([x['lnB_bandwidth'] for x in selected],axis=0).tolist(),
              verdict='PENDING_CATALOG_GR_HPD_AND_MODEL_SYSTEMATICS',
              not_sigma='A Bayes factor is not a sigma significance'))
    atomic_json(ROOT/'C4_CATALOG_220.json',dict(status='CONDITIONAL_SECTOR_CATALOG__NOT_COMPLETE',
              N_events=len(results),N_posterior_draws=sum(r['N'] for r in results),
              duplicate_policy='GW250114 included once; no multiplication by older overlapping releases',
              rows=results,catalog=sums,not_done=['Joint common-deformation GR HPD',
                   'pyRing robustness','Full physical higher-mode modification','Remnant-fit robustness']))
    print(json.dumps(dict(catalog=sums)),flush=True)

if __name__=='__main__':main()
