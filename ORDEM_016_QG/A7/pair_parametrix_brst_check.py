"""Check free BRST directly on the radial-frame Green matrices used by pairs."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json,time,uuid
from position_metric_bubble_engine import green_integer,LABELS
from ghost_direct_position_engine import green
H=Path(__file__).resolve().parent;D=H/'pair_parametrix_brst';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'position_metric_bubble_engine.py',H/'ghost_direct_position_engine.py',H/'free_parametrix_brst/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Same C_X H=-sym(nabla_Y G)/2 in actual radial-frame pair matrices',
 fixtures='Four axes, two mixed integer directions; first K and flat, every output covector and symmetric source fiber',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();lookup={pair:i for i,pair in enumerate(LABELS)}
def idx(a,b):return lookup[min(a,b),max(a,b)]
def entry(A,i,j):return A[i].get(j,0)
nodes=[tuple(int(i==j) for i in range(4)) for j in range(4)]+[(1,2,-1,1),(2,-1,3,1)]
fails=[];checks=0
for x in nodes:
    h0,h1,_,hd0,hd1=green_integer(x);g0,g1,_,gd0,gd1=green(x)
    for o,h,g,hd,gd in [(0,h0,g0,hd0,gd0),(1,h1,g1,hd1,gd1)]:
        for b in range(4):
            for f,(c,d) in enumerate(LABELS):
                lhs=sum(F(entry(h,10*(a+1)+idx(a,b),f),hd) for a in range(4))
                lhs-=sum(F(entry(h,10*(b+1)+idx(a,a),f),2*hd) for a in range(4))
                rhs=-F(entry(g,b,4*(c+1)+d)+entry(g,b,4*(d+1)+c),2*gd)
                checks+=1
                if lhs!=rhs:fails.append(dict(x=x,order=o,b=b,fiber=[c,d],residual=str(lhs-rhs)))
result=dict(at=datetime.now(timezone.utc).isoformat(),status='PAIR_PARAMETRIX_BRST_MATCH' if not fails else 'PAIR_PARAMETRIX_BRST_MISMATCH_MEASURED',
 checks=checks,failures=fails,cpu_seconds=time.process_time()-cpu,full_Q2=False,
 scope='Exact rational evaluations, not a polynomial identity proof or distributional contact test')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({**{k:v for k,v in result.items() if k!='failures'},'failure_count':len(fails),'first_failures':fails[:3]}))
