"""Check local Euler jets supporting a classical BRST differential quotient.

This is neither a quantum quotient nor a CAS proof of all BV identities.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, time, uuid
import sympy as s

HERE=Path(__file__).resolve().parent
DEST=HERE/'sigma_restriction'
DEST.mkdir(exist_ok=True)
def new(path,obj):
    data=json.dumps(obj,ensure_ascii=False,indent=2).encode()
    assert not path.exists(),path
    tmp=path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(data)
    assert tmp.read_bytes()==data
    tmp.replace(path)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    target='Classical sigma jet ideal; source-free S3 sigma model, no quantum quotient',
    dimension=4,target_dimension=3,
    checks=['Euler at zero jets','Euler linearization for arbitrary metric density',
            'stress at constant sigma','three nonzero fluctuation Hessians'],
    negatives=['linear sigma source breaks restriction',
               'antifields alone cannot be discarded off-shell'],
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
wall=time.perf_counter(); cpu=time.process_time()
x=s.symbols('x0:3'); cm=s.Symbol('cm', nonzero=True)
y=[[s.Symbol(f'y{i}_{mu}') for mu in range(4)] for i in range(3)]
z=[s.Matrix(4,4,lambda a,b:s.Symbol(f'z{i}_{min(a,b)}{max(a,b)}')) for i in range(3)]
A=s.Matrix(4,4,lambda a,b:s.Symbol(f'A{min(a,b)}{max(a,b)}'))
b=s.symbols('b0:4')  # b^nu=partial_mu(sqrt|g|g^{mu nu}), not Nakanishi-Lautrup b.
G=s.eye(3)+s.Matrix(x)*s.Matrix(x).T/(1-sum(v*v for v in x))
L=cm*s.Rational(1,2)*sum(A[mu,nu]*G[i,j]*y[i][mu]*y[j][nu]
    for i in range(3) for j in range(3) for mu in range(4) for nu in range(4))
# Total derivative of dL/d(partial_mu xi_i); metric-density derivative is
# cm G_ij partial_mu(A^{mu nu}) partial_nu xi_j.
E=[]
for i in range(3):
    q=s.diff(L,x[i])
    for mu in range(4):
        momentum=s.diff(L,y[i][mu])
        q-=sum(s.diff(momentum,x[k])*y[k][mu] for k in range(3))
        q-=sum(s.diff(momentum,y[k][nu])*z[k][mu,nu] for k in range(3) for nu in range(4))
    q-=cm*sum(G[i,j]*b[nu]*y[j][nu] for j in range(3) for nu in range(4))
    E.append(q)
zero={v:0 for v in x}
zero.update({v:0 for row in y for v in row})
zero.update({v:0 for matrix in z for v in matrix})
checks=[]
for i,ei in enumerate(E):
    assert ei.subs(zero)==0
    checks.append(f'Euler_{i}_vanishes_on_constant_sigma')
    # Derivative at zero along all sigma jets, without expanding the full rational function.
    linear=sum(s.diff(ei,var).subs(zero)*var for var in zero)
    expected=-cm*(sum(A[mu,nu]*z[i][mu,nu] for mu in range(4) for nu in range(4))+
                  sum(b[nu]*y[i][nu] for nu in range(4)))
    assert s.expand(linear-expected)==0
    checks.append(f'Euler_{i}_linear_wave_density')
    assert s.diff(linear,z[i][0,0])==-cm*A[0,0]
    checks.append(f'fluctuation_{i}_not_removed_by_constant_background')
# Stress variations are proportional to two sigma derivatives. Differentiate
# an independent symmetric density component; no equation of motion imposed.
for mu in range(4):
    for nu in range(mu,4):
        assert s.diff(L,A[mu,nu]).subs(zero)==0
        checks.append(f'stress_{mu}{nu}_zero')
J=s.Symbol('J',nonzero=True)
assert (E[0]+J).subs(zero)==J
assert s.diff(E[0],z[0][0,0]).subs(zero)==-cm*A[0,0]
negatives=['linear_source_E0=J_is_not_in_the_sigma_ideal',
           'discard_only_sigma_antifields_fails_because_E_sigma_is_nonzero']
result=dict(at=datetime.now(timezone.utc).isoformat(),status='EXACT_LOCAL_JET_CHECKS_PASSED',
    checks=checks,negative_controls=negatives,
    target_metric='delta_ij+xi_i xi_j/(1-|xi|^2), local hemisphere chart of S3',
    full_BRST_ideal_argument='Written derivation required; not inferred from finite checks',
    quantum_quotient=False,bv_poisson_quotient=False,gate_changed=False,
    cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall)
new(DEST/'results.json',result)
print(json.dumps(result,ensure_ascii=False))
