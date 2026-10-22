"""Pin the environment-only retry after real engine preflight."""
from pathlib import Path
import hashlib
import json
import datetime as dt

HERE = Path(__file__).resolve().parent
ROOT = Path(r"C:\IALD\Central de Patentes\work\rite394_20261015\r2")
def rec(p):
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size}
engine = json.loads((ROOT / "ENGINE_PREFLIGHT_RECEIPT.json").read_text(encoding="utf-8"))
assert engine["passed"] and len(engine["engine_selftest"]["checks"]) == 8
logs = [json.loads(line) for p in (ROOT / "environment/guard_logs/preflight").glob("*.jsonl")
        for line in p.read_text(encoding="utf-8").splitlines()]
assert not any(x["kind"] == "REFUSAL" and x["pid"] == engine["pid"] for x in logs)
record = {
    "time_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    "unit": "F1.FECHO_20261015", "claim_event": 845, "short_sandbox_scope_event": 849,
    "status": "READY_FOR_REAL_FULL_RITE_AFTER_ENGINE_PREFLIGHT",
    "root": str(ROOT), "candidate": rec(ROOT / "um.py"),
    "previous_attempt": rec(HERE / "FIRST_ATTEMPT_INTERRUPTION.json"),
    "original_plan": rec(HERE / "PLANO_RITO_REAL_R1.json"),
    "environment_change_only": ["Allow exact readonly cmd.exe /c ver used by platform", "Allow missing rocm-sdk path --root to raise the natural FileNotFoundError caught by Triton", "Local Triton/TorchInductor cache directories", "Unbuffered stdout"],
    "checks": {"real_engine_checks_passed": 8, "engine_guard_refusals": 0, "dependency_probes_passed": 7, "guard_negative_controls_passed": 3},
    "receipts": [rec(ROOT / name) for name in ["PREPARATION_RECEIPT_R4.json", "ENVIRONMENT_PREFLIGHT_R3.json", "GUARD_PREFLIGHT.json", "ENGINE_PREFLIGHT_RECEIPT.json"]],
    "scripts": [rec(HERE / name) for name in ["prepare_assets_r4.py", "prepare_environment_r3.py", "sitecustomize_rite_r2.py", "preflight_engine_r2.py", "launch_full_rite_r2.py"]],
    "execution": "Actual unmodified candidate main, stdin 1, whole existing rite including strict full Lake build/Audit and destructive negative selftest only in sandbox; no baseline-core injection, no skipped flags or reduced corpus.",
    "data_scope": "Fresh repeat of existing admitted historical calculations; Fase9 frozen function on old saved input only; v376 reads the Coma revelation already opened 19-Aug; void/KiDS replay admitted data. No new observed data, new Fase9 composite, d72 approval or scientific opening.",
    "resource_scope": "Existing quantum-pillar cache replay with current E1-E8 recheck; full GPU recomputation refused; production Llama remains running.",
    "containment_scope": "Python audit hook blocks external writes/network/arbitrary processes. Native Lean/Lake/MiKTeX use pinned paths, local copies/config and offline settings; this is not OS-level containment.",
    "gate_or_publication_changed": False,
}
raw = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode()
with (HERE / "PLANO_RITO_REAL_R2.json").open("xb") as f:
    f.write(raw)
print(json.dumps({"ready": True, "plan_sha256": hashlib.sha256(raw).hexdigest()}))
