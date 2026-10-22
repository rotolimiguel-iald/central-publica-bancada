"""Dispatch the single prepared Opus unit under the audited Windows identity."""

import json
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from iald_orchestrator.coordination import Coordination
from iald_orchestrator.worker_identity import require_expected_identity

JOB_ID = "65f577e6-8dd1-4e91-8b79-c86e2abbc68a"
REQUEST_ID = "4529daec-d42e-4c01-87d1-dd3d183070b7"


def main():
    identity = require_expected_identity()
    coordinator = Coordination()
    job = coordinator.get(JOB_ID)
    constraints = job["execution_constraints"]
    if (job["stage"] != "prompt_ready" or job["request_id"] != REQUEST_ID
            or constraints["required_provider"] != "claude"):
        raise RuntimeError("Opus unit is not prepared with its reserved identity")
    preview = coordinator.runtime.preview(job["prepared_prompt"], constraints)
    if preview["selected"] != "claude":
        raise RuntimeError("Claude executor no longer eligible")
    print(json.dumps({"event": "identity_verified", "job_id": JOB_ID,
                      "user": identity["user"], "sid": identity["sid"],
                      "pid": identity["pid"]}), flush=True)
    coordinator.act(JOB_ID, "execute")
    print(json.dumps({"event": "execution_registered", "job_id": JOB_ID}), flush=True)
    deadline = time.monotonic() + 1000
    while time.monotonic() < deadline:
        job = coordinator.get(JOB_ID)
        execution = job.get("execution") or {}
        if execution.get("status") not in ("queued", "running"):
            break
        time.sleep(2)
    job = coordinator.act(JOB_ID, "sync_execution")
    execution = job.get("execution") or {}
    print(json.dumps({"event": "execution_observed", "job_id": JOB_ID,
                      "stage": job["stage"], "execution_status": execution.get("status"),
                      "execution_task_id": job.get("execution_task_id"),
                      "error": (execution.get("error") or "")[:500]}), flush=True)


if __name__ == "__main__":
    main()
