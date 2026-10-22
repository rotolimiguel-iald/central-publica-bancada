"""SVD likelihood oracle, profile refinement, and prior-volume diagnostics.

Independent SVD singular values integrate the physical Gaussian amplitude
prior; no inverse normal-equation matrix is reused from the tested function.
Only task-local injection/noise caches are read. No target strain access.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.optimize import minimize_scalar
from diagnose_overtones import GROUPS,control_modes,mode_basis
from tgl_ringdown_prediction import prediction,scales
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def spectral_statistics(basis,targets,sd=10.):
    u,s,_=np.linalg.svd(basis,full_matrices=False)
    if s[-1]<1e-12*s[0]:raise ValueError('Unresolved column rank')
    projection=np.atleast_2d(targets)@u
    profile=.5*np.sum(projection**2,axis=1)
    marginal=.5*np.sum(projection**2*(s*s/(s*s+1/sd**2)),axis=1)-.5*np.sum(np.log1p((sd*s)**2))
    return profile,marginal,float(s[0]/s[-1])

def main():
    report=json.loads((ROOT/'C5_RECOLORED_FORECAST.json').read_bytes())
    families=json.loads((ROOT/'C5_IMR_CONTROLS.json').read_bytes())['families']
    checks=[];prior=[];refinements=[]
    responses={'H1':(.7,.2),'L1':(-.3,.8)}
    for family in families:
        exact=control_modes(family);mass=family['remnant_mass_detector_solar'];spin=family['remnant_spin']
        waveform=np.load(ROOT/f"cache/imr_controls/{family['family']}.npz")
        predictions={ell:prediction(mass,spin,'R-B',mode=(ell,ell,0),qnm_dimensionless=exact[(ell,ell,0)]) for ell in (2,4)}
        grid_step=2.8/1200/max(p['x'] for p in predictions.values())
        for psd in ('O4','O5','ET','CE'):
            cache=np.load(ROOT/f'cache/recolored_noise/{psd}_noise.npz');w=cache['whitener_scaled']
            t=np.arange(w.shape[1])/2048.;tp=t+10*scales(mass,'CODATA2018_IAU2015')[0]
            components={k:np.interp(tp,waveform['time_from_peak_s'],waveform[k])*1e21 for k in ('22_plus','22_cross','44_plus','44_cross','other_plus','other_cross')}
            xi={d:cache[d+'_strain_scaled'][:50]@w.T for d in responses}
            for label in ('220_440','220_221_222_440','eight_modes'):
                modes=GROUPS[label]
                raw=mode_basis(t,family,'R-B',modes,[0.,1.],exact)
                bases=np.einsum('kt,gti->gki',w,raw,optimize=True)
                noise_z=sum(np.array([spectral_statistics(b,xi[d])[1] for b in bases]) for d in responses)
                prior.append(dict(family=family['family'],psd=psd,recovery=label,
                    noise_only_lnB_mean=float(np.mean(noise_z[1]-noise_z[0])),
                    noise_only_lnB_sd=float(np.std(noise_z[1]-noise_z[0],ddof=1))))
                for injected in (0.,1.):
                    signals={}
                    for d,(fp,fc) in responses.items():
                        y=fp*components['other_plus']+fc*components['other_cross']
                        for ell in (2,4):
                            name=str(ell)*2;y=y+(fp*components[name+'_plus']+fc*components[name+'_cross'])*np.exp(-injected*predictions[ell]['gamma_per_s']*tp)
                        signals[d]=w@y
                    norm=np.sqrt(sum(s@s for s in signals.values()))
                    for snr in (40.,600.):
                        row=next(r for r in report['results'] if r['family']==family['family'] and r['psd']==psd and r['reading']=='R-B' and r['recovery']==label and r['content']=='FULL_IMR' and r['injected_a']==injected and r['SNR']==snr)
                        draws=np.load(ROOT/row['draws_cache'])['draws'][row['draws_index']]
                        marginal=[];conditions=[]
                        for b in bases:
                            mz=[]
                            for d in responses:
                                _,m,condition=spectral_statistics(b,xi[d]+signals[d][None,:]*snr/norm)
                                mz.append(m);conditions.append(condition)
                            marginal.append(sum(mz))
                        error=float(np.max(abs(marginal[1]-marginal[0]-draws[:,0])))
                        if error>1e-5:raise ValueError(f'Independent SVD likelihood failed: {error}')
                        checks.append(dict(family=family['family'],psd=psd,recovery=label,injected_a=injected,SNR=snr,independent_lnB_max_error=error,basis_condition=max(conditions)))
                    # Noiseless MLE at SNR40: continuous SVD objective around grid peak.
                    row=next(r for r in report['results'] if r['family']==family['family'] and r['psd']==psd and r['reading']=='R-B' and r['recovery']==label and r['content']=='FULL_IMR' and r['injected_a']==injected and r['SNR']==40.)
                    center=row['noiseless_a_hat']
                    def objective(a):
                        b=w@mode_basis(t,family,'R-B',modes,[a],exact)[0]
                        return -sum(spectral_statistics(b,signals[d]*40/norm)[0][0] for d in responses)
                    result=minimize_scalar(objective,bounds=(center-2*grid_step,center+2*grid_step),method='bounded',options={'xatol':1e-7})
                    if not result.success:raise ValueError('Continuous refinement failed')
                    shift=abs(float(result.x)-center)
                    if shift>grid_step:raise ValueError('Profile peak changes by more than one grid step')
                    refinements.append(dict(family=family['family'],psd=psd,recovery=label,injected_a=injected,grid_MLE=center,continuous_MLE=float(result.x),shift=shift,grid_step=grid_step))
    atomic_json(ROOT/'C5_RECOLORED_VALIDATION.json',dict(status='PASS',
        independent_SVD_controls=checks,continuous_profile_refinement=refinements,
        noise_only_prior_volume=prior,
        caution='A positive mean lnB under a fixed injected GR waveform can reflect proper amplitude-prior volume and model discrepancy. It is not a calibrated detection or an automatically valid conversion to sigma.',
        no_target_strain_access=True,
        forecast_sha256=hashlib.sha256((ROOT/'C5_RECOLORED_FORECAST.json').read_bytes()).hexdigest(),
        verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
    print(json.dumps(dict(status='PASS',cells=len(checks),max_lnB_error=max(r['independent_lnB_max_error'] for r in checks),max_MLE_shift=max(r['shift'] for r in refinements))))

if __name__=='__main__':main()
