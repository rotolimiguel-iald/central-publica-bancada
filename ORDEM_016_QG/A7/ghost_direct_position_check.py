"""Compare direct nonminimal ghost loops with minimalized determinant result."""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time
import hashlib,json
import sympy as s
from ghost_direct_position_engine import *
H=Path(__file__).resolve().parent;D=H/'ghost_direct_position';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,indent=2).encode();assert not p.exists()
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),engine_sha256=sha(H/'ghost_direct_position_engine.py'),
    target='Direct first-K ghost bubble versus heat factorization; flat normalization controls; no imposed equality',full_Q2=False))
cpu=process_time();nodes=json.loads((H/'angular_cubature/results.json').read_bytes())['nodes'];rows=[];values=[]
p=(1,0,0,0)
for a,b in [(4,7),(4,4),(0,4),(4,0),(1,1),(0,0)]:
    sums=[[F(),F()],[F(),F()]]
    for node in nodes:
        for o in (0,1):
            v=direct_node(BASIS[a],BASIS[b],p,tuple(node['vector']),o)
            for j in range(2):sums[o][j]+=F(node['weight'])*v[j]
    A=s.Matrix(4,4,BASIS[a]);B=s.Matrix(4,4,BASIS[b]);q=s.Matrix(p)
    iv=[s.trace(A*B),s.trace(A)*s.trace(B),(q.T*A*q)[0]*s.trace(B),(q.T*B*q)[0]*s.trace(A),(q.T*A*B*q)[0]]
    # Flat pAp*pBp independent sixth invariant; evaluate old flat table directly.
    pa=(q.T*A*q)[0];pb=(q.T*B*q)[0]
    flat=s.Rational(1,12)*iv[0]+s.Rational(7,48)*iv[1]-s.Rational(1,8)*(iv[2]+iv[3])-s.Rational(1,12)*iv[4]+s.Rational(1,6)*pa*pb
    rows.append(iv);values.append(dict(pair=[a,b],flat=str(sums[0][0]),flat_reference=str(flat),K=str(sums[1][0]),log=str(sums[1][1])))
    print(json.dumps(values[-1]),flush=True)
fit,params=s.Matrix(rows).gauss_jordan_solve(s.Matrix([v['K'] for v in values]));assert len(params)==0
previous=list(map(s.Rational,json.loads((H/'first_curvature_total_hessian/results.json').read_bytes())['ghost']))
fresh(D/'results.json',dict(statute='MEASURE_DIRECT_NONMINIMAL_GHOST_LOG',values=values,coefficients=list(map(str,fit)),
    previous=list(map(str,previous)),difference=[str(a-b) for a,b in zip(fit,previous)],
    flat_matches=all(s.Rational(v['flat'])==s.Rational(v['flat_reference']) for v in values),
    cpu_seconds=process_time()-cpu,full_Q2=False))
files=[Path(__file__),H/'ghost_direct_position_engine.py',D/'PRE_REGISTER.json',D/'results.json']
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps(dict(coefficients=list(map(str,fit)),difference=[str(a-b) for a,b in zip(fit,previous)],cpu=process_time()-cpu)))
