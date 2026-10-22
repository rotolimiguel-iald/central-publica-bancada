"""Baseline extraction only from pinned own qualifier; no grid runner."""
import numpy as np

def stellar_baseline(errors, rows):
    ak = [x['anchor'] for x in errors['anchor_errors']]
    mk = [x['mas_key'] for x in errors['mas_reference_errors']]
    hk = [x['key'] for x in errors['primitive_hms_groups']]
    assert all((len(set(keys)) == len(keys) for keys in (ak, mk, hk)))
    a = np.array([float(x['sigma_mag']) for x in errors['anchor_errors']])
    m = np.array([float(x['sigma_mag']) for x in errors['mas_reference_errors']])
    h = np.array([float(x['sigma_mag']) for x in errors['primitive_hms_groups']])
    row_hms = {row_id: x['key'] for x in errors['primitive_hms_groups'] for row_id in x['row_ids']}
    ai = [ak.index(x['anchor']) for x in rows]
    mi = [mk.index('&'.join([x['method'], x['anchor'], x['source']])) for x in rows]
    hi = [hk.index(row_hms[x['row_id']]) for x in rows]
    A, B, H = (np.eye(len(ak))[ai], np.eye(len(mk))[mi], np.eye(len(hk))[hi])
    anchor = A * a @ (A * a).T
    M, U = (B * m, H * h)
    baseline = anchor + M @ M.T + U @ U.T
    return baseline
