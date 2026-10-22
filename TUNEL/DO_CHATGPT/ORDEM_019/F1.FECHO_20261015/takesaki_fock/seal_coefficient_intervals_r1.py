"""Seal fresh graph, density, completion and faithful GNS evidence, without building."""
from pathlib import Path
import datetime, hashlib, json, os, re

BASE = Path(__file__).resolve().parent
NAMES = ['RegularDualGNSActionR1', 'ClosedSubmoduleRestrictionR2', 'RegularSpectralBoostedAverageR2', 'RegularAverageAdjointR4', 'RegularFiniteFibreRightR3', 'RegularFibreAverageStarR3', 'RegularBoostedReflectionR1', 'RegularOrbitMultiplicationR2', 'RegularSpectralAdjunctionR1', 'RegularTranslatedReflectionR1', 'RegularTranslatedAverageR2', 'RegularScalarRealGraphR2', 'CanonicalFockCoefficientDenseR6', 'CanonicalFockCoefficientEmbeddingR1', 'RegularTranslatedSpectralAdjunctionR2']
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
    earlier_components=pin(BASE / 'FOCK_COEFFICIENT_FOUNDATIONS_RECEIPT_R1.json'),
    earlier_limited_review=pin(BASE.parent / 'network_review/GNS_MODULAR_FLOW_SEMANTIC_REVIEW_ROOT_R1.json'),
    conclusions=[
        'Every vector coefficient belongs to the actual scalar-weight GNS completion, by interval totality and the concrete cyclic wedge vacuum.',
        'The normalized Fourier coefficient embedding into that GNS is isometric; surjectivity is not asserted by this batch.',
        'Translated regular averages with arbitrary bounded base coefficients have both finite quadratic sides.',
        'Both normalized Fourier coefficients of these adjunction pairs are computed exactly, with interval endpoint changes only almost everywhere.',
        'The actual closed GNS Tomita graph is packaged as a closed real linear subspace; no complex linearity of Tomita is imposed.'
    ], scope_limits=[
        'The reverse range inclusion, coefficient-unitary conclusion, and full graph consumers are separate unless pinned explicitly below.',
        'No scaled trace or complete certificate is supplied; the historical total cyclic interface is not filled by an absolute-value extension.',
        'Actual direct Lean builds with readonly dependency caches; no whole kernel or main rerun in this batch.'
    ], builders=[pin(BASE/'build_takesaki_stream_r1.py'),pin(BASE/'build_takesaki_stream_r2.py')], sealer=pin(Path(__file__).resolve()),
    production_modified=False, gate_modified=False)
target = BASE / 'FOCK_COEFFICIENT_INTERVALS_RECEIPT_R1.json'
data = (json.dumps(result, ensure_ascii=False, indent=2)+'\n').encode('utf-8')
with target.open('xb') as stream:
    stream.write(data)
    stream.flush()
    os.fsync(stream.fileno())
assert target.read_bytes() == data
print(json.dumps(dict(receipt=pin(target), components=len(records),
    printed_declarations=result['printed_declarations'], dependencies=len(deps))))
