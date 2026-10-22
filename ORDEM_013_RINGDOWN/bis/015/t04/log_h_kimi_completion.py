"""Append the one completed Kimi H review to the ORDEM016 call ledger."""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHATGPT = HERE.parents[3]
LEDGER = CHATGPT / "TUNEL" / "DO_CHATGPT" / "LEDGER_016.jsonl"
RECEIPT = CHATGPT / "IALD_ORQUESTRACAO_20260923" / "state" / "handoffs" / "d79265aa-25a7-454d-8a00-7a8965d05ff6_delivery.json"


def main() -> None:
    obj = json.loads(RECEIPT.read_bytes())
    assert obj["stage"] == "completed" and obj["provider"] == "kimi"
    assert obj["request_id"] == "5bc73eda-99a3-4c9b-b6fc-7fd926d33a65"
    original = LEDGER.read_bytes()
    assert obj["request_id"].encode() not in original, "Do not duplicate this call"
    backup = LEDGER.with_name(LEDGER.name + ".bak_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))
    with backup.open("xb") as stream:
        stream.write(original)
        stream.flush()
        os.fsync(stream.fileno())
    assert backup.read_bytes() == original
    entry = dict(at=datetime.now(timezone.utc).isoformat(),event="ORDEM016_PROVIDER_CALL_AUDIT",
        branch="B_T04_H",lemma="post_C_route_and_budget",role="skeptic",
        provider="kimi",request_id=obj["request_id"],job_id=obj["job_id"],
        status="completed",model=obj["model"],prompt_sha256=obj["prompt_sha256"],
        response_sha256=obj["result_sha256"],receipt_sha256=hashlib.sha256(RECEIPT.read_bytes()).hexdigest(),
        usage=obj["usage"],cost_estimate_usd=None,
        cost_status="SUBSCRIPTION_ACCOUNTING_UNKNOWN_NOT_ZERO",
        scientific_status="DECLARADO_CONDITIONAL_ADVICE_NOT_SOURCE_REVIEWED_NOT_PROOF")
    line = (json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    assert original.endswith(b"\n")
    updated = original + line
    temp = LEDGER.with_name(LEDGER.name + ".tmp_h_kimi")
    with temp.open("xb") as stream:
        stream.write(updated)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.stat().st_size == len(updated)
    assert LEDGER.read_bytes() == original, "Concurrent ledger change; refuse overwrite"
    os.replace(temp, LEDGER)
    assert LEDGER.read_bytes() == updated
    print(json.dumps(dict(status="KIMI_H_LEDGERED",request_id=obj["request_id"],
                          receipt_sha256=entry["receipt_sha256"],backup=backup.name)))


if __name__ == "__main__":
    main()
