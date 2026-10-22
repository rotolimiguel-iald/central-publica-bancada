"""Pin the queued single-use skeptical review to its existing request receipt."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECEIPT = HERE.parent / "orchestration" / "t04h_kimi_receipt.json"
JOB_ID = "d79265aa-25a7-454d-8a00-7a8965d05ff6"


def main() -> None:
    original = RECEIPT.read_bytes()
    obj = json.loads(original)
    assert obj["request_id"] == "5bc73eda-99a3-4c9b-b6fc-7fd926d33a65"
    assert obj["state"] == "PREPARED_NOT_SUBMITTED" and obj["job_id"] is None
    backup = RECEIPT.with_name(RECEIPT.name + ".bak_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))
    with backup.open("xb") as stream:
        stream.write(original)
        stream.flush()
        os.fsync(stream.fileno())
    assert backup.read_bytes() == original
    obj.update(job_id=JOB_ID, state="QUEUED_AWAITING_DISPATCH",
               submitted_utc=datetime.now(timezone.utc).isoformat(),
               queue_stage="awaiting_dispatch")
    data = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temporary = RECEIPT.with_name(RECEIPT.name + ".tmp")
    with temporary.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.stat().st_size == len(data)
    os.replace(temporary, RECEIPT)
    assert RECEIPT.read_bytes() == data
    print(json.dumps(dict(status=obj["state"], job_id=JOB_ID, backup=backup.name)))


if __name__ == "__main__":
    main()
