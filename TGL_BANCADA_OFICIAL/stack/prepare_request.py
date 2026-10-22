"""Create one idempotent orchestration request and its local receipt."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923")
BRIEF = HERE / "BRIEF_COCKPIT.md"
MARKER = HERE / "request_id.txt"


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_bytes(data)
    if temp.stat().st_size != len(data):
        raise OSError(f"Incomplete write: {temp}")
    temp.replace(path)


def main() -> None:
    if MARKER.exists():
        request_id = MARKER.read_text(encoding="ascii").strip()
        uuid.UUID(request_id)
    else:
        request_id = str(uuid.uuid4())
        atomic_write(MARKER, (request_id + "\n").encode("ascii"))
    prompt = BRIEF.read_text(encoding="utf-8")
    receipt = BASE / "state" / "session_requests" / f"{request_id}.json"
    if not receipt.exists():
        record = {
            "request_id": request_id,
            "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "origin": r"C:\IALD\Central de Patentes\Chatgpt\TGL_BANCADA_OFICIAL",
            "origin_thread_id": "01a070fc-9484-7e13-a654-c6b5f61093a4",
            "mission": "TGL interactive research cockpit design",
            "status": "prepared_not_submitted",
            "prompt": prompt,
        }
        atomic_write(receipt, json.dumps(record, ensure_ascii=False, indent=2).encode("utf-8"))
    call = {"operation": "submit", "prompt": prompt, "request_id": request_id}
    atomic_write(HERE / "submit.json", json.dumps(call, ensure_ascii=False).encode("utf-8"))
    print(json.dumps({"request_id": request_id, "receipt": str(receipt), "call": str(HERE / "submit.json")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
