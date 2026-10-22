"""Verify Einstein on whole first-K RNC polynomials before use under a kernel."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time,uuid
import sympy as s
from einstein_test_field_engine import *
H=Path(__file__).resolve().parent;D=H/'einstein_test_field';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'einstein_test_field_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),target='Einstein on full firstK RNC test field, with metric and all connection slots',
    checks='flat matrix symbol; EG=0 for polynomial covector; density transport; whole polynomial identities, not only origin',
    sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();checks=[]
def ck(name,a):assert ex(a)==0,(name,ex(a));checks.append(name)
p=s.Matrix([1,2,-1,1]);q=-s.I*p;v=s.Matrix([2,-1,1,3]);X=s.Matrix(x)
T=s.Matrix([[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]])
E=einstein(parallel_tensor(T),q)
expected=p.dot(p)*T-p*(T*p).T-(T*p)*p.T+p*p.T*s.trace(T)+I*((p.T*T*p)[0]-p.dot(p)*s.trace(T))
for a in range(4):
    for b in range(4):ck(f'flat_{a}_{b}',E[0][a,b]-expected[a,b])
V=[v,(-(Z*I-X*X.T)*v/6).applyfunc(ex)]
eg=einstein(gauge(V,q),q)
for o in (0,1):
    for a in range(4):
        for b in range(4):ck(f'gauge_{o}_{a}_{b}',eg[o][a,b])
density_T=density(parallel_tensor(T));target=-Z*T/6-(X*X.T*T+T*X*X.T)/6
for a in range(4):
    for b in range(4):ck(f'density_{a}_{b}',density_T[1][a,b]-target[a,b])
result=dict(at=datetime.now(timezone.utc).isoformat(),status='FULL_TEST_FIELD_EINSTEIN_FIRSTK_VERIFIED',checks=len(checks),check_names=checks,cpu_seconds=time.process_time()-cpu,full_Q2=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='check_names'}))
