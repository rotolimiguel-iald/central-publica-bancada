"""Check the received Killing recurrence against the existing bilocal kernel."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
from itertools import product
import json,hashlib,time,uuid
import sympy as s
import bilocal_first_curvature_engine as B
import bilocal_covariant_jet_engine as E
H=Path(__file__).resolve().parent;D=H/'kimi_transvection_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
 p=D/name;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),D/'RECEIPT.json',D/'RESPONSE.md',H/'bilocal_first_curvature_engine.py',H/'bilocal_covariant_jet_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),sources=[dict(path=str(p),sha256=sha(p)) for p in sources],
 target='Killing recurrence and claimed residual2K/3 deltaij deltaAB/w; do not change existing engines',
 tests=['derive Christoffel from metric','Killing Lie derivative','all64 first ghost jets','all256 second ghost jets','400 first symmetric metric jets','full distance second jet and omitted trace'],full_Q2=False))
start=time.process_time();checks=0
x,w=B.x,B.w;d=B.d
def eq(f,g=0):
 global checks
 num,den=s.fraction(s.cancel(B.anchored(f-g)));num=s.rem(num,B.xx-w,x[0]);assert s.expand(num)==0,(f,g,num);checks+=1
def dx(f,i):return B.derivative(f,'X',i)
def kap(i,a):return -(B.xx*d(i,a)-x[a]*x[i])/3
def dk(i,a,c):return s.diff(kap(i,a),x[c])
def qkk(i,j,b,c):return -(2*d(j,b)*d(i,c)-d(c,j)*d(i,b)-d(c,b)*d(i,j))/3
gamma_typo_count=0
for c,a,b in product(range(4),repeat=3):
 actual=(s.diff(B.gX1[c,b],x[a])+s.diff(B.gX1[c,a],x[b])-s.diff(B.gX1[a,b],x[c]))/2
 eq(actual,E.gamma(x,c,a,b))
 quoted=-(2*d(a,b)*x[c]-x[a]*d(c,b)-x[b]*d(c,a))/3
 if s.expand(actual-quoted)!=0:gamma_typo_count+=1
for i,a,b in product(range(4),repeat=3):
 eq(s.diff(B.gX1[a,b],x[i])+dk(i,b,a)+dk(i,a,b))

@lru_cache(None)
def anchor(kind,o,ids):return B.anchored(E.raw(kind,o,ids))
def D1(kind,i,ids,get):
 f=get(ids);out=sum(kap(i,c)*dx(f,c) for c in range(4))
 if kind=='ghost':out-=sum(dk(i,ids[0],c)*get((c,ids[1])) for c in range(4))
 else:
  for p in (0,1):
   for c in range(4):out+=dk(i,c,ids[p])*get(ids[:p]+(c,)+ids[p+1:])
 return s.expand(out)
def first_pred(kind,ids,i):return -dx(anchor(kind,1,ids),i)-D1(kind,i,ids,lambda v:anchor(kind,0,v))
def second_pred(kind,ids,i,j):
 get0=lambda v:anchor(kind,0,v)
 val=dx(dx(anchor(kind,1,ids),j),i)+dx(D1(kind,j,ids,get0),i)+D1(kind,i,ids,lambda v:dx(get0(v),j))
 for p in ((1,) if kind=='ghost' else (2,3)):
  for c in range(4):val-=qkk(i,j,ids[p],c)*get0(ids[:p]+(c,)+ids[p+1:])
 return s.expand(val)
for i,a,b in product(range(4),repeat=3):
 ids=(a,b);eq(B.derivative(B.ghost(1,a,b),'Y',i),first_pred('ghost',ids,i))
print('First ghost',checks,flush=True)
claimed_nonzero=0;controls=[]
for i,j,a,b in product(range(4),repeat=4):
 ids=(a,b);actual=B.derivative(B.derivative(B.ghost(1,a,b),'Y',j),'Y',i)
 pred=second_pred('ghost',ids,i,j);eq(actual,pred)
 claimed=2*d(i,j)*d(a,b)/(3*w)
 if claimed:claimed_nonzero+=1
 if (i,j,a,b) in [(0,0,1,1),(0,1,1,2)]:
  point={x[0]:1,x[1]:2,x[2]:-1,x[3]:1,w:7,B.L:s.log(7)}
  controls.append(dict(component=[i,j,a,b],actual=str(B.anchored(actual).subs(point)),recurrence=str(pred.subs(point)),claimed_extra=str(claimed.subs(point))))
print('Second ghost',checks,flush=True)
labels=[(a,b) for a in range(4) for b in range(a,4)]
for i in range(4):
 for a,b in labels:
  for c,e in labels:
   ids=(a,b,c,e);eq(B.derivative(B.metric(1,*ids),'Y',i),first_pred('metric',ids,i))
 print('Metric first direction',i,'checks',checks,'cpu',time.process_time()-start,flush=True)
for i,j in product(range(4),repeat=2):
 actual=s.diff(B.distance1,B.y[i],B.y[j]);eq(actual,-2*(B.xx*d(i,j)-x[i]*x[j])/3)
 # The term omitted in the reply is exactly -2xx deltaij/3.
 eq(B.anchored(actual)-2*x[i]*x[j]/3,-2*B.xx*d(i,j)/3)
for i,j,b,c in product(range(4),repeat=4):
 eq(-qkk(i,j,b,c),s.diff(E.gamma(B.y,c,j,b),B.y[i]))
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 first_ghost_components=64,second_ghost_components=256,first_metric_components=400,
 claimed_residual_refuted_components=claimed_nonzero,actual_recurrence_residual='0 on all256 ghost second jets',
 typo_gamma_components=gamma_typo_count,controls=controls,
 diagnosis='Reply omitted -2xx deltaij/3 in dYi dYj distance1; proposed residual is absent from actual kernel. Section1 gamma sign typo conflicts with engine, later formulas use correct sign.',
 scope='FirstK singular geometry only; no smooth state, no quantum anomaly, second metric jets not checked here',full_Q2=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
