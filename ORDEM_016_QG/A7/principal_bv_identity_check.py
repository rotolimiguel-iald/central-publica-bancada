"""Check logarithmic hc BV sector and a local ghost-change candidate, not full QME."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import json,hashlib
import sympy as s
HERE=Path(__file__).resolve().parent;DEST=HERE/'principal_bv_identity';DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode();assert not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),antifield_sha256=sha(HERE/'antifield_vertex/results.json'),
    metric_sha256=sha(HERE/'metric_bubble_v2/results.json'),
    targets=['K^T Sigma_log + H_ungauged R_log in hc sector',
             'R_log=K F local polynomial, antighost QF relation',
             'field-coordinate change completion of bracket, not measured triangle'],
    not_claimed='finite causal anomaly, full curved Slavnov identity, or complete one-loop effective action'))
start,cpu=perf_counter(),process_time();checks=[];neg=[]
def check(name,expr):
    ok=all(s.expand(v)==0 for v in expr) if isinstance(expr,s.MatrixBase) else s.expand(expr)==0
    assert ok,(name,expr);checks.append(name)
def reject(name,expr):
    assert any(s.expand(v)!=0 for v in expr) if isinstance(expr,s.MatrixBase) else s.expand(expr)!=0
    neg.append(name)
ar=json.loads((HERE/'antifield_vertex/results.json').read_bytes())
mr=json.loads((HERE/'metric_bubble_v2/results.json').read_bytes())
a,b,c=map(s.sympify,ar['coefficients_over_A0']);coef=list(map(s.sympify,mr['combined_Hessian_coefficients_over_hbar_A0']))
p=s.Matrix(s.symbols('p0:4'));v=s.Matrix(s.symbols('v0:4'));p2=p.dot(p);pv=p.dot(v)
H=s.zeros(4)
for n,(i,j) in enumerate((i,j) for i in range(4) for j in range(i,4)):H[i,j]=H[j,i]=s.Symbol(f'h{n}')
def gauge(k,w):return k*w.T+w*k.T
def F(k,w):return a*k.dot(k)*w+b*k*k.dot(w)/2
R=a*p2*gauge(p,v)+b*p*p.T*pv+c*p2*s.eye(4)*pv
check('R_is_gauge_of_local_F',R-gauge(p,F(p,v)))
Ric=(p2*R+p*p.T*s.trace(R)-p*(R*p).T-(R*p)*p.T)/2
Ein=Ric-s.eye(4)*s.trace(Ric)/2
check('Einstein_ungauged_annihilates_R',Ein)
def invariant(A,B):
    pa=(p.T*A*p)[0];pb=(p.T*B*p)[0]
    return [s.trace(A*B)*p2**2,s.trace(A)*s.trace(B)*p2**2,
            (pa*s.trace(B)+pb*s.trace(A))*p2,(p.T*A*B*p)[0]*p2,pa*pb]
ward_metric=sum(k*x for k,x in zip(coef,invariant(gauge(p,v),H)))
check('Sigma_log_annihilates_K',ward_metric)
# The two contributions vanish separately; their not-yet-fixed relative phase is immaterial here.
z=s.Symbol('z')
check('log_hc_identity_for_any_relative_normalization',ward_metric+z*s.trace(H*Ein))
C_R=R*p-p*s.trace(R)/2
check('C_K_F_is_p_squared_F',C_R-p2*F(p,v))
ghost_kernel=-C_R
check('antighost_Q_F_relation',ghost_kernel-(-p2)*F(p,v))
reject('erasing_nonzero_source_F',F(p,v))
reject('trace_only_spurious_source_not_in_Einstein_kernel',p2**2*(p*p.T-p2*s.eye(4))*pv)

# Algebraic coordinate change U=I+eps F transports any Lie bracket.
# Test its first-order Jacobi on Fourier vector fields; strip a common i.
def bracket(k,u,l,w):return u.dot(l)*w-w.dot(k)*u
def correction(k,u,l,w):
    return bracket(k,F(k,u),l,w)+bracket(k,u,l,F(l,w))-F(k+l,bracket(k,u,l,w))
mom=[s.Matrix([1,-1,0,1]),s.Matrix([0,1,2,-1]),s.Matrix([2,0,-1,1])]
axes=[s.eye(4)[:,j] for j in range(4)]
nonzero=0
for i in range(4):
    for j in range(4):
        for k in range(4):
            fields=list(zip(mom,[axes[i],axes[j],axes[k]]))
            ordinary=s.zeros(4,1);linear=s.zeros(4,1)
            for shift in range(3):
                (p0,v0),(p1,v1),(p2_,v2)=fields[shift:]+fields[:shift]
                B=bracket(p1,v1,p2_,v2);D=correction(p1,v1,p2_,v2)
                ordinary+=bracket(p0,v0,p1+p2_,B)
                linear+=bracket(p0,v0,p1+p2_,D)+correction(p0,v0,p1+p2_,B)
                if any(D):nonzero+=1
            check(f'Jacobi_ordinary_{i}_{j}_{k}',ordinary)
            check(f'Jacobi_linear_coordinate_change_{i}_{j}_{k}',linear)
assert nonzero
result=dict(statute='REAL_PRINCIPAL_LOG_HC_BV_IDENTITY_AND_COORDINATE_CHANGE_CHECK',
    checks_passed=len(checks),checks=checks,negative_controls=neg,
    F_coefficients=[str(a),str(b/2)],nonzero_bracket_corrections=nonzero,
    ghost_kernel_form='+3/8 p^4 I -1/4 p² p p^T, unweighted',
    measured_nonlinear_quantum_bracket=False,finite_causal_anomaly_computed=False,
    full_Q2=False,gate_changed=False,source_sha256=sha(Path(__file__)),
    plan_sha256=sha(DEST/'PRE_REGISTER.json'),wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu)
new(DEST/'results.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False))
