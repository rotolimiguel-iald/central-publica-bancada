"""Seal the Portuguese F1.2 receipt under new names, preserving the draft."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seal(path: Path, raw: bytes) -> None:
    if path.exists():
        raise FileExistsError(path)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False) as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
        tmp = Path(stream.name)
    if tmp.stat().st_size != len(raw):
        raise OSError(tmp)
    os.link(tmp, path)
    tmp.unlink()
    if path.read_bytes() != raw:
        raise OSError(path)


old_manifest = json.loads((ROOT / "HASHES_FECHO_V351_AGAPE_20261008.json").read_text(encoding="utf-8"))
for label, item in old_manifest["files"].items():
    path = Path(item["path"])
    if sha(path) != item["sha256"] or path.stat().st_size != item["bytes"]:
        raise RuntimeError(f"Changed source: {label}")

pt = ROOT / "DIAGNOSTICO_FECHO_V351_AGAPE_PTBR_20261008.md"
files = dict(old_manifest["files"])
files["diagnostic"] = {"path": str(pt), "bytes": pt.stat().st_size, "sha256": sha(pt)}
manifest = {"unit": "F1.2", "language": "pt-BR", "files": files}
manifest_path = ROOT / "HASHES_FECHO_V351_AGAPE_PTBR_20261008.json"
seal(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

old_result = json.loads((ROOT / "RESULTADO_FECHO_V351_AGAPE_20261008.json").read_text(encoding="utf-8"))
old_result["language"] = "pt-BR"
old_result["manifest"] = {"path": str(manifest_path), "sha256": sha(manifest_path)}
old_result["diagnostic"] = {"path": str(pt), "sha256": sha(pt)}
old_result["draft_receipt_preserved"] = str(ROOT / "RESULTADO_FECHO_V351_AGAPE_20261008.json")
result_path = ROOT / "RESULTADO_FECHO_V351_AGAPE_PTBR_20261008.json"
seal(result_path, (json.dumps(old_result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"result": str(result_path), "result_sha256": sha(result_path), "manifest": str(manifest_path), "manifest_sha256": sha(manifest_path), "diagnostic_sha256": sha(pt)}, ensure_ascii=False))
