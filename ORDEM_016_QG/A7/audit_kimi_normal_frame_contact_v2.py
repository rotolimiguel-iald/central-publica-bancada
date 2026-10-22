"""Check the concrete sign detector and bound the claims of the frame review."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import permutations
from fractions import Fraction as F
import json,hashlib,time,uuid
import sympy as s
from oneform_second_curvature_engine_v2 import oneform_second
H=Path(__file__).resolve().parent;D=H/'kimi_normal_frame_contact_review/local_audit_v2';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();raw=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)
data=json.loads((H/'bilocal_XY_extension_contact/results.json').read_bytes())
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D.parent/'RESPONSE.md',H/'bilocal_XY_extension_contact/results.json',H/'oneform_second_curvature_engine_v2.py']],
    targets=['Concrete odd Fourier sign examples','Reported scheme difference','Natural local counterterm defeats difference-implies-nonnaturality inference'],
    already_resolved='Endpoint/Fourier phase convention has earlier dedicated measured bridge; do not reopen it on missing context in provider excerpt'))
start=time.process_time();checks=0
def eq(a,b):
    global checks
    assert s.expand(a-b)==0,(a,b);checks+=1
p=(1,2,-1,1);v=(1,-1,2,1);p2=sum(t*t for t in p);pv=sum(a*b for a,b in zip(p,v));jet,_,_=oneform_second(v,p)
def sym(word,a):
    ws=set(permutations(word));return sum(jet(w,a,0) for w in ws)/len(ws)
rows=[];geo=list(map(s.Rational,data['coefficients_over_C_E']['geodesic'][1]));coord=list(map(s.Rational,data['coefficients_over_C_E']['coordinate'][1]))
for a,b in [(0,0),(0,2)]:
    values=[int(a==b)*sum(sym((r,k,k),r) for r in range(4) for k in range(4)),
        sum(sym((b,k,k),a)+sym((a,k,k),b) for k in range(4)),
        sum(sym((a,b,r),r) for r in range(4))]
    direct=[-int(a==b)*p2*pv,-p2*(p[b]*v[a]+p[a]*v[b]),-p[a]*p[b]*pv]
    for u,w in zip(values,direct):eq(u,w)
    value=sum(c*t for c,t in zip(geo,values));expected=s.Rational(113,8) if a==b else s.Rational(83,288)
    eq(value,expected);rows.append(dict(component=[a,b],structures=list(map(str,values)),over_CE=str(value)))
eq(sum(sym((0,2,r,k,k),r) for r in range(4) for k in range(4)),14)
diff=[a-b for a,b in zip(geo,coord)]
for u,w in zip(diff,[-s.Rational(35,144),-s.Rational(1,12),s.Rational(7,72)]):eq(u,w)
# Two intrinsic expressions may differ: K*g_ab*box(div c) is a nonzero natural local operator.
P=s.Matrix(p);V=s.Matrix(v);R=s.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]])
natural=lambda a,b:-(a.dot(a))*a.dot(b)*s.eye(4)
difference=natural(R*P,R*V)-R*natural(P,V)*R.T
for entry in difference:eq(entry,0)
eq(natural(P,V)[0,0],14)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
    detector=rows,order5_control=14,scheme_difference=list(map(str,diff)),
    accepted='Concrete Fourier sign detector and finite radial Taylor-jet interpretation',
    corrected='Nonzero difference of two prescriptions is not a proof that one is nonnatural; natural local counterterms can differ nontrivially',
    remaining_open='Naturality of the coordinate prescription still requires transformation law; this check neither proves nor disproves it',
    caveat='For arbitrary smooth tests radial Taylor formula is finite-jet identity with remainder, not necessarily convergent infinite expansion',
    phase_not_reopened=True,full_Q2=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D.parent/'RESPONSE.md',D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
