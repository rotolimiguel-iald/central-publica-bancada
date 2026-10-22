"""Full-wave controls of continuous strengths at difficult actual source draws."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
from datetime import datetime, timezone
import json
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
import real_fourier_phase as real
import real_continuous_phase_source as cp
from phase_marginal_real_source import phase_marginal_loglikes

FOLDER=se.ROOT/'continuous_real_phase_validation'


def main():
    pm.check()
    state=se.load_state()
    phenom=se.ROOT/'phase_ringdown_real_continuation/IMRPhenomXPHM_seed130892_N16384'
    seob=se.ROOT/'phase_native_seob/SEOBNRv4HM_seed130901_N2048'
    rate=json.loads((seob/'AUDIT_RATE.json').read_bytes())
    selected=max(rate['diagnostic_points'],key=lambda row:row['pooled_weight'])['index']
    jobs=[('IMRPhenomXPHM',phenom,15627),('SEOBNRv4HM',seob,selected)]
    strengths=np.array([-2.,0.,.37,1.,4.])
    names=['validate_real_continuous_api.py','real_continuous_phase_source.py','REAL_CONTINUOUS_API_PROVENANCE.json',
        'real_fourier_phase.py','phase_marginal_real_source.py','continuous_phase_source.py','coherent_imr_model.py',
        'real_phase_adapter_validation_corrected/RESULT.json']
    names += [str((folder/'PROPOSALS.npz').relative_to(se.ROOT)) for family,folder,index in jobs]
    FOLDER.mkdir(exist_ok=False)
    registration=dict(status='REGISTERED_REAL_CONTINUOUS_PHASE_VALIDATION',date_utc=datetime.now(timezone.utc).isoformat(),
        selected_points=[dict(family=f,index=i,folder=str(p.relative_to(se.ROOT))) for f,p,i in jobs],
        strengths=strengths.tolist(),reading='R-B',sample_rate=8192,
        relative_wave_limit=1e-6,logL_limit=.001,phase_quadrature_limit=1e-5,
        continuous_strength_prior_selected=False,negative_strength_scope='Numerical calibration extension, not physical GKLS',
        scientific_acceptance=False,hashes={n:se.sha(se.ROOT/n) for n in names})
    se.write(FOLDER/'REGISTRATION.json',registration)
    rows=[]
    for family,folder,index in jobs:
        with np.load(folder/'PROPOSALS.npz') as archive:
            u=archive['unit_cube'][index]
        x=pm.six_to_physical(u)
        raw=cp.raw_phase_samples(family,x,state['times'])
        full=[]
        for psd in ('O4','O5'):
            bank=cp.make_bank(raw,'R-B',strengths,state[psd+'_white'])
            controls=[]
            for phase in (.173,.619,1.413):
                y=x.copy();y[5]=phase
                for k,a in enumerate(strengths):
                    original,_=se.model.network_basis(family,y,state['times'],'R-B',float(a),state[psd+'_white'])
                    interp=real.evaluate_bank(bank,[phase],k)[0]
                    relative=float(np.linalg.norm(original-interp)/np.linalg.norm(original))
                    _,exact=se.linear_statistics(original,state[psd+'_targets'],3.)
                    error=float(np.max(np.abs(exact-real.bank_loglikes(bank,[phase],state[psd+'_targets'],k))))
                    if relative>1e-6 or error>.001:
                        raise ValueError(f'Continuous control failed:{family},{index},{phase},{a},{relative},{error}')
                    controls.append(dict(phase=phase,strength=float(a),relative_error=relative,logL_error=error))
            integrals,quadrature=cp.marginal_loglikes(bank,state[psd+'_targets'])
            full.append(integrals-state[psd+'_centers'][None,:])
            se.save_arrays(FOLDER/f'{family}_{psd}.npz',strengths=strengths,components=full[-1])
            rows.append(dict(family=family,index=index,psd=psd,controls=controls,quadrature=quadrature))
            print(json.dumps(dict(family=family,psd=psd,controls=len(controls))),flush=True)
        full=np.concatenate(full,axis=1)
        # Binary endpoints must agree with the source-integral reader.
        paired,paired_controls=phase_marginal_loglikes(family,u,state)
        got=full[[1,3]].ravel()
        error=float(np.max(np.abs(got-paired)))
        if error>2e-5:
            raise ValueError('Continuous integration changed binary endpoints')
        se.write(FOLDER/f'{family}_endpoints.json',dict(index=index,max_logL_error=error,controls=paired_controls))
    controls=[c for row in rows for c in row['controls']]
    output=dict(status='PASS_REAL_CONTINUOUS_PHASE_API',rows=rows,
        direct_full_wave_controls=len(controls),max_relative_wave_error=max(c['relative_error'] for c in controls),
        max_direct_logL_error=max(c['logL_error'] for c in controls),
        scientific_acceptance=False,continuous_source_integration_completed=False,coverage_completed=False,
        no_new_prior=True,registration_sha256=se.sha(FOLDER/'REGISTRATION.json'),
        arrays_sha256={p.name:se.sha(p) for p in FOLDER.glob('*.npz')})
    se.write(FOLDER/'RESULT.json',output)
    print(json.dumps({k:v for k,v in output.items() if k not in ('rows','arrays_sha256')}),flush=True)


if __name__=='__main__':
    main()
