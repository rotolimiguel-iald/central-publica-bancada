"""Check transport and recovery of the two-endpoint source parametrices."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
import bilocal_first_curvature_engine as B
import curved_source_jet_engine as E
H=Path(__file__).resolve().parent;D=H/'bilocal_first_curvature_v2';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'bilocal_first_curvature_engine.py',H/'curved_source_jet_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Explicit two-endpoint firstK squared distance and parallel propagator, not inferred only from jets at y=0',
 proofs='Distance from first variation of metric energy on the straight segment; transport integral of firstK connection; higher path correction contributes only at K²',
 checks='Endpoint symmetry, metric compatibility, segment transport ODE, all source metric/ghost fields and firstY jets',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();checks=[]
def ck(n,v):
    # The auxiliary radius is constrained only AFTER all endpoint derivatives.
    value=s.cancel(v.subs(E.z,sum(a*a for a in E.x)))
    assert s.expand(value)==0,(n,s.expand(value))
    checks.append(n)
swap=dict(zip(B.x,B.y));swap.update(dict(zip(B.y,B.x)))
ck('distance_symmetry',B.distance1-B.distance1.subs(swap,simultaneous=True))
ck('distance_coincident',B.distance1.subs(dict(zip(B.x,B.y)),simultaneous=True))
t=s.Symbol('t');Z=B.Y+t*(B.X-B.Y);segment=dict(zip(B.x,Z));V=B.X-B.Y
Pseg=B.P1.subs(segment,simultaneous=True)
for a in range(4):
    for b in range(4):
        ck(f'inverse_{a}_{b}',B.P1[a,b]+B.P1[a,b].subs(swap,simultaneous=True))
        ck(f'isometry_{a}_{b}',B.P1[a,b]+B.P1[b,a]+B.gX1[a,b]-B.gY1[a,b])
        connection=sum(-(B.d(a,b)*Z[i]+B.d(a,i)*Z[b]-2*B.d(i,b)*Z[a])*V[i]/3 for i in range(4))
        ck(f'transport_ODE_{a}_{b}',s.diff(Pseg[a,b],t)+connection)
        for order in (0,1):
            for j in range(4):
                f=B.anchored(B.derivative(B.ghost(order,a,b),'Y',j)).subs(B.w,E.z)
                ck(f'ghost_Y_{order}_{a}_{b}_{j}',f-E.gjet(order,a,b,j))
for a in range(4):
    for b in range(a,4):
        for c in range(4):
            for d in range(c,4):
                for order in (0,1):
                    f=B.anchored(B.metric(order,a,b,c,d)).subs(B.w,E.z)
                    ck(f'metric_base_{order}_{a}_{b}_{c}_{d}',f-E.hjet(order,a,b,c,d))
                    for j in range(4):
                        f=B.anchored(B.derivative(B.metric(order,a,b,c,d),'Y',j)).subs(B.w,E.z)
                        ck(f'metric_Y_{order}_{a}_{b}_{c}_{d}_{j}',f-E.hjet(order,a,b,c,d,yi=j))
result=dict(at=datetime.now(timezone.utc).isoformat(),status='BILOCAL_FIRSTK_PARAMETRIX_TRANSPORT_CHECKED',checks=len(checks),check_names=checks,cpu_seconds=time.process_time()-cpu,
 full_Q2=False,scope='FirstK two-endpoint parametrix; no higher products, smooth W or quantum Ward sum')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='check_names'}))
