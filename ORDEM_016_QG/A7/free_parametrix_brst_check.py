"""Off-diagonal C_X H versus ghost derivative, in the actual source kernels."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
import curved_source_jet_engine as E
H=Path(__file__).resolve().parent;D=H/'free_parametrix_brst';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'curved_source_jet_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Free BRST intertwinement off diagonal for actual firstK source parametrices',
 identity='C_X H_(ab,cd) = -1/2 [nablaY_c G_lower_(b,d)+nablaY_d G_lower_(b,c)]',
 conditions='H strips4kappa and4pi²; ghost Q inverse has opposite sign to positive Euclidean parametrix; all X metric/connection factors retained',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();x=E.x;z=E.z
def gamma(c,a,b):return -(E.d(c,b)*x[a]+E.d(c,a)*x[b]-2*E.d(a,b)*x[c])/3
def reduce(v):return s.factor(s.cancel(s.expand(v).subs(z,sum(q*q for q in x))))
failures=[];checks=0;flat=0
for order in (0,1):
    for b in range(4):
        for c in range(4):
            for d in range(c,4):
                trace=sum(E.hjet(order,a,a,c,d) for a in range(4))
                lhs=sum(E.hjet(order,a,b,c,d,xi=a) for a in range(4))
                if order:
                    trace-=sum(E.metric1(a,j)*E.hjet(0,a,j,c,d) for a in range(4) for j in range(4))
                    lhs-=sum(E.metric1(a,j)*E.hjet(0,a,b,c,d,xi=j) for a in range(4) for j in range(4))
                    lhs-=sum(gamma(e,a,a)*E.hjet(0,e,b,c,d)+gamma(e,a,b)*E.hjet(0,a,e,c,d) for a in range(4) for e in range(4))
                lhs-=E.dx(trace,b)/2
                rhs=-(E.gjet(order,b,d,c)+E.gjet(order,b,c,d))/2
                if order:rhs-=sum(E.metric1(b,m)*(E.gjet(0,m,d,c)+E.gjet(0,m,c,d)) for m in range(4))/2
                residual=reduce(lhs-rhs);checks+=1
                if not order:
                    assert residual==0,(b,c,d,residual);flat+=1
                if residual!=0:failures.append(dict(order=order,b=b,c=c,d=d,residual=str(residual)))
result=dict(at=datetime.now(timezone.utc).isoformat(),status='FREE_PARAMETRIX_BRST_MATCH' if not failures else 'FREE_PARAMETRIX_BRST_MISMATCH_MEASURED',
 checks=checks,flat_passed=flat,failures=failures,cpu_seconds=time.process_time()-cpu,
 interpretation='Off-diagonal test only; it does not supply distributional contacts or QME',full_Q2=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({**{k:v for k,v in result.items() if k!='failures'},'failure_count':len(failures),'first_failures':failures[:4]}))
