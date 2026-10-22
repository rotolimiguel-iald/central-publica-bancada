"""Remove only F3.1's local, non-link Python cache and write a receipt."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE / "__pycache__"
RECEIPT = HERE / "HIGIENE_PYCACHE_F31_R52_20261008.json"


def main() -> None:
    root = HERE.resolve(strict=True)
    target = TARGET.resolve(strict=True)
    if target.parent != root or target.name != "__pycache__":
        raise ValueError("cache path outside the intended F3.1 directory")
    if TARGET.is_symlink() or (hasattr(TARGET, "is_junction") and TARGET.is_junction()):
        raise ValueError("cache is a link or junction")
    if RECEIPT.exists():
        raise FileExistsError(RECEIPT)
    children = sorted(TARGET.iterdir(), key=lambda p: p.name)
    removed = []
    for child in children:
        if child.parent.resolve(strict=True) != target or child.is_symlink() or not child.is_file() or child.suffix != ".pyc":
            raise ValueError(f"unexpected cache child: {child}")
        data = child.read_bytes()
        removed.append({"name": child.name, "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest()})
    for child in children:
        child.unlink()
    TARGET.rmdir()
    if TARGET.exists():
        raise OSError("cache still exists")
    receipt = {"schema": "F31_R52_PYCACHE_HYGIENE_V1", "root": str(root),
               "target": str(target), "removed": removed, "target_absent_after": True,
               "other_directories_touched": False}
    data = (json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    fd, temporary = tempfile.mkstemp(prefix=RECEIPT.name + ".", suffix=".tmp", dir=HERE)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if Path(temporary).stat().st_size != len(data):
            raise OSError("temporary size mismatch")
        os.replace(temporary, RECEIPT)
        if RECEIPT.read_bytes() != data:
            raise OSError("receipt mismatch")
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
