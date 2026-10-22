"""One execution receipt with literal command, timing, exit and byte pins."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys, time
ROOT=Path(__file__).resolve().parent
def pin(p):
    p=Path(p); return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def new(p,data):
    with Path(p).open('xb') as f:f.write(data)
if any((ROOT/n).exists() for n in ('COMMAND_RESULT_R69.json','STDOUT_R69.txt','STDERR_R69.txt','START_R69.json')):
    raise RuntimeError('Execution artifacts already exist')
command=[sys.executable,'-B','-X','utf8',str(ROOT/'test_r69.py')]
start=datetime.datetime.now(datetime.timezone.utc); timer=time.perf_counter()
cp=subprocess.run(command,cwd=ROOT,capture_output=True)
new(ROOT/'STDOUT_R69.txt',cp.stdout);new(ROOT/'STDERR_R69.txt',cp.stderr)
r={'command':command,'cwd':str(ROOT),'started_utc':start.isoformat(),'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-timer,'exit_code':cp.returncode,'execution_count':1,'runner':pin(__file__),'stdout':pin(ROOT/'STDOUT_R69.txt'),'stderr':pin(ROOT/'STDERR_R69.txt'),'freeze':pin(ROOT/'FREEZE_R69.json')}
if (ROOT/'RESULT_R69.json').exists():r['result']=pin(ROOT/'RESULT_R69.json')
new(ROOT/'COMMAND_RESULT_R69.json',(json.dumps(r,indent=2)+'\n').encode())
print(cp.stdout.decode('utf8'));print(cp.stderr.decode('utf8'));print(json.dumps(r))
sys.exit(cp.returncode)
