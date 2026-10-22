"""Immutable build attempts for the v394 continuous-flow candidate."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')

def save(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    data = value if isinstance(value, bytes) else (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode()
    with p.open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    assert p.read_bytes() == data

def pin(p):
    b = p.read_bytes()
    return {'path':str(p), 'sha256':hashlib.sha256(b).hexdigest(), 'bytes':len(b)}

def main():
    modules = sys.argv[1:] or ['TimeGravitonScalar']
    out = BASE/'attempts'/dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    out.mkdir(parents=True, exist_ok=False)
    paths = [out]
    extra = os.environ.get('TIME_MATRIX_OLEAN_ROOT')
    if extra: paths.append(Path(extra))
    paths += [KERNEL/'.lake/build/lib/lean']
    paths += sorted((KERNEL/'.lake/packages').glob('*/.lake/build/lib/lean'))
    paths += [LEAN.parent.parent/'lib/lean']
    assert all(p.is_dir() for p in paths)
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, paths)))
    version = subprocess.check_output([str(LEAN),'--version'],text=True).strip()
    deps = [pin(KERNEL/'lean-toolchain'),pin(KERNEL/'lake-manifest.json')]
    deps += [pin(KERNEL/'TGLExt'/(m+'.lean')) for m in ['IALDJones','PhaseFrequencySeparation','TheRuleInTheContinuousMotor']]
    if extra:
        deps.append(pin(Path(extra)/'TimeGravitonMatrix.olean'))
        deps.append(pin(Path(extra)/'TimeGravitonMatrix.lean'))
    save(out/'DEPENDENCIES.json',deps)
    receipts=[]
    for mod in modules:
        source=BASE/'TGLExt'/(mod+'.lean')
        target=out/(mod+'.lean')
        data=source.read_bytes()
        assert not re.search(rb'\b(sorry|axiom)\b',data), 'Forbidden source token'
        save(target,data)
        cmd=[str(LEAN),'-o',str(target.with_suffix('.olean')),str(target)]
        start=dt.datetime.now(dt.timezone.utc).isoformat(); clock=time.perf_counter()
        cp=subprocess.run(cmd,cwd=out,env=env,capture_output=True)
        seconds=time.perf_counter()-clock; end=dt.datetime.now(dt.timezone.utc).isoformat()
        raw=cp.stdout+cp.stderr; text=raw.decode('utf-8','replace')
        axioms=[]
        for decl,items in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",text):
            axioms.append({'declaration':decl,'axioms':[s.strip() for s in items.split(',') if s.strip()]})
        for decl in re.findall(r"'([^']+)' does not depend on any axioms",text):
            axioms.append({'declaration':decl,'axioms':[]})
        requested=re.findall(r'^#print axioms\s+(\S+)',data.decode(),re.M)
        ok=len(axioms)==len(requested) and bool(axioms) and all(set(x['axioms']) <= {'propext','Classical.choice','Quot.sound'} for x in axioms)
        receipt={'module':mod,'start_utc':start,'end_utc':end,'seconds':seconds,'command':cmd,'cwd':str(out),'toolchain':version,'LEAN_PATH':env['LEAN_PATH'],'exit_code':cp.returncode,'source':pin(target),'axiom_reports':axioms,'requested_axiom_reports':len(requested),'axioms_within_trio':ok}
        save(out/(mod+'.BUILD.log'),(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n\nSTDOUT+STDERR\n').encode()+raw)
        save(out/(mod+'.AXIOMS.txt'),'\n'.join(l for l in text.splitlines() if 'axioms' in l).encode())
        save(out/(mod+'.RESULT.json'),receipt)
        receipts.append(receipt)
        if cp.returncode or not ok:
            print(json.dumps({'attempt':str(out),'module':mod,'exit_code':cp.returncode,'axioms_ok':ok},ensure_ascii=False)); print(text)
            raise SystemExit(cp.returncode or 2)
    assert all(pin(Path(d['path']))==d for d in deps)
    result={'passed':True,'attempt':str(out),'dependencies_unchanged':True,'modules':receipts,'artifacts':[pin(p) for p in sorted(out.rglob('*')) if p.is_file()]}
    save(out/'RESULTADO_BUILD.json',result)
    print(json.dumps({'passed':True,'attempt':str(out),'declarations':sum(len(r['axiom_reports']) for r in receipts),'result':pin(out/'RESULTADO_BUILD.json')},ensure_ascii=False))

if __name__=='__main__': main()
