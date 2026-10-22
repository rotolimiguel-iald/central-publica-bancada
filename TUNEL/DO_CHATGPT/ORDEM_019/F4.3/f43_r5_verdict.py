"""F4.3 R5 secondary diagnostic. No observational data are read."""
from __future__ import annotations
import json
import math
import re
import sys
from typing import Any

ALPHA = 2.8665e-7
MIN_EVENTS = 10
MIN_RECOVERY_LOWER95 = 0.90
ORDER = (
    "AWAITING_POWER",
    "DIAGNOSTIC_UNDERPOWERED_OR_NONIDENTIFIABLE",
    "DIAGNOSTIC_INCONCLUSIVE_SYSTEMATICS",
    "DIAGNOSTIC_BOTH_MODELS_REJECTED",
    "DIAGNOSTIC_CONFLICTS_V1",
    "DIAGNOSTIC_CORROBORATES_V1_SAME_DIRECTION",
    "DIAGNOSTIC_ONLY__NEITHER_REJECTED",
    "DIAGNOSTIC_ONLY__NO_V1_DIRECTION",
)
V1_FIXED = {
    "AWAITING_DATA", "AWAITING_DATA__INSUFFICIENT_SAMPLE",
    "INCONCLUSIVE_SYSTEMATICS", "NOT_FALSIFIED_UNDERPOWERED",
    "FALSIFIED_AT_5SIGMA", "NOT_FALSIFIED_POWERED",
    "NOT_FALSIFIED_POWERED__GR_TENSION_REPORTED",
}
V1_POWER = re.compile(r"NOT_FALSIFIED_UNDERPOWERED__POWER_(\d+(?:\.\d+)?)_OF_5_SIGMA\Z")
REQUIRED = (
    "manifest_complete", "exact_power_run", "recovery_lower_95",
    "identifiable_440", "systematics_ok", "rcond_stable", "n_events",
    "p_reject_B", "p_reject_GR", "v1_official_token",
)

def probability(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    value = float(value)
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError(f"{name} must be finite in [0,1]")
    return value

def v1_rejected_null(token: str) -> str | None:
    if token == "FALSIFIED_AT_5SIGMA":
        return "B"
    if token == "NOT_FALSIFIED_POWERED__GR_TENSION_REPORTED":
        return "GR"
    return None

def decide(x: dict[str, Any]) -> dict[str, Any]:
    """First matching row wins. Invalid/missing fields fail visibly."""
    missing = [k for k in REQUIRED if k not in x]
    if missing:
        raise ValueError(f"missing decision inputs: {missing}")
    for k in ("manifest_complete", "exact_power_run", "identifiable_440",
              "systematics_ok", "rcond_stable"):
        if type(x[k]) is not bool:
            raise ValueError(f"{k} must be bool")
    if type(x["n_events"]) is not int or x["n_events"] < 0:
        raise ValueError("n_events must be nonnegative int")
    v1 = x["v1_official_token"]
    if not isinstance(v1, str):
        raise ValueError("v1_official_token must be str")
    m = V1_POWER.fullmatch(v1)
    if v1 not in V1_FIXED and not (m and float(m.group(1)) < 5):
        raise ValueError("unrecognized V1 token or suffix")
    recovery = probability(x["recovery_lower_95"], "recovery_lower_95")
    pb = probability(x["p_reject_B"], "p_reject_B")
    pg = probability(x["p_reject_GR"], "p_reject_GR")
    rejected = {name for name,p in (("B",pb),("GR",pg)) if p <= ALPHA}
    d1 = v1_rejected_null(v1)
    matches = []
    if not x["manifest_complete"] or not x["exact_power_run"]:
        matches.append(ORDER[0])
    if x["n_events"] < MIN_EVENTS or recovery < MIN_RECOVERY_LOWER95 or not x["identifiable_440"]:
        matches.append(ORDER[1])
    if not x["systematics_ok"] or not x["rcond_stable"]:
        matches.append(ORDER[2])
    if rejected == {"B","GR"}:
        matches.append(ORDER[3])
    if len(rejected) == 1 and d1 is not None and d1 not in rejected:
        matches.append(ORDER[4])
    if len(rejected) == 1 and d1 is not None and d1 in rejected:
        matches.append(ORDER[5])
    if not rejected:
        matches.append(ORDER[6])
    if len(rejected) == 1 and d1 is None:
        matches.append(ORDER[7])
    token = next((t for t in ORDER if t in matches), None)
    if token is None:
        raise RuntimeError("no diagnostic row matched")
    joint = "NO_JOINT_VERDICT"
    if token in (ORDER[2], ORDER[3], ORDER[4]):
        joint = "INCONCLUSIVE_SYSTEMATICS"
    if token == ORDER[5]:
        joint = "CORROBORATES_V1_SAME_NAMED_NULL_ONLY"
    return {
        "v1_official_token_public_unchanged": v1,
        "diagnostic_token_local": token,
        "joint_reading_descriptive": joint,
        "review_required": token == ORDER[4] or
            (token == ORDER[7] and v1 == "NOT_FALSIFIED_POWERED"),
        "matched_rows": matches,
        "rejected_nulls": sorted(rejected),
        "opposite_threshold": ALPHA,
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python f43_r5_verdict.py INPUT.json")
    with open(sys.argv[1], encoding="utf-8") as stream:
        payload = json.load(stream)
    print(json.dumps(decide(payload), ensure_ascii=False, indent=2))