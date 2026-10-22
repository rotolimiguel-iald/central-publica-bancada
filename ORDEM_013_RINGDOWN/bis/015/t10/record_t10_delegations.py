"""Audit completed T10 advisory calls using the sanctioned bridge, no state files."""
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHATGPT = HERE.parents[3]
LEDGER = CHATGPT / "TUNEL" / "DO_CHATGPT" / "LEDGER_016.jsonl"
BRIDGE = CHATGPT / "IALD_ORQUESTRACAO_20260923" / "bridge.py"
PYTHON = Path(r"C:\Python314\python.exe")
JOBS = (
    ("a32abb36-8e3d-4651-9c4e-3841dda9e753", "local", "multimode_identifiability_local_mechanics", "REJECTED_WRONG_JACOBIAN_RANK_AND_DERIVATIVE"),
    ("45b2a2c5-04b8-4308-b7e2-3fc3d36edfc2", "mimo", "multimode_identifiability_draft", "ALGEBRA_CONSISTENT_WITH_LOCAL_GRID_NUMERICS_NOT_DATA_IDENTIFIABILITY"),
)


def sha_bytes(blob):
    return hashlib.sha256(blob).hexdigest()


def atomic_existing(path, raw):
    old = path.read_bytes()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    backup = path.with_name(path.name + ".bak_" + stamp)
    with backup.open("xb") as stream:
        stream.write(old)
        stream.flush()
        os.fsync(stream.fileno())
    assert backup.read_bytes() == old
    temp = path.with_name(path.name + ".tmp_" + stamp)
    with temp.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    os.replace(temp, path)
    assert path.read_bytes() == raw
    return backup


def get(job):
    call = subprocess.run([str(PYTHON), "-X", "utf8", str(BRIDGE)],
                          input=json.dumps({"operation": "get", "job_id": job}, ensure_ascii=False),
                          text=True, encoding="utf-8", capture_output=True, check=True)
    return json.loads(call.stdout)


def main():
    old = LEDGER.read_bytes()
    entries = []
    audit = []
    for job_id, provider, lemma, scientific_status in JOBS:
        item = get(job_id)
        assert item["stage"] == "completed"
        execution = item["execution"]
        assert execution["status"] == "result_ready"
        result = execution["result"]
        if provider == "mimo":
            assert float(result["cost_estimate_usd"]) < .5
        row = dict(at=datetime.now(timezone.utc).isoformat(),
                   event="ORDEM016_PROVIDER_CALL_AUDIT", branch="B_T10",
                   lemma=lemma, role="draft", provider=provider,
                   request_id=item["request_id"], job_id=job_id,
                   status="completed", prompt_sha256=sha_bytes(item["prompt"].encode()),
                   response_sha256=sha_bytes(result["text"].encode()),
                   usage=result.get("usage"), cost_estimate_usd=result.get("cost_estimate_usd"),
                   scientific_status=scientific_status, receipt_sha256=None,
                   receipt_note="queue receipt not opened directly; bridge verified completed result")
        if item["request_id"].encode() in old:
            raise ValueError("Ledger request already present")
        entries.append(row)
        audit.append({k: row[k] for k in ("job_id", "request_id", "provider", "response_sha256", "usage", "cost_estimate_usd", "scientific_status")})
    out = HERE / "T10_MODEL_ADVISORY_AUDIT.json"
    body = dict(status="SOURCE_ARBITRATES_MODEL_ADVICE", created_utc=datetime.now(timezone.utc).isoformat(),
                rank_grid_sha256=sha_bytes((HERE / "T10_APRIME_SPECTRAL_RANK.json").read_bytes()),
                local_jacobian_correction="single 220 rows (f220,tau220) have generic rank 2; d tau220(1+d)/dd = tau220, never tau220/220",
                multimode_condition="rank 3 iff one 3x3 minor containing tau220 row is nonzero; checked numerically for 220+440 at registered spin",
                data_identifiability="OPEN: mode amplitude, noise and posterior not in spectral grid",
                calls=audit, gate_changed=False)
    raw = (json.dumps(body, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    with out.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert out.read_bytes() == raw
    update = old + b"".join((json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n").encode() for row in entries)
    backup = atomic_existing(LEDGER, update)
    print(json.dumps({"audit_sha256": sha_bytes(raw), "ledger_sha256": sha_bytes(update),
                      "backup": str(backup), "mimo_cost_usd": audit[1]["cost_estimate_usd"]}))


if __name__ == "__main__":
    main()
