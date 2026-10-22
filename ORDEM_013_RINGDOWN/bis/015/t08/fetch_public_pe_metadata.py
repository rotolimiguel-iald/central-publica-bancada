"""Fetch only official Zenodo public release metadata, no PE sample blobs."""
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECORDS = (17602505, 20348005, 20348006)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

rows = []
for record_id in RECORDS:
    url = f"https://zenodo.org/api/records/{record_id}"
    request = urllib.request.Request(url, headers={"User-Agent": "IALD-T08-public-metadata-audit/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        assert response.status == 200
        raw = response.read(4_000_001)
        assert len(raw) <= 4_000_000
    doc = json.loads(raw)
    assert str(doc["id"]) == str(record_id)
    path = HERE / f"ZENODO_{record_id}_METADATA.json"
    with path.open("xb") as stream:
        stream.write(raw)
    files = doc.get("files", [])
    rows.append({"record_id": record_id, "url": url, "sha256": sha(path),
                 "title": doc.get("metadata", {}).get("title"),
                 "updated": doc.get("updated"), "license": doc.get("metadata", {}).get("license"),
                 "files": [{"key": f.get("key"), "size": f.get("size"),
                            "checksum": f.get("checksum"),
                            "self_url": f.get("links", {}).get("self")}
                           for f in files]})
    print(json.dumps({"record_id": record_id, "files": len(files),
                      "metadata_sha256": sha(path)}), flush=True)
result = {"status": "PUBLIC_PE_RELEASE_METADATA_ONLY_NO_POSTERIORS_DOWNLOADED",
          "created_utc": datetime.now(timezone.utc).isoformat(), "rows": rows}
out = HERE / "T08_PE_METADATA_INDEX.json"
with out.open("xb") as stream:
    stream.write((json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode())
print(json.dumps({"index_sha256": sha(out)}))
