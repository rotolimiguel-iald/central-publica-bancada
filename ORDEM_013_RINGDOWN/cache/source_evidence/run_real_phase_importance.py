"""Registered fresh source draws using validated real phase interpolation."""
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
from importance_source_evidence import importance_statistics
from phase_marginal_real_source import phase_marginal_loglikes

STAGE = se.ROOT/'phase_real_refined'
draw = tp.draw


def check():
    tp.STAGE = STAGE
    return tp.check()


def evaluate_real(job):
    index, u = job
    value, metadata = phase_marginal_loglikes(se._FAMILY, u, se._STATE)
    return index, value, metadata


def run(args):
    proposal = check()
    oracle_result = json.loads((STAGE / 'PROPOSAL_ORACLE.json').read_bytes())
    if oracle_result['status'] != 'PASS_TRANSPORT_PROPOSAL_MOMENTS':
        raise ValueError('Unvalidated proposal')
    folder = STAGE / f'{proposal['family']}_seed{args.seed}_N{args.draws}'
    folder.mkdir(exist_ok=False)
    samples = draw(proposal, args.draws, args.seed)
    se.save_arrays(folder / 'PROPOSALS.npz', **samples)
    se.write(folder / 'START.json', dict(date_utc=datetime.now(timezone.utc).isoformat(), family=proposal['family'], seed=args.seed, draws=args.draws, transport_registration_sha256=se.sha(STAGE / 'REGISTRATION.json'), physical_prior_changed=False, phase_registration_sha256=se.sha(pm.REG), proposal_sha256=se.sha(STAGE / 'PROPOSAL.json')))
    values = np.full((args.draws, 2400), -np.inf)
    jobs = [(int(i), samples['unit_cube'][i]) for i in np.flatnonzero(samples['inside'])]
    metadata = []
    chunk = []
    done = 0
    number = 0
    start = time.monotonic()
    with mp.get_context('fork').Pool(args.processes, initializer=se.initialize, initargs=(proposal['family'],)) as pool:
        for index, value, meta in pool.imap_unordered(evaluate_real, jobs, chunksize=1):
            values[index] = value
            chunk.append((index, value, meta))
            metadata.append(dict(index=index, **meta))
            done += 1
            if len(chunk) == 16 or done == len(jobs):
                se.save_arrays(folder / f'chunk_{number:05d}.npz', indices=np.array([c[0] for c in chunk]), components=np.stack([c[1] for c in chunk]), controls_json=np.asarray(json.dumps([dict(index=c[0], **c[2]) for c in chunk])))
                chunk = []
                number += 1
                progress = dict(done=done, valid_draws=len(jobs), seconds=time.monotonic() - start, date_utc=datetime.now(timezone.utc).isoformat())
                se.write(folder / 'PROGRESS.json', progress, replace=True)
                print(json.dumps(progress), flush=True)
    stats = importance_statistics(values, samples['logq'])
    se.save_arrays(folder / 'RESULT_ARRAYS.npz', **stats)
    passing = (np.minimum(stats['ESS'][:1200], stats['ESS'][1200:]) >= 100) & (np.maximum(stats['max_weight'][:1200], stats['max_weight'][1200:]) <= 0.05) & (stats['lnB_MC_sd'] <= 0.2)
    labels = se.load_state()['labels']
    rows = []
    for label in labels:
        cell = {k: label[k] for k in ('psd', 'source', 'injection_family', 'injection_a', 'snr')}
        if any((r['cell'] == cell for r in rows)):
            continue
        ids = np.array([i for i, l in enumerate(labels) if all((l[k] == v for k, v in cell.items()))])
        both = np.r_[ids, 1200 + ids]
        v = stats['lnB'][ids]
        rows.append(dict(cell=cell, N=len(ids), lnB_mean=float(v.mean()), lnB_sd_noise=float(v.std(ddof=1)), lnB_quantiles=np.quantile(v, [0.05, 0.5, 0.95]).tolist(), min_component_ESS=float(stats['ESS'][both].min()), max_weight=float(stats['max_weight'][both].max()), max_lnB_MC_sd=float(stats['lnB_MC_sd'][ids].max()), draws_passing_precision=int(passing[ids].sum())))
    report = dict(status='RINGDOWN_COORDINATE_PILOT_NOT_ACCEPTED', family=proposal['family'], seed=args.seed, draws=args.draws, evaluations=done, rows=rows, integration_controls=metadata, all_precision_pass=bool(passing.all()), draws_passing_precision=int(passing.sum()), ESS_range=[float(stats['ESS'].min()), float(stats['ESS'].max())], registration_sha256=se.sha(pm.REG), transport_registration_sha256=se.sha(STAGE / 'REGISTRATION.json'), source_parameters_integrated=7, source_parameters_sampled=6, physical_prior_changed=False, original_C6_changed=False, independent_repeat=False, scientific_acceptance=False, hashes={p.name: se.sha(p) for p in folder.glob('*.npz')})
    se.write(folder / 'RESULT.json', report)
    print(json.dumps({k: report[k] for k in ('status', 'draws', 'evaluations', 'draws_passing_precision', 'ESS_range')}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--processes', type=int, default=4)
    args = parser.parse_args()
    reg = json.loads((STAGE/'REGISTRATION.json').read_bytes())
    args.draws, args.seed = reg['draws'], reg['seed']
    with open(STAGE/'RUN.lock', 'a+b') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        run(args)
