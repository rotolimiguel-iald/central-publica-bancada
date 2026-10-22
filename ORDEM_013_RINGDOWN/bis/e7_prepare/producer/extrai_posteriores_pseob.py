"""Registered full-sample extraction; h5py stays on this side of the boundary.

No download, PE, strain access, waveform generation or Monte Carlo. Only
explicit source/dataset/field mappings: never choose a release or event by data.
Extraction additionally requires the principal's post-E2 authorization receipt.
"""
from pathlib import Path
import argparse
import json
import platform
import numpy as np
import h5py
from tgl_ringdown_ampliacao import (FIELDS, checked_context, contained, read_json,
                                     require_pin, sha, publish_new, validate_events,
                                     checked_authorization)


def prior_metadata(source, entry):
    """Read only explicitly named small textual prior declarations, never eval."""
    records = {}
    for field in FIELDS:
        declarations = []
        for name in entry['prior_paths'][field]:
            prefix = ''
            for part in name.strip('/').split('/'):
                prefix += '/' + part
                if not isinstance(source.get(prefix, getlink=True), h5py.HardLink):
                    raise ValueError('Prior declaration follows unpinned link')
            node = source[name]
            if (not isinstance(node, h5py.Dataset) or node.is_virtual or node.external or
                    not 1 <= node.size <= 256 or h5py.check_string_dtype(node.dtype) is None):
                raise ValueError('Unsupported/non-text prior metadata: ' + name)
            # Fixed-width allocation is bounded before I/O. Vlen text has no
            # metadata-only logical-length bound; validate decoded size below.
            if node.dtype.kind == 'S' and node.size * node.dtype.itemsize > 100000:
                raise ValueError('Prior text allocation too large')
            raw = np.asarray(node[()]).reshape(-1)
            if not all(isinstance(v, (str, bytes)) for v in raw):
                raise ValueError('Prior metadata contains non-text values')
            texts = [v.decode('utf-8') if isinstance(v, bytes) else v for v in raw]
            if sum(map(len, texts)) > 100000 or not all(t.strip() for t in texts):
                raise ValueError('Prior text too large or empty')
            declarations.append({'path': name, 'text': texts})
        if field in ('df220', 'dtau220') and not declarations:
            raise ValueError('Deformation prior declaration is required')
        records[field] = {'status': 'DECLARADO_TEXT_NOT_NORMALIZED' if declarations else
                          'OPEN_DERIVED_PRIOR_NOT_DECLARED', 'declarations': declarations,
                          'joint_factorization': 'OPEN', 'density': None}
    return records


def extract_one(root, entry):
    """Called only after E2 and principal authorization by extract()."""
    for stem in ('source', 'tar'):
        require_pin(contained(root, entry[stem + '_path']), entry[stem + '_sha256'])
    path = contained(root, entry['source_path'])
    if set(entry['fields']) != set(FIELDS) or set(entry['prior_paths']) != set(FIELDS):
        raise ValueError('Incomplete explicit field/prior mapping')
    if entry['mass_frame'] != 'detector' or entry['mass_unit'] != 'solar_mass':
        raise ValueError('Unregistered mass frame/units')
    with h5py.File(path, 'r') as source:
        # Reject external/soft links and virtual/external datasets.
        prefix = ''
        for part in entry['dataset'].strip('/').split('/'):
            prefix += '/' + part
            if not isinstance(source.get(prefix, getlink=True), h5py.HardLink):
                raise ValueError('Linked posterior outside pinned HDF5')
        ds = source[entry['dataset']]
        if not isinstance(ds, h5py.Dataset) or ds.ndim != 1 or not ds.dtype.names or ds.is_virtual or ds.external:
            raise ValueError('Only ordinary 1D compound posterior datasets supported')
        if ds.shape[0] != entry['N_source']:
            raise ValueError('Source sample count changed')
        if any('weight' in field.lower() for field in ds.dtype.names):
            raise ValueError('Posterior weights require an explicit audited implementation')
        if not all(field in ds.dtype.names for field in entry['fields'].values()):
            raise ValueError('Missing mapped posterior field')
        priors = prior_metadata(source, entry)
        columns = list(entry['fields'].values())
        data = ds.fields(columns)[()]  # one common row order, full samples
        samples = {key: np.asarray(data[name], dtype=float).tolist() for key, name in entry['fields'].items()}
    require_pin(path, entry['source_sha256'])  # catch source mutation during read
    out = {key: entry[key] for key in ('event_id', 'role', 'source_path', 'source_sha256',
                                      'tar_path', 'tar_sha256', 'dataset', 'model', 'mass_frame', 'mass_unit')}
    out.update(N=len(data), N_source=len(data), samples=samples, priors=priors,
               thinning={'factor': 1, 'seed': None, 'method': 'none'},
               sample_weights='equal_as_stored', source_field_mapping=entry['fields'])
    validate_events([out])
    return out


def extract(root, registration, registration_sha256, authorization, authorization_sha256):
    reg, guard = checked_context(root, registration, registration_sha256)
    spec = reg['e7']
    plan = read_json(contained(root, spec['plan_path']))
    checked_authorization(reg, guard, registration_sha256, authorization, authorization_sha256)
    if plan['status'] != 'READY_FOR_REGISTERED_CALIBRATION_EXTRACTION':
        raise ValueError('Extraction plan is not complete/reviewed')
    ids = [row['event_id'] for row in plan['events']]
    if len(ids) != len(set(ids)) or not ids:
        raise ValueError('Duplicate canonical events or empty extraction plan')
    products = [(e['source_sha256'], e['dataset']) for e in plan['events']]
    if len(products) != len(set(products)):
        raise ValueError('Duplicate source product')
    # Validate ALL roles before opening ANY posterior values. Blind support OPEN.
    for row in plan['events']:
        if row['role'] != 'calibration':
            raise ValueError('Blind extraction requires audited blinding adapter; unsupported here')
        guard.authorize_event(reg, row['event_id'], row['role'])
    events = [extract_one(root, row) for row in plan['events']]
    validate_events(events)
    return {'schema': 'POSTERIORES_PSEOB_V1', 'catalogue': plan['catalogue'],
            'registration_sha256': registration_sha256, 'plan_sha256': spec['plan_sha256'],
            'authorization_sha256': authorization_sha256,
            'producer_tree_sha256': spec['producer_tree_sha256'],
            'runtime': {'python': platform.python_version(), 'numpy': np.__version__,
                        'h5py': h5py.__version__, 'hdf5': h5py.version.hdf5_version},
            'events': events}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ('root', 'registration', 'registration-sha256', 'authorization', 'authorization-sha256', 'output'):
        ap.add_argument('--' + name, required=True)
    args = ap.parse_args()
    output = Path(args.output).resolve()
    cache = contained(args.root, 'ORDEM_013_RINGDOWN/cache')
    if output.parent != cache or not output.name.startswith('POSTERIORES_PSEOB_') or output.suffix != '.json':
        raise ValueError('Posterior JSON must be a new POSTERIORES_PSEOB_*.json directly in B/cache')
    result = extract(args.root, args.registration, args.registration_sha256,
                     args.authorization, args.authorization_sha256)
    publish_new(output, result)
    output.chmod(0o444)


if __name__ == '__main__':
    main()
