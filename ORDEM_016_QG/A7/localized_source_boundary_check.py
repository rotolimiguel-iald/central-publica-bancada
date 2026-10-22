"""Check full localized source against old zero-gradient data and raw residue."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
from functools import lru_cache
import ast,json,hashlib,time,uuid
import sympy as s
import logarithmic_contact_engine as R
from localized_source_boundary_engine import source_coefficients,source_reduced,source_extension,einstein,x,z,Q,dx,delta
from bilocal_source_divergence_engine import SourcePoint

H=Path(__file__).resolve().parent;D=H/'localized_source_boundary';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
 p=D/name;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'localized_source_boundary_engine.py',H/'full_loop_extension_engine.py',H/'source_two_cutoff_assembly/manifest.json',H/'source_adjoint_cutoff_check.py',H/'source_Y_cutoff_v2/B_COEFFICIENTS.json',H/'bilocal_source_divergence_engine.py']
for row in json.loads((H/'source_two_cutoff_assembly/manifest.json').read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),sources=[dict(path=str(p),sha256=sha(p)) for p in sources],
 target='Ghost boundary in source hstar/c loop, same pre-IBP density as paired ghosts',
 tests=['old unreduced B and reduced C','boundary source vs existing independent bitensor jets','direct regulated full Einstein vs assembled extension commutators','constant all40 source components'],
 full_Q2=False,scope='Flat rational singular source; three exponential local cutoff jets; no all diagram anomaly claim'))
start=time.process_time();checks=0
def eq(f,g=0):
 global checks
 assert s.expand(f-g)==0,(f,g);checks+=1
def radial_eq(f,g=0):
 global checks
 num,den=s.fraction(s.cancel(f-g));assert s.rem(num,sum(t*t for t in x)-z,x[0])==0,(f,g);checks+=1
zero=(0,0,0,0);coeff=list(map(s.Rational,json.loads((H/'source_Y_cutoff_v2/B_COEFFICIENTS.json').read_bytes())['coefficients']))
def oldB(j,u,v,r):
 terms=[delta(j,r)*delta(u,v),delta(j,u)*delta(v,r)+delta(j,v)*delta(u,r),delta(u,v)*x[j]*x[r],delta(j,r)*x[u]*x[v],
 delta(j,u)*x[v]*x[r]+delta(j,v)*x[u]*x[r],delta(u,r)*x[j]*x[v]+delta(v,r)*x[j]*x[u],x[j]*x[u]*x[v]*x[r]]
 return sum(c*t/z**n for c,t,n in zip(coeff,terms,[3,3,4,4,4,4,5]))
def oldC(u,v,r):return (-12*delta(u,v)*x[r]-30*(delta(u,r)*x[v]+delta(v,r)*x[u]))/z**4+96*x[u]*x[v]*x[r]/z**5
for u,v,r in product(range(4),repeat=3):
 A,B=source_coefficients(u,v,r,zero)
 for j in range(4):eq(B[j],oldB(j,u,v,r))
 radial_eq(source_reduced(u,v,r,zero),oldC(u,v,r))
print('Old source',checks,flush=True)

def independent_boundary(J,eta,j,u,v,r):
 ans=0
 for m,mu,nu in product(range(4),repeat=3):
  if not eta[mu]:continue
  for c,e,xi,gxi in [(u,v,m,-1),(u,m,-1,v),(v,m,-1,u)]:
   g=J.jet('ghost',0,(m,nu),gxi,-1)*eta[mu]
   if j<0:h=J.hj(0,c,e,mu,nu,xi,r)
   else:
    h=0
    if j==mu:h+=J.jet('metric',0,(c,e,r,nu),xi)
    if j==nu:h+=J.jet('metric',0,(c,e,mu,r),xi)
    if mu==nu:h-=J.jet('metric',0,(c,e,j,r),xi)
   ans-=g*h
 return s.expand(ans)
for point in [(1,0,0,0),(1,2,-1,1)]:
 J=SourcePoint(point);sub=dict(zip(x,point));sub[z]=sum(t*t for t in point)
 for eta in [(1,0,0,0),(0,1,0,0)]:
  for u,v,r in [(0,0,0),(1,1,0),(0,1,0),(0,2,1)]:
   A,B=source_coefficients(u,v,r,eta);A0,B0=source_coefficients(u,v,r,zero)
   eq((A-A0).subs(sub),independent_boundary(J,eta,-1,u,v,r))
   for j in range(4):eq((B[j]-B0[j]).subs(sub),independent_boundary(J,eta,j,u,v,r))
print('Boundary independent jets',checks,flush=True)

# Pure residue definitions only; old runner is never executed/imported.
ns=dict(s=s,x=x,z=z,Q=Q,R=R,lru_cache=lru_cache,product=product)
names={'monomials','residue'};tree=ast.parse((H/'source_adjoint_cutoff_check.py').read_text('utf-8'))
defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==len(names)
exec(compile(ast.Module(body=defs,type_ignores=[]),'source_residue_pure','exec'),ns);residue=ns['residue']
alpha=s.Symbol('alpha');rows=[];q2=sum(q*q for q in Q)
for label,lam,eta in [('constant',zero,zero),('Y_exp',zero,(1,0,0,0)),('XY_exp',(1,-1,0,0),(1,0,0,0))]:
 for r in range(4):
  actual=source_extension(r,lam,eta)
  if label=='constant':
   for u in range(4):
    for v in range(u,4):eq(actual[u,v],-s.Rational(3,32)*delta(u,v)*Q[r]*q2**2+s.Rational(3,32)*Q[u]*Q[v]*Q[r]*q2)
  if r==0:
   h=s.Matrix(4,4,lambda u,v:source_reduced(u,v,r,eta))
   rawY=s.Matrix(4,4,lambda u,v:2*sum(x[j]*source_coefficients(u,v,r,eta)[1][j] for j in range(4))/z)
   shifted=lambda f,i:s.expand(dx(f,i)+(lam[i]+2*alpha*x[i]/z)*f)
   normal=lambda f,i:s.expand(dx(f,i)+lam[i]*f)
   raw=einstein(h+alpha*rawY,shifted)-einstein(h,normal)
   for u,v in product(range(4),repeat=2):
    direct=residue(s.expand(raw[u,v]).coeff(alpha,1))
    direct=direct.subs({Q[i]:Q[i]-lam[i] for i in range(4)},simultaneous=True)
    eq(direct,actual[u,v])
  row=dict(case=label,r=r,components={str((u,v)):str(actual[u,v]) for u in range(4) for v in range(u,4)},value11_at2100=str(actual[1,1].subs(dict(zip(Q,(2,1,0,0))))))
  rows.append(row);put(label+'_r'+str(r)+'.json',row)
  print('Source contact',label,r,'checks',checks,'cpu',time.process_time()-start,flush=True)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,rows=rows,full_Q2=False,
 scope='Full ghost-boundary rational flat source contacts,10x4 basis for3 fixed cutoff configurations; no current insertions,curvature,tadpoles or fullQ2')
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(dict(checks=checks,cpu_seconds=result['cpu_seconds'])))
