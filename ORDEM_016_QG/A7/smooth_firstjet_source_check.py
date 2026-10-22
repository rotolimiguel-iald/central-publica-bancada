"""Compute previously excluded first smooth jets in the flat source contact.

No imports of runners or prescriptions selected; all comparisons exact.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from logarithmic_contact_engine import contact

H=Path(__file__).resolve().parent;D=H/'smooth_firstjet_source';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p
    raw=json.dumps(v,ensure_ascii=False,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(raw)
    assert t.read_bytes()==raw;t.replace(p)
sources=[Path(__file__),H/'curved_source_jet_engine.py',H/'smooth_source_contact_check.py',
         H/'logarithmic_contact_engine.py',H/'smooth_source_rotation/DERIVACAO.md']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Flat hdagger-c contact with first Y jets of smooth metric and ghost lines',
    units='C_E and common propagator prefactors stripped; real derivatives',
    fixed_prescription='Mixed singular XY second derivative has contact +delta_ij/4; lower derivatives uniquely integrable',
    method='Enumerate original source vertex, then closed tensor formula; no W bisolution/positivity assumed',
    exclusions=['curvature','higher local diagrams','full Q2'],
    sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
cpu=time.process_time();checks=[]
def ck(n,v):
    assert s.expand(v)==0,(n,s.expand(v));checks.append(n)
def d(a,b):return int(a==b)
def symI(a,b,c,e):return s.Rational(d(a,c)*d(b,e)+d(a,e)*d(b,c),2)
def S(a,b,c,e):return symI(a,b,c,e)-s.Rational(d(a,b)*d(c,e),2)
labels=[(a,b) for a in range(4) for b in range(a,4)]
lookup={pair:k for k,pair in enumerate(labels)}
def idx(a,b):return lookup[tuple(sorted((a,b)))]
# Check the extension tensor used to select the two critical contractions.
for a in range(4):
 for b in range(4):ck(('XYcontact',a,b),-contact(1,0,(a,b))-s.Rational(d(a,b),4))

# dW[r,a,b,c,e] is the first Y derivative. At the diagonal it need not
# itself have pair-exchange symmetry; only W(X,Y)=W(Y,X)^T relates X/Y jets.
# Exhaust the 4*10*10 unsymmetrized pair basis (includes admissible subspaces).
metric_checks=0
for r in range(4):
 for left in range(10):
  for right in range(10):
   def W(a,b,c,e):return int(idx(a,b)==left and idx(c,e)==right)
   for a,b in labels:
    # Direct original 2 h_am partial_b c^m source with ghost critical line;
    # symmetrize external hdagger indices. No invisible multiplicity factor.
    def raw(a,b):
     return -sum(W(a,m,b,m)-s.Rational(d(b,m),2)*sum(W(a,m,al,al) for al in range(4))
                 for m in range(4))/2
    actual=(raw(a,b)+raw(b,a))/2
    Sab=sum(W(a,m,b,m) for m in range(4))
    Sba=sum(W(b,m,a,m) for m in range(4))
    Tr=sum(W(a,b,al,al) for al in range(4))
    expected=-(Sab+Sba-Tr)/4
    ck(('metric_firstjet',r,left,right,a,b),actual-expected);metric_checks+=1

# Smooth ghost with one Y derivative, metric critical line in c^m partial_m h.
# T_ab symmetric, so coefficient is symmetrized in a,b. Full4^3 jet basis.
for mu0 in range(4):
 for m0 in range(4):
  for nu0 in range(4):
   def U(mu,m,nu):return int(mu==mu0 and m==m0 and nu==nu0)
   for r in range(4):
    for a,b in labels:
     actual=-sum(s.Rational(d(m,r),4)*U(mu,m,nu)*
         (S(a,b,mu,nu)-s.Rational(d(mu,nu),2)*sum(S(a,b,al,al) for al in range(4)))
          for m in range(4) for mu in range(4) for nu in range(4))
     expected=-s.Rational(1,8)*(U(a,r,b)+U(b,r,a))
     ck(('ghost_firstjet',mu0,m0,nu0,r,a,b),actual-expected)

# Isotropic center-dependent references: Y derivative = half diagonal derivative.
x=s.symbols('x0:4');c=s.Matrix(s.symbols('c0:4'));grad=s.Matrix(s.symbols('d0:4'))
for sector in ['I','T']:
 def W(a,b,c,e):return symI(a,b,c,e) if sector=='I' else d(a,b)*d(c,e)
 for a,b in labels:
  raw=-sum(W(a,m,b,m)-s.Rational(d(b,m),2)*sum(W(a,m,al,al) for al in range(4)) for m in range(4))/2
  expected=(-1 if sector=='I' else s.Rational(1,2))*d(a,b)
  ck(('isotropic_Yjet',sector,a,b),raw-expected)

def lap(f):return sum(s.diff(f,t,2) for t in x)
def E(h):
 tr=s.trace(h)
 C=s.Matrix([sum(s.diff(h[i,j],x[j]) for j in range(4))-s.diff(tr,x[i])/2 for i in range(4)])
 div=sum(s.diff(C[i],x[i]) for i in range(4))
 return s.Matrix(4,4,lambda a,b:s.expand(-lap(h[a,b])+d(a,b)*lap(tr)/2+
       s.diff(C[b],x[a])+s.diff(C[a],x[b])-d(a,b)*div))
w=x[0]**3-3*x[0]*x[1]**2
ck('harmonic_w',lap(w))
cv=s.Matrix([1,0,0,0]);dw=s.Matrix([s.diff(w,t) for t in x])
AI=-s.eye(4)*cv.dot(dw)/2
AT=s.eye(4)*cv.dot(dw)/4
AG=-(cv*dw.T+dw*cv.T)/16
ei,et,eg=E(AI),E(AT),E(AG)
for a in range(4):
 for b in range(4):
  ck(('metricI_counter',a,b),ei[a,b]-s.diag(6,-6,0,0)[a,b])
  ck(('metricT_counter',a,b),et[a,b]-s.diag(-3,3,0,0)[a,b])
  ck(('ghost_puregauge',a,b),eg[a,b])
assert ei!=s.zeros(4)

result=dict(at=datetime.now(timezone.utc).isoformat(),
 status='FIRST_SMOOTH_JET_SOURCE_CONTACT_EXPLICIT',checks=len(checks),cpu_seconds=time.process_time()-cpu,
 metric_formula='A_H,ab^r=-(sum_m dYr W_am|bm + sum_m dYr W_bm|am - sum_l dYr W_ab|ll)/4',
 ghost_formula='A_G,ab^r=-(dYa W_G^r|b + dYb W_G^r|a)/8',
 isotropic_center_formulas={'I':'-g_ab c.grad(wI)/2','T':'+g_ab c.grad(wT)/4',
    'G':'-(c_a grad_b(wG)+c_b grad_a(wG))/16'},
 counterexample=dict(w=str(w),c=[1,0,0,0],laplacian_w=0,
    E_AI=list(map(str,ei)),E_AT=list(map(str,et)),E_AG=list(map(str,eg)),
    scope='Formal local jets; harmonic center scalar only; not positive state or BRST-compatible pair'),
 implication='At frozen inhomogeneous reference, a metric-only primitive NG cannot account for E A c with constant c (Gc=0). Other Ward sectors/reference transport remain required.',
 no_reference_selected=True,full_Q2=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='counterexample'},ensure_ascii=False))
