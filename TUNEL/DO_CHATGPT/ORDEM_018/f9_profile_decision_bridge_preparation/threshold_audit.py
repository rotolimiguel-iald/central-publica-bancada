"""Independent rational audit of the existing float reducer; preparation only.

Proof: Mills/Machin/Taylor bounds reviewed by ROOT and preregistros on 2026-10-06.
No observed data, tail re-evaluation, inference, erfc, exp or log here.
"""
from fractions import Fraction
from functools import lru_cache
from math import factorial, isqrt
from frozen_contract import TESTS, SCENARIOS


class AuditUnavailable(ValueError):
    pass


def need(ok, reason):
    if not ok:
        raise AuditUnavailable(reason)


def enc(value):
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def prob(value):
    need(type(value) is dict and set(value) == {"numerator", "denominator"}, "P_SCHEMA")
    a, b = value["numerator"], value["denominator"]
    need(type(a) is str and type(b) is str and 1 <= len(a) <= 155 and 1 <= len(b) <= 155,
         "P_INPUT_BOUND")
    need(a.isascii() and a.isdigit() and b.isascii() and b.isdigit(), "P_GRAMMAR")
    x, y = int(a), int(b)
    need(str(x) == a and str(y) == b and 0 < x <= y and y.bit_length() <= 512,
         "P_RANGE")
    return Fraction(x, y)


def atan_partial(x, last):
    return sum(((-1)**n * x**(2*n+1) / (2*n+1)
                for n in range(last+1)), Fraction(0))


def integral_partial(last):
    return sum((Fraction((-1)**n * 5**(2*n+1),
                         2**n * factorial(n) * (2*n+1))
                for n in range(last+1)), Fraction(0))


def sqrt_bounds(x):
    q = 10**70
    a, b = x.numerator, x.denominator
    k = isqrt((a*q*q)//b)
    need(k*k*b <= a*q*q < (k+1)*(k+1)*b, "INTEGER_SQRT_ENCLOSURE")
    return Fraction(k, q), Fraction(k+1, q)


@lru_cache(maxsize=1)
def alpha_interval():
    """Finite exact construction, not a measured floating alpha or libm premise."""
    x, y = Fraction(1, 5), Fraction(1, 239)
    pi_lower = 16*atan_partial(x, 65) - 4*atan_partial(y, 64)
    pi_upper = 16*atan_partial(x, 64) - 4*atan_partial(y, 65)
    s_lower, _ = sqrt_bounds(2*pi_lower)
    _, s_upper = sqrt_bounds(2*pi_upper)
    lower = Fraction(1, 2) - integral_partial(128)/s_lower
    upper = Fraction(1, 2) - integral_partial(127)/s_upper
    need(0 < lower < upper < 1, "ALPHA_INTERVAL_RANGE")
    need(upper-lower < Fraction(1, 10**69), "ALPHA_INTERVAL_PRECISION")
    need(Fraction(5, 2**25) < lower < upper < Fraction(5, 2**24), "ALPHA_DYADIC_BRACKET")
    return lower, upper


def rejection(bound, interval):
    lower, upper = interval
    if bound <= lower:
        return True
    if bound > upper:
        return False
    raise AuditUnavailable("ALPHA_INTERVAL_CROSSED")


def audit(records, bindings, proposal):
    """Check ALL decision-bearing values against original rational tail bounds.

    Incomplete calibration remains incomplete. Near-threshold or float mismatch
    yields no certified decision, while the caller retains calibration evidence.
    Returned scientific fields contain exact rationals/booleans, never float p/log.
    """
    interval = alpha_interval()
    need(set(records) == set(TESTS) and set(proposal["tests"]) == set(TESTS), "TEST_SET")
    need(proposal["scenario_ids"] == list(SCENARIOS) and proposal["multiplicity"] == 5, "FAMILY_OR_FWER")
    tests = {}
    directions = {}
    for test in TESTS:
        rows = records[test]
        target = proposal["tests"][test]
        need(tuple(rows) == SCENARIOS and tuple(target["scenarios"]) == SCENARIOS, "SCENARIO_ORDER")
        completed = {}
        missing, raw_bounds, signed = [], [], {}
        for sid in SCENARIOS:
            raw, actual = rows[sid], target["scenarios"][sid]
            complete = (raw["statistic_available"] and raw["statistic_valid"] and
                        raw["calibration_status"] == "VALID_UNIFORM_NULL_OR_CONSERVATIVE_BOUND")
            need(actual["status"] == "AVAILABLE" and actual["record"] == raw and
                 actual["complete"] is complete, "SCENARIO_RECORD_OR_COMPLETENESS")
            if complete:
                key = test+":"+sid
                need(key in bindings, "RATIONAL_BOUND_MISSING")
                saved = bindings[key]
                p = prob(saved["log"]["probability_upper"])
                adjusted = min(Fraction(1), 5*p)
                reject = rejection(adjusted, interval)
                lower_stat = saved["lower"]
                need(type(lower_stat) is Fraction, "EXACT_LOWER_REQUIRED")
                signed[sid] = lower_stat > 0
                expected_direction = test in TESTS[2:] and lower_stat > 0
                need(raw["direction_positive_certified"] is expected_direction, "DIRECTION_EXACT_SIGN")
                raw_bounds.append(p)
                completed[sid] = {"complete": True, "reject": reject,
                                  "p_upper": enc(p), "p_FWER_upper": enc(adjusted)}
            else:
                reject = None
                missing.append(sid)
                completed[sid] = {"complete": False, "reject": None,
                                  "p_upper": None, "p_FWER_upper": None}
            need(actual["reject_within_scenario"] is reject, "FLOAT_SCENARIO_DECISION_MISMATCH")
        complete = not missing
        robust = max(raw_bounds) if complete else None
        adjusted = min(Fraction(1), 5*robust) if complete else None
        reject = rejection(adjusted, interval) if complete else None
        direction = (complete and test in TESTS[2:] and all(signed.values()))
        status = "COMPLETE_CONDITIONAL_CALIBRATION" if complete else "CALIBRATION_UNAVAILABLE_OR_PARTIAL"
        need(target["complete"] is complete and target["incomplete_scenarios"] == missing
             and target["reject"] is reject and target["status"] == status
             and target["all_directions_positive_certified"] is direction,
             "FLOAT_ROBUST_DECISION_MISMATCH")
        tests[test] = {"complete": complete, "reject": reject, "status": status,
                       "incomplete_scenarios": missing, "scenarios": completed,
                       "p_robust": enc(robust) if complete else None,
                       "p_FWER_upper": enc(adjusted) if complete else None,
                       "all_directions_positive_certified": direction}
        directions[test] = signed
    h1_rejected = any(tests[t]["reject"] is True for t in TESTS[:2])
    h1_nonrejected = all(tests[t]["complete"] and tests[t]["reject"] is False for t in TESTS[:2])
    compat = {"H1_rejected": h1_rejected, "H1_calibrated_not_rejected": h1_nonrejected,
              "missing_tests": [t for t in TESTS[:2] if not tests[t]["complete"]],
              "status": "ROUTE_H1_REJECTED_AT_5SIGMA_CONDITIONAL_CONTRACT" if h1_rejected else
                        "NOT_FALSIFIED_IN_THIS_CONTRACT" if h1_nonrejected else
                        "CALIBRATION_UNAVAILABLE_OR_PARTIAL"}
    comparisons = {}
    for test in TESTS[2:]:
        item = tests[test]
        combined = (h1_nonrejected and item["complete"]
                    and item["all_directions_positive_certified"] and item["reject"] is True)
        comparisons[test] = {"null_rejected": item["reject"], "combined_discrimination": combined,
                             "direction_complete": item["all_directions_positive_certified"],
                             "status": "CONDITIONAL_DISCRIMINATION_THRESHOLD_MET" if combined else
                                       "NO_COMBINED_CLAIM" if item["complete"] else
                                       "CALIBRATION_UNAVAILABLE_OR_PARTIAL"}
    need(proposal["compatibility"] == compat and proposal["comparisons"] == comparisons,
         "COMBINED_LOGIC_MISMATCH")
    if h1_rejected:
        status = compat["status"]
    elif any(v["combined_discrimination"] for v in comparisons.values()):
        status = "CONDITIONAL_DISCRIMINATION_THRESHOLD_MET"
    elif not all(t["complete"] for t in tests.values()):
        status = "CALIBRATION_UNAVAILABLE_OR_PARTIAL"
    else:
        mixed = any(len({r["reject"] for r in t["scenarios"].values()}) > 1 for t in tests.values())
        mixed_direction = any(len(set(directions[t].values())) > 1 for t in TESTS[2:])
        status = "SYSTEMATICS_SENSITIVE_RESULT" if mixed or mixed_direction else "NO_COMBINED_DISCRIMINATION_THRESHOLD_MET"
    need(proposal["status"] == status, "TOP_LEVEL_STATUS_MISMATCH")
    need(proposal["authorization_granted"] is False and proposal["gate_changed"] is False
         and proposal["observed_statistic_computed"] is False, "NO_AUTHORITY_OR_REEXECUTION")
    return {"schema": "F9_EXACT_THRESHOLD_AUDIT_V1", "status": status,
            "family_count": len(SCENARIOS), "family_factor": 5,
            "alpha5_interval": {"lower": enc(interval[0]), "upper": enc(interval[1])},
            "tests": tests, "compatibility": compat, "comparisons": comparisons,
            "p_semantics": "CERTIFIED_CONSERVATIVE_UPPER_CONDITIONAL_ON_EXTERNAL_SCIENTIFIC_PROOFS",
            "nonrejection_semantics": "NO_REJECTION_BY_CONSERVATIVE_BOUND_NOT_PROOF_TRUE_P_IS_LARGE",
            "float_values_certified": False, "physical_confirmation": False,
            "authorization_granted": False, "gate_changed": False}
