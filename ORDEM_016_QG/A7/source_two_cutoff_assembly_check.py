"""Assemble both endpoint cutoffs for the fixed flat source distribution."""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
from functools import lru_cache
import ast,json,hashlib,time,uuid
import sympy as s
import logarithmic_contact_engine as R
import einstein_radial_aux_engine as E
H=Path(__file__).resolve().parent;D=H/'source_two_cutoff_assembly';D.mkdir(exist_ok=False)
x=E.x;z=E.radial_z;Q=R.Q;a,lam=s.symbols('a lam')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,o):
 p=D/n;assert not p.exists();b=json.dumps(o,ensure_ascii=False,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
sources=[Path(__file__),H/'source_Y_cutoff_v2/B_COEFFICIENTS.json',H/'source_adjoint_cutoff_check.py',H/'source_Y_cutoff_check_v2.py',H/'bilocal_Y_regulator/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='P-Q=-C_E(chiX H)+E_X[chiX chiY C_divY(B)] with H=chiY C-dchiY.B',
 convention='C_D=R(Df)-D R(f), both cutoffs before source reduction, CE=-4pi²',
 reference='P=E chiX[chiY R A-divY(chiY R B)],Q=R E[chiX(chiY C-dchiY.B)]',
 tests='Y contact by first-derivative table and regulator residue; symbolic O4 reconstruction; full regulated P-Q versus assembled contact with chiX=exp(lambda x0), chiY jets 1,0/e0/e1',
 full_Q2=False,sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();checks=0
def d(i,j):return s.Integer(i==j)
def eq(f,g=0):
 global checks
 assert s.expand(f-g)==0,(f,g);checks+=1
ns=dict(s=s,x=x,z=z,Q=Q,R=R,lru_cache=lru_cache,product=product,delta=d)
names={'dx','flat_e','monomials','residue','multiply_delta','first'}
tree=ast.parse((H/'source_adjoint_cutoff_check.py').read_text('utf-8'));defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==len(names)
exec(compile(ast.Module(body=defs,type_ignores=[]),'source_contact_pure','exec'),ns)
flat_e,residue,first=ns['flat_e'],ns['residue'],ns['first']
coeff=[s.Rational(v) for v in json.loads(sources[1].read_bytes())['coefficients']]
@lru_cache(None)
def B(j,u,v,r):
 terms=[d(j,r)*d(u,v),d(j,u)*d(v,r)+d(j,v)*d(u,r),d(u,v)*x[j]*x[r],d(j,r)*x[u]*x[v],
        d(j,u)*x[v]*x[r]+d(j,v)*x[u]*x[r],d(u,r)*x[j]*x[v]+d(v,r)*x[j]*x[u],x[j]*x[u]*x[v]*x[r]]
 return s.expand(sum(c*t/z**n for c,t,n in zip(coeff,terms,[3,3,4,4,4,4,5])))
def C(u,v,r):return (-12*d(u,v)*x[r]-30*(d(u,r)*x[v]+d(v,r)*x[u]))/z**4+96*x[u]*x[v]*x[r]/z**5
DY={};rawY={}
for r in range(4):
 rawY[r]=s.Matrix(4,4,lambda u,v:s.expand(2*sum(x[j]*B(j,u,v,r) for j in range(4))/z))
 DY[r]=s.Matrix(4,4,lambda u,v:residue(rawY[r][u,v]))
 for u,v in product(range(4),repeat=2):
  eq(DY[r][u,v],-sum(first(B(j,u,v,r),j) for j in range(4)))
  # Compare the unextended regulator term to the original separate Y-stage.
  expected=(-12*d(u,v)*x[r]+32*(d(u,r)*x[v]+d(v,r)*x[u]))/z**4
  num,den=s.fraction(s.cancel(rawY[r][u,v]-expected));eq(s.rem(num,E.Z-z,x[0]))
q2=sum(t*t for t in Q);uu,vv,ww=s.symbols('uu vv ww');eqs=[]
def pred(u,v,r):return uu*d(u,v)*Q[r]*q2+vv*(d(u,r)*Q[v]+d(v,r)*Q[u])*q2+ww*Q[u]*Q[v]*Q[r]
for u,v,r in [(1,1,0),(0,1,1),(0,0,0)]:eqs+=s.Poly(s.expand(pred(u,v,r)-DY[r][u,v]),*Q).coeffs()
sol=s.solve(eqs,(uu,vv,ww),dict=True);assert len(sol)==1
for u,v,r in product(range(4),repeat=3):eq(pred(u,v,r).subs(sol[0]),DY[r][u,v])

def epol(h):
 tr=s.trace(h);qhq=sum(Q[i]*Q[j]*h[i,j] for i,j in product(range(4),repeat=2))
 return s.Matrix(4,4,lambda u,v:s.expand(-q2*h[u,v]-Q[u]*Q[v]*tr+sum(Q[u]*Q[i]*h[i,v]+Q[v]*Q[i]*h[i,u] for i in range(4))+d(u,v)*(q2*tr-qhq)))
def res_lam(f):
 p=s.Poly(s.expand(f),lam)
 return s.expand(sum(lam**i[0]*residue(c) for i,c in p.terms()))
reg=[2*a*t/z for t in x];shift=[reg[i]+lam*d(i,0) for i in range(4)];plain=[lam*d(i,0) for i in range(4)]
rows=[];results={}
for gy in [-1,0,1]:
 # chiY(0)=1; gy=-1 means zero Y gradient, otherwise e_gy.
 h=s.Matrix(4,4,lambda u,v:C(u,v,0)-(B(gy,u,v,0) if gy>=0 else 0))
 reg_image=flat_e(h,shift);normal_image=flat_e(h,plain)
 # Full regulated P-Q: the extra a*rawY comes from differentiating z^a
 # in Y before applying E at X. No contact is inserted by hand here.
 full=reg_image-normal_image+flat_e(a*rawY[0],shift)
 # Assemble using the separately computed distribution contacts.
 xcomm=(reg_image-normal_image).applyfunc(lambda f:-res_lam(s.expand(f).coeff(a,1)))
 shiftedY=DY[0].applyfunc(lambda f:s.expand(f.subs(Q[0],Q[0]-lam)))
 eY=epol(shiftedY)
 for u,v in product(range(4),repeat=2):
  direct=res_lam(s.expand(full[u,v]).coeff(a,1)).subs(Q[0],Q[0]-lam).expand()
  assembled=-xcomm[u,v].subs(Q[0],Q[0]-lam)+eY[u,v]
  eq(direct,assembled)
  results[str((gy,u,v))]=str(direct)
 sample=s.expand(assembled) if False else s.sympify(results[str((gy,1,1))],locals={'lam':lam,**{str(q):q for q in Q}})
 rows.append(dict(Y_gradient=gy,component=[1,1,0],polynomial=str(sample),at_q_e0_lambda1=str(sample.subs(dict(zip(Q,(1,0,0,0)))).subs(lam,1)),at_constant_X=str(sample.subs(lam,0))))
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-cpu,
 Y_contact_rank3_coefficients=[str(sol[0][t]) for t in (uu,vv,ww)],Y_contact_basis='delta_ab qr q²; (delta_ar qb+delta_br qa)q²; qa qb qr',
 controls=rows,values=results,scope='Complete flat source endpoint-localization contact relative to specified Q, not full metric/ghost Ward',full_Q2=False,gate_changed=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='values'}))
