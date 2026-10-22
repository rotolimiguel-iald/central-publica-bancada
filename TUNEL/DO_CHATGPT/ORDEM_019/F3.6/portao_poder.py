"""Pure C16 pre-data power gate. No data or cosmology worker is imported."""

import json
import math
import sys

ALPHA_FINE_CODATA_2018 = 0.0072973525693


def beta_tgl() -> float:
    return ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)


def classify_power(sigma_beta: float | None) -> str:
    """A pass awaits a separate operator decision; it never opens data."""
    if sigma_beta is None or not isinstance(sigma_beta, (int, float)):
        return "NO_ASIMOV_MEASUREMENT"
    if not math.isfinite(sigma_beta) or sigma_beta <= 0:
        return "INVALID_FISHER_RESULT"
    if sigma_beta >= beta_tgl():
        return "UNDERPOWERED_DO_NOT_OPEN_DATA"
    return "POWER_GATE_PASSED_PENDING_SEPARATE_OPERATOR_DATA_DECISION"


def selftest() -> dict:
    beta = beta_tgl()
    cases = [
        (None, "NO_ASIMOV_MEASUREMENT"),
        (float("nan"), "INVALID_FISHER_RESULT"),
        (0.0, "INVALID_FISHER_RESULT"),
        (beta / 2.0, "POWER_GATE_PASSED_PENDING_SEPARATE_OPERATOR_DATA_DECISION"),
        (beta, "UNDERPOWERED_DO_NOT_OPEN_DATA"),
        (beta * 2.0, "UNDERPOWERED_DO_NOT_OPEN_DATA"),
    ]
    results = [
        {"sigma_input": None if value is None or not math.isfinite(value) else value,
         "observed": classify_power(value), "expected": expected,
         "passed": classify_power(value) == expected}
        for value, expected in cases
    ]
    return {"beta_runtime": beta, "cases": results,
            "all_passed": all(item["passed"] for item in results),
            "physical_asimov_run": False, "observational_data_opened": False}


if __name__ == "__main__":
    if sys.argv[1:] != ["--selftest"]:
        raise SystemExit("Only --selftest is available until the CPL model is fixed")
    result = selftest()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["all_passed"] else 1)
