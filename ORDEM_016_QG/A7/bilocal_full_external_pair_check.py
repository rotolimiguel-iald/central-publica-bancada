"""Recover all O(4) first external jets and integrate the X derivative too."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,time,uuid
import sympy as s
import bilocal_ghost_external_jets as G
import bilocal_metric_external_jets as M
H=Path(__file__).resolve().parent;D=H/'bilocal_full_external_pair';D.mkdir(exist_ok=True)
L=s.Symbol('L');n=(1,0,0,0)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
    p=D/name;assert not p.exists(),p;b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'bilocal_ghost_external_jets.py',H/'bilocal_metric_external_jets.py',
 H/'bilocal_covariant_jet_engine.py',H/'bilocal_first_curvature_engine.py',H/'bilocal_external_jets_generation.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Full hX and DhX coefficient basis; divergenceX through firstK',
 rank3_basis=['delta_ab xr','delta_ar xb+delta_br xa','xa xb xr'],
 rank4_basis=['delta_ir delta_ab','delta_ia delta_br+delta_ib delta_ar',
 'delta_ab xi xr','delta_ir xa xb','delta_ia xb xr+delta_ib xa xr',
 'delta_ar xi xb+delta_br xi xa','xi xa xb xr'],
 homogeneity_C1=[-8,-6],point=n,
 scope='Rotational covariance and homogeneity reconstruction, off diagonal; contacts/source separate',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources],full_Q2=False))
cpu=time.process_time();count=0;records={};basis={}
def sym(pair):return s.Rational(pair[0])+s.Rational(pair[1])*L
def d(a,b):return s.Integer(a==b)
def f4(c,i,a,b,r):
    terms=[d(i,r)*d(a,b),d(i,a)*d(b,r)+d(i,b)*d(a,r),d(a,b)*n[i]*n[r],
      d(i,r)*n[a]*n[b],d(i,a)*n[b]*n[r]+d(i,b)*n[a]*n[r],
      d(a,r)*n[i]*n[b]+d(b,r)*n[i]*n[a],n[i]*n[a]*n[b]*n[r]]
    return s.expand(sum(t*v for t,v in zip(terms,c)))
def f3(c,a,b,r):return s.expand(c[0]*d(a,b)*n[r]+c[1]*(d(a,r)*n[b]+d(b,r)*n[a])+c[2]*n[a]*n[b]*n[r])
def omega(a,c,i):return (s.Integer(n[a])*d(i,c)-d(i,a)*n[c])/2
def divergence(c,o,a,b,r):
    get=lambda i,aa,bb,rr:f4(c[o],i,aa,bb,rr)
    A=get(0,a,b,r)
    val=(-8+2*o)*A+2*s.diff(A,L)
    def tangential(co):
        g=lambda i,aa,bb,rr:f4(co,i,aa,bb,rr)
        return sum(g(0,a,b,r)+d(a,j)*g(j,0,b,r)-d(a,0)*g(j,j,b,r)
          +d(b,j)*g(j,a,0,r)-d(b,0)*g(j,a,j,r)
          +d(r,j)*g(j,a,b,0)-d(r,0)*g(j,a,b,j) for j in (1,2,3))
    val+=tangential(c[o])
    if o:
        val+=tangential(c[0])/6
        val+=sum(omega(i,t,i)*f4(c[0],t,a,b,r)+omega(a,t,i)*f4(c[0],i,t,b,r)
                 +omega(b,t,i)*f4(c[0],i,a,t,r) for i in range(4) for t in range(4))
    return s.expand(val)
for name,mod,cls in [('ghost',G,G.PointJets),('metric',M,M.MetricPointJets)]:
    J=cls(n);cache={}
    def run(der,a,b):
        global count
        a,b=sorted((a,b));key=(der,a,b)
        if key not in cache:
            fn=mod.ghost_ward_point if name=='ghost' else mod.metric_ward_point
            values,_=fn(n,mod.tensor(a,b),jets=J,derivative_index=der)
            for rows in values:
                for row in rows:
                    for value in row:assert isinstance(value,F),(name,key,value,type(value));count+=1
            cache[key]=values
            put(name+'_jet_'+str(der)+'_'+str(a)+str(b)+'.json',dict(
                derivative_index=der,a=a,b=b,values=[[[str(v) for v in p] for p in row] for row in values],
                cpu_cumulative=time.process_time()-cpu))
            print('JET',name,key,'cpu',time.process_time()-cpu,flush=True)
        mult=1 if a==b else 2
        return [[sym(pair)/mult for pair in rows] for rows in cache[key]]
    def value(der,a,b,r,o):return run(der,a,b)[o][r]
    c0=[];c1=[]
    for o in (0,1):
        A=value(None,1,1,0,o);B=value(None,0,1,1,o);C=value(None,0,0,0,o)-A-2*B
        c0.append([A,B,C])
        u=value(1,2,2,1,o);v=value(1,1,2,2,o)
        w=value(0,1,1,0,o)-u;t=value(1,0,0,1,o)-u
        e=value(1,1,0,0,o)-v;f=value(0,1,0,1,o)-v
        g=value(0,0,0,0,o)-u-2*v-w-t-2*e-2*f
        c1.append([u,v,w,t,e,f,g])
    # The unused ghost-output components at the same anchor are held-out checks
    # on the tensor basis; not independent checks at nonaxial points.
    for (der,a,b),vals in cache.items():
        for o in (0,1):
            for r in range(4):
                actual=sym(vals[o][r])/(1 if a==b else 2)
                expect=f3(c0[o],a,b,r) if der is None else f4(c1[o],der,a,b,r)
                assert s.expand(actual-expect)==0,(name,der,a,b,r,o,actual,expect);count+=1
    strong=[]
    for o in (0,1):
        vals=[s.expand(f3(c0[o],a,b,r)-divergence(c1,o,a,b,r)) for a,b,r in [(1,1,0),(0,1,1),(0,0,0)]]
        strong.append(vals)
    basis[name]=dict(C0=[[str(v) for v in row] for row in c0],C1=[[str(v) for v in row] for row in c1],
                     strong_samples=[[str(v) for v in row] for row in strong])
    put(name+'_basis.json',basis[name])
    print('STRONG',name,basis[name]['strong_samples'],'cpu',time.process_time()-cpu,flush=True)
combined=[[str(s.expand(s.sympify(basis['ghost']['strong_samples'][o][j])-s.sympify(basis['metric']['strong_samples'][o][j])/2)) for j in range(3)] for o in (0,1)]
result=dict(at=datetime.now(timezone.utc).isoformat(),status='BILOCAL_FULL_FIRST_EXTERNAL_JET_CANDIDATE',
 checks=count,cpu_seconds=time.process_time()-cpu,coefficients=basis,
 combined_strong_samples=combined,sample_components=['110','011','000'],
 angular_divergence_independently_verified=False,full_Q2=False,source=False,contacts=False,
 scope='All seven O4 DhX tensors and three hX tensors reconstructed; anchor checks only; exact frame-divergence candidate')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json',D/'ghost_basis.json',D/'metric_basis.json']]))
print(json.dumps(result))
