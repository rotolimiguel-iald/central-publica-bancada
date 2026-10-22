"""Record the completed, single Kimi T04-F review without repeating the call."""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

here = Path(__file__).resolve().parent
chatgpt = here.parents[3]
ledger = chatgpt / "TUNEL" / "DO_CHATGPT" / "LEDGER_016.jsonl"
receipt = chatgpt / "IALD_ORQUESTRACAO_20260923" / "state" / "handoffs" / "70de5c3b-1dfe-47c5-b637-315f475e3b57_delivery.json"


def main() -> None:
    raw = receipt.read_bytes()
    item = json.loads(raw)
    assert item["stage"] == "completed" and item["provider"] == "kimi"
    assert item["request_id"] == "fbad86c6-6953-46f6-bcdf-bdaf6b43be67"
    old = ledger.read_bytes()
    assert item["request_id"].encode() not in old
    assert old.endswith(b"\n")
    now = datetime.now(timezone.utc)
    backup = ledger.with_name(ledger.name + ".bak_" + now.strftime("%Y%m%d_%H%M%S"))
    with backup.open("xb") as out:
        out.write(old)
        out.flush()
        os.fsync(out.fileno())
    assert backup.read_bytes() == old
    entry = dict(at=now.isoformat(), event="ORDEM016_PROVIDER_CALL_AUDIT", branch="B_T04_F",
                 lemma="concrete_kerr_dtau_f_skeptic", role="skeptic", provider="kimi",
                 request_id=item["request_id"], job_id=item["job_id"], status=item["stage"],
                 model=item["model"], prompt_sha256=item["prompt_sha256"],
                 response_sha256=item["result_sha256"],
                 receipt_sha256=hashlib.sha256(raw).hexdigest(), usage=item["usage"],
                 cost_estimate_usd=None,
                 scientific_status="DECLARADO_TEXTUAL_SPECIFICATION_REVIEW_NOT_SOURCE_AUDIT_OR_PROOF")
    new = old + (json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    temp = ledger.with_name(ledger.name + ".tmp_f_kimi")
    with temp.open("xb") as out:
        out.write(new)
        out.flush()
        os.fsync(out.fileno())
    assert ledger.read_bytes() == old
    os.replace(temp, ledger)
    assert ledger.read_bytes() == new
    print(json.dumps({"status": "F_KIMI_LOGGED", "receipt_sha256": entry["receipt_sha256"]}))


if __name__ == "__main__":
    main()
