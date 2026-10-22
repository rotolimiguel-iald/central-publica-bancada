"""Audit one MiMo draft and ledger it once, preserving original bytes."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAT = HERE.parents[3]
RECEIPT = CHAT / "IALD_ORQUESTRACAO_20260923" / "state" / "handoffs" / "8a5e90b6-2368-468e-8ebd-cdb2114eaff4_delivery.json"
LEDGER = CHAT / "TUNEL" / "DO_CHATGPT" / "LEDGER_016.jsonl"
AUDIT = HERE / "T08_MIMO_SCIENTIFIC_AUDIT.json"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

receipt = json.loads(RECEIPT.read_bytes())
assert receipt["job_id"] == "8a5e90b6-2368-468e-8ebd-cdb2114eaff4"
assert receipt["provider"] == "mimo" and receipt["stage"] == "completed"
audit = {
    "status": "DECLARADO_DRAFT_REJECTED_AS_T08_PROTOCOL",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "receipt_sha256": sha(RECEIPT), "provider_result_sha256": receipt["result_sha256"],
    "checks": [
        {"issue": "EPSILON_MISTYPED", "finding": "T08 epsilon(theta) is detection/selection efficiency under injections, not echo amplitude."},
        {"issue": "ALPHA_MISTYPED", "finding": "T08 alpha(Lambda) is per-reading selection normalization, not a coupling constant."},
        {"issue": "TABLE_IV_MISTYPED", "finding": "GWTC3 Table IV reports cutoff frequency and split SNR for selected O3b events, not GR full-IMR MAP posterior samples."},
        {"issue": "LVK_THRESHOLD_MISATTRIBUTED", "finding": "Primary GWTC3 and GWTC4 IMRCT papers use >6 for each part; >=8 is a stricter order input, not the cited LVK IMRCT rule."},
        {"issue": "SNR_FORMULA_INVALID", "finding": "Displayed first SNR equality inserts a redundant quotient undefined when (h|d)=0; expected waveform norm and observed matched-filter projection also have distinct roles."},
        {"issue": "ARBITRARY_CUTOFF_AND_ECHO", "finding": "Time/f220 alternatives and an echo template were invented outside the T08 prescribed source convention; sqrt(beta) echo route is dead in ORDEM016."},
        {"issue": "MAP_SUBSTITUTION", "finding": "A remnant mass/spin median cannot substitute for full binary MAP parameters in an accepted 74-event table."},
    ],
    "usable_fragment": "Need detector PSD, full-IMR GR source parameters, pre-registered frequency split, and explicit missingness by event; not accepted without local verification.",
    "gate_changed": False,
}
with AUDIT.open("xb") as stream:
    stream.write((json.dumps(audit, ensure_ascii=False, indent=2) + "\n").encode())

line = {"at": datetime.now(timezone.utc).isoformat(), "event": "ORDEM016_PROVIDER_CALL_AUDIT",
        "branch": "B_T08", "lemma": "selection_protocol_draft", "role": "draft", "provider": "mimo",
        "request_id": receipt["request_id"], "job_id": receipt["job_id"], "status": receipt["stage"],
        "model": receipt["model"], "prompt_sha256": receipt["prompt_sha256"],
        "response_sha256": receipt["result_sha256"], "receipt_sha256": sha(RECEIPT),
        "usage": receipt["usage"], "cost_estimate_usd": None,
        "scientific_status": audit["status"], "audit_sha256": sha(AUDIT)}
old = LEDGER.read_bytes()
assert receipt["job_id"].encode() not in old
backup = LEDGER.with_name(LEDGER.name + ".bak_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"))
with backup.open("xb") as stream:
    stream.write(old)
assert backup.read_bytes() == old
new = old + (json.dumps(line, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
temp = LEDGER.with_name(LEDGER.name + ".tmp_t08")
with temp.open("xb") as stream:
    stream.write(new)
assert temp.stat().st_size == len(new)
os.replace(temp, LEDGER)
assert LEDGER.read_bytes() == new
print(json.dumps({"audit_sha256": sha(AUDIT), "ledger_sha256": sha(LEDGER),
                  "prompt_tokens": receipt["usage"]["prompt_tokens"],
                  "completion_tokens": receipt["usage"]["completion_tokens"]}))
