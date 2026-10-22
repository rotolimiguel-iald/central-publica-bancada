"""Reproduce the terminal Phenom failure using preserved, exact source draws."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
from datetime import datetime, timezone
import json
import multiprocessing as mp
import traceback
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
import peak_phase_coordinates as pc

PILOT = se.ROOT/'phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384'
FOLDER = se.ROOT/'failed_phenom_phase_diagnostic'


def evaluate(job):
    index, u = job
    try:
        value, controls = pm.phase_marginal_loglikes('IMRPhenomXPHM', u, se._STATE)
        se.save_arrays(FOLDER/f'point_{index}_passing.npz', components=value)
        row = dict(index=index, status='ORIGINAL_PASSED_ON_REPLAY', controls=controls, coordinates=u.tolist())
    except Exception as exc:
        row = dict(index=index, status='ORIGINAL_FAILURE_REPRODUCED', error=repr(exc),
                   traceback=traceback.format_exc(), coordinates=u.tolist())
        x = pm.six_to_physical(u)
        tests = []
        for psd in ('O4', 'O5'):
            bank = pc.phase_bank('IMRPhenomXPHM', x, se._STATE['times'], se._STATE[psd+'_white'])
            phases = np.r_[.173, .619, 1.413, 2*np.pi*np.arange(512)/512]
            exponential = np.exp(1j*np.outer(phases, bank['orders']))
            for a in (0, 1):
                values = np.einsum('pk,ktj->ptj', exponential, bank['coefficients'][a], optimize=True)
                tests.append(dict(psd=psd, a=a,
                    max_imag=float(np.max(np.abs(values.imag))), max_real=float(np.max(np.abs(values.real))),
                    max_imag_over_scale=float(np.max(np.abs(values.imag))/max(1., np.max(np.abs(values.real)))),
                    nyquist_coefficient_norm=float(np.linalg.norm(bank['coefficients'][a, 8])),
                    total_coefficient_norm=float(np.linalg.norm(bank['coefficients'][a]))))
            se.save_arrays(FOLDER/f'point_{index}_{psd}_bank.npz', samples=bank['samples'],
                coefficients=bank['coefficients'], orders=bank['orders'], phases=phases)
        peaks = []
        for phase in 2*np.pi*np.arange(16)/16:
            y = x.copy(); y[5] = phase
            curves, mf, spin, peak = se.model.source_curves('IMRPhenomXPHM', tuple(y[:6]), 8192, True)
            peaks.append(float(peak))
        row.update(bank_diagnostics=tests, phase_peak_values=peaks, peak_span_s=max(peaks)-min(peaks))
    se.write(FOLDER/f'point_{index}.json', row)
    return row


def main():
    pm.check()
    if (PILOT/'RESULT.json').exists():
        raise ValueError('Expected preserved incomplete run')
    with np.load(PILOT/'PROPOSALS.npz') as f:
        u, inside = f['unit_cube'].copy(), f['inside'].copy()
    completed = np.concatenate([np.load(p)['indices'] for p in sorted(PILOT.glob('chunk_*.npz'))])
    if len(np.unique(completed)) != len(completed) or not np.all(inside[completed]):
        raise ValueError('Invalid preserved indices')
    missing = np.setdiff1d(np.flatnonzero(inside), completed)
    selected = missing[:32]
    FOLDER.mkdir(exist_ok=False)
    reg = dict(status='REGISTERED_REPLAY_OF_TERMINAL_PHASE_FAILURE',
        date_utc=datetime.now(timezone.utc).isoformat(), terminal_process=62818, exit_code_observed=1,
        saved_evaluations=len(completed), missing_evaluations=len(missing), selected_indices=selected.tolist(),
        scope='Reproduce failure only; not a restarted evidence run or accepted partial likelihood.',
        hashes={'diagnose_failed_phase_reconstruction.py': se.sha(se.ROOT/'diagnose_failed_phase_reconstruction.py'),
                'phase_marginal_source.py': se.sha(se.ROOT/'phase_marginal_source.py'),
                'peak_phase_coordinates.py': se.sha(se.ROOT/'peak_phase_coordinates.py'),
                'proposals': se.sha(PILOT/'PROPOSALS.npz')})
    se.write(FOLDER/'REGISTRATION.json', reg)
    rows = []
    with mp.get_context('fork').Pool(2, initializer=se.initialize, initargs=('IMRPhenomXPHM',)) as pool:
        for row in pool.imap_unordered(evaluate, [(int(i), u[i]) for i in selected]):
            rows.append(row)
            print(json.dumps(dict(done=len(rows), index=row['index'], status=row['status'])), flush=True)
    output = dict(status='PHASE_FAILURE_REPLAY_COMPLETE', rows=sorted(rows, key=lambda r: r['index']),
        failures=[r['index'] for r in rows if r['status']=='ORIGINAL_FAILURE_REPRODUCED'],
        scientific_acceptance=False, registration_sha256=se.sha(FOLDER/'REGISTRATION.json'))
    se.write(FOLDER/'RESULT.json', output)
    print(json.dumps({k: v for k, v in output.items() if k != 'rows'}), flush=True)


if __name__ == '__main__':
    main()
