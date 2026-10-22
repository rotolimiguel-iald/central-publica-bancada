"""Pin the additive F2.3 c1 receipt; never replace recorded evidence."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F2.3_F7.2_adendos")
RESULT = HERE / "RESULTADO_ADENDO_C1_F23_20261008_V3.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def item(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise RuntimeError(f"Missing evidence: {path}")
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def write_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise RuntimeError(f"Refusing to overwrite {path}")
    with tempfile.NamedTemporaryFile(
        dir=path.parent, prefix=".f23_result_", suffix=".tmp", delete=False
    ) as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    if temporary.read_bytes() != data:
        raise RuntimeError("Temporary result differs from intended bytes")
    os.rename(temporary, path)
    if path.read_bytes() != data:
        raise RuntimeError("Written result differs from intended bytes")


def main() -> None:
    original = HERE / "LiganteLeiCampoCurvo.lean"
    audited = HERE / "LiganteLeiCampoCurvoAuditoriaC1.lean"
    marker = b"set_option autoImplicit false"
    a, b = original.read_bytes(), audited.read_bytes()
    if a[a.index(marker):] != b[b.index(marker):]:
        raise RuntimeError("Proof body or imports differ between original and audited version")
    old_olean = HERE / "LiganteLeiCampoCurvoAuditoriaC1.olean"
    new_olean = HERE / "LiganteLeiCampoCurvoAuditoriaC1Rebuild_20261008.olean"
    if old_olean.read_bytes() != new_olean.read_bytes():
        raise RuntimeError("Rebuilt olean differs from the already recorded audited version")
    log = HERE / "BUILD_C1_ACT_V3_20261008.log"
    log_text = log.read_text(encoding="utf-8")
    for required in (
        "started_utc=", "ended_utc=", "elapsed_seconds=", "LEAN_PATH=",
        "exit_code=0", "compiler_transcript_begin", "compiler_transcript_end",
    ):
        if required not in log_text:
            raise RuntimeError(f"Build receipt omits {required}")
    transcript = log_text.split("compiler_transcript_begin", 1)[1].split(
        "compiler_transcript_end", 1
    )[0]
    if "sorryAx" in transcript or "error:" in transcript or "warning:" in transcript:
        raise RuntimeError("Successful compiler transcript is not clean")
    if transcript.count("depends on axioms:") != 2:
        raise RuntimeError("Expected two axiom reports")
    for name in ("propext", "Classical.choice", "Quot.sound"):
        if name not in transcript:
            raise RuntimeError(f"Axiom transcript omits {name}")
    evidence = [
        original, audited, HERE / "kernel/TGLExt/LiganteLeiCampoCurvoAuditoriaC1.lean",
        old_olean, new_olean, log, HERE / "build_f23_c1_act_20261008.py",
        HERE / "BUILD_FIRST_ATTEMPT.log", HERE / "BUILD_RAMOC.log",
        HERE / "BUILD_RAMOC_2.log", HERE / "ERRATA_RAMOC_SONDAS_C1_20261008.md",
        HERE / "RESULTADO_RESSALVAS_C1_F23_20261008.json",
        AUDIT / "AUDITORIA_F2_3_F7_2_adendos_C1_ae22d8a4.md",
        AUDIT / "f23/sandbox/AuditF23/SondasAdendoRamoC.lean",
    ]
    result = {
        "schema": "iald.f2_3.c1_adendo.v3",
        "unit": "F2.3",
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "status": "ENTREGUE_PARA_REAUDITORIA_C1",
        "reused_prior_work": [
            "Audited theorem source and its docstring-only side version already recorded",
            "Four memory corrections already appended under claimed F0.3, event 306",
            "Earlier actual build receipt retained; no evidence overwritten",
        ],
        "new_work": [
            "Fresh build act records actual UTC start and end, elapsed seconds, literal LEAN_PATH, command and exit 0",
            "Three historical attempts pinned; the last shows warnings, not a demonstrated compiler failure",
            "S-A, S-B, S-C and non-vacuity limitations stated beside the pinned branch C source",
        ],
        "checks": {
            "audited_proof_body_identical_to_original": True,
            "rebuilt_olean_byte_identical": True,
            "new_axiom_transcript_only_trio": True,
            "new_compiler_errors_or_warnings": 0,
            "branch_c_is_corollary": "REAL by c1 probe S-A",
            "wedge_point_label_has_no_geometric_weight": "REAL by c1 probe S-B",
            "fock_and_maxwell_inhabitants_exhibited": False,
        },
        "scope": {
            "temperature_candidate_audited_here": False,
            "kernel_of_nos_changed": False,
            "um_py_changed": False,
            "gate_effect": "NONE",
        },
        "artifacts": [item(path) for path in evidence],
    }
    data = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    write_new(RESULT, data)
    print(f"result={RESULT}\nresult_sha256={sha(RESULT)}\nartifacts={len(evidence)}")


if __name__ == "__main__":
    main()
