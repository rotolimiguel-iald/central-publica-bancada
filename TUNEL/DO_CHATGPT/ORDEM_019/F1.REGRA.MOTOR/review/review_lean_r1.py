"""Independent compilation in a fresh overlay; canonical caches are read only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, subprocess, time

OUT=Path(__file__).resolve().parents[1]
R=Path(__file__).resolve().parent
DEST=R/('lean_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ'))
DEST.mkdir(exist_ok=False)
SOURCE_BUILD=OUT/'attempts/20261014T143143_185233Z/RESULTADO_BUILD.json'
def now(): return datetime.now(timezone.utc).isoformat()
def pin(p):
    p=Path(p); b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def write(p,x):
    if not isinstance(x,bytes): x=(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
    with Path(p).open('xb') as f:f.write(x)

build=json.loads(SOURCE_BUILD.read_bytes()); modules=[]; allowed={'propext','Classical.choice','Quot.sound'}
started=now(); timer=time.perf_counter()
passed=True
for entry in build['modules']:
    name=entry['module']; original=Path(build['attempt'])/(name+'.lean')
    copy=DEST/original.name; write(copy,original.read_bytes())
    assert copy.read_bytes()==(OUT/'formal'/original.name).read_bytes()
    assert not re.search(r'\b(sorry|admit|sorryAx)\b',copy.read_text(encoding='utf-8'))
    env=os.environ.copy(); env['LEAN_PATH']=str(DEST)+';'+entry['LEAN_PATH'].split(';',1)[1]
    command=[entry['command'][0],'-o',str(DEST/(name+'.olean')),str(copy)]
    toolchain=subprocess.run([command[0],'--version'],capture_output=True,text=True,check=True).stdout.strip()
    begin=now(); t=time.perf_counter()
    proc=subprocess.run(command,cwd=DEST,env=env,capture_output=True)
    end=now(); seconds=time.perf_counter()-t
    write(DEST/(name+'.STDOUT.log'),proc.stdout); write(DEST/(name+'.STDERR.log'),proc.stderr)
    stdout=proc.stdout.decode('utf-8',errors='strict')
    local=[]
    for line in stdout.splitlines():
        if line.startswith('LOCAL_DECL\t'):
            _,decl,axioms=line.split('\t',2)
            local.append({'declaration':decl,'axioms':axioms.split(',') if axioms else []})
    module_pass=proc.returncode==0 and len(local)>0 and all(set(a['axioms'])<=allowed for a in local)
    source_theorems=len(re.findall(r'^theorem\s+',copy.read_text(encoding='utf-8'),flags=re.M))
    out=DEST/(name+'.olean'); prior=Path(build['attempt'])/out.name
    rec={'module':name,'passed':module_pass,'start_utc':begin,'finish_utc':end,'seconds':seconds,'command':command,'cwd':str(DEST),'toolchain':toolchain,'LEAN_PATH':env['LEAN_PATH'],'exit_code':proc.returncode,'theorems':source_theorems,'axiom_reports':local,'within_trio':all(set(a['axioms'])<=allowed for a in local),'source':pin(copy),'stdout':pin(DEST/(name+'.STDOUT.log')),'stderr':pin(DEST/(name+'.STDERR.log')),'olean':pin(out) if out.exists() else None,'olean_matches_builder':out.exists() and out.read_bytes()==prior.read_bytes()}
    write(DEST/(name+'.RECEIPT.json'),rec); modules.append(rec); passed=passed and module_pass
    if not module_pass: break
receipt={'passed':passed and len(modules)==2,'start_utc':started,'finish_utc':now(),'seconds':time.perf_counter()-timer,'builder_receipt':pin(SOURCE_BUILD),'script':pin(__file__),'modules':modules,'new_theorem_count':next((m['theorems'] for m in modules if m['module']=='TheRuleInTheContinuousMotor'),None),'reused_theorem_count':next((m['theorems'] for m in modules if m['module']=='RuleTruthContract'),None),'scope':'Continuous-time finite-dimensional motor; new M4 bridge matches runtime block pinching, not corner or vector motor.'}
write(DEST/'REVIEW_LEAN_R1.json',receipt)
print(json.dumps({'passed':receipt['passed'],'result':str(DEST/'REVIEW_LEAN_R1.json'),'modules':[(m['module'],m['exit_code'],m['theorems'],m['olean_matches_builder']) for m in modules]}))
raise SystemExit(0 if receipt['passed'] else 1)
