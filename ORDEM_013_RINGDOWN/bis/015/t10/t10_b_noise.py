"""T10-B: pinned off-source covariance diagnostics, no PE or gate update."""
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[variable] = "1"

import numpy as np
from scipy.linalg import cholesky, toeplitz
from scipy.signal import butter, freqz

HERE = Path(__file__).resolve().parent
RING = HERE.parents[2]
CHAT = RING.parent
SOURCE = RING / "bis" / "e2_code_v1_1_2"
sys.path.insert(0, str(SOURCE))
from strain_io import offsource_psd


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for part in iter(lambda: f.read(1 << 20), b""):
            h.update(part)
    return h.hexdigest()


def new_json(path, obj):
    raw = (json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode()
    with path.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())


def main():
    start = time.monotonic()
    prereg = HERE / "T10_B_PRE_REG.json"
    plan = json.loads(prereg.read_bytes())
    assert plan["status"] == "PREREGISTERED_B1_B2_B3_B4"
    cfg_path = RING / "bis" / "e3_kerr_dtau_f_015" / "CONFIG.json"
    cfg = json.loads(cfg_path.read_bytes())
    assert sha(cfg_path) == plan["config_sha256"]
    assert sha(SOURCE / "strain_io.py") == plan["reader_sha256"]
    assert sha(RING / "cache" / "E3_KERR220_CALIBRATION_V1" / "welch" / "FAILURE.json") == plan["b1_failure_sha256"]
    fs = cfg["sample_rate_hz"]
    n = int(fs * cfg["analysis_duration_s"])
    ba = butter(4, [v / (fs * .5) for v in cfg["band_hz"]], btype="band")
    rows = []
    for detector in cfg["detectors"]:
        d = cfg["data"][detector]
        source = CHAT / d["offsource_path"]
        spec = dict(psd_duration_s=512, psd_segment_s=cfg["noise_chunk_s"],
                    offsource_exclusion_s=cfg["offsource_exclusion_s"],
                    event_GPS=cfg["trigger_GPS"], segment_start_GPS=cfg["read_start_GPS"],
                    quality_required=cfg["quality_required"],
                    injection_flags_required=cfg["injection_flags_required"])
        row = dict(detector=detector, source_sha256=d["offsource_sha256"],
                   b2_status="NOT_MEASURED", b3_status="NOT_NEEDED", b4_status="NOT_NEEDED")
        try:
            f, p, receipt = offsource_psd(source, d["offsource_sha256"], spec)
            row["psd_receipt"] = receipt
            _, transfer = freqz(*ba, worN=f, fs=fs)
            acf = .5 * fs * np.fft.irfft(p * abs(transfer)**4, n=2 * (len(f) - 1))
            cov = toeplitz(acf[:n]) / cfg["reference_amplitude"]**2
            eig = np.linalg.eigvalsh(cov)
            emin, emax = float(eig[0]), float(eig[-1])
            row["b2_eigen_min"] = emin
            row["b2_eigen_max"] = emax
            row["b2_condition"] = float(emax / emin) if emin > 0 else None
            if emin > 0 and emax / emin <= plan["conditioning_limit"]:
                cholesky(cov, lower=True, check_finite=True)
                row["b2_status"] = "ACCEPTED_COVARIANCE_DIAGNOSTIC_ONLY"
            else:
                row["b2_status"] = "REFUSED_CONDITIONING"
                # Pre-registered diagonal loading to an exact condition ceiling.
                floor = emax / plan["conditioning_limit"]
                loading = max(0.0, (floor - emin) / (1.0 - 1.0 / plan["conditioning_limit"]))
                loaded = cov + loading * np.eye(n)
                cholesky(loaded, lower=True, check_finite=True)
                row["b3_diagonal_loading"] = float(loading)
                row["b3_condition"] = float((emax + loading) / (emin + loading))
                row["b3_status"] = "REGULARIZED_INPUT_NOT_PHYSICAL_NO_PE"
        except Exception as exc:
            row["b2_status"] = "FAILED"
            row["b2_error"] = repr(exc)
            row["b3_status"] = "FAILED_OR_NOT_RUN"
        if row["b2_status"] != "ACCEPTED_COVARIANCE_DIAGNOSTIC_ONLY":
            row["b4_status"] = "EXISTING_PUBLIC_PSD_SYNTHETIC_T10_A_NOT_REAL_NO_NEW_RUN"
        rows.append(row)
    result = dict(status="T10_B_CONDITIONING_DIAGNOSTIC", nonblind=True,
                  created_utc=datetime.now(timezone.utc).isoformat(),
                  wall_seconds=time.monotonic()-start, n_samples=n, fs=fs,
                  rows=rows, prereg_sha256=sha(prereg),
                  scope="B2 512s median Welch, B3 only if B2 refused, B4 descriptive existing synthetic only",
                  no_PE=True, sigma_c=None, gate_changed=False)
    new_json(HERE / "T10_B_RESULT.json", result)
    print(json.dumps({"status": result["status"], "rows": rows, "wall_seconds": result["wall_seconds"]}))


if __name__ == "__main__":
    main()
