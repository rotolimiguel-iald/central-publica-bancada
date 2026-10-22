"""An explicit quadratic local primitive for the measured h-c log component.

This is a restricted cohomological statement, not the full nonlinear
Epstein-Glaser anomaly, and no representative is adopted in the prescription.
"""
from pathlib import Path
from datetime import datetime,timezone
from time import process_time
from fractions import Fraction as F
import hashlib,json
import sympy as s
from oneform_second_curvature_engine_v2 import oneform_second,loop_gauge
H=Path(__file__).resolve().parent;D=H/'local_quadratic_ward_primitive';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,v):
    b=json.dumps(v,indent=2).encode();assert not p.exists()
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
fresh(D/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    target='Extend the existing firstK quadratic counterterm family through K2, with fixed measured linear tadpole; never choose a representative',full_Q2=False))
cpu=process_time();checks=0
def check(a,b=0):
    global checks
    assert s.expand(a-b)==0,(a,b);checks+=1
def read(p):return json.loads((H/p).read_bytes())
r1=list(map(s.Rational,read('first_curvature_ward_audit/results.json')['sum_coefficients']))
r2=list(map(s.Rational,read('linear_curvature_tadpole/results.json')['ward_after']))
t=s.Symbol('t',real=True);d1,d2,d3=s.symbols('d1 d2 d3');d4=t
sol=s.solve([d1+d4/2+r1[0],2*d3+d4+r1[1],2*(d2+d3)+r1[2]],(d1,d2,d3),dict=True)[0]
first=[sol[d1],sol[d2],sol[d3],sol[d3],t];zero=[F(0)]*5
rows=[];vals=[];cache=[]
for p,v in [((1,0,0,0),(1,0,0,0)),((1,0,0,0),(0,1,0,0)),((1,2,-1,1),(2,-1,1,2))]:
    _,_,sym=oneform_second(v,p);actual=loop_gauge(sym,zero,first,[F(0)]*2,2);pv=sum(a*b for a,b in zip(p,v))
    for a in range(4):
        for b in range(4):rows.append([p[a]*v[b]+p[b]*v[a],int(a==b)*pv]);vals.append(actual[a][b])
    cache.append((p,v,sym));print(json.dumps(dict(case=len(cache),cpu=process_time()-cpu)),flush=True)
fit,params=s.Matrix(rows).gauss_jordan_solve(s.Matrix(vals));check(len(params),0)
second=[s.expand(-r2[0]-fit[0]),s.expand((-r2[1]-fit[1])/2)]
for p,v,sym in cache:
    p2=sum(x*x for x in p);pv=sum(a*b for a,b in zip(p,v))
    for order in (1,2):
        actual=loop_gauge(sym,zero,first,second,order)
        for a in range(4):
            for b in range(4):
                G=p[a]*v[b]+p[b]*v[a];g=int(a==b)
                residue=r1[0]*p2*G+r1[1]*p[a]*p[b]*pv+r1[2]*g*p2*pv if order==1 else r2[0]*G+r2[1]*g*pv
                check(actual[a][b]+residue)
fresh(D/'results.json',dict(statute='DERIVED_LOCAL_QUADRATIC_PRIMITIVE_FOR_MEASURED_HC_LOG_COMPONENT',checks=checks,
    parameter=str(t),first_K_Hessian=list(map(str,first)),induced_K2_gauge=list(map(str,fit)),second_K_Hessian=list(map(str,second)),
    primitive='B_t[h]=1/2 integral h . deltaH_t h; s0 B_t=integral h . deltaH_t Gc by formal selfadjointness',
    formal_selfadjoint_assumptions='Parallel invariant coefficients, real t, symmetrized two derivatives, symmetric fiber transpose, compact support',
    scope='Only measured ghost-one/field-one logarithmic density on spaceform; linear tadpole kept fixed; excludes cutoff currents and nonlinear descent',
    prescription_changed=False,representative_selected=False,full_Q2=False,cpu_seconds=process_time()-cpu))
files=[Path(__file__),H/'oneform_second_curvature_engine_v2.py',H/'linear_curvature_tadpole/results.json',H/'first_curvature_ward_audit/results.json',D/'PRE_REGISTER.json',D/'results.json']
fresh(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in files]))
print(json.dumps(dict(checks=checks,first=list(map(str,first)),induced=list(map(str,fit)),second=list(map(str,second)),cpu=process_time()-cpu)))
