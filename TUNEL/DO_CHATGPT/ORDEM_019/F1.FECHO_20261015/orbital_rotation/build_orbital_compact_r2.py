"""Compile in an immutable sandbox with one verified local dependency directory.

Only sandbox .olean files are copied. Production kernel/mathlib remain read-only
search roots. Each copied dependency is checked against its completed receipt.
No hard links, junctions, retries, or reuse of an uncertain compilation.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
NET = BASE.parent.parent/'F1.REDE'
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
SOURCE = Path(sys.argv[1]).resolve()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pin(p):
    return dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size)


def save(p,raw):
    if isinstance(raw,str):
        raw=raw.encode('utf-8')
    with p.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert p.read_bytes()==raw


def imports(p):
    return re.findall(r'^import\s+([\w.]+)',p.read_text(encoding='utf-8'),re.M)


chosen={}
compiled_index={}
for root in (NET,BASE.parent):
    for obj in root.glob('*/attempts/*/*.olean'):
        compiled_index.setdefault(obj.stem,[]).append(obj)


def resolve(name):
    if name in {'Lean','Mathlib','Std','Batteries'} or name.startswith(('TGLExt.','Mathlib.','Lean.','Std.','Batteries.')):
        return
    if name in chosen:
        return
    srcs=([BASE/(name+'.lean')] if (BASE/(name+'.lean')).is_file() else
          [p for root in (NET,BASE.parent) for p in root.glob('*/'+name+'.lean') if 'review' not in p.parent.name])
    if len(srcs)!=1:
        raise RuntimeError(('source ambiguous',name,[str(p) for p in srcs]))
    src=srcs[0]
    match=[]
    for obj in sorted(compiled_index.get(name,[])):
        snap=obj.with_suffix('.lean')
        receipt=obj.parent/'RECEIPT.json'
        if not snap.exists() or not receipt.exists() or sha(snap)!=sha(src):
            continue
        r=json.loads(receipt.read_bytes())
        if type(r.get('exit_code')) is not int or r['exit_code']!=0:
            continue
        expected=next((x['sha256'] for x in r.get('artifacts',[]) if Path(x['path'])==obj),None)
        if expected is None or expected!=sha(obj):
            raise RuntimeError(('compiled artifact pin mismatch',str(obj)))
        source_expected=r.get('source',{}).get('sha256') or next((x['sha256'] for x in r.get('artifacts',[]) if Path(x['path'])==snap),None)
        if source_expected is None or source_expected!=sha(snap):
            raise RuntimeError(('compiled source pin mismatch',str(snap)))
        match.append((obj,snap,receipt))
    if not match:
        raise RuntimeError(('no matching compiled source',name))
    chosen[name]=match[-1]
    for child in imports(src):
        resolve(child)


for name in imports(SOURCE):
    resolve(name)
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
out=BASE/'attempts'/stamp
out.mkdir(parents=True,exist_ok=False)
cache=out/'dependency_cache'
cache.mkdir()
save(out/SOURCE.name,SOURCE.read_bytes())
deps=[pin(p) for triple in chosen.values() for p in triple]
copies=[]
for name,(obj,snap,receipt) in chosen.items():
    target=cache.joinpath(*name.split('.')).with_suffix('.olean')
    target.parent.mkdir(parents=True,exist_ok=True)
    save(target,obj.read_bytes())
    assert sha(target)==sha(obj)
    copies.append(dict(module=name,original=pin(obj),copy=pin(target),receipt=pin(receipt)))
paths=[out,cache,KERNEL/'.lake/build/lib/lean']+sorted((KERNEL/'.lake/packages').glob('*/.lake/build/lib/lean'))+[LEAN.parent.parent/'lib/lean']
assert all(p.is_dir() for p in paths)
env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,paths)))
save(out/'DEPENDENCY_CACHE.json',json.dumps(dict(copies=copies,path_count=len(paths),
    path_chars=len(env['LEAN_PATH']),scope='Copies only; no junctions or production writes.'),ensure_ascii=False,indent=2)+'\n')
cmd=[str(LEAN),'-j2','--profile','-o',str(out/SOURCE.with_suffix('.olean').name),str(out/SOURCE.name)]
version=subprocess.check_output([str(LEAN),'--version'],text=True).strip()
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
t0=time.perf_counter()
with (out/'RUNNING_OUTPUT.log').open('xb') as stream:
    process=subprocess.Popen(cmd,cwd=out,env=env,stdout=stream,stderr=subprocess.STDOUT)
    save(out/'START_RECEIPT.json',json.dumps(dict(start_utc=start,pid=process.pid,command=cmd,
        cwd=str(out),source=pin(out/SOURCE.name),builder=pin(Path(__file__)),LEAN_PATH=env['LEAN_PATH'],
        dependency_cache=pin(out/'DEPENDENCY_CACHE.json')),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(attempt=str(out),pid=process.pid,start_utc=start,path_count=len(paths),
        path_chars=len(env['LEAN_PATH']),copied_modules=len(copies))),flush=True)
    exit_code=process.wait()
end=datetime.datetime.now(datetime.timezone.utc).isoformat()
seconds=time.perf_counter()-t0
raw=(out/'RUNNING_OUTPUT.log').read_bytes()
unchanged=all(sha(Path(p['path']))==p['sha256'] for p in deps)
cache_unchanged=all(sha(Path(c['copy']['path']))==c['copy']['sha256'] for c in copies)
meta=dict(start_utc=start,end_utc=end,seconds=seconds,command=cmd,cwd=str(out),toolchain=version,
    LEAN_PATH=env['LEAN_PATH'],exit_code=exit_code,source=pin(out/SOURCE.name),builder=pin(Path(__file__)),
    dependencies=deps,readonly_dependencies_unchanged=unchanged,dependency_cache_unchanged=cache_unchanged,
    dependency_cache=pin(out/'DEPENDENCY_CACHE.json'),no_junction=True,production_modified=False)
save(out/'BUILD.log',json.dumps(meta,ensure_ascii=False,indent=2)+'\n\nSTDOUT+STDERR\n'+raw.decode('utf-8','replace'))
save(out/'AXIOMS.txt',raw)
meta['artifacts']=[pin(p) for p in sorted(out.iterdir()) if p.is_file()]
save(out/'RECEIPT.json',json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(attempt=str(out),exit_code=exit_code,seconds=seconds,
    readonly_dependencies_unchanged=unchanged,dependency_cache_unchanged=cache_unchanged),ensure_ascii=False))
print(raw.decode('utf-8','replace'))
raise SystemExit(exit_code or (0 if unchanged and cache_unchanged else 3))
