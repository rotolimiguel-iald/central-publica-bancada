"""Synthetic regression for the F4.3 R5.2 interface; no observational data."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
from f43_r5_2_verdict import decide
from f43_r5_2_calibrated_gate import ALPHA, FWER_RULE, decide_from_contract

ROOT = Path(__file__).resolve().parent
def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

spec = json.loads((ROOT / "PREREGISTRO_F4_3_V4_R5_20261008.json").read_text(encoding="utf-8"))
raw = {
    "manifest_complete": True, "exact_power_run": True,
    "recovery_lower_95": 0.95, "identifiable_440": True,
    "systematics_ok": True, "rcond_stable": True, "n_events": 10,
    "p_reject_B": 0.5, "p_reject_GR": 0.5,
    "v1_official_token": "NOT_FALSIFIED_UNDERPOWERED__POWER_0P2_OF_5_SIGMA",
}
checks = []
def require_reject(label: str, fn) -> None:
    try:
        fn()
    except ValueError:
        checks.append(label)
        return
    raise AssertionError(f"accepted invalid token or contract: {label}")

for token in ("NOT_FALSIFIED_UNDERPOWERED__POWER_0P2_OF_5_SIGMA",
              "NOT_FALSIFIED_UNDERPOWERED__POWER_4.9_OF_5_SIGMA"):
    out = decide({**raw, "v1_official_token": token})
    assert out["v1_official_token_public_unchanged"] == token
    checks.append("accepted_" + token)
for label, token in (
    ("bare_underpowered", "NOT_FALSIFIED_UNDERPOWERED"),
    ("power_equal_5", "NOT_FALSIFIED_UNDERPOWERED__POWER_5P0_OF_5_SIGMA"),
    ("power_over_5", "NOT_FALSIFIED_UNDERPOWERED__POWER_5.1_OF_5_SIGMA"),
    ("complete_prefix", "TGL_RINGDOWN_NOT_FALSIFIED_UNDERPOWERED__POWER_0P2_OF_5_SIGMA"),
    ("composed_token", "NOT_FALSIFIED_UNDERPOWERED__POWER_0P2_OF_5_SIGMA__DIAGNOSTIC_ONLY__NEITHER_REJECTED"),
):
    require_reject(label, lambda token=token: decide({**raw, "v1_official_token": token}))
for n in (0, 9):
    out = decide({**raw, "n_events": n})
    assert out["diagnostic_token_local"] == "DIAGNOSTIC_UNDERPOWERED_OR_NONIDENTIFIABLE__INSUFFICIENT_SAMPLE"
    checks.append(f"n_{n}_suffix")
out = decide({**raw, "n_events": 9, "exact_power_run": False})
assert out["diagnostic_token_local"] == "AWAITING_POWER__INSUFFICIENT_SAMPLE"
checks.append("n_9_awaiting_suffix")
assert decide(raw)["diagnostic_token_local"] == "DIAGNOSTIC_ONLY__NEITHER_REJECTED"
checks.append("n_10_no_suffix")

power_sha = "a" * 64
receipts = {
    "waveform_executable": {"status": "EXECUTABLE_FULL_IMR_COMMON_SOURCE", "sha256": "b" * 64},
    "power": {"status": "EXACT_INJECTION_POWER_MEASURED", "recovery_lower_95": 0.95,
              "identifiable_440": True, "n_events": 10, "result_sha256": power_sha},
    "systematics": {"source_power_sha256": power_sha,
                    "checks": {k: "PASS" for k in ("PSD", "family", "start_time", "coverage", "bias", "rcond")}},
    "tail_B": {"named_null": "B", "tail": "one_sided", "alpha_one_sided": ALPHA,
               "calibration": "PASS", "null_coverage": "PASS", "power_result_sha256": power_sha, "p": 0.5},
    "tail_GR": {"named_null": "GR", "tail": "one_sided", "alpha_one_sided": ALPHA,
                "calibration": "PASS", "null_coverage": "PASS", "power_result_sha256": power_sha, "p": 0.5},
    "v1_official": {"official_token": raw["v1_official_token"],
                    "spec_sha256": spec["sources"]["V1"]["sha256"]},
}
packet = {
    "mode": "SYNTHETIC_TEST_ONLY", "synthetic_receipts": receipts,
    "f43_spec_sha256": sha(ROOT / "PREREGISTRO_F4_3_V4_R5_20261008.json"),
    "v1_spec_sha256": spec["sources"]["V1"]["sha256"],
    "fwer_rule": FWER_RULE, "alpha_one_sided": ALPHA,
    "event_list_hash": spec["fields_13"]["event_list_hash"],
    "psd_map_hash": spec["fields_13"]["psd_hashes"]["map"],
}
require_reject("synthetic_not_production", lambda: decide_from_contract(packet))
out = decide_from_contract(packet, synthetic_test=True)
assert out["v1_official_token_public_unchanged"] == raw["v1_official_token"]
assert out["scope"] == "SYNTHETIC_ONLY_NOT_EVIDENCE"
assert not out["official_opening_or_gate_authorized"]
checks.append("synthetic_packet_house_power")
bare = copy.deepcopy(packet)
bare["synthetic_receipts"]["v1_official"]["official_token"] = "NOT_FALSIFIED_UNDERPOWERED"
require_reject("synthetic_bare_underpowered", lambda: decide_from_contract(bare, synthetic_test=True))
small = copy.deepcopy(packet)
small["synthetic_receipts"]["power"]["n_events"] = 9
out = decide_from_contract(small, synthetic_test=True)
assert out["diagnostic_token_local"].endswith("__INSUFFICIENT_SAMPLE")
checks.append("synthetic_packet_small_sample")
missing = copy.deepcopy(packet)
missing["mode"] = "C1_AUDITED_PRODUCTION"
missing.pop("synthetic_receipts")
require_reject("production_requires_receipts", lambda: decide_from_contract(missing))
receipt = {
    "unit": "F4.3", "layer": "R5.2", "status": "SYNTHETIC_ONLY_NOT_EVIDENCE",
    "checks": checks, "n_checks": len(checks),
    "r5_2_verdict_sha256": sha(ROOT / "f43_r5_2_verdict.py"),
    "r5_2_gate_sha256": sha(ROOT / "f43_r5_2_calibrated_gate.py"),
    "v1_spec_sha256": spec["sources"]["V1"]["sha256"],
    "no_observational_data": True, "exact_injections_run": False, "gate_moved": False,
}
target = ROOT / "F43_R5_2_SYNTHETIC_SELFTEST_20261008.json"
with target.open("x", encoding="utf-8") as stream:
    json.dump(receipt, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
print(json.dumps({"n_checks": len(checks), "receipt": str(target)}, ensure_ascii=False))