"""Synthetic-only gate tests. No fake audit is presented as real evidence."""
import copy
import hashlib
import json
from pathlib import Path
from f43_r5_1_calibrated_gate import ALPHA, FWER_RULE, decide_from_contract
root=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
spec=json.loads((root/"PREREGISTRO_F4_3_V4_R5_20261008.json").read_text(encoding="utf-8"))
result_sha="a"*64
data={
 "waveform_executable":{"status":"EXECUTABLE_FULL_IMR_COMMON_SOURCE","sha256":"b"*64},
 "power":{"status":"EXACT_INJECTION_POWER_MEASURED","recovery_lower_95":0.95,
          "identifiable_440":True,"n_events":10,"result_sha256":result_sha},
 "systematics":{"source_power_sha256":result_sha,
                "checks":{k:"PASS" for k in ("PSD","family","start_time","coverage","bias","rcond")}},
 "tail_B":{"named_null":"B","tail":"one_sided","alpha_one_sided":ALPHA,
           "calibration":"PASS","null_coverage":"PASS",
           "power_result_sha256":result_sha,"p":0.5},
 "tail_GR":{"named_null":"GR","tail":"one_sided","alpha_one_sided":ALPHA,
            "calibration":"PASS","null_coverage":"PASS",
            "power_result_sha256":result_sha,"p":0.5},
 "v1_official":{"official_token":"FALSIFIED_AT_5SIGMA",
                "spec_sha256":spec["sources"]["V1"]["sha256"],
                "named_null":"B","tail":"one_sided","calibration":"PASS","p":ALPHA},
}
packet={
 "mode":"SYNTHETIC_TEST_ONLY","synthetic_receipts":data,
 "f43_spec_sha256":sha(root/"PREREGISTRO_F4_3_V4_R5_20261008.json"),
 "v1_spec_sha256":spec["sources"]["V1"]["sha256"],
 "fwer_rule":FWER_RULE,"alpha_one_sided":ALPHA,
 "event_list_hash":spec["fields_13"]["event_list_hash"],
 "psd_map_hash":spec["fields_13"]["psd_hashes"]["map"],
}
def reject(p,synthetic=True):
    try: decide_from_contract(p,synthetic_test=synthetic)
    except ValueError: return
    raise AssertionError("malformed contract accepted")
reject(packet,False)
reject({**packet,"mode":"C1_AUDITED_PRODUCTION"},True)
baseline=decide_from_contract(packet,synthetic_test=True)
assert baseline["scope"]=="SYNTHETIC_ONLY_NOT_EVIDENCE"
assert baseline["diagnostic_token_local"]=="DIAGNOSTIC_ONLY__NEITHER_REJECTED"
assert not baseline["official_opening_or_gate_authorized"]
tests=0
for mutate in (
 lambda x: x["synthetic_receipts"]["tail_B"].update(tail="two_sided"),
 lambda x: x["synthetic_receipts"]["tail_B"].update(calibration="OPEN"),
 lambda x: x["synthetic_receipts"]["tail_GR"].update(null_coverage="FAIL"),
 lambda x: x["synthetic_receipts"]["tail_GR"].update(named_null="B"),
 lambda x: x["synthetic_receipts"]["tail_B"].update(power_result_sha256="c"*64),
 lambda x: x["synthetic_receipts"]["v1_official"].update(p=ALPHA*2),
 lambda x: x["synthetic_receipts"]["waveform_executable"].update(sha256=spec["fields_13"]["waveform_hash"]),
 lambda x: x.update(fwer_rule="TWO_TAILS_SUMMED"),
 lambda x: x.update(psd_map_hash="0"*64),
):
    bad=copy.deepcopy(packet)
    mutate(bad)
    reject(bad)
    tests+=1
opposite=copy.deepcopy(packet)
opposite["synthetic_receipts"]["tail_GR"]["p"]=ALPHA
out=decide_from_contract(opposite,synthetic_test=True)
assert out["diagnostic_token_local"]=="DIAGNOSTIC_CONFLICTS_V1"
assert out["joint_reading_descriptive"]=="INCONCLUSIVE_SYSTEMATICS"
above=copy.deepcopy(opposite)
above["synthetic_receipts"]["tail_GR"]["p"]=ALPHA*1.000001
assert decide_from_contract(above,synthetic_test=True)["diagnostic_token_local"]=="DIAGNOSTIC_ONLY__NEITHER_REJECTED"
same=copy.deepcopy(packet)
same["synthetic_receipts"]["tail_B"]["p"]=ALPHA
assert decide_from_contract(same,synthetic_test=True)["diagnostic_token_local"]=="DIAGNOSTIC_CORROBORATES_V1_SAME_DIRECTION"
bad_systematics=copy.deepcopy(same)
bad_systematics["synthetic_receipts"]["systematics"]["checks"]["PSD"]="FAIL"
assert decide_from_contract(bad_systematics,synthetic_test=True)["diagnostic_token_local"]=="DIAGNOSTIC_INCONCLUSIVE_SYSTEMATICS"
receipt={
 "status":"REAL_TEST_EXECUTION__SYNTHETIC_ONLY",
 "production_mode_refused_without_pinned_receipts":True,
 "malformed_contracts_refused":tests,
 "boundary_cases":["p_equals_alpha_opposite","p_above_alpha_no_rejection",
                   "same_null_intersection","PSD_failure_inconclusive"],
 "wrapper_sha256":sha(root/"f43_r5_1_calibrated_gate.py"),
 "r5_function_sha256":sha(root/"f43_r5_verdict.py"),
 "no_observational_data":True,"no_gate_change":True,
}
with (root/"F43_R5_1_SYNTHETIC_SELFTEST_20261008.json").open("x",encoding="utf-8") as f:
    json.dump(receipt,f,ensure_ascii=False,indent=2)
    f.write("\n")
print(json.dumps(receipt,ensure_ascii=False))