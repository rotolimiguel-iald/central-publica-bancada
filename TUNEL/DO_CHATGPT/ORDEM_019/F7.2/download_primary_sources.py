"""Download fixed open-access primary papers for F7.2 custody.

No local corpus content is transmitted. Each PDF is capped, checked, and saved
atomically. Existing files are verified and never overwritten.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile
from urllib.request import Request, urlopen


BASE = Path(__file__).resolve().parent / "fontes_primarias"
SOURCES = {
    "Fogli_2007_arxiv_0704.2568.pdf": "https://arxiv.org/pdf/0704.2568",
    "DeRomeri_2023_arxiv_2306.14699.pdf": "https://arxiv.org/pdf/2306.14699",
    "ORCA6_2025_arxiv_2410.01388.pdf": "https://arxiv.org/pdf/2410.01388",
    "IceCube_2024_arxiv_2308.00105.pdf": "https://arxiv.org/pdf/2308.00105",
    "Coloma_2018_arxiv_1803.04438.pdf": "https://arxiv.org/pdf/1803.04438",
}
MAX_BYTES = 20_000_000


def atomic_write(path: Path, data: bytes) -> None:
    fd, temporary_name = tempfile.mkstemp(prefix=path.name + ".tmp_", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary_name, path)
    except Exception:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    receipts = []
    for filename, url in SOURCES.items():
        target = BASE / filename
        if target.exists():
            data = target.read_bytes()
            status = "already_present"
        else:
            request = Request(url, headers={"User-Agent": "IALD-F7.2-source-custody/1.0"})
            with urlopen(request, timeout=60) as response:
                data = response.read(MAX_BYTES + 1)
            status = "downloaded"
        if len(data) < 1000 or len(data) > MAX_BYTES or not data.startswith(b"%PDF-"):
            raise RuntimeError(f"Invalid PDF from {url}; bytes={len(data)}")
        if status == "downloaded":
            atomic_write(target, data)
        row = {
            "file": str(target),
            "url": url,
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
            "status": status,
        }
        receipts.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
    manifest = {
        "schema": "iald.f7_2.primary_source_custody.v1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "sources": receipts,
        "scope": "Downloaded open-access primary PDFs; article interpretation remains in the F7.2 report.",
    }
    manifest_path = BASE / "SOURCE_CUSTODY.json"
    if manifest_path.exists():
        raise RuntimeError("Custody manifest already exists; inspect before replacing")
    atomic_write(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
