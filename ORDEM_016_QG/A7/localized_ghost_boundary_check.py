"""Check ghost boundary against its unreduced divergence and assemble loop sum."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import json,hashlib,time,uuid
from localized_ghost_boundary_engine import ghost_localized_data,FullGhostLoop
from ghost_direct_position_engine import vertex
from flat_loop_cutoff_engine import tensor
from position_metric_bubble_engine import BASIS

H=Path(__file__).resolve().parent;D=H/'localized_ghost_boundary';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
 p=D/name;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
 t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'localized_ghost_boundary_engine.py',H/'ghost_direct_position_engine.py',H/'full_eh_localized_loop_engine.py',H/'full_eh_localized_loop/manifest.json']
for row in json.loads((H/'full_eh_localized_loop/manifest.json').read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),sources=[dict(path=str(p),sha256=sha(p)) for p in sources],
 target='Restore boundary of the original ghost divergence, then assemble with fullEH bubble',
 prescription='chi barc divZ, localized before integration by parts; compare chi (-dbarc Z) explicitly',full_Q2=False))
start=time.process_time();checks=0;neg=[];controls=[]
def eq(a,b):
 global checks
 assert a==b,(a,b);checks+=1
def dot(a,b):return sum(u*v for u,v in zip(a,b))
def add(*v):return tuple(sum(t) for t in zip(*v))
def eval_vertex(V,p,c,q,bar,r):
    u=list(c)+[qi*cv for qi in q for cv in c];v=list(bar)+[ri*b for ri in r for b in bar]
    def pair(W):return sum(u[i]*value*v[j] for i,row in enumerate(W) for j,value in row.items())
    return pair(V[0])+sum(p[i]*pair(V[1][i]) for i in range(4))
def current(A,p,c,q):
    tr=sum(A[4*i+i] for i in range(4));cp=dot(c,p)
    return [[cp*A[4*mu+nu]+sum(A[4*rho+nu]*q[mu]*c[rho]+A[4*mu+rho]*q[nu]*c[rho] for rho in range(4))
      -F(int(mu==nu),2)*(cp*tr+2*sum(A[4*rho+lam]*q[lam]*c[rho] for rho in range(4) for lam in range(4))) for nu in range(4)] for mu in range(4)]
for A in BASIS:
 for p,q,r in [((1,2,-1,1),(2,-1,0,3),(0,1,1,0)),((0,1,0,-1),(1,0,2,1),(2,1,-1,0))]:
    ell=tuple(-v for v in add(p,q,r));c=(1,2,-1,0);bar=(2,-1,0,3);Z=current(A,p,c,q)
    plain=eval_vertex(vertex(A),p,c,q,bar,r)
    eq(plain,-sum(r[mu]*bar[nu]*Z[mu][nu] for mu in range(4) for nu in range(4)))
    full=eval_vertex(ghost_localized_data(A,F(1),ell),p,c,q,bar,r)
    original=sum((p[mu]+q[mu])*bar[nu]*Z[mu][nu] for mu in range(4) for nu in range(4))
    eq(full,original)
    if full!=plain:neg.append(str(full-plain))
assert neg;checks+=1
point=(1,2,-1,1)
cases=[('constant',{():1},{():1}),('Y_gradient',{():1},{():1,(0,):1}),
 ('XY_gradient',{():1,(0,):1,(1,):-1},{():1,(0,):1}),
 ('Y_hessian',{():1},{():1,(0,0):1,(0,1):2,(1,1):-1}),
 ('X_hessian',{():1,(0,0):1,(0,1):2,(1,1):-1},{():1}),
 ('Y_third_jet',{():1},{():1,(0,0,1):1})]
metric=json.loads((H/'full_eh_localized_loop/results.json').read_bytes())['rows']
for a,b in [(1,1),(0,1)]:
    engine=FullGhostLoop(point,tensor(a,b));mult=1 if a==b else 2
    for label,xj,yj in cases:
      values=[engine.full_localized(r,xj,yj)/mult for r in range(4)]
      assert all(isinstance(v,F) for v in values);checks+=4
      m=next(t for t in metric if (t['a'],t['b'],t['case'])==(a,b,label))
      total=[g-F(v)/2 for g,v in zip(values,m['full_metric'])]
      if label=='constant':eq(total,[0]*4)
      row=dict(a=a,b=b,case=label,full_ghost=list(map(str,values)),full_metric=m['full_metric'],
        ghost_minus_half_metric=list(map(str,total)))
      controls.append(row);put(str(a)+str(b)+'_'+label+'.json',row)
      print('GHOST_COMPLETE',a,b,label,'cpu',time.process_time()-start,flush=True)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 negative_vertex_controls=neg,rows=controls,full_Q2=False,gate_changed=False,
 scope='Flat metric+ghost localized vertices completed. Source, BRST cutoff flux, extension and nonlinear arities not summed; nonzero boundary flux is not anomaly.')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
