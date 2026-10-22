# Operational v2 only. Existing audited results remain in bis/f2_injection.
"""Bounded read-only contract check; distinguish declarations from global proof."""

def publish_exclusive(temp, destination):
    """Atomic no-replace publication; fail closed if hard links unsupported."""
    import os
    try:
        os.link(temp, destination)
    finally:
        temp.unlink()
from pathlib import Path
import hashlib, json
import h5py
import numpy as np
OUT = Path(__file__).resolve().parent
B = OUT.parents[1]

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()
meta = json.loads((OUT / 'METADATA.json').read_bytes())
src = B / meta['source']
if not sha(src) == meta['sha256']:
    raise ValueError("Guard rejected: sha(src) == meta['sha256']")
res = {'status': 'PARTIAL_PRIOR_CONTRACT_VERIFIED__NO_BAYES_FACTOR_IN_THIS_DIAGNOSTIC', 'lnB': None, 'source_sha256': sha(src), 'groups': {}, 'known': ['Analytic Uniform(-0.8,2) declarations for domega220 and dtau220 in both groups', 'Analytic Uniform(-0.8,0.8) declarations for domega440 and dtau440 in both groups', 'All archived analytic prior dictionaries are identical between groups', 'Joint posterior and prior-sample remnant fields exist'], 'not_proved': ['Global support and normalization of the restricted spin-dependent models over the full nuisance prior', 'Full reproducibility of the external prior_file and remnant conversion from this HDF5 alone'], 'decision': 'No claim that priors are wholly unknown or data unusable. Descriptive diagnostic only; no density ratio relabeled as a Bayes factor.', 'why_sample_check_is_not_proof': 'A finite prior sample checks observed support; it does not certify support everywhere under the nuisance prior.', 'necessary_identity': 'Z_L/Z_GR = integral p(eta,df=0,dtau=g_L(eta)|d)/pi(df=0,dtau=g_L(eta)|eta) d eta divided by the same integral with g=0, using identical normalized nuisance priors.', 'caution': 'Unknown injection truths do not themselves prevent a Bayes factor; the deferred issue here is the complete restricted-prior contract, not truth fields.', 'not_applied': ['R-A', 'R-B', 'R-MOD', 'R-PROP', 'R-GLOBAL', 'R-RAIZ-0', 'R-RAIZ-REST', 'R-RAIZ-EP4', 'R-RAIZ-COHERENT', 'R-LIN']}
with h5py.File(src, 'r') as f:
    for label in ['NR_with_44', 'NR_without_44']:
        g = f[label]
        fields = {}
        for name in ['final_spin_non_evolved', 'final_mass_non_evolved']:
            arr = g['priors/samples/' + name][:]
            ok = np.isfinite(arr)
            fields[name] = {'n': len(arr), 'finite': int(ok.sum()), 'min': float(arr[ok].min()), 'max': float(arr[ok].max())}
        res['groups'][label] = {'prior_remnant_sample_check': fields, 'prior_file': g['config_file/config/prior_file'][0].decode(), 'prior_dict': g['config_file/config/prior_dict'][0].decode(), 'default_prior': g['config_file/config/default_prior'][0].decode()}
if not sha(src) == meta['sha256']:
    raise ValueError("Guard rejected: sha(src) == meta['sha256']")
res['code_sha256'] = sha(Path(__file__))
p = OUT / 'PRIOR_CONTRACT.json'
if not not p.exists():
    raise FileExistsError('Guard rejected: not p.exists()')
raw = (json.dumps(res, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()
t = p.with_suffix('.json.tmp')
with t.open('xb') as f:
    f.write(raw)
if not t.read_bytes() == raw:
    raise ValueError('Guard rejected: t.read_bytes() == raw')
publish_exclusive(t, p)
print(json.dumps({'status': res['status'], 'lnB': None, 'groups': res['groups']}))
