"""Build an evidence-only F1.3 v3 delivery manifest from files on disk."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile


UNIT = Path(__file__).resolve().parent
KERNEL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F1.3\AUDITORIA_F1_3_C1_20261007.md")
TARGET = UNIT / "RESULTADO_V3.json"
ARTIFACTS = [
    UNIT / "GRAFO_DEGRAUS_V3.md",
    UNIT / "SOURCE_PROBE_V3B.json",
    UNIT / "MIMO_RECIBO_ERRATA_V3.json",
    UNIT / "REVISAO_INTERNA_V3.md",
    UNIT / "MIMO_EXECUTION_RECEIPT.json",
    UNIT / "PARECER_MIMO_CONFERIDO.md",
    UNIT / "CONCILIACAO_F11_V376.md",
    UNIT / "GRAFO_DEGRAUS_REVISTO.md",
    AUDIT,
]


def record(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main() -> None:
    if TARGET.exists():
        raise SystemExit("FAIL_CLOSED: RESULTADO_V3.json already exists")
    refs = [record(path) for path in ARTIFACTS]
    pin = (KERNEL / "lean-toolchain").read_text(encoding="utf-8").strip()
    mathlib_head = subprocess.check_output(
        ["git", "-C", str(KERNEL / ".lake/packages/mathlib"), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    errata = json.loads((UNIT / "MIMO_RECIBO_ERRATA_V3.json").read_text(encoding="utf-8"))
    if not errata["body_equals_origin_after_header"] or errata["omitted_header_bytes"] != 116:
        raise SystemExit("FAIL_CLOSED: MiMo provenance correction invalid")
    result = {
        "unit": "F1.3",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PLAN_V3_READY_FOR_C1_REAUDIT",
        "statute": "REAL_DOCUMENTARY_PLAN; DERIVED_PROPOSED_D1A; OPEN_PHYSICAL_REALIZATION; DECLARADO_PROVIDER_REVIEW",
        "auditor_c1_prior_verdict": "V2_REPROVED_GRAPH; F11_V376_AND_LOCAL_MIMO_P1_CHECK_ACCEPTED",
        "artifacts": refs,
        "pin": {"lean_toolchain": pin, "mathlib_head": mathlib_head},
        "corrections": [
            "D0.5 is REAL, already measured in v391 and c1 sandbox",
            "D1a exits only with nonzero StandardSubspace H1 and modular group B0(-2pi*t)",
            "orbital H1-to-rapidity transport and boost intertwining are already proved in O16",
            "partial Fourier, physical J_W, and modular multiplier remain open in the same H1",
            "D.K rightWedge must be identified with the nonzero standard K(W_R)",
            "A1/A3/D4 and seven inventory themes are mapped with lines",
            "per-degree mathlib feasibility and conditional Araki/Fock shortcuts are explicit",
            "full MiMo origin hash and 116-byte omitted DECLARADO header are recorded",
        ],
        "first_new_constructive_target": "D1a.1 partial Fourier in rapidity on Lp Fib 2 momentumMeasure and physical J_W",
        "first_physical_exit": "D1a.3 nonzero standard right-wedge subspace and its modular group equality",
        "new_mimo_call": False,
        "new_lean_compilation_for_v3": False,
        "canonical_kernel_modified": False,
        "physical_core_constructed": False,
        "physical_corner_constructed": False,
        "gate_changed": False,
        "next_action": "c1 independent reaudit; only c1 may mark AUDITADA/FECHADA",
    }
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with NamedTemporaryFile(dir=UNIT, prefix=".f13_result_v3_", suffix=".tmp", delete=False) as temp:
        temp.write(payload)
        temp.flush()
        os.fsync(temp.fileno())
        temp_path = Path(temp.name)
    if temp_path.stat().st_size != len(payload):
        temp_path.unlink(missing_ok=True)
        raise SystemExit("FAIL_CLOSED: incomplete manifest")
    os.replace(temp_path, TARGET)
    if TARGET.read_bytes() != payload:
        raise SystemExit("FAIL_CLOSED: manifest differs after replace")
    print(json.dumps(record(TARGET), ensure_ascii=False))


if __name__ == "__main__":
    main()
