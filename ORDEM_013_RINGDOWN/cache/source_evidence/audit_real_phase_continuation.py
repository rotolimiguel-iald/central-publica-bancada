"""Audit resumed complete draws without inventing lost old control metadata."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
import argparse
import fcntl
import json
import multiprocessing as mp
import numpy as np
import source_evidence as se
from audit_phase_source import load_run, direct_statistics
from continue_real_phase_source import FOLDER, STAGE, check
from phase_marginal_real_source import phase_marginal_loglikes


def evaluate(item):
    index, u, original, active = item
    value, controls = phase_marginal_loglikes(se._FAMILY, u, se._STATE, sample_rate=16384)
    change = value-original
    return dict(index=int(index), components_above_one_percent=int(active.sum()),
        max_active_logL_change=float(np.max(np.abs(change[active]))),
        max_all_logL_change=float(np.max(np.abs(change))), controls=controls)


def run(args):
    reg = check()
    result, u, logq, inside, values, stats = load_run(FOLDER)
    if result['transport_registration_sha256'] != se.sha(STAGE/'REGISTRATION.json'):
        raise ValueError('Continuation registration mismatch')
    for name, expected in result['control_sidecar_hashes'].items():
        if se.sha(FOLDER/name) != expected:
            raise ValueError('Changed continuation control checkpoint')
    independent, weights = direct_statistics(values, logq)
    errors = {k:float(np.max(np.abs(stats[k]-v))) for k,v in independent.items()}
    if max(errors.values()) > 1e-9:
        raise ValueError('Independent arithmetic differs')
    controls = result['integration_controls']
    if len(controls)+reg['original_preserved_evaluations'] != int(inside.sum()):
        raise ValueError('Unaccounted control-metadata coverage')
    selected = np.unique(np.argmax(weights, axis=0))
    out = dict(status='PASS_CONTINUATION_ARITHMETIC_NOT_PRECISION', scientific_acceptance=False,
        draws=len(u), inside=int(inside.sum()), outside=int((~inside).sum()), independent_arithmetic_errors=errors,
        ESS_quantiles=np.quantile(stats['ESS'], [0,.1,.5,.9,1]).tolist(),
        max_weight_quantiles=np.quantile(stats['max_weight'], [0,.1,.5,.9,1]).tolist(),
        lnB_MC_sd_quantiles=np.quantile(stats['lnB_MC_sd'], [0,.1,.5,.9,1]).tolist(),
        passed_precision=result['draws_passing_precision'],
        control_metadata_coverage=result['control_metadata_coverage'],
        available_controls_only={key:max(c[key] for c in controls) for key in
            ('max_logL_interpolation_error','max_relative_waveform_interpolation_error','max_phase_quadrature_error','largest_phase_grid')},
        unique_dominant_samples=selected.tolist(),
        hashes={'RESULT.json':se.sha(FOLDER/'RESULT.json'), 'source':se.sha(se.ROOT/'audit_real_phase_continuation.py')})
    if not (FOLDER/'ARITHMETIC_AUDIT.json').exists():
        se.write(FOLDER/'ARITHMETIC_AUDIT.json', out)
    else:
        if json.loads((FOLDER/'ARITHMETIC_AUDIT.json').read_bytes()) != out:
            raise ValueError('Existing arithmetic audit differs')
    print(json.dumps({k:v for k,v in out.items() if k not in ('hashes','unique_dominant_samples')}), flush=True)
    if not args.rate:
        return
    folder = FOLDER/'real_rate_control'
    folder.mkdir(exist_ok=True)
    registration = dict(status='REGISTERED_DOMINANT_POINT_RATE_CHECK', source_rate=8192, comparison_rate=16384,
        selected_indices=selected.tolist(), active_weight_threshold=.01, logL_limit=.1,
        scope='All component-dominant points; not a global posterior error bound',
        original_waveform_generator=True, interpolation='Validated real Nyquist convention at both rates',
        result_sha256=se.sha(FOLDER/'RESULT.json'), script_sha256=se.sha(se.ROOT/'audit_real_phase_continuation.py'),
        adapter_sha256=se.sha(se.ROOT/'phase_marginal_real_source.py'), real_fourier_sha256=se.sha(se.ROOT/'real_fourier_phase.py'))
    if (folder/'REGISTRATION.json').exists():
        if json.loads((folder/'REGISTRATION.json').read_bytes()) != registration:
            raise ValueError('Rate registration changed')
    else:
        se.write(folder/'REGISTRATION.json', registration)
    rows = []
    pending = []
    for index in selected:
        path = folder/f'point_{index}.json'
        if path.exists():
            row = json.loads(path.read_bytes())
            if row['index'] != int(index):
                raise ValueError('Rate checkpoint index differs')
            rows.append(row)
        else:
            pending.append((int(index),u[index],values[index],weights[index]>.01))
    with mp.get_context('fork').Pool(args.processes, initializer=se.initialize, initargs=(result['family'],)) as pool:
        for row in pool.imap_unordered(evaluate, pending, chunksize=1):
            se.write(folder/f"point_{row['index']}.json", row)
            rows.append(row)
            print(json.dumps(dict(rate_done=len(rows), total=len(selected))), flush=True)
    maximum = max(r['max_active_logL_change'] for r in rows)
    output = dict(status='PASS_DOMINANT_RATE_CONTROL' if maximum <= .1 else 'DOMINANT_RATE_CONTROL_FAILED',
        max_active_logL_change=maximum, numerical_scope=registration['scope'], scientific_acceptance=False,
        rows=sorted(rows,key=lambda r:r['index']), registration_sha256=se.sha(folder/'REGISTRATION.json'),
        point_hashes={p.name:se.sha(p) for p in folder.glob('point_*.json')})
    se.write(folder/'RESULT.json', output)
    print(json.dumps({k:v for k,v in output.items() if k not in ('rows','point_hashes')}), flush=True)
    if maximum > .1:
        raise ValueError('Rate control exceeded the registered likelihood tolerance')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--rate', action='store_true')
    parser.add_argument('--processes', type=int, default=2); args = parser.parse_args()
    with open(STAGE/'AUDIT.lock', 'a+b') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        run(args)
