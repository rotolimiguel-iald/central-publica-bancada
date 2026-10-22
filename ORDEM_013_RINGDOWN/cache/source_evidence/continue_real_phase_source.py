"""Resume the terminal Phenom draw set in a new, registered directory.

Reuse only saved complete likelihood vectors. Never drop the failed point or
change the total importance denominator. Old numerical control maxima lost
with the worker process are explicitly unavailable, not reconstructed.
"""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
import argparse
from datetime import datetime, timezone
import fcntl
import json
import multiprocessing as mp
import time
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
import transport_phase_source as tp
from phase_marginal_real_source import phase_marginal_loglikes
from importance_source_evidence import importance_statistics

OLD_STAGE = se.ROOT/'phase_ringdown_balanced'
NAME = 'IMRPhenomXPHM_seed130892_N16384'
OLD = OLD_STAGE/NAME
STAGE = se.ROOT/'phase_ringdown_real_continuation'
FOLDER = STAGE/NAME
DIAG = se.ROOT/'failed_phenom_phase_diagnostic'
VALID = se.ROOT/'real_phase_adapter_validation_corrected'


def copy_bytes(source, target):
    if target.exists():
        raise FileExistsError(target)
    raw = source.read_bytes()
    temporary = target.with_name(target.name+'.part')
    temporary.write_bytes(raw)
    if temporary.read_bytes() != raw:
        raise ValueError('Incomplete custody copy')
    temporary.replace(target)


def read_chunks(folder, inside, dimension=2400):
    values = np.full((len(inside), dimension), -np.inf)
    seen = np.zeros(len(inside), dtype=bool)
    paths = sorted(folder.glob('chunk_*.npz'))
    for path in paths:
        with np.load(path) as archive:
            ids, components = archive['indices'], archive['components']
            if (ids.ndim != 1 or not np.issubdtype(ids.dtype, np.integer) or
                    np.any(ids < 0) or np.any(ids >= len(inside)) or
                    len(np.unique(ids)) != len(ids) or np.any(seen[ids]) or
                    not np.all(inside[ids]) or components.shape != (len(ids), dimension) or
                    not np.all(np.isfinite(components))):
                raise ValueError('Invalid saved complete components: '+str(path))
            values[ids] = components
            seen[ids] = True
    return values, seen, paths


def register():
    tp.STAGE = OLD_STAGE
    tp.check()
    if (OLD/'RESULT.json').exists():
        raise ValueError('Original terminal run unexpectedly completed')
    validation = json.loads((VALID/'RESULT.json').read_bytes())
    if (validation['status'] != 'PASS_REAL_PHASE_ADAPTER' or
            validation['registration_sha256'] != se.sha(VALID/'REGISTRATION.json')):
        raise ValueError('Missing matching real interpolation validation')
    vreg = json.loads((VALID/'REGISTRATION.json').read_bytes())
    for name, expected in vreg['hashes'].items():
        if se.sha(se.ROOT/name) != expected:
            raise ValueError('Changed real phase validation input')
    old_reg = json.loads((OLD_STAGE/'REGISTRATION.json').read_bytes())
    start = json.loads((OLD/'START.json').read_bytes())
    oracle = json.loads((OLD_STAGE/'PROPOSAL_ORACLE.json').read_bytes())
    if (oracle['status'] != 'PASS_TRANSPORT_PROPOSAL_MOMENTS' or
            oracle['registration_sha256'] != se.sha(OLD_STAGE/'REGISTRATION.json')):
        raise ValueError('Missing original proposal validation')
    with np.load(OLD/'PROPOSALS.npz') as archive:
        inside, u = archive['inside'].copy(), archive['unit_cube'].copy()
    values, seen, chunks = read_chunks(OLD, inside)
    original_count = int(seen.sum())
    replay = json.loads((DIAG/'RESULT.json').read_bytes())
    replay_ids, replay_values, metadata = [], [], []
    provenance = list(chunks)+[OLD/'PROPOSALS.npz', OLD/'START.json', VALID/'RESULT.json', VALID/'REGISTRATION.json', DIAG/'RESULT.json']
    for row in replay['rows']:
        i = row['index']
        if seen[i] or not inside[i] or not np.array_equal(row['coordinates'], u[i]):
            raise ValueError('Replay coordinates changed or duplicated')
        if row['status'] == 'ORIGINAL_PASSED_ON_REPLAY':
            path = DIAG/f'point_{i}_passing.npz'
            controls = row['controls']
            origin = 'original_passed_replay'
        else:
            path = VALID/f'point_{i}.npz'
            matches = [r for r in validation['source_rows'] if r['index'] == i]
            if len(matches) != 1:
                raise ValueError('Failed source lacks full validation')
            controls = matches[0]['controls']
            origin = 'corrected_full_wave_validation'
        with np.load(path) as archive:
            value = archive['components'].copy()
        if value.shape != (2400,) or not np.all(np.isfinite(value)):
            raise ValueError('Invalid replay component vector')
        replay_ids.append(i); replay_values.append(value)
        metadata.append(dict(index=i, origin=origin, **controls))
        provenance += [path, DIAG/f'point_{i}.json']
    STAGE.mkdir(exist_ok=False); FOLDER.mkdir()
    copy_bytes(OLD_STAGE/'PROPOSAL.json', STAGE/'PROPOSAL.json')
    copy_bytes(OLD/'PROPOSALS.npz', FOLDER/'PROPOSALS.npz')
    for chunk in chunks:
        copy_bytes(chunk, FOLDER/chunk.name)
    next_number = max(int(p.stem.split('_')[1]) for p in chunks)+1
    extra = FOLDER/f'chunk_{next_number:05d}.npz'
    se.save_arrays(extra, indices=np.array(replay_ids), components=np.array(replay_values))
    se.write(extra.with_suffix('.json'), dict(components_sha256=se.sha(extra), controls=metadata))
    names = list(old_reg['hashes'])+[
        'continue_real_phase_source.py', 'real_fourier_phase.py', 'phase_marginal_real_source.py',
        'REAL_PHASE_ADAPTER_PROVENANCE.json', 'phase_ringdown_balanced/REGISTRATION.json',
        'phase_ringdown_balanced/PROPOSAL_ORACLE.json', 'phase_ringdown_real_continuation/PROPOSAL.json',
        'REAL_PHASE_VALIDATION_CORRECTION.json']+[str(p.relative_to(se.ROOT)) for p in provenance]
    reg = dict(status='REGISTERED_REAL_PHASE_CONTINUATION_OF_TERMINAL_RUN',
        date_utc=datetime.now(timezone.utc).isoformat(), family=start['family'],
        draws=start['draws'], seed=start['seed'], original_directory=str(OLD.relative_to(se.ROOT)),
        original_terminal_handle=62818, original_observed_exit_code=1,
        original_preserved_evaluations=original_count, recovered_evaluations=len(replay_ids),
        remaining_evaluations=int(inside.sum())-original_count-len(replay_ids),
        total_valid_evaluations=int(inside.sum()), proposal_or_draws_changed=False,
        physical_prior_changed=False, waveform_model_changed=False,
        correction='Use the real Nyquist cosine. Original returned real likelihoods are algebraically unchanged.',
        metadata_limitation='Original chunk writers returned only after all full-wave and phase tests passed, but per-point numerical maxima were in process memory and are unavailable for the original saved chunks.',
        acceptance='Unchanged ESS>=100,maxweight<=.05,MCsdlnB<=.2, independent repeat agreement, rate and continuous-strength calibration',
        copied_npz_hashes={p.name:se.sha(p) for p in FOLDER.glob('*.npz')},
        initial_sidecar_hashes={p.name:se.sha(p) for p in FOLDER.glob('chunk_*.json')},
        scientific_acceptance=False, C6_changed=False,
        hashes={n:se.sha(se.ROOT/n) for n in dict.fromkeys(names)})
    se.write(STAGE/'REGISTRATION.json', reg)
    oracle.update(original_registration_sha256=oracle['registration_sha256'],
        registration_sha256=se.sha(STAGE/'REGISTRATION.json'), fresh_oracle_run=False,
        reused_from='phase_ringdown_balanced/PROPOSAL_ORACLE.json',
        reuse_reason='Byte-identical proposal and unchanged transport')
    se.write(STAGE/'PROPOSAL_ORACLE.json', oracle)
    se.write(FOLDER/'START.json', dict(**start, continuation_registration_sha256=se.sha(STAGE/'REGISTRATION.json'),
        continuation_date_utc=datetime.now(timezone.utc).isoformat()))
    print(json.dumps({k:reg[k] for k in ('status', 'draws', 'original_preserved_evaluations', 'recovered_evaluations', 'remaining_evaluations')}), flush=True)


def check():
    tp.STAGE = STAGE
    tp.check()
    reg = json.loads((STAGE/'REGISTRATION.json').read_bytes())
    for key in ('copied_npz_hashes', 'initial_sidecar_hashes'):
        for name, expected in reg[key].items():
            if se.sha(FOLDER/name) != expected:
                raise ValueError('Saved continuation input changed: '+name)
    return reg


def evaluate(job):
    index, u = job
    value, metadata = phase_marginal_loglikes(se._FAMILY, u, se._STATE)
    return index, value, dict(index=index, origin='corrected_continuation', **metadata)


def run(processes):
    reg = check()
    if (FOLDER/'RESULT.json').exists():
        raise FileExistsError('Continuation already completed')
    with np.load(FOLDER/'PROPOSALS.npz') as archive:
        inside, u, logq = (archive[k].copy() for k in ('inside', 'unit_cube', 'logq'))
    values, seen, chunks = read_chunks(FOLDER, inside)
    controls = []
    for chunk in chunks:
        sidecar = chunk.with_suffix('.json')
        if not sidecar.exists():
            if chunk.name not in reg['copied_npz_hashes']:
                raise ValueError('New chunk lacks its numerical-control checkpoint')
            continue
        info = json.loads(sidecar.read_bytes())
        if info['components_sha256'] != se.sha(chunk):
            raise ValueError('Control checkpoint does not match component bytes')
        with np.load(chunk) as archive:
            if sorted(archive['indices']) != sorted(r['index'] for r in info['controls']):
                raise ValueError('Control checkpoint index mismatch')
        controls += info['controls']
    jobs = [(int(i), u[i]) for i in np.flatnonzero(inside & ~seen)]
    number = max(int(p.stem.split('_')[1]) for p in chunks)+1
    done = 0; batch = []; begin = time.monotonic()
    with mp.get_context('fork').Pool(processes, initializer=se.initialize, initargs=(reg['family'],)) as pool:
        for index, value, metadata in pool.imap_unordered(evaluate, jobs, chunksize=1):
            values[index] = value; seen[index] = True
            batch.append((index, value, metadata)); controls.append(metadata); done += 1
            if len(batch) == 16 or done == len(jobs):
                chunk = FOLDER/f'chunk_{number:05d}.npz'
                se.save_arrays(chunk, indices=np.array([v[0] for v in batch]), components=np.stack([v[1] for v in batch]))
                se.write(chunk.with_suffix('.json'), dict(components_sha256=se.sha(chunk), controls=[v[2] for v in batch]))
                batch = []; number += 1
                progress = dict(new_done=done, new_required=len(jobs), total_saved=int(seen.sum()),
                    valid_draws=int(inside.sum()), seconds=time.monotonic()-begin, date_utc=datetime.now(timezone.utc).isoformat())
                se.write(FOLDER/'PROGRESS.json', progress, replace=True)
                print(json.dumps(progress), flush=True)
    if not np.array_equal(seen, inside):
        raise ValueError('Incomplete draw set, cannot form evidence')
    stats = importance_statistics(values, logq)
    se.save_arrays(FOLDER/'RESULT_ARRAYS.npz', **stats)
    passing = ((np.minimum(stats['ESS'][:1200], stats['ESS'][1200:]) >= 100) &
               (np.maximum(stats['max_weight'][:1200], stats['max_weight'][1200:]) <= .05) & (stats['lnB_MC_sd'] <= .2))
    labels = se.load_state()['labels']; rows = []
    for label in labels:
        cell = {k:label[k] for k in ('psd', 'source', 'injection_family', 'injection_a', 'snr')}
        if any(r['cell'] == cell for r in rows):
            continue
        ids = np.array([i for i,l in enumerate(labels) if all(l[k] == v for k,v in cell.items())]); both = np.r_[ids,1200+ids]
        v = stats['lnB'][ids]
        rows.append(dict(cell=cell, N=len(ids), lnB_mean=float(v.mean()), lnB_sd_noise=float(v.std(ddof=1)),
            lnB_quantiles=np.quantile(v, [.05,.5,.95]).tolist(), min_component_ESS=float(stats['ESS'][both].min()),
            max_weight=float(stats['max_weight'][both].max()), max_lnB_MC_sd=float(stats['lnB_MC_sd'][ids].max()),
            draws_passing_precision=int(passing[ids].sum())))
    report = dict(status='REAL_PHASE_CONTINUATION_PILOT_NOT_ACCEPTED', family=reg['family'], seed=reg['seed'], draws=len(u),
        evaluations=int(inside.sum()), rows=rows, integration_controls=controls,
        control_metadata_coverage=dict(exact_maxima_available=len(controls), exact_maxima_unavailable=reg['original_preserved_evaluations'],
            statement=reg['metadata_limitation']),
        all_precision_pass=bool(passing.all()), draws_passing_precision=int(passing.sum()),
        ESS_range=[float(stats['ESS'].min()),float(stats['ESS'].max())], registration_sha256=se.sha(pm.REG),
        transport_registration_sha256=se.sha(STAGE/'REGISTRATION.json'), source_parameters_integrated=7,
        source_parameters_sampled=6, physical_prior_changed=False, original_C6_changed=False,
        independent_repeat=False, scientific_acceptance=False,
        hashes={p.name:se.sha(p) for p in FOLDER.glob('*.npz')},
        control_sidecar_hashes={p.name:se.sha(p) for p in FOLDER.glob('chunk_*.json')})
    se.write(FOLDER/'RESULT.json', report)
    print(json.dumps({k:report[k] for k in ('status','draws','evaluations','draws_passing_precision','ESS_range')}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('command', choices=['register','run'])
    parser.add_argument('--processes', type=int, default=2); args = parser.parse_args()
    if args.command == 'register':
        register()
    else:
        with open(STAGE/'RUN.lock', 'a+b') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            run(args.processes)
