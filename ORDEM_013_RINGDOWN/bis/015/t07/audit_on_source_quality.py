"""Audit public on-source DQ/injection masks and finite samples for all T07 measured rows."""
import hashlib
import json
import math
import sys
from pathlib import Path

import h5py
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import measure_rho_catalog_v5 as base


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


INITIAL = HERE / "T07_RHO_CATALOG_RESULT_v5.json"
SALVAGE = HERE / "T07_RHO_SALVAGE_RESULT.json"
rows = []
for directory in (HERE / "results_rho", HERE / "results_rho_salvage"):
    for result_path in sorted(directory.glob("*.json")):
        result = json.loads(result_path.read_bytes())
        if not result["status"].startswith("MEASURED_"):
            continue
        event = result["event"]
        for entry in result["detectors"]:
            detector = entry["detector"]
            item = base.BY_EVENT[event][("onsource", detector)]
            path, _ = base.checked_file(item)
            with h5py.File(path, "r") as handle:
                gps0 = float(handle["meta/GPSstart"][()])
                raw = handle["strain/Strain"]
                start = entry["first_index"]
                stop = start + 2 * base.N
                if stop > len(raw):
                    raise ValueError("WINDOW_OUTSIDE_FRAME")
                data = np.asarray(raw[start:stop:2], dtype=float) * 1e21
                quality = base.quality_good(handle)
            second_start = int(math.floor(start / 4096))
            second_last = int(math.floor((stop - 1) / 4096))
            mask = [bool(quality[s]) for s in range(second_start, second_last + 1)]
            rows.append({
                "event": event, "detector": detector,
                "result_sha256": sha(result_path),
                "onsource_sha256": sha(path),
                "frame_start_GPS": gps0,
                "window_GPS": [entry["first_sample_GPS"], entry["first_sample_GPS"] + base.N / 2048],
                "quality_seconds": list(range(second_start, second_last + 1)),
                "required_quality_and_injection_mask_each_second": mask,
                "all_required_masks_good": all(mask),
                "samples_all_finite": bool(np.all(np.isfinite(data))),
                "raw_scaled_abs_max": float(np.max(np.abs(data))) if np.all(np.isfinite(data)) else None,
                "norm_squared_over_dof": entry["norm_squared"] / entry["noise_degrees_of_freedom"],
                "outlier_diagnostic_ratio_gt_10_not_exclusion_rule": entry["norm_squared"] / entry["noise_degrees_of_freedom"] > 10,
            })
            print(json.dumps({"event": event, "detector": detector,
                              "good": all(mask), "finite": bool(np.all(np.isfinite(data))),
                              "power_per_dof": rows[-1]["norm_squared_over_dof"]}), flush=True)
result = {"status": "T07_ONSOURCE_DATA_QUALITY_AUDIT",
          "initial_sha256": sha(INITIAL), "salvage_sha256": sha(SALVAGE),
          "rows": rows,
          "outlier_threshold_scope": "ratio>10 is descriptive diagnostic selected after data, never a detection or exclusion rule",
          "gate_changed": False}
target = HERE / "T07_ONSOURCE_QUALITY_AUDIT.json"
raw = (json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
with target.open("xb") as handle:
    handle.write(raw)
print(json.dumps({"sha256": sha(target), "detectors": len(rows),
                  "bad_masks": sum(not r["all_required_masks_good"] for r in rows),
                  "nonfinite": sum(not r["samples_all_finite"] for r in rows),
                  "descriptive_power_outliers": sum(r["outlier_diagnostic_ratio_gt_10_not_exclusion_rule"] for r in rows)}))
