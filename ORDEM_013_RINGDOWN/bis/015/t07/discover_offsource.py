"""Locate an independent 4096 s GWOSC off-source frame per event/detector."""
import hashlib
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DISCOVERY = ROOT / "metadata" / "DISCOVERY_v2.json"
source_raw = DISCOVERY.read_bytes()
source = json.loads(source_raw)
out_dir = ROOT / "metadata" / "offsource"
out_dir.mkdir(exist_ok=True)


def sha(data):
    return hashlib.sha256(data).hexdigest()


rows = []
for row in source["rows"]:
    name = row["event"]
    gps = float(row["gps"])
    params = urllib.parse.urlencode({
        "format": "json", "start": int(gps) - 8192,
        "stop": int(gps) - 8, "sample-rate": 4, "pagesize": 100,
    })
    url = "https://gwosc.org/api/v2/strain-files?" + params
    p = out_dir / (name + "_frames.json")
    record = {"event": name, "metadata_url": url}
    try:
        if p.exists():
            raw = p.read_bytes()
        else:
            req = urllib.request.Request(url, headers={
                "Accept": "application/json", "User-Agent": "IALD-T07-offsource-discovery/1.0"
            })
            with urllib.request.urlopen(req, timeout=25) as response:
                raw = response.read()
            with p.open("xb") as handle:
                handle.write(raw)
        payload = json.loads(raw)
        record["metadata_sha256"] = sha(raw)
        frames = []
        for detector in row["detectors"]:
            choices = [f for f in payload["results"]
                       if f["detector"] == detector and
                       f["gps_start"] + 4096 <= gps - 2 and
                       f["hdf5_url"].split("?", 1)[0].endswith("-4096.hdf5")]
            if not choices:
                record.setdefault("missing_detectors", []).append(detector)
                continue
            best = max(choices, key=lambda item: item["gps_start"])
            frames.append({"detector": detector,
                           "gps_start": best["gps_start"],
                           "hdf5_url": best["hdf5_url"],
                           "gps_end": best["gps_start"] + 4096})
        record["frames"] = frames
        record["status"] = "OFFSOURCE_FRAMES_FOUND" if len(frames) == len(row["detectors"]) else "PARTIAL_OFFSOURCE_FRAMES"
    except Exception as exc:
        record["status"] = "API_ERROR"
        record["error"] = type(exc).__name__ + ":" + str(exc)[:200]
    rows.append(record)
    print(json.dumps({"event": name, "status": record["status"], "frames": len(record.get("frames", []))}), flush=True)
    time.sleep(.05)

result = {
    "status": "T07_OFFSOURCE_METADATA_ONLY",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "onsource_metadata_sha256": sha(source_raw),
    "license_url": "https://gwosc.org/api/v2/",
    "license_statement": "GWOSC API root says data released under CC BY 4.0; individual files still require receipts before download",
    "rows": rows,
}
target = out_dir / "DISCOVERY_OFFSOURCE.json"
raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
with target.open("xb") as handle:
    handle.write(raw)
print(json.dumps({"sha256": sha(raw), "found": sum(r["status"] == "OFFSOURCE_FRAMES_FOUND" for r in rows)}))
