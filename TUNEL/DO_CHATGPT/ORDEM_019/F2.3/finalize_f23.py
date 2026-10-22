"""Fail-closed evidence packaging for the F2.3 sandbox Lean build."""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile


HERE = Path(__file__).resolve().parent
LEAN = HERE / "LiganteLeiCampoCurvo.lean"
COPY = HERE / "kernel/TGLExt/LiganteLeiCampoCurvo.lean"
OLEAN = HERE / "LiganteLeiCampoCurvo.olean"
LOG = HERE / "BUILD.log"
AX = HERE / "AXIOMAS.txt"
DIAG = HERE / "DIAGNOSTICO_TIPADO.md"
SOURCES = HERE / "FONTES_SHA256.json"
HASHES = HERE / "HASHES.json"
RESULT = HERE / "RESULTADO.json"
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def record(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def atomic_new(path: Path, payload: bytes) -> None:
    if path.exists():
        raise RuntimeError(f"FAIL_CLOSED: output exists: {path}")
    with NamedTemporaryFile(dir=path.parent, prefix=".f23_evidence_", suffix=".tmp", delete=False) as temp:
        temp.write(payload)
        temp.flush()
        os.fsync(temp.fileno())
        temporary = Path(temp.name)
    if temporary.stat().st_size != len(payload):
        temporary.unlink(missing_ok=True)
        raise RuntimeError("FAIL_CLOSED: short temp")
    os.replace(temporary, path)
    if path.read_bytes() != payload:
        raise RuntimeError("FAIL_CLOSED: post-write mismatch")


def main() -> None:
    if HASHES.exists() or RESULT.exists():
        raise RuntimeError("FAIL_CLOSED: evidence already finalized")
    src = LEAN.read_bytes()
    if src != COPY.read_bytes():
        raise RuntimeError("FAIL_CLOSED: sandbox copy differs from delivered source")
    if not OLEAN.exists() or OLEAN.stat().st_size == 0:
        raise RuntimeError("FAIL_CLOSED: compiled module missing")
    if re.search(rb"\b(sorry|admit|axiom)\b", src):
        raise RuntimeError("FAIL_CLOSED: prohibited source token")
    log = LOG.read_text(encoding="utf-8")
    if LOG.read_bytes() != AX.read_bytes():
        raise RuntimeError("FAIL_CLOSED: axioms transcript differs from build log")
    if re.search(r"\b(error|warning|sorryAx)\b", log, flags=re.I):
        raise RuntimeError("FAIL_CLOSED: error, warning or sorryAx in build log")
    observed = {}
    for name, bracket in re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]", log, flags=re.S):
        ax = {part.strip() for part in bracket.split(",")}
        if ax != ALLOWED:
            raise RuntimeError(f"FAIL_CLOSED: axioms outside trio for {name}: {sorted(ax)}")
        observed[name] = sorted(ax)
    required = {
        "ChatgptAudit.F23CurvedFieldLigand.NamedAtlasH3",
        "ChatgptAudit.F23CurvedFieldLigand.passage_h3_to_connected_smooth_atlas_einstein",
    }
    if set(observed) != required:
        raise RuntimeError(f"FAIL_CLOSED: unexpected #print axioms declarations: {sorted(observed)}")
    if not DIAG.exists() or not SOURCES.exists():
        raise RuntimeError("FAIL_CLOSED: independent source audit artifacts missing")
    source_doc = json.loads(SOURCES.read_text(encoding="utf-8"))
    if not source_doc:
        raise RuntimeError("FAIL_CLOSED: empty source manifest")
    files = [record(p) for p in (LEAN, COPY, OLEAN, LOG, AX, DIAG, SOURCES)]
    hash_doc = {
        "unit": "F2.3",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "algorithm": "sha256_bytes",
        "artifacts": files,
        "lean_source_equals_sandbox_copy": True,
        "build_log_equals_axioms_transcript": True,
        "original_sources": source_doc,
    }
    atomic_new(HASHES, (json.dumps(hash_doc, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    result = {
        "unit": "F2.3",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "ENTREGUE_PARA_AUDITORIA_C1",
        "statute": "REAL_CONDITIONAL_FORMAL_TERM_IN_SANDBOX__INPUT_NAMED_H3_BRIDGE",
        "anti_wall_branch": "C",
        "source_theorem": "TGLExt.Fundacao.the_post_lives_in_the_passage",
        "theorem": "ChatgptAudit.F23CurvedFieldLigand.passage_h3_to_connected_smooth_atlas_einstein",
        "proven_conclusion": "Under named H3 and explicit chart, matter-conservation and smooth-transition data, there exists a unique common cosmological constant with Einstein equation in every chart and coefficient 8*pi*G, eta=(4*G)^-1",
        "h3_limit": "hH3 : finite passage result -> all-point/all-null-direction atlas area law is entirely an input; since the passage result is proven under its premises, hH3 carries the missing physical bridge and is logically equivalent there to the named area law",
        "light_h3_limit": "lightH3 covers nullDir in the wedge, not every null direction or the curved atlas",
        "global_solution_claimed": False,
        "new_kernel_imported": False,
        "integration_owner": "claude-c1 at v392",
        "gate_changed": False,
        "build": {
            "tool": "Lean 4.31.0 direct module build on kernel source copy, with read-only prebuilt original dependency caches",
            "exit_code_observed_by_command_tool": 0,
            "olean_nonempty": True,
            "log_has_error_or_warning": False,
            "sorry_or_admit_or_new_axiom_in_source": False,
            "axioms": observed,
        },
        "hashes": record(HASHES),
        "artifacts": files,
        "next_action": "Attach evidence to board; c1 reviews and may integrate in v392",
    }
    atomic_new(RESULT, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"hashes": record(HASHES), "result": record(RESULT), "axioms": observed}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
