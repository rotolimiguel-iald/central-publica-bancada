"""Pre-register first available alternate PSD frame for each failed detector."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
FAIL_PATH = HERE / "T07_NOISE_FAILURES.json"
OLDER_PATH = HERE / "metadata" / "offsource" / "failure_older" / "PROBE_RESULT.json"
failed = json.loads(FAIL_PATH.read_bytes())
older = {r["event"]: r for r in json.loads(OLDER_PATH.read_bytes())["rows"]}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


files = []
no_alt = []
for row in failed["rows"]:
    event = row["event"]
    for detector in row["detectors"]:
        if detector["train_all_finite"]:
            continue
        name = detector["detector"]
        choices = detector["alternative_frames"]
        if not choices:
            choices = older.get(event, {}).get("candidate_frames", {}).get(name, [])
        if not choices:
            no_alt.append({"event": event, "detector": name})
            continue
        chosen = choices[0]
        url = chosen["url"].split("?", 1)[0]
        assert url.startswith("https://gwosc.org/archive/data/")
        basename = Path(urlsplit(url).path).name
        assert basename.endswith("-4096.hdf5")
        files.append({"event": event, "role": "offsource_alt",
                      "detector": name, "gps_start": chosen["gps_start"],
                      "duration_seconds": 4096, "url": url,
                      "relative_path": f"strain/{event}/offsource_alt/{basename}",
                      "selection_rule": "nearest distinct eligible frame in initial 8192 s query, else nearest in older 8192 s probe; selected before reading strain",
                      "license_receipt": {"license": "CC BY 4.0 as stated by GWOSC API root",
                                          "source_url": "https://gwosc.org/api/v2/",
                                          "archive_url": url,
                                          "attribution": "Gravitational Wave Open Science Center (GWOSC) and LVK"}})
assert len({r["relative_path"] for r in files}) == len(files)
result = {"status": "PRE_DOWNLOAD_ALTERNATE_NOISE_PLAN_CC_BY_4_0_PER_FILE",
          "created_utc": datetime.now(timezone.utc).isoformat(),
          "initial_catalog_sha256": sha(HERE / "T07_RHO_CATALOG_RESULT_v5.json"),
          "failure_diagnostic_sha256": sha(FAIL_PATH),
          "older_probe_sha256": sha(OLDER_PATH),
          "file_count": len(files), "files": files,
          "no_alternate": no_alt,
          "download_cap_bytes": 3_000_000_000,
          "interpretation": "Alternative PSD is farther from event; success is still only local window power, not sigma or matched-filter SNR. Held-out noise controls required.",
          "gate_changed": False}
target = HERE / "T07_ALTERNATE_PLAN.json"
raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
with target.open("xb") as handle:
    handle.write(raw)
print(json.dumps({"sha256": sha(target), "files": len(files), "no_alt": no_alt}))
