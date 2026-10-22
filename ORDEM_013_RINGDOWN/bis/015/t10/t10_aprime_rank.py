"""T10-A' local spectral-Jacobian diagnostic from the existing 220/440 grid."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
GRID = HERE.parents[2] / "QNM_GRID.json"
OUT = HERE / "T10_APRIME_SPECTRAL_RANK.json"
SPIN = 0.7519521363178578


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    data = json.loads(GRID.read_bytes())
    values = np.asarray(data["spins"], dtype=float)
    if not np.all(np.diff(values) > 0) or not values[0] < SPIN < values[-1]:
        raise ValueError("Invalid spin grid")
    derivs = {}
    for key in ("220", "440"):
        record = data["modes"][key]
        real = np.asarray(record["real"], dtype=float)
        imag = np.asarray(record["imag"], dtype=float)
        if len(real) != len(values) or len(imag) != len(values) or not np.all(imag < 0):
            raise ValueError("Invalid QNM mode")
        f = CubicSpline(values, real, extrapolate=False)
        decay = CubicSpline(values, -imag, extrapolate=False)
        derivs[key] = dict(log_f=float(f(SPIN, 1) / f(SPIN)),
                           log_tau=float(-decay(SPIN, 1) / decay(SPIN)),
                           dimensionless_frequency=float(f(SPIN)),
                           dimensionless_decay=float(decay(SPIN)))
    u = derivs["220"]
    v = derivs["440"]
    # Coordinates (log M, a, d); d=0. The third column belongs to tau220 only.
    jac = np.asarray([[-1, u["log_f"], 0],
                      [1, u["log_tau"], 1],
                      [-1, v["log_f"], 0],
                      [1, v["log_tau"], 0]], dtype=float)
    s = np.linalg.svd(jac, compute_uv=False)
    minors = {"f220_tau220_f440": float(np.linalg.det(jac[[0, 1, 2], :])),
              "f220_tau220_tau440": float(np.linalg.det(jac[[0, 1, 3], :]))}
    result = dict(status="LOCAL_SPECTRAL_RANK_ONLY_NOT_DATA_IDENTIFIABILITY",
                  created_utc=datetime.now(timezone.utc).isoformat(),
                  source_grid_sha256=sha(GRID), spin=SPIN, mode_derivatives=derivs,
                  jacobian_rows=["log_f220", "log_tau220", "log_f440", "log_tau440"],
                  jacobian_columns=["log_M", "a", "dtau220"],
                  jacobian=jac.tolist(), singular_values=s.tolist(),
                  rank_tolerance=float(1e-10 * s[0]), rank=int(np.sum(s > 1e-10 * s[0])),
                  minors=minors,
                  limitations=["Mode440 amplitudes, phases and noise absent from this Jacobian",
                               "No posterior, injection recovery or Fisher data metric computed",
                               "Local rank at one spin does not prove global identifiability",
                               "No pSEOB transfer; no sigma_c or gate movement"])
    raw = (json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    with OUT.open("xb") as handle:
        handle.write(raw)
    print(json.dumps({"rank": result["rank"], "minors": minors,
                      "smallest_singular_value": float(s[-1]), "sha256": sha(OUT)}))


if __name__ == "__main__":
    main()
