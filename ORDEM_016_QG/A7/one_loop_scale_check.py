"""Preregister and verify the one-loop principal scale-coefficient engine."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter,process_time
import hashlib,json
import sympy as s
from one_loop_scale_engine import q,n,ANGULAR_FACTOR as A,log_coefficient as lc,sphere_average_monomial

HERE=Path(__file__).resolve().parent
DEST=HERE/'one_loop_scale'
DEST.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode('utf-8')
    assert not p.exists() and b,str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b
    t.replace(p)
new(DEST/'PRE_REGISTER.json',dict(at=datetime.now(timezone.utc).isoformat(),
    source_sha256=sha(Path(__file__)),engine_sha256=sha(HERE/'one_loop_scale_engine.py'),
    precursor_sha256=sha(HERE/'triangle_contacts_v2/manifest.json'),
    prescription='Radial UV expansion q=r*n, sphere S3, extract coefficient r^-1 with d4q/(2pi)^4',
    normalization='Angular factor area(S3)/(2pi)^4; Lorentzian phases not supplied automatically',
    denominator='product[(q+p_e)^2+m_e^2], commuting scalar principal symbols',
    tests=['Independent Dirichlet moments','Feynman-parameter rank2 bubble',
        'Routing including numerator shift','Algebraic Ward numerator identity',
        'Triangle/box/pentagon/hexagon leading moments'],
    finite_time_ordered_products_fixed=False,quantum_anomaly_computed=False,
    gate_changed=False))
start,cpu=perf_counter(),process_time()
checks=[];neg=[]
def check(name,expr):
    assert s.simplify(expr)==0,name
    checks.append(dict(name=name,passed=True))
def reject(name,expr):
    assert s.simplify(expr)!=0,name
    neg.append(dict(name=name,detected=True))
zero=(0,0,0,0)
p=s.symbols('p0:4',real=True)
m0,m1=s.symbols('m0_squared m1_squared',positive=True)
psq=sum(x*x for x in p)

# Independent normalized Dirichlet(1/2,...,1/2) moments.
for exps in [(0,0,0,0),(2,0,0,0),(2,2,0,0),(4,0,0,0),
             (6,2,0,0),(2,2,2,2),(8,0,0,0)]:
    aa=[s.Rational(e,2) for e in exps]
    direct=s.gamma(2)/s.gamma(2+sum(aa))*s.prod(
        s.gamma(x+s.Rational(1,2))/s.gamma(s.Rational(1,2)) for x in aa)
    check('dirichlet_moment_'+str(exps),sphere_average_monomial(exps)-direct)
check('odd_angular_moment',sphere_average_monomial((3,1,0,0)))

check('scalar_bubble',lc(1,[zero,p],[m0,m1])-A)
check('shifted_tadpole',lc(1,[p],[m1])+A*m1)
vector=[]
tensor=[]
for i in range(4):
    val=lc(q[i],[zero,p],[m0,m1]);vector.append(val)
    check(f'vector_bubble_{i}',val+A*p[i]/2)
for i in range(4):
    row=[]
    for j in range(4):
        val=lc(q[i]*q[j],[zero,p],[m0,m1]);row.append(val)
        expected=A*(p[i]*p[j]/3-(psq/12+(m0+m1)/4)*(1 if i==j else 0))
        check(f'rank2_bubble_{i}_{j}',val-expected)
    tensor.append(row)
check('rank2_bubble_trace',sum(tensor[i][i] for i in range(4))+A*(m0+m1))

# A separate Feynman-parameter integral derives the target tensor coefficient.
x=s.symbols('x',real=True)
Delta=(1-x)*m0+x*m1+x*(1-x)*psq
fp=A*s.integrate(-Delta/2+x*x*p[0]**2,(x,0,1))
check('rank2_bubble_Feynman_parameter_independent',tensor[0][0]-fp)
reject('isotropic_second_moment_without_factor_four',4*tensor[0][0]-fp)
reject('dropping_external_shift',lc(q[0]**2,[zero,zero],[m0,m1])-tensor[0][0])

# Algebraic numerator identity, verified at the coefficient level.
lhs=2*sum(p[i]*vector[i] for i in range(4))
rhs=lc(1,[zero],[m0])-lc(1,[p],[m1])-(psq+m1-m0)*lc(1,[zero,p],[m0,m1])
check('bubble_numerator_Ward_identity',lhs-rhs)
reject('odd_numerator_discarded_before_denominator_expansion',lhs)

# Same integral with loop variable shifted. Both numerator and denominators move.
shift=(1,2,0,-1)
shifted_p=tuple(p[i]+shift[i] for i in range(4))
routed=lc((q[0]+shift[0])**2,[shift,shifted_p],[m0,m1])
check('routing_invariance_with_numerator',routed-tensor[0][0])
reject('routing_without_numerator_shift',lc(q[0]**2,[shift,shifted_p],[m0,m1])-tensor[0][0])

cycles=[]
for edges in range(2,7):
    rank=2*edges-4
    val=lc(q[0]**rank,[zero]*edges,[0]*edges)
    direct=A*s.gamma(s.Rational(rank+1,2))/s.sqrt(s.pi)/s.gamma(s.Rational(rank,2)+2)
    check(f'cycle_{edges}_critical_rank_{rank}',val-direct)
    cycles.append(dict(edges=edges,numerator_degree=rank,coefficient=str(val)))
    if rank:
        check(f'cycle_{edges}_below_log_threshold',lc(q[0]**(rank-1),[zero]*edges,[0]*edges))
check('triangle_matches_previous_Euclidean_magnitude',lc(q[0]**2,[zero]*3,[0]*3)-s.Rational(1,32)/s.pi**2)
check('massive_rank4_bubble',lc(q[0]**4,[zero,zero],[m0,m0])-3*m0*m0*A/8)
reject('degree_count_mistakes_power_divergence_for_log',A-lc(q[0]**2,[zero,zero],[0,0]))
try:lc(1,[(q[0],0,0,0)],[0])
except ValueError:neg.append(dict(name='loop_dependent_shift_rejected',detected=True))
else:raise AssertionError('Invalid shift accepted')

new(DEST/'results.json',dict(statute='REAL_EXACT_ONE_LOOP_PRINCIPAL_SCALE_COEFFICIENTS',
    source_sha256=sha(Path(__file__)),engine_sha256=sha(HERE/'one_loop_scale_engine.py'),
    plan_sha256=sha(DEST/'PRE_REGISTER.json'),checks=checks,negative_controls=neg,
    checks_passed=len(checks),negative_controls_detected=len(neg),
    scalar_bubble=str(A),vector_bubble=list(map(str,vector)),
    tensor_bubble=[[str(v) for v in row] for row in tensor],cycles=cycles,
    sympy_version=s.__version__,wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu,
    full_finite_products_constructed=False,full_tensor_ghost_vertices_contracted=False,
    quantum_anomaly_computed=False,gate_changed=False))
print(json.dumps(dict(checks=len(checks),negative_controls=len(neg),
    scope='Euclidean_principal_UV_log_coefficient_not_full_Ward'),ensure_ascii=False))
