"""Custody of generic positive comparison, directed regulator additivity and order normality; no build."""
from pathlib import Path
import datetime, hashlib, json, os, re

BASE = Path(__file__).resolve().parent
NAMES = ['GeneralInverseAdditivityR3']
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

for rp in sorted((BASE/'attempts').glob('*/RECEIPT.json')):
    r=json.loads(rp.read_bytes())
    if Path(r['source']['path']).stem in {'GeneralInverseAdditivityR1','GeneralInverseAdditivityR2'}:
        assert type(r['exit_code']) is int and r['exit_code'] != 0
        failed.append(pin(rp))

result = dict(unit='F1.FECHO_20261015', claim=845,
    actor='codex-gerente-tgl/tempo_math_review',
    created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    status='REAL_COMPILED_SANDBOX_INDEPENDENT_REVIEW_PENDING', records=records,
    checked_dependency_count=len(deps), checked_dependencies=list(deps.values()),
    printed_declarations=sum(len(r['printed_axioms']) for r in records),
    axioms_only_trio=True, source_has_no_sorry=True, failed_same_name_attempts=failed,
    prepared_sources=[pin(BASE/'GeneralInverseOrderNormalR1.lean'),pin(BASE/'GeneralInverseAdditivityR1.lean'),pin(BASE/'GeneralInverseAdditivityR2.lean')],
    conclusions=[
        'Comparison of right perturbations extends from the existing uniform finite-square ideal to every square by actual regular averages and boost-invariance of the vector.',
        'The existing Hilbert positive square root in the same core then extends the comparison to every positive operator.',
        'Additivity of the regulator supremum uses explicit antitonicity and the common positive regulator min(e,d). It is not inferred from an arbitrary supremum.',
        'The sequence of inverse regulators 1/(n+1) is monotone under that antitonicity premise.',
        'Order normality for ambient and internal positive suprema is derived by the existing monotone operator-limit theorem and von Neumann internal-supremum inclusion.'
    ], scope_limits=[
        'The actual Fock finite-ideal comparison and regulator antitonicity require the concrete polar-right consumer; no trace axiom is introduced here.',
        'No square traciality, actual semifiniteness, or total cyclic ENNReal extension to all complex operators is asserted by this batch.',
        'Six explicit printed declarations are checked; no independent rebuild or environment-wide local audit is claimed.'
    ], builders=[pin(BASE/'build_takesaki_stream_r4.py')], sealer=pin(Path(__file__).resolve()),
    production_modified=False, gate_modified=False)
target = BASE / 'GENERAL_INVERSE_ADDITIVITY_RECEIPT_R1.json'
data = (json.dumps(result, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
with target.open('xb') as stream:
    stream.write(data)
    stream.flush()
    os.fsync(stream.fileno())
assert target.read_bytes() == data
print(json.dumps(dict(receipt=pin(target), components=len(records),
    printed_declarations=result['printed_declarations'], dependencies=len(deps))))
