"""Combine independently computed source and loop data, with no coefficient fit."""
from pathlib import Path
from datetime import datetime, timezone
from functools import lru_cache
import hashlib, json, time, uuid
import sympy as s

H = Path(__file__).resolve().parent
D = H / 'bilocal_bulk_ward_closure'
D.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(name, value):
    p = D / name
    assert not p.exists(), p
    b = json.dumps(value, indent=2).encode()
    t = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    t.write_bytes(b)
    assert t.read_bytes() == b
    t.replace(p)

names = ['bilocal_full_external_pair', 'source_einstein_radial_aux',
         'bilocal_frame_divergence_audit']
inputs = [H / name / 'results.json' for name in names]
for name in names:
    manifest = json.loads((H / name / 'manifest.json').read_bytes())
    for row in manifest['artifacts']:
        assert sha(Path(row['path'])) == row['sha256'], row['path']
loop, source, audit = [json.loads(p.read_bytes()) for p in inputs]
assert audit['status'] == 'FRAME_DIVERGENCE_RECONSTRUCTION_VERIFIED'
put('PRE_REGISTER.json', dict(at=datetime.now(timezone.utc).isoformat(),
    combination='-metric/2 + ghost + Einstein(source)',
    scope='O(K), off diagonal, O4 invariant singular reference; no contact extension or arbitrary smooth W',
    sources=[dict(path=str(p), sha256=sha(p)) for p in inputs + [Path(__file__)]],
    no_fitting=True, full_Q2=False))
cpu = time.process_time()
x = s.symbols('x0:4'); z, L = s.symbols('z L')
Z = sum(v*v for v in x)
def delta(a,b): return s.Integer(a == b)
def dx(f,i): return s.diff(f,x[i]) + 2*x[i]*(s.diff(f,z)+s.diff(f,L)/z)
def frame(a,b): return (z*delta(a,b)-x[a]*x[b])/6
def gamma(c,i,a): return -(delta(c,a)*x[i]+delta(c,i)*x[a]-2*delta(i,a)*x[c])/3
def reduced(f):
    num, den = s.fraction(s.cancel(s.expand(f)))
    return s.cancel(s.rem(num,Z-z,x[0])/den)
def rational_data(kind, key):
    return [[s.sympify(v,locals={'L':L}) for v in row]
            for row in loop['coefficients'][kind][key]]
g0,g1 = rational_data('ghost','C0'),rational_data('ghost','C1')
m0,m1 = rational_data('metric','C0'),rational_data('metric','C1')
c0 = [[s.expand(g0[o][i]-m0[o][i]/2) for i in range(3)] for o in (0,1)]
c1 = [[s.expand(g1[o][i]-m1[o][i]/2) for i in range(7)] for o in (0,1)]
@lru_cache(None)
def rank3(o,a,b,r):
    A,B,C = c0[o]
    return (A*delta(a,b)*x[r]+B*(delta(a,r)*x[b]+delta(b,r)*x[a]))/z**(5-o)+C*x[a]*x[b]*x[r]/z**(6-o)
@lru_cache(None)
def rank4(o,i,a,b,r):
    terms = [delta(i,r)*delta(a,b),delta(i,a)*delta(b,r)+delta(i,b)*delta(a,r),
      delta(a,b)*x[i]*x[r],delta(i,r)*x[a]*x[b],
      delta(i,a)*x[b]*x[r]+delta(i,b)*x[a]*x[r],
      delta(a,r)*x[i]*x[b]+delta(b,r)*x[i]*x[a],x[i]*x[a]*x[b]*x[r]]
    return sum(v*t/z**(p-o) for v,t,p in zip(c1[o],terms,[4,4,5,5,5,5,6]))
@lru_cache(None)
def coordinate_tensor(o,i,a,b,r):
    f = rank4(o,i,a,b,r)
    if o:
        f += sum(frame(i,t)*rank4(0,t,a,b,r)+frame(a,t)*rank4(0,i,t,b,r)
                 +frame(b,t)*rank4(0,i,a,t,r) for t in range(4))
    return s.expand(f)
@lru_cache(None)
def coordinate_divergence(o,a,b,r):
    f = sum(dx(coordinate_tensor(o,i,a,b,r),i) for i in range(4))
    if o:
        f += sum(gamma(i,i,t)*rank4(0,t,a,b,r)+gamma(a,i,t)*rank4(0,i,t,b,r)
                 +gamma(b,i,t)*rank4(0,i,a,t,r) for i in range(4) for t in range(4))
    return s.expand(f)
def frame_divergence(o,a,b,r):
    f = coordinate_divergence(o,a,b,r)
    if o:
        f -= sum(frame(a,t)*coordinate_divergence(0,t,b,r)+frame(b,t)*coordinate_divergence(0,a,t,r)
                 for t in range(4))
    return f
src = [s.Rational(v) for v in source['Einstein_curvature_rank3_coefficients']]
def source_image(o,a,b,r):
    if not o: return s.Integer(0)
    A,B,C = src
    return (A*delta(a,b)*x[r]+B*(delta(a,r)*x[b]+delta(b,r)*x[a]))/z**4+C*x[a]*x[b]*x[r]/z**5
checks = []
samples = [[],[]]
for o in (0,1):
    for a in range(4):
        for b in range(4):
            for r in range(4):
                bulk = reduced(rank3(o,a,b,r)-frame_divergence(o,a,b,r))
                residual = reduced(bulk + source_image(o,a,b,r))
                assert residual == 0, (o,a,b,r,residual)
                checks.append([o,a,b,r])
    for a,b,r in [(1,1,0),(0,1,1),(0,0,0)]:
        sub=dict(zip(x,(1,0,0,0)));sub[z]=1
        samples[o].append(str(s.expand(source_image(o,a,b,r).subs(sub))))
    print('ORDER',o,'checks',len(checks),'cpu',time.process_time()-cpu,flush=True)
negatives = []
for label, expression in [
    ('omit_external_X_derivative_integration_K0',rank3(0,1,1,0)),
    ('omit_Einstein_source_K1',rank3(1,1,1,0)-frame_divergence(1,1,1,0)),
    ('reverse_source_sign_K1',rank3(1,1,1,0)-frame_divergence(1,1,1,0)-source_image(1,1,1,0))]:
    residual = reduced(expression)
    assert residual != 0, label
    negatives.append(dict(name=label,residual=str(residual)))
result = dict(at=datetime.now(timezone.utc).isoformat(),
    status='OFF_DIAGONAL_WARD_IDENTITY_THROUGH_FIRST_CURVATURE_CHECKED',
    checks=len(checks),negative_controls=negatives,cpu_seconds=time.process_time()-cpu,
    combined_loop_samples=loop['combined_strong_samples'],source_samples=samples,
    sum_samples=[['0','0','0'],['0','0','0']],
    loop_rank3_coefficients_K1=[str(-v) for v in src],
    source_rank3_coefficients_K1=[str(v) for v in src],
    tensor_identity_modulo='z=sum(x_i^2)',
    completeness_basis='Parity even O4, source index at origin, loop h and Dh jets; covariance and homogeneity used',
    quantum_anomaly_computed=False,full_Q2=False,contacts=False,smooth_W=False,
    tadpoles=False,higher_arities=False,lorentzian_distribution_boundary_values=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p))
    for p in inputs + [Path(__file__),D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
