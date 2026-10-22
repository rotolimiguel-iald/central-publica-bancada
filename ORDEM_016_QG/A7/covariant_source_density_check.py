"""Transport external source density before interpreting the first-K profile."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time
import sympy as s
import curved_source_jet_engine as e
H=Path(__file__).resolve().parent;O=H/'covariant_source_density';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=O/n;assert not p.exists(),p;b=json.dumps(v,ensure_ascii=False,indent=2).encode()
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    engine_sha256=sha(H/'curved_source_jet_engine.py'),
    formula='density T(X)=sqrt(gX) P(X,Y) t(X in parallel frame) P(X,Y)^t; coefficient K: -z*t/6-(xx*t+t*xx)/6',
    goals=['Include the density and index transport missing from direct coordinate polarization profile',
        'Retain terms with derivative on the external ghost separately before integration by parts',
        'Verify fit on a nonaxial polarization'],
    exclusion='Do not call the sum a covariant differential operator after suppressing derivative ordering'))
start=time.process_time();I=s.eye(4);X=s.Matrix(e.x);axes=[I[:,i] for i in range(4)];p=axes[0]
fits=[]
for a,b,v in [(0,1,axes[1]),(1,1,axes[0]),(0,0,axes[0])]:
    T=s.zeros(4);T[a,b]=T[b,a]=1;fits.append((T,v))
rows=[];vals=[];split=[]
for T,v in fits:
    # P1=(Iz-xx)/6 and density1=-z/2 imply exactly this correction.
    P1=(I*e.z-X*X.T)/6
    correction=s.simplify(P1*T+T*P1.T-e.z*T/2)
    assert all(s.expand(t)==0 for t in correction+e.z*T/6+(X*X.T*T+T*X*X.T)/6)
    px=sum(p[i]*e.x[i] for i in range(4))
    a,b=e.kernel(T,v,p,1);c,d=e.kernel(correction,v,p,0)
    pieces=[e.average(-a*px),e.average(b),e.average(-c*px),e.average(d)]
    split.append(list(map(str,pieces)));vals.append(s.expand(sum(pieces)))
    rows.append([2*(v.T*T*p)[0],s.trace(T)*p.dot(v)])
M=s.Matrix(rows);fit=M.gauss_jordan_solve(s.Matrix(vals))[0]
assert M*fit==s.Matrix(vals)
T=s.Matrix([[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]])
p=s.Matrix([1,2,-1,1]);v=s.Matrix([2,-1,1,3]);px=sum(p[i]*e.x[i] for i in range(4))
correction=-e.z*T/6-(X*X.T*T+T*X*X.T)/6
a,b=e.kernel(T,v,p,1);c,d=e.kernel(correction,v,p,0)
got=e.average(-(a+c)*px+b+d)
assert s.expand(got-(fit[0]*2*(v.T*T*p)[0]+fit[1]*s.trace(T)*p.dot(v)))==0
result=dict(status='COVARIANT_SOURCE_DENSITY_JETS_INCLUDED',
    fit_basis=['2(v.T.p)','tr(T)(p.v)'],coefficients=list(map(str,fit)),
    fit_values=list(map(str,vals)),split_order=['curved_v','curved_dv','density_transport_v','density_transport_dv'],
    split_values=split,nonaxis_value=str(got),cpu_seconds=time.process_time()-start,
    derivative_ordering_retained_in_engine=True,
    covariant_operator_identified=False,finite_Ward_coefficient=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
 [Path(__file__),O/'PRE_REGISTER.json',O/'results.json',H/'curved_source_jet_engine.py']]))
print(json.dumps(result,ensure_ascii=False))
