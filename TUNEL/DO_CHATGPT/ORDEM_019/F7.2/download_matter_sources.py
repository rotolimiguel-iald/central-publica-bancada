"""Custody fixed primary matter-interferometry papers for F7.2.

PDFs are article/preprint bytes. Publisher HTML is abstract-only evidence when
full-text PDF access is unavailable. The remote URLs receive no local content.
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
PDFS = {
    "Pedalino_2025_preprint_arxiv_2507.21211v1.pdf": "https://arxiv.org/pdf/2507.21211v1",
    "Pedalino_2026_published_author.pdf": "https://www.klaus-hornberger.de/pdf/nature2.pdf",
    "Hackermueller_2004_arxiv_quant-ph_0402146.pdf": "https://arxiv.org/pdf/quant-ph/0402146",
    "Chapman_1995_author.pdf": "https://chapmanlabs.gatech.edu/papers/scattering_ifm_prl95.pdf",
}
HTML = {
    "Kovachy_2015_Nature_abstract.html": "https://www.nature.com/articles/nature16155",
    "Fein_2019_NaturePhysics_abstract.html": "https://www.nature.com/articles/s41567-019-0663-9",
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
    BASE.mkdir(exist_ok=True)
    receipts = []
    for filename, url, kind in [
        *((name, url, "PDF_FULL_TEXT") for name, url in PDFS.items()),
        *((name, url, "PUBLISHER_ABSTRACT_HTML") for name, url in HTML.items()),
    ]:
        target = BASE / filename
        try:
            if target.exists():
                data = target.read_bytes()
                status = "already_present"
                final_url = url
            else:
                request = Request(url, headers={"User-Agent": "Mozilla/5.0 (IALD-F7.2-custody)"})
                with urlopen(request, timeout=60) as response:
                    data = response.read(MAX_BYTES + 1)
                    final_url = response.geturl()
                status = "downloaded"
            if len(data) < 1000 or len(data) > MAX_BYTES:
                raise RuntimeError(f"invalid source size: {len(data)}")
            if kind == "PDF_FULL_TEXT" and not data.startswith(b"%PDF-"):
                raise RuntimeError("response is not a PDF")
            if kind == "PUBLISHER_ABSTRACT_HTML" and b"<html" not in data[:1000].lower():
                raise RuntimeError("response is not HTML")
            if status == "downloaded":
                atomic_write(target, data)
            row = {
                "file": str(target),
                "url": url,
                "final_url": final_url,
                "kind": kind,
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
                "status": status,
            }
        except Exception as exc:
            row = {
                "file": None,
                "url": url,
                "kind": kind,
                "status": "UNAVAILABLE",
                "error": f"{type(exc).__name__}: {exc}",
            }
        receipts.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
    manifest = {
        "schema": "iald.f7_2.matter_source_custody.v1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "sources": receipts,
        "raw_experimental_data_custodied": False,
    }
    path = BASE / "MATTER_SOURCE_CUSTODY.json"
    if path.exists():
        raise RuntimeError("Matter custody manifest exists; inspect before replacing")
    atomic_write(path, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
