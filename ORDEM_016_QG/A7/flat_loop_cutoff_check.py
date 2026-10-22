"""Extract localized flat loop values and compare independent saved bulk data."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
from fractions import Fraction as F
import sympy as s
import flat_loop_cutoff_engine as E

H=Path(__file__).resolve().parent;D=H/'flat_loop_cutoff';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
    p=D/name;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'flat_loop_cutoff_engine.py',H/'bilocal_full_external_pair/results.json',
 H/'ghost_direct_position_engine.py',H/'position_metric_ordered_operator_engine.py',H/'position_metric_bubble_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),sources=[dict(path=str(p),sha256=sha(p)) for p in sources],
 scope='Flat unreduced bubble localization; GammaGamma metric part; not contacts or fullEH',full_Q2=False))
start=time.process_time();checks=0;rows=[];zero=(0,)*4;zh=((0,)*4,)*4
old=json.loads((H/'bilocal_full_external_pair/results.json').read_bytes())['coefficients']
point=(1,2,-1,1);z=sum(v*v for v in point)
def delta(a,b):return int(a==b)
def expected(kind,ex,a,b,r):
    if ex<0:
        A,B,C=map(F,old[kind]['C0'][0])
        return F(A*delta(a,b)*point[r]+B*(delta(a,r)*point[b]+delta(b,r)*point[a]),z**5)+F(C*point[a]*point[b]*point[r],z**6)
    c=list(map(F,old[kind]['C1'][0]));i=ex
    terms=[delta(i,r)*delta(a,b),delta(i,a)*delta(b,r)+delta(i,b)*delta(a,r),delta(a,b)*point[i]*point[r],
      delta(i,r)*point[a]*point[b],delta(i,a)*point[b]*point[r]+delta(i,b)*point[a]*point[r],
      delta(a,r)*point[i]*point[b]+delta(b,r)*point[i]*point[a],point[i]*point[a]*point[b]*point[r]]
    return sum(F(v*t,z**p) for v,t,p in zip(c,terms,[4,4,5,5,5,5,6]))
cases=[('constant',zero,zero,zh),('Y_gradient',(0,)*4,(1,0,0,0),zh),
 ('XY_gradient',(1,-1,0,0),(1,0,0,0),zh),
 ('Y_hessian',zero,zero,((1,2,0,0),(2,-1,0,0),(0,0,0,0),(0,0,0,0)))]
for kind in ['ghost','metric']:
 for a,b in [(1,1),(0,1)]:
    engine=E.FlatLoop(kind,point,E.tensor(a,b));mult=1 if a==b else 2
    for ex in [-1,0,1,2,3]:
      for r in range(4):
        val=engine.y_ward(ex,r,1,zero,zh)/mult
        exp=expected(kind,ex,a,b,r)
        assert val==exp,(kind,ex,a,b,r,val,exp);checks+=1
    print('BULK_MATCH',kind,a,b,'cpu',time.process_time()-start,flush=True)
    vals=[]
    for label,gx,gy,hy in cases:
      v=[engine.localized(r,1,gx,1,gy,hy)/mult for r in range(4)]
      assert all(isinstance(t,F) for t in v);checks+=4
      vals.append(dict(case=label,values=list(map(str,v))))
    rows.append(dict(kind=kind,a=a,b=b,cutoffs=vals))
    put(kind+'_'+str(a)+str(b)+'.json',rows[-1])
    print('LOCALIZED',kind,a,b,'cpu',time.process_time()-start,flush=True)
combined=[]
for a,b in [(1,1),(0,1)]:
 g=next(t for t in rows if t['kind']=='ghost' and (t['a'],t['b'])==(a,b))
 m=next(t for t in rows if t['kind']=='metric' and (t['a'],t['b'])==(a,b))
 vals=[]
 for gr,mr in zip(g['cutoffs'],m['cutoffs']):
    v=[F(u)-F(w)/2 for u,w in zip(gr['values'],mr['values'])]
    if gr['case']=='constant':assert v==[0]*4;checks+=4
    vals.append(dict(case=gr['case'],values=list(map(str,v))))
 assert any(F(v) for t in vals[1:] for v in t['values']);checks+=1
 combined.append(dict(a=a,b=b,cutoffs=vals))
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 point=point,rows=rows,combined_ghost_minus_half_metric=combined,full_Q2=False,
 scope='Nonaxial exact flat GammaGamma/ghost localized kernels; full EH boundary and extension still separate')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'results.json',D/'PRE_REGISTER.json']]))
print(json.dumps(result))
