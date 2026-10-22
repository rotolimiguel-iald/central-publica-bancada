"""Record elapsed Part B wall time; concurrent receipt durations are not added."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import re

BASE = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", required=True)
    parser.add_argument("--record", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_]{1,70}", args.stage):
        raise ValueError("Unsafe stage label")
    source = BASE / "bis/PART_B_BUDGET_START.json"
    budget = json.loads(source.read_bytes())
    deadline = datetime.fromisoformat(budget["hard_deadline_utc"].replace("Z", "+00:00"))
    # The signed budget defines a continuous forty-hour envelope.
    from datetime import timedelta
    start = deadline - timedelta(hours=40)
    now = datetime.now(timezone.utc)
    elapsed = (now-start).total_seconds()
    remaining = (deadline-now).total_seconds()
    if elapsed < 0:
        raise ValueError("Budget has not begun")
    data = {
        "status": "WITHIN_SHARED_WALL_ENVELOPE" if remaining > 0 else "BUDGET_EXPIRED",
        "stage": args.stage,
        "measured_utc": now.isoformat(),
        "start_utc_from_deadline_minus_40h": start.isoformat(),
        "hard_deadline_utc": deadline.isoformat(),
        "elapsed_wall_seconds": elapsed,
        "remaining_wall_seconds": max(0.0, remaining),
        "elapsed_wall_hours": elapsed/3600,
        "remaining_wall_hours": max(0.0, remaining)/3600,
        "budget_sha256": digest(source),
        "code_sha256": digest(Path(__file__)),
        "accounting": "Continuous wall time since signed Part B start. No sum of concurrent jobs; includes orchestration/review. Historical F0 before this start is outside this envelope.",
        "scope": "Accounting only; this receipt neither allocates nor authorizes any job."
    }
    if args.record:
        target = BASE / "bis" / ("PART_B_CLOCK_"+now.strftime("%Y%m%dT%H%M%S%fZ")+"_"+args.stage+".json")
        raw = (json.dumps(data, indent=2, allow_nan=False)+"\n").encode()
        temporary = target.with_name(target.name+".pending")
        with temporary.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        if temporary.stat().st_size != len(raw):
            raise IOError("Incomplete accounting receipt")
        os.link(temporary, target)
        temporary.unlink()
        data["receipt"] = str(target)
        data["receipt_sha256"] = digest(target)
    print(json.dumps(data, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
