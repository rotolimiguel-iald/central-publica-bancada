"""Copy only the existing phase integral, replacing its real interpolation API."""
import ast
import hashlib
import json
import source_evidence as se


def main():
    path = se.ROOT/'phase_marginal_source.py'
    source = path.read_text(encoding='utf-8')
    tree = ast.parse(source)
    node = next(v for v in tree.body if isinstance(v, ast.FunctionDef) and v.name == 'phase_marginal_loglikes')
    original = ast.get_source_segment(source, node)
    expected = {'pc.evaluate_bank': 1, 'pc.bank_loglikes': 2}
    revised = original
    for before, count in expected.items():
        if revised.count(before) != count:
            raise ValueError('Unexpected original phase function')
        revised = revised.replace(before, before.replace('pc.', 'real.'))
    header = '''"""Copied original source integral; same physical source and tolerances.

Only the even-DFT Nyquist convention is corrected. This does not change the
real part returned by the previous interpolant. Full-wave held-out controls
and phase-integral accuracy checks are retained verbatim.
"""
import numpy as np
from scipy.special import logsumexp
import source_evidence as se
import peak_phase_coordinates as pc
import real_fourier_phase as real
from phase_marginal_source import six_to_physical

'''
    output = se.ROOT/'phase_marginal_real_source.py'
    if output.exists():
        raise FileExistsError('Adapter source is create-once')
    raw = (header+revised+'\n').encode()
    ast.parse(raw.decode())
    temporary = output.with_suffix('.py.part'); temporary.write_bytes(raw)
    if temporary.read_bytes() != raw:
        raise ValueError('Short adapter write')
    temporary.replace(output)
    record = dict(status='COPIED_INTEGRAL_REAL_NYQUIST_ADAPTER',
        source_sha256=se.sha(path), original_function_sha256=hashlib.sha256(original.encode()).hexdigest(),
        revised_sha256=se.sha(output), substitutions=expected,
        no_physical_prior_change=True, no_tolerance_relaxation=True, scientific_acceptance=False)
    se.write(se.ROOT/'REAL_PHASE_ADAPTER_PROVENANCE.json', record)
    print(json.dumps(record), flush=True)


if __name__ == '__main__':
    main()
