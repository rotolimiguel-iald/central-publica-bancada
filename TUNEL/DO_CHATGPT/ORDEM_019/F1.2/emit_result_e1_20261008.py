"""Seal the bookkeeping-only F1.2.E1 correction as new evidence."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "RESULTADO_ERRATA_ESCRITURACAO_E1_F12_20261008.json"


def pin(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def main() -> None:
    if OUT.exists():
        raise FileExistsError(OUT)
    paths = [
        ROOT / "ERRATA_MAPA_ALVO_SEQ728_F12_20261008_INPUT.json",
        ROOT / "MEMORY_ERRATA_E1_RECEIPT_20261008.json",
        ROOT / "append_memory_errata_e1_20261008.py",
        ROOT / "sandbox" / "build_completion.py",
        ROOT / "sandbox" / "build_completion.py.bak_20261008_110954_339",
        ROOT / "sandbox" / "BUILD_COMPLETION_RESULT.json",
        ROOT / "VALIDACAO_BUILD_COMPLETION_E1_20261008.json",
        ROOT / "verify_build_completion_write_e1_20261008.py",
        Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F1.2\AUDITORIA_F1_2_C1_a5aa4480.md"),
    ]
    expected = {
        "build_completion.py": "a73b808d34ec47b23adb399488684a6951ad238741e9dd83b6bd98253f7ecd78",
        "build_completion.py.bak_20261008_110954_339": "20c7594c09eb4a8d24a7ba7fa46b38b4e7263e08bd76d11ae804975be41b6a7a",
        "BUILD_COMPLETION_RESULT.json": "b7fc3cb68654a74aa62e549f1d6869f410de421b1ffeda2dda8bf0aebadde078",
        "AUDITORIA_F1_2_C1_a5aa4480.md": "ec1040a05d51cde22f3cb6cd6ffe3674049084eae0208397aa2ff36096bcffb5",
    }
    for path in paths:
        if path.name in expected and pin(path)["sha256"] != expected[path.name]:
            raise RuntimeError(f"pinned source changed: {path}")
    memory = json.loads((ROOT / "MEMORY_ERRATA_E1_RECEIPT_20261008.json").read_text(encoding="utf-8"))
    for record in memory["targets"]:
        if pin(Path(record["before"]["path"]))["sha256"] != record["before"]["sha256"]:
            raise RuntimeError("memory backup changed")
        if pin(Path(record["after"]["path"]))["sha256"] != record["after"]["sha256"]:
            raise RuntimeError("memory target changed")
    test = json.loads((ROOT / "VALIDACAO_BUILD_COMPLETION_E1_20261008.json").read_text(encoding="utf-8"))
    if not test["observed"]["repeat_refused_FileExistsError"] or test["observed"]["temporary_files_remaining"]:
        raise RuntimeError("writer validation did not pass")
    data = {
        "schema": "iald.f1_2.e1.bookkeeping_errata.v1",
        "unit": "F1.2.E1",
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "original_unit": {"id": "F1.2", "status": "FECHADA", "closed_event": 287},
        "new_unit_created_event": 343,
        "new_unit_claimed_event": 344,
        "nos_vivo": "F1.2 consulted; F1.2.E1 not yet in graph immediately after creation",
        "map_errata": {"seq": 853, "corrige": 728, "historical_wrong_target_in_seq_823": 716},
        "memory": "four named surfaces appended with byte backups and signature codex-gerente-tgl",
        "trace_of_positiveUnit": "REAL per c1 S6 and prior skeptic C9; old OPEN label corrected beside",
        "writer": "temporary in same directory, fsync, size check, exclusive os.link, byte check; sealed result unchanged",
        "writer_validation": "isolated final block: first write passed, second refused, no temp residual",
        "scope": {"lean_rebuilt": False, "kernel_changed": False, "um_py_changed": False, "gate_effect": "NONE"},
        "artifacts": [pin(path) for path in paths],
    }
    with OUT.open("xb") as stream:
        stream.write((json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(pin(OUT), ensure_ascii=False))


if __name__ == "__main__":
    main()
