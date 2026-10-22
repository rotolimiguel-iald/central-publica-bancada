"""Symbolic mixed ghost derivative comparison; upper X index matters."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
import curved_source_jet_engine as E
H=Path(__file__).resolve().parent;D=H/'ghost_mixed_parametrix_frame_v2';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'curved_source_jet_engine.py',H/'ghost_direct_position_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),target='Mixed ghost jets source/pair, symbolic in every x',
 method='Covariant X derivative with PLUS connection on upper X vector; coframe on vector, inverse coframe on derivative',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();x=E.x;z=E.z
def d(a,b):return s.Integer(a==b)
def gamma(c,a,b):return -(d(c,b)*x[a]+d(c,a)*x[b]-2*d(a,b)*x[c])/3
def frame(a,b):return (z*d(a,b)-x[a]*x[b])/6
def omega(i,j,a,b):return d(a,i)*d(b,j)-d(a,j)*d(b,i)
def A(i,a,b):return sum(x[j]*omega(j,i,a,b) for j in range(4))
fails=[];checks=0
for i in range(4):
    for j in range(4):
        for a in range(4):
            for b in range(4):
                left=E.gjet(1,a,b,j,i)
                for c in range(4):
                    left+=gamma(a,i,c)*E.gjet(0,c,b,j)
                    left+=frame(i,c)*E.gjet(0,a,b,j,c)-frame(a,c)*E.gjet(0,c,b,j,i)
                N=z*d(i,j)-x[i]*x[j]
                right=(4*N*d(a,b)+6*z*omega(i,j,a,b)-12*x[i]*A(j,a,b)+12*x[j]*A(i,a,b)+30*(d(i,j)*z-2*x[i]*x[j])*d(a,b))/(12*z*z)
                residual=s.factor(s.cancel(s.expand(left-right).subs(z,sum(q*q for q in x))))
                checks+=1
                if residual!=0:fails.append(dict(indices=[i,j,a,b],residual=str(residual)))
result=dict(at=datetime.now(timezone.utc).isoformat(),status='GHOST_MIXED_SYMBOLIC_MATCH' if not fails else 'GHOST_MIXED_SYMBOLIC_MISMATCH',checks=checks,failures=fails,cpu_seconds=time.process_time()-cpu,full_Q2=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({**{k:v for k,v in result.items() if k!='failures'},'failure_count':len(fails),'first_failures':fails[:3]}))
