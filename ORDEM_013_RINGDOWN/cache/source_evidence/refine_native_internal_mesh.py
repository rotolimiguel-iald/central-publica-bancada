"""Refine the actual SEOB internal mesh, not only its output sampling.

Selected-source numerical control. Injections stay frozen at8192Hz; rescaling
them to high SNR does not validate their own accuracy. No source evidence here.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
from datetime import datetime,timezone
import json
import time
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
import peak_phase_coordinates as pc
import stable_peak_phase_source as api
import stable_peak_imr_model as stable
import native_seob_phase_source as native
from diagnose_generator_alignment import targets_for_source

FOLDER=se.ROOT/'native_internal_mesh_refinement'
RATES=(131072,262144,524288)


def main():
    pm.check()
    validation=json.loads((se.ROOT/'native_seob_phase_validation/RESULT.json').read_bytes())
    if validation['status']!='PASS_NATIVE_SEOB_PHASE_ADAPTER':
        raise ValueError('Native phase adapter validation failed')
    reg0=json.loads((se.ROOT/'native_seob_phase_validation/REGISTRATION.json').read_bytes())
    for n,h in reg0['hashes'].items():
        if se.sha(se.ROOT/n)!=h:
            raise ValueError('Validated adapter custody changed: '+n)
    FOLDER.mkdir(exist_ok=False)
    paths=['refine_native_internal_mesh.py','native_seob_phase_source.py','direct_seob_modes.py',
           'stable_peak_phase_source.py','stable_peak_imr_model.py','native_seob_phase_validation/RESULT.json',
           'LAL_INTERNAL_MESH_AUDIT.json','INJECTIONS.npz','generator_alignment_diagnostic/SEOBNRv4HM_131072.npz']
    se.write(FOLDER/'REGISTRATION.json',dict(status='REGISTERED_ACTUAL_INTERNAL_MESH_REFINEMENT',
        date_utc=datetime.now(timezone.utc).isoformat(),source='source_90',rates=list(RATES),snrs=[40,200,600],
        reading='R-B',strengths=[0.,1.],heldout_phase=.619,heldout_strengths=[.37,1.],
        criteria=dict(max_adapter_relative_error=1e-6,max_adapter_logL_error=.001,max_phase_integral_rate_change=.1),
        scope='Selected source only; actual internal step measured from LAL dynamics. Frozen8192Hz injections are not validated for highSNR by this comparison.',
        physical_prior_changed=False,C6_changed=False,scientific_acceptance=False,
        hashes={n:se.sha(se.ROOT/n) for n in paths}))
    state=se.load_state(); source=next(s for s in se.SOURCES if s['name']=='source_90')
    x=se.source_vector(source); targets=targets_for_source(state,source['name'])
    rates=[]; arrays={}; basis_by_rate={}
    for rate in RATES:
        started=time.monotonic()
        raw=native.raw_phase_samples('SEOBNRv4HM',x,state['times'],sample_rate=rate)
        se.save_arrays(FOLDER/f'raw_{rate}.npz',samples=raw['samples'],times=raw['times'])
        repeated_error=None
        if rate==RATES[0]:
            with np.load(se.ROOT/'generator_alignment_diagnostic/SEOBNRv4HM_131072.npz') as f:
                original=f['common_phase_zero_peak_raw']
                repeated_error=float(np.linalg.norm(raw['samples']-original)/np.linalg.norm(original))
        checks=[]; quadratures=[]
        for psd in ('O4','O5'):
            white=state[psd+'_white']
            bank=api.make_bank(raw,'R-B',[0.,1.],white)
            integrals,control=api.marginal_loglikes(bank,targets[psd])
            arrays[(rate,psd)]=integrals
            se.save_arrays(FOLDER/f'integrals_{rate}_{psd}.npz',values=integrals)
            quadratures.append(dict(psd=psd,controls=control))
            basis_by_rate[(rate,psd)]=[pc.evaluate_bank(bank,[source['phase']],i)[0] for i in range(2)]
            more=api.make_bank(raw,'R-B',[.37,1.],white)
            for i,a in enumerate((.37,1.)):
                y=x.copy(); y[5]=.619
                direct,_=stable.network_basis('SEOBNRv4HM',y,state['times'],'R-B',a,white,rate)
                b=pc.evaluate_bank(more,[.619],i)[0]
                relative=float(np.linalg.norm(b-direct)/np.linalg.norm(direct))
                _,ll=se.linear_statistics(direct,targets[psd],3.)
                errors=np.abs(ll-pc.bank_loglikes(more,[.619],targets[psd],i)).reshape(3,200).max(axis=1)
                checks.append(dict(psd=psd,strength=a,phase=.619,relative_error=relative,
                    max_logL_errors_SNR40_200_600=errors.tolist(),passes=bool(relative<=1e-6 and errors.max()<=.001)))
        stable.source_curves.cache_clear()
        row=dict(rate=rate,dynamics=raw['native_dynamics'],peak_generator_s=raw['peak_generator_s'],
                 checks=checks,quadratures=quadratures,original_bank_relative_error=repeated_error,
                 seconds=time.monotonic()-started)
        rates.append(row); se.write(FOLDER/f'rate_{rate}.json',row)
        print(json.dumps(dict(rate=rate,internal_step_M=raw['native_dynamics']['high_time_step_M'],
             max_adapter_logL_error=max(max(c['max_logL_errors_SNR40_200_600']) for c in checks),seconds=row['seconds'])),flush=True)
    comparison=[]
    for low,high in zip(RATES[:-1],RATES[1:]):
        for psd in ('O4','O5'):
            difference=arrays[(high,psd)]-arrays[(low,psd)]
            errors=np.abs(difference).reshape(2,3,200).max(axis=(0,2))
            noiseless=[]
            for i in range(2):
                bl,bh=basis_by_rate[(low,psd)][i],basis_by_rate[(high,psd)][i]
                orientation=np.array([np.cos(2*source['psi']),np.sin(2*source['psi'])])
                target=bh@orientation; target*=600./np.linalg.norm(target)
                coefficients=np.linalg.lstsq(bl,target,rcond=None)[0]
                noiseless.append(float(np.linalg.norm(target-bl@coefficients)))
            comparison.append(dict(low=low,high=high,psd=psd,max_logL_integral_change_SNR40_200_600=errors.tolist(),
                passes_by_SNR=(errors<=.1).tolist(),noiseless_common_amplitude_residual_norm_SNR600=noiseless,
                caveat='Residual norms are waveform distances, not detection sigma. No full-source marginalization.'))
    rows=[c for r in rates for c in r['checks']]
    steps=[r['dynamics']['high_time_step_M'] for r in rates]
    ratios=(np.array(steps[:-1])/np.array(steps[1:])).tolist()
    if np.max(np.abs(np.array(ratios)-2.))>1e-8:
        raise ValueError('Requested output rates did not halve actual internal steps')
    result=dict(status='ACTUAL_INTERNAL_MESH_MEASURED_NOT_SCIENTIFIC_ACCEPTANCE',rates=rates,comparisons=comparison,
        internal_step_ratios=ratios,adapter_pass=all(c['passes'] for c in rows),adapter_check_count=len(rows),
        all_rate_pass=all(all(r['passes_by_SNR']) for r in comparison),scientific_acceptance=False,
        registration_sha256=se.sha(FOLDER/'REGISTRATION.json'))
    se.write(FOLDER/'RESULT.json',result)
    print(json.dumps({k:result[k] for k in ('status','internal_step_ratios','adapter_pass','all_rate_pass','comparisons')}),flush=True)


if __name__=='__main__':
    main()
