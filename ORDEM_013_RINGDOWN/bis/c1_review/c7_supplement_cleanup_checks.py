"""Read-only package checks and in-memory wrapper lifecycle probes; no science runs."""
from pathlib import Path, PurePosixPath
from types import SimpleNamespace
from datetime import datetime, timezone
import ast
import hashlib
import json
import zipfile

B = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name('c7_supplement_cleanup_results.json')

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_bytes())

def check_manifest(root):
    manifest = read(root / 'MANIFEST.json')
    names = set()
    for row in manifest['shipped_files']:
        name = row['path']
        require(name not in names, 'Duplicate shipped path')
        names.add(name)
        p = (root / name).resolve()
        require(p.is_relative_to(root.resolve()), 'Shipped path escaped')
        require(p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], 'Shipped bytes differ: ' + name)
    return manifest, names

def check_zip(path, root, names, historical=False):
    with zipfile.ZipFile(path) as z:
        wanted = {root.name + '/' + n for n in names | {'MANIFEST.json'}}
        extras = set(z.namelist()) - wanted
        require(len(z.namelist()) == len(set(z.namelist())) and wanted <= set(z.namelist()), 'ZIP missing/duplicate member')
        require(not extras or (historical and all(n.startswith(root.name + '/replay_receipts/') for n in extras)), 'Unexpected ZIP extras')
        for n in names | {'MANIFEST.json'}:
            require(z.read(root.name + '/' + n) == (root / n).read_bytes(), 'ZIP bytes differ: ' + n)
        return {n: hashlib.sha256(z.read(n)).hexdigest() for n in sorted(extras)}

def lifecycle_probes(source, label):
    main = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    start = next(i for i, n in enumerate(main.body) if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == 'workroot' for t in n.targets))
    stop = next(i for i in range(start, len(main.body)) if isinstance(main.body[i], ast.Try))
    # Retain the original try/finally while replacing ONLY the science body by pass.
    guard_try = main.body[stop]
    safe_try = ast.Try(body=[ast.Pass()], handlers=[], orelse=[], finalbody=guard_try.finalbody)
    module = ast.fix_missing_locations(ast.Module(body=main.body[start:stop] + [safe_try], type_ignores=[]))
    code = compile(module, label + ':lifecycle-only', 'exec', optimize=1)
    outcomes = []
    for case in ['internal_work', 'internal_output', 'preserved_mkdir_fails', 'normal', 'report_write_fails']:
        events = []
        active = set()
        class FakePath:
            def __init__(self, value):
                self.value = value.value if isinstance(value, FakePath) else PurePosixPath(str(value))
            def __str__(self): return str(self.value)
            def __truediv__(self, other): return FakePath(self.value / str(other))
            def __eq__(self, other): return isinstance(other, FakePath) and self.value == other.value
            def resolve(self): return self
            def is_relative_to(self, other): return self.value.is_relative_to(other.value)
            @property
            def name(self): return self.value.name
            def mkdir(self, **kwargs):
                events.append(['mkdir', str(self)])
                if case == 'preserved_mkdir_fails' and self.name.startswith('package_stage_'):
                    raise PermissionError('Injected output failure')
            def glob(self, pattern): return []
            def exists(self): return str(self) in active
        def mkdtemp(**kwargs):
            p = kwargs['dir'] / 'replay_stage_fake'
            active.add(str(p))
            events.append(['mkdtemp', str(p)])
            return str(p)
        def rmtree(p):
            events.append(['rmtree', str(p)])
            require(str(p) == '/work/replay_stage_fake', 'Mock unexpected removal target')
            active.remove(str(p))
        def atomic(p, value):
            events.append(['atomic', str(p)])
            if case == 'report_write_fails' and p.name == 'CLEANUP_INTENT.json':
                raise PermissionError('Injected report write failure')
        namespace = dict(ROOT=FakePath('/package'), Path=FakePath, stamp='fixed',
                         args=SimpleNamespace(stage='stage',
                            work_root=FakePath('/package/new_work' if case == 'internal_work' else '/work'),
                            output_root=FakePath('/package/new_output' if case == 'internal_output' else '/output')),
                         tempfile=SimpleNamespace(mkdtemp=mkdtemp), shutil=SimpleNamespace(rmtree=rmtree),
                         sha=lambda p: 'mock-only-not-an-artifact-hash', atomic=atomic,
                         datetime=datetime, timezone=timezone)
        error = None
        try:
            exec(code, namespace)
        except Exception as e:
            error = type(e).__name__ + ': ' + str(e)
        outcomes.append(dict(case=case, error=error, events=events, remaining_mock_temporaries=sorted(active)))
        if case.startswith('internal_'):
            require(error and error.startswith('ValueError:'), 'Internal root not refused')
            require(any(e[0] == 'mkdir' and e[1].startswith('/package/') for e in events), 'Write-before-validation not reproduced')
        elif case == 'preserved_mkdir_fails':
            require(error and error.startswith('PermissionError:') and len(active) == 1, 'Pretry leak not reproduced')
        else:
            require(not active and any(e[0] == 'rmtree' for e in events), 'Entered-finally cleanup failed')
            require((error is None) == (case == 'normal'), 'Unexpected mock result')
    return dict(first_setup_line=main.body[start].lineno, try_line=guard_try.lineno,
                final_cleanup_line=guard_try.finalbody[0].lineno, cases=outcomes)

build = read(B / 'bis/C7_SUPPLEMENTS_V3_BUILD.json')
controls_path = B / 'bis/C7_SUPPLEMENTS_V3_CLEANUP_CONTROLS.json'
controls = read(controls_path)
require(sha(B / 'refeito/build_supplements_v3_013bis.py') == build['builder_sha256'], 'Builder changed')
rows = []
for receipt in build['packages']:
    name = receipt['package']
    root = B / name
    old = B / name.removesuffix('_v3')
    manifest, names = check_manifest(root)
    old_manifest, old_names = check_manifest(old)
    require(sha(root / 'MANIFEST.json') == receipt['manifest_sha256'], 'Manifest receipt mismatch')
    require(sha(B / receipt['archive']) == receipt['archive_sha256'], 'Archive receipt mismatch')
    require(manifest['supersedes_manifest_sha256'] == sha(old / 'MANIFEST.json'), 'Superseded manifest mismatch')
    check_zip(B / receipt['archive'], root, names)
    old_zip = B / 'cache' / (old.name + '_v1.zip')
    require(old_zip.is_file(), 'Old ZIP missing')
    old_extras = check_zip(old_zip, old, old_names, historical=True)
    preserved = old_names - {'README.md', 'reproduce.py'}
    for n in preserved:
        require((old / n).read_bytes() == (root / n).read_bytes(), 'Changed scientific/reference asset: ' + n)
    require((old / 'README.md').read_bytes() == (root / 'historical_README_v1.md').read_bytes(), 'Historical README changed')
    negative = next(r for r in controls['rows'] if r['package'] == name)
    log = B / 'bis/supplement_cleanup_v3' / (name + '.log')
    require(sha(log) == negative['log_sha256'], 'Negative log hash mismatch')
    require('FileNotFoundError: Provide --source-root' in log.read_text(encoding='utf-8'), 'Wrong failure')
    candidates = list((B / 'bis/supplement_cleanup_v3').glob(name + '_*/TEMPORARY_REMOVED.json'))
    require(len(candidates) == 1, 'Ambiguous cleanup receipt')
    removed = read(candidates[0])
    intent = read(candidates[0].with_name('CLEANUP_INTENT.json'))
    temp = Path(removed['temporary']).resolve()
    work = Path(negative['command'][negative['command'].index('--work-root') + 1]).resolve()
    require(negative['expected_failure'] is True and negative['temporary_removed'] is True, 'Wrong receipt status')
    require(removed['removed'] is True and intent['temporary'] == removed['temporary'], 'Cleanup receipt mismatch')
    require(intent['manifest_sha256'] == sha(root / 'MANIFEST.json'), 'Cleanup manifest mismatch')
    require(temp.is_relative_to(work) and temp != work and not temp.exists(), 'Temporary not confined/removed')
    wrapper = root / 'reproduce.py'
    probe = lifecycle_probes(wrapper.read_text(encoding='utf-8'), name)
    rows.append(dict(package=name, shipped_files=len(names), unchanged_old_files=len(preserved),
                     scientific_assets=len(manifest['assets']), new_manifest_sha256=sha(root / 'MANIFEST.json'),
                     new_zip_sha256=sha(B / receipt['archive']), old_zip_sha256=sha(old_zip), historical_zip_extra_receipts=old_extras,
                     wrapper_sha256=sha(wrapper), negative_log_sha256=sha(log),
                     temporary_absent=True, temporary=str(temp),
                     removal_receipt_sha256=sha(candidates[0]),
                     intent_receipt_sha256=sha(candidates[0].with_name('CLEANUP_INTENT.json')),
                     lifecycle_probe=probe))

result = dict(status='VERIFIED_3_NEGATIVES_AND_PRESERVED_ASSETS_WITH_2_LIFECYCLE_FINDINGS',
              method='Read/hash/ZIP and AST lifecycle-only in-memory probes under optimize=1; no wrapper/science subprocess',
              utc=datetime.now(timezone.utc).isoformat(), builder_sha256=build['builder_sha256'],
              controls_sha256=sha(controls_path), script_sha256=sha(Path(__file__)), rows=rows)
raw = (json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')
with OUT.open('xb') as f:
    f.write(raw)
require(OUT.read_bytes() == raw, 'Results write mismatch')
print(json.dumps(dict(status=result['status'], results=str(OUT), cases=sum(len(r['lifecycle_probe']['cases']) for r in rows),
    packages=[dict(package=r['package'], shipped_files=r['shipped_files'], assets=r['scientific_assets'],
                   setup=r['lifecycle_probe']['first_setup_line'], try_line=r['lifecycle_probe']['try_line']) for r in rows])))
