"""Identify exact detector failures and already-listed alternative off-source frames."""
import hashlib
import json
import sys
from pathlib import Path

import h5py
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from measure_rho_catalog_v5 import BY_EVENT, quality_good


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


catalog_path = HERE / "T07_RHO_CATALOG_RESULT_v5.json"
catalog = json.loads(catalog_path.read_bytes())
events = [r["event"] for r in catalog["rows"] if r["status"] == "MEASUREMENT_FAILED"]
on = {r["event"]: r for r in json.loads((HERE / "metadata" / "DISCOVERY_v2.json").read_bytes())["rows"]}
rows = []
for event in events:
    gps = float(on[event]["gps"])
    raw_candidates = json.loads((HERE / "metadata" / "offsource" / (event + "_frames.json")).read_bytes())["results"]
    detectors = []
    for (role, detector), item in BY_EVENT[event].items():
        if role != "offsource":
            continue
        path = HERE / item["relative_path"]
        with h5py.File(path, "r") as handle:
            train = handle["strain/Strain"][:2048 * 4096]
            good = quality_good(handle)
            finite = bool(np.all(np.isfinite(train)))
            clean = sum(bool(np.all(good[s:s + 4])) for s in range(0, 2048 - 4 + 1, 2))
        choices = [f for f in raw_candidates
                   if f["detector"] == detector and
                   f["gps_start"] + 4096 <= gps - 2 and
                   f["gps_start"] != item["gps_start"] and
                   f["hdf5_url"].split("?", 1)[0].endswith("-4096.hdf5")]
        detectors.append({"detector": detector, "source_sha256": sha(path),
                          "train_all_finite": finite, "clean_4s_windows": clean,
                          "alternative_frames": [{"gps_start": f["gps_start"],
                                                  "url": f["hdf5_url"].split("?", 1)[0]}
                                                 for f in sorted(choices, key=lambda f: f["gps_start"], reverse=True)]})
    rows.append({"event": event, "detectors": detectors})
    print(json.dumps({"event": event, "detectors": [{"name": d["detector"], "finite": d["train_all_finite"], "clean": d["clean_4s_windows"], "alternatives": len(d["alternative_frames"])} for d in detectors]}), flush=True)
report = {"status": "T07_DIAGNOSE_MEASUREMENT_FAILURES", "catalog_sha256": sha(catalog_path),
          "rows": rows, "no_gate_change": True}
target = HERE / "T07_NOISE_FAILURES.json"
raw = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode()
with target.open("xb") as handle:
    handle.write(raw)
print(json.dumps({"sha256": sha(target), "failures": len(rows)}))
