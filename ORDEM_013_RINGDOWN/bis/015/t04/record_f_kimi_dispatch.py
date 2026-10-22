"""Pin the queued one-call Kimi F review to its original request."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "orchestration" / "t04f_kimi_receipt.json"
old = p.read_bytes()
obj = json.loads(old)
assert obj["request_id"] == "fbad86c6-6953-46f6-bcdf-bdaf6b43be67"
assert obj["state"] == "PREPARED_NOT_SUBMITTED" and obj["job_id"] is None
backup = p.with_name(p.name + ".bak_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))
with backup.open("xb") as stream:
    stream.write(old)
    stream.flush()
    os.fsync(stream.fileno())
assert backup.read_bytes() == old
obj.update(job_id="70de5c3b-1dfe-47c5-b637-315f475e3b57",state="QUEUED_AWAITING_DISPATCH",
           submitted_utc=datetime.now(timezone.utc).isoformat())
data = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
temp = p.with_name(p.name + ".tmp")
with temp.open("xb") as stream:
    stream.write(data)
    stream.flush()
    os.fsync(stream.fileno())
assert temp.stat().st_size == len(data)
os.replace(temp, p)
assert p.read_bytes() == data
print(json.dumps(dict(status=obj["state"],job_id=obj["job_id"],backup=backup.name)))
