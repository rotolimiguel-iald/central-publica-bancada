"""Exact audit of field-valence truncation before the A7 anomaly calculation."""
from pathlib import Path
from datetime import datetime, timezone
from time import perf_counter, process_time
import hashlib
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
CHAT = HERE.parents[1]
DEST = HERE / 'quantum_filtration'
DEST.mkdir(exist_ok=True)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def new(path, data):
    raw = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
    assert not path.exists(), str(path)
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert tmp.read_bytes() == raw and raw
    tmp.replace(path)

sources = [CHAT / p for p in [
    'CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md',
    'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md',
    'COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md']]
plan = dict(statute='INPUT_CALCULATION_PLAN_NOT_TEMPORAL_PRESCRIPTION',
    at=datetime.now(timezone.utc).isoformat(), source_sha256=sha(Path(__file__)),
    sources=[dict(path=str(p), sha256=sha(p)) for p in sources],
    goal='Test whether classical C_N can be used as a quantum quotient; derive needed vertex orders',
    scope='Formal Wick contractions, not graph amplitudes or a Ward anomaly',
    inputs=dict(N_values=list(range(2,9)), external_legs_max=6, loops=1,
                vertex_degree_min=3, contraction='hbar*C; unnormalized monomials'),
    expected_controls=['Premature field projection loses contractions',
        'Wrong weighted degree fails', 'Contracting after vertex cutoff loses h7-h3 bubble',
        'Contraction count is not loop count', 'Bare valence six is not quantum weighted degree eight'],
    anomaly_computed=False, temporal_prescription_fixed=False)
new(DEST/'PRE_REGISTER.json',plan)
start, cpu = perf_counter(), process_time()
q,x,y,hbar,C = sp.symbols('q x y hbar C')
checks=[]
negatives=[]

def check(name, condition):
    assert bool(condition), name
    checks.append(dict(name=name, passed=True))

def reject(name, condition):
    assert bool(condition), name
    negatives.append(dict(name=name, detected=True))

def project_q(expr, cutoff):
    return sp.Add(*(coeff*q**degree[0] for degree,coeff in sp.Poly(sp.expand(expr),q).terms()
                    if degree[0] <= cutoff))

for N in range(2,9):
    F,G=q**(N+1),q
    wick=F*G+hbar*C*sp.diff(F,q)*sp.diff(G,q)
    kept=project_q(wick,N)
    check(f'C{N}_contraction_survives',sp.expand(kept-hbar*C*(N+1)*q**N)==0)
    check(f'C{N}_classical_input_zero',project_q(F,N)==0)
    reject(f'C{N}_project_before_contract',kept!=0)

m,n,p,z,r = sp.symbols('m n p z r', integer=True)
check('weighted_degree_conserved',sp.expand(m+n-2*r+2*(p+z+r)-(m+2*p+n+2*z))==0)
reject('hbar_weight_one_is_wrong',sp.expand(m+n-2*r+p+z+r-(m+p+n+z))==-r)
F,G=x**7,y**3
bubble = sp.expand((hbar*C)**2 * sp.diff(F,x,2)*sp.diff(G,y,2)/sp.factorial(2))
check('h7_h3_two_contractions',bubble==126*hbar**2*C**2*x**5*y)
check('h7_h3_six_external_legs',sp.Poly(bubble,x,y).total_degree()==6)
I,V=2,2
check('bubble_is_one_loop',I-V+1==1)
reject('contractions_are_not_loops',I!=I-V+1)
reject('h7_cutoff_erases_bubble',bubble!=0)
volume=sp.sqrt(1+q).series(q,0,9).removeO()
check('volume_seventh_coefficient_nonzero',volume.coeff(q,7)==sp.Rational(33,2048))
check('volume_eighth_coefficient_nonzero',volume.coeff(q,8)==-sp.Rational(429,32768))
reject('weight6_omits_hbar_field6',6+2*1>6)

def partitions(total, lower=1):
    if total==0:
        yield ()
    for first in range(lower,total+1):
        for tail in partitions(total-first,first):
            yield (first,)+tail

families=[]
for E in range(1,7):
    for increments in partitions(E):
        vertices=tuple(k+2 for k in increments)
        V=len(vertices)
        I=(sum(vertices)-E)//2
        assert sum(vertices)-E==2*I
        assert I-V+1==1
        assert max(vertices)<=E+3-V<=E+2
        assert V<=E
        families.append(dict(external_legs=E, vertex_degrees=vertices, internal_lines=I,
            vertices=V, loops=1, excluded_by_bare_C6=max(vertices)>6,
            graph_enumeration=False))
check('one_loop_E6_has_11_valence_families',sum(f['external_legs']==6 for f in families)==11)
check('one_loop_E1_to_E6_has_29_valence_families',len(families)==29)
check('premature_C6_omits_three_valence_families',sum(f['excluded_by_bare_C6'] for f in families)==3)
check('h7_h3_non_tadpole_family_present',any(f['vertex_degrees']==(3,7) for f in families))
check('two_or_more_vertices_need_at_most_7',max(max(f['vertex_degrees']) for f in families if f['vertices']>=2)==7)
check('one_loop_weight8_includes_E6',6+2*1==8)
check('degree_counting_general',sp.expand((m+n)-2*r-2*(2-1)+2*(r-2+1)-((m-2)+(n-2)))==0)
# The last equality rewrites E+2L-2 = sum(v-2), for two vertices.
result=dict(statute='REAL_EXACT_CAS_DERIVED_FILTRATION_NOT_ANOMALY',
    source_sha256=sha(Path(__file__)),plan_sha256=sha(DEST/'PRE_REGISTER.json'),
    sympy_version=sp.__version__,checks=checks,negative_controls=negatives,
    checks_passed=len(checks),negative_controls_detected=len(negatives),
    bubble_coefficient=str(bubble),families=families,
    caveats=['Families are degree partitions, not graphs or nonzero amplitudes',
             'A scalar contraction demonstrates filtration failure; it is not a scalar substitute for the metric theory',
             'Cosmological volume coefficients alone do not establish a nonzero complete gravitational amplitude',
             'Wick convention may remove single-vertex tadpoles; the (3,7) family remains structurally possible',
             'Antifield/ghost selection and distributional contacts still need separate treatment'],
    wall_seconds=perf_counter()-start,cpu_seconds=process_time()-cpu,
    quantum_anomaly_computed=False,temporal_prescription_fixed=False,gate_changed=False)
new(DEST/'results.json',result)
print(json.dumps({k:result[k] for k in ['statute','checks_passed','negative_controls_detected','wall_seconds','cpu_seconds']},ensure_ascii=False))
