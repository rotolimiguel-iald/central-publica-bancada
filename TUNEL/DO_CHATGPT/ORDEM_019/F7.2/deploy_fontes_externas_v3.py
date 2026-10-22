"""Copy the reviewed F7.2 V3 source bundle into Bancada Um, without overwrites.

This script does not install a channel, manifest, MCP tool or process reload.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile

UNIT = Path(__file__).resolve().parent
SOURCE = UNIT / "V3_STAGING" / "fontes_externas" / "F7.2"
BANCADA = Path(r"C:\IALD\Bancada_Um")
TARGET = BANCADA / "fontes_externas" / "F7.2"
RECEIPT = UNIT / "SOURCE_MIGRATION_RECEIPT_V3.json"
PROTECTED = [
    BANCADA / "mcp_um.py",
    BANCADA / "bancada" / "neutrino_canal.py",
    BANCADA / "bancada" / "neutrino_fontes_f72.json",
    BANCADA / "bancada" / "neutrino_canal_v2.py",
    BANCADA / "bancada" / "neutrino_fontes_f72_v2.json",
]


def fingerprint(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": str(path), "sha256": sha256(raw).hexdigest(), "bytes": len(raw)}


def copy_new(src: Path, dst: Path, expected: dict) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if fingerprint(dst)["sha256"] != expected["sha256"] or dst.stat().st_size != expected["bytes"]:
            raise RuntimeError(f"destination conflict: {dst}")
        return "already_identical"
    raw = src.read_bytes()
    if sha256(raw).hexdigest() != expected["sha256"] or len(raw) != expected["bytes"]:
        raise RuntimeError(f"source drift: {src}")
    with tempfile.NamedTemporaryFile(dir=dst.parent, prefix=dst.name + ".", suffix=".tmp", delete=False) as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    try:
        if fingerprint(temporary)["sha256"] != expected["sha256"]:
            raise RuntimeError(f"temporary drift: {temporary}")
        if dst.exists():
            raise RuntimeError(f"destination appeared during copy: {dst}")
        os.rename(temporary, dst)  # Windows rename refuses an existing destination.
    finally:
        if temporary.exists():
            temporary.unlink()
    if fingerprint(dst)["sha256"] != expected["sha256"]:
        raise RuntimeError(f"copied bytes differ: {dst}")
    return "created"


def main() -> None:
    if RECEIPT.exists():
        raise RuntimeError(f"receipt already exists: {RECEIPT}")
    if not SOURCE.is_dir():
        raise RuntimeError(f"staged source bundle missing: {SOURCE}")
    base = BANCADA.resolve()
    target = TARGET.resolve()
    if target != (base / "fontes_externas" / "F7.2") or not target.is_relative_to(base):
        raise RuntimeError(f"unexpected resolved target: {target}")
    before = {str(p): fingerprint(p) for p in PROTECTED}
    files = sorted(p for p in SOURCE.rglob("*") if p.is_file())
    if len(files) < 24 or any(p.is_symlink() for p in files):
        raise RuntimeError(f"unexpected source count or symlink: {len(files)}")
    rows = []
    for src in files:
        rel = src.relative_to(SOURCE)
        if rel.parts[0] not in {"scripts", "pdfs", "documents", "context"}:
            raise RuntimeError(f"unexpected source category: {rel}")
        if any(part.startswith(".") or ".bak_" in part or part.endswith(".tmp") for part in rel.parts):
            raise RuntimeError(f"temporary/backup in bundle: {rel}")
        dst = target / rel
        if not dst.resolve().is_relative_to(target):
            raise RuntimeError(f"source escapes destination: {rel}")
        expected = fingerprint(src)
        status = copy_new(src, dst, expected)
        rows.append({"relative_path": str(rel), "source": expected, "destination": fingerprint(dst), "status": status})
    after = {str(p): fingerprint(p) for p in PROTECTED}
    if before != after:
        raise RuntimeError("protected Bancada files changed")
    receipt = {
        "schema": "iald.f7_2.source_migration.v3",
        "unit": "F7.2",
        "time_utc": datetime.now(timezone.utc).isoformat(),
        "source_root": str(SOURCE),
        "destination_root": str(target),
        "file_count": len(rows),
        "files": rows,
        "protected_bancada_files_unchanged": before,
        "channel_or_manifest_installed": False,
        "mcp_touched_or_reloaded": False,
        "gate_effect": "NONE",
    }
    encoded = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with RECEIPT.open("xb") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps({"receipt": str(RECEIPT), "sha256": sha256(encoded).hexdigest(), "file_count": len(rows),
                      "created": sum(r["status"] == "created" for r in rows), "protected_unchanged": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
