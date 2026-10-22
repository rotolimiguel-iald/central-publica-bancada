"""Append the audited R3 delivery note to four memories after local review.

This script is prepared under F3.1/F3.2 claims. It is not a publication step.
Run only after both R3 results have been independently checked.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile


BASE = Path(r"C:\IALD\Central de Patentes")
SURFACES = (
    BASE / "memory" / "TGL_ATLAS.md",
    BASE / "memory" / "TGL_INDICE_VIVO.md",
    BASE / "memory" / "TGL_CORE_MEMORY.md",
    BASE / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_019" / "AVISO_GERENCIA.md",
)
MARKER = "<!-- F31_F32_R3_C1_REVIEW_PENDING_20261008 -->"


def digest(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    if not raw:
        raise ValueError(f"empty evidence: {path}")
    return {"path": str(path.resolve()), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def append_one(path: Path, payload: bytes, stamp: str) -> dict[str, object]:
    old = path.read_bytes()
    if not old or MARKER.encode("utf-8") in old:
        raise ValueError(f"empty or already updated memory: {path}")
    backup = path.with_name(path.name + ".bak_" + stamp)
    with backup.open("xb") as stream:
        stream.write(old)
        stream.flush()
        os.fsync(stream.fileno())
    if backup.read_bytes() != old:
        raise IOError(f"backup mismatch: {backup}")
    separator = b"" if old.endswith((b"\n", b"\r")) else b"\n"
    new = old + separator + payload
    handle, temporary_name = tempfile.mkstemp(prefix=path.name + ".tmp_", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(new)
            stream.flush()
            os.fsync(stream.fileno())
        if temporary.stat().st_size != len(new):
            raise IOError(f"temporary size mismatch: {temporary}")
        os.replace(temporary, path)
        actual = path.read_bytes()
        if len(actual) <= len(old) or not actual.startswith(old) or actual != new:
            shutil.copyfile(backup, path)
            raise IOError(f"append verification failed; restored backup: {path}")
    finally:
        temporary.unlink(missing_ok=True)
    return {"path": str(path), "backup": str(backup), "before_sha256": hashlib.sha256(old).hexdigest(),
            "after_sha256": hashlib.sha256(new).hexdigest(), "before_bytes": len(old), "after_bytes": len(new)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--f31-result", type=Path, required=True)
    parser.add_argument("--f32-result", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    f31 = digest(args.f31_result)
    f32 = digest(args.f32_result)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    paragraph = (
        "\n\n" + MARKER + "\n"
        "### 08/10/2026 — Fase 9, F3.1/F3.2 R3 [REAL — entrega local; auditoria c1 pendente]\n"
        "Em nome de codex-gerente-tgl, sob as reivindicações F3.1 evento 362 e F3.2 evento 363: "
        "a R3 aditiva da V2 e do gate/runner V1.x foi entregue para conferência. "
        "A V2 permanece RASCUNHO_NAO_CONGELADO; F3.4, X13/NAT-22, D-J e D-H seguem pendentes. "
        "A admissão das fontes, o congelamento, a abertura de dado observado, qualquer veredito da natureza "
        "e qualquer mudança de gate não ocorreram nesta entrega. O lnB contra o fundo livre e as famílias "
        "adicionais têm alcance somente sintético até auditoria. "
        f"Evidências lidas por script: F3.1 {f31['path']} ({f31['bytes']} bytes, sha256 {f31['sha256']}); "
        f"F3.2 {f32['path']} ({f32['bytes']} bytes, sha256 {f32['sha256']}). "
        "[DECLARADO] A c1 ainda não auditou a R3; nenhum resultado é promovido ao cânone por esta nota.\n"
    )
    payload = paragraph.encode("utf-8")
    for path in SURFACES:
        if not path.is_file():
            raise FileNotFoundError(path)
        if MARKER.encode("utf-8") in path.read_bytes():
            raise ValueError(f"marker already present: {path}")
    if args.receipt.exists():
        raise FileExistsError(args.receipt)
    updates = [append_one(path, payload, stamp) for path in SURFACES]
    receipt = {"marker": MARKER, "f31_result": f31, "f32_result": f32, "updates": updates,
               "status": "R3_LOCAL_DELIVERY_C1_AUDIT_PENDING"}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with args.receipt.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
