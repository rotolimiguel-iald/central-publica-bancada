"""Seal fresh graph, density, completion and faithful GNS evidence, without building."""
from pathlib import Path
import datetime, hashlib, json, os, re

BASE = Path(__file__).resolve().parent
NAMES = [
    'CanonicalFockGNSRepresentationR6', 'CanonicalFockWeightGraphR3',
    'CanonicalFockWeightCompletionR5', 'RegularScalarGNSStrongContinuityR1',
    'RegularScalarStarDensityR1', 'CanonicalFockWeightStarDensityR2',
    'RegularScalarClosedTomitaR1', 'CanonicalFockWeightClosedTomitaR2',
]
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
    assert receipt['readonly_dependencies_unchanged']
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
    earlier_components=pin(BASE / 'FOCK_SCALAR_GNS_GRAPH_RECEIPT_R1.json'),
    earlier_limited_review=pin(BASE.parent / 'network_review/SCALAR_GNS_GRAPH_SEMANTIC_REVIEW_ROOT_R1.json'),
    conclusions=[
        'The actual regular Fock core acts faithfully on its scalar dual-weight GNS completion.',
        'All finite-weight-square orbit vectors belong to this GNS completion; it equals the completion of the original uniform finite ideal.',
        'The star-core initial graph is closable and has a concrete nonzero input, witnessed using the actual finite regular average.',
        'The star-core image is dense, using uniform boundedness and actual strongly convergent averages, not a density input field.',
        'The closure of Lambda(A) -> Lambda(A*) is a closed densely defined antilinear involution that extends that initial graph.'
    ], scope_limits=[
        'The scalar dual weight is not the scaled trace; invariance of that weight is not exp(-s) scaling.',
        'No equality of its modular flow with regular conjugation or geometric boost is claimed in this batch.',
        'The earlier root review covered six critical sources and their pins; it is not an independent review of these eight new sources.',
        'Build receipts record actual direct Lean compilation with readonly dependency caches, not a new full Lake build.'
    ], builder=pin(BASE/'build_takesaki_fock.py'), sealer=pin(Path(__file__).resolve()),
    production_modified=False, gate_modified=False)
target = BASE / 'FOCK_GNS_CLOSED_TOMITA_RECEIPT_R1.json'
data = (json.dumps(result, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
with target.open('xb') as stream:
    stream.write(data)
    stream.flush()
    os.fsync(stream.fileno())
assert target.read_bytes() == data
print(json.dumps(dict(receipt=pin(target), components=len(records),
    printed_declarations=result['printed_declarations'], dependencies=len(deps))))
