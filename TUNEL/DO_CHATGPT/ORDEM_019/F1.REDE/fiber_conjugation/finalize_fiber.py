"""Pin the successful fiber conjugation candidate without altering previous artifacts."""
from pathlib import Path
import hashlib
import json
import os
import re

BASE = Path(__file__).resolve().parent
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def pin(p):
    return {'path': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p)}

attempt = sorted((BASE / 'attempts').iterdir())[-1]
receipt = json.loads((attempt / 'RECEIPT.json').read_bytes())
source = BASE / 'FiberConjugation.lean'
assert receipt['exit_code'] == 0
assert receipt['source_sha256'] == sha(source)
out = (attempt / 'AXIOMS.txt').read_text(encoding='utf-8')
assert 'sorryAx' not in out and 'error:' not in out
decls = [line.split('\t')[1:] for line in out.splitlines() if line.startswith('LOCAL_DECL\t')]
checks = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", out)
assert len(checks) == 5
dependencies = [
    KERNEL / 'TGLExt/LightNetStandardWedgeDataBGL.lean',
    KERNEL / 'TGLExt/TheImportedSecondQuantization.lean',
    KERNEL / '.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean',
    KERNEL / '.lake/packages/mathlib/Mathlib/Analysis/Normed/Lp/PiLp.lean',
    KERNEL / 'lake-manifest.json', KERNEL / 'lean-toolchain',
]
delivery = {
    'unit': 'F1.REDE', 'scope': 'Coordinate fiber conjugation and its pointwise transverse L2 lift',
    'status': 'CANDIDATE_KERNEL_CHECKED', 'exit_code': 0,
    'source': pin(source), 'build_receipt': pin(attempt / 'RECEIPT.json'),
    'build': receipt, 'olean': pin(attempt / 'FiberConjugation.olean'),
    'import': 'FiberConjugation', 'add_to_LEAN_PATH': str(attempt),
    'axiom_checks': checks, 'all_local_declarations': decls,
    'dependencies': [pin(p) for p in dependencies],
    'apis': {
        'fiberJ': 'F1Rede.FiberConjugation.fiberJ : Fib ≃ₛₗᵢ[starRingEnd ℂ] Fib',
        'fiberJ_involutive': 'Function.Involutive fiberJ',
        'fiberJ_apply': 'fiberJ v i = star (v i)',
        'transverseJ': 'F1Rede.FiberConjugation.transverseJ : TransverseFiber ≃ₛₗᵢ[starRingEnd ℂ] TransverseFiber',
        'transverseJ_involutive': 'Function.Involutive transverseJ',
        'transverseJ_ae': 'almost everywhere q: transverseJ f q = fiberJ (f q)',
        'transverseJ_coordinates': 'almost everywhere q, every i: transverseJ f q i = star (f q i)',
    },
    'construction': 'WithLp.toLp coordinate conjugation; norm by PiLp.norm_eq_of_L2; ContinuousLinearMap.compLpₗ pointwise lift; norm equality by eLpNorm_congr_norm_ae; involution by Lp.ext.',
    'scope_limits': ['Does not identify this conjugation with physical PCT or Lorentz transformations.', 'Spectral reflection, transport to H1, Tomita, standard wedge and network are separate constructions.'],
    'production_changed': False, 'junction_created': False,
    'previous_attempt_receipts': [pin(p / 'RECEIPT.json') for p in sorted((BASE / 'attempts').iterdir())],
    'scripts': [pin(BASE / 'build_fiber.py'), pin(Path(__file__))],
}
p = BASE / 'DELIVERY_FIBER_R1.json'
b = (json.dumps(delivery, ensure_ascii=False, indent=2) + '\n').encode()
with p.open('xb') as f:
    f.write(b)
    f.flush()
    os.fsync(f.fileno())
assert p.read_bytes() == b
print(json.dumps({'delivery': pin(p), 'source': pin(source), 'olean': pin(attempt / 'FiberConjugation.olean'), 'declarations': len(decls)}, ensure_ascii=False))
