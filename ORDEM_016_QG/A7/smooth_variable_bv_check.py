"""Verify BV primitive including the first-jet source and local Green currents."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
from smooth_variable_ward_engine import gauge,einstein,source,hessian,green_current_N,green_current_E,einstein_coefficients
from smooth_mixed_gradient_engine import gradient_tensor
H=Path(__file__).resolve().parent;D=H/'smooth_variable_bv';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p;raw=json.dumps(v,ensure_ascii=False,indent=2).encode()
    q=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);q.write_bytes(raw);assert q.read_bytes()==raw;q.replace(p)
inputs=[Path(__file__),H/'smooth_variable_ward_engine.py',H/'smooth_mixed_gradient_engine.py',
 H/'smooth_firstjet_source/results.json',H/'smooth_mixed_gradient/results.json']
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='BV ghost0 primitive for variable isotropic smooth contact shift: B=-C_E(1/2 hN_w h+hdagger R_w c)',
    differential='s0 h=Gc; s0 hdagger=Eh; s0c=0; s0W=0 in this free variation',
    scope='Fixed flat smooth-relative two-vertex contact only, not full interacting Q2',
    sources=[dict(path=str(p),sha256=sha(p)) for p in inputs]))
cpu=time.process_time();checks=[]
def ck(n,v):assert s.expand(v)==0,(n,s.expand(v));checks.append(n)
def inner(a,b):return s.trace(a*b)
x=s.symbols('x0:4')
def div(j):return sum(s.diff(j[i],x[i]) for i in range(4))
C=einstein_coefficients()
for (a,b,i,j),value in C.items():ck(('E_fiber_adjoint',a,b,i,j),value-C.get((b,a,j,i),0))
cases=[]
for k in range(2):
 h=s.Matrix(4,4,lambda a,b: (a+b+1)*x[(a+b+k)%4]**2 + (1+a*b)*x[(a+k)%4]*x[(b+k)%4])
 c=s.Matrix([(a+1)*x[(a+k)%4]**3 + x[(a+1)%4]*x[(a+2)%4] for a in range(4)])
 w=1+x[k]**3-3*x[k]*x[(k+1)%4]**2+x[(k+2)%4]
 cases.append((h,c,w))
records=[]
for n,(h,c,w) in enumerate(cases):
 g=gauge(c,x);eh=einstein(h,x)
 for a in range(4):
  for b in range(4):ck(('EG',n,a,b),einstein(g,x)[a,b])
 for sector in ['metric_I','metric_T','ghost_I']:
  r=source(sector,c,w,x);nh=hessian(sector,h,w,x);ng=hessian(sector,g,w,x);er=einstein(r,x)
  jn=green_current_N(sector,h,g,w,x);je=green_current_E(h,r,x)
  ck(('greenN',n,sector),div(jn)-inner(h,ng)+inner(nh,g))
  ck(('greenE',n,sector),div(je)-inner(h,er)+inner(eh,r))
  # s0 of the ghost0 primitive density: minus sign for odd hdagger
  # multiplies s0(Rc)=0; the surviving first term is -(Eh).Rc.
  variation=-(inner(g,nh)+inner(h,ng))/2-inner(eh,r)
  ward=inner(h,ng+er)
  divergence=div([jn[i]/2+je[i] for i in range(4)])
  ck(('BV_density_identity',n,sector),variation+ward-divergence)
  records.append(dict(case=n,sector=sector,identity='s0b+h.(N_wG+ER_w)c=div(J_N/2+J_E)'))
  print('CASE',n,sector,'cpu',time.process_time()-cpu,flush=True)

# Constant ghost detects why the antifield term cannot simply be dropped.
w=x[0]**3-3*x[0]*x[1]**2;c=s.Matrix([1,0,0,0]);g=gauge(c,x)
assert g==s.zeros(4)
r=source('metric_I',c,w,x);er=einstein(r,x)
assert er==s.diag(6,-6,0,0)
h=s.diag(x[0]**2,0,0,0)
negative=s.expand(inner(h,er));assert negative==6*x[0]**2
result=dict(at=datetime.now(timezone.utc).isoformat(),
    status='VARIABLE_SMOOTH_RELATIVE_CONTACT_BV_PRIMITIVE_WITH_CURRENTS',
    checks=len(checks),cpu_seconds=time.process_time()-cpu,polynomial_cases=records,
    primitive='B=-C_E integral(1/2 h.N_w h+hdagger.R_w c)',
    identity='s0b=-C_E h.(N_wG+ER_w)c+C_E div(J_N/2+J_E)',
    degrees=dict(B=0,hdagger=-1,c=1,anomaly=1),
    negative_omit_antifield=str(negative),
    proof_scope='Universal algebraic proof uses measured tensor transpose, free s0 and Green currents; polynomial checks are independent controls, not extrapolation',
    no_counterterm_selected=True,full_Q2=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k!='polynomial_cases'},ensure_ascii=False))
