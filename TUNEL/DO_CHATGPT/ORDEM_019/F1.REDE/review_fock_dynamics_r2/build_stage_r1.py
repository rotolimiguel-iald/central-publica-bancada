"""Independent incremental recompilation; each frozen new module is compiled once."""
from pathlib import Path
import sys, json, hashlib, os, re, subprocess, time, datetime as dt
BASE=Path(__file__).resolve().parent; ROOT=BASE.parent; SRC=ROOT/'fock_construction'
OUT=BASE/'sandbox'; OUT.mkdir(exist_ok=True)
KERNEL=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
previous=json.loads((ROOT/'review_fock_r2/REVIEW_FOCK_R1.json').read_text())
OLD2=Path(previous['builds'][0]['cwd'])
OLD=ROOT/'review_fock_full_r2/sandbox'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,b):
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert p.read_bytes()==b
paths=[OUT,OLD,OLD2,KERNEL/'.lake/build/lib/lean']+sorted((KERNEL/'.lake/packages').glob('*/.lake/build/lib/lean'))+[LEAN.parent.parent/'lib/lean']
env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,paths)))
version=subprocess.check_output([str(LEAN),'--version'],text=True).strip()
for module in sys.argv[1:]:
    assert re.fullmatch('[A-Za-z0-9_]+',module)
    source=SRC/(module+'.lean'); local=OUT/source.name
    assert not local.exists() and not local.with_suffix('.olean').exists()
    b=source.read_bytes(); save(local,b)
    assert not re.search(rb'\bsorry\b|\badmit\b|^\s*axiom\s',b,re.M)
    cmd=[str(LEAN),'-o',str(local.with_suffix('.olean')),str(local)]
    deps=[pin(p) for d in [OUT,OLD,OLD2] for p in sorted(d.glob('*.olean'))]
    start=dt.datetime.now(dt.timezone.utc).isoformat(); timer=time.perf_counter()
    result=subprocess.run(cmd,cwd=OUT,env=env,capture_output=True)
    seconds=time.perf_counter()-timer; end=dt.datetime.now(dt.timezone.utc).isoformat()
    raw=result.stdout+result.stderr; output=raw.decode('utf-8')
    meta={'module':module,'source':pin(source),'copy':pin(local),'command':cmd,'cwd':str(OUT),'LEAN_PATH':env['LEAN_PATH'],'toolchain':version,'start_utc':start,'end_utc':end,'seconds':seconds,'exit_code':result.returncode,'dependencies_read_only':deps}
    save(BASE/(module+'.log'),(json.dumps(meta,ensure_ascii=False,indent=2)+'\nSTDOUT+STDERR\n').encode()+raw)
    meta['log']=pin(BASE/(module+'.log'))
    localdecl=[]
    for line in output.splitlines():
        if line.startswith('LOCAL_DECL\t'):
            pp=line.split('\t'); localdecl.append(pp[1]); assert (set(pp[2].split(','))-{''})<={'propext','Classical.choice','Quot.sound'}
    for axs in re.findall(rb'depends on axioms:\s*\[([^\]]*)\]',raw):
        assert {s.strip().decode() for s in axs.split(b',') if s.strip()}<={'propext','Classical.choice','Quot.sound'}
    assert b'sorryAx' not in raw
    meta['local_constants']=localdecl; meta['printed_axiom_count']=len(re.findall(rb'depends on axioms:',raw))
    if not result.returncode: meta['olean']=pin(local.with_suffix('.olean'))
    save(BASE/(module+'_RECEIPT.json'),(json.dumps(meta,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps({'module':module,'exit_code':result.returncode,'seconds':seconds,'local_constants':len(localdecl),'printed_axiom_count':meta['printed_axiom_count'],'receipt_sha256':sha(BASE/(module+'_RECEIPT.json'))}),flush=True)
    if result.returncode: raise SystemExit(result.returncode)
    assert sha(source)==meta['source']['sha256']
    for p in deps: assert sha(Path(p['path']))==p['sha256']
