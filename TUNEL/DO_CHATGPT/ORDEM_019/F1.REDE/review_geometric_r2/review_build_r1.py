"""Independent geometric identification review; use previously rebuilt dependencies read-only."""
from pathlib import Path
import json, hashlib, datetime as dt, subprocess, time, os, re
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
SRC=ROOT/'geometric_identification'
OLD=ROOT/'review_modular/20261013T215402_817152Z'
KERNEL=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(p,b):
    with p.open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert p.read_bytes()==b
def jsave(p,o): save(p,(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode())
out=BASE/dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ'); out.mkdir()
sources=[SRC/'attempts/20261013T221637_926790Z/FourierConjugation.lean',SRC/'attempts/20261013T221808_560069Z/GeometricIdentification.lean',SRC/'AuditGeometric.lean']
for p in sources:
    save(out/p.name,p.read_bytes())
    assert not re.search(rb'\bsorry\b|\badmit\b|^\s*axiom\s',p.read_bytes(),re.M)
deps=[pin(p) for p in sorted(OLD.glob('*.olean'))]
oldreceipt=ROOT/'review_modular/REVIEW_MODULAR_R1.json'
assert sha(oldreceipt)=='2fbdff5d6e1cea00047c80fead0c89d2663cbe5b041ad15ebe669b039aae81a4'
paths=[out,OLD,KERNEL/'.lake/build/lib/lean']+sorted((KERNEL/'.lake/packages').glob('*/.lake/build/lib/lean'))+[LEAN.parent.parent/'lib/lean']
env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,paths)))
toolchain=subprocess.check_output([str(LEAN),'--version'],text=True).strip()
builds=[]
for p in sources:
    copied=out/p.name; cmd=[str(LEAN),'-o',str(copied.with_suffix('.olean')),str(copied)]
    start=dt.datetime.now(dt.timezone.utc).isoformat(); timer=time.perf_counter()
    result=subprocess.run(cmd,cwd=out,env=env,capture_output=True)
    end=dt.datetime.now(dt.timezone.utc).isoformat(); seconds=time.perf_counter()-timer
    raw=result.stdout+result.stderr
    meta={'source':pin(copied),'command':cmd,'cwd':str(out),'start_utc':start,'end_utc':end,'seconds':seconds,'exit_code':result.returncode,'LEAN_PATH':env['LEAN_PATH'],'toolchain':toolchain}
    save(out/(p.stem+'.log'),(json.dumps(meta,ensure_ascii=False,indent=2)+'\nSTDOUT+STDERR\n').encode()+raw)
    builds.append(meta)
    print(json.dumps({'module':p.stem,'exit_code':result.returncode,'seconds':seconds}),flush=True)
    if result.returncode:
        jsave(out/'FAILED_BUILD.json',builds); raise SystemExit(result.returncode)
    assert b'sorryAx' not in raw
    for axs in re.findall(rb'depends on axioms:\s*\[([^\]]*)\]',raw):
        assert {a.strip().decode() for a in axs.split(b',') if a.strip()} <= {'propext','Classical.choice','Quot.sound'}
audit=(out/'AuditGeometric.log').read_text(encoding='utf-8')
names=json.loads((SRC/'LOCAL_DECLARATIONS.json').read_text())['names']
assert len(names)==22
for n in names: assert "'"+n+"'" in audit,n
for p in deps: assert sha(Path(p['path']))==p['sha256']
jsave(out/'RECOMPILE_RECEIPT.json',{'status':'PASS','sources':[pin(p) for p in sources],'builds':builds,'dependency_receipt':pin(oldreceipt),'compiled_dependencies_read_only':deps,'declarations':names,'only_trio':True,'zero_sorry':True})
print(json.dumps({'out':str(out),'receipt_sha256':sha(out/'RECOMPILE_RECEIPT.json')}))
