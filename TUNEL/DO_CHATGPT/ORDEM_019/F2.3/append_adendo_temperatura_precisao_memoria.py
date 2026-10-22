"""Add one signed scope clarification to the F2.3 Temperature adendo."""

import hashlib
import json
import os
from pathlib import Path
import tempfile
from datetime import datetime


root = Path(__file__).resolve().parent
target = root / "ADENDO_TEMPERATURA_DIAGNOSTICO.md"
first_receipt = root / "ADENDO_TEMPERATURA_ERRATA_C1_RECEIPT_20261008.json"
memory_receipt = root / "MEMORIA_ERRATA_AUDITORIA_TEMPERATURA_F11_20261008.json"
receipt = root / "ADENDO_TEMPERATURA_PRECISAO_MEMORIA_RECEIPT_20261008.json"
entry = ("\n**Precisão de escopo, 08/10/2026 — Codex gerente TGL:** a frase acima sobre não tocar memória "
         "descreve apenas esta subtarefa de adendo técnico. A entrega conjunta da errata de auditoria "
         "atualizou quatro superfícies de memória sob F2.3/F1.1.E1, com backup de bytes e recibo "
         "`MEMORIA_ERRATA_AUDITORIA_TEMPERATURA_F11_20261008.json`. Não se afirma ausência de "
         "escrita de memória na entrega conjunta.\n").encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def create(path: Path, data: bytes) -> None:
    with path.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


if __name__ == "__main__":
    if receipt.exists() or not memory_receipt.is_file():
        raise RuntimeError("Receipt already exists or joint memory receipt is absent")
    before = target.read_bytes()
    expected = json.loads(first_receipt.read_text(encoding="utf-8"))["after_sha256"]
    if sha(before) != expected or b"Precis\xc3\xa3o de escopo" in before:
        raise RuntimeError("Pinned prior state differs or clarification is already present")
    newline = b"\r\n" if b"\r\n" in before else b"\n"
    after = before + entry.replace(b"\n", newline)
    backup = target.with_name(target.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    create(backup, before)
    if backup.read_bytes() != before:
        raise RuntimeError("Backup bytes differ")
    with tempfile.NamedTemporaryFile(dir=root, prefix=".adendo_precisao_", suffix=".tmp", delete=False) as handle:
        handle.write(after)
        handle.flush()
        os.fsync(handle.fileno())
        temp = Path(handle.name)
    if temp.read_bytes() != after or target.read_bytes() != before:
        raise RuntimeError("Concurrent change or incomplete temporary file")
    os.replace(temp, target)
    if target.read_bytes() != after or not after.startswith(before):
        os.replace(backup, target)
        raise RuntimeError("Append failed; previous bytes restored")
    result = {"target": str(target), "backup": str(backup), "before_sha256": sha(before),
              "backup_sha256": sha(backup.read_bytes()), "after_sha256": sha(after),
              "memory_receipt": str(memory_receipt), "memory_receipt_sha256": sha(memory_receipt.read_bytes()),
              "prefix_preserved": True}
    create(receipt, (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps(result, ensure_ascii=False))
