"""Compare stored continuous endpoints to the separate binary source run.

Atomic checkpoint bytes are snapshotted, hashed and read once. Partial runs
may be inspected, but unmatched points remain pending and cannot pass a full
audit. No partial importance integral is substituted for the registered N.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
import numpy as np
import source_evidence as se
import run_continuous_source_curves as run


def checkpoint(path, reference_hash=None):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if reference_hash is not None and digest != reference_hash:
        raise ValueError('Completed checkpoint hash changed: ' + str(path))
    with np.load(io.BytesIO(raw)) as archive:
        ids, values = archive['indices'], archive['components']
        if (ids.ndim != 1 or not np.issubdtype(ids.dtype, np.integer) or
                len(np.unique(ids)) != len(ids) or len(ids) != len(values) or
                not np.isfinite(values).all()):
            raise ValueError('Invalid checkpoint rows')
        return ids.copy(), values.copy(), digest


def audit(family, require_complete=False):
    folder, reg = run.check(family)
    source = se.ROOT/reg['source_run']
    endpoints = [int(np.flatnonzero(run.STRENGTHS == a)[0]) for a in (0., 1.)]
    complete_path = folder/'EVALUATIONS_COMPLETE.json'
    binary_path = source/'RESULT.json'
    completed = complete_path.exists() and binary_path.exists()
    if require_complete and not completed:
        raise ValueError('Full endpoint audit requires both completed runs')
    curve_hashes = json.loads(complete_path.read_bytes())['hashes'] if complete_path.exists() else None
    binary_hashes = json.loads(binary_path.read_bytes())['hashes'] if binary_path.exists() else None
    with np.load(source/'PROPOSALS.npz') as archive:
        inside = archive['inside'].copy()
    wanted, curve_files = {}, {}
    for path in sorted(folder.glob('chunk_*.npz')):
        ids, values, digest = checkpoint(path, None if curve_hashes is None else curve_hashes[path.name])
        if (values.shape != (len(ids), len(run.STRENGTHS), reg['targets']) or
                np.any(ids < 0) or np.any(ids >= len(inside)) or not inside[ids].all()):
            raise ValueError('Continuous checkpoint violates registered dimensions/support')
        for index, value in zip(ids, values[:, endpoints].reshape(len(ids), -1)):
            if int(index) in wanted:
                raise ValueError('Duplicate continuous source index')
            wanted[int(index)] = value
        curve_files[path.name] = digest
    if not wanted:
        raise ValueError('No complete continuous checkpoint available')
    differences, binary_files, seen = [], {}, set()
    requested = np.array(sorted(wanted))
    for path in sorted(source.glob('chunk_*.npz')):
        # IDs are tiny: avoid materializing irrelevant large binary chunks.
        with np.load(path) as archive:
            intersects = bool(np.isin(archive['indices'], requested).any())
        if not intersects:
            continue
        ids, values, digest = checkpoint(path, None if binary_hashes is None else binary_hashes[path.name])
        if values.shape != (len(ids), 2*reg['targets']):
            raise ValueError('Binary checkpoint dimensions differ')
        binary_files[path.name] = digest
        for index, value in zip(ids, values):
            index = int(index)
            if index not in wanted:
                continue
            if index in seen:
                raise ValueError('Duplicate matched binary index')
            seen.add(index)
            delta = np.abs(wanted[index] - value)
            differences.append(dict(index=index, max_abs_logL_difference=float(delta.max()),
                a0_max=float(delta[:reg['targets']].max()), a1_max=float(delta[reg['targets']:].max())))
    if not differences:
        raise ValueError('No common complete source evaluations available yet')
    maximum = max(row['max_abs_logL_difference'] for row in differences)
    missing = sorted(set(wanted) - seen)
    full = completed and not missing and len(wanted) == int(inside.sum())
    if require_complete and not full:
        raise ValueError('Completed integral has missing endpoint comparisons')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    destination = folder/'endpoint_audits'/stamp
    destination.mkdir(parents=True, exist_ok=False)
    status = ('ENDPOINT_MISMATCH' if maximum > 2e-5 else
              'PASS_FULL_ENDPOINT_COMPARISON' if full else 'PASS_SNAPSHOT_ENDPOINT_COMPARISON')
    result = dict(status=status, date_utc=datetime.now(timezone.utc).isoformat(), family=family,
        total_registered_source_draws=len(inside), valid_source_draws=int(inside.sum()),
        continuous_points_snapshotted=len(wanted), matched_binary_points=len(seen),
        unmatched_points_pending=missing, max_abs_logL_difference=maximum,
        component_comparisons=2*reg['targets']*len(seen), full_comparison_complete=full,
        scientific_acceptance=False, source_integral_precision_claimed=False,
        covariance_and_noise_scope='Same draws and mocks; this is identity of numerical readers, not independent events',
        rows=differences, continuous_checkpoint_hashes=curve_files, binary_checkpoint_hashes=binary_files,
        continuous_registration_sha256=se.sha(folder/'REGISTRATION.json'),
        proposal_draws_sha256=se.sha(source/'PROPOSALS.npz'), script_sha256=se.sha(se.Path(__file__)))
    se.write(destination/'RESULT.json', result)
    print(json.dumps({k:result[k] for k in ('status','family','continuous_points_snapshotted',
        'matched_binary_points','max_abs_logL_difference','full_comparison_complete')}
        | dict(result_path=str((destination/'RESULT.json').relative_to(se.ROOT)))), flush=True)
    if maximum > 2e-5:
        raise ValueError('Continuous source extension changed binary endpoints')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--family', choices=tuple(run.SOURCES), required=True)
    parser.add_argument('--require-complete', action='store_true')
    args=parser.parse_args()
    audit(args.family,args.require_complete)
