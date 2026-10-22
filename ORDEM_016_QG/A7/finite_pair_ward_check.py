"""Direct gauge insertion into the finite pair kernels, not a commuting-symbol test."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
from itertools import combinations_with_replacement,permutations
from math import factorial
import hashlib,json,time,uuid
import sympy as s
from fractions import Fraction as F
from finite_metric_pair_engine_v2 import finite_node as metric_node
from finite_ghost_pair_engine_v2 import finite_node as ghost_node
from position_metric_ordered_operator_engine import external_jets
from position_metric_bubble_engine import BASIS,LABELS
from oneform_second_curvature_engine_v2 import oneform_second,einstein_gauge

H=Path(__file__).resolve().parent;D=H/'finite_pair_ward';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):
    p=D/name;assert not p.exists(),p
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)

@lru_cache(None)
def gauge_provider(v):
    @lru_cache(None)
    def provider(ignored,p,order,n,xi,yj):
        _,gauge,_=oneform_second(v,p);out=[]
        for w in combinations_with_replacement(range(4),n):
            words=set(permutations(w));vec=[]
            for a,b in LABELS:
                value=sum((gauge(((yj,) if yj>=0 else ())+q+((xi,) if xi>=0 else ()),a,b,order)
                           for q in words),F())/len(words)
                vec.append(value)
            if any(vec):
                den=1
                for i in set(w):den*=factorial(w.count(i))
                out.append((w,den,tuple(vec)))
        return out
    return provider

prior=json.loads((H/'finite_source_covariant_operator_v3/results.json').read_bytes())
aa,bb,cc=map(F,map(s.Rational,prior['flat_coefficients']))
dd,ee=map(F,map(s.Rational,prior['curved_coefficients']))
def source_einstein(T,v,p,o):
    jet,_,_=oneform_second(v,p)
    @lru_cache(None)
    def source(w,a,b,k):
        value=aa*sum(jet(w+(a,i,i),b,k)+jet(w+(b,i,i),a,k) for i in range(4))
        value+=bb*sum(jet(w+(a,b,i),i,k) for i in range(4))
        value+=int(a==b)*cc*sum(jet(w+(j,j,i),i,k) for i in range(4) for j in range(4))
        if k:
            value+=dd*(jet(w+(a,),b,k-1)+jet(w+(b,),a,k-1))
            value+=ee*int(a==b)*sum(jet(w+(i,),i,k-1) for i in range(4))
        return value
    return sum((T[4*a+b]*einstein_gauge(source,(),a,b,o) for a in range(4) for b in range(4)),F())

def invariant(T,v,p,o):
    t=s.Matrix(4,4,T);u=s.Matrix(v);q=s.Matrix(p);q2=q.dot(q)
    first=(q.T*t*u)[0];second=(q.T*t*q)[0]*q.dot(u);third=s.trace(t)*q.dot(u)
    if o==2:return [first,third]
    return [q2**(2-o)*first,q2**(1-o)*second,q2**(2-o)*third]

fixtures=[(1,(0,1,0,0)),(4,(1,0,0,0)),(0,(1,0,0,0))]
sources=[Path(__file__),H/'finite_metric_pair_engine_v2.py',H/'finite_ghost_pair_engine_v2.py',
    H/'oneform_second_curvature_engine_v2.py',H/'finite_source_covariant_operator_v3/results.json',
    H/'finite_pair_jet_inputs_manifest.json',H/'angular_cubature/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Finite metric+ghost local difference on exact covariant G(v), plus Einstein image of actual source difference',
    cases=fixtures,orders=[0,1,2],nonaxis=dict(order=1,T=4,v=[2,-1,1,3],p=[1,2,-1,1]),
    normalizations='-metric_raw/2+ghost_direct+E DeltaR, contact/C, common Fourier i stripped; relative factor1 from prior custody',
    exclusions=['finite tadpole','smooth W','nonlocal reference Ward amplitude','higher arities','full Q2'],
    sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();checks=[];p=(1,0,0,0)
for vi in range(4):
    v=tuple(int(i==vi) for i in range(4));provider=gauge_provider(v)
    gauge0=tuple(p[a]*v[b]+p[b]*v[a] for a in range(4) for b in range(4))
    for nx,xi in [(2,-1)]+[(1,i) for i in range(4)]:
        for ny,yj in [(2,-1)]+[(1,i) for i in range(4)]:
            n=nx+ny
            assert provider(BASIS[0],p,0,n,xi,yj)==external_jets(gauge0,p,0,n,xi,yj)
            checks.append('flat_gauge_jet')
nodes=json.loads((H/'angular_cubature/results.json').read_bytes())['nodes']
values=[]
def evaluate(Tidx,v,p,o):
    T=BASIS[Tidx];provider=gauge_provider(v);m=[F()]*4;g=[F()]*4
    for ni,node in enumerate(nodes):
        x=tuple(node['vector']);weight=F(node['weight'])
        mv=metric_node(BASIS[0],T,p,x,o,jet_provider=provider)
        gv=ghost_node(BASIS[0],T,p,x,o,jet_provider=provider)
        for i in range(4):m[i]+=weight*mv[i];g[i]+=weight*gv[i]
        if ni%64==0:print(json.dumps(dict(order=o,T=Tidx,v=v,node=ni,cpu=time.process_time()-cpu)),flush=True)
    es=source_einstein(T,v,p,o);loop=-sum(m)/2+sum(g);total=loop+es
    row=dict(order=o,T=Tidx,v=v,p=p,metric_pieces=list(map(str,m)),ghost_pieces=list(map(str,g)),
        loops=str(loop),Einstein_source=str(es),partial_sum=str(total))
    values.append(row);print(json.dumps(row),flush=True)
    return loop,es,total

fits={}
for o in range(3):
    rows=[];data=[]
    for ti,v in fixtures:
        got=evaluate(ti,v,p,o);rows.append(invariant(BASIS[ti],v,p,o));data.append(s.Rational(got[2]))
    matrix=s.Matrix(rows);coefs,params=matrix.gauss_jordan_solve(s.Matrix(data));assert not len(params)
    assert matrix*coefs==s.Matrix(data);checks.append('fit_'+str(o))
    fits[str(o)]=list(map(str,coefs))
np=(1,2,-1,1);nv=(2,-1,1,3);got=evaluate(4,nv,np,1)
expected=sum(c*q for c,q in zip(map(s.Rational,fits['1']),invariant(BASIS[4],nv,np,1)))
assert s.Rational(got[2])==expected,(got[2],expected)
checks.append('nonaxis_firstK')
result=dict(at=datetime.now(timezone.utc).isoformat(),status='PARTIAL_FINITE_WARD_DIFFERENCE_MEASURED',
    checks=len(checks),values=values,partial_Ward_coefficients=fits,
    bases=dict(flat=['p4 Tpv','p2 pTp pv','p4 trT pv'],firstK=['p2 Tpv','pTp pv','p2 trT pv'],secondK=['Tpv','trT pv']),
    cpu_seconds=time.process_time()-cpu,full_Q2=False,
    scope='Contact difference only; references have not been proved Ward preserving; smooth W and finite tadpole excluded',
    finite_tadpole_parameter='An independent tau K² trh contributes tau K²[G-gdiv], not fixed here')
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(q),sha256=sha(q)) for q in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='values'},ensure_ascii=False))
