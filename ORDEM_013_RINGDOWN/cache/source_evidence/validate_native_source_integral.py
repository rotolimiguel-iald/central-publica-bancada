"""Compare the accelerated integral against frozen full-wave phase quadrature."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
from datetime import datetime,timezone
import json
import multiprocessing as mp
import time
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
from native_seob_source_likelihood import phase_marginal_loglikes

FOLDER=se.ROOT/'native_source_integral_validation'


def evaluate(job):
    source,rate=job
    u=np.array([(source['mass']-50)/60,(source['q']-1)/2,(source['s1']+.4)/.8,
                (source['s2']+.4)/.8,(np.cos(source['inclination'])+.95)/1.9,.5])
    start=time.monotonic()
    exact,ec=pm.phase_marginal_loglikes('SEOBNRv4HM',u,se._STATE,rate)
    original_seconds=time.monotonic()-start; start=time.monotonic()
    got,gc=phase_marginal_loglikes('SEOBNRv4HM',u,se._STATE,rate)
    error=float(np.max(np.abs(exact-got)))
    row=dict(source=source['name'],rate=rate,unit_coordinates=u.tolist(),count=len(got),
        max_logL_integral_error=error,original_seconds=original_seconds,
        native_seconds=time.monotonic()-start,original_controls=ec,native_controls=gc,
        passes=bool(error<=.001))
    se.save_arrays(FOLDER/f"{source['name']}_{rate}.npz",original=exact,native=got)
    se.write(FOLDER/f"{source['name']}_{rate}.json",row)
    return row


def main():
    pm.check(); FOLDER.mkdir(exist_ok=False)
    names=['validate_native_source_integral.py','native_seob_source_likelihood.py',
           'native_seob_phase_source.py','direct_seob_modes.py','stable_peak_phase_source.py',
           'phase_marginal_source.py','phase_runs/REGISTRATION.json','native_seob_phase_validation/RESULT.json']
    se.write(FOLDER/'REGISTRATION.json',dict(status='REGISTERED_NATIVE_SOURCE_INTEGRAL_EQUIVALENCE',
        date_utc=datetime.now(timezone.utc).isoformat(),family='SEOBNRv4HM',sources=['reference','source_90'],
        rates=[8192,16384],max_logL_integral_error=.001,
        scope='Four source/rate points, each with all2400 components; only numerical equivalence, not evidence convergence',
        hashes={n:se.sha(se.ROOT/n) for n in names}))
    jobs=[(s,r) for s in se.SOURCES if s['name'] in ('reference','source_90') for r in (8192,16384)]
    rows=[]
    with mp.get_context('fork').Pool(2,initializer=se.initialize,initargs=('SEOBNRv4HM',)) as pool:
        for row in pool.imap_unordered(evaluate,jobs):
            rows.append(row); print(json.dumps(row),flush=True)
    output=dict(status='PASS_NATIVE_SOURCE_INTEGRAL' if all(r['passes'] for r in rows) else 'FAIL_NATIVE_SOURCE_INTEGRAL',
        rows=rows,max_logL_integral_error=max(r['max_logL_integral_error'] for r in rows),
        scientific_acceptance=False,registration_sha256=se.sha(FOLDER/'REGISTRATION.json'))
    se.write(FOLDER/'RESULT.json',output)
    print(json.dumps({k:v for k,v in output.items() if k!='rows'}),flush=True)


if __name__=='__main__': main()
