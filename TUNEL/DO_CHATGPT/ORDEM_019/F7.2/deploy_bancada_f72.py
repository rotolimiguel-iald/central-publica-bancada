"""Install the reviewed F7.2 MCP channel on disk, without restarting services."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path


UNIT = Path(__file__).resolve().parent
STAGE = UNIT / "STAGING"
LIVE = Path(r"C:\IALD\Bancada_Um")
RECEIPT = STAGE / "STAGING_RECEIPT.json"
OUTPUT = UNIT / "DEPLOYMENT_RECEIPT.json"
FILES = (
    "bancada/neutrino_canal.py",
    "bancada/neutrino_fontes_f72.json",
    "mcp_um.py",  # entry point is installed last
)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def atomic_write(path: Path, raw: bytes) -> None:
    temp = path.with_name(path.name + ".tmp_f72")
    with temp.open("wb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if temp.stat().st_size != len(raw):
        raise OSError(f"incomplete temporary file: {temp}")
    os.replace(temp, path)
    if path.read_bytes() != raw:
        raise OSError(f"post-install byte mismatch: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    receipt_raw = RECEIPT.read_bytes()
    receipt = json.loads(receipt_raw)
    if receipt.get("schema") != "iald.f7_2.neutrino_staging.v5":
        raise ValueError("staging receipt version mismatch")
    if receipt.get("status") != "STAGING_NOT_DEPLOYED":
        raise ValueError("unexpected staging status")
    staged = {}
    for relative, pin in receipt["files"].items():
        path = STAGE / relative
        raw = path.read_bytes()
        if sha(raw) != pin:
            raise ValueError(f"staging SHA mismatch: {path}")
        staged[relative] = raw
    for relative in FILES:
        if relative not in staged:
            raise ValueError(f"missing staged deployment file: {relative}")
    if sha(staged["bancada/neutrino_fontes_f72.json"]) != receipt["manifest_sha256_locked"]:
        raise ValueError("manifest pin mismatch")
    live_entry = LIVE / "mcp_um.py"
    original = live_entry.read_bytes()
    if sha(original) != receipt["source_mcp_sha256"]:
        raise ValueError(f"live MCP drift: {sha(original)}")
    if OUTPUT.exists():
        raise FileExistsError(f"deployment receipt already exists: {OUTPUT}")
    target_state = []
    for relative in FILES:
        path = LIVE / relative
        if not path.parent.is_dir():
            raise FileNotFoundError(path.parent)
        prior = path.read_bytes() if path.exists() else None
        if relative != "mcp_um.py" and prior not in (None, staged[relative]):
            raise ValueError(f"existing different channel file: {path}")
        target_state.append((relative, path, prior))
    preview = {
        "schema": "iald.f7_2.bancada_deployment.v1",
        "unit": "F7.2",
        "stage_receipt_sha256": sha(receipt_raw),
        "source_mcp_sha256": sha(original),
        "target_mcp_sha256": sha(staged["mcp_um.py"]),
        "files": [{"path": str(path), "prior_sha256": sha(prior) if prior else None,
                   "new_sha256": sha(staged[relative])}
                  for relative, path, prior in target_state],
        "process_reloaded": False,
        "gate_effect": "NONE",
    }
    if not args.apply:
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_UTC")
    backups = {}
    for relative, path, prior in target_state:
        if prior is not None and prior != staged[relative]:
            backup = path.with_name(path.name + ".bak_" + stamp)
            with backup.open("wb") as stream:
                stream.write(prior)
                stream.flush()
                os.fsync(stream.fileno())
            if backup.read_bytes() != prior:
                raise OSError(f"backup mismatch: {backup}")
            backups[relative] = str(backup)
    for relative, path, prior in target_state:
        if prior != staged[relative]:
            atomic_write(path, staged[relative])
    preview["backups"] = backups
    preview["installed_at_utc"] = datetime.now(timezone.utc).isoformat()
    preview["status"] = "INSTALLED_ON_DISK_PROCESS_NOT_RELOADED"
    raw = (json.dumps(preview, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    atomic_write(OUTPUT, raw)
    print(json.dumps({"receipt": str(OUTPUT), "sha256": sha(raw), "status": preview["status"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
