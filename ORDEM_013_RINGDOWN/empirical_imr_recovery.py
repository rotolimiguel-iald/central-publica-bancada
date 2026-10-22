"""C5 injections into held-out H1/L1 data, with two independent IMR families.

Effective ensemble hypothesis: damp the isolated 22 and 44 spherical-harmonic
IMR contributions after their common 22 peak. This acts on all overtones in
each harmonic; it is NOT a claimed derivation of a full modified-gravity IMR.
Recovery uses fundamental 220+440, fixed true remnant, free detector-wise
complex amplitudes. Other IMR modes remain in injections as model discrepancy.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.interpolate import CubicSpline
from fetch_public import atomic_json
from tgl_ringdown_prediction import prediction, scales
from tgl_ringdown_likelihood import linear_statistics,profile_intervals

ROOT=Path(__file__).resolve().parent
READINGS=['R-A','R-B','R-RAIZ-0','R-RAIZ-EP4','R-RAIZ-REST','R-LIN','R-MOD','R-GLOBAL']

def main():
    source=json.loads((ROOT/'C5_IMR_CONTROLS.json').read_bytes())
    noise_meta=json.loads((ROOT/'C5_EMPIRICAL_NOISE.json').read_bytes())
    qgrid=json.loads((ROOT/'QNM_GRID.json').read_bytes())['modes']
    modes={k:CubicSpline(v['spins'],np.asarray(v['real'])+1j*np.asarray(v['imag']),extrapolate=False)
           for k,v in qgrid.items() if k in ('220','440')}
    caches={d:np.load(ROOT/'cache/empirical_noise'/f'{d}_noise.npz') for d in ('H1','L1')}
    for row in noise_meta['detectors']:
        p=ROOT/'cache/empirical_noise'/f"{row['detector']}_noise.npz"
        if hashlib.sha256(p.read_bytes()).hexdigest()!=row['cache_sha256']:raise ValueError('Noise cache changed')
    whitening={d:caches[d]['whitener_scaled'] for d in caches}
    # Selection fixed by position, not by noise residual or recovered parameters.
    selected=np.arange(50)
    noise={d:caches[d]['held_out_strain_scaled'][selected]@whitening[d].T for d in caches}
    times=np.arange(caches['H1']['held_out_strain_scaled'].shape[1])/2048.
    responses={'H1':(.7,.2),'L1':(-.3,.8)}
    results=[]
    for family,start_tm in [(f,s) for f in source['families'] for s in (6.,8.,10.,10.5,12.)]:
        p=ROOT/'cache/imr_controls'/f"{family['family']}.npz"
        if hashlib.sha256(p.read_bytes()).hexdigest()!=family['sha256']:raise ValueError('IMR control changed')
        waveform=np.load(p)
        mass,spin=family['remnant_mass_detector_solar'],family['remnant_spin']
        start=start_tm*scales(mass,'CODATA2018_IAU2015')[0]
        time_peak=start+times
        components={key:np.interp(time_peak,waveform['time_from_peak_s'],waveform[key])*1e21
                    for key in ('22_plus','22_cross','44_plus','44_cross','other_plus','other_cross')}
        for reading in READINGS:
            predicted=[prediction(mass,spin,reading,mode=mode,
                 qnm_dimensionless=complex(modes[str(mode[0])+str(mode[1])+'0'](spin)))
                       for mode in ((2,2,0),(4,4,0))]
            omega=np.array([x['omega_rad_s'] for x in predicted])
            decay=np.array([1/x['tau_gr_s'] for x in predicted])
            gamma=np.array([x['gamma_per_s'] for x in predicted])
            x=gamma/decay
            # tiny or identically zero signals have no identifiable a in [0,1].
            unresolved=bool(np.max(x)<1e-12)
            maxx=float(np.max(x))
            if unresolved:
                agrid=np.array([0.,1.])
            else:
                agrid=np.unique(np.r_[np.linspace(-.8,2.,1001)/maxx,0.,1.])
            damping=decay[None,:]+agrid[:,None]*gamma[None,:]
            if np.any(damping<=0):raise ValueError('Diagnostic grid gives growing ringdown')
            env=np.exp(-damping[:,:,None]*times[None,None,:])
            raw=np.stack([env[:,0,:]*np.cos(omega[0]*times),env[:,0,:]*np.sin(omega[0]*times),
                          env[:,1,:]*np.cos(omega[1]*times),env[:,1,:]*np.sin(omega[1]*times)],axis=-1)
            bases={d:np.einsum('kt,gti->gki',whitening[d],raw,optimize=True) for d in caches}
            for snr in (20.,40.,80.):
                for injected in (0.,1.):
                    signals={}
                    for detector,(fp,fc) in responses.items():
                        y=fp*components['other_plus']+fc*components['other_cross']
                        for j,name in enumerate(('22','44')):
                            y=y+(fp*components[name+'_plus']+fc*components[name+'_cross'])*np.exp(-injected*gamma[j]*time_peak)
                        signals[detector]=whitening[detector]@y
                    norm=np.sqrt(sum(np.dot(y,y) for y in signals.values()))
                    scale=snr/norm
                    target={d:noise[d]+signals[d][None,:]*scale for d in caches}
                    profiles=[];marginals=[];clean_profiles=[]
                    for d in caches:
                        prof,marg=linear_statistics(bases[d],target[d],amplitude_prior_sd=10.)
                        profiles.append(prof);marginals.append(marg)
                        clean_profiles.append(linear_statistics(bases[d],signals[d][None,:]*scale,10.)[0])
                    profile=sum(profiles);marginal=sum(marginals)
                    zero=int(np.flatnonzero(agrid==0.)[0]);one=int(np.flatnonzero(agrid==1.)[0])
                    logB=marginal[one]-marginal[zero]
                    row=dict(family=family['family'],reading=reading,PSD='O4_H1_L1_MEASURED',
                        N=50,network_ringdown_SNR=snr,injected_a=injected,start_tM=start_tm,start_s=start,
                        remnant_mass_fixed=mass,remnant_spin_fixed=spin,
                        dimensionless_extra_damping=x.tolist(),input_scale=float(scale),
                        lnB_point_mean=float(logB.mean()),lnB_point_sd=float(logB.std(ddof=1)),
                        lnB_point_05_50_95=np.quantile(logB,[.05,.5,.95]).tolist(),lnB_draws=logB.tolist(),
                        amplitude_prior='Independent Normal(0, (1e-20 strain)^2) for each real quadrature in each detector; proper analytic integral',
                        all_QNMs='Exact qnm grid for both 220 and 440, including non-modular readings')
                    if unresolved:
                        if np.max(abs(logB))>1e-9:raise ValueError('Sub-resolution dephasing changed likelihood')
                        row.update(status='UNIDENTIFIABLE_AT_NUMERICAL_AND_OBSERVATIONAL_PRECISION',
                                   bias_a=None,coverage90=None,profile_intervals=None)
                    else:
                        fits=profile_intervals(agrid,profile)
                        clean_fit=profile_intervals(agrid,sum(clean_profiles))[0]
                        estimates=np.array([f['MLE'] for f in fits])
                        coverage=np.mean([f['CI90'][0]<=injected<=f['CI90'][1] for f in fits])
                        bias=abs(float(np.median(estimates))-injected)
                        boundaries=sum(f['boundary'] for f in fits)
                        row.update(status='PASS_BIAS_AND_COVERAGE' if bias<=.2 and .8<=coverage<=.97 and boundaries==0 else 'INCONCLUSIVE_SYSTEMATICS',
                            bias_a=bias,coverage90=float(coverage),boundary_count=boundaries,
                            median_a=float(np.median(estimates)),profile_intervals=fits,
                            noiseless_MLE=clean_fit['MLE'],noiseless_bias=abs(clean_fit['MLE']-injected))
                    results.append(row)
        print(json.dumps(dict(family=family['family'],start_tM=start_tm,completed_cells=len(results))),flush=True)
    atomic_json(ROOT/'C5_EMPIRICAL_IMR_STARTS.json',dict(status='TWO_FAMILY_FIVE_STARTS_OFFSOURCE_RECOVERY_MEASURED',
        on_source_strain_read=False,results=results,N_per_cell=50,noise_indices=selected.tolist(),
        noise_policy='Same 50 held-out intervals across hypotheses and SNRs as paired controls, never counted as independent repetitions across cells',
        relative_bias_threshold=.2,coverage_acceptance=[.8,.97],
        amplitude_model_scope='Fundamental 220+440 with independent detector quadratures; true remnant fixed. Optimistic conditional model, not full IMR or coherent-sky inference.',
        injection_scope='Conditional ensemble deformation of isolated 22 and 44 IMR harmonics, including their overtones; other harmonics unchanged. Aligned-spin representative system.',
        profile_scope='Signed a allowed only for diagnostic MLE/coverage while all modal damping rates remain positive; negative a is not a physical GKSL model',
        limitations=['Additional PSD recoloring still required','No marginalization of remnant mass/spin here','No event-window samples read'],
        hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ('tgl_ringdown_prediction.py','tgl_ringdown_likelihood.py','empirical_imr_recovery.py','C5_EMPIRICAL_NOISE.json','C5_IMR_CONTROLS.json','QNM_GRID.json')}))

if __name__=='__main__':main()
