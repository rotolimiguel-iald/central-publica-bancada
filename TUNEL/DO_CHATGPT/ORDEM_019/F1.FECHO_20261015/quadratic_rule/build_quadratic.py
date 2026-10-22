"""Compile a fresh snapshot only; no original or previous artifact is overwritten."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess
import time

BASE = Path(__file__).resolve().parent
SOURCE = BASE / 'src/TGLExt/RuleQuadraticResidual.lean'
REUSE = BASE.parent.parent / 'F1.TEMPO.V394/formal_verified'
LEAN = Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
PACKAGES = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake\packages')

def pin(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def write_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f:
        f.write(data)

stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
attempt = BASE / 'attempts' / stamp
snapshot = attempt / 'src/TGLExt/RuleQuadraticResidual.lean'
write_new(snapshot, SOURCE.read_bytes())
olean = attempt / 'lib/TGLExt/RuleQuadraticResidual.olean'
olean.parent.mkdir(parents=True)
lean_path = ';'.join([str(REUSE/'lib')] + [str(p/'.lake/build/lib/lean')
    for p in sorted(PACKAGES.iterdir()) if (p/'.lake/build/lib/lean').is_dir()])
env = dict(os.environ, LEAN_PATH=lean_path)
toolchain = subprocess.run([str(LEAN), '--version'], capture_output=True, text=True, check=True).stdout.strip()
cmd = [str(LEAN), '-R', str(attempt/'src'), '-o', str(olean), str(snapshot)]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
tic = time.monotonic()
run = subprocess.run(cmd, env=env, cwd=str(attempt/'src'), capture_output=True)
seconds = time.monotonic() - tic
end = datetime.datetime.now(datetime.timezone.utc).isoformat()
write_new(attempt/'STDOUT.log', run.stdout)
write_new(attempt/'STDERR.log', run.stderr)
out = run.stdout.decode('utf-8', errors='replace') + run.stderr.decode('utf-8', errors='replace')
reports = {}
for name, axioms in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", out, flags=re.S):
    reports[name] = [a.strip() for a in axioms.split(',') if a.strip()]
expected = re.findall(r'^#print axioms (\S+)', snapshot.read_text(encoding='utf-8'), re.M)
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
passed = run.returncode == 0 and set(reports)==set(expected) and all(set(v)<=allowed for v in reports.values())
receipt = {'unit':'F1.FECHO_20261015', 'claim_event':845, 'toolchain':toolchain,
    'start_utc':start,'end_utc':end,'seconds':seconds,'command':cmd,'LEAN_PATH':lean_path,
    'exit_code':run.returncode,'passed':passed,'source':pin(snapshot),
    'stdout':pin(attempt/'STDOUT.log'),'stderr':pin(attempt/'STDERR.log'),
    'axiom_reports':reports,'expected_declarations':expected,'olean':pin(olean) if olean.exists() else None,
    'reused_sources':[pin(REUSE/'src/TGLExt/TimeGravitonMatrix.lean'),pin(REUSE/'src/TGLExt/TimeGravitonFlow.lean')],
    'scope':'Constructed M2 residual of the existing reading; no gate, original, memory or production mutation.'}
payload = json.dumps(receipt,ensure_ascii=False,indent=2).encode('utf-8')+b'\n'
write_new(attempt/'BUILD_RECEIPT.json',payload)
header=json.dumps({k:receipt[k] for k in ['toolchain','start_utc','end_utc','seconds','command','LEAN_PATH','exit_code']},ensure_ascii=False,indent=2)
write_new(attempt/'BUILD.log',(header+'\n\nSTDOUT\n').encode()+run.stdout+b'\nSTDERR\n'+run.stderr)
print(json.dumps({'receipt':str(attempt/'BUILD_RECEIPT.json'),'sha256':hashlib.sha256(payload).hexdigest(),'passed':passed,'exit_code':run.returncode,'declarations':len(reports),'seconds':seconds}))
if not passed:
    print(out)
raise SystemExit(0 if passed else 1)
