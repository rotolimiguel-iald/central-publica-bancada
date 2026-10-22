"""Transport ordered source derivatives to an explicit covariant ghost operator."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
import json,hashlib,time,itertools
import sympy as s
import curved_source_jet_engine as e
H=Path(__file__).resolve().parent;O=H/'covariant_source_operator';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    q=O/n;assert not q.exists(),q;b=json.dumps(v,ensure_ascii=False,indent=2).encode()
    t=q.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(q)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    sources=[dict(path=str(q),sha256=sha(q)) for q in
       [H/'curved_source_jet_engine.py',H/'covariant_source_density/derivative_placements.json']],
    scope='Universal logarithmic source-bubble local functional to first K; auxiliary Euclidean convention',
    operation='A source third derivatives adjoint -D_(ijk)v; B source second derivatives adjoint +D_(ij)D_k v; preserve ordering',
    candidate='3/8 K_gauge(Box v) -1/2 Hess(div v) + K[d K_gauge(v)+e g div(v)]',
    acceptance='Flat symbol matches, source adjoint and candidate evaluated with normal-coordinate connection jets, independent nonaxis',
    excluded=['finite causal anomaly','higher K orders','full graph hierarchy','gate change']))
t=time.process_time();axes=[s.eye(4)[:,i] for i in range(4)];checks=[]
def ck(n,v):assert s.expand(v)==0,(n,v);checks.append(n)
def gamma(r,j,k,i):
    return -(e.d(r,k)*e.d(j,i)+e.d(r,j)*e.d(k,i)-2*e.d(j,k)*e.d(r,i))/3
def d3(r,i,j,k,p,v):
    flat=-p[i]*p[j]*p[k]*v[r]
    curved=sum(gamma(r,k,b,j)*p[i]*v[b]+gamma(r,k,b,i)*p[j]*v[b]
       +gamma(r,j,b,i)*p[k]*v[b]-gamma(b,j,k,i)*p[b]*v[r] for b in range(4))
    return flat,curved
def terms(f):return s.Poly(s.expand(f.subs(e.z,1)),*e.x).terms()
def moment(ts,indices):
    add=tuple(indices.count(i) for i in range(4))
    return sum(c*e.spherical_moment(tuple(a+b for a,b in zip(powers,add))) for powers,c in ts)
def source_adjoint(T,p,v):
    out=[s.Integer(0),s.Integer(0)]
    for r in range(4):
        a,_=e.kernel(T,axes[r],axes[0],0);at=terms(a)
        for i,j,k in itertools.product(range(4),repeat=3):
            q=moment(at,(i,j,k))
            if q:
                ds=d3(r,i,j,k,p,v)
                for n in range(2):out[n]-=q*ds[n]/6
        for k in range(4):
            _,b=e.kernel(T,axes[r],axes[k],0);bt=terms(b)
            for i,j in itertools.product(range(4),repeat=2):
                q=moment(bt,(i,j))
                if q:
                    ds=d3(r,i,j,k,p,v)
                    for n in range(2):out[n]+=q*ds[n]/2
    return list(map(s.expand,out))
def candidate(T,p,v):
    ans=[0,0]
    for a in range(4):
     for b in range(4):
      if not T[a,b]:continue
      for i in range(4):
       aa=d3(b,a,i,i,p,v);bb=d3(a,b,i,i,p,v);cc=d3(i,a,b,i,p,v)
       for n in range(2):ans[n]+=T[a,b]*(s.Rational(3,8)*(aa[n]+bb[n])-cc[n]/2)
    return list(map(s.expand,ans))
def explicitK(T,p,v):return -s.Rational(23,6)*(v.T*T*p)[0]+s.Rational(13,12)*s.trace(T)*p.dot(v)
fits=[];p=axes[0]
for a,b,v in [(0,1,axes[1]),(1,1,axes[0]),(0,0,axes[0])]:
    T=s.zeros(4);T[a,b]=T[b,a]=1;fits.append((T,v))
rows=[];values=[];details=[]
for n,(T,v) in enumerate(fits):
    adj=source_adjoint(T,p,v);cand=candidate(T,p,v)
    expected=-s.Rational(3,4)*p.dot(p)*(v.T*T*p)[0]+s.Rational(1,2)*(p.T*T*p)[0]*p.dot(v)
    ck(f'flat_adjoint_{n}',adj[0]-expected);ck(f'flat_candidate_{n}',cand[0]-expected)
    total=s.expand(adj[1]+explicitK(T,p,v));diff=s.expand(total-cand[1])
    rows.append([2*(v.T*T*p)[0],s.trace(T)*p.dot(v)]);values.append(diff)
    details.append(dict(adjoint_curvature=str(adj[1]),explicit_curvature=str(explicitK(T,p,v)),
         total_curvature=str(total),candidate_curvature=str(cand[1]),difference=str(diff)))
    print(json.dumps({'fit':n,**details[-1]}),flush=True)
M=s.Matrix(rows);coefs=M.gauss_jordan_solve(s.Matrix(values))[0]
for n in range(3):ck(f'fit_residual_{n}',(M*coefs)[n]-values[n])
T=s.Matrix([[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]])
p=s.Matrix([1,2,-1,1]);v=s.Matrix([2,-1,1,3]);adj=source_adjoint(T,p,v);cand=candidate(T,p,v)
ck('nonaxis_flat',adj[0]-cand[0])
ck('nonaxis_curvature',adj[1]+explicitK(T,p,v)-cand[1]-coefs[0]*2*(v.T*T*p)[0]-coefs[1]*s.trace(T)*p.dot(v))
# The scalar div(v) has commuting Hessian, an independent convention control.
for a in range(4):
 for b in range(4):
    ck(f'div_scalar_hessian_commutes_{a}_{b}',sum(d3(i,a,b,i,p,v)[1]-d3(i,b,a,i,p,v)[1] for i in range(4)))
result=dict(status='COVARIANT_UNIVERSAL_LOG_SOURCE_OPERATOR_FIRST_K',checks=len(checks),check_names=checks,
    formula='R(v)=3/8 K_gauge(Box v)-1/2 Hess(div v)+K[d K_gauge(v)+e g div(v)]+O(K^2)',
    curvature_coefficients=list(map(str,coefs)),fit_details=details,
    cpu_seconds=time.process_time()-t,finite_Ward_anomaly=False,cutoff_derivatives_included=False,
    global_factors='A0,source phase,4kappa,ghost inverse and Wick weights remain as previously separated')
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(q),sha256=sha(q)) for q in
 [Path(__file__),O/'PRE_REGISTER.json',O/'results.json',H/'curved_source_jet_engine.py',H/'covariant_source_density/derivative_placements.json']]))
print(json.dumps({k:v for k,v in result.items() if k not in ('check_names','fit_details')},ensure_ascii=False),flush=True)
