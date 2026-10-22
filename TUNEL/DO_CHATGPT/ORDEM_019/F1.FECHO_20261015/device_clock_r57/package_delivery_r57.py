"""Custody-only packaging of R57 completed artifacts; no mission mutation."""
import datetime as dt
import json
import re
from pathlib import Path

from derive_polarization_r57 import ROOT, REFERENCE, ACTOR, new, pin

target = ROOT / 'DELIVERY_R57.json'
if target.exists():
    raise FileExistsError(target)
symbolic = json.loads((ROOT / 'SYMBOLIC_RESULT_R57.json').read_text(encoding='utf-8'))
assert len(symbolic['checks']) == 34 and all(c['passed'] for c in symbolic['checks'])
results = sorted((ROOT / 'builds').glob('*/RESULT.json'))
assert len(results) == 2
records = [json.loads(p.read_text(encoding='utf-8')) for p in results]
assert records[0]['exit_code'] == 1 and records[1]['exit_code'] == 0
ok = records[1]
assert pin(ok['source']['path']) == ok['source']
assert pin(ok['olean']['path']) == ok['olean']
axioms = re.findall(r"depends on axioms:\s*\[([^\]]*)\]", ok['axioms'])
assert len(axioms) == 6
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
assert all({x.strip() for x in block.split(',')} <= allowed for block in axioms)
assert not ok['source_has_sorry'] and 'error:' not in ok['axioms']
files = [
    'SCOPE_R57.json', 'derive_polarization_r57.py', 'RUN_START_R57.json',
    'RUN_END_R57.json', 'SYMBOLIC_RESULT_R57.json', 'DERIVACAO_R57.md',
    'COMPLEMENTO_DOMINIO_RELOGIO_LOCAL_R57.md',
    'MiguelFixedBoundaryScalarReadingR57.lean', 'MiguelFixedBoundaryScalarReadingR57R2.lean',
    'build_fixed_boundary_r57.py', 'package_delivery_r57.py',
]
for attempt in results:
    for item in sorted(attempt.parent.iterdir()):
        if item.is_file():
            files.append(str(item.relative_to(ROOT)))
scope = json.loads((ROOT / 'SCOPE_R57.json').read_text(encoding='utf-8'))
for item in scope['source_pins']:
    assert pin(item['path']) == item
delivery = {
    'schema': 'iald-scientific-partial-delivery/v1',
    'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
    'actor': ACTOR,
    'mission_reference': str(REFERENCE),
    'unit': 'F1.FECHO_20261015', 'board_team_claim': 938, 'requirement': 'R4',
    'criterion_satisfied': False,
    'requirement_disposition': 'Leave R4 working; no submit or self acceptance of the integral requirement.',
    'statute': 'Candidate construction with exact symbolic and Lean checks; independent review required.',
    'symbolic': {'passed': 34, 'total': 34, 'domain': 'finite 2x2x2 model; all terms retained and rates positive',
                 'result': pin(ROOT / 'SYMBOLIC_RESULT_R57.json')},
    'lean': {'exit_code': 0, 'printed_axiom_checks': 6, 'allowed_axioms': sorted(allowed),
             'sorry': False, 'source': ok['source'], 'build': pin(results[1]), 'olean': ok['olean'],
             'scope': 'Multiplicative scalar encoding of a fixed beta boundary; reading/reconstruction/rereading and weights.'},
    'failed_attempt_preserved': {'source': records[0]['source'], 'receipt': pin(results[0]),
        'reason': 'Third Matrix.mul_smul rewrite redundant; R2 uses simp only, no theorem weakened.'},
    'derived_additions': [
        'Local inverse of analytic finite-model phase because phi prime at zero equals omegaOH > 0.',
        'Algebraic bosonic-core vacuum-ground pump witness, without asserting unbounded semigroup existence.',
        'Relative ideal demodulation removes the external carrier; hardware chain and bandwidth remain unbuilt.'
    ],
    'remaining_R4': [
        'Actual receiver observable and optical-to-complex-signal map in the same device.',
        'Physical laboratory/rotating-frame contract, preparation and envelope response; tanh not derived.',
        'Clock calibration and identification of V0/Eref/Killing-kappa, with domains and units.',
        'No full bosonic semigroup, global clock interval or physically implemented detector proved.'
    ],
    'source_pins': scope['source_pins'],
    'artifacts': [pin(ROOT / name) for name in files],
    'unchanged': ['originals', 'canonical memory', 'Nos kernel', 'Bancada', 'observed data', 'gate', 'R5'],
}
print(json.dumps(new('DELIVERY_R57.json', delivery), ensure_ascii=False))
