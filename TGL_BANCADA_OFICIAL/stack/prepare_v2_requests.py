"""Prepare immutable provider-locked requests for the official IALD transport."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923")
UNITS = (
    ("kimi_architecture", "BRIEF_V2_ARCHITECTURE.md", "kimi", "architecture"),
    ("mimo_data_audit", "BRIEF_V2_DATA_AUDIT.md", "mimo", "data-audit"),
)


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".new")
    temp.write_bytes(content)
    if temp.stat().st_size != len(content):
        raise OSError("Incomplete request write")
    temp.replace(path)


def main() -> None:
    for name, brief_name, provider, lemma in UNITS:
        marker = HERE / (name + ".request_id")
        if marker.exists():
            request_id = marker.read_text(encoding="ascii").strip()
            uuid.UUID(request_id)
        else:
            request_id = str(uuid.uuid4())
            atomic_write(marker, (request_id + "\n").encode("ascii"))
        prompt = (HERE / brief_name).read_text(encoding="utf-8").strip()
        constraints = {
            "mission_id": "TGL_BANCADA_OFICIAL", "branch_id": "cockpit-v2",
            "lemma_id": lemma, "role": "draft" if provider == "kimi" else "skeptic",
            "required_provider": provider, "max_calls": 1,
        }
        request = {"operation": "submit_execution", "request_id": request_id,
                   "prompt": prompt, "execution_constraints": constraints}
        atomic_write(HERE / (name + ".submit.json"),
                     json.dumps(request, ensure_ascii=False).encode("utf-8"))
        receipt = BASE / "state" / "session_requests" / (request_id + ".json")
        if not receipt.exists():
            record = {"request_id": request_id,
                      "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                      "origin": str(HERE.parent), "mission": "TGL_BANCADA_OFICIAL",
                      "status": "prepared_not_submitted", "required_provider": provider,
                      "prompt": prompt, "execution_constraints": constraints}
            atomic_write(receipt, json.dumps(record, ensure_ascii=False, indent=2).encode("utf-8"))
        print(json.dumps({"name": name, "request_id": request_id,
                          "submit_file": str(HERE / (name + ".submit.json"))}))


if __name__ == "__main__":
    main()
