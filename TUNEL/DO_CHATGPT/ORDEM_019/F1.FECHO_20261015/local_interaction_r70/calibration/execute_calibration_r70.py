"""Exclusive command receipt; wrapper is itself frozen before execution."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
def pin(p):
    p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def new(p,raw):
    with Path(p).open('xb') as f:f.write(raw)
if any((ROOT/n).exists() for n in ['COMMAND_CALIBRATION_R70.json','STDOUT_CALIBRATION_R70.txt','STDERR_CALIBRATION_R70.txt','START_CALIBRATION_R70.json']):raise RuntimeError('No repeated run')
command=[sys.executable,'-B','-X','utf8',str(ROOT/'test_reservoir_r70.py')]
started=datetime.datetime.now(datetime.timezone.utc);timer=time.perf_counter()
p=subprocess.run(command,cwd=ROOT,capture_output=True)
new(ROOT/'STDOUT_CALIBRATION_R70.txt',p.stdout);new(ROOT/'STDERR_CALIBRATION_R70.txt',p.stderr)
r={'command':command,'cwd':str(ROOT),'started_utc':started.isoformat(),'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-timer,'exit_code':p.returncode,'runner':pin(__file__),'stdout':pin(ROOT/'STDOUT_CALIBRATION_R70.txt'),'stderr':pin(ROOT/'STDERR_CALIBRATION_R70.txt')}
new(ROOT/'COMMAND_CALIBRATION_R70.json',(json.dumps(r,indent=2)+'\n').encode())
print(p.stdout.decode('utf8'));print(p.stderr.decode('utf8'));print(json.dumps(r));sys.exit(p.returncode)
