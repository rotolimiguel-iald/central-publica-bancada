"""Compare the written ordered Hessian with variation of the heat density."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
from ghost_covariant_word_engine import *
from spaceform_covariant_jet_engine import second_curvature_constant
HOM=Path(__file__).resolve().parent;D0=HOM/'ghost_closed_hessian_audit';D0.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,v):
 b=json.dumps(v,ensure_ascii=False,indent=2).encode();assert not p.exists(),str(p)
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
new(D0/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),script_sha256=sha(Path(__file__)),
 report_sha256=sha(HOM/'ghost_curved_hessian/DERIVACAO.md'),target='Ordered Hessian in written report versus density variation',full_Q2=False))
start,cpu=perf_counter(),process_time()
def lap(f):return add(*(derivative(derivative(f,i),i) for i in range(4)))
def hes(f,a,b):return derivative(derivative(f,b),a)
tt=trh();uu=[divergence(a) for a in range(4)];dd=add(*(derivative(uu[a],a) for a in range(4)))
closed=defaultdict(Q)
for a in range(4):
 for b in range(4):
  hab=term((),a,b);delta=int(a==b)
  v0=add(scale(lap(lap(hab)),Q(1,12)),scale(lap(lap(tt)),Q(7,48)*delta),
    scale(hes(lap(tt),a,b),Q(-1,8)),scale(lap(dd),Q(-1,8)*delta),
    scale(add(derivative(lap(uu[b]),a),derivative(lap(uu[a]),b)),Q(-1,24)),
    scale(hes(dd,a,b),Q(1,6)))
  v1=add(scale(lap(hab),Q(-7,6)),scale(lap(tt),Q(17,6)*delta),
    scale(hes(tt,a,b),Q(-7,2)),scale(dd,Q(-7,2)*delta),
    scale(add(derivative(uu[b],a),derivative(uu[a],b)),Q(79,24)))
  v2=add(scale(hab,Q(52,3)),scale(tt,Q(-13,3)*delta))
  for ko,f in enumerate((v0,v1,v2)):
   for (w,u,v),c in f.items():closed[(ko,min(a,b),max(a,b),u,v,w)]+=c
closed={k:c for k,c in closed.items() if c};source=hessian_terms();labels=[(i,j) for i in range(4) for j in range(i,4)]
checks=[];cache={}
def j2(H):
 key=tuple(tuple(row) for row in H)
 if key not in cache:cache[key]=second_curvature_constant(H)
 return cache[key]
def ev(o,T,H,order):
 if order<2:return evaluate(o,T,H,(1,0,0,0),order)
 jj=j2(H)
 return sum(c*T[a][b]*jj(w,u,v,2-ko) for (ko,a,b,u,v,w),c in o.items() if T[a][b])
for i,l in enumerate(labels):
 for r in labels[i:]:
  T,H=matrix_unit(*l),matrix_unit(*r)
  for order in range(3):
   diff=ev(source,T,H,order)-ev(closed,T,H,order)
   assert diff==0,(l,r,order,diff);checks.append(f'{l}_{r}_K{order}')
result=dict(statute='REAL_ORDERED_HESSIAN_REPRESENTATIVE_CHECK',checks=len(checks),check_names=checks,
 result='Written Hessian equals variation of integrated ghost heat density through all homogeneous orders',
 analytic_assumptions_inherited=True,full_Q2=False,gate_changed=False,
 wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu)
new(D0/'results.json',result)
new(D0/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D0/'PRE_REGISTER.json',D0/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='check_names'}))
