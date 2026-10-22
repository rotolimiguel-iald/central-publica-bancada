"""Apply measured reference-change trace defect to the existing P4 Hessian."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'principal_harmonic_bridge';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
 p=D/n;assert not p.exists(),p;raw=json.dumps(v,ensure_ascii=False,indent=2).encode()
 q=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);q.write_bytes(raw);assert q.read_bytes()==raw;q.replace(p)
inp=H/'finite_principal_contact/results.json';audit=H/'harmonic_reference_audit/results.json'
inputs=[Path(__file__),inp,audit]
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Transfer the same measured principal quartic kernel between two differential references, retaining finite local defect',
 no_full_kernel_identification=True,sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
cpu=time.process_time();checks=[];old=json.loads(inp.read_bytes());table=json.loads(audit.read_bytes())
q=s.Matrix(s.symbols('q0:4'));q2=q.dot(q)
source=list(map(s.Rational,old['input_quartic_hessian_coefficients']))
npco=list(map(s.Rational,old['finite_contact_coefficients_over_C']))
def inv(A,B):
 a=(q.T*A*q)[0];b=(q.T*B*q)[0]
 return [q2**2*s.trace(A*B),q2**2*s.trace(A)*s.trace(B),
         q2*(s.trace(A)*b+s.trace(B)*a),q2*(q.T*A*B*q)[0],a*b]
def poly(A,B,coeff):return s.expand(sum(a*b for a,b in zip(coeff,inv(A,B))))
def lap(v):return s.expand(sum(s.diff(v,t,2) for t in q))
def delta(v):return s.expand(-3*q2*lap(v)/128-q2**2*lap(lap(v))/9216)
def ck(n,v):assert s.expand(v)==0,(n,s.expand(v));checks.append(n)
basis=[]
for a in range(4):
 for b in range(a,4):
  v=s.zeros(4);v[a,b]=v[b,a]=1;basis.append(v)
unknown=s.symbols('d0:5');eq=[]
qaxis={q[i]:int(i==0) for i in range(4)}
for A in basis:
 for B in basis:
  eq.append((delta(poly(A,B,source))-poly(A,B,unknown)).subs(qaxis))
sol=s.solve(eq,unknown,dict=True);assert len(sol)==1
dco=[sol[0][v] for v in unknown];nhco=[a-b for a,b in zip(npco,dco)]
monomial_table={tuple(r['indices']):r for r in table['quartic_basis']}
for a,A in enumerate(basis):
 for b,B in enumerate(basis):
  P=poly(A,B,source);defect=delta(P)
  ck(('defect_invariants',a,b),defect-poly(A,B,dco))
  from_basis=0
  for powers,co in s.Poly(P,*q).terms():
   idx=tuple(i for i,n in enumerate(powers) for _ in range(n))
   from_basis+=co*s.sympify(monomial_table[idx]['NH'])
  ck(('harmonic_basis',a,b),from_basis-poly(A,B,nhco))
  ck(('total_extension',a,b),poly(A,B,nhco)+defect-poly(A,B,npco))

negative=None
for b,B in enumerate(basis):
 for r in range(4):
  v=s.eye(4)[:,r];G=q*v.T+v*q.T
  ck(('principal_transverse',b,r),poly(G,B,source))
  diff=poly(G,B,dco)
  if negative is None and diff!=0:negative=dict(test_fiber=b,ghost=r,omitted_local_defect=str(diff))
assert negative is not None
result=dict(at=datetime.now(timezone.utc).isoformat(),
 status='MEASURED_PRINCIPAL_HESSIAN_REFERENCE_TRANSFER_WITH_LOCAL_DEFECT',
 checks=len(checks),cpu_seconds=time.process_time()-cpu,
 N_P_coefficients=list(map(str,npco)),N_H_coefficients=list(map(str,nhco)),
 N_P_minus_N_H_coefficients=list(map(str,dco)),
 negative_control=negative,
 relation='D_H-X_P=C_E*(N_P-N_H)delta for this same principal P4U2 kernel',
 full_Q2=False,full_actual_kernel_identified_with_P4U2=False,prescription_changed=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result,ensure_ascii=False))
