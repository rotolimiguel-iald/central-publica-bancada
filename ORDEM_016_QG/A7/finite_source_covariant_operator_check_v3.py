"""Move the actual flat source harmonic contacts to covariant ghost jets.

Adds the measured explicit first-K contact. No scalar momentum substitution
is used to commute third covariant derivatives.
"""
from pathlib import Path
from datetime import datetime,timezone
from itertools import permutations
import hashlib,json,time,uuid
import sympy as s
import curved_source_jet_engine as e
from finite_harmonic_extension_engine_v2 import represent,Q
H=Path(__file__).resolve().parent;D=H/'finite_source_covariant_operator_v3';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
    q=D/name;assert not q.exists(),q
    b=json.dumps(v,ensure_ascii=False,indent=2).encode();t=q.with_name(q.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(q)
sources=[Path(__file__),H/'finite_harmonic_extension_engine_v2.py',H/'curved_source_jet_engine.py',
    H/'covariant_source_operator_check.py',H/'finite_curved_source_harmonics_v2/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    supersedes_source_sha256=sha(H/'finite_source_covariant_operator_check_v2.py'),
    target='Finite source operator through firstK with original derivative ordering and actual harmonic-reference contacts',
    operation='delta derivatives act on source test then adjoint to ghost: A +symD3v, B +symD2Dkv; no repeated Taylor factors',
    ansatz='a G(Boxv)+b Hess(divv)+c gBoxdivv+K[d G(v)+e gdivv]',
    fits='3flat structures and2curved structures; dense nonaxis holdout',
    sources=[dict(path=str(q),sha256=sha(q)) for q in sources],full_Q2=False))
cpu=time.process_time();axes=[s.eye(4)[:,i] for i in range(4)];checks=[];details=[]
def ck(n,x):assert s.expand(x)==0,(n,x);checks.append(n)
def gamma(r,j,k,i):return -(e.d(r,k)*e.d(j,i)+e.d(r,j)*e.d(k,i)-2*e.d(j,k)*e.d(r,i))/3
def d3(r,i,j,k,p,v):
    flat=-p[i]*p[j]*p[k]*v[r]
    curved=sum(gamma(r,k,b,j)*p[i]*v[b]+gamma(r,k,b,i)*p[j]*v[b]
       +gamma(r,j,b,i)*p[k]*v[b]-gamma(b,j,k,i)*p[b]*v[r] for b in range(4))
    return (flat,curved)
def contact_to_jet(poly,r,p,v,inner=()):
    out=[0,0]
    if poly==0:return out
    for powers,c in s.Poly(poly,*Q).terms():
        word=tuple(i for i,n in enumerate(powers) for _ in range(n))
        assert len(word)+len(inner)==3
        words=set(permutations(word))
        for w in words:
            j=d3(r,*(w+inner),p,v)
            for o in range(2):out[o]+=c*j[o]/len(words)
    return out

def adjoint(T,p,v):
    out=[0,0];fourier=0
    for r in range(4):
        ka,_=e.kernel(T,axes[r],axes[0],0)
        _,ca=represent(ka)
        aa=contact_to_jet(ca,r,p,v)
        for o in range(2):out[o]+=aa[o]
        fourier-=v[r]*ca.subs(dict(zip(Q,p)))
        for k in range(4):
            _,kb=e.kernel(T,axes[r],axes[k],0)
            _,cb=represent(kb)
            bb=contact_to_jet(cb,r,p,v,(k,))
            for o in range(2):out[o]+=bb[o]
            fourier-=v[r]*p[k]*cb.subs(dict(zip(Q,p)))
    out=list(map(s.expand,out))
    ck('Fourier_sign_'+str(len(details)),out[0]-fourier)
    return out

def candidate_basis(T,p,v):
    vals=[[0,0] for _ in range(3)]
    for a in range(4):
        for b in range(4):
            if not T[a,b]:continue
            for i in range(4):
                aa=d3(b,a,i,i,p,v);bb=d3(a,b,i,i,p,v);cc=d3(i,a,b,i,p,v)
                for o in range(2):
                    vals[0][o]+=T[a,b]*(aa[o]+bb[o])
                    vals[1][o]+=T[a,b]*cc[o]
    for i in range(4):
        for j in range(4):
            aa=d3(j,i,i,j,p,v)
            for o in range(2):vals[2][o]+=s.trace(T)*aa[o]
    return vals

curve=json.loads((H/'finite_curved_source_harmonics_v2/results.json').read_bytes())
ca,cb=map(s.Rational,curve['A_contact_coefficients'])
def explicit(T,p,v):return ca*(v.T*T*p)[0]+cb*s.trace(T)*p.dot(v)

p=axes[0];fit=[]
for a,b,v in [(0,1,axes[1]),(1,1,axes[0]),(0,0,axes[0])]:
    T=s.zeros(4);T[a,b]=T[b,a]=1
    out=adjoint(T,p,v);basis=candidate_basis(T,p,v)
    fit.append((T,v,out,basis))
    details.append(dict(fiber=[a,b],v=list(v),adjoint=list(map(str,out)),explicitK=str(explicit(T,p,v))))
    print(json.dumps(dict(fiber=[a,b],adjoint=list(map(str,out)),cpu=time.process_time()-cpu)),flush=True)
matrix=s.Matrix([[q[0] for q in row[3]] for row in fit])
abc=list(matrix.inv()*s.Matrix([row[2][0] for row in fit]))
rows=[];values=[]
for T,v,out,basis in fit:
    ck('flat_reconstruction',sum(c*q[0] for c,q in zip(abc,basis))-out[0])
    rows.append([2*(v.T*T*p)[0],s.trace(T)*p.dot(v)])
    values.append(out[1]+explicit(T,p,v)-sum(c*q[1] for c,q in zip(abc,basis)))
de,params=s.Matrix(rows).gauss_jordan_solve(s.Matrix(values));assert not len(params)
for x,y in zip(s.Matrix(rows)*de,values):ck('curvature_fit',x-y)
T=s.Matrix([[1,2,0,-1],[2,3,1,0],[0,1,-2,1],[-1,0,1,4]])
p=s.Matrix([1,2,-1,1]);v=s.Matrix([2,-1,1,3])
out=adjoint(T,p,v);basis=candidate_basis(T,p,v)
ck('dense_flat',out[0]-sum(c*q[0] for c,q in zip(abc,basis)))
ck('dense_curved',out[1]+explicit(T,p,v)-sum(c*q[1] for c,q in zip(abc,basis))
   -de[0]*2*(v.T*T*p)[0]-de[1]*s.trace(T)*p.dot(v))
result=dict(at=datetime.now(timezone.utc).isoformat(),status='FINITE_SOURCE_COVARIANT_OPERATOR_FIRST_K',
    checks=len(checks),check_names=checks,flat_coefficients=list(map(str,abc)),
    curved_coefficients=list(map(str,de)),fit_details=[{**row,'v':list(map(str,row['v']))} for row in details],
    formula='DeltaR/C=a G(Boxv)+b Hess(divv)+c gBox(divv)+K[dG(v)+e gdivv]',
    nongauge_scalar='c Box(divv)+e K divv; E(gf)=-2Hessf+2gBoxf+6Kgf',
    cpu_seconds=time.process_time()-cpu,full_Q2=False,smooth_W_included=False,
    differential_reference='Actual pair harmonic reference; not asserted BRST invariant')
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(q),sha256=sha(q)) for q in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k not in ('fit_details','check_names')},ensure_ascii=False))
