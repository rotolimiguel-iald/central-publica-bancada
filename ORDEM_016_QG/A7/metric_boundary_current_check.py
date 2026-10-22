"""Check localized quartic EH Ward with the previously omitted divergence."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import json,hashlib,time
from metric_principal_vertices import I,gauge_matrix,lie_matrix,eh_cubic_16k,clear_caches
from metric_quartic_vertices import eh_quartic_32k
from metric_boundary_current_engine import boundary_current,eh_boundary_vertex_raw,metric_series
from position_metric_bubble_engine import BASIS
H=Path(__file__).resolve().parent;D=H/'metric_boundary_current';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
 p=D/name;assert not p.exists();raw=json.dumps(value,ensure_ascii=False,indent=2).encode();t=p.with_suffix('.tmp');t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)
inputs=[Path(__file__),H/'metric_boundary_current_engine.py',H/'metric_principal_vertices.py',
 H/'metric_quartic_vertices.py',H/'finite_smooth_tadpole_derivative_jets/DERIVACAO.md',H/'linear_normalization_v2/DERIVACAO_CONTATO.md']
save('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Full polarization EH divergence current and quartic Ward at nonzero total momentum',
 action='S=-1/(2k) integral chi sqrt(g) R; sqrt(g) R=GammaGamma+div B',
 current='B^mu=sqrt(g)(g^ab Gamma^mu_ab-g^mu,a Gamma^b_ab)',
 method='Square-free inverse and determinant jets, no commuting-matrix assumption; independent diffeomorphism Ward',
 momentum='exp(+ipx); total Q not zero, cutoff supplies -Q',
 scope='Classical metric vertices required for quantum contact bookkeeping; flat coordinate frame, not Q2',
 sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
cpu=time.process_time();checks=0
def eq(a,b=0):
 global checks
 assert a==b,(a,b);checks+=1
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def v3(fields):
 ((A,p),(B,q),(C,r))=fields
 return eh_cubic_16k(A,p,B,q,C,r)+eh_boundary_vertex_raw(*fields)
def v4(fields):return eh_quartic_32k(*fields)+eh_boundary_vertex_raw(*fields)
# Conformal metric: B=-3 du exactly, hence all higher polarized B vanish.
ps=[(1,2,-1,1),(2,-1,0,3),(0,1,1,0),(-1,0,2,1)]
eq(boundary_current((I,ps[0])),tuple(-3*v for v in ps[0]))
for n in (2,3,4):eq(boundary_current(*[(I,p) for p in ps[:n]]),(F(),)*4)
# Rank-one metric determinant sqrt(1+t); repeated directions pick n! coefficient.
inv,dens=metric_series([BASIS[0]]*4)
for n,target in [(1,F(1,2)),(2,F(-1,4)),(3,F(3,8)),(4,F(-15,16))]:eq(dens[(1<<n)-1],target)
controls=[];bad_count=0
triples=[(0,0,1),(0,1,2),(1,4,8),(2,5,9),(3,6,7),(0,4,9)]
for f,(a,b,c) in enumerate(triples):
 A,U,V=BASIS[a],BASIS[b],BASIS[c]
 p,r,sp=ps[0],ps[1],ps[2];k=ps[3];ghost=(2,-1,1,3)
 total=add(add(p,r),add(sp,k));G=gauge_matrix(k,ghost)
 quartic=((A,p),(G,k),(U,r),(V,sp))
 three=[((lie_matrix(A,p,k,ghost),add(p,k)),(U,r),(V,sp)),
        ((A,p),(lie_matrix(U,r,k,ghost),add(r,k)),(V,sp)),
        ((A,p),(U,r),(lie_matrix(V,sp,k,ghost),add(sp,k)))]
 left=v4(quartic)+2*sum(v3(fields) for fields in three)
 right=2*dot(total,ghost)*v3(((A,p),(U,r),(V,sp)))
 eq(left,right)
 plain=eh_quartic_32k(*quartic)+2*sum(eh_cubic_16k(*sum(([m,q] for m,q in fields),[])) for fields in three)
 plain_right=2*dot(total,ghost)*eh_cubic_16k(A,p,U,r,V,sp)
 bad=plain-plain_right
 if bad:bad_count+=1
 controls.append(dict(fiber=[a,b,c],total_momentum=total,full_Ward_left=str(left),full_Ward_right=str(right),
                      GammaGamma_only_defect=str(bad),quartic_boundary=str(eh_boundary_vertex_raw(*quartic))))
 # Current permutation symmetry probes the coefficient construction.
 eq(boundary_current(*quartic),boundary_current(quartic[3],quartic[1],quartic[0],quartic[2]))
 clear_caches()
assert bad_count>0;checks+=1
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-cpu,
 controls=controls,negative_controls_nonzero=bad_count,
 identity='V4raw_full(A,Gc,U,V)+2 sum V3raw_full(Lie terms)=2(Q.c)V3raw_full(A,U,V)',
 physical_state_selected=False,full_Q2=False,gate_changed=False)
save('results.json',result);save('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
