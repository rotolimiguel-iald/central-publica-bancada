"""Stop only the witnessed T04-H supervisor, letting it clean its own child."""
from __future__ import annotations

import json
import os
import signal
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROCESS = HERE / "branch_h" / "PROCESS.json"
EXPECTED_CHILD = b"run_controlled.py\0--job\0GW250114_PILOT_V2_S220_H1\0"
EXPECTED_PARENT = b"supervise_t04_h.py\0branch_h\0"


def main() -> None:
    obj = json.loads(PROCESS.read_bytes())
    child = obj["pid"]
    child_cmd = Path(f"/proc/{child}/cmdline").read_bytes()
    assert EXPECTED_CHILD in child_cmd, "Child PID no longer belongs to H1"
    status = Path(f"/proc/{child}/status").read_text()
    parent = int(next(line.split(":", 1)[1] for line in status.splitlines() if line.startswith("PPid:")))
    parent_cmd = Path(f"/proc/{parent}/cmdline").read_bytes()
    assert EXPECTED_PARENT in parent_cmd, "Parent PID is not the H supervisor"
    os.kill(parent, signal.SIGTERM)
    print(json.dumps(dict(status="SIGTERM_SENT_TO_OWNED_H_SUPERVISOR", parent_pid=parent,
                          child_pid=child, cleanup_by_supervisor=True)))


if __name__ == "__main__":
    main()
