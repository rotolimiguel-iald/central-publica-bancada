"""Transverse regulator contact invisible after anchoring; exact first-K test.

This compares two specified off-diagonal extensions of the same anchored
regulator. It does not select a physical state or establish a full Ward sum.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, time, uuid
import sympy as s
import bilocal_first_curvature_engine as B

H = Path(__file__).resolve().parent
D = H / 'bilocal_regulator_contact'
D.mkdir(exist_ok=True)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def put(name, value):
    p = D / name
    assert not p.exists()
    b = json.dumps(value, indent=2).encode()
    t = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    t.write_bytes(b)
    assert t.read_bytes() == b
    t.replace(p)

sources = [Path(__file__), H / 'bilocal_first_curvature_engine.py']
put('PRE_REGISTER.json', dict(
    at=datetime.now(timezone.utc).isoformat(),
    target='Difference of second Y derivatives of rho^(2a) versus w^a at Y=0',
    prescription='FP_a (1-a) mu^(2a) rho^(2a), rho²=w+K distance1; comparator w=(X-Y)²',
    test_distributions=['w^-2', 'w^-2 log(mu²w)'],
    source_scope='Two chosen completions of the anchored prescription; no selection by Ward cancellation',
    sources=[dict(path=str(p), sha256=sha(p)) for p in sources]))

cpu = time.process_time()
checks = []
negative = []
def ck(name, value):
    value = s.cancel(value)
    assert value == 0, (name, value)
    checks.append(name)

# Expand (rho²)^a = w^a [1 + K a distance1/w] before differentiating.
# distance1 and its first Y derivative vanish at Y=0; only the second remains.
ck('coincident_anchor_value', B.anchored(B.distance1))
for i in range(4):
    ck(f'anchor_first_{i}', B.anchored(s.diff(B.distance1, B.y[i])))
second = []
for i in range(4):
    for j in range(4):
        actual = B.anchored(s.diff(B.distance1, B.y[i], B.y[j]))
        expected = -s.Rational(2, 3) * (B.xx * int(i == j) - B.x[i] * B.x[j])
        ck(f'second_distance_{i}_{j}', actual - expected)
        # Sphere average <n_i n_j> = delta_ij / 4, measure area S^3=2pi².
        avg = -s.Rational(2, 3) * (int(i == j) - s.Rational(int(i == j), 4))
        second.append(dict(i=i, j=j, distance=str(actual), regulator_angular_factor=str(avg)))

# Analytic radial continuation on a smooth test equal to one near the origin.
# The integral over 0<r<1 is exactly 1/(2a); the outer compact annulus is analytic.
# A derivative in a yields log(mu²w), INCLUDING the mu factor.
a = s.Symbol('a')
log_mu = s.Symbol('log_mu')
regulated_radial = s.exp(2*a*log_mu) / (2*a)
contacts = []
for ell in (0, 1):
    family = s.diff(regulated_radial, a, ell)
    finite = s.expand(s.series(a*(1-a)*family, a, 0, 1).removeO()).coeff(a, 0)
    ck(f'finite_part_radial_{ell}', finite-s.Rational(1, 2))
    for i in range(4):
        for j in range(4):
            avg = -s.Rational(1, 2) * int(i == j)
            value = s.simplify(2*s.pi**2 * avg * finite)
            expected = -s.pi**2*s.Rational(1, 2)*int(i == j)
            ck(f'contact_{ell}_{i}_{j}', value-expected)
            contacts.append(dict(ell=ell, i=i, j=j, coefficient_of_K_delta=str(value)))
            if i == j:
                assert value != 0
                negative.append(f'anchor_before_two_derivatives_fails_{ell}_{i}')

result = dict(
    at=datetime.now(timezone.utc).isoformat(),
    status='TRANSVERSE_REGULATOR_CONTACT_MEASURED', checks=len(checks),
    negative_controls=len(negative), check_names=checks, negative_names=negative,
    cpu_seconds=time.process_time()-cpu,
    formula='For u=w^-2 log(mu²w)^ell (ell=0,1), delta(DYi DYj R) at Y=0 = -K pi² delta_ij delta^(4)(X)/2, through firstK',
    interpretation='Difference between rho² and w regulator completions; scalar flat-measure contact coefficient at orderK',
    proof='Radial meromorphic integral, sphere second moment, exact transverse distance derivatives',
    locality='Terms in the test vanishing at X=0 have no pole at a=0 in this critical-degree example',
    full_Q2=False, general_bitensor_commutator=False,
    second_distance=second, contacts=contacts)
put('results.json', result)
put('manifest.json', dict(artifacts=[dict(path=str(p), sha256=sha(p)) for p in
    sources+[D/'PRE_REGISTER.json', D/'results.json']]))
print(json.dumps({k:v for k,v in result.items() if k not in ('second_distance','contacts','check_names','negative_names')}))
