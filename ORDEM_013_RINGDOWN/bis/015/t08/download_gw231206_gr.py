"""Fetch one public LVK GR PE file for a source-controlled T08 pilot."""
import hashlib
import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
INDEX = HERE / "T08_PE_METADATA_INDEX.json"
EVENT = "GW231206_233901"
records = json.loads(INDEX.read_bytes())["rows"]
matches = [(r, f) for r in records for f in r["files"]
           if EVENT in (f["key"] or "") and f["key"].endswith("combined_PEDataRelease.hdf5")]
assert len(matches) == 1
record, f = matches[0]
assert record["record_id"] == 17602505 and record["license"]["id"] == "cc-by-4.0"
assert f["size"] == 189649148 and f["self_url"].startswith("https://zenodo.org/api/records/17602505/files/")
destination = HERE / f["key"]
part = HERE / (f["key"] + ".part")
started = time.monotonic()
request = urllib.request.Request(f["self_url"], headers={"User-Agent": "IALD-T08-public-GR-control/1.0"})
md5 = hashlib.md5()
sha = hashlib.sha256()
size = 0
with urllib.request.urlopen(request, timeout=60) as response, part.open("xb") as stream:
    assert response.status == 200
    while True:
        block = response.read(1024 * 1024)
        if not block:
            break
        stream.write(block)
        md5.update(block)
        sha.update(block)
        size += len(block)
        if size > f["size"]:
            raise ValueError("DOWNLOADED_MORE_THAN_METADATA")
assert size == f["size"]
assert "md5:" + md5.hexdigest() == f["checksum"]
os.replace(part, destination)
receipt = {"status": "PUBLIC_GR_PE_FILE_VERIFIED_NOT_YET_USED_FOR_SNR",
           "created_utc": datetime.now(timezone.utc).isoformat(), "event": EVENT,
           "record_id": record["record_id"], "source_url": f["self_url"],
           "license": record["license"], "bytes": size, "md5": md5.hexdigest(),
           "sha256": sha.hexdigest(), "metadata_index_sha256": hashlib.sha256(INDEX.read_bytes()).hexdigest(),
           "wall_seconds": time.monotonic() - started}
path = HERE / "GW231206_GR_PE_DOWNLOAD_RECEIPT.json"
with path.open("xb") as stream:
    stream.write((json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode())
print(json.dumps({"receipt_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                  "bytes": size, "wall_seconds": receipt["wall_seconds"]}))
