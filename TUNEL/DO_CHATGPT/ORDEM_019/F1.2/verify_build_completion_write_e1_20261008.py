"""Exercise only the result-writing block of build_completion.py in isolation."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "sandbox" / "build_completion.py"
SEALED = ROOT / "sandbox" / "BUILD_COMPLETION_RESULT.json"
OUT = ROOT / "VALIDACAO_BUILD_COMPLETION_E1_20261008.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if OUT.exists():
        raise FileExistsError(OUT)
    sealed_before = sha(SEALED)
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    start = next(i for i, node in enumerate(tree.body)
                 if isinstance(node, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == "result_path" for t in node.targets))
    block = ast.Module(body=tree.body[start:], type_ignores=[])
    code = compile(ast.fix_missing_locations(block), str(SOURCE), "exec")
    with tempfile.TemporaryDirectory(prefix="f12_e1_write_") as directory:
        scratch = Path(directory)
        context = {"SANDBOX": scratch, "results": [{"step": "isolated", "returncode": 0}],
                   "Path": Path, "os": os, "json": json, "tempfile": tempfile}
        exec(code, context)
        result = scratch / "BUILD_COMPLETION_RESULT.json"
        first = result.read_bytes()
        repeated_refused = False
        try:
            exec(code, context)
        except FileExistsError:
            repeated_refused = True
        if not repeated_refused or result.read_bytes() != first:
            raise RuntimeError("second write did not fail closed")
        if list(scratch.glob("*.tmp")):
            raise RuntimeError("temporary file remains")
        observed = {
            "first_write_bytes": len(first),
            "first_write_sha256": hashlib.sha256(first).hexdigest(),
            "repeat_refused_FileExistsError": repeated_refused,
            "existing_bytes_preserved": True,
            "temporary_files_remaining": 0,
        }
    sealed_after = sha(SEALED)
    if sealed_before != sealed_after:
        raise RuntimeError("sealed result changed")
    data = {
        "schema": "iald.f1_2.e1.exclusive_atomic_write_check.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(SOURCE), "source_sha256": sha(SOURCE),
        "sealed_result": str(SEALED), "sealed_before_after_sha256": sealed_after,
        "scope": "AST-derived final writer only; no Lean, kernel or original result rewrite",
        "observed": observed,
        "exit": 0,
    }
    with OUT.open("xb") as stream:
        stream.write((json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
