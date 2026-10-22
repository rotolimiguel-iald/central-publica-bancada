"""Persist the audited disposition of the two September 28 opportunities."""

import hashlib
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
JOBS = {
    "kimi": "0898f7cb-bd8e-4d67-96e9-e44e03a19762",
    "mimo": "a8442454-7fbe-4bed-b8ad-c9b65d88f2b0",
}


def bridge_get(job_id):
    process = subprocess.run(
        [r"C:\Python314\python.exe", "-X", "utf8", str(BASE / "bridge.py")],
        input=json.dumps({"operation": "get", "job_id": job_id}),
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    return json.loads(process.stdout)


def atomic_write(path, data, existing=False):
    if existing:
        original = path.read_bytes()
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        backup = path.with_name(path.name + ".bak_" + stamp)
        with backup.open("xb") as handle:
            handle.write(original)
            handle.flush()
            os.fsync(handle.fileno())
        assert backup.read_bytes() == original
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".tmp_", delete=False) as handle:
        temp = Path(handle.name)
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    assert temp.stat().st_size == len(data)
    os.replace(temp, path)
    assert path.read_bytes() == data


def main():
    kimi = bridge_get(JOBS["kimi"])
    mimo = bridge_get(JOBS["mimo"])
    assert kimi["stage"] == "failed"
    assert mimo["stage"] == "completed"
    assert mimo["execution"]["status"] == "result_ready"
    assert mimo["execution"]["decision"]["selected"] == "mimo"
    assert mimo["synthesis_source"] == "executor_direct"
    result = mimo["execution"]["result"]["text"]
    raw_path = HERE / "MIMO_OPPORTUNITY_RESULT_DECLARADO.txt"
    raw = result.encode("utf-8")
    if raw_path.exists():
        assert raw_path.read_bytes() == raw
    else:
        atomic_write(raw_path, raw)
    raw_hash = hashlib.sha256(raw).hexdigest()

    audit = {
        "status": "LOCAL_CRITICAL_REVIEW_NOT_CANONICAL",
        "at": datetime.now(timezone.utc).isoformat(),
        "job_id": JOBS["mimo"],
        "request_id": mimo["request_id"],
        "execution_task_id": mimo["execution_task_id"],
        "executor": "mimo",
        "synthesis_source": mimo["synthesis_source"],
        "work_assistance_used": False,
        "raw_result_path": str(raw_path),
        "raw_result_sha256": raw_hash,
        "assessment": "[DECLARADO] useful statistical design suggestions, but mathematical and calibration errors prevent promotion as an approved scientific protocol",
        "corrections": [
            "[DERIVED] With exp(-Gamma t), tau_obs/tau_GR-1 = -x/(1+x), x=Gamma*tau_GR; -x is first-order only.",
            "[DERIVED] A calibrated nominal 1-sigma interval covers about 68.3%, not 95%; use nominal 95% intervals for a 95% coverage check.",
            "[DERIVED] For whitened residuals use Jw=C^(-1/2)J and P=I-Jw(Jw^T Jw)^+Jw^T; the result's original-coordinate projector cannot be applied to an already whitened residual.",
            "[OPEN] A 5-sigma threshold/power needs null-tail calibration or justified extrapolation; 10^4 null simulations cannot directly resolve a 5-sigma p-value. The proposed pre-tail power gate is circular as written.",
            "[OPEN] The offsource >5% stop threshold and correlation >0.95 cutoff are proposals without a calibrated alpha or identifiability rationale.",
            "[DECLARADO] The cited v367/v369 propagation-versus-local-G interpretation was not checked against the cited original in this review.",
        ],
        "preserved_suggestions": [
            "Pre-register clock and selection rules; split by event identity and data lineage.",
            "Model nuisance parameters and covariance, run injection-recovery/offsource controls, and do not infer sigma from fixed Delta-chi-squared.",
            "Keep D10 acoustic work first and avoid adding dependent D9/D10/Planck likelihoods as independent evidence.",
        ],
    }
    audit_path = HERE / "MIMO_OPPORTUNITY_LOCAL_AUDIT.json"
    audit_data = json.dumps(audit, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    if audit_path.exists():
        assert audit_path.read_bytes() == audit_data
    else:
        atomic_write(audit_path, audit_data)

    manifest_path = HERE / "OPPORTUNITY_UNITS_20260928.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["units"]["kimi"]["request_id"] == kimi["request_id"]
    assert manifest["units"]["mimo"]["request_id"] == mimo["request_id"]
    manifest["status"] = "kimi_failed_terminal_mimo_completed_declared"
    manifest["disposition"] = {
        "kimi_job_id": JOBS["kimi"],
        "kimi_stage": kimi["stage"],
        "kimi_retry": "forbidden_without_new_specific_authorization",
        "mimo_job_id": JOBS["mimo"],
        "mimo_stage": mimo["stage"],
        "mimo_result_sha256": raw_hash,
        "mimo_local_audit": str(audit_path),
    }
    atomic_write(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"), existing=True)

    slots_path = BASE / "state" / "handoffs" / "slot_management.json"
    slots = json.loads(slots_path.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc).isoformat()
    slots["at"] = now
    slots["last_checked_at"] = now
    slots["status"] = "MANAGER_TWO_NEW_UNITS_KIMI_FAILED_MIMO_COMPLETED_DECLARADO"
    slots["active_providers"] = []
    slots["free_admission_slots"] = 4
    slots["free_execution_slots"] = 3
    slots["mimo_status"] = "NEW_DISTINCT_UNIT_COMPLETED_AUDITED_PROCESS_DECLARADO"
    slots["manager_response_status"] = "TWO_NEW_UNITS_RESOLVED_ONE_FAILED_ONE_COMPLETED_DECLARADO"
    slots["manager_response"] = "Manager authorized two distinct units; Kimi failed terminal without accepted result and cannot retry. MiMo completed once under audited normal-user identity; its direct response needs corrections documented in local audit."
    slots["next_action"] = "Report compact disposition to manager; await genuinely new unit or changed authorization. Do not repeat Kimi or blocked Claude."
    slots["deduplication"] = "Both new request IDs are consumed. Kimi is terminal failed; MiMo completed. No duplicate provider calls or slot solicitation."
    slots["current_jobs"][JOBS["mimo"]]["stage"] = "completed"
    slots["current_jobs"][JOBS["mimo"]]["result_sha256"] = raw_hash
    slots["current_jobs"][JOBS["mimo"]]["synthesis_source"] = "executor_direct"
    slots["mimo_opportunity_raw_result"] = str(raw_path)
    slots["mimo_opportunity_raw_sha256"] = raw_hash
    slots["mimo_opportunity_local_audit"] = str(audit_path)
    slots["mimo_opportunity_local_audit_sha256"] = hashlib.sha256(audit_data).hexdigest()
    for item in slots["prior_slot_requests"]:
        if item.get("status") == "MANAGER_INITIATED_TWO_NEW_UNITS" and item.get("request_ids") == [kimi["request_id"], mimo["request_id"]]:
            item["status"] = "RESOLVED_KIMI_FAILED_MIMO_COMPLETED_DECLARADO"
            item["resolved_at"] = now
            item["response"] = slots["manager_response"]
            break
    else:
        raise ValueError("Expected manager request record missing")
    atomic_write(slots_path, (json.dumps(slots, ensure_ascii=False, indent=2) + "\n").encode("utf-8"), existing=True)
    print(json.dumps({"kimi": kimi["stage"], "mimo": mimo["stage"], "result_sha256": raw_hash, "audit_sha256": slots["mimo_opportunity_local_audit_sha256"]}))


if __name__ == "__main__":
    main()
