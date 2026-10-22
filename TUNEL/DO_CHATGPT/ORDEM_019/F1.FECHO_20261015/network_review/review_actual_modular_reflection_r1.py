"""Root review and custody; includes root-authored helpers, no independent rebuild."""
from pathlib import Path
import datetime, hashlib, json, os, re

BASE = Path(__file__).resolve().parent
OUT = BASE.parent
NAMES = ['CanonicalFockModularIdentificationR17', 'PhysicalSmearReflectionR6', 'ComplexHalfConjugationR1', 'GenericCutRecognitionR1', 'CompactPairCoverR1']
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def new(p, value):
    b = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf8')
    with p.open('xb') as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    assert p.read_bytes() == b

def main():
    target = BASE / 'ACTUAL_MODULAR_REFLECTION_REVIEW_R1.json'
    assert not target.exists()
    checked = {}
    def walk(v):
        if isinstance(v, dict):
            if 'path' in v and 'sha256' in v:
                actual = pin(v['path'])
                assert actual['sha256'] == v['sha256'], v['path']
                if 'bytes' in v:
                    assert actual['bytes'] == v['bytes']
                checked[actual['path']] = actual
            for child in v.values(): walk(child)
        elif isinstance(v, list):
            for child in v: walk(child)
    records = []
    printed = {}
    for name in NAMES:
        candidates = list(OUT.glob('*/' + name + '.lean'))
        assert len(candidates) == 1, candidates
        source = candidates[0]
        source_pin = pin(source)
        builds = []
        for snapshot in OUT.glob('*/attempts/*/' + name + '.lean'):
            rp = snapshot.parent / 'RECEIPT.json'
            if not rp.exists() or pin(snapshot)['sha256'] != source_pin['sha256']:
                continue
            rr = json.loads(rp.read_bytes())
            if type(rr.get('exit_code')) is int and rr['exit_code'] == 0:
                builds.append((rp, rr))
        assert builds, name
        rp, rr = sorted(builds)[-1]
        assert rr['readonly_dependencies_unchanged']
        walk(rr)
        text = source.read_text(encoding='utf8')
        assert not re.search(r'\b(sorry|admit)\b', text)
        log = (rp.parent / 'AXIOMS.txt').read_text(encoding='utf8')
        assert 'sorryAx' not in log and 'error:' not in log
        names = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", log, re.S)
        names += [(n, '') for n in re.findall(r"'([^']+)' does not depend on any axioms", log)]
        assert len(names) == len(re.findall(r'^#print axioms ', text, re.M)), name
        for declaration, ax in names:
            axioms = [a.strip() for a in ax.split(',') if a.strip()]
            assert set(axioms) <= ALLOWED
            printed[declaration] = axioms
        records.append({'source': source_pin, 'receipt': pin(rp),
                        'build': pin(rp.parent/'BUILD.log'),
                        'axioms': pin(rp.parent/'AXIOMS.txt'),
                        'olean': pin(rp.parent/(name+'.olean')),
                        'exit_code': rr['exit_code'], 'seconds': rr['seconds'],
                        'start_utc': rr['start_utc'], 'end_utc': rr['end_utc']})
    walk(records)
    provenance = json.loads((OUT/'PROVENIENCIA_V393_REUSO_V351_R1.json').read_bytes())
    assert pin(provenance['program_path'])['sha256'] == provenance['program_sha256']
    assert pin(provenance['seal_path'])['sha256'] == provenance['seal_sha256']
    result = dict(unit='F1.FECHO_20261015', claim=881, reviewer='/root',
        created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        verdict='PASS_WITH_STATED_SCOPE',
        mode='root_source_review_and_custody_including_root_authored_helpers_no_independent_rebuild',
        records=records, module_count=len(records), printed_count=len(printed),
        printed_axioms=printed, checked_files=list(checked.values()),
        checked_file_count=len(checked), material_findings=[],
        conclusions=[
            'The independently constructed dual-weight Tomita resolvent and imaginary powers are intertwined by the actual coefficient unitary. The modular group equals regular conjugation on the same Fock GNS; no modular-flow equality or trace is an input.',
            'Real physical Maxwell test inversion is exactly Theta on the circular one-particle realization, and the actual localized real subspaces transform under spacetime inversion.',
            'Conjugation fixes the scalar one-half. The abstract cut-recognition equivalence uses no axioms; actual cut recovery remains its explicit premise.',
            'Two compact sets with pointwise local rectangular relations admit finite nested covers preserving a relation hereditary in its first region. No single pair of wedges for whole arbitrary sets is assumed.'
        ], scope_limits=[
            'Named sources read in full by root. Some sources and revisions are root-authored; this is not independent audit.',
            'Dependency artifacts hash-checked; no independent rebuild or semantic review of every transitive source.',
            'The polar factorization, scaled trace, opposite-wedge duality and locality for arbitrary regions are not certified by this receipt. Theta is full inversion, not the wedge modular J by itself.',
            'Program and seal verified as v393. Historical V351-named sources remain incorporated; new candidates stay in sandbox.'
        ], review_script=pin(__file__))
    new(target, result)
    print(json.dumps({'receipt': pin(target), 'modules':len(records),
                      'prints':len(printed), 'pins':len(checked)}, ensure_ascii=False))

if __name__ == '__main__': main()
