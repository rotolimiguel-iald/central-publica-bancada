# Operational v2 only. Existing audited results remain in bis/f2_injection.
"""Read only selected public HDF5 metadata; never deserialize executable content."""

def publish_exclusive(temp, destination):
    """Atomic no-replace publication; fail closed if hard links unsupported."""
    import os
    try:
        os.link(temp, destination)
    finally:
        temp.unlink()
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
from pathlib import Path
import hashlib, json
import h5py
import numpy as np
OUT = Path(__file__).resolve().parent
B = OUT.parents[1]

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def new(name, obj):
    p = OUT / name
    raw = (json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()
    if p.exists():
        raise FileExistsError(p)
    t = p.with_suffix(p.suffix + '.tmp')
    with t.open('xb') as f:
        f.write(raw)
    if not t.read_bytes() == raw:
        raise ValueError('Guard rejected: t.read_bytes() == raw')
    publish_exclusive(t, p)

def clean(v):
    if isinstance(v, bytes):
        return v.decode('utf-8', errors='strict')
    if isinstance(v, np.ndarray):
        if v.dtype.names:
            return [{k: clean(x[k]) for k in v.dtype.names} for x in v]
        return [clean(x) for x in v]
    if isinstance(v, np.generic):
        return clean(v.item())
    if isinstance(v, float) and (not np.isfinite(v)):
        return None
    return v
schemas = B / 'bis/F2_CONTROL_SCHEMAS.json'
entry = [r for r in json.loads(schemas.read_bytes()) if 'pseobnr_injection' in r['path'] and r['path'].endswith('.h5')]
if not len(entry) == 1:
    raise ValueError('Guard rejected: len(entry) == 1')
src = B / entry[0]['path'].replace('\\', '/')
digest = sha(src)
if not digest == entry[0]['sha256']:
    raise ValueError("Guard rejected: digest == entry[0]['sha256']")
res = {'source': str(src.relative_to(B)), 'sha256': digest, 'bytes': src.stat().st_size, 'schema_receipt_sha256': sha(schemas), 'groups': {}}
config_keys = ['prior_dict', 'prior_file', 'default_prior', 'injection', 'injection_file', 'injection_dict', 'injection_numbers', 'waveform_approximant', 'waveform_arguments_dict', 'frequency_domain_source_model', 'mode_array', 'zero_noise', 'gaussian_noise', 'sampler', 'sampler_kwargs', 'duration', 'sampling_frequency', 'minimum_frequency', 'maximum_frequency', 'reference_frequency', 'likelihood_type']
with h5py.File(src, 'r') as f:
    for label in ('NR_with_44', 'NR_without_44'):
        g = f[label]
        d = {'keys': list(g.keys()), 'metadata': {}, 'priors_analytic': {}, 'posterior_fields': list(g['posterior_samples'].dtype.names), 'posterior_shape': list(g['posterior_samples'].shape)}
        for key in config_keys:
            path = 'config_file/config/' + key
            if path in g:
                d['metadata'][path] = clean(g[path][()])
        for path in ['injection_data', 'meta_data/other/injection_parameters', 'meta_data/sampler/nsamples', 'meta_data/sampler/pe_algorithm']:
            if path in g:
                d['metadata'][path] = clean(g[path][()])
        for key in g['priors/analytic']:
            d['priors_analytic'][key] = clean(g['priors/analytic/' + key][()])
        d['prior_sample_fields'] = list(g['priors/samples'].keys())
        res['groups'][label] = d
if not sha(src) == digest:
    raise ValueError('Guard rejected: sha(src) == digest')
new('METADATA.json', res)
print(json.dumps({'source': res['source'], 'sha256': digest, 'groups': {k: {'N': v['posterior_shape'], 'injection_data': v['metadata'].get('injection_data'), 'injection_parameters': v['metadata'].get('meta_data/other/injection_parameters'), 'priors': {p: v['priors_analytic'].get(p) for p in ['domega220', 'dtau220', 'domega440', 'dtau440']}, 'config': {p: x for p, x in v['metadata'].items() if not p.endswith('prior_dict')}} for k, v in res['groups'].items()}}, ensure_ascii=False))
