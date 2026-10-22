"""Exact switching-function completion of the finite principal quadratic BV contact."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, time, uuid
import sympy as s

HERE=Path(__file__).resolve().parent; DEST=HERE/'finite_cutoff_contact'; DEST.mkdir(exist_ok=True)
def new(name,obj):
    p=DEST/name; assert not p.exists()
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert t.read_bytes()==b;t.replace(p)
new('PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    scope='Flat principal finite quadratic BV contact with arbitrary BRST-inert switching chi, formal derivative symbols; not full curved causal amplitude',
    method='Polarize s0 B_chi, retain independent field momenta q,r and cutoff k=-q-r; compare exact commutator completion and graded exchange',
    negative_controls=['drop cutoff commutators','halve first metric commutator','forget odd formal adjoint of cubic source'],
    source_sha256=hashlib.sha256((HERE/'finite_antifield_contact_v3/results.json').read_bytes()).hexdigest(),
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
cpu=time.process_time();wall=time.perf_counter()
q=s.Matrix(s.symbols('q0:4'));r=s.Matrix(s.symbols('r0:4'));k=-q-r
data=json.loads((HERE/'finite_principal_contact/results.json').read_bytes())
ns=list(map(s.Rational,data['finite_contact_coefficients_over_C']))
rs=list(map(s.Rational,json.loads((HERE/'finite_antifield_contact_v3/results.json').read_bytes())['source_contact_coefficients']))
checks=[];examples=[]
def check(expr,name):
    assert s.expand(expr)==0,name
    checks.append(name)
basis=[]
for i in range(4):
    for j in range(i,4):
        H=s.zeros(4);H[i,j]=1;H[j,i]=1;basis.append(H)

for label,signs in [('Euclidean',[1,1,1,1]),('Lorentz',[-1,1,1,1])]:
    g=s.diag(*signs)
    def inner(H,T):return s.trace(g*H*g*T)
    def K(p,v):return p*(g*v).T+(g*v)*p.T
    def Itr(H):return H-g*s.trace(g*H)/2
    def E(p,H):
        cp=g*(H*g*p-p*s.trace(g*H)/2)
        return (p.T*g*p)[0]*Itr(H)-Itr(K(p,cp))
    def N(p,H,T):
        p2=(p.T*g*p)[0];ph=(p.T*g*H*g*p)[0];pt=(p.T*g*T*g*p)[0]
        invariants=[p2*p2*inner(H,T),p2*p2*s.trace(g*H)*s.trace(g*T),
            p2*(s.trace(g*H)*pt+s.trace(g*T)*ph),p2*(p.T*g*H*g*T*g*p)[0],ph*pt]
        return sum(a*b for a,b in zip(ns,invariants))
    def R(p,v):
        p2=(p.T*g*p)[0];pv=(p.T*v)[0]
        return rs[0]*p2*K(p,v)+rs[1]*p*p.T*pv+rs[2]*p2*g*pv
    def metric_full(p,u,H,v):
        # p is h momentum, u is ghost momentum.
        return (N(p,H,K(u,v))+N(u,H,K(u,v)))/2
    for j in range(4):
        v=s.eye(4)[:,j]
        for a,H in enumerate(basis):
            full=metric_full(q,r,H,v)
            bulk=-N(q,H,K(q,v))
            completion=-N(q,H,K(k,v))-(N(q+k,H,K(q+k,v))-N(q,H,K(q+k,v)))/2
            check(full-bulk-completion,f'{label}_metric_cutoff_{a}_{j}')
            source=inner(E(q,H),R(r,v));source_bulk=-inner(E(q,H),R(q,v))
            source_completion=-inner(E(q,H),R(q+k,v)-R(q,v))
            check(source-source_bulk-source_completion,f'{label}_source_cutoff_{a}_{j}')
            check((full-bulk).subs(dict(zip(r,-q))),f'{label}_constant_cutoff_{a}_{j}')
        for i in range(4):
            w=s.eye(4)[:,i]
            # Distinct Fourier ghost modes anticommute. Their coefficient is symmetric.
            check(metric_full(q,r,K(q,w),v)-metric_full(r,q,K(r,v),w),f'{label}_graded_WZ_{i}_{j}')
            check(inner(E(q,K(q,w)),R(r,v)),f'{label}_source_WZ_{i}_{j}')
    # A counterexample when only chi times the constant-cutoff expression is retained.
    e0=s.eye(4)[:,0];p=e0;u=2*e0;switch=-p-u
    bulk1=-N(p,K(p,e0),K(p,e0));bulk2=-N(u,K(u,e0),K(u,e0))
    full1=metric_full(p,u,K(p,e0),e0);full2=metric_full(u,p,K(u,e0),e0)
    assert bulk1-bulk2!=0 and full1-full2==0
    # The first commutator occurs TWICE before collecting; its final coefficient is one.
    lost_half=N(p,K(p,e0),K(switch,e0))/2
    assert lost_half!=0
    examples.append(dict(signature=label,bulk_exchange_defect=str(bulk1-bulk2),
        completed_exchange_defect=str(full1-full2),completed_coefficient=str(full1),
        lost_half_first_commutator=str(lost_half)))
    # Cubic R*=-R^T; the error is visible already at chi constant for nongauge H.
    H=s.diag(0,1,0,0)
    wrong_source=2*inner(E(p,H),R(p,e0))
    assert wrong_source!=0

result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),check_names=checks,
    examples=examples,negative_controls=3,signatures=['Euclidean','Lorentz'],
    cutoff_derivative_order_metric_max=5,cutoff_derivative_order_source_max=3,
    corrected_metric_operator='chi K* N + [K*,chi] N + (1/2) K* [N,chi]',
    corrected_source_operator='chi R* E + [R*,chi] E',
    s0_exact_for_arbitrary_inert_chi=True,full_curved_causal_Q2=False,
    physical_relative_phase_not_fixed=True,cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall)
new('results.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='check_names'}),flush=True)
