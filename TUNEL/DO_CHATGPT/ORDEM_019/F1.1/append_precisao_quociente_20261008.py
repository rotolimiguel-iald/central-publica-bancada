"""Append a type-accurate clarification to the fifth F1.1 layer."""

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.1")
FILE = BASE / "INVENTARIO.md"
RECEIPT = BASE / "RESULTADO_PRECISAO_QUOCIENTE_20261008.json"
MARKER = "<!-- F11_QUINTA_CAMADA_PRECISAO_QUOCIENTE_20261008 -->"
NOTE = """

<!-- F11_QUINTA_CAMADA_PRECISAO_QUOCIENTE_20261008 -->

[ERRATA AO LADO — precisão do tipo] Na primeira linha da tabela da quinta camada, leia «`polar_descends_injectively_iff` **caracteriza a existência** da leitura injetiva do quociente: sob `radius > 0` e `κ ≠ 0`, `∃ F` fiel se e somente se `κP = ±2π`». O lema não fornece `F` sob a positividade do raio sozinha. Esta precisão não altera as outras classes nem supõe um estado KMS.
"""


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    before = FILE.read_bytes()
    if sha(before) != "0f864bf7a92e20688c202b4542a9764ddd5b62d3ce0b9dc0057962c9cbb11069":
        raise RuntimeError("Unexpected fifth-layer revision")
    if MARKER.encode() in before:
        raise RuntimeError("Clarification already present")
    sep = "\r\n" if before.count(b"\r\n") > before.count(b"\n") / 2 else "\n"
    after = before + NOTE.replace("\n", sep).encode("utf-8")
    backup = FILE.with_name(FILE.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    with backup.open("xb") as f:
        f.write(before)
        f.flush()
        os.fsync(f.fileno())
    if backup.read_bytes() != before or FILE.read_bytes() != before:
        raise RuntimeError("Backup or compare-and-swap failed")
    tmp = FILE.with_name(FILE.name + f".tmp_{os.getpid()}")
    with tmp.open("xb") as f:
        f.write(after)
        f.flush()
        os.fsync(f.fileno())
    if tmp.stat().st_size != len(after):
        raise RuntimeError("Short temporary write")
    os.replace(tmp, FILE)
    actual = FILE.read_bytes()
    if actual != after or not actual.startswith(before):
        os.replace(backup, FILE)
        raise RuntimeError("Postcondition failed; restored")
    result = {
        "unit": "F1.1",
        "action": "precision_on_polar_descends_injectively_iff",
        "backup": str(backup),
        "before_bytes": len(before),
        "before_sha256": sha(before),
        "after_bytes": len(actual),
        "after_sha256": sha(actual),
        "prefix_preserved": True,
        "marker_count": actual.count(MARKER.encode()),
    }
    data = json.dumps(result, ensure_ascii=False, indent=2).encode() + b"\n"
    tmp_receipt = RECEIPT.with_name(RECEIPT.name + f".tmp_{os.getpid()}")
    with tmp_receipt.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    if RECEIPT.exists():
        raise RuntimeError("Receipt already exists")
    os.replace(tmp_receipt, RECEIPT)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
