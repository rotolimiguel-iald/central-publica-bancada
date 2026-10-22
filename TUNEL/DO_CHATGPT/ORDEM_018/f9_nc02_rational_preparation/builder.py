"""NC02-RAT-01 only: build a rational dual lower and feasible upper witness.

Preparation only; no execution permission is embedded in this module.
No expected analytic value, metadata pin or source hash participates in the
calculation. The external worker binds the payload/dependency bytes and request.
"""
from codec_adapter import ExactArithmetic, InvalidRational, RationalResourceLimit

SCHEMA = "F9_NC02_RATIONAL_UNIT_PROPOSAL_V1"
PREPARATION_ID = "bf2a5692-1aff-423e-9345-7bfa256d5072"
UNIT_ID = PREPARATION_ID + "::NC02-RAT-01"
TARGET = "SYNTHETIC_NC02_ONLY_NOT_ANY_PHYSICAL_HYPOTHESIS"
CASE_IDS = ("NC02-RAT-01-POSITIVE", "NC02-RAT-01-NEGATIVE-ANNIHILATION")


class InvalidFixture(ValueError):
    """Input lies outside the two fixed synthetic cases."""


def _require(condition, reason):
    if not condition:
        raise InvalidFixture(reason)


def _mapping(value, required, optional=()):
    _require(type(value) is dict, "MAPPING_REQUIRED")
    keys = set(value)
    _require(set(required) <= keys <= set(required) | set(optional), "MAPPING_KEYS")


def _list(value, size):
    _require(type(value) is list and len(value) == size, "FIXED_LIST_SHAPE")
    return value


def _pair_equal(value, numerator, denominator):
    return value.numerator == numerator and value.denominator == denominator


def _fixed(value, numerator, denominator):
    _require(_pair_equal(value, numerator, denominator), "VALUE_OUTSIDE_FIXED_FIXTURE")


def _vector(raw, arithmetic):
    return tuple(arithmetic.parse(x) for x in _list(raw, 2))


def _dot(a, b, arithmetic):
    _require(len(a) == len(b) == 2, "INTERNAL_VECTOR_SHAPE")
    return arithmetic.add(arithmetic.multiply(a[0], b[0]),
                          arithmetic.multiply(a[1], b[1]))


def _case(raw, arithmetic):
    _require(type(raw) is dict and type(raw.get("id")) is str, "CASE_ID_TYPE")
    case_id = raw["id"]
    _require(case_id in CASE_IDS, "UNKNOWN_CASE_ID")
    required = ("id", "dual_v", "witness") if case_id == CASE_IDS[0] else ("id", "dual_v")
    # Annotation keys are allowed; neither their values nor predictions are read.
    _mapping(raw, required, ("required_checks", "expected_analytic_not_run"))
    v = _vector(raw["dual_v"], arithmetic)
    _fixed(v[0], 1, 4)
    if case_id == CASE_IDS[0]:
        _fixed(v[1], -1, 4)
        _mapping(raw["witness"], ("u", "eta"))
        u = arithmetic.parse(raw["witness"]["u"])
        eta = arithmetic.parse(raw["witness"]["eta"])
        _fixed(u, 1, 2)
        _fixed(eta, 3, 4)
        witness = (u, eta)
    else:
        _fixed(v[1], -255, 1024)
        witness = None
    return case_id, v, witness


def _geometry_and_scope(payload, case, arithmetic):
    _require(type(payload) is dict, "PAYLOAD_MAPPING")
    _require(payload.get("schema") == SCHEMA and type(payload.get("schema")) is str,
             "SCHEMA_OUTSIDE_SCOPE")
    _require(all(type(payload.get(k)) is str for k in
                 ("preparation_request_id", "proposed_unit_identity", "target")),
             "UNIT_OR_TARGET_TYPE")
    _require(payload.get("preparation_request_id") == PREPARATION_ID and
             payload.get("proposed_unit_identity") == UNIT_ID and
             payload.get("target") == TARGET, "UNIT_OR_TARGET_OUTSIDE_SCOPE")
    # Operational authorization/pins are external. These fields only prevent a
    # physical-contract mutation from being accepted as the same toy proposal.
    _require(payload.get("canonical_F9_contract_changed") is False,
             "PHYSICAL_CONTRACT_CHANGE_OUTSIDE_SCOPE")
    geometry = payload.get("geometry")
    _mapping(geometry, ("C", "X", "data_dimension", "nuisance_dimension",
                        "support", "nuisance_domain", "no_numerical_rank_or_tolerance"))
    _require(type(geometry["data_dimension"]) is int and geometry["data_dimension"] == 2,
             "DATA_DIMENSION")
    _require(type(geometry["nuisance_dimension"]) is int and geometry["nuisance_dimension"] == 1,
             "NUISANCE_DIMENSION")
    _require(type(geometry["support"]) is str and type(geometry["nuisance_domain"]) is str,
             "GEOMETRY_LABEL_TYPE")
    _require(geometry["support"] == "R^2" and geometry["nuisance_domain"] == "R" and
             geometry["no_numerical_rank_or_tolerance"] is True, "GEOMETRY_SCOPE")
    C = tuple(_vector(row, arithmetic) for row in _list(geometry["C"], 2))
    X = tuple(arithmetic.parse(_list(row, 1)[0]) for row in _list(geometry["X"], 2))
    for i in range(2):
        _fixed(X[i], 1, 1)
        for j in range(2):
            _fixed(C[i][j], 1 if i == j else 0, 1)
    cell = payload.get("cell")
    _mapping(cell, ("coordinate", "closed_lower", "closed_upper",
                    "b_constant", "b_linear", "cover"))
    _require(type(cell["coordinate"]) is str and type(cell["cover"]) is str,
             "CELL_LABEL_TYPE")
    _require(cell["coordinate"] == "u" and
             cell["cover"] == "this one closed interval is the entire toy domain",
             "CELL_SCOPE")
    lo = arithmetic.parse(cell["closed_lower"])
    hi = arithmetic.parse(cell["closed_upper"])
    _fixed(lo, 0, 1)
    _fixed(hi, 1, 2)
    b0 = _vector(cell["b_constant"], arithmetic)
    b1 = _vector(cell["b_linear"], arithmetic)
    for value, num in zip(b0 + b1, (1, 0, 0, 1)):
        _fixed(value, num, 1)
    # Validate the two input cases and exact order. The selected case is decoded
    # separately, so a detached JSON copy is permitted without trusting flags.
    catalog = tuple(_case(x, arithmetic) for x in _list(payload.get("cases"), 2))
    _require(tuple(x[0] for x in catalog) == CASE_IDS, "CASE_ORDER_OR_DUPLICATE")
    selected = _case(case, arithmetic)
    catalog_case = catalog[CASE_IDS.index(selected[0])]
    # Both decoded cases have already passed exact fixed-fixture restrictions.
    _require(selected[0] == catalog_case[0], "SELECTED_CASE_NOT_IN_PAYLOAD")
    return C, X, lo, hi, b0, b1, selected


def _output(case_id, status, reason=None):
    return {"case_id": case_id, "status": status, "reason": reason,
            "annihilation_residual": None,
            "dual_affine_constant": None, "dual_affine_slope": None,
            "lower": None, "upper": None, "witness": None}


def build_case(payload, case, rational_parser):
    """Return JSON primitives; refuse out-of-scope input without accepted bounds.

    rational_parser must be the externally pinned _rational dependency and must
    return (int, int). Its identity is checked by the worker, never guessed here.
    """
    case_id = case.get("id") if type(case) is dict else None
    case_id = case_id if type(case_id) is str and case_id in CASE_IDS else None
    try:
        arithmetic = ExactArithmetic(rational_parser)
        C, X, lo, hi, b0, b1, selected = _geometry_and_scope(payload, case, arithmetic)
        case_id, v, witness = selected
        annihilation = _dot(X, v, arithmetic)
        if annihilation.numerator != 0:
            result = _output(case_id, "INVALID_DUAL_ANNIHILATION",
                             "EXACT_NONZERO_X_TRANSPOSE_V_UNBOUNDED_NUISANCE")
            result["annihilation_residual"] = arithmetic.encode(annihilation)
            # No dual coefficients, endpoint bound or upper witness is evaluated.
            return result
        _require(witness is not None, "FEASIBLE_WITNESS_REQUIRED")
        zero = arithmetic.integer(0)
        two = arithmetic.integer(2)
        Cv = tuple(_dot(row, v, arithmetic) for row in C)
        constant = arithmetic.subtract(
            arithmetic.multiply(two, _dot(v, b0, arithmetic)),
            _dot(v, Cv, arithmetic))
        slope = arithmetic.multiply(two, _dot(v, b1, arithmetic))
        lower_endpoint = arithmetic.add(constant, arithmetic.multiply(slope, lo))
        upper_endpoint = arithmetic.add(constant, arithmetic.multiply(slope, hi))
        lower = (lower_endpoint if arithmetic.compare(lower_endpoint, upper_endpoint) <= 0
                 else upper_endpoint)
        if arithmetic.compare(lower, zero) < 0:
            lower = zero
        u, eta = witness
        _require(arithmetic.compare(lo, u) <= 0 and arithmetic.compare(u, hi) <= 0,
                 "WITNESS_OUTSIDE_CLOSED_CELL")
        b_point = tuple(arithmetic.add(b0[i], arithmetic.multiply(b1[i], u))
                        for i in range(2))
        residual = tuple(arithmetic.subtract(b_point[i], arithmetic.multiply(X[i], eta))
                         for i in range(2))
        # C is exactly I2; this is a feasible nuisance value, not an optimizer.
        upper = _dot(residual, residual, arithmetic)
        _require(arithmetic.compare(lower, upper) <= 0, "INCONSISTENT_DERIVED_BOUNDS")
        status = ("CERTIFIED_TOY_MINIMUM" if arithmetic.compare(lower, upper) == 0
                  else "CERTIFIED_TOY_MINIMUM_INTERVAL")
        result = _output(case_id, status)
        result.update({
            "annihilation_residual": arithmetic.encode(annihilation),
            "dual_affine_constant": arithmetic.encode(constant),
            "dual_affine_slope": arithmetic.encode(slope),
            "lower": arithmetic.encode(lower), "upper": arithmetic.encode(upper),
            "witness": {"u": arithmetic.encode(u), "eta": arithmetic.encode(eta),
                        "residual": [arithmetic.encode(x) for x in residual]},
        })
        return result
    except RationalResourceLimit as error:
        return _output(case_id, "RESOURCE_LIMIT", str(error))
    except (InvalidRational, InvalidFixture) as error:
        return _output(case_id, "INVALID_INPUT", str(error))
