"""Reconstruct the anchored source covector and apply Einstein in X."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
import bilocal_first_curvature_engine as B
from bilocal_source_divergence_engine import SourcePoint
import curved_source_jet_engine as OLD
import einstein_test_field_engine as EN
H=Path(__file__).resolve().parent;D=H/'bilocal_source_divergence';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'bilocal_source_divergence_engine.py',H/'bilocal_first_curvature_engine.py',
 H/'bilocal_covariant_jet_engine.py',H/'curved_source_jet_engine.py',H/'einstein_test_field_engine.py']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 aim='Source A-divY B, then EinsteinX, same anchor as loop pair',
 basis='a delta_ab xr+b(delta_ar xb+delta_br xa)+c xa xb xr',
 homogeneity='a,b:z^(-4+order),c:z^(-5+order); coefficients linear in L',
 calibration='axis (1,0,0,0), components110,011,000; nonaxis checks held out',
 scope='FirstK off diagonal, no temporal extension/W/tadpole',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources],full_Q2=False))
cpu=time.process_time();checks=[];J=SourcePoint((1,0,0,0));coeff=[]
for o in (0,1):
    a=J.component(o,1,1,0);b=J.component(o,0,1,1)
    c=s.expand(J.component(o,0,0,0)-a-2*b)
    coeff.append((a,b,c))
    print('SOURCE_BASIS',o,list(map(str,coeff[-1])),'cpu',time.process_time()-cpu,flush=True)
def predict(o,a,b,r,point):
    z=sum(t*t for t in point);ca,cb,cc=coeff[o]
    return s.expand((ca*int(a==b)*point[r]+cb*(int(a==r)*point[b]+int(b==r)*point[a]))/z**(4-o)+cc*point[a]*point[b]*point[r]/z**(5-o))
def equal(label,a,b):
    residue=s.simplify(a-b);assert residue==0,(label,residue);checks.append(label)
# Flat independent implementation: ordinary translation of old A/B kernel.
for a,b,r in [(1,1,0),(0,1,1),(0,0,0)]:
    T=s.zeros(4);T[a,b]=1
    if a!=b:T[b,a]=1
    v=s.eye(4)[:,r];A,_=OLD.kernel(T,v,s.zeros(4,1),0)
    C=A
    for j in range(4):
        _,Bj=OLD.kernel(T,v,s.eye(4)[:,j],0)
        C+=OLD.dx(Bj,j)
    C=s.expand(C.subs(dict(zip(OLD.x,J.point))).subs(OLD.z,J.z))
    equal(('flat_translation_source',a,b,r),C,J.component(0,a,b,r)*(1 if a==b else 2))
for point,ids in [((2,0,0,0),[(1,1,0),(0,1,1),(0,0,0)]),
                  ((1,2,-1,1),[(0,0,0),(1,1,2),(0,1,1),(2,3,0),(0,3,2),(2,2,3)])]:
    P=SourcePoint(point)
    for o in (0,1):
        for a,b,r in ids:
            equal(('heldout',point,o,a,b,r),P.component(o,a,b,r),predict(o,a,b,r,point))
        print('HELDOUT',point,o,'cpu',time.process_time()-cpu,flush=True)
# Apply the already checked geometric differential operator; do not commute it
# through a Fourier multiplier or through a distribution extension.
mu=s.Symbol('mu',positive=True);x=EN.x;Z=EN.Z
h=[]
for o in (0,1):
    ca,cb,cc=[t.subs(B.L,s.log(mu**2*Z)) for t in coeff[o]]
    h.append(s.Matrix(4,4,lambda a,b:
        (ca*int(a==b)*x[0]+cb*(int(a==0)*x[b]+int(b==0)*x[a]))/Z**(4-o)
        +cc*x[a]*x[b]*x[0]/Z**(5-o)))
image=EN.einstein(h,[0]*4)
pointmap=dict(zip(x,(1,0,0,0)));values=[]
for o in (0,1):
    values.append(str(s.simplify(image[o][1,1].subs(pointmap))))
result=dict(at=datetime.now(timezone.utc).isoformat(),status='BILOCAL_SOURCE_DIVERGENCE_AND_EINSTEIN_COMPONENT_MEASURED',
 checks=len(checks),check_names=checks,cpu_seconds=time.process_time()-cpu,
 coefficients=[[str(v) for v in row] for row in coeff],
 Einstein_source_at_pair_point=values,source_covariant_indices=True,
 loop_combination_not_asserted=True,full_Q2=False,distribution_extension=False,
 scope='Isotropic ansatz, calibration plus heldout source coefficients; Einstein on r0, component11')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
