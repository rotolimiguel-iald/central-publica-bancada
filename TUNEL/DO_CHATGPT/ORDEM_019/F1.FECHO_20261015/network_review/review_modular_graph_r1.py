"""Root review and custody; includes root-authored helpers, no independent rebuild."""
from pathlib import Path
import datetime, hashlib, json, os, re

BASE = Path(__file__).resolve().parent
OUT = BASE.parent
NAMES = ['CanonicalFockPolarRightAlgebraR6', 'GeneralRepresentedDoubleCutR2', 'GenericRootCutSupremumR1', 'ModularTransportTargetR1', 'CanonicalFockModularGraphEqualityR1']
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
    target = BASE / 'MODULAR_GRAPH_ROOT_REVIEW_R1.json'
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
            'The actual coefficient Tomita graph equals the actual GNS closed Tomita graph. Gaussian regularizers preserve the latter, take values in the former, and converge strongly; graph equality is a conclusion.',
            'The GNS polar candidate is a concrete involutive antiunitary transported by the previously constructed coefficient unitary. Its polar decomposition is still a separate consumer.',
            'The concrete polar-right predicate forms a star algebra for an explicitly supplied J. No regular-unitary membership or traciality follows merely from this predicate.',
            'Double-cut balance and the root quadratic-form supremum compile with all their balance, commutation, injectivity, flip and convergence premises explicit.',
            'Generic graph, resolvent, imaginary-power and root transports retain their explicit intertwining premise; they are not independent physical identifications.'
        ], scope_limits=[
            'Named sources read in full by root. Several helpers are root-authored, so this is not an independent semantic audit of the whole batch.',
            'Dependency artifacts hash-checked. No independent recompilation and no semantic review of every transitive source.',
            'Actual modular identification, polar decomposition and the concrete scaled trace still require the subsequent consumers.',
            'Base program and seal rechecked as v393. V350/V351 are historical module names within that base. No production or gate change.'
        ], review_script=pin(__file__))
    new(target, result)
    print(json.dumps({'receipt': pin(target), 'modules':len(records),
                      'prints':len(printed), 'pins':len(checked)}, ensure_ascii=False))

if __name__ == '__main__': main()
