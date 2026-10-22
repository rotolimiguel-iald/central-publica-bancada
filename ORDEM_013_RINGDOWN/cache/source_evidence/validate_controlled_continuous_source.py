"""Time complete continuous curves and check their binary stored endpoints."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
from datetime import datetime, timezone
import json
import time
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
from controlled_continuous_source import evaluate

STAGE = se.ROOT / 'controlled_continuous_validation'


def stored_points(folder, requested):
    result = json.loads((folder / 'RESULT.json').read_bytes())
    found = {}
    for path in sorted(folder.glob('chunk_*.npz')):
        with np.load(path) as archive:
            ids = archive['indices']
            selected = np.flatnonzero(np.isin(ids, requested))
            if len(selected):
                if se.sha(path) != result['hashes'][path.name]:
                    raise ValueError('Stored binary checkpoint changed')
                data = archive['components']
                for k in selected:
                    index = int(ids[k])
                    if index in found:
                        raise ValueError('Duplicate stored source point')
                    found[index] = (data[k], path.name, se.sha(path))
    if set(found) != set(requested):
        raise ValueError('Incomplete binary reference')
    return found


def main():
    pm.check()
    phenom = se.ROOT / 'phase_ringdown_real_continuation/IMRPhenomXPHM_seed130892_N16384'
    seob = se.ROOT / 'phase_native_seob/SEOBNRv4HM_seed130901_N2048'
    ph_rate = json.loads((phenom / 'real_rate_control/RESULT.json').read_bytes())
    se_rate = json.loads((seob / 'AUDIT_RATE.json').read_bytes())
    jobs = [('IMRPhenomXPHM', phenom, [15627, max(ph_rate['rows'], key=lambda r:r['max_active_logL_change'])['index']]),
        ('SEOBNRv4HM', seob, [max(se_rate['diagnostic_points'], key=lambda r:r['pooled_weight'])['index'],
         max(se_rate['diagnostic_points'], key=lambda r:r['dominant_components'])['index']])]
    strengths = np.arange(-4., 4.25, .5)
    names = ['validate_controlled_continuous_source.py', 'controlled_continuous_source.py',
        'real_continuous_phase_source.py', 'real_fourier_phase.py', 'native_seob_phase_source.py',
        'continuous_phase_source.py', 'coherent_imr_model.py', 'continuous_real_phase_validation/RESULT.json']
    names += [str((folder / name).relative_to(se.ROOT)) for _,folder,_ in jobs for name in ('PROPOSALS.npz', 'RESULT.json')]
    STAGE.mkdir(exist_ok=False)
    se.write(STAGE / 'REGISTRATION.json', dict(date_utc=datetime.now(timezone.utc).isoformat(),
        strengths=strengths.tolist(), reading='R-B', sample_rate=8192,
        jobs=[dict(family=f, folder=str(p.relative_to(se.ROOT)), indices=i) for f,p,i in jobs],
        purpose='Validate the complete curve evaluator and estimate cost, not integrate source parameters',
        scientific_acceptance=False, hashes={n:se.sha(se.ROOT/n) for n in names}))
    state = se.load_state()
    rows = []
    for family, folder, indices in jobs:
        indices = sorted(set(indices))
        references = stored_points(folder, indices)
        with np.load(folder/'PROPOSALS.npz') as archive:
            coordinates = archive['unit_cube'][indices]
        for index, u in zip(indices, coordinates):
            started = time.monotonic()
            values, controls = evaluate(family, u, state, strengths)
            seconds = time.monotonic() - started
            baseline, name, digest = references[index]
            endpoints = values[[int(np.flatnonzero(strengths == a)[0]) for a in (0.,1.)]].ravel()
            error = float(np.max(np.abs(endpoints - baseline)))
            if error > 2e-5:
                raise ValueError('Continuous evaluator changed stored binary likelihoods')
            se.save_arrays(STAGE/f'{family}_{index}.npz', strengths=strengths, components=values)
            row = dict(family=family, index=index, seconds=seconds, endpoint_error=error,
                binary_checkpoint=name, binary_checkpoint_sha256=digest, **controls)
            rows.append(row)
            se.write(STAGE/f'{family}_{index}.json', row)
            print(json.dumps({k:row[k] for k in ('family','index','seconds','endpoint_error')}), flush=True)
    result = dict(status='PASS_CONTROLLED_CONTINUOUS_SOURCE_EVALUATOR', rows=rows,
        source_integration_completed=False, physical_bias_coverage_completed=False,
        scientific_acceptance=False, strengths=strengths.tolist(),
        registration_sha256=se.sha(STAGE/'REGISTRATION.json'),
        hashes={p.name:se.sha(p) for p in STAGE.glob('*.npz')})
    se.write(STAGE/'RESULT.json', result)
    print(json.dumps(dict(status=result['status'], points=len(rows))), flush=True)


if __name__ == '__main__':
    main()
