"""Restricted flat hc contact is s0 exact; no subtraction adopted."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'bilocal_flat_contact_primitive';D.mkdir(exist_ok=True)
source=H/'bilocal_XY_extension_contact/results.json';data=json.loads(source.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,v):
    p=D/n;assert not p.exists(),p;b=json.dumps(v,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
put('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Selfadjoint fourth-order family N with N G=A_flat, all polynomial components, no parameter chosen',
    scope='Integrated hc, flat, compact support; not curved/nonlinear/cutoff complete Q2',
    sources=[dict(path=str(p),sha256=sha(p)) for p in [source,Path(__file__)]]))
cpu=time.process_time();u,v,w=map(s.Rational,data['coefficients_over_C_E']['geodesic'][0])
assert data['coefficients_over_C_E']['geodesic'][0]==data['coefficients_over_C_E']['coordinate'][0]
b,c=s.symbols('b c',real=True);q=s.Matrix(s.symbols('q0:4'));q2=(q.T*q)[0]
co=[v-c/2,u/2-b,b,c,w/2-b-c/2]
def dot(A,B):return sum(A[i,j]*B[i,j] for i in range(4) for j in range(4))
def gauge(V):return q*V.T+V*q.T
def op(T):
    return co[0]*q2*q2*T+co[1]*s.eye(4)*q2*q2*s.trace(T)+co[2]*q2*(q*q.T*s.trace(T)+s.eye(4)*(q.T*T*q)[0])+co[3]*q2*(q*(q.T*T)+(T*q)*q.T)/2+co[4]*q*q.T*(q.T*T*q)[0]
def ward(V):
    qv=(q.T*V)[0]
    return u*s.eye(4)*qv*q2*q2+v*gauge(V)*q2*q2+w*q*q.T*qv*q2
checks=[]
def ck(label,f):assert s.expand(f)==0,(label,f);checks.append(label)
basis=[]
for i in range(4):
    for j in range(i,4):
        T=s.zeros(4);T[i,j]=T[j,i]=1;basis.append(T)
for r in range(4):
    V=s.eye(4)[:,r];diff=op(gauge(V))-ward(V)
    for i in range(4):
        for j in range(4):ck(('NG=A',r,i,j),diff[i,j])
for i,A in enumerate(basis):
    for j,B in enumerate(basis):ck(('formal_adjoint_symbol',i,j),dot(A,op(B))-dot(op(A),B))
for i in range(4):
    for j in range(4):
        A=gauge(s.eye(4)[:,i]);B=gauge(s.eye(4)[:,j])
        ck(('graded_integrated_WZ',i,j),dot(A,op(B))-dot(B,op(A)))
assert ward(s.eye(4)[:,0])[1,1]!=0
result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-cpu,
    status='FLAT_HC_CONTACT_HAS_EXPLICIT_QUADRATIC_PRIMITIVE_FAMILY',
    ward_coefficients_over_C_E=list(map(str,[u,v,w])),Hessian_coefficients_over_C_E=list(map(str,co)),
    basis=['q4 I_sym','q4 metric_trace','q2*(qq trace+metric qq_contraction)','q2 sym(q tensor_q)','qq tensor_qq'],
    free_parameters=['b','c'],primitive='B_bc=-C_E/2 integral h.N_bc h, so s0 B_bc=-A_hc at K0',
    formal_adjoint_assumptions='Real constant coefficients, symmetrized derivative indices, compact support, flat background',
    prescription_changed=False,representative_selected=False,full_Q2=False,
    curved_completion=False,nonlinear_completion=False,switching_function_completion=False)
put('results.json',result);put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),source,D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
