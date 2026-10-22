"""Connect the existing finite-contact primitive to its K² algebraic completion."""
from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
from itertools import permutations
from fractions import Fraction as F
import hashlib,json,time,uuid
import sympy as s
from oneform_second_curvature_engine_v2 import oneform_second,loop_gauge
H=Path(__file__).resolve().parent;D=H/'finite_contact_second_curvature_primitive';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
 p=D/n;assert not p.exists();raw=json.dumps(v,indent=2).encode();tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
 tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p)
prior=H/'bilocal_curved_contact_primitive/results.json'
contact=H/'bilocal_XY_extension_contact/results.json'
families=json.loads(prior.read_bytes())['families'];coefs=json.loads(contact.read_bytes())['coefficients_over_C_E']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Complete already computed finite-contact N4+K*N2 through K², leaving unknown actual K² contact coefficients u,v symbolic',
 exclusions='Does not compute actual curved distribution coefficients, prove normal-frame naturality, or nonlinear/cutoff consistency',
 reuse='Existing oneform_second/loop_gauge and earlier K² primitive method; no changes to them',
 sources=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),prior,contact,H/'oneform_second_curvature_engine_v2.py',H/'local_quadratic_ward_primitive_check.py']]))
start=time.process_time();checks=0
b,c,t,u,v=s.symbols('b c t u v',real=True);locals={str(x):x for x in [b,c,t,u,v]}
def eq(a,b):
 global checks
 assert s.expand(a-b)==0,(a,b);checks+=1

def operators(p,V):
 jet,gauge,symh=oneform_second(V,p)
 @lru_cache(None)
 def symv(word,r,o):
  words=set(permutations(word))
  return sum((jet(w,r,o) for w in words),F())/len(words)
 def lower_target(mode):
  co=[[s.Rational(x) for x in row] for row in coefs[mode]]
  out=s.zeros(4)
  for i in range(4):
   for j in range(4):
    aa,bb,cc=co[0]
    value=aa*sum(symv((r,k,k,l,l),r,2) for r in range(4) for k in range(4) for l in range(4)) if i==j else 0
    value+=bb*sum(symv((j,k,k,l,l),i,2)+symv((i,k,k,l,l),j,2) for k in range(4) for l in range(4))
    value+=cc*sum(symv((i,j,r,k,k),r,2) for r in range(4) for k in range(4))
    aa,bb,cc=co[1]
    if i==j:value+=aa*sum(symv((r,k,k),r,1) for r in range(4) for k in range(4))
    value+=bb*sum(symv((j,k,k),i,1)+symv((i,k,k),j,1) for k in range(4))
    value+=cc*sum(symv((i,j,r),r,1) for r in range(4))
    out[i,j]=s.expand(value)
  return out
 return symh,lower_target

inputs={mode:([s.sympify(x,locals=locals) for x in f['flat']],
              [s.sympify(x,locals=locals) for x in f['first']]) for mode,f in families.items()}
samples=[]
for p,V in [((1,0,0,0),(1,0,0,0)),((1,0,0,0),(0,1,0,0))]:
 symh,target=operators(p,V);samples.append((p,V,symh,target))
output={}
for mode,(flat,first) in inputs.items():
 rows=[];values=[]
 for p,V,symh,target in samples:
  diff=s.Matrix(loop_gauge(symh,flat,first,[F(0)]*2,2))-target(mode)
  pv=sum(x*y for x,y in zip(p,V))
  for i in range(4):
   for j in range(4):
    rows.append([p[i]*V[j]+p[j]*V[i],int(i==j)*pv]);values.append(diff[i,j])
 fit,params=s.Matrix(rows).gauss_jordan_solve(s.Matrix(values));assert not list(params);checks+=1
 second=[s.expand(u-fit[0]),s.expand((v-fit[1])/2)]
 output[mode]=dict(induced_residual=list(map(str,fit)),second_K_Hessian=list(map(str,second)))
 print(json.dumps(dict(mode=mode,family=output[mode],cpu=time.process_time()-start)),flush=True)

p=s.symbols('p0:4')
for r in range(4):
 V=tuple(int(i==r) for i in range(4));symh,target=operators(p,V);pv=p[r]
 for mode,(flat,first) in inputs.items():
  second=[s.sympify(x,locals=locals) for x in output[mode]['second_K_Hessian']]
  actual=s.Matrix(loop_gauge(symh,flat,first,second,2))
  wanted=target(mode)+s.Matrix(4,4,lambda i,j:u*(p[i]*V[j]+p[j]*V[i])+v*int(i==j)*pv)
  for value in actual-wanted:eq(value,0)
 print(json.dumps(dict(polarization=r,checks=checks,cpu=time.process_time()-start)),flush=True)

# Independent pointwise variation of the final, algebraic K² counterterm.
hvars=s.symbols('h0:10');pairs=[(i,j) for i in range(4) for j in range(i,4)]
h=s.zeros(4)
for z,(i,j) in zip(hvars,pairs):h[i,j]=h[j,i]=z
M=s.Matrix(4,4,lambda i,j:s.Symbol(f'dc{i}{j}'));Gc=M+M.T
functional=v*s.trace(h)**2/4+u*s.trace(h*h)/2
variation=sum(s.diff(functional,z)*Gc[i,j] for z,(i,j) in zip(hvars,pairs))
wanted=u*s.trace(h*Gc)+v*s.trace(h)*s.trace(M)
eq(variation,wanted)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 families=output,unknown_second_contact='K²[u*(nabla_a c_b+nabla_b c_a)+v*g_ab*div(c)]',
 primitive='N=N4+K*N2+K²(e1*Id+e2*g*tr), existing flat/first families retained, e1/e2 listed; B=-CE/2 integral h.Nh',
 theorem_scope='Formal parity-even natural h/c operator with stated derivative-degree filtration on a 4D constant-curvature background; compact support and geometric formal adjoint',
 inference='Conditional algebraic K² completion for any u,v; not a measurement of these coefficients and not a normalization choice',
 actual_second_curvature_contact_measured=False,nonlinear_Q2_complete=False,prescription_changed=False,gate_changed=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),prior,contact,D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
