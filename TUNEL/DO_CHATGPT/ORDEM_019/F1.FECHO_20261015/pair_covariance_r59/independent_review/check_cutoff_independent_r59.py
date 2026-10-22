"""Independent sparse-Fock checks; does not import the author's implementation."""
from pathlib import Path
import datetime
import hashlib
import json
import time
import sympy as s

ROOT = Path(__file__).resolve().parent
t = s.symbols('t', positive=True)
q = t**2
checks = []
start = time.perf_counter()

def record(name, value):
    residual = s.simplify(value)
    assert residual == 0, (name, residual)
    checks.append({'name': name, 'residual': str(residual), 'pass': True})

def op(vector, mode, raising=False, cutoff=None):
    output = {}
    for index, coefficient in vector.items():
        n = index[mode]
        if not raising and n == 0:
            continue
        if raising and cutoff is not None and n == cutoff:
            continue
        target = list(index)
        target[mode] += 1 if raising else -1
        factor = s.sqrt(n+1 if raising else n)
        key = tuple(target)
        output[key] = output.get(key, 0) + factor*coefficient
    return output

def add(x, y, scale=1):
    result = dict(x)
    for key, value in y.items():
        result[key] = result.get(key, 0) + scale*value
    return result

def inner(x, y):
    return s.simplify(sum(s.conjugate(v)*y.get(key, 0) for key, v in x.items()))

def quadrature(vector, cutoff=None):
    vector = add(op(vector, 0, cutoff=cutoff), op(vector, 0, raising=True, cutoff=cutoff))
    return {key: value/s.sqrt(2) for key, value in vector.items()}

for N in (0, 1, 3):
    # Phase pi/2 tests the complex sign of <ab>, rather than just its modulus.
    vector = {(n,n): (s.I*t)**n for n in range(N+1)}
    Z = inner(vector, vector)
    annihilated = op(vector, 0)
    n_value = inner(annihilated, annihilated)/Z
    m_value = inner(vector, op(op(vector, 1), 0))/Z
    expected = (q-(N+1)*q**(N+1)+N*q**(N+2))/((1-q)*(1-q**(N+1)))
    record(f'N{N}:occupation_from_sparse_action', n_value-expected)
    record(f'N{N}:complex_pair_from_sparse_action', m_value-s.I*expected/t)
    record(f'N{N}:one_point_a_zero', inner(vector, op(vector, 0)))
    record(f'N{N}:one_point_b_zero', inner(vector, op(vector, 1)))
    record(f'N{N}:full_quadrature', inner(quadrature(vector), quadrature(vector))/Z-n_value-s.Rational(1,2))
    top_probability=q**N/Z
    record(f'N{N}:hard_cut_quadrature', inner(quadrature(vector,N), quadrature(vector,N))/Z-n_value-s.Rational(1,2)+(N+1)*top_probability/2)
    record(f'N{N}:occupation_error', q/(1-q)-n_value-(N+1)*q**(N+1)/(1-q**(N+1)))
    record(f'N{N}:pair_error', s.I*t/(1-q)-m_value-s.I*(N+1)*t**(2*N+1)/(1-q**(N+1)))
    record(f'N{N}:normalizer', (1-q)*Z-(1-q**(N+1)))
    for n in range(N+1):
        basis={(n,0):s.Integer(1)}
        comm=add(op(op(basis,0,True,N),0,False,N), op(op(basis,0,False,N),0,True,N),-1)
        expected_basis={(n,0):s.Integer(1-(N+1)*(n==N))}
        record(f'N{N}:CCR_on_basis_{n}', inner(add(comm,expected_basis,-1), add(comm,expected_basis,-1)))

# Difference of the two rank-one projectors on their exact two-dimensional span.
# c=overlap=sqrt(1-Q), Q=geometric tail. D has eigenvalues +/-sqrt(Q).
Q=s.symbols('Q', positive=True)
c=s.sqrt(1-Q)
D=s.Matrix([[Q,-c*s.sqrt(Q)],[-c*s.sqrt(Q),-Q]])
record('projector_difference_trace', s.trace(D))
record('projector_difference_determinant', D.det()+Q)
record('projector_difference_square', sum(D*D-Q*s.eye(2)))
record('unit_vectors_distance', (1-c)**2+Q-2*(1-c))

# Projection P_M applied to the normalized cut N has the following norm.
M,N=s.symbols('M N', integer=True, nonnegative=True)
q0=s.symbols('q', positive=True)
ratio=s.sqrt((1-q0**(M+1))/(1-q0**(N+1)))
record('projection_renormalization_factor_squared', ratio**2-(1-q0**(M+1))/(1-q0**(N+1)))

result={
 'status':'PASS_SELECTED_IDENTITIES',
 'author':'codex-mission-memory-review',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'seconds':time.perf_counter()-start,
 'sympy':s.__version__,
 'script':{'path':str(Path(__file__)), 'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
 'method':'Sparse occupation-basis action of full creation/annihilation and hard-cut operators; independent of root implementation. Exact complex phase pi/2, cuts0/1/3. Analytic projector difference in a 2D span.',
 'checks':checks,
 'count':len(checks),
 'limits':'Selected exact identities only. Infinite convergence uses the written geometric-tail/graph-norm argument reviewed separately. No source imports, mission mutations, providers or scientific builds.',
}
path=ROOT/'CUTOFF_INDEPENDENT_CHECKS_R59.json'
with path.open('x',encoding='utf-8') as stream:
    json.dump(result,stream,ensure_ascii=False,indent=2)
print(json.dumps({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'count':len(checks),'status':result['status']}))
