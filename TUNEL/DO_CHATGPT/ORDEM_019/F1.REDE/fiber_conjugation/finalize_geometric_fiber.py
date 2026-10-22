"""Additive receipt for the transverse-reflected, component-swapping conjugation."""
from pathlib import Path
import hashlib
import json
import os
import re

BASE = Path(__file__).resolve().parent

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def pin(p):
    return {'path': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p)}

attempt = sorted(p for p in (BASE / 'attempts').iterdir() if (p / 'GeometricFiberConjugation.lean').is_file())[-1]
receipt = json.loads((attempt / 'RECEIPT.json').read_bytes())
source = BASE / 'GeometricFiberConjugation.lean'
assert receipt['exit_code'] == 0
assert receipt['source_sha256'] == sha(source)
out = (attempt / 'AXIOMS.txt').read_text(encoding='utf-8')
assert 'sorryAx' not in out and 'error:' not in out
decls = [line.split('\t')[1:] for line in out.splitlines() if line.startswith('LOCAL_DECL\t')]
checks = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", out)
assert len(checks) == 5
ancestor = json.loads((BASE / 'DELIVERY_FIBER_R1.json').read_bytes())
assert sha(BASE / 'FiberConjugation.lean') == ancestor['source']['sha256']
assert sha(Path(ancestor['olean']['path'])) == ancestor['olean']['sha256']
delivery = {
    'unit': 'F1.REDE', 'scope': 'Geometric candidate antiunitary: transverse q negation, coordinate conjugation and two-component exchange',
    'status': 'CANDIDATE_KERNEL_CHECKED', 'exit_code': 0,
    'source': pin(source), 'build_receipt': pin(attempt / 'RECEIPT.json'), 'build': receipt,
    'olean': pin(attempt / 'GeometricFiberConjugation.olean'),
    'import': 'GeometricFiberConjugation',
    'add_to_LEAN_PATH': [str(attempt), str(Path(ancestor['olean']['path']).parent)],
    'ancestor_delivery': pin(BASE / 'DELIVERY_FIBER_R1.json'),
    'ancestor_source_unchanged': True,
    'axiom_checks': checks, 'all_local_declarations': decls,
    'apis': {
        'transverseGeometricJ': 'F1Rede.FiberConjugation.transverseGeometricJ : TransverseFiber ≃ₛₗᵢ[starRingEnd ℂ] TransverseFiber',
        'transverseGeometricJ_involutive': 'Function.Involutive transverseGeometricJ',
        'transverseGeometricJ_ae': 'almost everywhere q: transverseGeometricJ f q = fiberSwappedJ (f (-q))',
        'transverseGeometricJ_coordinates': 'almost everywhere q, every i: transverseGeometricJ f q i = star (f (-q) (helicitySwap i))',
        'fiberSwappedJ': 'fiberJ.trans fiberSwap',
        'fiberSwappedJ_involutive': 'Function.Involutive fiberSwappedJ',
        'helicitySwap': 'Equiv.swap (0 : Fin 2) 1',
    },
    'construction': 'Negation is Lebesgue-measure-preserving; component exchange is piLpCongrLeft; coordinate conjugation is the unchanged fiberJ. Semilinear compLp lift and reflection compose into a norm-preserving involution.',
    'scope_limits': ['A mathematical candidate, not an identification with physical PCT or full Lorentz covariance.', 'Rapidity-space formula and its Fourier transport are delegated to the modular-wedge construction.', 'No wedge locality or full net is claimed by this file alone.'],
    'production_changed': False, 'junction_created': False,
    'previous_attempt_receipts': [pin(p / 'RECEIPT.json') for p in sorted((BASE / 'attempts').iterdir()) if (p / 'GeometricFiberConjugation.lean').is_file()],
    'scripts': [pin(BASE / 'build_geometric_fiber.py'), pin(Path(__file__))],
}
p = BASE / 'DELIVERY_GEOMETRIC_FIBER_R1.json'
b = (json.dumps(delivery, ensure_ascii=False, indent=2) + '\n').encode()
with p.open('xb') as f:
    f.write(b)
    f.flush()
    os.fsync(f.fileno())
assert p.read_bytes() == b
print(json.dumps({'delivery': pin(p), 'source': pin(source), 'olean': pin(attempt / 'GeometricFiberConjugation.olean'), 'declarations': len(decls)}, ensure_ascii=False))
