"""Independent controls for source sign, finite-part log weights and regulator jets."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time,uuid
import sympy as s
import bilocal_first_curvature_engine as B
import curved_source_jet_engine as OLD
from bilocal_Y_regulator_engine import SourceYDefect
H=Path(__file__).resolve().parent;D=H/'bilocal_regulator_controls';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p;b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
inputs=[H/'bilocal_Y_regulator/results.json',H/'bilocal_XY_extension_contact/results.json',
        H/'bilocal_Y_regulator_engine.py',H/'curved_source_jet_engine.py',Path(__file__)]
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Flat source against old contraction, nonaxial curved source, exact Laurent rule and distance Hessian',
    sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
cpu=time.process_time();checks=[];negatives=[]
def ck(label,f):
    assert s.simplify(f)==0,(label,f);checks.append(label)
a,mu,d1,d2,d3=s.symbols('a mu d1 d2 d3');lm=s.Symbol('log_mu')
base=s.exp(2*a*lm)/a
for ell in (0,1):
    integrand=(1-a)*(d1*a+d2*a*a+d3*a**3)*s.diff(base,a,ell)
    actual=s.expand(s.series(integrand,a,0,1).removeO()).coeff(a,0)
    ck(('Laurent',ell),actual-(d1 if ell==0 else d1-d2))
    if ell:assert s.expand(actual-d1)!=0;negatives.append('discard_a_squared_in_log_contact')
for i in range(4):
    for j in range(4):
        derivative=B.anchored(s.diff(B.distance1/B.w,B.y[i],B.y[j]))
        expected=-s.Rational(2,3)*(int(i==j)-B.x[i]*B.x[j]/B.w)
        ck(('geodesic_Hessian',i,j),derivative-expected)
J=SourceYDefect((1,0,0,0))
for b,c,r in [(1,1,0),(0,1,1),(0,0,0)]:
    T=s.zeros(4);T[b,c]=T[c,b]=1;v=s.eye(4)[:,r]
    expected=0
    for j in range(4):
        _,Bj=OLD.kernel(T,v,s.eye(4)[:,j],0)
        expected+=2*OLD.x[j]*Bj/OLD.z
    expected=s.expand(expected.subs(dict(zip(OLD.x,J.point))).subs(OLD.z,J.z))
    got=J.regulator_coefficient(0,b,c,r)*(1 if b==c else 2)
    ck(('flat_source_regulator',b,c,r),got-expected)
    if expected:assert got+expected!=0;negatives.append('source_wrong_sign_'+str((b,c,r)))
data=json.loads(inputs[0].read_bytes());point=(1,2,-1,1);P=SourceYDefect(point)
for o in (0,1):
    co=[s.sympify(v,locals={'a':a,'L':B.L})/a for v in data['source_coefficients'][o]]
    for b,c,r in [(0,1,2),(2,2,3),(0,0,1)]:
        expected=(co[0]*int(b==c)*point[r]+co[1]*(int(b==r)*point[c]+int(c==r)*point[b]))/P.z**(4-o)+co[2]*point[b]*point[c]*point[r]/P.z**(5-o)
        ck(('curved_source_nonaxis',o,b,c,r),P.regulator_coefficient(o,b,c,r)-expected)
    print('SOURCE_HELDOUT',o,'checks',len(checks),'cpu',time.process_time()-cpu,flush=True)
result=dict(at=datetime.now(timezone.utc).isoformat(),status='REGULATOR_SOURCE_AND_LAURENT_CONTROLS_PASSED',
    checks=len(checks),negative_controls=negatives,cpu_seconds=time.process_time()-cpu,
    full_Q2=False,nonaxial_point=point)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
