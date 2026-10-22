"""Exact localization defect and antifield-current component, no quantum inference."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s

H=Path(__file__).resolve().parent;D=H/'localized_brst_anticommutator';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):
 p=D/name;assert not p.exists();b=json.dumps(obj,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Compute {s0,s1_chi}h and the corresponding antifield boundary term explicitly',
 convention='s0h=Gc,s0c=0,s1h=L_c h,s1c=c.dc; s1_chi=chi*s1 on field generators',
 antifield_projection='s0hdagger=E_h; s0cdagger restricted to hdagger=-G* hdagger in the convention of the existing source',
 excluded='No full quantum descendant contraction or claimed cancellation of measured localized contact',
 script_sha256=sha(Path(__file__))))
start=time.process_time();checks=0
p=s.symbols('p0:4');q=s.symbols('q0:4');lam=s.symbols('lambda0:4')
u=s.symbols('u0:4');v=s.symbols('v0:4')
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
G=lambda k,c:s.Matrix(4,4,lambda i,j:k[i]*c[j]+k[j]*c[i])
Gu,Gv=G(p,u),G(q,v)
w=tuple(dot(u,q)*v[i]-dot(v,p)*u[i] for i in range(4))
s0Z=s.Matrix(4,4,lambda i,j:-dot(u,q)*Gv[i,j]+dot(v,p)*Gu[i,j]+
 sum(Gu[i,m]*q[j]*v[m]-Gv[i,m]*p[j]*u[m]+Gu[j,m]*q[i]*v[m]-Gv[j,m]*p[i]*u[m] for m in range(4)))
k=tuple(p[i]+q[i] for i in range(4))
for value in (s0Z+G(k,w)).applyfunc(s.expand):assert value==0;checks+=1
defect=(s0Z+G(tuple(k[i]+lam[i] for i in range(4)),w)).applyfunc(s.expand)
expected=G(lam,w)
for value in (defect-expected).applyfunc(s.expand):assert value==0;checks+=1
for value in defect.subs(dict.fromkeys(lam,0)):assert value==0;checks+=1

# The hdagger projection in s0 V_chi has the opposite localization defect.
# -hdagger*chi*s0Z from its odd Leibniz sign, and
# -hdagger*G(chi*w) from the cdagger term after the formal adjoint.
antifield_tensor=(-s0Z-G(tuple(k[i]+lam[i] for i in range(4)),w)).applyfunc(s.expand)
for value in (antifield_tensor+expected).applyfunc(s.expand):assert value==0;checks+=1

# Arbitrary symmetric Euler coefficient: compare full contraction and current form.
coeff=s.symbols('E0:10');labels=[(i,j) for i in range(4) for j in range(i,4)]
E=s.zeros(4)
for c,(i,j) in zip(coeff,labels):E[i,j]=E[j,i]=c
eom=dot(list(E),list(defect));current=2*sum(lam[i]*E[i,j]*w[j] for i in range(4) for j in range(4))
assert s.expand(eom-current)==0;checks+=1
assert s.expand(eom+dot(list(E),list(antifield_tensor)))==0;checks+=1

# Nonzero control rules out an accidental constant-cutoff test.
sub=dict(zip(p,(1,2,-1,1)));sub.update(zip(q,(0,1,2,-1)))
sub.update(zip(u,(1,0,1,0)));sub.update(zip(v,(0,1,-1,1)));sub.update(zip(lam,(1,-1,0,0)))
measured=defect.subs(sub);assert measured!=s.zeros(4);checks+=1
evalue=eom.subs(sub).subs(dict(zip(coeff,range(1,11))))
assert evalue!=0;checks+=1
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 identity='{s0,s1_chi}h=[G,chi]w=(d_mu chi)w_nu+(d_nu chi)w_mu; w=c.dc',
 antifield_current='J_af^mu=-2*hdagger^(mu,nu)*w_nu in the stated source convention',
 classical_completion='C_full_chi=C_fields_chi-integral hdagger.[G,chi]w; its s0 variations cancel the Euler term',
 nonzero_control_matrix=[[str(v) for v in row] for row in measured.tolist()],euler_pairing_control=str(evalue),
 limitation='Classical antifield projection and Euler-sector cancellation only; no number of the one-loop localized defect has been canceled',
 quantum_next='Include time-ordered insertions of the full BV breaking and free equations-of-motion contact normalizations; antifields themselves have no propagators',
 full_Q2=False,gate_changed=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'PRE_REGISTER.json',D/'results.json',H/'localized_gauge_fixing_commutator_check.py']]))
print(json.dumps(result,ensure_ascii=False))
