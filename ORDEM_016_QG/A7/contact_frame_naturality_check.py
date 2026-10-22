"""Check first-curvature naturality, radial frames and contact adjoint signs.

Independent local checks of the bridge, not a new anomaly computation.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, time, uuid
import sympy as s
import bilocal_first_curvature_engine as B

H = Path(__file__).resolve().parent
D = H / 'contact_frame_naturality'
D.mkdir(exist_ok=True)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def put(name, obj):
    p = D / name
    assert not p.exists(), p
    raw = json.dumps(obj, ensure_ascii=False, indent=2).encode()
    tmp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    tmp.write_bytes(raw)
    assert tmp.read_bytes() == raw
    tmp.replace(p)

inputs = [Path(__file__), H / 'bilocal_first_curvature_engine.py',
          H / 'bilocal_XY_extension_contact/results.json',
          H / 'bilocal_curved_contact_primitive/results.json']
put('PRE_REGISTER.json', dict(at=datetime.now(timezone.utc).isoformat(),
    target='Simultaneous infinitesimal isometries of bilocal kernels and regulator through O(K); radial-frame Taylor bridge and contact signs',
    method='Direct Lie derivatives at unfrozen X,Y; symbolic variables, every fiber component',
    warning='This does not verify all vertex contractions or the full QME',
    sources=[dict(path=str(p), sha256=sha(p)) for p in inputs], full_Q2=False))
cpu = time.process_time()
x, y = B.x, B.y
X, Y = B.X, B.Y
radius = (X-Y).dot(X-Y)
checks, negative = [], []

def ck(name, expr):
    value = s.cancel(s.expand(expr).subs(B.w, radius))
    assert value == 0, (name, value)
    checks.append(name)

def k1(pt, axis, a):
    z = sum(v*v for v in pt)
    return -(z*int(a == axis)-pt[a]*pt[axis])/3

def dk1(pt, axis, a, j):
    return s.diff(k1(pt, axis, a), pt[j])

# Check candidate Killing field against the metric, separately at both ends.
for axis in range(4):
    for pt, g1, name in [(x, B.gX1, 'X'), (y, B.gY1, 'Y')]:
        for a in range(4):
            for b in range(4):
                ck(('Killing', name, axis, a, b), s.diff(g1[a,b], pt[axis])
                   + dk1(pt,axis,b,a) + dk1(pt,axis,a,b))
    coord_shift = sum(k1(x,axis,a)*s.diff(radius,x[a])
                      + k1(y,axis,a)*s.diff(radius,y[a]) for a in range(4))
    ck(('geodesic_distance',axis), coord_shift
       + s.diff(B.distance1,x[axis]) + s.diff(B.distance1,y[axis]))
    bad = s.expand(coord_shift)
    assert bad != 0
    negative.append(dict(name='coordinate_distance_is_not_bilocal_scalar_for_transvections',
                         axis=axis, residual=str(bad)))
    for a in range(4):
        for b in range(4):
            g0, g1 = B.ghost(0,a,b), B.ghost(1,a,b)
            value = B.derivative(g1,'X',axis) + B.derivative(g1,'Y',axis)
            for r in range(4):
                value += k1(x,axis,r)*B.derivative(g0,'X',r)
                value += k1(y,axis,r)*B.derivative(g0,'Y',r)
                value -= dk1(x,axis,a,r)*B.ghost(0,r,b)
                value += dk1(y,axis,r,b)*B.ghost(0,a,r)
            ck(('ghost',axis,a,b), value)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    indices = (a,b,c,d)
                    g0, g1 = B.metric(0,*indices), B.metric(1,*indices)
                    value = B.derivative(g1,'X',axis) + B.derivative(g1,'Y',axis)
                    for r in range(4):
                        value += k1(x,axis,r)*B.derivative(g0,'X',r)
                        value += k1(y,axis,r)*B.derivative(g0,'Y',r)
                        for pos, j in enumerate(indices):
                            pt = x if pos < 2 else y
                            changed = list(indices)
                            changed[pos] = r
                            value += dk1(pt,axis,r,j)*B.metric(0,*changed)
                    ck(('metric',axis,*indices),value)
    print('TRANSVECTION',axis,'checks',len(checks),'cpu',time.process_time()-cpu,flush=True)

# Radial parallel coframe to O(K), valid for every tensor component.
I = s.eye(4)
coframe1 = -(B.xx*I-X*X.T)/6
def gamma(a,b,c):
    return -(int(a==c)*x[b]+int(a==b)*x[c]-2*int(b==c)*x[a])/3
for a in range(4):
    for r in range(4):
        euler = sum(x[i]*s.diff(coframe1[a,r],x[i]) for i in range(4))
        transport = sum(x[i]*gamma(r,i,a) for i in range(4))
        ck(('parallel_coframe',a,r), euler-transport)
for a in range(4):
    ck(('radial_geodesic',a),sum(x[i]*x[j]*gamma(a,i,j)
       for i in range(4) for j in range(4)))

# Scalar Fourier test of the two integrations by parts, per contact component.
# q=d_X delta acts on h with q=-p_h. Translating the integrated expression
# to an operator on c uses p_h=-p_c, hence q=p_c, not -p_c.
p = s.symbols('p0:4')
q = s.symbols('q0:4')
data = json.loads((H/'bilocal_XY_extension_contact/results.json').read_bytes())
q2 = sum(v*v for v in q)
for mode in ('geodesic','coordinate'):
    for order in (0,1):
        u,v,w = map(s.Rational,data['coefficients_over_C_E'][mode][order])
        for a in range(4):
            for b in range(4):
                for r in range(4):
                    expr = u*int(a==b)*q[r]*q2**(2-order)
                    expr += v*(int(a==r)*q[b]+int(b==r)*q[a])*q2**(2-order)
                    expr += w*q[a]*q[b]*q[r]*q2**(1-order)
                    left = expr.subs(dict(zip(q,[-v for v in p])),simultaneous=True)
                    right = left.subs(dict(zip(p,[-v for v in q])),simultaneous=True)
                    ck(('two_transposes',mode,order,a,b,r),right-expr)
        bad = s.expand(left.subs(dict(zip(p,q)),simultaneous=True)-expr)
        assert bad != 0
        negative.append(dict(name='one_odd_transpose_loses_sign',mode=mode,
                             order=order,residual=str(bad)))

result = dict(at=datetime.now(timezone.utc).isoformat(),
    status='FIRST_K_BILOCAL_NATURALITY_RADIAL_FRAME_AND_SIGN_CHECKED',
    checks=len(checks),negative_controls=negative,cpu_seconds=time.process_time()-cpu,
    geodesic_regulator_natural_through_first_K=True,
    coordinate_regulator_naturality=False,
    source='Explicit simultaneous Lie derivatives before anchoring; radial transport equations; formal contact pairings',
    limitation='Individual kernels and distance checked, not all vertices or loop assembly. Full nonlinear anomaly and Lorentzian continuation remain open.',
    full_Q2=False)
put('results.json',result)
put('manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p))
    for p in inputs+[D/'PRE_REGISTER.json',D/'results.json']]))
print(json.dumps(result))
