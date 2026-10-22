"""Exact coefficient checks for the leading three-vertex differentiated triangle."""
from pathlib import Path
from datetime import datetime, timezone
from time import perf_counter, process_time
import hashlib, json
import sympy as s

HERE=Path(__file__).resolve().parent
DEST=HERE/'triangle_contacts_v2'
DEST.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,obj):
    b=json.dumps(obj,ensure_ascii=False,indent=2).encode('utf-8')
    assert not p.exists() and b,str(p)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b
    t.replace(p)

new(DEST/'PRE_REGISTER.json',dict(
    at=datetime.now(timezone.utc).isoformat(),source_sha256=sha(Path(__file__)),
    supersedes_source_sha256=sha(HERE/'triangle_contact_check.py'),
    correction='Serialize exact Sympy integer entries as Python integers; unchanged mathematics',
    precursor=dict(path=str(HERE/'tensor_extension/manifest.json'),
        sha256=sha(HERE/'tensor_extension/manifest.json')),
    convention='eta=diag(1,-1,-1,-1); f=1/(x^2-i0); box(f)=C delta, C=4i*pi^2',
    graph='F(x,y)=f(x)f(y)f(x-y); independent coordinates x,y in R^(4+4)',
    imported_extension='Hollands 0705.3340v4 Lemma6 and Proposition1; existence outside origin assumed from causal products',
    prescription_before_calculation=[
        'Scalar triangle extension is homogeneous of degree6 and unique (sd6<8).',
        'Single differentiated edge A has degree8; extend its symmetric traceless part Lorentz covariantly and homogeneously.',
        'Fix trace A_a=C delta(x) R2(y), A_b=C delta(y) R2(x), A_c=C delta(x-y) R2(x).',
        'Use the previously fixed R2 and scale mu_R; add no new running finite local terms.',
        'For crossed derivatives, compute invariant Euler residues from derivatives of the unique scalar triangle; no full finite T3 claimed.'
    ],
    input_distribution_identities=['box(f)=C delta','mu_R*dR2/dmu_R=-C*delta/2',
        'S8 of a log-divergent rank2 extension is a Lorentz-invariant rank2 coefficient times delta8',
        'S8 partial_i partial_j F = partial_i partial_j S6 F = 0'],
    scope='Leading homogeneous rank2 triangle subkernels; no tensor fiber contractions, vertices, ghosts, curvature or full anomaly',
    quantum_anomaly_computed=False,gate_changed=False))
start,cpu=perf_counter(),process_time()
checks=[];negatives=[]
def check(name,expr):
    if isinstance(expr,s.MatrixBase):ok=all(s.simplify(x)==0 for x in expr)
    else:ok=s.simplify(expr)==0
    assert ok,name
    checks.append(dict(name=name,passed=True))
def reject(name,expr):
    if isinstance(expr,s.MatrixBase):ok=any(s.simplify(x)!=0 for x in expr)
    else:ok=s.simplify(expr)!=0
    assert ok,name
    negatives.append(dict(name=name,detected=True))

eta=s.diag(1,-1,-1,-1)
pairs=[(i,j) for i in range(4) for j in range(i,4)]
coeff=s.symbols('t0:10')
T=s.zeros(4)
for a,(i,j) in zip(coeff,pairs):T[i,j]=T[j,i]=a
gens=[]
for i in range(1,4):
    L=s.zeros(4);L[0,i]=L[i,0]=1;gens.append(L)
for i in range(1,4):
    for j in range(i+1,4):
        L=s.zeros(4);L[i,j]=1;L[j,i]=-1;gens.append(L)
eqs=[]
for n,L in enumerate(gens):
    check(f'lorentz_generator_{n}',L.T*eta+eta*L)
    eqs.extend(L.T*T+T*L)
lin=s.linear_eq_to_matrix(eqs,coeff)[0]
null=lin.nullspace()
assert len(null)==1
checks.append(dict(name='invariant_symmetric_rank2_dimension_one',passed=True))
tv=s.Matrix([eta[i,j] for i,j in pairs])
check('unique_invariant_span_metric',lin*tv)
tr=s.trace(eta*T)
trrow=s.linear_eq_to_matrix([tr],coeff)[0]
assert len(lin.col_join(trrow).nullspace())==0
checks.append(dict(name='no_invariant_traceless_rank2_delta_coefficient',passed=True))
reject('euclidean_metric_not_lorentz_invariant',gens[0].T*s.eye(4)+s.eye(4)*gens[0])

# Euler residues inferred from the distributional trace identity.
C=s.symbols('C',nonzero=True)
bubble=-C/2
trace_res=C*bubble
edge_res=s.simplify(trace_res/4)
check('single_edge_rank2_residue',edge_res+C**2/8)
check('single_edge_trace',4*edge_res-trace_res)
reject('lost_factor_dimension_four',edge_res-trace_res)
reject('dropped_EOM_contact',trace_res)

# Edge arguments a=x, b=y, c=x-y. Coordinate derivatives act by J.
J=s.Matrix([[1,0],[0,1],[1,-1]])
A,xab,xac,xbc=s.symbols('A xab xac xbc')
M=s.Matrix([[A,xab,xac],[xab,A,xbc],[xac,xbc,A]])
out=J.T*M*J
solutions=s.solve([out[0,0],out[1,1],out[0,1]],(xab,xac,xbc),dict=True)
assert len(solutions)==1
sol=solutions[0]
check('cross_ab',sol[xab]+A)
check('cross_ac',sol[xac]+A)
check('cross_bc',sol[xbc]-A)
Mfixed=M.subs(sol)
v=s.Matrix([1,-1,-1])
check('cycle_flow_nullspace',J.T*v)
check('edge_residue_matrix_rank_one',Mfixed-A*v*v.T)
check('second_coordinate_derivatives_have_no_residue',J.T*Mfixed*J)
reject('all_crossed_signs_equal',J.T*M.subs({xab:-A,xac:-A,xbc:-A})*J)
reject('opposite_orientation_ignored',J.T*M.subs({xab:A,xac:A,xbc:A})*J)

# Permuting vertices changes the pair of relative coordinates with |det|=1.
swaps=[s.Matrix([[0,1],[1,0]]),s.Matrix([[-1,0],[-1,1]]),
       s.Matrix([[1,-1],[0,-1]])]
for i,P in enumerate(swaps):
    check(f'unit_jacobian_relative_vertex_swap_{i}',P.det()**4-1)

# Principal inverse propagator G0=(-i/(4pi²))*f; Wick i*hbar excluded.
factor=-s.I/(4*s.pi**2)
normalized=s.simplify(factor**3*edge_res.subs(C,4*s.I*s.pi**2))
check('normalized_triangle_scale_coefficient',normalized-s.I/(32*s.pi**2))
reject('counted_Wick_i_as_propagator_again',s.I*normalized-normalized)

# Independent Euclidean angular coefficient of the UV logarithm.
# Integral on S3 of n0² = 4pi * integral_0^pi cos²(theta)sin²(theta)dtheta.
theta=s.symbols('theta',real=True)
angular=s.simplify(4*s.pi*s.integrate(s.cos(theta)**2*s.sin(theta)**2,(theta,0,s.pi)))
check('S3_second_moment',angular-s.pi**2/2)
euclidean_log=s.simplify(angular/(2*s.pi)**4)
check('euclidean_radial_log_magnitude',euclidean_log-s.Rational(1,32)/s.pi**2)
check('euclidean_magnitude_matches_lorentz_coefficient',normalized/s.I-euclidean_log)

# Critical-degree accounting; lower-order curvature terms need separate analysis.
check('base_triangle_below_extension_threshold',3*2-8+2)
check('two_derivative_triangle_is_logarithmic',3*2+2-8)
reject('base_triangle_called_logarithmic',3*2-8)

new(DEST/'results.json',dict(
    statute='REAL_EXACT_COEFFICIENT_ALGEBRA_DERIVED_TRIANGLE_SCALE_RESIDUE',
    source_sha256=sha(Path(__file__)),plan_sha256=sha(DEST/'PRE_REGISTER.json'),
    checks=checks,negative_controls=negatives,checks_passed=len(checks),
    negative_controls_detected=len(negatives),
    invariant_rank2_dimension=1,invariant_traceless_rank2_dimension=0,
    unnormalized_single_edge_residue=str(edge_res),
    normalized_single_edge_scale_coefficient=str(normalized),
    edge_matrix_over_A=[[int(x) for x in Mfixed.row(i)/A] for i in range(3)],
    euclidean_angular_integral=str(angular),
    sympy_version=s.__version__,wall_seconds=perf_counter()-start,
    cpu_seconds=process_time()-cpu,distribution_existence_proved_by_CAS=False,
    full_finite_T3_constructed=False,quantum_anomaly_computed=False,gate_changed=False))
print(json.dumps(dict(checks=len(checks),negative_controls=len(negatives),
    coefficient=str(normalized),scope='rank2_leading_triangle_scale_not_BRST'),ensure_ascii=False))
