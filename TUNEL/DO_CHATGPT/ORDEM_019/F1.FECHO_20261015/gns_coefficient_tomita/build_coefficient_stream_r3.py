"""Compile a new immutable attempt, reusing measured readonly dependency caches."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
BASE=Path(__file__).resolve().parent
NET=BASE.parent.parent/'F1.REDE'
KERNEL=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
SOURCE=BASE/(sys.argv[1] if len(sys.argv)>1 else 'CanonicalFockAssemblyR1.lean')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size)
def save(p,b):
    b=b.encode('utf-8') if isinstance(b,str) else b
    with p.open('xb') as f: f.write(b);f.flush();os.fsync(f.fileno())
    assert p.read_bytes()==b
def imports(p): return re.findall(r'^import\s+([\w.]+)',p.read_text(encoding='utf-8'),re.M)
chosen={}
compiled_index={}
for root in (NET,BASE.parent):
    for obj in root.glob('*/attempts/*/*.olean'):
        compiled_index.setdefault(obj.stem,[]).append(obj)
def resolve(name):
    if name.startswith(('TGLExt.','Mathlib.','Lean.','Std.','Batteries.')): return
    if name in chosen: return
    srcs=([BASE/(name+'.lean')] if (BASE/(name+'.lean')).is_file() else [p for root in [NET,BASE.parent] for p in root.glob('*/'+name+'.lean') if 'review' not in p.parent.name])
    if len(srcs)!=1: raise RuntimeError(('source ambiguous',name,[str(p) for p in srcs]))
    src=srcs[0]; match=[]
    for obj in sorted(compiled_index.get(name,[])):
        snap=obj.with_suffix('.lean'); receipt=obj.parent/'RECEIPT.json'
        if snap.exists() and sha(snap)==sha(src) and receipt.exists():
            r=json.loads(receipt.read_bytes())
            if r.get('exit_code')==0: match.append((obj,snap,receipt))
    if not match: raise RuntimeError(('no matching compiled source',name))
    chosen[name]=match[-1]
    for imp in imports(src): resolve(imp)
for name in imports(SOURCE): resolve(name)
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
out=BASE/'attempts'/stamp;out.mkdir(parents=True,exist_ok=False)
save(out/SOURCE.name,SOURCE.read_bytes())
deps=[pin(p) for triple in chosen.values() for p in triple]
paths=list(dict.fromkeys([out]+[t[0].parent for t in chosen.values()]+[KERNEL/'.lake/build/lib/lean']+sorted((KERNEL/'.lake/packages').glob('*/.lake/build/lib/lean'))+[LEAN.parent.parent/'lib/lean']))
assert all(p.is_dir() for p in paths)
env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,paths)))
cmd=[str(LEAN),'--profile','-o',str(out/SOURCE.with_suffix('.olean').name),str(out/SOURCE.name)]
version=subprocess.check_output([str(LEAN),'--version'],text=True).strip()
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t0=time.perf_counter()
with (out/'RUNNING_OUTPUT.log').open('xb') as stream:
    process=subprocess.Popen(cmd,cwd=out,env=env,stdout=stream,stderr=subprocess.STDOUT)
    start_record=dict(start_utc=start,pid=process.pid,command=cmd,cwd=str(out),source=pin(out/SOURCE.name),LEAN_PATH=env['LEAN_PATH'])
    save(out/'START_RECEIPT.json',json.dumps(start_record,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(attempt=str(out),pid=process.pid,start_utc=start)),flush=True)
    exit_code=process.wait()
end=datetime.datetime.now(datetime.timezone.utc).isoformat();seconds=time.perf_counter()-t0
raw=(out/'RUNNING_OUTPUT.log').read_bytes()
unchanged=all(sha(Path(p['path']))==p['sha256'] for p in deps)
meta=dict(start_utc=start,end_utc=end,seconds=seconds,command=cmd,cwd=str(out),toolchain=version,LEAN_PATH=env['LEAN_PATH'],exit_code=exit_code,source=pin(out/SOURCE.name),dependencies=deps,readonly_dependencies_unchanged=unchanged,no_junction=True,production_modified=False)
save(out/'BUILD.log',json.dumps(meta,ensure_ascii=False,indent=2)+'\n\nSTDOUT+STDERR\n'+raw.decode('utf-8','replace'))
save(out/'AXIOMS.txt',raw)
meta['artifacts']=[pin(p) for p in sorted(out.iterdir()) if p.is_file()]
save(out/'RECEIPT.json',json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(attempt=str(out),exit_code=exit_code,seconds=seconds,readonly_dependencies_unchanged=unchanged),ensure_ascii=False))
print(raw.decode('utf-8','replace'))
raise SystemExit(exit_code or (0 if unchanged else 3))
