"""One fresh audited process per admitted D10 provider unit."""

import hashlib
import json
from pathlib import Path
import sys
import time

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from iald_orchestrator.coordination import Coordination
from iald_orchestrator.worker_identity import require_expected_identity

CATALOG = Path(__file__).resolve().parent / "D10_CMB_BAO_PREPARED_UNITS.json"


def main(provider):
    if provider not in ("kimi", "mimo"):
        raise ValueError("Unknown D10 provider")
    identity = require_expected_identity()
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    unit = catalog["units"][provider]
    if unit["status"] != "PROMPT_READY_LOCAL":
        raise RuntimeError("Unit not prepared or already attempted")
    if hashlib.sha256(unit["prompt"].encode("utf-8")).hexdigest() != unit["prompt_sha256"]:
        raise RuntimeError("Prompt hash mismatch")
    coordinator = Coordination()
    job = coordinator.get(unit["job_id"])
    if (job["stage"] != "prompt_ready" or job["request_id"] != unit["request_id"]
            or job["execution_constraints"]["required_provider"] != provider
            or job["prepared_prompt"] != unit["prompt"].strip()):
        raise RuntimeError("Coordinator state differs from manager-admitted unit")
    preview = coordinator.runtime.preview(job["prompt"], job["execution_constraints"])
    if preview["selected"] != provider:
        raise RuntimeError("Required provider no longer eligible")
    print(json.dumps({"event": "identity_verified", "provider": provider,
                      "job_id": unit["job_id"], "user": identity["user"],
                      "sid": identity["sid"], "pid": identity["pid"]}), flush=True)
    coordinator.act(unit["job_id"], "execute")
    print(json.dumps({"event": "execution_registered", "provider": provider,
                      "job_id": unit["job_id"]}), flush=True)
    deadline = time.monotonic() + 3900
    while time.monotonic() < deadline:
        job = coordinator.get(unit["job_id"])
        execution = job.get("execution") or {}
        if execution.get("status") not in ("queued", "running"):
            break
        time.sleep(2)
    job = coordinator.act(unit["job_id"], "sync_execution")
    execution = job.get("execution") or {}
    print(json.dumps({"event": "execution_observed", "provider": provider,
                      "job_id": unit["job_id"], "stage": job["stage"],
                      "execution_status": execution.get("status"),
                      "execution_task_id": job.get("execution_task_id"),
                      "error": (execution.get("error") or "")[:500]}), flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
