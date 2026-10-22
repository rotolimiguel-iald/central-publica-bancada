"""Extend frozen source proposals to full diagnostic strength curves.

This is additional integration over the already registered source prior, not
new event data, a changed beta, or a prior over strength. Runs are independent
between waveform families but share their original binary source draws. A
separate independent-repeat and waveform-rate audit remains necessary.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
import argparse
from datetime import datetime, timezone
import fcntl
import json
import multiprocessing as mp
import shutil
import time
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
from controlled_continuous_source import evaluate
from continuous_source_calibration import curve_statistics, read_curves

STAGE = se.ROOT / 'continuous_source_curves'
SOURCES = {
    'IMRPhenomXPHM': 'phase_real_refined/IMRPhenomXPHM_seed130972_N32768',
    'SEOBNRv4HM': 'phase_native_repeat/SEOBNRv4HM_seed130942_N16384',
}
STRENGTHS = np.arange(-4., 4.25, .5)
_GRID = None


def folder_for(family):
    return STAGE / (se.ROOT / SOURCES[family]).name


def check(family):
    pm.check()
    folder = folder_for(family)
    reg = json.loads((folder/'REGISTRATION.json').read_bytes())
    if reg['family'] != family or reg['strengths'] != STRENGTHS.tolist():
        raise ValueError('Registered family or strength grid changed')
    for name, digest in reg['hashes'].items():
        if se.sha(se.ROOT/name) != digest:
            raise ValueError('Registered continuous input changed: ' + name)
    return folder, reg


def register(family):
    pm.check()
    validated = json.loads((se.ROOT/'controlled_continuous_validation/RESULT.json').read_bytes())
    arithmetic = json.loads((se.ROOT/'continuous_calibration_validation/RESULT.json').read_bytes())
    if (validated['status'] != 'PASS_CONTROLLED_CONTINUOUS_SOURCE_EVALUATOR' or
            arithmetic['status'] != 'PASS_CONTINUOUS_CALIBRATION_ARITHMETIC'):
        raise ValueError('Continuous evaluator/arithmetic not validated')
    for stage, report in [('controlled_continuous_validation', validated),
                          ('continuous_calibration_validation', arithmetic)]:
        regpath = se.ROOT/stage/'REGISTRATION.json'
        if report['registration_sha256'] != se.sha(regpath):
            raise ValueError('Validation receipt does not match its registration')
        for name, digest in json.loads(regpath.read_bytes())['hashes'].items():
            if se.sha(se.ROOT/name) != digest:
                raise ValueError('Validated input changed: ' + name)
    source = se.ROOT/SOURCES[family]
    source_reg = json.loads((source.parent/'REGISTRATION.json').read_bytes())
    for name, digest in source_reg['hashes'].items():
        if se.sha(se.ROOT/name) != digest:
            raise ValueError('Parent source registration changed: ' + name)
    start = json.loads((source/'START.json').read_bytes())
    if (start['transport_registration_sha256'] != se.sha(source.parent/'REGISTRATION.json') or
            start['proposal_sha256'] != se.sha(source.parent/'PROPOSAL.json')):
        raise ValueError('Frozen draws belong to a different proposal/registration')
    oracle = json.loads((source.parent/'PROPOSAL_ORACLE.json').read_bytes())
    if oracle['status'] != 'PASS_TRANSPORT_PROPOSAL_MOMENTS':
        raise ValueError('Source proposal normalization not validated')
    with np.load(source/'PROPOSALS.npz') as archive:
        total, valid = len(archive['inside']), int(archive['inside'].sum())
    if total != start['draws'] or family != start['family']:
        raise ValueError('Source draw count/family changed')
    state = se.load_state()
    if len(state['labels']) != 1200:
        raise ValueError('Registered target set changed')
    names = [str((source/p).relative_to(se.ROOT)) for p in ('PROPOSALS.npz', 'START.json')]
    names += [str((source.parent/p).relative_to(se.ROOT)) for p in ('REGISTRATION.json', 'PROPOSAL.json', 'PROPOSAL_ORACLE.json')]
    names += ['run_continuous_source_curves.py', 'controlled_continuous_source.py',
        'continuous_source_calibration.py', 'real_continuous_phase_source.py',
        'continuous_phase_source.py', 'real_fourier_phase.py', 'native_seob_phase_source.py',
        'direct_seob_modes.py', 'stable_peak_imr_model.py', 'phase_marginal_source.py',
        'importance_source_evidence.py', 'tgl_ringdown_likelihood.py', 'INJECTIONS.json',
        'INJECTIONS.npz', 'controlled_continuous_validation/RESULT.json',
        'controlled_continuous_validation/REGISTRATION.json',
        'continuous_calibration_validation/RESULT.json', 'continuous_calibration_validation/REGISTRATION.json']
    folder = folder_for(family)
    folder.mkdir(parents=True, exist_ok=False)
    reg = dict(status='REGISTERED_CONTINUOUS_SOURCE_CURVES', date_utc=datetime.now(timezone.utc).isoformat(),
        family=family, source_run=SOURCES[family], draws=total, inside_draws=valid,
        targets=1200, strengths=STRENGTHS.tolist(), reading='R-B', waveform_hz=8192,
        physical_prior_changed=False, likelihood_changed=False, strength_prior_selected=False,
        amplitude_prior_sd=3., all_source_parameters_integrated=True,
        interval='Existing LR interval geometry applied to nuisance-marginal logZ(a); requires empirical calibration',
        negative_strength='Diagnostic extension only, not physical GKLS',
        grid_control='Compare every other point; MLE and both endpoints must change by <=0.05. Boundary/islands/flatness are visible failures. Finer grid/domain may be necessary.',
        precision='Every strength ESS>=100,maxweight<=0.05,paired logZ(a)/Z(0) MCsd<=0.2; independent repeats/rate controls remain required',
        acceptance='Every mock retained, N>=50/cell; abs(median(ahat)-injected)<=0.2; empirical LR90 coverage in[0.80,0.97]. No result accepted when numerical controls fail.',
        other_readings_and_SNR='Remain required in full goal; this is the current R-B SNR40 registered matrix',
        binary_source_job_changed=False, C6_changed=False, scientific_acceptance=False,
        hashes={n:se.sha(se.ROOT/n) for n in names})
    se.write(folder/'REGISTRATION.json', reg)
    print(json.dumps({k:reg[k] for k in ('status','family','draws','inside_draws')}), flush=True)


def initialize(family, strengths):
    global _GRID
    se.initialize(family)
    _GRID = np.asarray(strengths)


def worker(job):
    index, u = job
    values, controls = evaluate(se._FAMILY, u, se._STATE, _GRID)
    return index, values, controls


def run(family, workers):
    folder, reg = check(family)
    if (folder/'START.json').exists():
        raise FileExistsError('Existing run preserved; verify live handle before any separate recovery')
    if workers < 1:
        raise ValueError('At least one worker required')
    source = se.ROOT/reg['source_run']
    with np.load(source/'PROPOSALS.npz') as archive:
        inside = archive['inside'].copy()
        u = archive['unit_cube'].copy()
    # Check space for immutable chunks plus a complete diagnostic memory map.
    required = 3 * reg['draws'] * len(STRENGTHS) * reg['targets'] * 8
    if shutil.disk_usage(folder).free < required:
        raise OSError('Insufficient space for full continuous curves and analysis')
    se.write(folder/'START.json', dict(date_utc=datetime.now(timezone.utc).isoformat(),
        family=family, workers=workers, pid=os.getpid(), draws=reg['draws'],
        registration_sha256=se.sha(folder/'REGISTRATION.json')))
    jobs = [(int(i), u[i]) for i in np.flatnonzero(inside)]
    started, completed, chunk = time.monotonic(), 0, []
    with mp.get_context('fork').Pool(workers, initializer=initialize, initargs=(family, STRENGTHS)) as pool:
        for index, values, controls in pool.imap_unordered(worker, jobs, chunksize=1):
            chunk.append((index, values, controls)); completed += 1
            if len(chunk) == 16 or completed == len(jobs):
                path = folder/f'chunk_{(completed-1)//16:05d}.npz'
                se.save_arrays(path, indices=np.array([c[0] for c in chunk]),
                    components=np.stack([c[1] for c in chunk]),
                    controls_json=np.asarray(json.dumps([dict(index=c[0], **c[2]) for c in chunk])))
                chunk = []
                progress = dict(completed=completed, valid_draws=len(jobs),
                    seconds=time.monotonic()-started, date_utc=datetime.now(timezone.utc).isoformat())
                se.write(folder/'PROGRESS.json', progress, replace=True)
                print(json.dumps(progress), flush=True)
    hashes = {p.name:se.sha(p) for p in folder.glob('chunk_*.npz')}
    se.write(folder/'EVALUATIONS_COMPLETE.json', dict(status='SOURCE_CURVE_EVALUATIONS_COMPLETE',
        completed=completed, registration_sha256=se.sha(folder/'REGISTRATION.json'), hashes=hashes,
        scientific_acceptance=False, analysis_completed=False))


def analyze(family):
    folder, reg = check(family)
    complete = json.loads((folder/'EVALUATIONS_COMPLETE.json').read_bytes())
    if complete['registration_sha256'] != se.sha(folder/'REGISTRATION.json'):
        raise ValueError('Evaluation receipt differs')
    if (folder/'RESULT.json').exists() or (folder/'CURVES.npy').exists():
        raise FileExistsError('Existing analysis or incomplete memory map preserved')
    with np.load(se.ROOT/reg['source_run']/'PROPOSALS.npz') as archive:
        inside, logq = archive['inside'].copy(), archive['logq'].copy()
    if complete['completed'] != int(inside.sum()):
        raise ValueError('Incomplete source evaluations')
    values = np.lib.format.open_memmap(folder/'CURVES.npy', mode='w+', dtype=np.float64,
        shape=(len(inside), len(STRENGTHS), reg['targets']))
    values[:] = -np.inf
    seen = np.zeros(len(inside), dtype=bool)
    for name, digest in complete['hashes'].items():
        path = folder/name
        if se.sha(path) != digest:
            raise ValueError('Continuous checkpoint changed')
        with np.load(path) as archive:
            ids, data = archive['indices'], archive['components']
            controls = json.loads(str(archive['controls_json']))
            if (len(np.unique(ids)) != len(ids) or np.any(ids < 0) or np.any(ids >= len(inside)) or
                    np.any(seen[ids]) or not inside[ids].all() or
                    ids.tolist() != [v['index'] for v in controls] or
                    data.shape != (len(ids), len(STRENGTHS), reg['targets']) or not np.isfinite(data).all()):
                raise ValueError('Invalid complete continuous checkpoint')
            for point in controls:
                if len(point['controls']) != 2:
                    raise ValueError('Missing PSD controls')
                for row in point['controls']:
                    if (row['max_relative_wave_error'] > 1e-6 or row['max_logL_error'] > .001 or
                            len(row['phase_quadrature']) != len(STRENGTHS) or
                            any(q['error'] > 1e-5 for q in row['phase_quadrature'])):
                        raise ValueError('Failed numerical controls in checkpoint')
            values[ids] = data; seen[ids] = True
    if not np.array_equal(seen, inside):
        raise ValueError('Missing source coordinates')
    values.flush()
    statistics = curve_statistics(STRENGTHS, values, logq)
    se.save_arrays(folder/'RESULT_ARRAYS.npz', strengths=STRENGTHS, **statistics)
    report = read_curves(STRENGTHS, statistics, se.load_state()['labels'])
    report.update(status='CONTINUOUS_SOURCE_CALIBRATION_DIAGNOSTIC', family=family,
        draws=len(inside), valid_draws=int(inside.sum()),
        scientific_acceptance=False, registration_sha256=se.sha(folder/'REGISTRATION.json'),
        complete_evaluations_sha256=se.sha(folder/'EVALUATIONS_COMPLETE.json'),
        arrays_sha256=se.sha(folder/'RESULT_ARRAYS.npz'), curves_sha256=se.sha(folder/'CURVES.npy'))
    se.write(folder/'RESULT.json', report)
    print(json.dumps(dict(status=report['status'], family=family,
        usable_curves=sum(r['numerically_usable'] for r in report['curves']),
        locally_passing_cells=sum(r['numerical_and_local_calibration_pass'] for r in report['cells']))), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=('register', 'run', 'analyze'))
    parser.add_argument('--family', choices=tuple(SOURCES), required=True)
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args()
    if args.command == 'register':
        register(args.family)
    else:
        folder = folder_for(args.family)
        with open(folder/'RUN.lock', 'a+b') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            if args.command == 'run':
                run(args.family, args.workers)
            else:
                analyze(args.family)
