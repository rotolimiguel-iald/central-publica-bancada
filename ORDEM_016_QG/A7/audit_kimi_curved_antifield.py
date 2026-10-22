"""Check claimed geometric identities; do not run the supplied placeholder."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,time,uuid
import sympy as s
H=Path(__file__).resolve().parent;D=H/'kimi_curved_antifield_audit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,v):
    p=D/name;assert not p.exists(),p
    b=json.dumps(v,indent=2,ensure_ascii=False).encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
put('AUDIT_PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
 target='Normal-metric derivative, eikonal/scale, VanVleck square root, parallel transport and source derivative placement',
 sources=[dict(path=str(p),sha256=sha(p)) for p in (Path(__file__),D/'ANSWER.md',D/'RECEIPT.json')],
 external_code_run=False))
cpu=time.process_time();x=s.symbols('x0:4');K=s.Symbol('K');z=sum(q*q for q in x);I=s.eye(4);X=s.Matrix(x)
g=I-K*(z*I-X*X.T)/3;inverse=I+K*(z*I-X*X.T)/3;P=I+K*(z*I-X*X.T)/6
def delta(a,b):return s.Integer(a==b)
def gamma(a,b,c):return -K*(delta(a,c)*x[b]+delta(a,b)*x[c]-2*delta(b,c)*x[a])/3
def k1(v):return s.expand(v).coeff(K,0)+K*s.expand(v).coeff(K,1)
def check(name,got,want=0):
    assert s.expand(got-want)==0,(name,got,want)
    checks.append(name)
checks=[];metric_defects=[]
for a in range(4):
    for b in range(4):
        derivative=s.expand(sum(s.diff(g[a,c],x[b])*x[c] for c in range(4)))
        expected=K*(delta(a,b)*z-x[a]*x[b])/3
        check('metric_derivative_'+str((a,b)),derivative,expected)
        metric_defects.append(str(derivative))
        transport=sum(x[c]*s.diff(P[a,b],x[c]) for c in range(4))
        transport+=sum(x[c]*gamma(a,c,d)*P[d,b] for c in range(4) for d in range(4))
        check('upper_parallel_radial_'+str((a,b)),k1(transport))
    check('metric_radial_identity_'+str(a),sum(g[a,b]*x[b] for b in range(4)),x[a])
grad=s.Matrix([s.diff(z,q) for q in x]);check('raw_z_eikonal',k1((grad.T*inverse*grad)[0]),4*z)
box=sum(inverse[a,b]*(s.diff(z,x[a],x[b])-sum(gamma(c,a,b)*s.diff(z,x[c]) for c in range(4)))
        for a in range(4) for b in range(4))
check('raw_z_laplacian',k1(box),8-2*K*z)
check('sigma_half_eikonal',k1((grad.T*inverse*grad)[0]/16),z/4)
check('sigma_half_laplacian',k1(box/4),2-K*z/2)
r=s.Symbol('r')
van=s.series((r/s.sin(r))**3,r,0,4).removeO()
root=s.series((r/s.sin(r))**s.Rational(3,2),r,0,4).removeO()
check('VanVleck',van,1+r*r/2);check('sqrt_VanVleck',root,1+r*r/4)
term=s.expand((-5*K/4)*(-8*K/4))
check('heat_times_heat_no_firstK',term.coeff(K,1),0)
assert term.coeff(K,2)!=0;checks.append('heat_times_heat_secondK_present')
# U2=h_am*d_b ghost^m places d_b on the ghost contraction, not h.
t=s.Symbol('test');ghost=t;metric=s.Integer(1)
right=s.diff(ghost,t)*metric;wrong=ghost*s.diff(metric,t)
assert right==1 and wrong==0;checks.append('derivative_placement_counterexample')
result=dict(at=datetime.now(timezone.utc).isoformat(),status='GEOMETRIC_ERRORS_LOCALIZED_PARALLEL_TRANSPORT_ACCEPTED',
 checks=len(checks),check_names=checks,cpu_seconds=time.process_time()-cpu,
 nonzero_metric_derivative=str(K*(z-x[0]**2)/3),raw_z=dict(eikonal=str(4*z),laplacian=str(8-2*K*z)),
 alternate_z='z_alt=sigma/2=z_raw/4, Box(z_alt)=2-2*K*z_alt; do not reuse raw-z coefficients',
 VanVleck=str(van),sqrt_VanVleck=str(root),heat_product=str(term),
 source_correction='-T_ab[(nablaY GQ)*nablaXm M_ab +2(nablaXb nablaY GQ)*M_am]',
 accepted='Upper-index radial parallel propagator through firstK, not the claimed mixed world-function derivative',
 scope='Geometric identities and placement only; no replacement curved loop computed in this audit',full_Q2=False)
put('audit_results.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='check_names'},ensure_ascii=False))
