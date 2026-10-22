"""Check radial Taylor jets against explicit coframe differentiation."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations_with_replacement,product
from time import process_time,perf_counter
from fractions import Fraction as F
import hashlib,json
import sympy as s
from radial_covariant_jet_engine import radial_jets
from ghost_covariant_word_engine import jet,matrix_unit
H=Path(__file__).resolve().parent;D=H/'radial_covariant_jet';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),code_sha256=sha(Path(__file__)),engine_sha256=sha(H/'radial_covariant_jet_engine.py'),
    claim='Fully symmetrized covariant jets of constant radial-frame plane waves have no first-curvature coefficient',full_Q2=False))
cpu,wall=process_time(),perf_counter();checks=[]
def check(n,a,b=0):assert a==b,(n,str(a),str(b));checks.append(n)
labels=list(combinations_with_replacement(range(4),2));p=(1,2,-1,1)
nonzero=0
for a,b in labels:
    A=matrix_unit(a,b);v,sy,outer=radial_jets(A,p)
    for n in (2,4):
        for w in combinations_with_replacement(range(4),n):
            for u,t in labels:
                check(f'sym_{a}{b}_{w}_{u}{t}',sy(w,u,t),0)
    for j in range(4):
        for w in combinations_with_replacement(range(4),3):
            for u,t in labels:
                if outer(j,w,u,t):nonzero+=1
check('nonvacuous_outer_jets',nonzero>0,True)
# Direct partial differentiation of the coframe correction for nonsymmetric words.
x=s.symbols('x0:4');z=sum(t*t for t in x);pv=sum(a*b for a,b in zip(p,x))
A=s.Matrix([[1,2,0,-1],[2,-1,1,0],[0,1,2,1],[-1,0,1,3]])
coframe=-(z*s.eye(4)-s.Matrix(x)*s.Matrix(x).T)/6
corr=(coframe*A+A*coframe.T)*(1+s.I*pv-pv**2/2)
v,_,_=radial_jets(A.tolist(),p);zero={t:0 for t in x}
for w in [(0,1),(2,2),(0,1,2,3),(0,0,1,1),(2,3,2,0)]:
    for a,b in labels:
        f=corr[a,b]
        for i in w:f=s.diff(f,x[i])
        check(f'direct_{w}_{a}{b}',s.Rational(v(w,a,b)-jet(w,a,b,A.tolist(),p,1)),s.simplify(f.subs(zero)))
fresh(D/'results.json',dict(statute='REAL_RADIAL_COVARIANT_TAYLOR_JETS',checks=len(checks),nonzero_outer_jets=nonzero,cpu_seconds=process_time()-cpu,wall_seconds=perf_counter()-wall,full_Q2=False))
fresh(D/'manifest.json',dict(files=[dict(path=str(f),sha256=sha(f)) for f in [Path(__file__),H/'radial_covariant_jet_engine.py',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=len(checks),nonzero_outer_jets=nonzero,cpu_seconds=process_time()-cpu)))
