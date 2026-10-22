"""Synthetic-only checks of the R5 decision function and documentary pins."""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path
from f43_r5_verdict import ALPHA, ORDER, decide

ROOT = Path(__file__).resolve().parent
SPEC = ROOT / "PREREGISTRO_F4_3_V4_R5_20261008.json"
def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
spec = json.loads(SPEC.read_text(encoding="utf-8"))
fields = spec["fields_13"]
assert len(fields) == 13 and all(v is not None for v in fields.values())
for item in spec["artifacts"].values():
    path = Path(item["path"])
    assert path.stat().st_size == item["bytes"] and sha(path) == item["sha256"]
assert fields["event_list_hash"] == spec["artifacts"]["events"]["sha256"]
assert fields["waveform_hash"] == spec["artifacts"]["waveform_contract"]["sha256"]
assert fields["prior_hash"] == spec["artifacts"]["priors"]["sha256"]
assert fields["psd_hashes"]["map"] == spec["artifacts"]["psd"]["sha256"]
assert fields["window_hashes"]["all_events"] == spec["artifacts"]["windows"]["sha256"]
assert spec["sources"]["R4_inventory_generator"]["sha256"] == sha(ROOT / "f43_r4_inventory.py")
v1s = [
    "AWAITING_DATA", "AWAITING_DATA__INSUFFICIENT_SAMPLE",
    "INCONCLUSIVE_SYSTEMATICS",
    "NOT_FALSIFIED_UNDERPOWERED__POWER_3_OF_5_SIGMA",
    "FALSIFIED_AT_5SIGMA", "NOT_FALSIFIED_POWERED",
    "NOT_FALSIFIED_POWERED__GR_TENSION_REPORTED",
]
ps = {"none":(0.5,0.5), "B":(1e-8,0.5), "GR":(0.5,1e-8),
      "both":(1e-8,1e-8), "weak":(1e-3,0.5)}
base = dict(manifest_complete=True, exact_power_run=True, recovery_lower_95=0.95,
            identifiable_440=True, systematics_ok=True, rcond_stable=True,
            n_events=10, p_reject_B=0.5, p_reject_GR=0.5,
            v1_official_token="NOT_FALSIFIED_POWERED")
def check(expected, **changes):
    x = {**base, **changes}
    out = decide(x)
    assert out["diagnostic_token_local"] == expected, (x,out)
    assert out["v1_official_token_public_unchanged"] == x["v1_official_token"]
    return out
named = {
    "today": check("AWAITING_POWER", manifest_complete=False, exact_power_run=False),
    "opposite_at_alpha": check("DIAGNOSTIC_CONFLICTS_V1",
        v1_official_token="FALSIFIED_AT_5SIGMA", p_reject_GR=ALPHA),
    "opposite_above_alpha": check("DIAGNOSTIC_ONLY__NEITHER_REJECTED",
        v1_official_token="FALSIFIED_AT_5SIGMA", p_reject_GR=ALPHA*1.000001),
    "same_B": check("DIAGNOSTIC_CORROBORATES_V1_SAME_DIRECTION",
        v1_official_token="FALSIFIED_AT_5SIGMA", p_reject_B=1e-8),
    "both": check("DIAGNOSTIC_BOTH_MODELS_REJECTED", p_reject_B=1e-8,p_reject_GR=1e-8),
    "no_direction_review": check("DIAGNOSTIC_ONLY__NO_V1_DIRECTION",
        p_reject_B=1e-8),
    "underpowered_first": check("DIAGNOSTIC_UNDERPOWERED_OR_NONIDENTIFIABLE",
        recovery_lower_95=0.89,systematics_ok=False,p_reject_B=1e-8),
    "insufficient": check("DIAGNOSTIC_UNDERPOWERED_OR_NONIDENTIFIABLE",
        n_events=9,v1_official_token="AWAITING_DATA__INSUFFICIENT_SAMPLE"),
    "power_suffix": check("DIAGNOSTIC_ONLY__NEITHER_REJECTED",
        v1_official_token="NOT_FALSIFIED_UNDERPOWERED__POWER_4.9_OF_5_SIGMA"),
}
assert named["no_direction_review"]["review_required"]
assert named["underpowered_first"]["matched_rows"][0] == ORDER[1]
invalid = [
    {**base, "p_reject_B": float("nan")},
    {**base, "v1_official_token": "NOT_FALSIFIED_UNDERPOWERED__POWER_5_OF_5_SIGMA"},
    {k:v for k,v in base.items() if k != "p_reject_GR"},
]
for x in invalid:
    try:
        decide(x)
    except ValueError:
        continue
    raise AssertionError("malformed input accepted")
count = 0
overlap = 0
tokens = set()
for mc,er,rec,idf,sys,rc,p_case,v1 in itertools.product(
    (False,True),(False,True),(0.1,0.95),(False,True),
    (False,True),(False,True),ps,v1s):
    pb,pg = ps[p_case]
    x = dict(manifest_complete=mc,exact_power_run=er,recovery_lower_95=rec,
             identifiable_440=idf,systematics_ok=sys,rcond_stable=rc,
             n_events=10,p_reject_B=pb,p_reject_GR=pg,v1_official_token=v1)
    out = decide(x)
    assert out["diagnostic_token_local"] in ORDER
    assert out["v1_official_token_public_unchanged"] == v1
    count += 1
    overlap += len(out["matched_rows"]) > 1
    tokens.add(out["diagnostic_token_local"])
assert count == 2240 and tokens == set(ORDER)
receipt = {
    "status": "REAL_SYNTHETIC_ONLY", "cases": count, "overlap_cases": overlap,
    "all_eight_local_tokens_reached": sorted(tokens),
    "named_cases": {k:v["diagnostic_token_local"] for k,v in named.items()},
    "invalid_refusals": len(invalid), "spec_sha256": sha(SPEC),
    "verdict_sha256": sha(ROOT/"f43_r5_verdict.py"),
    "no_observational_data": True,
}
path = ROOT / "F43_R5_SYNTHETIC_SELFTEST_20261008.json"
with path.open("x",encoding="utf-8") as stream:
    json.dump(receipt,stream,ensure_ascii=False,indent=2)
    stream.write("\n")
print(json.dumps(receipt,ensure_ascii=False))