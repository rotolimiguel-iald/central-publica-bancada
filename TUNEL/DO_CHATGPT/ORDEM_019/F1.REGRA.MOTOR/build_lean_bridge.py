"""Immutable Lean sandbox attempts, explicit commands, clocks, paths and axioms."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import time

BASE=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\Central de Patentes')
KERNEL=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
LEAN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
MODULES=['RuleTruthContract','TheRuleInTheContinuousMotor']

def save(p,b):
    if not isinstance(b,bytes):
        b=(json.dumps(b,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    with p.open('xb') as f:
        f.write(b);f.flush();os.fsync(f.fileno())
    assert p.read_bytes()==b

def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}

def main():
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    out=BASE/'attempts'/stamp
    out.mkdir(parents=True,exist_ok=False)
    for mod in MODULES:
        save(out/(mod+'.lean'),(BASE/'formal'/(mod+'.lean')).read_bytes())
    paths=[out,KERNEL/'.lake/build/lib/lean']
    paths+=sorted((KERNEL/'.lake/packages').glob('*/.lake/build/lib/lean'))
    paths+=[LEAN.parent.parent/'lib/lean']
    assert all(p.is_dir() for p in paths) and LEAN.is_file()
    env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,paths)))
    version=subprocess.check_output([str(LEAN),'--version'],text=True).strip()
    deps=[]
    for name in ['IALD','IALDJones','CondExpect','IALDRhoStar']:
        p=KERNEL/'TGLExt'/(name+'.lean')
        q=ROOT/'work/cadeia_de_selo/v392/kb_stub_v392/TGLExt'/(name+'.lean')
        assert p.read_bytes()==q.read_bytes(), 'Source snapshot mismatch: '+name
        deps.append(pin(p))
    for p in [KERNEL/'lean-toolchain',KERNEL/'lake-manifest.json',KERNEL/'.lake/packages/mathlib/lake-manifest.json']:
        if p.exists():deps.append(pin(p))
    for p in [BASE/'PREREGISTRO_R1.json',BASE/'OPERADOR_VERBATIM.txt',
              BASE.parent/'F1.REGRA.P1/formal/RuleTruthContract.lean']:
        deps.append(pin(p))
    assert (BASE/'formal/RuleTruthContract.lean').read_bytes() == (BASE.parent/'F1.REGRA.P1/formal/RuleTruthContract.lean').read_bytes()
    save(out/'DEPENDENCIES.json',deps)
    receipts=[]
    for mod in MODULES:
        cmd=[str(LEAN),'-o',str(out/(mod+'.olean')),str(out/(mod+'.lean'))]
        start=dt.datetime.now(dt.timezone.utc).isoformat();clock=time.perf_counter()
        cp=subprocess.run(cmd,cwd=out,env=env,capture_output=True)
        seconds=time.perf_counter()-clock;end=dt.datetime.now(dt.timezone.utc).isoformat()
        raw=cp.stdout+cp.stderr
        text=raw.decode('utf-8','replace')
        ax=[]
        for decl,items in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",text):
            names=[v.strip() for v in items.split(',') if v.strip()]
            ax.append({'declaration':decl,'axioms':names})
        for decl in re.findall(r"'([^']+)' does not depend on any axioms",text):
            ax.append({'declaration':decl,'axioms':[]})
        requested=re.findall(r'^#print axioms\s+(\S+)',(out/(mod+'.lean')).read_text(encoding='utf-8'),re.M)
        method='print_axioms'
        if mod in MODULES:
            method='Lean.collectAxioms_all_local_constants'
            for line in text.splitlines():
                if line.startswith('LOCAL_DECL\t'):
                    _,decl,names=line.split('\t',2)
                    ax.append({'declaration':decl,'axioms':[v for v in names.split(',') if v]})
        axioms_ok=((len(ax)==len(requested) or mod in MODULES) and len(ax)>0 and
            all(set(a['axioms'])<={'propext','Classical.choice','Quot.sound'} for a in ax))
        metadata={'module':mod,'start_utc':start,'end_utc':end,'seconds':seconds,
            'command':cmd,'cwd':str(out),'toolchain':version,'LEAN_PATH':env['LEAN_PATH'],
            'exit_code':cp.returncode,'source':pin(out/(mod+'.lean')),
            'axiom_reports':ax,'axiom_method':method,'requested_axiom_reports':len(requested),'axioms_within_trio':axioms_ok}
        save(out/(mod+'.BUILD.log'),(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n\nSTDOUT+STDERR\n').encode()+raw)
        save(out/(mod+'.AXIOMS.txt'),raw)
        save(out/(mod+'.RESULT.json'),metadata)
        receipts.append(metadata)
        if cp.returncode or not axioms_ok:
            print(json.dumps({'attempt':str(out),'module':mod,'exit_code':cp.returncode,'axioms_ok':axioms_ok},ensure_ascii=False))
            print(text)
            raise SystemExit(cp.returncode or 2)
    assert all(pin(Path(p['path']))==p for p in deps)
    result={'attempt':str(out),'passed':True,'dependencies_unchanged':True,'modules':receipts,
        'artifacts':[pin(p) for p in sorted(out.iterdir()) if p.is_file()]}
    save(out/'RESULTADO_BUILD.json',result)
    print(json.dumps({'attempt':str(out),'passed':True,'declarations':sum(len(r['axiom_reports']) for r in receipts),
        'seconds':sum(r['seconds'] for r in receipts),'result':pin(out/'RESULTADO_BUILD.json')},ensure_ascii=False))

if __name__=='__main__':main()
