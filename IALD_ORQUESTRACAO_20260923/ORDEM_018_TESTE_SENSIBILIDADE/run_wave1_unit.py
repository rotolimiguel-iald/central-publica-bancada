"""Run one already prepared ORDEM_018 unit with an audited Windows identity."""

import json
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from iald_orchestrator.coordination import Coordination
from iald_orchestrator.worker_identity import require_expected_identity


JOBS = {
    "wave1": {
        "kimi": "d630a1f1-5979-49ef-abc0-5bbc83765d4e",
        "mimo": "562a6e05-3d29-44a9-adc8-9e3c878fce81",
        "deepseek": "f36f9022-6f74-467c-bb55-dccf8c535a76",
    },
    "wave2": {
        "kimi": "6251ffbf-ac6c-4677-8554-2751d44cca1d",
        "mimo": "4e5d6abc-f34e-4b74-b844-d54d9beca920",
        "deepseek": "a7950ace-ac09-4ff6-a163-f49193ff5cd9",
    },
}


def main():
    wave = sys.argv[2] if len(sys.argv) > 2 else "wave1"
    provider = sys.argv[1]
    job_id = JOBS[wave][provider]
    identity = require_expected_identity()
    coordinator = Coordination()
    job = coordinator.get(job_id)
    constraints = job["execution_constraints"]
    if job["stage"] != "prompt_ready" or constraints["required_provider"] != provider:
        raise RuntimeError("Unit is not prepared for the required provider.")
    preview = coordinator.runtime.preview(job["prepared_prompt"], constraints)
    if preview["selected"] != provider:
        raise RuntimeError("Provider preview no longer matches the required provider.")
    print(json.dumps({"event": "identity_verified", "provider": provider,
                      "job_id": job_id, "user": identity["user"],
                      "sid": identity["sid"], "pid": identity["pid"]}), flush=True)
    coordinator.act(job_id, "execute")
    print(json.dumps({"event": "execution_registered", "provider": provider,
                      "job_id": job_id}), flush=True)
    deadline = time.monotonic() + 3600
    while time.monotonic() < deadline:
        job = coordinator.get(job_id)
        execution = job.get("execution") or {}
        if execution.get("status") not in ("queued", "running"):
            break
        time.sleep(1)
    job = coordinator.act(job_id, "sync_execution")
    execution = job.get("execution") or {}
    print(json.dumps({"event": "execution_observed", "provider": provider,
                      "job_id": job_id, "stage": job["stage"],
                      "execution_status": execution.get("status"),
                      "execution_task_id": job.get("execution_task_id"),
                      "error": (execution.get("error") or "")[:500]}), flush=True)


if __name__ == "__main__":
    main()
