"""Finite graded BV check of inhomogeneous consistency with classical breaking."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s

H=Path(__file__).resolve().parent;D=H/'inhomogeneous_bv_consistency';D.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
 p=D/n;assert not p.exists();b=json.dumps(v,indent=2).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
x,y,g=s.symbols('x y g')
def clean(P):return {m:s.expand(c) for m,c in P.items() if s.expand(c)!=0}
def add(*Ps):
 out={}
 for P in Ps:
  for m,c in P.items():out[m]=out.get(m,0)+c
 return clean(out)
def scale(P,a):return clean({m:a*c for m,c in P.items()})
def mul(A,B):
 out={}
 for u,a in A.items():
  for v,b in B.items():
   if set(u)&set(v):continue
   sign=(-1)**sum(i>j for i in u for j in v);m=tuple(sorted(u+v))
   out[m]=out.get(m,0)+sign*a*b
 return clean(out)
def derivative(P,var):return clean({m:s.diff(c,var) for m,c in P.items()})
def oddleft(P,i):
 out={}
 for m,c in P.items():
  if i not in m:continue
  n=m.index(i);out[m[:n]+m[n+1:]]=(-1)**n*c
 return clean(out)
def parity(P):
 values={len(m)%2 for m in P};assert len(values)<=1
 return next(iter(values),0)
def oddright(P,i):return scale(oddleft(P,i),(-1)**(parity(P)+1))
def bracket(A,B):
 # Even fields x,y with odd antifields xi,eta; ghosts c1,c2 are spectators.
 out={}
 for variable,antifield in [(x,0),(y,1)]:
  out=add(out,mul(derivative(A,variable),oddleft(B,antifield)),
          scale(mul(oddright(A,antifield),derivative(B,variable)),-1))
 return out
def serial(P):return [{'odd_word':m,'coefficient':str(c)} for m,c in P.items()]
start=time.process_time();checks=0
def eq(a,b):
 global checks
 assert add(a,scale(b,-1))=={},(a,b);checks+=1
eq(bracket({():x},{(0,):1}),{():1})
eq(bracket({(0,):1},{():x}),{():-1})
results=[]
for f,W in [(x,{():x*x/2}),(x*x+y,{():x*y+y**3}),(x*y+y*y,{():x**3+y*y})]:
 S0={(0,2):s.Integer(1),(1,3):s.Integer(1)}
 V={(0,3):f};S=add(S0,scale(V,g))
 I=scale(bracket(S,S),s.Rational(1,2));Q1=bracket(S,W)
 homogeneous=bracket(S,Q1);inhomogeneous=bracket(W,I)
 eq(bracket(S,I),{})
 eq(add(homogeneous,inhomogeneous),{})
 assert I and homogeneous and inhomogeneous;checks+=3
 # At g=0 classical master breaking disappears and homogeneous identity recovers.
 eq(clean({m:c.subs(g,0) for m,c in homogeneous.items()}),{})
 results.append(dict(f=str(f),W=serial(W),classical_breaking=serial(I),quantum_first_variation=serial(Q1),
  homogeneous_defect=serial(homogeneous),required_inhomogeneous_term=serial(inhomogeneous)))
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
 identity='I={S,S}/2, Q1={S,W} => {S,Q1}+{W,I}=0 by graded Jacobi',
 formal_application='For a nonzero cutoff-dependent classical BV breaking, do not demand homogeneous consistency without including the insertion/descent terms',
 examples=results,scope='Finite exact controls of the algebraic identity, not the calculated gravitational Q2',
 not_claimed='No identification of W with the full effective action or cancellation of the measured local matrix',
 full_Q2=False,gate_changed=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'results.json']]))
print(json.dumps(result,ensure_ascii=False))
