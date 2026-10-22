"""Synthetic falsifiers for bounded causal-error bounds; not a device simulation."""
import json
import numpy as np
from scipy.linalg import expm

def norm(x):
    return float(np.linalg.norm(x, 2))

def comm(x, y):
    return x @ y - y @ x

def dual(h, jumps, b):
    out = 1j * comm(h, b)
    for l in jumps:
        ld = l.conj().T
        out += ld @ b @ l - (ld @ l @ b + b @ ld @ l) / 2
    return out

def matrix(h, jumps):
    columns = []
    for k in range(16):
        e = np.zeros(16, complex)
        e[k] = 1
        columns.append(dual(h, jumps, e.reshape((4, 4), order='F')).reshape(-1, order='F'))
    return np.column_stack(columns)

def run():
    i = np.eye(2)
    x = np.array([[0, 1], [1, 0]], complex)
    z = np.diag([1., -1.]).astype(complex)
    h0 = .3 * np.kron(z, i)
    l0 = .7 * np.kron(x, i)
    b = np.kron(i, z)
    g0 = matrix(h0, [l0])
    t = .7
    vector = b.reshape(-1, order='F')
    evolved0 = (expm(t * g0) @ vector).reshape((4, 4), order='F')
    local_error = norm(evolved0 - b)
    rows = []
    for epsilon in [.1, .05, .025]:
        h = h0 + epsilon * np.kron(x, x)
        l = l0 + epsilon * np.kron(z, x)
        g = matrix(h, [l])
        evolved = (expm(t * g) @ vector).reshape((4, 4), order='F')
        defect = norm(comm(h, b)) + norm(l) * (norm(comm(b, l)) + norm(comm(l.conj().T, b))) / 2
        comparison = 2 * norm(h - h0) + 2 * norm(l - l0) * (norm(l) + norm(l0))
        observed = norm(evolved - b)
        rows.append({'epsilon':epsilon, 'observed':observed, 'direct_bound':t*defect,
                     'comparison_bound':t*comparison*norm(b), 'generator_defect':norm(dual(h,[l],b))})
    checks = [
        {'name':'local_semigroup_fixes_external_observable','passed':local_error <= 1e-12, 'value':local_error},
        {'name':'nonlocal_control_is_detected','passed':all(r['observed'] > 1e-4 for r in rows)},
        {'name':'direct_and_comparison_bounds_hold','passed':all(r['observed'] <= min(r['direct_bound'],r['comparison_bound'])+1e-12 for r in rows)},
    ]
    return {'scope':'SYNTHETIC_BOUNDED_TWO_QUBIT_ONLY','checks':checks,'rows':rows,
            'passed':all(c['passed'] for c in checks),'physical_calibration':False,'R66_locality_proved':False}

if __name__ == '__main__':
    result=run()
    print(json.dumps(result, indent=2, allow_nan=False))
    raise SystemExit(0 if result['passed'] else 1)
