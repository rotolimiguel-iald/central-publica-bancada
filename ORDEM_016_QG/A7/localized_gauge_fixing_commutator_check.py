"""Retain the b and ghost cutoff currents required by the BV069 convention."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'localized_gauge_fixing_commutators';D.mkdir(exist_ok=False)
source=H.parents[1]/'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
 p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),source,H/'localized_brst_flux/DERIVACAO.md']],
 target='With s0barc=-b, localize pre-IBP ghost interaction and BV field transformations consistently',
 identity='s0 Vghost_chi+s1_chi S0_gf = <b,[C,chi]Z>-<barc,[Q,chi]w>, Z=L_c h,w=c.dc, modulo defined integrated adjoints',
 tests='Graded nilpotence polarized in two odd plane waves; differential commutators on polynomial fields; ghost boundary identity modulo exact divergence',
 full_Q2=False,not_included='Full antifield sector and quantum current contractions'))
start=time.process_time();checks=0
def eq(a,b=0):
 global checks
 assert s.expand(a-b)==0,s.expand(a-b);checks+=1
p=s.symbols('p0:4');q=s.symbols('q0:4');u=s.symbols('u0:4');v=s.symbols('v0:4')
dot=lambda a,b:sum(t*w for t,w in zip(a,b))
G=lambda p,c:s.Matrix(4,4,lambda a,b:p[a]*c[b]+p[b]*c[a])
Gu,Gv=G(p,u),G(q,v);w=[dot(u,q)*v[i]-dot(v,p)*u[i] for i in range(4)];gw=G([p[i]+q[i] for i in range(4)],w)
s0Z=s.Matrix(4,4,lambda a,b:-dot(u,q)*Gv[a,b]+dot(v,p)*Gu[a,b]
 +sum(Gu[a,m]*q[b]*v[m]-Gv[a,m]*p[b]*u[m]+Gu[b,m]*q[a]*v[m]-Gv[b,m]*p[a]*u[m] for m in range(4)))
for a in range(4):
 for b in range(4):eq(s0Z[a,b]+gw[a,b])
x=s.symbols('y0:4');chi=1+x[0]+x[1]**2+x[2]*x[3]
C=lambda Z:s.Matrix([sum(s.diff(Z[i,j],x[i]) for i in range(4))-s.diff(s.trace(Z),x[j])/2 for j in range(4)])
box=lambda f:sum(s.diff(f,y,2) for y in x)
h=s.Matrix(4,4,lambda a,b:(a+b+1)*(1+x[a]*x[b])+x[(a+b)%4]**3)
c=s.Matrix([x[(i+1)%4]+x[i]**2+i+1 for i in range(4)])
Z=s.Matrix(4,4,lambda a,b:sum(c[m]*s.diff(h[a,b],x[m])+h[a,m]*s.diff(c[m],x[b])+h[b,m]*s.diff(c[m],x[a]) for m in range(4)))
comm=C(chi*Z)-chi*C(Z);trbar=Z-s.eye(4)*s.trace(Z)/2
for j in range(4):eq(comm[j],sum(s.diff(chi,x[i])*trbar[i,j] for i in range(4)))
ww=s.Matrix([sum(c[m]*s.diff((x[i]+x[(i+2)%4]**2),x[m])-(x[m]+x[(m+2)%4]**2)*s.diff(c[i],x[m]) for m in range(4)) for i in range(4)])
bar=s.Matrix([1+x[i]+x[(i+1)%4]**2 for i in range(4)])
qc=(chi*ww).applyfunc(box)-chi*ww.applyfunc(box)
for i in range(4):eq(qc[i],box(chi)*ww[i]+2*sum(s.diff(chi,y)*s.diff(ww[i],y) for y in x))
ghost_residual=-(bar.dot(qc))
current=s.Matrix([sum(s.diff(bar[i],x[mu])*ww[i]-bar[i]*s.diff(ww[i],x[mu]) for i in range(4)) for mu in range(4)])
integrated=sum(s.diff(chi,x[mu])*current[mu] for mu in range(4))
boundary=-sum(s.diff(s.diff(chi,y)*bar.dot(ww),y) for y in x)
eq(ghost_residual-integrated,boundary)
point=dict(zip(x,(1,2,-1,1)));comm_value=[str(s.expand(v.subs(point))) for v in comm]
ghost_value=str(s.expand(ghost_residual.subs(point)));assert any(s.Rational(t) for t in comm_value) and s.Rational(ghost_value)!=0;checks+=1
# The free convention is already enough to falsify the old +b shorthand.
wrong_free=2*sum((i+1)*box(c[i]) for i in range(4));eq(wrong_free,40)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 convention='BV069 s0barc=-b, Q=CG; Euclidean differential Q=box, Fourier symbol carries i² separately',
 b_commutator_at_point=comm_value,ghost_commutator_at_point=ghost_value,wrong_positive_b_free_variation=str(wrong_free),
 identity='J_gf^mu=b_nu Zbar^(mu,nu)+(partial_mu barc_nu)w^nu-barc_nu partial_mu w^nu, integrated against partial_mu chi',
 full_Q2=False,scope='Localized gauge-fixing sector identity including b and odd ghost terms; actual quantum mixed b-h and ghost current diagrams remain')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),source,D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
