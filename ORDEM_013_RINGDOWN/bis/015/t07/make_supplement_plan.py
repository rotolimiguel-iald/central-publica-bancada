"""Register two additional T07 events using earlier public off-source frames."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
ON_PATH = ROOT / "metadata" / "DISCOVERY_v2.json"
OFF_PATH = ROOT / "metadata" / "offsource" / "DISCOVERY_OFFSOURCE.json"
PROBE_PATH = ROOT / "metadata" / "offsource" / "MISSING_PROBE.json"
on = {r["event"]: r for r in json.loads(ON_PATH.read_bytes())["rows"]}
off = {r["event"]: r for r in json.loads(OFF_PATH.read_bytes())["rows"]}
probe = {r["event"]: r for r in json.loads(PROBE_PATH.read_bytes())["rows"]}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


files = []
for event in ("GW150914_095045", "GW231206_233901"):
    row = on[event]
    existing = {f["detector"]: f for f in off[event]["frames"]}
    for detector in row["detectors"]:
        if detector not in existing:
            choices = probe[event]["candidates"][detector]
            assert choices
            best = max(choices, key=lambda f: f["gps_start"])
            existing[detector] = {"detector": detector, **best}
    for role, frames in (("onsource", row["frames"]), ("offsource", list(existing.values()))):
        for frame in frames:
            url = frame.get("hdf5_url", frame.get("url")).split("?", 1)[0]
            assert url.startswith("https://gwosc.org/archive/data/")
            name = Path(urlsplit(url).path).name
            assert name.endswith("-4096.hdf5")
            files.append({"event": event, "role": role, "detector": frame["detector"],
                          "gps_start": frame["gps_start"], "duration_seconds": 4096,
                          "url": url, "relative_path": f"strain/{event}/{role}/{name}",
                          "license_receipt": {"license": "CC BY 4.0 as stated by GWOSC API root",
                                              "source_url": "https://gwosc.org/api/v2/",
                                              "archive_url": url,
                                              "attribution": "Gravitational Wave Open Science Center (GWOSC) and LVK"}})
assert len(files) == 8
result = {"status": "PRE_DOWNLOAD_SUPPLEMENT_PLAN_CC_BY_4_0_PER_FILE",
          "created_utc": datetime.now(timezone.utc).isoformat(),
          "onsource_metadata_sha256": sha(ON_PATH),
          "offsource_metadata_sha256": sha(OFF_PATH),
          "older_probe_sha256": sha(PROBE_PATH),
          "base_plan_v3_sha256": sha(ROOT / "T07_DOWNLOAD_PLAN_v3.json"),
          "event_count": 2, "file_count": len(files), "files": files,
          "download_cap_bytes": 2_000_000_000,
          "warning": "Earlier off-source frames are farther from the event than F4's GW250114 frame; held-out whitened-power control and PSD stationarity must be reported.",
          "gate_changed": False}
path = ROOT / "T07_SUPPLEMENT_PLAN.json"
raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
with path.open("xb") as handle:
    handle.write(raw)
print(json.dumps({"plan_sha256": sha(path), "files": len(files)}))
