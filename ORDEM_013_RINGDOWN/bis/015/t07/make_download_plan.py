"""Register public strain and per-file license provenance before T07 download."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent
ON = ROOT / "metadata" / "DISCOVERY_v2.json"
OFF = ROOT / "metadata" / "offsource" / "DISCOVERY_OFFSOURCE.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


on = json.loads(ON.read_bytes())
off = json.loads(OFF.read_bytes())
off_by_name = {row["event"]: row for row in off["rows"]}
license_url = "https://gwosc.org/api/v2/"
records = []
skipped = []
for row in on["rows"]:
    other = off_by_name[row["event"]]
    if row["status"] != "METADATA_FOUND" or other["status"] != "OFFSOURCE_FRAMES_FOUND":
        skipped.append({"event": row["event"], "reason": other["status"],
                        "missing_detectors": other.get("missing_detectors", [])})
        continue
    for role, frames in (("onsource", row["frames"]), ("offsource", other["frames"])):
        for frame in frames:
            url = frame["hdf5_url"].split("?", 1)[0]
            assert url.startswith("https://gwosc.org/archive/data/")
            name = Path(urlsplit(url).path).name
            assert name.endswith("-4096.hdf5")
            relative = f"strain/{row['event']}/{role}/{name}"
            records.append({
                "event": row["event"], "role": role,
                "detector": frame["detector"],
                "gps_start": frame["gps_start"], "duration_seconds": 4096,
                "url": url, "relative_path": relative,
                "license_receipt": {
                    "license": "CC BY 4.0 as stated by GWOSC API root",
                    "source_url": license_url,
                    "archive_url": url,
                    "attribution": "Gravitational Wave Open Science Center (GWOSC) and LVK",
                },
            })

assert len({r["relative_path"] for r in records}) == len(records)
assert len({r["event"] for r in records}) == 30
result = {
    "status": "PRE_DOWNLOAD_PLAN_CC_BY_4_0_PER_FILE",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "onsource_metadata_sha256": sha(ON),
    "offsource_metadata_sha256": sha(OFF),
    "event_count": len({r["event"] for r in records}),
    "file_count": len(records),
    "files": records,
    "skipped": skipped,
    "download_cap_bytes": 8_000_000_000,
    "rule": "No strain download before this immutable manifest. Save SHA256 and bytes per file afterward; no original source modification.",
    "gate_changed": False,
}
target = ROOT / "T07_DOWNLOAD_PLAN.json"
raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
with target.open("xb") as handle:
    handle.write(raw)
print(json.dumps({"plan_sha256": sha(target), "events": result["event_count"], "files": len(records), "skipped": skipped}))
