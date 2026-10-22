"""Dispatch audit events synthetically: this script performs no socket I/O."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time

B=Path(__file__).resolve().parent
def pin(p):
    p=Path(p);r=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(r).hexdigest(),'bytes':len(r)}
code=r'''
from pathlib import Path
import importlib.util,json,os,sys
p=Path(os.environ['TEST_GUARD_SOURCE'])
s=importlib.util.spec_from_file_location('guard_under_review',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
checks=[]
for name,args in [('socket.connect',(None,('127.0.0.1',9))),('socket.sendto',(None,('127.0.0.1',9))),('socket.sendmsg',(None,('127.0.0.1',9))),('socket.getnameinfo',(('127.0.0.1',9),0))]:
 refused=False
 try:sys.audit(name,*args)
 except PermissionError:refused=True
 checks.append({'audit_event':name,'refused':refused})
print(json.dumps(checks))
'''
results=[]
for version,path in [('R3',B/'sitecustomize_rite_r3.py'),('R4',B/'replay_r4_sentinel/sitecustomize_rite_r4.py')]:
    root=B/('synthetic_events_'+version);root.mkdir(exist_ok=False)
    env=dict(os.environ,TGL_RITE_SANDBOX=str(root),TGL_RITE_GUARD_PHASE='preflight',TGL_LAKE=r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lake.exe',TEST_GUARD_SOURCE=str(path),PYTHONDONTWRITEBYTECODE='1')
    t=time.perf_counter();start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    command=[sys.executable,'-B','-X','utf8','-c',code]
    p=subprocess.run(command,cwd=root,env=env,capture_output=True,text=True,encoding='utf-8',timeout=30)
    assert p.returncode==0,(p.stdout,p.stderr)
    checks=json.loads(p.stdout)
    results.append({'version':version,'source':pin(path),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-t,'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'checks':checks})
assert [x['refused'] for x in results[0]['checks']]==[True,False,False,False]
assert all(x['refused'] for x in results[1]['checks'])
out={'schema':'guard-audit-events-independent/v1','unit':'F1.FECHO_20261015','claim_event':845,'actual_network_calls':0,'scientific_program_executed':False,'results':results,'finding':'R3 did not refuse sendto/sendmsg/getnameinfo synthetic audit events; R4 refuses all three. These are event dispatch probes, not network transmissions.','script':pin(__file__)}
f=B/'NETWORK_EVENT_PROBE_R1.json'
with f.open('x',encoding='utf-8') as h:json.dump(out,h,ensure_ascii=False,indent=2)
print(json.dumps(pin(f)))
