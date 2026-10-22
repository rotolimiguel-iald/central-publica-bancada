"""Apply the validated real Fourier reader to the existing strength integral."""
import ast
import inspect
import source_evidence as se
import continuous_phase_source as old

target=se.ROOT/'real_continuous_phase_source.py'
if target.exists():
    raise FileExistsError(target)
tree=ast.parse(inspect.getsource(old.marginal_loglikes))
count=0


class RealReader(ast.NodeTransformer):
    def visit_Attribute(self,node):
        global count
        self.generic_visit(node)
        if isinstance(node.value,ast.Name) and node.value.id=='pc' and node.attr=='bank_loglikes':
            node.value.id='real'; count+=1
        return node


tree=RealReader().visit(tree); ast.fix_missing_locations(tree)
if count!=1:
    raise ValueError('Unexpected number of continuous phase readers')
prefix='''"""Existing continuous-strength integral with the validated real phase reader.

This API selects no strength prior or physical interpretation. Negative strength
is a numerical estimator control only. No new physical dynamics are introduced.
"""
import numpy as np
from scipy.special import logsumexp
from continuous_phase_source import raw_phase_samples, make_bank
import real_fourier_phase as real


'''
raw=(prefix+ast.unparse(tree)+'\n').encode()
temporary=target.with_suffix('.py.part');temporary.write_bytes(raw)
if temporary.read_bytes()!=raw:
    raise ValueError('Incomplete continuous API copy')
temporary.replace(target)
se.write(se.ROOT/'REAL_CONTINUOUS_API_PROVENANCE.json',dict(
    original_source_sha256=se.sha(se.ROOT/'continuous_phase_source.py'),
    output_sha256=se.sha(target),reader_replacements=count,
    waveform_or_prior_changed=False,tolerances_changed=False,
    method='Reuse original raw waveforms and continuous damping; change only the real Nyquist reader in phase integration'))
print('Continuous API copied with one validated reader replacement.',flush=True)
