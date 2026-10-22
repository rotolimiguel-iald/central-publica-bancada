"""Pure V2 logical decisions over caller-verified records; no data authorization."""
import math

CONTRACT_SHA256 = "6b5118548490392a26eb43a8de9e5a252ae6e6fd28c3d0edbc2daa15c5813655"
TESTS = ("COMPAT_H1", "LAW_H1_VS_FREE", "H2_TO_H1", "H4_TO_H1", "H5_TO_H1")
CALIBRATIONS = ("VALID_UNIFORM_NULL_OR_CONSERVATIVE_BOUND", "UNAVAILABLE", "PARTIAL", "INVALID")
RECORD_KEYS = {"statistic", "statistic_available", "statistic_valid", "calibration_status",
               "calibration_scope", "log_p_upper", "numerical_certificate",
               "calibration_reference", "direction_positive_certified", "direction_reference"}

class DecisionError(ValueError):
    pass

def _need(condition, message):
    if not condition:
        raise DecisionError(message)

def _flag(value, name):
    _need(type(value) is bool, name + " must be bool")
    return value

def _number(value, name):
    _need(type(value) in (int, float), name + " must be a built-in finite number")
    try:
        result = float(value)
    except (ValueError, OverflowError) as exc:
        raise DecisionError(name + " not representable") from exc
    _need(math.isfinite(result), name + " must be finite")
    return result

def _reference(value, name):
    _need(type(value) is dict and set(value) == {"id", "sha256"}, name + " reference keys")
    _need(type(value["id"]) is str and bool(value["id"].strip()), name + " reference id")
    digest = value["sha256"]
    _need(type(digest) is str and len(digest) == 64 and
          all(c in "0123456789abcdef" for c in digest), name + " SHA256")
    return dict(value)

def _record(raw, test):
    _need(type(raw) is dict and set(raw) == RECORD_KEYS, "record keys")
    result = dict(raw)
    available = _flag(raw["statistic_available"], "statistic_available")
    valid = _flag(raw["statistic_valid"], "statistic_valid")
    direction = _flag(raw["direction_positive_certified"], "direction_positive_certified")
    _need(not valid or available, "valid statistic cannot be unavailable")
    if available:
        result["statistic"] = _number(raw["statistic"], "statistic")
        if valid and test in TESTS[:2]:
            _need(result["statistic"] >= 0, "valid G/Q must be nonnegative")
    else:
        _need(raw["statistic"] is None, "unavailable statistic must be null")
    _need(raw["calibration_status"] in CALIBRATIONS, "calibration status")
    _need(type(raw["calibration_scope"]) is str, "calibration scope")
    for name in ("numerical_certificate", "calibration_reference", "direction_reference"):
        if raw[name] is not None:
            result[name] = _reference(raw[name], name)
    if raw["calibration_status"] == CALIBRATIONS[0]:
        _need(valid and bool(raw["calibration_scope"].strip()), "calibration requires valid statistic and scope")
        value = _number(raw["log_p_upper"], "log_p_upper")
        _need(value <= 0, "log probability exceeds zero")
        result["log_p_upper"] = value
        _need(raw["numerical_certificate"] is not None and raw["calibration_reference"] is not None,
              "complete calibration requires both external references")
    else:
        _need(raw["log_p_upper"] is None, "uncalibrated record cannot carry an admitted p bound")
    if direction:
        _need(test in TESTS[2:] and valid and result["statistic"] > 0 and raw["direction_reference"] is not None,
              "certified direction requires valid positive rival statistic and reference")
    else:
        _need(raw["direction_reference"] is None, "unasserted direction reference must be null")
    return result

def _probability(log_value):
    value = math.exp(log_value)
    if value == 0:
        return {"p_upper": None, "log_p_upper": log_value,
                "representation": "FLOAT_UNDERFLOW_USE_FINITE_LOG_BOUND"}
    return {"p_upper": value, "log_p_upper": log_value, "representation": "FLOAT_AND_LOG"}

def evaluate_decisions(records, *, scenario_ids, readiness, contract_sha256):
    """Reduce verified calibration metadata. Caller authenticates all scientific inputs.

    This function has no I/O, imports no scientific backend, and cannot ratify/release data.
    Missing records are incomplete, never non-rejections. Bayes and sigma are not computed.
    """
    _need(contract_sha256 == CONTRACT_SHA256, "frozen source contract mismatch")
    _need(type(scenario_ids) in (list, tuple) and len(scenario_ids) > 0, "nonempty frozen scenarios required")
    _need(all(type(s) is str and bool(s.strip()) for s in scenario_ids), "scenario id type")
    _need(len(set(scenario_ids)) == len(scenario_ids), "duplicate scenario id")
    keys = {"data_released", "v1_ratified", "integrity_valid", "common_support_valid"}
    _need(type(readiness) is dict and set(readiness) == keys, "readiness keys")
    for name, value in readiness.items():
        _flag(value, name)
    result = {"schema": "F9_LOGICAL_DECISION_RESULT_V1", "source_contract_sha256": CONTRACT_SHA256,
              "scope": "CONDITIONAL_ON_CALLER_VERIFIED_RECORDS_NOT_CERTIFICATE_VERIFICATION",
              "systematics_coverage": "FINITE_FROZEN_FAMILY_PHYSICAL_COVERAGE_LIMITED",
              "scenario_ids": list(scenario_ids), "readiness": dict(readiness),
              "tests": None, "compatibility": None, "comparisons": None,
              "relative_evidence": None, "sigma_equivalent": None,
              "sigma_status": "NOT_COMPUTED_NO_BAYES_OR_SQRT_STATISTIC_CONVERSION",
              "observed_statistic_computed": False, "authorization_granted": False,
              "gate_changed": False, "information_power": None, "use_novelty": None}
    if not readiness["data_released"] or not readiness["v1_ratified"]:
        _need(records is None, "closed/unratified input must not carry observed records")
        result["status"] = "AWAITING_DATA_OR_RATIFICATION"
        return result
    if not readiness["integrity_valid"] or not readiness["common_support_valid"]:
        _need(records is None, "invalid input contract must not carry admitted records")
        result["status"] = "INVALID_INPUT_CONTRACT_NO_PHYSICAL_DECISION"
        return result
    _need(type(records) is dict and set(records).issubset(TESTS), "unknown test id")
    alpha5 = 0.5 * math.erfc(5 / math.sqrt(2))
    log_alpha5 = math.log(alpha5)
    log_m = math.log(len(TESTS))
    result.update(alpha5=alpha5, log_alpha5=log_alpha5, multiplicity=len(TESTS))
    tests = {}
    for test in TESTS:
        supplied = records.get(test, {})
        _need(type(supplied) is dict and set(supplied).issubset(scenario_ids), "unknown scenario id")
        rows = {}
        for sid in scenario_ids:
            raw = supplied.get(sid)
            if raw is None:
                rows[sid] = {"status": "MISSING", "complete": False, "reject_within_scenario": None}
                continue
            record = _record(raw, test)
            complete = (record["statistic_available"] and record["statistic_valid"] and
                        record["calibration_status"] == CALIBRATIONS[0])
            adjusted = min(0.0, log_m + record["log_p_upper"]) if complete else None
            rows[sid] = {"status": "AVAILABLE", "record": record, "complete": complete,
                         "log_p_FWER": adjusted,
                         "reject_within_scenario": adjusted <= log_alpha5 if complete else None}
        complete = all(row["complete"] for row in rows.values())
        missing = [sid for sid, row in rows.items() if not row["complete"]]
        item = {"complete": complete, "incomplete_scenarios": missing, "scenarios": rows,
                "robust_bound": None, "adjusted_bound": None, "reject": None,
                "all_directions_positive_certified": False,
                "status": "CALIBRATION_UNAVAILABLE_OR_PARTIAL"}
        if complete:
            log_robust = max(row["record"]["log_p_upper"] for row in rows.values())
            log_adjusted = min(0.0, log_m + log_robust)
            item.update(robust_bound=_probability(log_robust), adjusted_bound=_probability(log_adjusted),
                        reject=log_adjusted <= log_alpha5, status="COMPLETE_CONDITIONAL_CALIBRATION")
            if test in TESTS[2:]:
                item["all_directions_positive_certified"] = all(
                    row["record"]["direction_positive_certified"] for row in rows.values())
        tests[test] = item
    h1_rejected = any(tests[t]["reject"] is True for t in TESTS[:2])
    h1_not_rejected = all(tests[t]["complete"] and tests[t]["reject"] is False for t in TESTS[:2])
    compat = {"H1_rejected": h1_rejected, "H1_calibrated_not_rejected": h1_not_rejected,
              "missing_tests": [t for t in TESTS[:2] if not tests[t]["complete"]],
              "status": "ROUTE_H1_REJECTED_AT_5SIGMA_CONDITIONAL_CONTRACT" if h1_rejected else
              ("NOT_FALSIFIED_IN_THIS_CONTRACT" if h1_not_rejected else "CALIBRATION_UNAVAILABLE_OR_PARTIAL")}
    comparisons = {}
    for test in TESTS[2:]:
        item = tests[test]
        combined = h1_not_rejected and item["complete"] and item["all_directions_positive_certified"] and item["reject"] is True
        comparisons[test] = {"null_rejected": item["reject"], "combined_discrimination": combined,
            "direction_complete": item["all_directions_positive_certified"],
            "status": "CONDITIONAL_DISCRIMINATION_THRESHOLD_MET" if combined else
                      ("NO_COMBINED_CLAIM" if item["complete"] else "CALIBRATION_UNAVAILABLE_OR_PARTIAL")}
    result.update(tests=tests, compatibility=compat, comparisons=comparisons)
    if h1_rejected:
        result["status"] = compat["status"]
    elif any(v["combined_discrimination"] for v in comparisons.values()):
        result["status"] = "CONDITIONAL_DISCRIMINATION_THRESHOLD_MET"
    elif not all(t["complete"] for t in tests.values()):
        result["status"] = "CALIBRATION_UNAVAILABLE_OR_PARTIAL"
    else:
        mixed = any(len({v["reject_within_scenario"] for v in t["scenarios"].values()}) > 1 for t in tests.values())
        mixed_direction = any(len({row["record"]["statistic"] > 0
                                   for row in tests[t]["scenarios"].values()}) > 1
                              for t in TESTS[2:])
        result["status"] = "SYSTEMATICS_SENSITIVE_RESULT" if mixed or mixed_direction else "NO_COMBINED_DISCRIMINATION_THRESHOLD_MET"
    return result
