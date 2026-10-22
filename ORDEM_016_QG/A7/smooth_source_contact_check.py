"""Smooth-reference dependence of the source bubble: residue versus finite contact."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time
import sympy as s
from logarithmic_contact_engine import contact
from curved_source_jet_engine import x,z,dx,average,d
H=Path(__file__).resolve().parent;O=H/'smooth_source_contact';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=O/n;assert not p.exists(),p;b=json.dumps(v,ensure_ascii=False,indent=2).encode()
    t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    scope='Two-vertex hdagger-c bubble; smooth change in Hadamard reference; no full Ward claim',
    sources=[dict(path=str(p),sha256=sha(p)) for p in
     [H/'curved_source_jet_engine.py',H/'logarithmic_contact_engine.py']],
    expected_structure='Only a smooth coefficient times second derivatives of 1/z has critical scaling degree4; higher Taylor terms are locally integrable',
    goals=['Prove zero angular logarithmic residue, not absence of finite contact',
           'Apply fixed extension to mixed XY derivatives and contract the original vertices',
           'Evaluate isotropic metric W jets as a nonzero finite-contact control'],
    excluded=['assuming W is zero','claiming arbitrary jet data define a physical state','full curved amplitude']))
t=time.process_time();checks=[]
def ck(n,v):assert s.expand(v)==0,(n,v);checks.append(n)
for i in range(4):
 for j in range(4):
    ck(f'zero_residue_{i}_{j}',average(dx(dx(1/z,i),j)))
    ck(f'fixed_contact_{i}_{j}',contact(1,0,(i,j))+d(i,j)/4)
# Smooth metric reference at coincidence, with all first jets zero for this
# algebraic control. No claim that this truncation is a curved bisolution.
wI,wT=s.symbols('wI wT');p=s.Matrix(s.symbols('p0:4'));v=s.Matrix(s.symbols('v0:4'))
def W(a,b,c,e):return wI*(d(a,c)*d(b,e)+d(a,e)*d(b,c))/2+wT*d(a,b)*d(c,e)
def contracted(T):
    out=0
    for a in range(4):
     for b in range(4):
      if T[a,b]==0:continue
      for m in range(4):
       B=sum(v[r]*(p[b]*W(a,m,r,m)+p[m]*W(a,m,b,r)) for r in range(4))
       if b==m:B-=sum(p[al]*v[r]*W(a,m,al,r) for al in range(4) for r in range(4))
       out-=T[a,b]*B/2
    return s.expand(out)
for a in range(4):
 for b in range(a,4):
    T=s.zeros(4);T[a,b]=T[b,a]=1
    expected=-(wI+wT)*(p.T*T*v)[0]-(wI/4-wT/2)*s.trace(T)*p.dot(v)
    ck(f'isotropic_contact_{a}_{b}',contracted(T)-expected)
T=s.zeros(4);T[0,1]=T[1,0]=1
nonzero=contracted(T).subs({wI:1,wT:0,**dict(zip(p,[1,0,0,0])),**dict(zip(v,[0,1,0,0]))})
assert nonzero==-1
result=dict(status='ZERO_LOG_RESIDUE_NONZERO_FINITE_CONTACT',checks=len(checks),check_names=checks,
    finite_mixed_derivative='(R(partial_Xi partial_Yj z^-1)-partial_Xi partial_Yj z^-1)/C = delta_ij delta/4',
    metric_isotropic_contact_over_C='-(wI+wT) p.T.v -(wI/4-wT/2) tr(T)(p.v)',
    negative_control= str(nonzero),cpu_seconds=time.process_time()-t,
    smooth_reference_not_discarded=True,full_Q2=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in
 [Path(__file__),O/'PRE_REGISTER.json',O/'results.json',H/'logarithmic_contact_engine.py',H/'curved_source_jet_engine.py']]))
print(json.dumps({k:v for k,v in result.items() if k!='check_names'},ensure_ascii=False))
