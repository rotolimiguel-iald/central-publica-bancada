"""Copy the existing sampler, changing only the validated phase reader.

The extra chunk metadata is checkpointed inside the same NPZ to survive a
terminal process failure. Numerical proposal and acceptance code are retained.
"""
import ast
import inspect
import source_evidence as se
import transport_phase_source as tp

target = se.ROOT/'run_real_phase_importance.py'
if target.exists():
    raise FileExistsError(target)
source = inspect.getsource(tp.run)
tree = ast.parse(source)
counts = dict(reader=0, chunk=0, metadata=0)


class ReaderAndCheckpoint(ast.NodeTransformer):
    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.attr == 'imap_unordered' and ast.unparse(node.args[0]) == 'pm.evaluate':
                node.args[0] = ast.Name(id='evaluate_real', ctx=ast.Load()); counts['reader'] += 1
            if node.func.value.id == 'chunk' and node.func.attr == 'append':
                if ast.unparse(node.args[0]) != '(index, value)':
                    raise ValueError('Unexpected checkpoint tuple')
                node.args[0].elts.append(ast.Name(id='meta', ctx=ast.Load())); counts['chunk'] += 1
            if node.func.value.id == 'se' and node.func.attr == 'save_arrays' and 'chunk_' in ast.unparse(node.args[0]):
                expression = ast.parse('np.asarray(json.dumps([dict(index=c[0], **c[2]) for c in chunk]))', mode='eval').body
                node.keywords.append(ast.keyword(arg='controls_json', value=expression)); counts['metadata'] += 1
        return node


tree = ReaderAndCheckpoint().visit(tree)
ast.fix_missing_locations(tree)
if counts != dict(reader=1, chunk=1, metadata=1):
    raise ValueError('Unexpected sampler edit counts')
prefix = '''"""Registered fresh source draws using validated real phase interpolation."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
import argparse
from datetime import datetime, timezone
import fcntl
import json
import multiprocessing as mp
import time
import numpy as np
import source_evidence as se
import phase_marginal_source as pm
import transport_phase_source as tp
from importance_source_evidence import importance_statistics
from phase_marginal_real_source import phase_marginal_loglikes

STAGE = se.ROOT/'phase_real_refined'
draw = tp.draw


def check():
    tp.STAGE = STAGE
    return tp.check()


def evaluate_real(job):
    index, u = job
    value, metadata = phase_marginal_loglikes(se._FAMILY, u, se._STATE)
    return index, value, metadata


'''
suffix = '''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--processes', type=int, default=4)
    args = parser.parse_args()
    reg = json.loads((STAGE/'REGISTRATION.json').read_bytes())
    args.draws, args.seed = reg['draws'], reg['seed']
    with open(STAGE/'RUN.lock', 'a+b') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        run(args)
'''
raw = (prefix+ast.unparse(tree)+'\n'+suffix).encode()
temporary = target.with_suffix('.py.part'); temporary.write_bytes(raw)
if temporary.read_bytes() != raw:
    raise ValueError('Incomplete new sampler')
temporary.replace(target)
se.write(se.ROOT/'REAL_IMPORTANCE_RUNNER_PROVENANCE.json', dict(
    original_source_sha256=se.sha(se.ROOT/'transport_phase_source.py'), generated_source_sha256=se.sha(target),
    edits=counts, physical_prior_changed=False, acceptance_changed=False,
    chunk_controls='Per-point maxima embedded as controls_json in each complete NPZ; previous output arrays and result schema unchanged'))
print('Original sampler copied with checked reader and atomic control metadata.', flush=True)
