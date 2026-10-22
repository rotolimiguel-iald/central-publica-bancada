"""Sandbox-only immutable Lean attempts, with readonly dependency pins."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
from mission_r57 import check, pin as basic_pin

BASE = Path(__file__).resolve().parent
OUT = BASE.parent
NET = OUT.parent / 'F1.REDE'
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
SOURCE = (BASE / sys.argv[1]).resolve()
assert SOURCE.parent == BASE and SOURCE.suffix == '.lean'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return dict(path=str(p), sha256=sha(p), bytes=p.stat().st_size)
def save(p, b):
    if isinstance(b, str): b=b.encode('utf-8')
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert p.read_bytes()==b
def imports(p): return re.findall(r'^import\s+([\w.]+)', p.read_text(encoding='utf-8'), re.M)
def js(p, v): save(p, json.dumps(v, ensure_ascii=False, indent=2)+'\n')

p, projection_path, checked, check_path = check()
compiled = {}
for root in (NET, OUT):
    for obj in root.glob('*/attempts/*/*.olean'):
        compiled.setdefault(obj.stem, []).append(obj)
chosen = {}
kernel_modules = {}

def resolve(name):
    if (KERNEL/(name.replace('.', '/')+'.lean')).is_file():
        if name in kernel_modules: return
        src=KERNEL/(name.replace('.', '/')+'.lean')
        obj=KERNEL/'.lake/build/lib/lean'/(name.replace('.', '/')+'.olean')
        assert src.is_file() and obj.is_file(), (name, src, obj)
        kernel_modules[name]=(src, obj)
        for imp in imports(src): resolve(imp)
        return
    if name in {'Lean', 'Mathlib', 'Std', 'Batteries', 'Aesop'} or name.startswith(
            ('Mathlib.', 'Lean.', 'Std.', 'Batteries.', 'Aesop.', 'Qq.', 'ProofWidgets.', 'ImportGraph.', 'Plausible.')):
        return
    if name in chosen: return
    srcs = [BASE/(name+'.lean')] if (BASE/(name+'.lean')).is_file() else [
        x for root in (NET, OUT) for x in root.glob('*/'+name+'.lean') if 'review' not in x.parent.name]
    assert len(srcs)==1, ('source ambiguity', name, srcs)
    src=srcs[0]; good=[]
    for obj in sorted(compiled.get(name, [])):
        snap=obj.with_suffix('.lean'); receipt=obj.parent/'RECEIPT.json'
        if snap.is_file() and receipt.is_file() and sha(snap)==sha(src):
            r=json.loads(receipt.read_bytes())
            if type(r.get('exit_code')) is int and r['exit_code']==0: good.append((src, obj, snap, receipt))
    assert good, ('no green matching cache', name)
    chosen[name]=good[-1]
    for imp in imports(src): resolve(imp)

for name in imports(SOURCE): resolve(name)
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
attempt=BASE/'attempts'/stamp
attempt.mkdir(parents=True, exist_ok=False)
save(attempt/SOURCE.name, SOURCE.read_bytes())
dep_paths = list(dict.fromkeys(x for group in list(chosen.values())+list(kernel_modules.values()) for x in group))
deps=[pin(x) for x in dep_paths]
paths=list(dict.fromkeys([attempt]+[v[1].parent for v in chosen.values()]+[
    KERNEL/'.lake/build/lib/lean']+sorted((KERNEL/'.lake/packages').glob('*/.lake/build/lib/lean'))+[
    LEAN.parent.parent/'lib/lean']))
assert all(x.is_dir() for x in paths)
env=dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, paths)))
cmd=[str(LEAN), '-j2', '-M4096', '--profile', '-o', str(attempt/(SOURCE.stem+'.olean')), str(attempt/SOURCE.name)]
version=subprocess.check_output([str(LEAN), '--version'], text=True).strip()
meta=dict(source=pin(attempt/SOURCE.name), source_original=pin(SOURCE), toolchain=version,
    lean_executable=pin(LEAN), command=cmd, cwd=str(attempt), LEAN_PATH=env['LEAN_PATH'],
    memory_limit_mb=4096, threads=2, dependencies=deps,
    dependency_scope='Transitive TGLExt source/olean and exact custom green source/cache/receipts; bundled mathlib runtime readonly, not recompiled.',
    mission_revision=p['receipt']['revision'], mission_projection=basic_pin(projection_path),
    mission_preflight=basic_pin(check_path), production_modified=False)
t0=time.perf_counter()
with (attempt/'RUNNING_OUTPUT.log').open('xb') as stream:
    process=subprocess.Popen(cmd, cwd=attempt, env=env, stdout=stream, stderr=subprocess.STDOUT)
    meta.update(pid=process.pid, start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    js(attempt/'START_RECEIPT.json', meta)
    print(json.dumps(dict(attempt=str(attempt), pid=process.pid, source=SOURCE.name)), flush=True)
    code=process.wait()
raw=(attempt/'RUNNING_OUTPUT.log').read_bytes()
meta.update(exit_code=code, seconds=time.perf_counter()-t0,
    end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    readonly_dependencies_unchanged=all(sha(Path(x['path']))==x['sha256'] for x in deps),
    source_unchanged=sha(SOURCE)==meta['source']['sha256'])
save(attempt/'BUILD.log', raw)
save(attempt/'AXIOMS.txt', raw)
meta['artifacts']=[pin(x) for x in sorted(attempt.iterdir()) if x.is_file()]
js(attempt/'RECEIPT.json', meta)
print(json.dumps({k:meta[k] for k in ('exit_code','seconds','readonly_dependencies_unchanged','source_unchanged')}, ensure_ascii=False))
print(raw.decode('utf-8', 'replace'))
raise SystemExit(code or (0 if meta['readonly_dependencies_unchanged'] and meta['source_unchanged'] else 3))
