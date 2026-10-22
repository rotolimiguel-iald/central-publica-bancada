"""Append the signed c1 Temperature errata with an immediate byte backup."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile
from datetime import datetime


ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "ADENDO_TEMPERATURA_DIAGNOSTICO.md"
ENTRY = ROOT / "ADENDO_TEMPERATURA_ERRATA_C1_ENTRY_20261008.md"
PRIOR_MANIFEST = ROOT / "HASHES_TEMPERATURA.json"
RECEIPT = ROOT / "ADENDO_TEMPERATURA_ERRATA_C1_RECEIPT_20261008.json"
MARKER = b"Errata ao lado da auditoria c1 da Temperatura"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_exclusive(path: Path, payload: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


if __name__ == "__main__":
    if RECEIPT.exists():
        raise FileExistsError(RECEIPT)
    before = TARGET.read_bytes()
    expected = json.loads(PRIOR_MANIFEST.read_text(encoding="utf-8"))["files"][TARGET.name]["sha256"]
    if digest(before) != expected or MARKER in before:
        raise RuntimeError("Prior pinned bytes differ or this errata is already present")
    entry = ENTRY.read_bytes()
    newline = b"\r\n" if before.count(b"\r\n") > before.count(b"\n") // 2 else b"\n"
    entry = entry.replace(b"\r\n", b"\n").replace(b"\n", newline)
    if not entry.startswith(newline) or MARKER not in entry:
        raise RuntimeError("Entry is missing its leading separator or marker")
    after = before + entry
    backup = TARGET.with_name(TARGET.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    write_exclusive(backup, before)
    if backup.read_bytes() != before:
        raise RuntimeError("Immediate byte backup differs from the pinned prior state")
    with tempfile.NamedTemporaryFile(dir=ROOT, prefix=".adendo_temperatura_c1_", suffix=".tmp", delete=False) as stream:
        stream.write(after)
        stream.flush()
        os.fsync(stream.fileno())
        temp = Path(stream.name)
    if temp.read_bytes() != after or TARGET.read_bytes() != before:
        raise RuntimeError("Temporary payload or original changed before replace")
    os.replace(temp, TARGET)
    if TARGET.read_bytes() != after or not after.startswith(before) or len(after) <= len(before):
        os.replace(backup, TARGET)
        raise RuntimeError("Append verification failed; prior state restored")
    receipt = {
        "unit": "F2.3",
        "mode": "append_only_with_immediate_byte_backup",
        "target": str(TARGET),
        "backup": str(backup),
        "entry": str(ENTRY),
        "before_bytes": len(before),
        "before_sha256": digest(before),
        "backup_sha256": digest(backup.read_bytes()),
        "entry_sha256": digest(ENTRY.read_bytes()),
        "after_bytes": len(after),
        "after_sha256": digest(after),
        "prefix_preserved": True,
    }
    write_exclusive(RECEIPT, (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(receipt, ensure_ascii=False))
