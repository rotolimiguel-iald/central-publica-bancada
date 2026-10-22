"""Append the single completed MiMo F draft to the ORDEM016 call ledger."""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHATGPT = HERE.parents[3]
LEDGER = CHATGPT / "TUNEL" / "DO_CHATGPT" / "LEDGER_016.jsonl"
RECEIPT = CHATGPT / "IALD_ORQUESTRACAO_20260923" / "state" / "handoffs" / "7f3e16e9-694e-461c-8606-dfe3466c4938_delivery.json"


def main() -> None:
    obj = json.loads(RECEIPT.read_bytes())
    assert obj["stage"] == "completed" and obj["provider"] == "mimo"
    assert obj["request_id"] == "8800472d-1455-43c2-bb0b-4a7a21e43de1"
    usage = obj["usage"]
    cached = usage.get("prompt_tokens_details", {}).get("cached_tokens", 0)
    estimate = ((Decimal(usage["prompt_tokens"]-cached)*Decimal("0.435"))
                +(Decimal(cached)*Decimal("0.0036"))
                +(Decimal(usage["completion_tokens"])*Decimal("0.87")))/Decimal(1_000_000)
    assert estimate < Decimal("0.50")
    original = LEDGER.read_bytes()
    assert obj["request_id"].encode() not in original
    backup = LEDGER.with_name(LEDGER.name + ".bak_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))
    with backup.open("xb") as stream:
        stream.write(original)
        stream.flush()
        os.fsync(stream.fileno())
    assert backup.read_bytes() == original
    entry = dict(at=datetime.now(timezone.utc).isoformat(),event="ORDEM016_PROVIDER_CALL_AUDIT",
        branch="B_T04_F",lemma="kerr_dtau220_extension",role="draft",
        provider="mimo",request_id=obj["request_id"],job_id=obj["job_id"],
        status="completed",model=obj["model"],prompt_sha256=obj["prompt_sha256"],
        response_sha256=obj["result_sha256"],receipt_sha256=hashlib.sha256(RECEIPT.read_bytes()).hexdigest(),
        usage=usage,cost_estimate_usd=str(estimate),
        cost_status="ESTIMATE_FROM_PROVIDER_TOKENS_AND_PINNED_20260923_RATES_NOT_INVOICE",
        scientific_status="DECLARADO_DRAFT_DEFECT_FOUND_AND_CORRECTED_LOCALLY_NOT_PROOF")
    line = (json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    assert original.endswith(b"\n")
    updated = original + line
    temp = LEDGER.with_name(LEDGER.name + ".tmp_f_mimo")
    with temp.open("xb") as stream:
        stream.write(updated)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.stat().st_size == len(updated)
    assert LEDGER.read_bytes() == original, "Concurrent ledger change; refuse overwrite"
    os.replace(temp, LEDGER)
    assert LEDGER.read_bytes() == updated
    print(json.dumps(dict(status="MIMO_F_LEDGERED",cost_estimate_usd=str(estimate),
                          receipt_sha256=entry["receipt_sha256"],backup=backup.name)))


if __name__ == "__main__":
    main()
