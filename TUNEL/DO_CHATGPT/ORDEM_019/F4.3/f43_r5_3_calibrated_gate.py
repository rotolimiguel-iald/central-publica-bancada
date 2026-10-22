"""Fail-closed calibration boundary for the additive F4.3 R5.3 verdict.

A numeric p or a Boolean systematics_ok is not evidence of calibration.
Production requires pinned receipts for both named nulls, exact power,
systematics, the V1 verdict, an executable waveform and a c1 audit.
Synthetic mode is visibly non-evidentiary. No observational data are read.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
R5_RESULT = ROOT / "RESULTADO_F43_R5_20261008.json"
R5_RESULT_SHA = "a6f407706ee6dedf39fbc1854dc8199fe5539855873a7298515e4750d535a210"
R5_1_GATE_SHA = "941fb4f16059115a7c4f098c7a85dbe5c97debc2adf3f8693ca02fb6e0f2c8f9"
R5_2_RESULT_SHA = "45260f1166f5b658ac11739c069ae18454523cb7e8b379058084e6dfa1d69205"
R5_2_GATE_SHA = "e61f5d19eb8c855d0cdf9d7972f454f2dac4261036ff462d08afe004f21b6899"
R5_3_VERDICT_SHA = "736c3a39677a21c302b3af80b7d1c44658d791759d053c4d8671acc5d765c17d"
AUDIT_ROOT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F4.3")
ALPHA = 2.8665e-7
CHECKS = ("PSD", "family", "start_time", "coverage", "bias")
FWER_RULE = "INTERSECTION_OF_V1_AND_F43_SAME_NAMED_NULL"
RECEIPTS = ("power", "systematics", "tail_B", "tail_GR",
            "v1_official", "waveform_executable", "c1_audit")

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def _pinned_r5() -> tuple[dict, Any]:
    if sha(R5_RESULT) != R5_RESULT_SHA:
        raise ValueError("R5 result bytes changed")
    if sha(ROOT / "f43_r5_1_calibrated_gate.py") != R5_1_GATE_SHA:
        raise ValueError("R5.1 gate bytes changed")
    if sha(ROOT / "RESULTADO_F43_R5_2_20261008.json") != R5_2_RESULT_SHA:
        raise ValueError("R5.2 result bytes changed")
    if sha(ROOT / "f43_r5_2_calibrated_gate.py") != R5_2_GATE_SHA:
        raise ValueError("R5.2 gate bytes changed")
    if sha(ROOT / "f43_r5_3_verdict.py") != R5_3_VERDICT_SHA:
        raise ValueError("R5.3 verdict bytes changed")
    result = json.loads(R5_RESULT.read_text(encoding="utf-8"))
    pins = {Path(x["path"]).name:x for x in result["artifacts"]}
    for name in ("PREREGISTRO_F4_3_V4_R5_20261008.json",
                 "f43_r5_verdict.py"):
        p = ROOT / name
        if sha(p) != pins[name]["sha256"]:
            raise ValueError(f"R5 dependency changed: {name}")
    spec = json.loads((ROOT/"PREREGISTRO_F4_3_V4_R5_20261008.json").read_text(encoding="utf-8"))
    module_path = ROOT/"f43_r5_3_verdict.py"
    m_spec = importlib.util.spec_from_file_location("f43_r5_3_verdict",module_path)
    module = importlib.util.module_from_spec(m_spec)
    assert m_spec.loader is not None
    m_spec.loader.exec_module(module)
    return spec,module

def _receipt(ref: dict) -> Any:
    if not isinstance(ref,dict) or set(ref)!={"path","sha256"}:
        raise ValueError("receipt reference requires exact path and sha256")
    p=Path(ref["path"]).resolve()
    if not (p.is_relative_to(ROOT.resolve()) or p.is_relative_to(AUDIT_ROOT.resolve())):
        raise ValueError("receipt path outside F4.3 custody")
    expected=ref["sha256"]
    if not isinstance(expected,str) or len(expected)!=64:
        raise ValueError("receipt sha256 malformed")
    if sha(p)!=expected.lower():
        raise ValueError(f"receipt hash mismatch: {p}")
    if p.suffix.lower()==".json":
        return json.loads(p.read_text(encoding="utf-8"))
    return {"verified_sha256":expected.lower(),"path":str(p)}

def _finite_p(value: Any) -> float:
    if isinstance(value,bool) or not isinstance(value,(int,float)):
        raise ValueError("p must be numeric")
    value=float(value)
    if not math.isfinite(value) or not 0<=value<=1:
        raise ValueError("p outside [0,1]")
    return value

def decide_from_contract(packet: dict, *, synthetic_test: bool=False) -> dict:
    """Derive all raw R5 inputs from typed receipts; never trust caller booleans."""
    spec,base=_pinned_r5()
    mode=packet.get("mode")
    if mode=="SYNTHETIC_TEST_ONLY":
        if not synthetic_test:
            raise ValueError("synthetic receipt cannot enter production")
        data=packet.get("synthetic_receipts")
        if not isinstance(data,dict):
            raise ValueError("missing synthetic receipts")
        scope="SYNTHETIC_ONLY_NOT_EVIDENCE"
    elif mode=="C1_AUDITED_PRODUCTION":
        if synthetic_test:
            raise ValueError("production packet cannot be run in synthetic mode")
        refs=packet.get("receipts")
        if not isinstance(refs,dict) or any(k not in refs for k in RECEIPTS):
            raise ValueError("all seven pinned production receipts required")
        data={k:_receipt(refs[k]) for k in RECEIPTS}
        if packet.get("c1_audit_event_id",0)<=0:
            raise ValueError("c1 audit event required")
        scope="CONTRACT_VALIDATED__C1_STILL_REVIEWS_SCIENTIFIC_MERIT"
    else:
        raise ValueError("unknown or missing mode")
    if packet.get("f43_spec_sha256")!=sha(ROOT/"PREREGISTRO_F4_3_V4_R5_20261008.json"):
        raise ValueError("F4.3 spec pin mismatch")
    if packet.get("v1_spec_sha256")!=spec["sources"]["V1"]["sha256"]:
        raise ValueError("V1 spec pin mismatch")
    if packet.get("fwer_rule")!=FWER_RULE or packet.get("alpha_one_sided")!=ALPHA:
        raise ValueError("FWER/one-sided alpha mismatch")
    if packet.get("event_list_hash")!=spec["fields_13"]["event_list_hash"]:
        raise ValueError("event cohort mismatch")
    if packet.get("psd_map_hash")!=spec["fields_13"]["psd_hashes"]["map"]:
        raise ValueError("PSD design mismatch")
    if not isinstance(data.get("waveform_executable"),dict):
        raise ValueError("executable waveform receipt required")
    wf=data["waveform_executable"]
    if wf.get("status")!="EXECUTABLE_FULL_IMR_COMMON_SOURCE":
        raise ValueError("full IMR common-source implementation absent")
    if wf.get("sha256")==spec["fields_13"]["waveform_hash"]:
        raise ValueError("contract hash is not executable waveform hash")
    power=data["power"]
    if power.get("status")!="EXACT_INJECTION_POWER_MEASURED":
        raise ValueError("exact injection power absent")
    recovery=power.get("recovery_lower_95")
    identifiable=power.get("identifiable_440")
    n_events=power.get("n_events")
    if type(identifiable) is not bool or type(n_events) is not int:
        raise ValueError("power fields malformed")
    systematics=data["systematics"]
    checks=systematics.get("checks")
    if not isinstance(checks,dict) or any(checks.get(k) not in ("PASS","FAIL") for k in CHECKS+("rcond",)):
        raise ValueError("systematics controls missing or malformed")
    if systematics.get("source_power_sha256")!=power.get("result_sha256"):
        raise ValueError("systematics/power linkage mismatch")
    pvals={}
    for name in ("B","GR"):
        tail=data["tail_"+name]
        if tail.get("named_null")!=name or tail.get("tail")!="one_sided":
            raise ValueError(f"{name} null/tail mismatch")
        if tail.get("alpha_one_sided")!=ALPHA or tail.get("calibration")!="PASS" or tail.get("null_coverage")!="PASS":
            raise ValueError(f"{name} calibration/coverage not passed")
        if tail.get("power_result_sha256")!=power.get("result_sha256"):
            raise ValueError(f"{name} tail not linked to power")
        pvals[name]=_finite_p(tail.get("p"))
    v1=data["v1_official"]
    token=v1.get("official_token")
    if not isinstance(token,str):
        raise ValueError("V1 token absent")
    if v1.get("spec_sha256")!=spec["sources"]["V1"]["sha256"]:
        raise ValueError("V1 official receipt linked to wrong spec")
    rejected=base.v1_rejected_null(token)
    if rejected:
        if v1.get("named_null")!=rejected or v1.get("tail")!="one_sided" or v1.get("calibration")!="PASS":
            raise ValueError("V1 directional tail uncertified")
        if _finite_p(v1.get("p"))>ALPHA:
            raise ValueError("V1 directional tail above alpha")
    raw={
        "manifest_complete":True,"exact_power_run":True,
        "recovery_lower_95":recovery,"identifiable_440":identifiable,
        "systematics_ok":all(checks[k]=="PASS" for k in CHECKS),
        "rcond_stable":checks["rcond"]=="PASS",
        "n_events":n_events,"p_reject_B":pvals["B"],
        "p_reject_GR":pvals["GR"],"v1_official_token":token,
    }
    out=base.decide(raw)
    out["scope"]=scope
    out["fwer_rule"]=FWER_RULE
    out["p_values_are_receipt_bound"]=True
    out["systematics_are_receipt_bound"]=True
    out["official_opening_or_gate_authorized"]=False
    return out