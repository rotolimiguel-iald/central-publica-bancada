"""Independent material review: byte copies, fresh builds, no production writes."""
from pathlib import Path
import datetime as dt
import hashlib, json, os, re, subprocess, time

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, b):
    with p.open('xb') as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    assert p.read_bytes() == b
def jsave(p, x): save(p, (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode())

attempt = BASE / dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
attempt.mkdir()
sources = [ROOT/'fubini/FubiniL2.lean', ROOT/'fiber_conjugation/FiberConjugation.lean',
           ROOT/'fiber_conjugation/GeometricFiberConjugation.lean']
sources += [ROOT/'modular_wedge'/n for n in ['VectorWedge.lean','SpectralConjugation.lean','VectorSquare.lean','CanonicalWedge.lean','CanonicalOutput.lean','AuditAll.lean']]
pins = []
for p in sources:
    b=p.read_bytes(); save(attempt/p.name,b)
    pins.append({'path':str(p),'sha256':sha(p),'bytes':len(b),'copy':str(attempt/p.name)})
    if re.search(rb'\bsorry\b|\badmit\b|^\s*axiom\s',b,re.M):
        raise RuntimeError(f'Unproved source token: {p}')
paths=[attempt,KERNEL/'.lake/build/lib/lean']+sorted((KERNEL/'.lake/packages').glob('*/.lake/build/lib/lean'))+[LEAN.parent.parent/'lib/lean']
env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,paths)))
version=subprocess.check_output([str(LEAN),'--version'],text=True).strip()
results=[]
for source in sources:
    local=attempt/source.name
    command=[str(LEAN),'-o',str(local.with_suffix('.olean')),str(local)]
    start=dt.datetime.now(dt.timezone.utc).isoformat(); t=time.perf_counter()
    proc=subprocess.run(command,cwd=attempt,env=env,capture_output=True)
    sec=time.perf_counter()-t; end=dt.datetime.now(dt.timezone.utc).isoformat()
    raw=proc.stdout+proc.stderr
    meta={'module':source.stem,'command':command,'cwd':str(attempt),'start_utc':start,'end_utc':end,'seconds':sec,'exit_code':proc.returncode,'LEAN_PATH':env['LEAN_PATH'],'toolchain':version,'source_sha256':sha(local)}
    save(attempt/(source.stem+'.log'),(json.dumps(meta,ensure_ascii=False,indent=2)+'\nSTDOUT+STDERR\n').encode()+raw)
    meta['log_sha256']=sha(attempt/(source.stem+'.log'))
    results.append(meta)
    print(json.dumps({'module':source.stem,'exit':proc.returncode,'seconds':sec}),flush=True)
    if proc.returncode:
        jsave(attempt/'FAILED_BUILD.json',{'sources':pins,'builds':results}); raise SystemExit(proc.returncode)
    if b'sorryAx' in raw: raise RuntimeError('sorry axiom emitted')
    for content in re.findall(rb'depends on axioms:\s*\[([^\]]*)\]',raw):
        axs={s.strip().decode() for s in content.split(b',') if s.strip()}
        if not axs <= {'propext','Classical.choice','Quot.sound'}: raise RuntimeError(str(axs))
jsave(attempt/'RECOMPILE_RECEIPT.json',{'reviewer':'codex-independent-modular-review','sources':pins,'builds':results,'all_exit_zero':True,'axioms_subset_trio':True,'production_writes':False,'junctions_created':False})
print(json.dumps({'attempt':str(attempt),'receipt_sha256':sha(attempt/'RECOMPILE_RECEIPT.json')},ensure_ascii=False))
