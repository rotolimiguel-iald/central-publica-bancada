"""Independent connection-jet derivation and the non-gauge first-K remainder."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
import json,hashlib,time
import sympy as s
import ast
import curved_source_jet_engine as e
H=Path(__file__).resolve().parent;O=H/'covariant_source_operator_audit';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=O/n;assert not p.exists(),p;b=json.dumps(v,ensure_ascii=False,indent=2).encode()
    q=p.with_suffix('.tmp');q.write_bytes(b);assert q.read_bytes()==b;q.replace(p)
source=H/'covariant_source_operator_check.py'
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(source),
    targets=['All ordered third covariant derivatives using direct connection recursion',
             'Separate pure gauge from non-gauge first-curvature source operator'],
    scope='First K, auxiliary Euclidean operator and Einstein principal Hessian; no full Ward conclusion'))
# Extract just two pure definitions, never import the top-level check runner.
tree=ast.parse(source.read_text('utf-8'));nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('gamma','d3')]
assert len(nodes)==2;ns={'s':s,'e':e}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),ns)
t=time.process_time();checks=[]
def ck(n,v):assert s.expand(v)==0,(n,v);checks.append(n)
x=e.x;p=s.Matrix(s.symbols('p0:4'));v=s.Matrix(s.symbols('v0:4'));px=sum(p[i]*x[i] for i in range(4));zero=dict.fromkeys(x,0)
def G(r,j,b):return -(e.d(r,b)*x[j]+e.d(r,j)*x[b]-2*e.d(j,b)*x[r])/3
D1flat={(r,k):s.I*p[k]*v[r] for r in range(4) for k in range(4)}
D1K={(r,k):s.expand(sum(G(r,k,b)*v[b]*(1+s.I*px) for b in range(4))) for r in range(4) for k in range(4)}
for r in range(4):
 for j in range(4):
  for k in range(4):
    d2=s.expand(s.diff(D1K[r,k],x[j])+sum(G(r,j,b)*D1flat[b,k]-G(b,j,k)*D1flat[r,b] for b in range(4)))
    for i in range(4):ck(f'ordered_covariant_jet_{r}_{i}_{j}_{k}',s.diff(d2,x[i]).subs(zero)/s.I-ns['d3'](r,i,j,k,p,v)[1])
result=json.loads((H/'covariant_source_operator/results.json').read_bytes())
dcoef,ecoef=map(s.sympify,result['curvature_coefficients'])
ck('residual_trace_coefficient',ecoef-2)
# Gauge covariance of the full Einstein Hessian is an existing source identity.
# Its non-gauge first-K residual is computed with the principal Hessian only.
I=s.eye(4)
def itr(A):return A-I*s.trace(A)/2
def ein_pr(A):
    cp=A*p-p*s.trace(A)/2
    return s.expand(p.dot(p))*itr(A)-itr(p*cp.T+cp*p.T)
Rtrace=ecoef*I*p.dot(v)
ER=ein_pr(Rtrace)
expected=4*(p*p.T-I*p.dot(p))*p.dot(v)
for a in range(4):
 for b in range(4):ck(f'Einstein_of_nongauge_residual_{a}_{b}',ER[a,b]-expected[a,b])
witness=ER[1,1].subs(dict(zip(p,[1,0,0,0]))|dict(zip(v,[1,0,0,0])))
assert witness==-4
out=dict(status='ORDERED_JETS_PASS_NON_GAUGE_RESIDUAL_NONZERO',checks=len(checks),check_names=checks,
    decomposition='R=K_gauge(3/8 Box v -1/4 grad(div v) -37K/8 v)+2K g div(v)+O(K^2)',
    Einstein_nongauge_principal='4K (p tensor p -g p^2)(p.v), common Fourier i stripped',
    witness_E11_over_K=str(witness),cpu_seconds=time.process_time()-t,
    conclusion='Source log is no longer separately killed by the Einstein Hessian at first curvature; other loop sectors are required',
    full_Ward_anomaly=False)
put('results.json',out)
put('manifest.json',dict(artifacts=[dict(path=str(q),sha256=sha(q)) for q in
 [Path(__file__),source,O/'PRE_REGISTER.json',O/'results.json',H/'covariant_source_operator/results.json']]))
print(json.dumps({k:v for k,v in out.items() if k!='check_names'},ensure_ascii=False))
