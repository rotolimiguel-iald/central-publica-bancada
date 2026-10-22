"""Create new retry scripts; retain every source, result and failed attempt."""
from pathlib import Path
import ast
import datetime as dt
import hashlib
import json

HERE = Path(__file__).resolve().parent
OLD = r"C:\IALD\Central de Patentes\work\rite394_20261015\r2"
NEW = r"C:\IALD\Central de Patentes\work\rite394_20261015\r3"
records = []

def emit(source, target, changes):
    p = HERE / source
    raw = p.read_bytes()
    text = raw.decode("utf-8")
    for a, b in changes:
        if a not in text:
            raise RuntimeError(f"Expected exact source fragment absent: {a}")
        text = text.replace(a, b)
    ast.parse(text)
    dest = HERE / target
    payload = text.encode("utf-8")
    with dest.open("xb") as f:
        f.write(payload)
    assert dest.read_bytes() == payload
    records.append({"source": str(p), "source_sha256": hashlib.sha256(raw).hexdigest(),
                    "path": str(dest), "sha256": hashlib.sha256(payload).hexdigest()})

emit("prepare_assets_r4.py", "prepare_assets_r5.py", [
    (OLD, NEW), ("PREPARATION_PLAN_R4", "PREPARATION_PLAN_R5"),
    ("ASSET_INVENTORY_R4", "ASSET_INVENTORY_R5"),
    ("COPY_MANIFEST_R4", "COPY_MANIFEST_R5"),
    ("PREPARATION_RECEIPT_R4", "PREPARATION_RECEIPT_R5")])
emit("prepare_environment_r3.py", "prepare_environment_r4.py", [
    (OLD, NEW), ("ENVIRONMENT_PREFLIGHT_R3", "ENVIRONMENT_PREFLIGHT_R4")])
emit("preflight_engine_r2.py", "preflight_engine_r3.py", [
    ('ROOT = OLD / "r2"', 'ROOT = OLD / "r3"'),
    ("ENVIRONMENT_PREFLIGHT_R3", "ENVIRONMENT_PREFLIGHT_R4"),
    ("sitecustomize_rite_r2.py", "sitecustomize_rite_r3.py")])
emit("launch_full_rite_r2.py", "launch_full_rite_r3.py", [
    (OLD, NEW), ("PREPARATION_RECEIPT_R4", "PREPARATION_RECEIPT_R5"),
    ("ENVIRONMENT_PREFLIGHT_R3", "ENVIRONMENT_PREFLIGHT_R4"),
    ("sitecustomize_rite_r2.py", "sitecustomize_rite_r3.py"),
    ("UM_ABSOLUTO_SEAL.json", "um_absoluto_selo.json")])

plan = {
    "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    "unit": "F1.FECHO_20261015", "claim_event": 845, "scope_event": 849,
    "purpose": "Additive environment retry after extended DOS path containment false refusals",
    "prior_attempt_preserved": OLD, "retry_sandbox": NEW,
    "scripts": records,
    "candidate_unchanged": True, "full_main_unmodified": True,
    "copy_source": "Read-only canonical admitted cache, kernel/cache, packages, and existing MiKTeX metadata; physical byte copies with hashes and no links",
    "guard_change": "Normalize extended DOS/UNC spelling, preserve strict containment and local junction resolution; no network or additional subprocess permissions",
    "guard_regression": {"path": str(HERE / "GUARD_PATHS_R3B_RESULT.json"),
       "sha256": hashlib.sha256((HERE / "GUARD_PATHS_R3B_RESULT.json").read_bytes()).hexdigest()},
    "DES_Y3": {"source": "candidate_r3/um.py:149321-149333", "canonical_cache_absent": True,
       "copied_cache_absent": True, "acquisition": "explicitly outside sealed rite in source docstring",
       "policy": "DNS remains blocked; absent_offline is retained and reported; no new observed data or fabricated cache"},
    "scientific_success_not_claimed": True,
    "wait_for_prior_process_terminal_before_launch": True,
}
with (HERE / "PLANO_RITO_REAL_R3.json").open("x", encoding="utf-8") as f:
    json.dump(plan, f, ensure_ascii=False, indent=2)
print(json.dumps({"created_scripts": len(records), "plan": "PLANO_RITO_REAL_R3.json"}))
