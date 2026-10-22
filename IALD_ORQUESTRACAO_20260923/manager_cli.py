"""Manager-neutral JSON/stdin entry point for the one IALD queue.

Codex, Claude and a future native Qwen controller use the same persistent
coordination state. Reading and previewing never calls a model. Mutations are
limited to already admitted jobs and remain guarded by Coordination.act.
"""

import json
import sys

from iald_orchestrator.coordination import Coordination
from iald_orchestrator.transport import Transport


def dispatch(request, coordination=None):
    if not isinstance(request, dict):
        raise ValueError("JSON object required.")
    coordination = coordination or Coordination()
    operation = request.get("operation")

    if operation == "status":
        return {
            "runtime": coordination.runtime.status(),
            "coordination_jobs": coordination.listing(),
        }
    if operation == "next":
        return Transport(coordination).next_job()
    if operation == "list":
        return coordination.listing()
    if operation == "get":
        return coordination.get(request["job_id"])
    if operation == "preview_job":
        job = coordination.get(request["job_id"])
        return {
            "job_id": job["id"],
            "stage": job["stage"],
            "decision": coordination.runtime.preview(
                job["prompt"], job["execution_constraints"]
            ),
        }
    if operation == "act":
        # No submit operation here: a model's output cannot create authority.
        return coordination.act(
            request["job_id"], request["action"], request.get("payload")
        )
    raise ValueError("Unsupported manager operation.")


def main():
    request = json.load(sys.stdin)
    result = dispatch(request)
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
