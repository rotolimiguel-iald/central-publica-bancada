"""Check the flat normalization before extracting first-curvature singular jets."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time
import sympy as s
import curved_source_jet_engine as e
H=Path(__file__).resolve().parent;O=H/'curved_source_jet';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):
    p=O/name;assert not p.exists(),p
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode();t=p.with_suffix('.tmp');t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    scope='Normal-coordinate first-K singular parametrix contribution, NOT full curved causal amplitude',
    engine_sha256=sha(H/'curved_source_jet_engine.py'),
    flat_reference_sha256=sha(H/'antifield_vertex/results.json'),
    fixed=['metric and ghost endpoints Y=0, X=x', 'same source/ghost vertex signs as prior Fourier numerator',
           'normal metric g=delta-K(delta z-xx)/3', 'parallel P=I+K(delta z-xx)/6 at Y=0',
           'include first Y derivative before specialization',
           'metric V0=+K delta_ab delta_cd/2; ghost V0=-5K delta/4',
           'smooth W jets remain omitted and named, not set zero as a physical state'],
    acceptance='Reproduce flat three coefficients first; then extract both L and constant first-K angular terms',
    exclusions=['full Lorentzian continuation','smooth state contribution','finite contact','full Q2']))
start=time.process_time();checks=[]
def ck(n,value):
    assert s.expand(value)==0,(n,value);checks.append(n)
axes=[s.eye(4)[:,i] for i in range(4)]
p=axes[0]; fits=[]
for i,j,v in [(0,1,axes[1]),(1,1,axes[0]),(0,0,axes[0])]:
    T=s.zeros(4);T[i,j]=T[j,i]=1;fits.append((T,v))
flat=[];curved=[]
for i,(T,v) in enumerate(fits):
    got=e.local_log_profile(T,v,p,0);flat.append(got)
    expected=-s.Rational(3,4)*(v.T*T*p)[0]+s.Rational(1,2)*(p.T*T*p)[0]*(p.dot(v))
    print(json.dumps(dict(stage='flat',i=i,got=str(got),expected=str(expected))),flush=True)
    ck('flat_reference_'+str(i),got-expected)
for i,(T,v) in enumerate(fits):
    got=e.local_log_profile(T,v,p,1);curved.append(got)
    print(json.dumps(dict(stage='curved',i=i,got=str(got))),flush=True)
M=s.Matrix([[2*(v.T*T*p)[0],s.trace(T)*p.dot(v)] for T,v in fits])
sol=M.gauss_jordan_solve(s.Matrix(curved))[0]
for i in range(3):ck('curvature_covariant_fit_'+str(i),(M*sol)[i]-curved[i])
put('results.json',dict(status='CONDITIONAL_SINGULAR_PROFILE_ONLY',checks=len(checks),check_names=checks,
    flat_values=list(map(str,flat)),curved_values=list(map(str,curved)),
    basis=['2(v.T.p)','tr(T)(p.v)'],curved_coefficients=list(map(str,sol)),
    cpu_seconds=time.process_time()-start,smooth_W_included=False,finite_extension_applied=False,full_Q2=False))
put('manifest.json',dict(artifacts=[dict(path=str(q),sha256=sha(q)) for q in
    [H/'curved_source_jet_engine.py',H/'curved_source_jet_check.py',O/'PRE_REGISTER.json',O/'results.json']]))
print(json.dumps({'status':'PASS','checks':len(checks),'cpu_seconds':time.process_time()-start}),flush=True)
