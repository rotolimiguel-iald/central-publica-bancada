"""R88 exact local metric-density variation controls; not spacetime EOM proof."""
from pathlib import Path
import datetime, hashlib, itertools, json
import sympy as S
HERE=Path(__file__).resolve().parent
plan=json.loads((HERE/'EXACT_PLAN_R88.json').read_text(encoding='utf8'))
assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==plan['script_sha256']
with (HERE/'EXACT_STARTED_R88.json').open('x',encoding='utf8') as f:
 json.dump({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'plan_sha256':hashlib.sha256((HERE/'EXACT_PLAN_R88.json').read_bytes()).hexdigest(),'execution_count':1},f)
t=S.symbols('t',real=True);xi=S.Rational(1,6);R=S.Rational(5,7);Rdot=S.Rational(-2,9);F0=S.Rational(3,2)
metrics=[S.diag(1,-1,-1,-1),S.diag(S.Rational(3,2),-2,-3,-4)]
vectors=[S.Matrix([1,2,-1,3]),S.Matrix([2,-1,3,1])]
Fs=[S.Matrix([[0,1,2,0],[-1,0,3,1],[-2,-3,0,-2],[0,-1,2,0]]),S.Matrix([[0,2,-1,3],[-2,0,0,1],[1,0,0,2],[-3,-1,-2,0]])]
Hs=[S.diag(1,0,-2,1),S.Matrix([[0,1,0,0],[1,0,0,2],[0,0,0,0],[0,2,0,0]]),S.Matrix([[2,-1,1,0],[-1,3,0,1],[1,0,-1,2],[0,1,2,1]])]
checks=[];wrong=[]
def contract(X,Y):return sum(X[a,b]*Y[a,b] for a in range(4) for b in range(4))
for idx,(G,A,F,H) in enumerate(itertools.product(metrics,vectors,Fs,Hs)):
 Gt=G+t*H;g=G.inv();v=1/S.sqrt(-G.det());vt=1/S.sqrt(-Gt.det());u=(A.T*G*A)[0];ut=(A.T*Gt*A)[0]
 Q=contract(F,G*F*G);Qt=contract(F,Gt*F*Gt)
 Sab=F*G*F.T;T=Sab-g*Q/4
 du=contract(H,A*A.T);dQ=2*contract(H,Sab)
 D=vt*((F0+xi*ut)*(R+t*Rdot)-Qt/4)
 expected=v*(-S.trace(g*H)*((F0+xi*u)*R-Q/4)/2+xi*R*du+(F0+xi*u)*Rdot-dQ/4)
 values=[S.diff(ut,t).subs(t,0)-du,S.diff(Qt,t).subs(t,0)-dQ,S.diff(D,t).subs(t,0)-expected,contract(g.inv(),T)]
 for label,val in zip(['du','dF2','full_density','maxwell_trace4'],values):
  val=S.simplify(val);assert val==0,(idx,label,val);checks.append({'case':idx,'check':label,'residual':str(val)})
 omission=S.simplify(v*xi*R*du)
 if omission!=0:wrong.append({'case':idx,'omitted_metric_norm_residual':str(omission)})
# Literal complex extension has Re(Fbar G F^T) and Hermitian norm variation.
G=metrics[0];H=Hs[2];A=vectors[0]+S.I*vectors[1];F=Fs[0]+S.I*Fs[1];Gt=G+t*H
ut=(S.conjugate(A).T*Gt*A)[0];Qt=contract(S.conjugate(F),Gt*F*Gt)
C=S.re(S.conjugate(A)*A.T);Sab=S.re(S.conjugate(F)*G*F.T)
for label,val in [('complex_du',S.diff(ut,t).subs(t,0)-contract(H,C)),('complex_dF2',S.diff(Qt,t).subs(t,0)-2*contract(H,Sab))]:
 val=S.simplify(val);assert val==0,(label,val);checks.append({'check':label,'residual':str(val)})
assert wrong
result={'status':'PASS','exact_cases':24,'checks_count':len(checks),'checks':checks,'negative_omission_nonzero_count':len(wrong),'negative_omission_controls':wrong,'sympy':S.__version__,'scope':'pointwise inverse-metric variations and four-dimensional Maxwell trace; no integrated EOM/Noether/physical test','finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with (HERE/'EXACT_RESULT_R88.json').open('x',encoding='utf8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({k:result[k] for k in ['status','exact_cases','checks_count','negative_omission_nonzero_count']}))
