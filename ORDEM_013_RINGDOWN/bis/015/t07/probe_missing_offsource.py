"""Check one earlier 8192 s GWOSC interval for the three uncovered events."""
import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ON = json.loads((ROOT / "metadata" / "DISCOVERY_v2.json").read_bytes())
OFF = json.loads((ROOT / "metadata" / "offsource" / "DISCOVERY_OFFSOURCE.json").read_bytes())
on = {r["event"]: r for r in ON["rows"]}
missing = [r for r in OFF["rows"] if r["status"] != "OFFSOURCE_FRAMES_FOUND"]
assert len(missing) == 3
rows = []
for row in missing:
    event = row["event"]
    gps = float(on[event]["gps"])
    params = urllib.parse.urlencode({"format": "json", "start": int(gps) - 16384,
                                     "stop": int(gps) - 8192, "sample-rate": 4,
                                     "pagesize": 100})
    url = "https://gwosc.org/api/v2/strain-files?" + params
    req = urllib.request.Request(url, headers={"Accept": "application/json",
                                           "User-Agent": "IALD-T07-missing-probe/1.0"})
    with urllib.request.urlopen(req, timeout=25) as response:
        raw = response.read()
    path = ROOT / "metadata" / "offsource" / (event + "_older_frames.json")
    with path.open("xb") as handle:
        handle.write(raw)
    data = json.loads(raw)
    candidates = {}
    for detector in row["missing_detectors"]:
        choices = [f for f in data["results"]
                   if f["detector"] == detector and f["gps_start"] + 4096 <= gps - 2
                   and f["hdf5_url"].split("?", 1)[0].endswith("-4096.hdf5")]
        candidates[detector] = [{"gps_start": f["gps_start"], "url": f["hdf5_url"]} for f in choices]
    rows.append({"event": event, "url": url,
                 "raw_sha256": hashlib.sha256(raw).hexdigest(),
                 "api_results_count": len(data["results"]),
                 "has_next": bool(data.get("next")),
                 "candidates": candidates})
    print(json.dumps({"event": event, "candidate_counts": {k: len(v) for k, v in candidates.items()}}), flush=True)
result = {"status": "TARGETED_EARLIER_OFFSOURCE_PROBE", "rows": rows,
          "no_strain_downloaded": True, "gate_changed": False}
target = ROOT / "metadata" / "offsource" / "MISSING_PROBE.json"
raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
with target.open("xb") as handle:
    handle.write(raw)
print(json.dumps({"sha256": hashlib.sha256(raw).hexdigest()}))
