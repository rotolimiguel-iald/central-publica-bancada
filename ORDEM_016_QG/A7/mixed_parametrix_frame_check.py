"""Compare mixed propagator derivatives across source-coordinate/pair-frame engines."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
import hashlib,json,time,uuid
import sympy as s
import curved_source_jet_engine as E
from position_metric_bubble_engine import green_integer,LABELS
H=Path(__file__).resolve().parent;D=H/'mixed_parametrix_frame';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'curved_source_jet_engine.py',H/'position_metric_bubble_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),target='Mixed XY metric propagator jets, coordinate source versus radial-frame pair representation',
 checks='All derivative slots and 10x10 fibers, on axis and generic nonaxis; connection on X tensor indices plus frame on X derivative and tensor slots',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();checks=0;failures=[]
def gamma(c,a,b):return -(E.d(c,b)*E.x[a]+E.d(c,a)*E.x[b]-2*E.d(a,b)*E.x[c])/3
def frame(a,b):return (E.z*E.d(a,b)-E.x[a]*E.x[b])/6
@lru_cache(None)
def coordinate(i,j,a,b,c,d):
    val=E.hjet(1,a,b,c,d,yi=j,xi=i)
    for e in range(4):
        val-=gamma(e,i,a)*E.hjet(0,e,b,c,d,yi=j)+gamma(e,i,b)*E.hjet(0,a,e,c,d,yi=j)
        val+=frame(i,e)*E.hjet(0,a,b,c,d,yi=j,xi=e)
        val+=frame(a,e)*E.hjet(0,e,b,c,d,yi=j,xi=i)+frame(b,e)*E.hjet(0,a,e,c,d,yi=j,xi=i)
    return s.expand(val)
for node in ((1,0,0,0),(1,2,-1,1)):
    _,g1,_,_,den=green_integer(node);subs=dict(zip(E.x,node));subs[E.z]=sum(q*q for q in node)
    count=0
    for i in range(4):
        for j in range(4):
            for aidx,(a,b) in enumerate(LABELS):
                for cidx,(c,d) in enumerate(LABELS):
                    left=coordinate(i,j,a,b,c,d).subs(subs,simultaneous=True)
                    right=s.Rational(g1[10*(i+1)+aidx].get(10*(j+1)+cidx,0),den)
                    residual=s.simplify(left-right);checks+=1
                    if residual!=0:
                        count+=1
                        failures.append(dict(node=node,derivatives=[i,j],left_fiber=[a,b],right_fiber=[c,d],residual=str(residual)))
    print(json.dumps(dict(node=node,failures=count,cpu=time.process_time()-cpu)),flush=True)
result=dict(at=datetime.now(timezone.utc).isoformat(),status='MIXED_PARAMETRIX_FRAME_MATCH' if not failures else 'MIXED_PARAMETRIX_FRAME_MISMATCH_MEASURED',
 checks=checks,failures=failures,cpu_seconds=time.process_time()-cpu,full_Q2=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({**{k:v for k,v in result.items() if k!='failures'},'failure_count':len(failures),'first_failures':failures[:3]}))
