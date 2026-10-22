"""Verify the original MiMo response against the F1.3 copied body."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile


UNIT = Path(__file__).resolve().parent
ORIGIN = Path(
    r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\state\handoffs"
    r"\befba7c0-456a-469a-9751-32ebb1a08c67_mimo_declared_response.md"
)
COPY = UNIT / "MIMO_PARECER_BRUTO.md"
TARGET = UNIT / "MIMO_RECIBO_ERRATA_V3.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    original = ORIGIN.read_bytes()
    copy = COPY.read_bytes()
    header_size = len(original) - len(copy)
    if header_size != 116 or original[header_size:] != copy:
        raise SystemExit("FAIL_CLOSED: copied body differs from origin after the expected header")
    header = original[:header_size].decode("utf-8")
    if "DECLARADO" not in header:
        raise SystemExit("FAIL_CLOSED: original header has no DECLARADO label")
    report = {
        "unit": "F1.3",
        "purpose": "additive provenance correction; original receipt remains unchanged",
        "origin_path": str(ORIGIN),
        "origin_bytes": len(original),
        "origin_sha256": digest(original),
        "copied_body_path": str(COPY),
        "copied_body_bytes": len(copy),
        "copied_body_sha256": digest(copy),
        "omitted_header_bytes": header_size,
        "omitted_header_utf8": header,
        "body_equals_origin_after_header": True,
        "provider_statute": "DECLARADO_PROVIDER_COMPLETED_NOT_FACT_CHECKED",
        "new_provider_call": False,
    }
    if TARGET.exists():
        raise SystemExit("FAIL_CLOSED: provenance correction already exists")
    payload = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with NamedTemporaryFile(dir=UNIT, prefix=".mimo_v3_", suffix=".tmp", delete=False) as temp:
        temp.write(payload)
        temp.flush()
        os.fsync(temp.fileno())
        temp_path = Path(temp.name)
    if temp_path.stat().st_size != len(payload):
        temp_path.unlink(missing_ok=True)
        raise SystemExit("FAIL_CLOSED: incomplete temporary file")
    os.replace(temp_path, TARGET)
    if TARGET.read_bytes() != payload:
        raise SystemExit("FAIL_CLOSED: provenance correction differs after replace")
    print(json.dumps({"path": str(TARGET), "sha256": digest(payload), "origin_sha256": digest(original)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
