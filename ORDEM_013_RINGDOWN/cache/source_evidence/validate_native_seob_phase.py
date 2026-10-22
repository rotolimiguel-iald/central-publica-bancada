"""Validate the native modes adapter before any statistical production use."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
from datetime import datetime, timezone
import argparse
import json
import multiprocessing as mp
import time
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
import peak_phase_coordinates as pc
import stable_peak_imr_model as stable
import stable_peak_phase_source as api
import native_seob_phase_source as native
from validate_stable_phase_prior import initialize
import validate_stable_phase_prior as controls

FOLDER=se.ROOT/'native_seob_phase_validation'


def evaluate(job):
    name,x,rate=job; x=np.array(x); started=time.monotonic()
    state,targets=controls._STATE,controls._TARGETS
    raw=native.raw_phase_samples('SEOBNRv4HM',x,state['times'],sample_rate=rate)
    generation_seconds=time.monotonic()-started
    rows=[]
    for psd in ('O4','O5'):
        white=state[psd+'_white']
        bank=api.make_bank(raw,'R-B',[0.,.37,1.],white)
        for phase in (.173,.619,1.413):
            y=x.copy(); y[5]=phase
            for i,a in enumerate((0.,.37,1.)):
                direct,meta=stable.network_basis('SEOBNRv4HM',y,state['times'],'R-B',a,white,rate)
                reconstructed=pc.evaluate_bank(bank,[phase],i)[0]
                relative=float(np.linalg.norm(reconstructed-direct)/np.linalg.norm(direct))
                _,logl=se.linear_statistics(direct,targets[psd],3.)
                errors=np.abs(logl-pc.bank_loglikes(bank,[phase],targets[psd],i)).reshape(2,600).max(axis=1)
                rows.append(dict(psd=psd,phase=phase,strength=a,relative_error=relative,
                                 logL_errors_SNR40_600=errors.tolist(),peak_difference_s=meta['peak_generator_s']-raw['peak_generator_s'],
                                 passes=bool(relative<=1e-6 and errors.max()<=.001)))
    result=dict(source=name,coordinates=x.tolist(),rate=rate,native_generation_seconds=generation_seconds,
                elapsed_seconds=time.monotonic()-started,controls=rows,dynamics=raw['native_dynamics'],
                max_relative_error=max(r['relative_error'] for r in rows),
                max_logL_error=max(max(r['logL_errors_SNR40_600']) for r in rows),
                passes=all(r['passes'] for r in rows))
    se.write(FOLDER/f'{name}_{rate}.json',result)
    return result


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--processes',type=int,default=2)
    args=parser.parse_args(); pm.check(); FOLDER.mkdir(exist_ok=False)
    prior=json.loads((se.ROOT/'stable_phase_prior_controls/REGISTRATION.json').read_bytes())
    points=prior['all_points'][:5]
    for i,(name,x) in enumerate(points):
        x=list(x); x[6]=(-.6 if i%2 else .6)
        points[i]=[name,x]
    jobs=[(name,x,rate) for name,x in points for rate in (8192,16384)]
    names=['validate_native_seob_phase.py','native_seob_phase_source.py','direct_seob_modes.py',
           'stable_peak_imr_model.py','stable_peak_phase_source.py','INJECTIONS.npz',
           'stable_phase_prior_controls/REGISTRATION.json','DIRECT_SEOB_MODES_CORRECTED_VALIDATION.json']
    se.write(FOLDER/'REGISTRATION.json',dict(status='REGISTERED_NATIVE_SEOB_PHASE_ADAPTER',
        date_utc=datetime.now(timezone.utc).isoformat(),points=points,rates=[8192,16384],
        scope='Three reference sources and two prior points, both time-shift signs, three held-out phases and strengths; not uniform source-prior calibration',
        physical_prior_changed=False,C6_changed=False,hashes={n:se.sha(se.ROOT/n) for n in names}))
    results=[]
    with mp.get_context('fork').Pool(args.processes,initializer=initialize) as pool:
        for result in pool.imap_unordered(evaluate,jobs,chunksize=1):
            results.append(result)
            print(json.dumps({k:result[k] for k in ('source','rate','max_relative_error','max_logL_error','passes','native_generation_seconds')}),flush=True)
    rows=[r for item in results for r in item['controls']]
    summary=dict(status='PASS_NATIVE_SEOB_PHASE_ADAPTER' if all(r['passes'] for r in rows) else 'FAIL_NATIVE_SEOB_PHASE_ADAPTER',
        count=len(rows),failures=sum(not r['passes'] for r in rows),
        max_relative_error=max(r['relative_error'] for r in rows),
        max_logL_errors_SNR40_600=np.max([r['logL_errors_SNR40_600'] for r in rows],axis=0).tolist(),
        max_peak_difference_s=max(abs(r['peak_difference_s']) for r in rows),results=results,
        scientific_acceptance=False,registration_sha256=se.sha(FOLDER/'REGISTRATION.json'))
    se.write(FOLDER/'RESULT.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k!='results'}),flush=True)


if __name__=='__main__':
    main()
