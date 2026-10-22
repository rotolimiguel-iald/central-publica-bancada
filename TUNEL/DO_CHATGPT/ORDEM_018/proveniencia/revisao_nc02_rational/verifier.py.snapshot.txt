"""Independent NC02 verifier: integer pairs, no Fraction or builder imports.

This verifies only the frozen two-dimensional synthetic experiment. It does
not qualify physical geometry, a cosmological prediction or a general solver.
The caller pins the full payload and attaches its identity to this result.
"""
from math import gcd

MAX_BITS = 4096
ZERO = (0, 1)
ONE = (1, 1)
FIELDS = {"case_id", "status", "annihilation_residual", "dual_affine_constant",
          "dual_affine_slope", "lower", "upper", "witness", "reason"}


class InvalidCertificate(Exception):
    pass


def require(condition, message):
    if not condition:
        raise InvalidCertificate(message)


def norm(n, d):
    require(type(n) is int and type(d) is int and d != 0, "PAIR_TYPE")
    require(abs(n).bit_length() <= MAX_BITS and abs(d).bit_length() <= MAX_BITS,
            "INTERMEDIATE_BITS")
    if d < 0:
        n, d = -n, -d
    g = gcd(abs(n), d)
    return n // g, d // g


def multiply_int(a, b):
    require(abs(a).bit_length() + abs(b).bit_length() <= MAX_BITS,
            "PRODUCT_PREFLIGHT_BITS")
    return a * b


def add(a, b):
    x = multiply_int(a[0], b[1])
    y = multiply_int(b[0], a[1])
    require(max(abs(x).bit_length(), abs(y).bit_length()) + 1 <= MAX_BITS,
            "SUM_PREFLIGHT_BITS")
    return norm(x + y, multiply_int(a[1], b[1]))


def neg(a):
    return -a[0], a[1]


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    return norm(multiply_int(a[0], b[0]), multiply_int(a[1], b[1]))


def less(a, b):
    return multiply_int(a[0], b[1]) < multiply_int(b[0], a[1])


def minimum(a, b):
    return a if less(a, b) else b


def dot(a, b):
    require(len(a) == len(b) == 2, "VECTOR_DIMENSION")
    return add(mul(a[0], b[0]), mul(a[1], b[1]))


def encode(a):
    return {"numerator": str(a[0]), "denominator": str(a[1])}


def parse(value, parser):
    pair = parser(value)
    require(type(pair) is tuple and len(pair) == 2, "CODEC_RETURN")
    n, d = pair
    require(type(n) is int and type(d) is int and d > 0, "CODEC_PAIR")
    require(abs(n).bit_length() <= 512 and d.bit_length() <= 512,
            "CODEC_INPUT_BITS")
    require(norm(n, d) == pair and encode(pair) == value, "CODEC_CANONICAL")
    return pair


def verify_case(payload, case, certificate, rational_parser):
    """Recompute endpoints and a feasible residual, never use expected output."""
    require(type(certificate) is dict and set(certificate) == FIELDS,
            "CERTIFICATE_SCHEMA")
    require(certificate["case_id"] == case["id"], "CASE_BINDING")
    p = lambda value: parse(value, rational_parser)
    geometry = payload["geometry"]
    require(geometry["data_dimension"] == 2 and geometry["nuisance_dimension"] == 1,
            "GEOMETRY_DIMENSIONS")
    c = [[p(x) for x in row] for row in geometry["C"]]
    x = [[p(a) for a in row] for row in geometry["X"]]
    require(c == [[ONE, ZERO], [ZERO, ONE]] and x == [[ONE], [ONE]],
            "GEOMETRY_OUTSIDE_SCOPE")
    require(geometry["support"] == "R^2" and geometry["nuisance_domain"] == "R",
            "GEOMETRY_DOMAIN")
    cell = payload["cell"]
    lo, hi = p(cell["closed_lower"]), p(cell["closed_upper"])
    a = [p(z) for z in cell["b_constant"]]
    t = [p(z) for z in cell["b_linear"]]
    require(lo == ZERO and hi == (1, 2) and a == [ONE, ZERO] and t == [ZERO, ONE],
            "CELL_OUTSIDE_SCOPE")
    v = [p(z) for z in case["dual_v"]]
    require(len(v) == 2, "DUAL_DIMENSION")
    annihilation = add(v[0], v[1])
    require(p(certificate["annihilation_residual"]) == annihilation,
            "ANNIHILATION_WITNESS_MISMATCH")
    bounds = ("dual_affine_constant", "dual_affine_slope", "lower", "upper", "witness")
    if annihilation != ZERO:
        require(certificate["status"] == "INVALID_DUAL_ANNIHILATION" and
                certificate["reason"] == "EXACT_NONZERO_X_TRANSPOSE_V_UNBOUNDED_NUISANCE" and
                all(certificate[k] is None for k in bounds),
                "NONZERO_ANNIHILATION_MUST_REFUSE")
        return {"verified": True, "case_id": case["id"],
                "status": "VERIFIED_REFUSAL", "annihilation": encode(annihilation),
                "physical_certificate": False}
    require(certificate["status"] == "CERTIFIED_TOY_MINIMUM" and certificate["reason"] is None, "POSITIVE_STATUS")
    # Independent path: evaluate the dual at both endpoints, not via the
    # builder's coefficient-based lower-bound computation.
    dual_endpoints = []
    vv = dot(v, v)
    for u in (lo, hi):
        b = [add(a[j], mul(t[j], u)) for j in range(2)]
        vb = dot(v, b)
        dual_endpoints.append(sub(add(vb, vb), vv))
    lower = minimum(*dual_endpoints)
    if less(lower, ZERO):
        lower = ZERO
    const = p(certificate["dual_affine_constant"])
    slope = p(certificate["dual_affine_slope"])
    for u, endpoint in zip((lo, hi), dual_endpoints):
        require(add(const, mul(slope, u)) == endpoint, "AFFINE_ENDPOINT_MISMATCH")
    require(p(certificate["lower"]) == lower, "LOWER_MISMATCH")
    witness = certificate["witness"]
    require(type(witness) is dict and set(witness) == {"u", "eta", "residual"}, "WITNESS_SCHEMA")
    require({k: witness[k] for k in ("u", "eta")} == case["witness"], "WITNESS_BINDING")
    u, eta = p(witness["u"]), p(witness["eta"])
    require(not less(u, lo) and not less(hi, u), "INFEASIBLE_WITNESS")
    residual = [sub(add(a[j], mul(t[j], u)), eta) for j in range(2)]
    upper = dot(residual, residual)
    require(witness["residual"] == [encode(r) for r in residual], "RESIDUAL_WITNESS_MISMATCH")
    require(p(certificate["upper"]) == upper and not less(upper, lower),
            "UPPER_OR_INTERVAL_MISMATCH")
    return {"verified": True, "case_id": case["id"], "status": "VERIFIED_TOY_INTERVAL",
            "lower": encode(lower), "upper": encode(upper),
            "exact_minimum": lower == upper, "physical_certificate": False}
