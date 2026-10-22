"""Read-only artifact audit for R6; report is new and immutable."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
ATTEMPT = BASE / 'orbital_rotation/attempts/20261016T124312_530135Z'
DELIVERY = BASE / 'orbital_rotation/PHYSICAL_FOCK_NET_DELIVERY_R2.json'
SOURCE = BASE / 'orbital_rotation/PhysicalFockNetRealizationR2.lean'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def pin(path):
    path = Path(path)
    return {'path': str(path), 'sha256': sha(path), 'bytes': path.stat().st_size}

def save_new(path, value):
    assert not path.exists(), path
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    tmp = path.with_suffix(path.suffix + '.tmp')
    with tmp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == raw
    os.rename(tmp, path)
    assert path.read_bytes() == raw

delivery = json.loads(DELIVERY.read_bytes())
receipt = json.loads((ATTEMPT / 'RECEIPT.json').read_bytes())
cache = json.loads((ATTEMPT / 'DEPENDENCY_CACHE.json').read_bytes())
expected = {}

def collect(value):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
            path = str(Path(value['path']))
            assert path not in expected or expected[path] == value['sha256'], ('conflicting_pin', path)
            expected[path] = value['sha256']
        for child in value.values():
            collect(child)
    elif isinstance(value, list):
        for child in value:
            collect(child)

for document in (delivery, receipt, cache):
    collect(document)
checked = []
for path, digest in sorted(expected.items()):
    actual = sha(path)
    assert actual == digest, ('mismatch', path, actual, digest)
    checked.append({'path': path, 'sha256': actual})

assert sha(SOURCE) == sha(ATTEMPT / SOURCE.name)
assert receipt['exit_code'] == 0
assert receipt['readonly_dependencies_unchanged'] is True
assert receipt['dependency_cache_unchanged'] is True
assert receipt['production_modified'] is False
assert (ATTEMPT / 'RUNNING_OUTPUT.log').read_bytes() == (ATTEMPT / 'AXIOMS.txt').read_bytes()
log = (ATTEMPT / 'AXIOMS.txt').read_text(encoding='utf-8')
axioms = dict(re.findall(r'^LOCAL_DECL\t([^\t]+)\t([^\r\n]*)$', log, re.M))
assert len(axioms) == 16
assert all(set(a.split(',')) <= {'propext', 'Classical.choice', 'Quot.sound'} for a in axioms.values())
assert 'sorryAx' not in log
assert not re.search(r'\berror:|AXIOM_AUDIT_REFUSED|LOCAL_AXIOM_REFUSED', log)
assert delivery['build']['axioms'] == axioms
assert (ATTEMPT / 'BUILD.log').read_bytes().endswith((ATTEMPT / 'AXIOMS.txt').read_bytes())

module_checks = []
for copy in cache['copies']:
    original, cached = Path(copy['original']['path']), Path(copy['copy']['path'])
    assert sha(original) == sha(cached)
    dependency_receipt = json.loads(Path(copy['receipt']['path']).read_bytes())
    assert dependency_receipt['exit_code'] == 0
    artifact_hashes = {}
    def gather_receipt_pins(value):
        if isinstance(value, dict):
            if 'path' in value and 'sha256' in value:
                key = str(Path(value['path']))
                assert key not in artifact_hashes or artifact_hashes[key] == value['sha256']
                artifact_hashes[key] = value['sha256']
            for child in value.values():
                gather_receipt_pins(child)
        elif isinstance(value, list):
            for child in value:
                gather_receipt_pins(child)
    gather_receipt_pins(dependency_receipt)
    assert artifact_hashes[str(original)] == sha(original)
    snapshot = original.with_suffix('.lean')
    assert artifact_hashes[str(snapshot)] == sha(snapshot)
    # Older receipts pin the snapshot only in artifacts; check the named source too when present.
    if 'source' in dependency_receipt:
        assert dependency_receipt['source']['sha256'] == sha(snapshot)
    module_checks.append({'module': copy['module'], 'original': str(original), 'source': str(snapshot),
                          'source_sha256': sha(snapshot), 'compiled_sha256': sha(original)})

semantic_names = {
    'PhysicalCanonicalNetCompleteR1.lean', 'PhysicalCompactNetCovarianceR1.lean',
    'PhysicalCanonicalWedgeEqualityR3.lean', 'PhysicalSmearTranslationR2.lean',
    'PhysicalSchwartzMaxwellR1.lean', 'BosonicFock.lean', 'CanonicalWedge.lean',
    'FieldWeylR3.lean', 'WeylNetWiringR1.lean', 'WedgeCyclicR3.lean',
    'WedgeNonabelianR4.lean', 'BosonicGammaJR5.lean', 'CanonicalFockAntiAssemblyR4.lean',
    'WedgePairTomitaR2.lean', 'CanonicalFockPolarR1.lean', 'CanonicalFockGraphRealizationR3.lean',
    'CanonicalFockModularFlowR2.lean', 'CanonicalWedgeKMSR4.lean', 'CanonicalFockBWR2.lean',
    'CanonicalModularCoreAssemblyR1.lean', 'CanonicalWedgeFlowR2.lean',
}
semantic_sources = [pin(x['path']) for x in receipt['dependencies'] if Path(x['path']).name in semantic_names]
assert len(semantic_sources) == len(semantic_names)
kernel = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
canonical_sources = [pin(kernel / rel) for rel in [
    'TGLExt/TheImportedSecondQuantization.lean',
    'TGLExt/O16/ContentContractProposal.lean',
    'TGLExt/O16/RecognitionModular_v2.lean',
]]
result = {
    'reviewer': 'codex-fock-r6-review', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'statute': 'REAL', 'unit': 'F1.FECHO_20261015', 'requirement': 'R6', 'pass': True,
    'delivery': pin(DELIVERY), 'source': pin(SOURCE), 'build_receipt': pin(ATTEMPT / 'RECEIPT.json'),
    'hash_checked_unique_paths': len(checked), 'hash_failures': 0, 'checked_files': checked,
    'dependency_modules': len(module_checks), 'dependency_checks': module_checks,
    'axiom_declarations': len(axioms), 'axioms': axioms,
    'seconds_recorded_by_builder': receipt['seconds'], 'lean_toolchain': receipt['toolchain'],
    'independent_rebuild': False,
    'rebuild_reason': 'Source/receipt/copy integrity and semantic consumers checked; no remaining concrete compile risk requiring a rebuild.',
    'semantic_sources': semantic_sources, 'canonical_definition_sources': canonical_sources,
    'script': pin(__file__),
    'scope': 'Integrity audit of supplied build and selective semantic review. Not a new full kernel compilation or independent audit of every transitive theorem.',
}
save_new(OUT / 'R6_ARTIFACT_VERIFICATION_R1.json', result)
print(json.dumps({k: result[k] for k in ['pass', 'hash_checked_unique_paths', 'hash_failures', 'dependency_modules', 'axiom_declarations', 'independent_rebuild']}))
