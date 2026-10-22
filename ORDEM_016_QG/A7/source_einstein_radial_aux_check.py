"""Exact rational source image, avoiding expanded coordinate denominators."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from bilocal_source_divergence_engine import SourcePoint
import bilocal_first_curvature_engine as B
import einstein_radial_aux_engine as E
H=Path(__file__).resolve().parent;D=H/'source_einstein_radial_aux';D.mkdir(exist_ok=True)
x=E.x;z=E.radial_z;Z=E.Z
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'bilocal_source_divergence_engine.py',H/'einstein_radial_aux_engine.py',
 H/'einstein_test_field_engine.py',H/'prepare_einstein_radial_aux.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 aim='Same source coefficients re-evaluated, Einstein by auxiliary-radius chain rule and gauge decomposition',
 scope='Strong source only; not Ward sum, no distribution contacts',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();J=SourcePoint((1,0,0,0));cs=[];checks=[]
def reduced(f):
    num,den=s.fraction(s.cancel(s.expand(f)))
    return s.cancel(s.rem(num,Z-z,x[0])/den)
def zero(label,f):
    r=reduced(f);assert r==0,(label,r);checks.append(label)
for o in (0,1):
    a=J.component(o,1,1,0);b=J.component(o,0,1,1);c=J.component(o,0,0,0)-a-2*b
    cs.append((a,b,s.expand(c)))
    assert all(s.diff(t,B.L)==0 for t in cs[-1]),'Handle logarithmic coefficients explicitly if present'
put('SOURCE_COEFFICIENTS.json',dict(values=[[str(t) for t in row] for row in cs],cpu_seconds=time.process_time()-cpu))
print('COEFFICIENTS',cs,'cpu',time.process_time()-cpu,flush=True)
def field(o,r):
    a,b,c=cs[o]
    return s.Matrix(4,4,lambda i,j:(a*int(i==j)*x[r]+b*(int(i==r)*x[j]+int(j==r)*x[i]))/z**(4-o)+c*x[i]*x[j]*x[r]/z**(5-o))
images={};gauge_remainder=None
for r in (0,1):
    a0,b0,c0=cs[0];g0=a0/2;f0=(g0-b0)/6
    v0=[f0*int(i==r)/z**3+g0*x[i]*x[r]/z**4 for i in range(4)]
    G0=E.gauge([v0,[s.Integer(0)]*4],[0]*4)
    for i in range(4):
        for j in range(4):zero(('C0_is_gauge',r,i,j),field(0,r)[i,j]-G0[0][i,j])
    residual=field(1,r)-G0[1]
    # Read the remaining rank3 coefficients at the radial axis for r0.
    if r==0:
        sub=dict(zip(x,(1,0,0,0)));sub[z]=1
        aa=s.expand(residual[1,1].subs(sub));bb=s.expand(residual[0,1].subs(sub))
        # b requires the r1 component; use the explicit connection formula instead.
        G01=E.gauge([[f0*int(i==1)/z**3+g0*x[i]*x[1]/z**4 for i in range(4)],[s.Integer(0)]*4],[0]*4)
        bb=s.expand((field(1,1)[0,1]-G01[1][0,1]).subs(sub))
        cc=s.expand(residual[0,0].subs(sub)-aa-2*bb)
        g1=aa/2;f1=(g1-bb)/4;gauge_remainder=s.expand(cc+12*g1)
    v1=[f1*int(i==r)/z**2+g1*x[i]*x[r]/z**3 for i in range(4)]
    totalG=E.gauge([v0,v1],[0]*4)
    for i in range(4):
        for j in range(4):zero(('curved_gauge_remainder',r,i,j),field(1,r)[i,j]-totalG[1][i,j]-gauge_remainder*x[i]*x[j]*x[r]/z**4)
    image=E.einstein([field(0,r),field(1,r)],[0]*4)
    f=gauge_remainder*x[r]/(6*z**3)
    expected=s.Matrix(4,4,lambda i,j:2*(int(i==j)*sum(E.derivative(E.derivative(f,k,[0]*4),k,[0]*4) for k in range(4))-E.derivative(E.derivative(f,j,[0]*4),i,[0]*4)))
    for i in range(4):
        for j in range(4):
            zero(('Einstein0',r,i,j),image[0][i,j]);zero(('Einstein1',r,i,j),image[1][i,j]-expected[i,j])
    sub=dict(zip(x,(1,0,0,0)));sub[z]=1
    images[str(r)]=[[[str(s.expand(v.subs(sub))) for v in row] for row in image[o].tolist()] for o in (0,1)]
    print('EINSTEIN',r,'checks',len(checks),'cpu',time.process_time()-cpu,flush=True)
result=dict(at=datetime.now(timezone.utc).isoformat(),status='SOURCE_EINSTEIN_EXACT_GAUGE_DECOMPOSITION_CHECKED',
 checks=len(checks),cpu_seconds=time.process_time()-cpu,source_coefficients=[[str(t) for t in row] for row in cs],
 curvature_remainder=str(gauge_remainder),Einstein_curvature_rank3_coefficients=[str(6*gauge_remainder),str(2*gauge_remainder),str(-16*gauge_remainder)],
 image_at_anchor=images,full_Q2=False,contacts=False,
 scope='Exact rational identities modulo z=X²; r0/r1 Einstein components, scalar coefficient decomposition')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'SOURCE_COEFFICIENTS.json',D/'results.json']]))
print(json.dumps(result))
