"""Read/hash/AST-only independent review. Never imports candidate modules."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
PACKAGE = ROOT / "f9_engine_assembly_integration_preparation"
OUT = Path(__file__).parent

def stamp():
    return datetime.now(timezone.utc).isoformat()

def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def atomic(path, obj):
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if path.exists():
        backup = path.with_name(path.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        before = path.read_bytes()
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    temp = path.with_name(path.name + ".tmp")
    temp.write_bytes(raw)
    assert temp.read_bytes() == raw and raw
    os.replace(temp, path)
    assert path.read_bytes() == raw

def check(path, expected, category):
    actual = pin(path)
    return {"category": category, **actual,
            "matches": all(actual[k] == expected[k] for k in ("bytes", "sha256")),
            "expected": {k: expected[k] for k in ("bytes", "sha256")}}

manifest = json.loads((PACKAGE / "MANIFESTO_PREPARACAO.json").read_bytes())
contract = json.loads((PACKAGE / "CONTRATO_WSL.json").read_bytes())
lineage = json.loads((PACKAGE / "SOURCE_LINEAGE.json").read_bytes())
inventory = json.loads((PACKAGE / "RUNTIME_INVENTORY.json").read_bytes())
initial = json.loads((OUT / "SNAPSHOT_INICIAL.json").read_bytes())
checks = []
checks += [check(PACKAGE / r["path"], r, "manifest_member") for r in manifest["files"]]
checks += [check(PACKAGE / r["relative_path"], r, "contract_local") for r in contract["local_pins"]]
checks += [check(Path(r["path"]), r, "lineage_source") for r in lineage["sources"]]
checks += [check(Path(lineage["request"]["path"]), lineage["request"], "request_lineage")]
checks += [check(Path(r["path"]), r, "initial_snapshot") for r in initial["files"]]
checks += [check(Path(r["path"]), r, "windows_runtime") for r in contract["windows_pins"]]
asts = []
for r in manifest["files"]:
    if r["path"].endswith(".py"):
        path = PACKAGE / r["path"]
        tree = ast.parse(path.read_bytes(), filename=str(path))
        asts.append({"relative_path": r["path"], "parsed": True,
                     "imports": [{"line": node.lineno, "source": ast.unparse(node)}
                                 for node in ast.walk(tree)
                                 if isinstance(node, (ast.Import, ast.ImportFrom))]})
pins = {r["path"]: r for r in inventory["pins"]}
linux_crosscheck = []
for r in contract["linux_pins"]:
    x = pins.get(r["path"])
    linux_crosscheck.append({"path": r["path"], "inventory_entry_exists": x is not None,
                            "matches": x is not None and all(x[k] == r[k] for k in ("bytes", "sha256"))})
py_sources = [s for s in pins if s.endswith(".py")]
missing_cache = []
for s in py_sources:
    parent, name = s.rsplit("/", 1)
    cache = parent + "/__pycache__/" + name[:-3] + ".cpython-312.pyc"
    if cache not in pins:
        missing_cache.append({"source": s, "expected_cache": cache})
supplements = [pin(PACKAGE / n) for n in ("NOTA_INTEGRACAO.md", "VERIFICACAO_FINAL_ESTATICA.json")
               if (PACKAGE / n).exists()]
terminal_markers = {n: (PACKAGE / n).exists() for n in
                    ("AUTORIZACAO_ROOT.json", "CLAIM.json", "RUN", "RESULT.json")}
result = {
    "schema": "INDEPENDENT_F9_ENVELOPE_STATIC_METADATA_V1", "at": stamp(),
    "scope": "READ_HASH_AST_ONLY_NO_CANDIDATE_IMPORT_NO_WSL_NO_SOLVER_NO_OBSERVED_DATA",
    "manifest": pin(PACKAGE / "MANIFESTO_PREPARACAO.json"),
    "contract": pin(PACKAGE / "CONTRATO_WSL.json"),
    "checks": checks, "check_count": len(checks),
    "all_checks_match": all(r["matches"] for r in checks),
    "unique_checked_paths": len({r["path"] for r in checks}),
    "AST": asts, "AST_file_count": len(asts),
    "linux_contract_vs_inventory": linux_crosscheck,
    "inventory_summary": {"pins": len(inventory["pins"]), "unique_paths": len(pins),
                          "python_sources": len(py_sources),
                          "pyc_files": sum(s.endswith(".pyc") for s in pins),
                          "sources_without_standard_cache_pin": missing_cache,
                          "unresolved_native_dependencies": inventory["unresolved_native_dependencies"],
                          "all_5074_runtime_bytes_rehashed_here": False,
                          "scope_limit": "Inventory is metadata, not observed import trace. Selected runtime source hashes are independently read in RUNTIME_SOURCE_READS.json."},
    "supplemental_documents_outside_initial_manifest": supplements,
    "terminal_marker_existence_only": terminal_markers,
    "candidate_imports": 0, "candidate_controls": 0, "Linux_processes_started": 0,
    "scientific_calls": 0, "authorization_or_claim_written": False,
}
atomic(OUT / "STATIC_METADATA_RESULT.json", result)
print(json.dumps({"receipt": pin(OUT / "STATIC_METADATA_RESULT.json"),
                  "checks": len(checks), "all_match": result["all_checks_match"],
                  "unique_paths": result["unique_checked_paths"], "ast_files": len(asts),
                  "linux_inventory_all_match": all(r["matches"] for r in linux_crosscheck),
                  "terminal_markers": terminal_markers}, ensure_ascii=False))
