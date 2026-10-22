"""Custody of proved generic regularization, finite-approximation and polar-flip helpers; no build."""
from pathlib import Path
import datetime, hashlib, json, os, re

BASE = Path(__file__).resolve().parent
NAMES = ['UnitaryAntiunitaryTransportR2','GeneralCutoffAverageCommutationR1','GeneralInverseStrongFatouR1','ClosedTomitaPolarFlipR2','GeneralInverseFiniteApproximationR1']
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

def pin(path):
    data = path.read_bytes()
    return dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))

def parse(text):
    out = {}
    for name, axioms in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", text, re.S):
        out[name] = [v.strip() for v in axioms.split(',') if v.strip()]
    for line in text.splitlines():
        if line.startswith('LOCAL_DECL\t'):
            _, name, axioms = line.split('\t', 2)
            values = [v.strip() for v in axioms.split(',') if v.strip()]
            assert name not in out or out[name] == values
            out[name] = values
    assert out and all(set(v) <= ALLOWED for v in out.values())
    return out

records = []
deps = {}
failed = []
for name in NAMES:
    src = BASE / (name + '.lean')
    source_pin = pin(src)
    assert not re.search(r'\b(?:sorry|admit)\b', src.read_text(encoding='utf-8'))
    matches = []
    for rp in sorted((BASE / 'attempts').glob('*/RECEIPT.json')):
        receipt = json.loads(rp.read_bytes())
        if Path(receipt['source']['path']).stem != name:
            continue
        if receipt['exit_code']:
            failed.append(pin(rp))
        elif receipt['source']['sha256'] == source_pin['sha256']:
            matches.append((rp, receipt))
    assert matches, name
    rp, receipt = matches[-1]
    assert type(receipt['exit_code']) is int and receipt['exit_code']==0
    assert receipt['readonly_dependencies_unchanged'] is True
    assert pin(Path(receipt['source']['path'])) == receipt['source']
    for dep in receipt['dependencies']:
        if dep['path'] not in deps:
            assert pin(Path(dep['path'])) == dep
            deps[dep['path']] = dep
        else:
            assert deps[dep['path']] == dep
    axioms = parse((rp.parent / 'AXIOMS.txt').read_text(encoding='utf-8'))
    records.append(dict(source=source_pin, receipt=pin(rp), build=pin(rp.parent / 'BUILD.log'),
        axioms=pin(rp.parent / 'AXIOMS.txt'), olean=pin(rp.parent / (name + '.olean')),
        exit_code=receipt['exit_code'], seconds=receipt['seconds'],
        start_utc=receipt['start_utc'], end_utc=receipt['end_utc'], printed_axioms=axioms))

result = dict(unit='F1.FECHO_20261015', claim=845,
    actor='codex-gerente-tgl/tempo_math_review',
    created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    status='REAL_COMPILED_SANDBOX_INDEPENDENT_REVIEW_PENDING', records=records,
    checked_dependency_count=len(deps), checked_dependencies=list(deps.values()),
    printed_declarations=sum(len(r['printed_axioms']) for r in records),
    axioms_only_trio=True, source_has_no_sorry=True, failed_same_name_attempts=failed,
    assembly=pin(BASE/'FINITE_APPROXIMATION_ASSEMBLY_R1.json'),
    conclusions=[
        'Unitary transport of an antiunitary and its involution; actual proofs, not an assumed polar decomposition.',
        'The same regular inverse-cutoff square root commutes with regular translations and their averages.',
        'Strong Fatou for square values of the inverse supremum needs no convergence of adjoints.',
        'For a closed dense antilinear involution, the adjoint is involutive and S flips the resolvent; a proved J-root factorization with dense range yields J R J inverse = I-R.',
        'Regular averages decrease square values; traciality on the existing finite star core extends to the full represented core.',
        'Given the explicit domain-cut estimate, a contractive finite-square approximate identity is constructed; with square traciality it gives finite positive minorants.'
    ], scope_limits=[
        'The actual Fock polar factor, regular polar-right membership, domain-cut estimate and square traciality are separate consumers; no final trace is assumed proved by these helpers.',
        'No total cyclic ENNReal extension on all complex operators is asserted.',
        'Counts refer to explicit printed declarations; no independent rebuild or full local-declaration audit is claimed by this custody step.'
    ], builders=[pin(BASE/'build_takesaki_stream_r4.py')], sealer=pin(Path(__file__).resolve()),
    production_modified=False, gate_modified=False)
target = BASE / 'GENERAL_FINITE_APPROXIMATION_POLAR_RECEIPT_R1.json'
data = (json.dumps(result, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
with target.open('xb') as stream:
    stream.write(data)
    stream.flush()
    os.fsync(stream.fileno())
assert target.read_bytes() == data
print(json.dumps(dict(receipt=pin(target), components=len(records),
    printed_declarations=result['printed_declarations'], dependencies=len(deps))))
