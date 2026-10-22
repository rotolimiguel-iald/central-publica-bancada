"""Restore the exact result bytes that the manager audited in event 73."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path


HERE = Path(__file__).resolve().parent
RESULT = HERE / "RESULTADO.json"
ADDENDUM = HERE / "RESULTADO_ADENDO_LIGHT_TERM.json"
CLI = Path(r"C:\IALD\PROGRAMA_IALD\iald.py")
PYTHON = Path(r"C:\Python314\python.exe")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    board = json.loads(subprocess.check_output([str(PYTHON), str(CLI), "ver", "F1.1"], text=True, encoding="utf-8"))
    audited = [entry for entry in board["evidencia"] if entry["por"] == "claude-c1" and
               Path(entry["caminho"]).name == "RESULTADO.json"]
    if len(audited) != 1:
        raise RuntimeError("audited receipt not uniquely identified")
    audited_hash = audited[0]["sha256"]
    candidates = [path for path in HERE.glob("RESULTADO.json.bak_*") if digest(path.read_bytes()) == audited_hash]
    if len(candidates) != 1:
        raise RuntimeError("audited bytes not uniquely available")
    current = RESULT.read_bytes()
    original = candidates[0].read_bytes()
    if digest(current) == audited_hash:
        raise RuntimeError("result already equals audited bytes; no mutation needed")
    if ADDENDUM.exists():
        raise RuntimeError("addendum path already exists")
    with ADDENDUM.open("xb") as handle:
        handle.write(current)
    if ADDENDUM.read_bytes() != current:
        raise RuntimeError("addendum copy mismatch")
    backup = RESULT.with_name(RESULT.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    with backup.open("xb") as handle:
        handle.write(current)
    if backup.read_bytes() != current:
        raise RuntimeError("immediate backup mismatch")
    temp = RESULT.with_name(RESULT.name + ".tmp_" + str(os.getpid()))
    with temp.open("xb") as handle:
        handle.write(original)
        handle.flush()
        os.fsync(handle.fileno())
    if temp.stat().st_size != len(original):
        raise RuntimeError("temporary size mismatch")
    os.replace(temp, RESULT)
    if digest(RESULT.read_bytes()) != audited_hash:
        raise RuntimeError("restored bytes differ from audited hash")
    print(json.dumps({"audited_restored_sha256": audited_hash,
                      "addendum_sha256": digest(ADDENDUM.read_bytes()),
                      "backup": str(backup)}))


if __name__ == "__main__":
    main()
