"""Audit the signs of the nonlinear descent in the received skeptical review."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'kimi_curved_ward_review';D.mkdir(exist_ok=True)
response=H/'bilocal_bulk_closure_delivery/KIMI_CURVED_WARD_RESPONSE.md'
old=H/'local_quadratic_ward_primitive/results.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p;b=json.dumps(v,indent=2).encode()
    q=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);q.write_bytes(b);assert q.read_bytes()==b;q.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Existing coefficient consistency and sign of O2 under A1=-s0 B and WZ s0 A2+s1 A1=0',
    sources=[dict(path=str(p),sha256=sha(p)) for p in [response,old,Path(__file__)]],
    full_Q2=False,no_new_counterterm_adopted=True))
cpu=time.process_time();j=json.loads(old.read_bytes());t=s.Symbol('t',real=True)
first=[s.sympify(v,locals={'t':t}) for v in j['first_K_Hessian']]
second=[s.sympify(v,locals={'t':t}) for v in j['second_K_Hessian']]
checks=[]
def ck(label,f):
    if isinstance(f,s.MatrixBase):assert f==s.zeros(*f.shape),(label,f)
    else:assert s.expand(f)==0,(label,f)
    checks.append(label)
for i,v in enumerate([s.Rational(1,2)-t/2,s.Rational(9,4)+t/2,-1-t/2,-1-t/2,t]):ck(('first',i),first[i]-v)
for i,v in enumerate([t+s.Rational(7,3),-t-s.Rational(22,3)]):ck(('second',i),second[i]-v)
# Plane symbol adjoint, symmetric fiber basis. The written derivative ordering
# is symmetrized, coefficients are parallel, and this verifies the transpose.
p=s.Matrix(s.symbols('p0:4'));p2=(p.T*p)[0];basis=[]
for a in range(4):
    for b in range(a,4):
        T=s.zeros(4);T[a,b]=T[b,a]=1;basis.append(T)
def dot(A,B):return sum(A[a,b]*B[a,b] for a in range(4) for b in range(4))
def symbol(T,o):
    if o==2:return second[0]*T+second[1]*s.eye(4)*s.trace(T)
    return first[0]*p2*T+first[1]*s.eye(4)*p2*s.trace(T)+first[2]*(p*p.T*s.trace(T)+s.eye(4)*(p.T*T*p)[0])+first[4]*(p*(p.T*T)+(T*p)*p.T)/2
for o in (1,2):
    for i,A in enumerate(basis):
        for k,B in enumerate(basis):ck(('fiber_transpose',o,i,k),dot(A,symbol(B,o))-dot(symbol(A,o),B))

# A finite exact exterior-algebra counterexample to the sign implication.
# Basis 1,eta,zeta,eta*zeta; s0 = eta wedge, s1 = zeta wedge.
s0=s.zeros(4);s0[1,0]=1;s0[3,2]=1
s1=s.zeros(4);s1[2,0]=1;s1[3,1]=-1
ck('nilpotent_s0',s0*s0);ck('nilpotent_s1',s1*s1);ck('anticommutation',s0*s1+s1*s0)
B=s.eye(4)[:,0];A1=-s0*B;A2=-s1*B
ck('A1_convention',A1+s0*B);ck('WZ_order2',s0*A2+s1*A1)
wrong=A2-s1*B;right=A2+s1*B
assert s0*wrong!=s.zeros(4,1)
ck('correct_obstruction_closed',s0*right)
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-cpu,
    status='QUADRATIC_SCOPE_RETAINED_NONLINEAR_DESCENT_SIGN_CORRECTED',
    retained='Existing firstK/K2 family and symmetric-fiber second-derivative construction',
    error='Section6 takes A1=-s0 B but uses O2=A2-s1 B; with anticommutation the closed combination is A2+s1 B',
    exact_counterexample=dict(basis=['1','eta','zeta','eta*zeta'],wrong_s0_O=list(map(str,s0*wrong)),
                              right_s0_O=list(map(str,s0*right))),
    correct_next_condition='A2+s1 B=-s0 B3 modulo total derivatives, for cancellation convention A+sB=0',
    conditional_parameter_note='If s0 S3+s1 S2=0 and d_t B=c S2, d_t O2=-c s0 S3; nonzero s1(d_t B) alone does not distinguish the cohomology class',
    no_nonlinear_diagrams_computed=True,full_Q2=False,prescription_changed=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),response,old,D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
