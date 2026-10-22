"""Normalize localized matrix vertices against full EH density and Ward identity."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
from fractions import Fraction as F
from localized_eh_cubic_engine import localized_vertex_data,boundary_vertex_data,evaluate,AXES
from metric_boundary_current_engine import boundary_current,eh_boundary_vertex_raw
from metric_principal_vertices import eh_cubic_16k,eh_quadratic_8k,gauge_matrix,lie_matrix,clear_caches
from position_metric_bubble_engine import BASIS,vertex_data

H=Path(__file__).resolve().parent;D=H/'localized_eh_cubic';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
 p=D/name;assert not p.exists();b=json.dumps(v,indent=2).encode();tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
 tmp.write_bytes(b);assert tmp.read_bytes()==b;tmp.replace(p)
sources=[Path(__file__),H/'localized_eh_cubic_engine.py',H/'metric_boundary_current_engine.py',H/'metric_principal_vertices.py',H/'position_metric_bubble_engine.py',H/'flat_loop_cutoff/manifest.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),sources=[dict(path=str(p),sha256=sha(p)) for p in sources],
 target='Matrix realization of localized full cubic EH vertex with correct boundary sign',
 convention='raw=16k V3; total field momentum Q; cutoff Fourier momentum ell=-Q; boundary=-8ell.b3',full_Q2=False))
cpu=time.process_time();checks=0;controls=[];negative=[]
def eq(a,b):
 global checks
 assert a==b,(a,b);checks+=1
def add(*vs):return tuple(sum(x) for x in zip(*vs))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
momenta=[((1,2,-1,1),(2,-1,0,3),(0,1,1,0)),((0,1,0,-1),(1,0,2,1),(2,1,-1,0))]
for ia in [0,1,4,7]:
 A=BASIS[ia]
 for case,(p,q,r) in enumerate(momenta):
    total=add(p,q,r);ell=tuple(-v for v in total)
    V=localized_vertex_data(A,F(1),ell)
    BND=boundary_vertex_data(A,ell);bulk=vertex_data(A)
    for ib,ic in [(0,0),(0,4),(1,7),(2,5),(6,9)]:
      B,C=BASIS[ib],BASIS[ic]
      plain=eh_cubic_16k(A,p,B,q,C,r)
      corr=eh_boundary_vertex_raw((A,p),(B,q),(C,r))
      value=evaluate(V,p,B,q,C,r)
      eq(evaluate(bulk,p,B,q,C,r),plain)
      eq(evaluate(BND,p,B,q,C,r),corr)
      eq(value,plain+corr)
      # Symmetry of the two internal legs is required by the metric Hessian.
      eq(value,evaluate(V,p,C,r,B,q))
      if corr:negative.append(dict(fiber=[ia,ib,ic],case=case,omit_boundary=str(corr),reverse_sign_defect=str(2*corr)))
      controls.append(dict(fiber=[ia,ib,ic],case=case,total_momentum=total,raw=str(value),boundary=str(corr)))
    print('VERTEX',ia,case,'checks',checks,'cpu',time.process_time()-cpu,flush=True)
# Independent full-density cubic Ward identity with nonzero total momentum.
ward=[]
for ib,ic in [(0,0),(0,4),(1,7),(2,5),(6,9)]:
 B,C=BASIS[ib],BASIS[ic];p,q,r=momenta[0];v=(2,-1,1,3)
 A=gauge_matrix(p,v);ell=tuple(-t for t in add(p,q,r))
 lhs=evaluate(localized_vertex_data(A,F(1),ell),p,B,q,C,r)
 LB=lie_matrix(B,q,p,v);LC=lie_matrix(C,r,p,v)
 def v2(U,k,V,l):return eh_quadratic_8k(U,k,V,l)+eh_boundary_vertex_raw((U,k),(V,l))
 lhs+=2*v2(LB,add(q,p),C,r)+2*v2(B,q,LC,add(r,p))
 rhs=2*dot(add(p,q,r),v)*v2(B,q,C,r)
 eq(lhs,rhs);ward.append(dict(fibers=[ib,ic],lhs=str(lhs),rhs=str(rhs)))
assert negative;checks+=1
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-cpu,controls=controls,negative_controls=negative,
 cubic_Ward=ward,normalization='Wlocalized=chi Wbulk-8 gradchi.b3',full_Q2=False,
 scope='Full localized cubic metric vertex; not assembled bubble contacts or quantum anomaly')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
