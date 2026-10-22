"""Exact polynomial checks of weighted curvature integration by parts, flat 4D.

These are algebraic controls, not curved-space proofs or physical measurements.
All outputs are exclusive. No canonical imports, parameter fitting, or data.
"""
from pathlib import Path
import json, hashlib
import sympy as s

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'BOUNDARY_CONTROLS.json'
if OUT.exists():
    raise FileExistsError(OUT)
x = s.symbols('t x y z', real=True)
sign = [1, -1, -1, -1]

def integral(p, variables):
    p = s.Poly(s.expand(p), *variables)
    out = s.S(0)
    for powers, c in p.terms():
        if all(k % 2 == 0 for k in powers):
            out += c * s.prod(s.Rational(2, k + 1) for k in powers)
    return s.factor(out)

def check(label, f, h, zero_flux):
    # h is the covariant metric variation; H is its raised version.
    H = s.Matrix(4, 4, lambda a, b: sign[a]*sign[b]*h[a,b])
    tr = sum(sign[a]*h[a,a] for a in range(4))
    boxf = sum(sign[a]*s.diff(f,x[a],2) for a in range(4))
    V = [sum(s.diff(H[a,b],x[b]) for b in range(4))
         -sign[a]*s.diff(tr,x[a]) for a in range(4)]
    B = [f*V[a]-sum(s.diff(f,x[b])*H[a,b] for b in range(4))
         +sign[a]*s.diff(f,x[a])*tr for a in range(4)]
    raw = f*sum(s.diff(V[a],x[a]) for a in range(4))
    bulk = sum((sign[a]*sign[b]*s.diff(f,x[a],x[b])
                -(sign[a]*boxf if a == b else 0))*h[a,b]
               for a in range(4) for b in range(4))
    divergence = sum(s.diff(B[a],x[a]) for a in range(4))
    assert s.expand(raw-bulk-divergence) == 0
    iraw, ibulk = integral(raw,x), integral(bulk,x)
    flux = sum(integral(B[a].subs(x[a],1)-B[a].subs(x[a],-1),
                        [v for v in x if v != x[a]]) for a in range(4))
    assert s.simplify(iraw-ibulk-flux) == 0
    if zero_flux:
        assert flux == 0
        for a in range(4):
            for side in [-1,1]:
                assert all(s.expand(h[i,j].subs(x[a],side)) == 0
                           for i in range(4) for j in range(4))
                assert all(s.expand(s.diff(h[i,j],v).subs(x[a],side)) == 0
                           for i in range(4) for j in range(4) for v in x)
    else:
        assert flux != 0
    return {'case':label,'pointwise_residual':'0','integral_raw':str(iraw),
            'integral_bulk':str(ibulk),'boundary_flux':str(flux),
            'zero_boundary_metric_and_first_jet':zero_flux}

w = s.prod((1-v*v)**2 for v in x)
f = 1+x[0]**2+2*x[1]**2+3*x[0]*x[1]+x[2]*x[3]
A = s.Matrix([[1,2,0,0],[2,3,0,0],[0,0,4,1],[0,0,1,5]])
cases = [check('weighted_zero_boundary_jet',f,w*A,True),
         check('constant_weight_zero_boundary_jet',s.S(1),w*A,True),
         check('nonzero_boundary_flux_must_be_kept',s.S(1),x[0]**2*s.eye(4),False)]
result = {'status':'PASS_EXACT_ALGEBRA_ONLY','dimension':4,
          'metric_signature':[1,-1,-1,-1],'domain':'[-1,1]^4',
          'sympy_version':s.__version__,'cases':cases,
          'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'limits':['Flat constant metric; no curved-connection proof.',
                    'Zero boundary value AND first jet; not mere Dirichlet data.',
                    'No stationarity inferred; no physical data or sigma significance.']}
with OUT.open('x',encoding='utf-8') as stream:
    json.dump(result,stream,ensure_ascii=False,indent=2)
print(json.dumps(result,ensure_ascii=False))
