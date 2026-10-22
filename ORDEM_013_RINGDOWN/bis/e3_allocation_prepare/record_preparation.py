"""Record static source hashes and parse-only checks; never run the renderer."""
import ast
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
ROOT = BASE.parent
SOURCES = [
    ROOT / "TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md",
    *[BASE / "bis/e2_code" / name for name in (
        "registration_guard.py", "pe_runner.py", "injection_design.py", "strain_io.py",
        "blinding.py", "run_controlled.py", "remnant_conversion.py")],
]
ARTIFACTS = ["CONTRACT_AND_CHECKLIST.md", "CONTRACT_SCHEMA.json", "GENERATOR_INPUT.md",
             "render_allocation_candidates.py", "record_preparation.py"]


def describe(path):
    path = path.resolve()
    if not path.is_relative_to(ROOT) or path.stat().st_size > 25_000_000:
        raise ValueError("Source outside scope/over size cap")
    raw = path.read_bytes()
    if len(raw) > 25_000_000:
        raise ValueError("File grew beyond cap")
    result = {"relative_to_Chatgpt": path.relative_to(ROOT).as_posix(),
              "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    text = raw.decode("utf-8-sig")
    if path.suffix == ".py":
        tree = ast.parse(text, filename=str(path))
        result["function_lines"] = {node.name: node.lineno for node in tree.body
                                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    elif path.name.startswith("ORDEM_013BIS_"):
        result["contract_lines"] = {key: [i for i, line in enumerate(text.splitlines(), 1)
                                          if line.startswith("- **" + key + " —")]
                                    for key in ("E3.2", "E3.3")}
    return result


def main():
    target = HERE / "PREPARATION_RECEIPT.json"
    if target.exists():
        raise FileExistsError("Receipt is immutable; use a separately reviewed successor")
    sources = [describe(path) for path in SOURCES]
    artifacts = [describe(HERE / name) for name in ARTIFACTS]
    schema = json.loads((HERE / "CONTRACT_SCHEMA.json").read_text(encoding="utf-8"))
    if len(schema["prior_names_exact"]) != 16 or len(set(schema["prior_names_exact"])) != 16:
        raise ValueError("Wrong prior inventory")
    renderer = ast.parse((HERE / "render_allocation_candidates.py").read_text(encoding="utf-8"))
    modules = []
    for node in ast.walk(renderer):
        if isinstance(node, ast.Import):
            modules.extend(item.name for item in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.append(node.module)
    allowed = {"argparse", "hashlib", "json", "math", "os", "re", "datetime", "pathlib"}
    if not set(modules) <= allowed:
        raise ValueError("Unexpected renderer import")
    for before in sources:
        after = describe(ROOT / before["relative_to_Chatgpt"])
        if before["sha256"] != after["sha256"]:
            raise ValueError("Source changed during static receipt")
    receipt = {
        "status": "PREPARATION_ONLY_NO_ALLOCATION_NO_SCIENCE",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Only bis/e3_allocation_prepare written; no frozen source edits",
        "sources": sources, "artifacts": artifacts,
        "checks": {
            "source_size_cap_bytes": 25_000_000,
            "all_sources_inside_Chatgpt": True,
            "source_hashes_stable_during_receipt": True,
            "python_AST_parse_only": True, "prior_inventory_unique_16": True,
            "renderer_imports_stdlib_only_static": sorted(set(modules)),
            "renderer_executed": False, "renderer_functional_tests": "NOT_RUN",
            "production_imports": False, "active_registration_checked": False,
            "pilot_cost_read": False, "posterior_strain_waveform_reads": False,
            "candidate_jobs_or_allocation_emitted": False,
            "independent_review": "OPEN"
        },
        "axioms": "N/A", "theorems": 0,
        "all_written_files": [str(HERE / name) for name in ARTIFACTS] + [str(target)],
        "receipt_self_hash": "Not embedded; compute externally from final bytes"
    }
    raw = (json.dumps(receipt, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    pending = target.with_name(target.name + ".pending")
    with pending.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    if pending.stat().st_size != len(raw):
        raise OSError("Incomplete receipt")
    os.link(pending, target)
    pending.unlink()
    print(json.dumps({"receipt": str(target), "sha256": hashlib.sha256(raw).hexdigest(),
                      "written_files": receipt["all_written_files"], "checks": receipt["checks"]}))


if __name__ == "__main__":
    main()
