"""Extract the unreduced source B and its missing Y-cutoff contacts at K0."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
from itertools import product
import ast,json,hashlib,time,uuid
import sympy as s
import logarithmic_contact_engine as R
import einstein_radial_aux_engine as E
from bilocal_source_divergence_engine import SourcePoint
H=Path(__file__).resolve().parent;D=H/'source_Y_cutoff_v2';D.mkdir(exist_ok=False)
x=E.x;z=E.radial_z;Q=R.Q;a,lam=s.symbols('a lam')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,obj):
 p=D/n;assert not p.exists();b=json.dumps(obj,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'source_Y_cutoff_check.py',H/'source_Y_cutoff_run.log',H/'bilocal_source_divergence_engine.py',H/'bilocal_first_curvature_engine.py',H/'source_adjoint_cutoff_check.py',H/'logarithmic_contact_engine.py',H/'source_einstein_radial_aux/DERIVACAO.md']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 supersedes='v1 failed missing product in AST namespace after B coefficients/checks; preserved',target='Unreduced B_ab,r^j and source cutoff in Y before EinsteinX; flat singular source only',
 identity='A_chi-divY B_chi=chiY C-(dchiY)_j B^j; X multiplier is kept separately',
 checks='Closed flat contractions versus existing SourcePoint jets, O4 coefficient reconstruction, old reduced source, meromorphic contact and cutoffX first jet',
 prescription='unchanged FP[(1-a)mu^(2a)z^a], CE=-4pi²; q denotes derivatives of delta',
 sources=[dict(path=str(p),sha256=sha(p)) for p in sources],full_Q2=False))
cpu=time.process_time();checks=0
def d(i,j):return s.Integer(i==j)
def eq(f,g=0):
 global checks
 n,den=s.fraction(s.cancel(s.expand(f-g)));n=s.rem(n,E.Z-z,x[0])
 assert s.expand(n)==0,(f,g,n);checks+=1
def S(c,e,mu,nu):return (d(c,mu)*d(e,nu)+d(c,nu)*d(e,mu)-d(c,e)*d(mu,nu))/2
def Sbar(c,e,mu,nu):return (d(c,mu)*d(e,nu)+d(c,nu)*d(e,mu))/2
def hc(c,e,j,r,mu,m):return d(j,mu)*S(c,e,r,m)+d(j,m)*S(c,e,mu,r)-d(mu,m)*S(c,e,j,r)
@lru_cache(None)
def B(j,u,v,r):
 ans=0
 for m,mu in product(range(4),repeat=2):
  ans+=4*x[mu]*x[m]*hc(u,v,j,r,mu,m)/z**4
  ans-=(2*d(mu,v)/z**3-8*x[mu]*x[v]/z**4)*hc(u,m,j,r,mu,m)
  ans-=(2*d(mu,u)/z**3-8*x[mu]*x[u]/z**4)*hc(v,m,j,r,mu,m)
 return s.expand(ans)
def Avec(u,v,r):
 ans=0
 for m,mu in product(range(4),repeat=2):
  ans-=2*x[mu]/z**2*(2*d(m,r)/z**2-8*x[m]*x[r]/z**3)*Sbar(u,v,mu,m)
  ans-=(2*d(mu,v)/z**2-8*x[mu]*x[v]/z**3)*2*x[r]/z**2*Sbar(u,m,mu,m)
  ans-=(2*d(mu,u)/z**2-8*x[mu]*x[u]/z**3)*2*x[r]/z**2*Sbar(v,m,mu,m)
 return s.expand(ans)
def derivative(f,i):return s.expand(s.diff(f,x[i])+2*x[i]*s.diff(f,z))
def C(u,v,r):return (-12*d(u,v)*x[r]-30*(d(u,r)*x[v]+d(v,r)*x[u]))/z**4+96*x[u]*x[v]*x[r]/z**5
for u,v,r in product(range(4),repeat=3):eq(Avec(u,v,r)+sum(derivative(B(j,u,v,r),j) for j in range(4)),C(u,v,r))

# Recover the complete seven-tensor O4 form, then verify it symbolically.
axis=dict(zip(x,(1,0,0,0)));axis[z]=1
def at(j,u,v,r):return B(j,u,v,r).subs(axis)
c0=at(1,2,2,1);c1=at(1,1,2,2);c2=at(0,1,1,0)-c0;c3=at(1,0,0,1)-c0
c4=at(1,1,0,0)-c1;c5=at(0,1,0,1)-c1;c6=at(0,0,0,0)-c0-2*c1-c2-c3-2*c4-2*c5
coeff=[c0,c1,c2,c3,c4,c5,c6]
def reconstructed(j,u,v,r):
 terms=[d(j,r)*d(u,v),d(j,u)*d(v,r)+d(j,v)*d(u,r),d(u,v)*x[j]*x[r],d(j,r)*x[u]*x[v],
        d(j,u)*x[v]*x[r]+d(j,v)*x[u]*x[r],d(u,r)*x[j]*x[v]+d(v,r)*x[j]*x[u],x[j]*x[u]*x[v]*x[r]]
 return sum(c*t/z**n for c,t,n in zip(coeff,terms,[3,3,4,4,4,4,5]))
for j,u,v,r in product(range(4),repeat=4):eq(B(j,u,v,r),reconstructed(j,u,v,r))
put('B_COEFFICIENTS.json',dict(coefficients=[str(c) for c in coeff],cpu_seconds=time.process_time()-cpu))
print('B coefficients',coeff,flush=True)

# Independent existing bitensor jets, with no fitting to the reduced source.
def existing_B(J,j,u,v,r):
 ans=0
 for m,mu,nu in product(range(4),repeat=3):
  for c,e,xi,gxi in [(u,v,m,-1),(u,m,-1,v),(v,m,-1,u)]:
   g=J.jet('ghost',0,(m,nu),gxi,mu)
   if not g:continue
   h=0
   if j==mu:h+=J.jet('metric',0,(c,e,r,nu),xi)
   if j==nu:h+=J.jet('metric',0,(c,e,mu,r),xi)
   if mu==nu:h-=J.jet('metric',0,(c,e,j,r),xi)
   ans-=g*h
 return s.expand(ans)
for point in [(1,0,0,0),(1,2,-1,1)]:
 J=SourcePoint(point);sub=dict(zip(x,point));sub[z]=sum(v*v for v in point)
 for j,u,v,r in [(1,2,2,1),(1,1,2,2),(0,1,1,0),(1,0,0,1),(1,1,0,0),(0,1,0,1),(0,0,0,0),(2,0,3,1)]:eq(existing_B(J,j,u,v,r),B(j,u,v,r).subs(sub))

# Reuse pure definitions from the already audited prior runner only;
# no top-level I/O or old checks are executed.
ns=dict(s=s,x=x,z=z,Q=Q,R=R,lru_cache=lru_cache,product=product,delta=d)
tree=ast.parse((H/'source_adjoint_cutoff_check.py').read_text('utf-8'))
names={'dx','flat_e','monomials','residue','multiply_delta','first'}
defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==len(names)
exec(compile(ast.Module(body=defs,type_ignores=[]),'source_adjoint_cutoff_pure_defs','exec'),ns)
flat_e,residue=ns['flat_e'],ns['residue'];reg=[2*a*t/z for t in x]
contacts={};cross={};nonzero=0
for ydirection in (0,1):
 h=s.Matrix(4,4,lambda u,v:-B(ydirection,u,v,0))
 base=flat_e(h,reg);withx=flat_e(h,[reg[i]+lam*d(i,0) for i in range(4)])
 for u,v in product(range(4),repeat=2):
  contact=-residue(s.expand(base[u,v]).coeff(a,1))
  correction=-residue(s.expand(withx[u,v]-base[u,v]).coeff(a,1).coeff(lam,1))
  eq(s.expand(withx[u,v]-base[u,v]).coeff(a,1).coeff(lam,2),0)
  contacts[str((ydirection,u,v))]=str(contact);cross[str((ydirection,u,v))]=str(correction)
  if contact or correction:nonzero+=1
 # Check E commutator identity on constant multiplication: no contact
 # can arise from a bare second derivative of the cutoff alone.
 eq(sum(s.expand(withx[i,i]-base[i,i]).coeff(a,1).coeff(lam,2) for i in range(4)),0)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-cpu,
 B_coefficients=[str(c) for c in coeff],Y_cutoff_E_contact_over_C_E=contacts,XY_cutoff_contact_over_C_E=cross,
 nonzero_components=nonzero,convention='R E-E R,source correction h=-(dchiY)B; chiX multiplier retained',
 full_Q2=False,scope='flat source X commutator on new Y cutoff term; not Y regulator correction nor full loop cutoff identity',gate_changed=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'B_COEFFICIENTS.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if not isinstance(v,dict)}))
