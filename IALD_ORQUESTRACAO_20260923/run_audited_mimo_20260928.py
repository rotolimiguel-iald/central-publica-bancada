"""Run one authorized MiMo coordination job under a measured Windows identity."""

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from iald_orchestrator.coordination import Coordination
from iald_orchestrator.worker_identity import require_expected_identity


BASE = Path(__file__).resolve().parent
JOB_ID = "a8442454-7fbe-4bed-b8ad-c9b65d88f2b0"
REQUEST_ID = "6f74a1e8-0891-4da3-9955-38e1c746f158"
PROOF = BASE / "state" / "handoffs" / f"{JOB_ID}_worker_proof.json"
RESULT = BASE / "state" / "handoffs" / f"{JOB_ID}_worker_outcome.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_new_json(path: Path, payload: dict) -> None:
    if path.exists():
        raise RuntimeError(f"Evidence already exists; refusing a second run: {path.name}")
    encoded = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temporary = path.with_name(path.name + f".tmp_{os.getpid()}")
    with temporary.open("xb") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.stat().st_size != len(encoded):
        raise RuntimeError("Evidence size verification failed.")
    os.replace(temporary, path)


def main() -> None:
    identity = require_expected_identity()
    coordinator = Coordination()
    job = coordinator.get(JOB_ID)
    if job["request_id"] != REQUEST_ID or job["stage"] != "awaiting_dispatch":
        raise RuntimeError("Job identity or stage changed; no provider call allowed.")
    constraints = job["execution_constraints"] or {}
    if constraints.get("required_provider") != "mimo" or constraints.get("max_calls") != 1:
        raise RuntimeError("MiMo lock or one-call constraint missing.")
    files = ["iald_orchestrator/mimo.py", "iald_orchestrator/providers.py", "iald_orchestrator/coordination.py"]
    proof = {
        "at": datetime.now(timezone.utc).isoformat(),
        "job_id": JOB_ID,
        "request_id": REQUEST_ID,
        "identity": identity,
        "adapter_source_sha256": {name: sha256(BASE / name) for name in files},
        "stage_before": job["stage"],
        "required_provider": "mimo",
        "max_calls": 1,
        "process_scope": "new process, one MiMo unit, no retry",
    }
    write_new_json(PROOF, proof)
    prepared = coordinator.act(JOB_ID, "prepare_without_work", {"reason": "assistance_not_needed"})
    if prepared["stage"] != "prompt_ready":
        raise RuntimeError("Preparation did not reach prompt_ready; no provider call.")
    try:
        coordinator.act(JOB_ID, "execute")
        while coordinator.runtime.worker_lock.locked() or coordinator.get(JOB_ID)["execution"]["status"] in ("queued", "running"):
            time.sleep(0.2)
        final = coordinator.act(JOB_ID, "sync_execution")
    except Exception as exc:
        final = coordinator.get(JOB_ID)
        write_new_json(RESULT, {
            "at": datetime.now(timezone.utc).isoformat(),
            "job_id": JOB_ID,
            "stage": final["stage"],
            "error_type": type(exc).__name__,
            "error": str(exc)[:600],
            "execution_task_id": final.get("execution_task_id"),
        })
        raise
    write_new_json(RESULT, {
        "at": datetime.now(timezone.utc).isoformat(),
        "job_id": JOB_ID,
        "stage": final["stage"],
        "error": final.get("error"),
        "execution_task_id": final.get("execution_task_id"),
        "execution_status": (final.get("execution") or {}).get("status"),
        "selected": ((final.get("execution") or {}).get("decision") or {}).get("selected"),
    })
    print(json.dumps({"job_id": JOB_ID, "stage": final["stage"], "error": final.get("error"), "execution_task_id": final.get("execution_task_id")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
