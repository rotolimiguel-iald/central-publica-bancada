"""Qualify the proposed stellar covariance family using errors and identifiers only."""
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
import hashlib
import json
import os
import sys
import time
import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from audit_inputs import file_info, save_json
from singular_gaussian_v2 import SupportGaussian


def block_correlation(keys, groups, scenario):
    out = np.eye(len(keys))
    lookup = {key: i for i, key in enumerate(keys)}
    seen = set()
    for group in groups:
        if len(set(group)) != len(group) or seen.intersection(group):
            raise ValueError('Repeated primitive in a block partition')
        seen.update(group)
        indexes = [lookup[key] for key in group]
        signs = []
        for key in group:
            fields = key.split('&')
            method = next(x for x in fields if x.startswith(('ceph_', 'trgb_', 'jagb_')))
            negative = ((scenario == 'cepheid_opposite' and method.startswith('ceph_')) or
                        (scenario == 'SH0ES_JAGB_opposite' and method.startswith('jagb_') and fields[-1] == 'SH0ES'))
            signs.append(-1 if negative else 1)
        out[np.ix_(indexes, indexes)] = np.outer(signs, signs)
    return out


def main():
    protocol_path = ROOT / 'STELLAR_FAMILY_PROTOCOL.json'
    protocol = json.loads(protocol_path.read_bytes())
    target = ROOT / 'STELLAR_FAMILY_RESULT.json'
    if target.exists():
        raise RuntimeError('Existing control result; do not repeat')
    for pin in protocol['inputs']:
        actual = file_info(pin['path'])
        if actual['sha256'] != pin['sha256'] or actual['bytes'] != pin['bytes']:
            raise ValueError('Input pin changed: ' + pin['path'])
    start, cpu = time.perf_counter(), time.process_time()
    base = ROOT.parent / 'h0dn_documentary_review/jagb_extension'
    selection = json.loads((base / 'SELECTION_V01_IDENTIFIERS.json').read_bytes())
    errors = json.loads((base / 'residual_systematics/ERROR_COMPONENTS.json').read_bytes())
    contract = json.loads((base / 'residual_systematics/CONTRATO_PSD_CANDIDATO.json').read_bytes())
    rows = selection['v01']['hosts']
    ak = [x['anchor'] for x in errors['anchor_errors']]
    mk = [x['mas_key'] for x in errors['mas_reference_errors']]
    hk = [x['key'] for x in errors['primitive_hms_groups']]
    assert all(len(set(keys)) == len(keys) for keys in (ak, mk, hk))
    a = np.array([float(x['sigma_mag']) for x in errors['anchor_errors']])
    m = np.array([float(x['sigma_mag']) for x in errors['mas_reference_errors']])
    h = np.array([float(x['sigma_mag']) for x in errors['primitive_hms_groups']])
    row_hms = {row_id: x['key'] for x in errors['primitive_hms_groups'] for row_id in x['row_ids']}
    ai = [ak.index(x['anchor']) for x in rows]
    mi = [mk.index('&'.join([x['method'], x['anchor'], x['source']])) for x in rows]
    hi = [hk.index(row_hms[x['row_id']]) for x in rows]
    A, B, H = np.eye(len(ak))[ai], np.eye(len(mk))[mi], np.eye(len(hk))[hi]
    anchor = (A * a) @ (A * a).T
    M, U = B * m, H * h
    baseline = anchor + M @ M.T + U @ U.T
    expected_diag = a[ai]**2 + m[mi]**2 + h[hi]**2
    # An independent pairwise transcription of the documented upstream rule.
    pairwise = np.zeros_like(baseline)
    for i in range(len(rows)):
        for j in range(len(rows)):
            pairwise[i,j] = ((a[ai[i]]**2 if ai[i] == ai[j] else 0) +
                             (m[mi[i]]**2 if mi[i] == mi[j] else 0) +
                             (h[hi[i]]**2 if hi[i] == hi[j] else 0))
    assert np.max(np.abs(pairwise-baseline)) < 1e-15
    guard = SupportGaussian.from_covariance(baseline, relative_cutoff=1e-12, absolute_cutoff=0, support_tolerance=1e-10)
    projector = guard.null_vectors @ guard.null_vectors.T
    groups = contract['groups']
    cases = []
    seen = {}
    for scenario_row in contract['candidate_grid']['sign_scenarios']:
        scenario = scenario_row['id']
        ref = block_correlation(mk, groups['MAS_same_program_at_N4258'], scenario)
        jagb = block_correlation(mk, [groups['MAS_JAGB_reference_pair']], scenario)
        host = block_correlation(hk, groups['HMS_by_eleven_hosts'], scenario)
        n5643 = block_correlation(hk, [groups['HMS_N5643_JAGB_pair']], scenario)
        for fractions in contract['candidate_grid']['fraction_tuples_order_u_v_p_q']:
            u,v,p,q = [float(Fraction(x)) for x in fractions]
            assert min(u,v,p,q) >= 0 and u+v <= .75 and p+q <= .75
            rm = (1-u-v)*np.eye(len(mk)) + u*ref + v*jagb
            rh = (1-p-q)*np.eye(len(hk)) + p*host + q*n5643
            assert np.min(np.linalg.eigvalsh(rm)) >= .25-1e-12
            assert np.min(np.linalg.eigvalsh(rh)) >= .25-1e-12
            c = anchor + M @ rm @ M.T + U @ rh @ U.T
            diag_error = float(np.max(np.abs(np.diag(c)-expected_diag)))
            assert diag_error < 1e-15
            # Exact quarter-fraction primitive matrices identify duplicate designs.
            design_hash = hashlib.sha256(rm.astype('<f8').tobytes()+rh.astype('<f8').tobytes()).hexdigest()
            entry = {'scenario':scenario, 'fractions':fractions, 'design_sha256':design_hash}
            if design_hash in seen:
                entry['same_primitive_design_as'] = seen[design_hash]
            else:
                supported = SupportGaussian.from_covariance(c, relative_cutoff=1e-12, absolute_cutoff=0, support_tolerance=1e-10)
                delta = float(np.linalg.norm(supported.null_vectors @ supported.null_vectors.T-projector, ord='fro'))
                assert supported.rank == guard.rank and delta < 1e-8
                ranks = [SupportGaussian.from_covariance(c, relative_cutoff=t, absolute_cutoff=0, support_tolerance=1e-10).rank for t in (1e-10,1e-14)]
                assert ranks == [guard.rank, guard.rank]
                entry.update(rank=supported.rank, cutoff=supported.threshold, null_projector_error=delta,
                             marginal_error=diag_error, cutoff_sensitivity_ranks=ranks)
                seen[design_hash] = len(cases)
            cases.append(entry)
            if time.perf_counter()-start > protocol['wall_budget_seconds']:
                raise TimeoutError('Control budget reached; no automatic repeat')
    result = {'at':datetime.now(timezone.utc).isoformat(), 'status':'ERROR_ONLY_STELLAR_BLOCK_QUALIFIED',
              'protocol':file_info(protocol_path), 'inputs':protocol['inputs'],
              'rows':len(rows), 'primitives':{'anchor':len(ak),'MAS':len(mk),'HMS':len(hk)},
              'baseline_rank':guard.rank, 'baseline_nullity':len(rows)-guard.rank,
              'pairwise_max_error':float(np.max(np.abs(pairwise-baseline))),
              'cases':cases, 'unique_primitive_designs':len(seen),
              'wall_seconds':time.perf_counter()-start, 'cpu_seconds':time.process_time()-cpu,
              'numpy':np.__version__, 'centres_opened':False, 'upstream_executed':False,
              'likelihood_evaluated':False, 'global_SN_background_covariance_assembled':False,
              'model_verdict':None, 'limitations':protocol['limitations']}
    save_json(target,result)
    print(json.dumps({k:result[k] for k in ['status','rows','baseline_rank','baseline_nullity','unique_primitive_designs','wall_seconds','cpu_seconds']}))


if __name__ == '__main__':
    main()
