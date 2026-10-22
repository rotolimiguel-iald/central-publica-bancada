"""One-use invented-record logic checks; no observations or statistical calibration."""
import copy
import hashlib
import importlib.util
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent

def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def main():
    claim_path = BASE / "CLAIM_LOGIC.json"
    result_path = BASE / "RESULT_LOGIC.json"
    manifest = json.loads((BASE / "MANIFESTO_PREPARACAO.json").read_bytes())
    for entry in manifest["artifacts"]:
        actual = pin(Path(entry["path"]))
        assert all(actual[k] == entry[k] for k in ("bytes", "sha256"))
    approval = json.loads((BASE / "REVISAO_ROOT.json").read_bytes())
    assert approval["accepted"] and approval["logical_checks_authorized_once"]
    assert approval["manifest_sha256"] == pin(BASE / "MANIFESTO_PREPARACAO.json")["sha256"]
    assert not result_path.exists()
    claim = {"at": datetime.now(timezone.utc).isoformat(), "pid": os.getpid(),
             "scope": "INVENTED_METADATA_LOGICAL_CHECKS_NOT_SCIENCE", "retry_allowed": False,
             "review": pin(BASE / "REVISAO_ROOT.json"), "source": pin(BASE / "decision_reducer.py")}
    raw = (json.dumps(claim, sort_keys=True) + "\n").encode()
    fd = os.open(claim_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        raise
    assert claim_path.read_bytes() == raw
    spec = importlib.util.spec_from_file_location("f9_decision_reducer_logic_checked", BASE / "decision_reducer.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sha = module.CONTRACT_SHA256
    ready = {"data_released": True, "v1_ratified": True, "integrity_valid": True, "common_support_valid": True}
    ref = {"id": "INVENTED_LOGICAL_FIXTURE_NOT_CERTIFICATE", "sha256": pin(BASE / "REQUEST.json")["sha256"]}
    checks = []
    def check(name, condition):
        assert condition, name
        checks.append({"name": name, "passed": True})
    def rejected(name, call):
        try:
            call()
        except module.DecisionError:
            check(name, True)
        else:
            check(name, False)
    def row(p=0.5, statistic=1.0, direction=False):
        return {"statistic": statistic, "statistic_available": True, "statistic_valid": True,
                "calibration_status": "VALID_UNIFORM_NULL_OR_CONSERVATIVE_BOUND", "calibration_scope": "INVENTED_FOR_LOGIC_ONLY",
                "log_p_upper": math.log(p), "numerical_certificate": dict(ref), "calibration_reference": dict(ref),
                "direction_positive_certified": direction, "direction_reference": dict(ref) if direction else None}
    def full():
        return {t: {s: row(direction=t in module.TESTS[2:]) for s in ("s1", "s2")} for t in module.TESTS}
    def run(data, state=None, scenarios=("s1", "s2")):
        return module.evaluate_decisions(data, scenario_ids=scenarios, readiness=ready if state is None else state, contract_sha256=sha)
    closed = {**ready, "data_released": False}
    check("closed_has_no_observed_fields", run(None, closed)["tests"] is None)
    rejected("closed_rejects_records", lambda: run({}, closed))
    check("invalid_support_has_no_verdict", run(None, {**ready,"common_support_valid":False})["compatibility"] is None)
    rejected("unknown_scenario", lambda: run({"COMPAT_H1":{"outside":row()}}))
    rejected("duplicate_scenario", lambda: run({}, scenarios=("s1","s1")))
    check("empty_is_not_nonrejection", not run({})["compatibility"]["H1_calibrated_not_rejected"])
    for test in module.TESTS[:2]:
        ans=run({test:{s:row(1e-10) for s in ("s1","s2")}})
        check("valid_rejection_survives_missing_"+test, ans["compatibility"]["H1_rejected"] and len(ans["compatibility"]["missing_tests"])==1)
    d=full();del d["H5_TO_H1"]
    check("two_h1_pass_without_rival", run(d)["compatibility"]["H1_calibrated_not_rejected"])
    del d["COMPAT_H1"]
    check("one_h1_pass_is_not_two", not run(d)["compatibility"]["H1_calibrated_not_rejected"])
    d=full();d["H2_TO_H1"]={s:row(1e-10,direction=True) for s in ("s1","s2")}
    check("combined_requires_all_conditions", run(d)["comparisons"]["H2_TO_H1"]["combined_discrimination"])
    d["H2_TO_H1"]["s2"]=row(0.1,direction=True)
    ans=run(d)
    check("maximum_and_factor_five", abs(ans["tests"]["H2_TO_H1"]["adjusted_bound"]["p_upper"]-0.5)<1e-14 and not ans["comparisons"]["H2_TO_H1"]["combined_discrimination"])
    d["H2_TO_H1"]={s:row(1e-10,direction=False) for s in ("s1","s2")}
    check("positive_uncertified_not_enough", not run(d)["comparisons"]["H2_TO_H1"]["combined_discrimination"])
    d["H2_TO_H1"]={s:row(1e-10,direction=True) for s in ("s1","s2")}
    d["COMPAT_H1"]={s:row(1e-10) for s in ("s1","s2")}
    check("rejected_h1_no_combined_claim", not run(d)["comparisons"]["H2_TO_H1"]["combined_discrimination"])
    d["LAW_H1_VS_FREE"]["s2"].update(calibration_status="PARTIAL",log_p_upper=None)
    check("other_partial_preserves_rejection", run(d)["compatibility"]["H1_rejected"])
    d=full()
    for s in ("s1","s2"):
        d["H2_TO_H1"][s]["log_p_upper"]=-1000.0
    bound=run(d)["tests"]["H2_TO_H1"]["adjusted_bound"]
    check("underflow_not_reported_as_zero_p", bound["p_upper"] is None and math.isfinite(bound["log_p_upper"]))
    bad=copy.deepcopy(d);bad["COMPAT_H1"]["s1"]["log_p_upper"]=0.1
    rejected("positive_log_probability", lambda:run(bad))
    bad=copy.deepcopy(d);bad["COMPAT_H1"]["s1"]["statistic"]=True
    rejected("bool_is_not_statistic", lambda:run(bad))
    bad=copy.deepcopy(d);bad["COMPAT_H1"]["s1"]["calibration_reference"]=None
    rejected("missing_external_reference", lambda:run(bad))
    bad=copy.deepcopy(d);bad["COMPAT_H1"]["s1"].update(statistic=-1.0,statistic_valid=False,calibration_status="INVALID",log_p_upper=None)
    check("invalid_statistic_not_rejection", run(bad)["tests"]["COMPAT_H1"]["reject"] is None)
    bad=copy.deepcopy(d);bad["COMPAT_H1"]["s1"]["log_p_upper"]=float("nan")
    rejected("nan_log_probability", lambda:run(bad))
    d=full();d["H2_TO_H1"]["s2"]=row(statistic=-1.0,direction=False)
    check("mixed_direction_visible", run(d)["status"]=="SYSTEMATICS_SENSITIVE_RESULT")
    d=full();del d["H2_TO_H1"]["s2"]
    check("missing_scenario_no_subset_bound", run(d)["tests"]["H2_TO_H1"]["robust_bound"] is None)
    rejected("unknown_test", lambda:run({"not_a_test":{}}))
    assert len(checks)==24
    result={"at":datetime.now(timezone.utc).isoformat(),"status":"PASS_LOGICAL_CHECKS_ONCE", "checks":checks,
            "science_calls":0,"observed_reads":0,"statistical_calibration":False,"retry_allowed":False,
            "claim":pin(claim_path),"source":pin(BASE/"decision_reducer.py"),"test_driver":pin(Path(__file__).resolve()),
            "limitations":"Invented logical records with explicit dummy references; no certificate verification, physical data, calibration, power, or scientific verdict."}
    output=(json.dumps(result,ensure_ascii=False,sort_keys=True,allow_nan=False)+"\n").encode()
    temporary=result_path.with_name(result_path.name+".tmp_"+str(os.getpid()))
    temporary.write_bytes(output)
    assert temporary.read_bytes()==output and not result_path.exists()
    os.replace(temporary,result_path)
    assert result_path.read_bytes()==output
    print(json.dumps({"result":pin(result_path),"checks":len(checks),"science_calls":0,"observed_reads":0}))

if __name__=="__main__":
    main()
