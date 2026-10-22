"""Preregister/check principal metric vertex normalization before loop use."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
from itertools import permutations
import hashlib,json
from metric_principal_vertices import *

HERE=Path(__file__).resolve().parent
DEST=HERE/'metric_vertices'
DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode('utf-8')
    assert not p.exists() and b,str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),vertices_sha256=sha(HERE/'metric_principal_vertices.py'),
    predecessor_sha256=sha(HERE/'ghost_bubble/manifest.json'),
    metric_input_sha256=sha(HERE/'model_inputs/DERIVACAO_OPERADORES.md'),
    conventions='Euclidean principal indices, Fourier exp(+ipx), covariant h, g=delta+h',
    action='-sqrt(g)/(2*kappa)*g^mu,nu*(Gamma^rho_mu,sigma Gamma^sigma_nu,rho-Gamma^rho_mu,nu Gamma^sigma_rho,sigma)',
    gauge='+(1/(4*kappa))*C(h)^2, linear de Donder, no cubic gauge vertex',
    expected_quadratic='H_gf(p)=p² I_tr/(4*kappa), inner product includes symmetric off-diagonal multiplicity',
    cubic_normalization='Return 16*kappa times coefficient epsilon1 epsilon2 epsilon3; not Taylor coefficient divided by 3!',
    boundary='constant cutoff only; discarded divergence produces cutoff contacts separately',
    quantum_anomaly_computed=False,gate_changed=False))
start,cpu=perf_counter(),process_time()
checks=[];neg=[]
def check(name,a,b=0):
    assert a==b,(name,a,b);checks.append(dict(name=name,passed=True))
def reject(name,a):
    assert a!=0,name;neg.append(dict(name=name,detected=True))
p=(1,2,-1,1);mp=tuple(-v for v in p)
bs=[basis(i,j) for i in range(4) for j in range(i,4)]
for i,H in enumerate(bs):
    for j,J in enumerate(bs[i:],start=i):
        expected=dot(p,p)*(2*inner(H,J)-trace(H)*trace(J))
        check(f'free_Hessian_pair_{i}_{j}',gauge_fixed_quadratic_8k(H,p,J,mp),expected)
v=(1,-1,2,0)
for i,H in enumerate(bs):
    check(f'ungauged_Hessian_gauge_null_{i}',eh_quadratic_8k(H,p,gauge_matrix(mp,v),mp))

momenta=[(1,0,0,0),(0,1,0,0),(-1,-1,0,0)]
check('trace_family_cubic_normalization',eh_cubic_16k(I,momenta[0],I,momenta[1],I,momenta[2]),
    12*sum(dot(x,x) for x in momenta))
H,J,L=bs[0],bs[4],bs[1]
original=eh_cubic_16k(H,momenta[0],J,momenta[1],L,momenta[2])
fields=list(zip([H,J,L],momenta))
for k,perm in enumerate(permutations(range(3))):
    args=[x for i in perm for x in fields[i]]
    check(f'cubic_bose_symmetry_{k}',eh_cubic_16k(*args),original)

# Off-shell classical diffeomorphism identity. Strip a common i from s h.
k=(1,-1,0,1);p=(0,1,2,-1);r=tuple(-k[i]-p[i] for i in range(4));v=(1,2,0,-1)
ward_nonzero=0
for a,b in [(0,0),(0,4),(1,1),(2,7),(4,8),(6,9),(3,5),(7,7)]:
    H,J=bs[a],bs[b]
    first=eh_cubic_16k(gauge_matrix(k,v),k,H,p,J,r)
    second=2*eh_quadratic_8k(lie_matrix(H,p,k,v),tuple(k[i]+p[i] for i in range(4)),J,r)
    third=2*eh_quadratic_8k(H,p,lie_matrix(J,r,k,v),tuple(k[i]+r[i] for i in range(4)))
    check(f'classical_cubic_Ward_{a}_{b}',first+second+third)
    if first:ward_nonzero+=1
assert ward_nonzero>0
checks.append(dict(name='Ward_examples_nonvacuous',passed=True))
reject('discarding_gauge_fixing_from_free_Hessian',
    eh_quadratic_8k(I,p,I,tuple(-x for x in p))-gauge_fixed_quadratic_8k(I,p,I,tuple(-x for x in p)))
reject('dividing_cubic_vertex_by_extra_factorial',
    eh_cubic_16k(I,momenta[0],I,momenta[1],I,momenta[2])-2*sum(dot(x,x) for x in momenta))

new(DEST/'results.json',dict(statute='REAL_PRINCIPAL_METRIC_VERTEX_NORMALIZATION',
    source_sha256=sha(Path(__file__)),vertices_sha256=sha(HERE/'metric_principal_vertices.py'),
    plan_sha256=sha(DEST/'PRE_REGISTER.json'),checks=checks,negative_controls=neg,
    checks_passed=len(checks),negative_controls_detected=len(neg),
    nonzero_classical_Ward_examples=ward_nonzero,
    wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu,
    full_curved_vertices=False,quantum_anomaly_computed=False,gate_changed=False))
print(json.dumps(dict(checks=len(checks),negative_controls=len(neg),scope='metric_principal_cubic_and_free_Hessian'),ensure_ascii=False))
