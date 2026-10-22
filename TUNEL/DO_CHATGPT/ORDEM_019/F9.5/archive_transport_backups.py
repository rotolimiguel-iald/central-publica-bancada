"""Archive historical TRANSPORTE_DESASSISTIDO backups with byte custody."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923").resolve()
EVIDENCE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F9.5")
PATTERN = re.compile(r"^TRANSPORTE_DESASSISTIDO\.md\.bak_(\d{8})_\d{6}_\d+$")
CUTOFF = "20260929"  # All older edit windows; the current-session backup remains beside the guide.
PLAN = EVIDENCE / "BACKUP_ARCHIVE_PLAN.json"
RESULT = EVIDENCE / "BACKUP_ARCHIVE_RESULT.json"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic(path: Path, payload: dict) -> None:
    data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if path.exists():
        old = path.read_bytes()
        if old == data:
            return
        backup = path.with_name(path.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        with backup.open("xb") as handle:
            handle.write(old)
        if backup.read_bytes() != old:
            raise RuntimeError("backup mismatch")
    temp = path.with_name(path.name + ".tmp_" + str(os.getpid()))
    with temp.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if temp.stat().st_size != len(data):
        raise RuntimeError("temporary size mismatch")
    os.replace(temp, path)
    if path.read_bytes() != data:
        raise RuntimeError("replacement mismatch")


def confined(path: Path) -> None:
    resolved = path.resolve(strict=False)
    if not resolved.is_relative_to(ROOT):
        raise RuntimeError(f"path escapes intended directory: {path}")


def build_plan() -> dict:
    entries = []
    for source in sorted(ROOT.glob("TRANSPORTE_DESASSISTIDO.md.bak_*"), key=lambda p: p.name):
        match = PATTERN.fullmatch(source.name)
        if not match or match.group(1) >= CUTOFF:
            continue
        if source.parent.resolve() != ROOT or not source.is_file() or source.is_symlink():
            raise RuntimeError(f"unexpected source: {source}")
        destination = ROOT / "_backups" / match.group(1) / source.name
        confined(destination)
        if destination.exists():
            raise RuntimeError(f"destination already exists: {destination}")
        entries.append({"source": str(source), "destination": str(destination),
                        "sha256_before": sha(source), "bytes": source.stat().st_size})
    return {"created_utc": datetime.now(timezone.utc).isoformat(),
            "cutoff_exclusive": CUTOFF, "entries": entries, "count": len(entries),
            "statute": "REAL_BYTES_MEASURED_BEFORE_MOVE"}


def apply(plan: dict) -> dict:
    done = []
    for item in plan["entries"]:
        source = Path(item["source"])
        destination = Path(item["destination"])
        confined(source)
        confined(destination)
        if source.parent.resolve() != ROOT:
            raise RuntimeError(f"source not adjacent to guide: {source}")
        if destination.exists():
            if source.exists() or sha(destination) != item["sha256_before"]:
                raise RuntimeError(f"conflicting destination: {destination}")
        else:
            if not source.is_file() or source.stat().st_size != item["bytes"] or sha(source) != item["sha256_before"]:
                raise RuntimeError(f"source changed: {source}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(source, destination)
        after = sha(destination)
        if after != item["sha256_before"] or destination.stat().st_size != item["bytes"]:
            raise RuntimeError(f"moved bytes differ: {destination}")
        done.append({**item, "sha256_after": after})
    return {"completed_utc": datetime.now(timezone.utc).isoformat(),
            "count": len(done), "entries": done,
            "statute": "REAL_MOVED_AND_SHA256_VERIFIED"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if PLAN.exists():
        plan = json.loads(PLAN.read_text(encoding="utf-8"))
    else:
        plan = build_plan()
        atomic(PLAN, plan)
    if args.apply:
        result = apply(plan)
        atomic(RESULT, result)
        print(json.dumps({"moved": result["count"], "result_sha256": sha(RESULT)}))
    else:
        print(json.dumps({"planned": plan["count"], "plan_sha256": sha(PLAN)}))


if __name__ == "__main__":
    main()
