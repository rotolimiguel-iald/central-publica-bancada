"""Independent custody and algebra audit of the T10-C bank and first C5 control."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
RING = HERE.parents[2]
CHAT = RING.parent


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for part in iter(lambda: f.read(1 << 20), b""):
            h.update(part)
    return h.hexdigest()


def main():
    result = json.loads((HERE / "T10_C_BANK_RESULT_v4.json").read_bytes())
    c5 = json.loads((RING / "C5_IMR_CONTROLS.json").read_bytes())
    rows = result["rows"]
    assert len(rows) == 10
    assert sorted((r["bin"], r["family"]) for r in rows) == sorted(
        (j, f) for j in range(5) for f in ("SEOBNRv4HM", "IMRPhenomXPHM"))
    controls = {item["family"]: item for item in c5["families"]}
    checks = []
    for row in rows:
        path = CHAT / row["file_relative_to_Chatgpt"]
        assert sha(path) == row["sha256"]
        with np.load(path) as data:
            shape = data["relative_time_s"].shape
            assert shape == (819,)
            assert all(data[k].shape == shape and np.isfinite(data[k]).all() for k in data.files)
            closure = max(float(np.max(np.abs(data["data_" + name] - data["signal_" + name] - data["noise_" + name])))
                          for name in ("H1", "L1"))
            assert closure < 1e-34
            validation = dict(bin=row["bin"], family=row["family"], sha256=row["sha256"],
                              closure_max_abs=closure, target_snr=row["target_optimal_snr"],
                              reported_snr=row["measured_optimal_snr"])
            assert abs(validation["target_snr"] - validation["reported_snr"]) < 1e-12
            if row["bin"] == 0:
                anchor = controls[row["family"]]
                c5path = Path(anchor["path"])
                assert sha(c5path) == anchor["sha256"]
                with np.load(c5path) as reference:
                    ref_t = reference["time_from_peak_s"]
                    t = data["relative_time_s"]
                    ref_plus = np.interp(t, ref_t, reference["all_plus"])
                    ref_cross = np.interp(t, ref_t, reference["all_cross"])
                    output = np.concatenate([data["plus"], data["cross"]]) / row["scale"]
                    expected = np.concatenate([ref_plus, ref_cross])
                    residual = np.linalg.norm(output - expected) / np.linalg.norm(expected)
                    validation["relative_waveform_residual_vs_C5"] = float(residual)
            checks.append(validation)
    report = dict(status="T10_C_BANK_AUDITED", created_utc=datetime.now(timezone.utc).isoformat(),
                  count=len(checks), checks=checks, bank_manifest_sha256=sha(HERE / "T10_C_BANK_RESULT_v4.json"),
                  C5_sha256=sha(RING / "C5_IMR_CONTROLS.json"),
                  gate_changed=False, sigma_c=None)
    path = HERE / "T10_C_BANK_AUDIT.json"
    with path.open("xb") as stream:
        stream.write((json.dumps(report, indent=2, allow_nan=False) + "\n").encode())
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps({"count": len(checks), "C5_residuals": [x.get("relative_waveform_residual_vs_C5") for x in checks if x["bin"] == 0]}))


if __name__ == "__main__":
    main()
