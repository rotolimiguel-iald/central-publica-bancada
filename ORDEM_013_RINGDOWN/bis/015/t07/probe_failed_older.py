"""Probe one older GWOSC interval for failed detectors lacking nearby alternatives."""
import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FAIL = json.loads((ROOT / "T07_NOISE_FAILURES.json").read_bytes())
ON = {r["event"]: r for r in json.loads((ROOT / "metadata" / "DISCOVERY_v2.json").read_bytes())["rows"]}
out_dir = ROOT / "metadata" / "offsource" / "failure_older"
out_dir.mkdir(exist_ok=True)
rows = []
for row in FAIL["rows"]:
    event = row["event"]
    needed = [d["detector"] for d in row["detectors"] if not d["train_all_finite"] and not d["alternative_frames"]]
    if not needed:
        continue
    gps = float(ON[event]["gps"])
    params = urllib.parse.urlencode({"format": "json", "start": int(gps) - 16384,
                                     "stop": int(gps) - 8192,
                                     "sample-rate": 4, "pagesize": 100})
    url = "https://gwosc.org/api/v2/strain-files?" + params
    req = urllib.request.Request(url, headers={"Accept": "application/json",
                                           "User-Agent": "IALD-T07-quality-older-probe/1.0"})
    with urllib.request.urlopen(req, timeout=25) as response:
        raw = response.read()
    target = out_dir / (event + ".json")
    with target.open("xb") as handle:
        handle.write(raw)
    payload = json.loads(raw)
    candidates = {}
    for detector in needed:
        frames = [f for f in payload["results"]
                  if f["detector"] == detector and f["gps_start"] + 4096 <= gps - 2
                  and f["hdf5_url"].split("?", 1)[0].endswith("-4096.hdf5")]
        candidates[detector] = [{"gps_start": f["gps_start"],
                                 "url": f["hdf5_url"].split("?", 1)[0]}
                                for f in sorted(frames, key=lambda f: f["gps_start"], reverse=True)]
    rows.append({"event": event, "metadata_url": url,
                 "metadata_sha256": hashlib.sha256(raw).hexdigest(),
                 "candidate_frames": candidates})
    print(json.dumps({"event": event, "candidate_counts": {k: len(v) for k, v in candidates.items()}}), flush=True)
result = {"status": "T07_FAILED_DETECTOR_EARLIER_METADATA_PROBE",
          "failure_diagnostic_sha256": hashlib.sha256((ROOT / "T07_NOISE_FAILURES.json").read_bytes()).hexdigest(),
          "rows": rows, "no_strain_downloaded": True}
target = out_dir / "PROBE_RESULT.json"
raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
with target.open("xb") as handle:
    handle.write(raw)
print(json.dumps({"sha256": hashlib.sha256(raw).hexdigest()}))
