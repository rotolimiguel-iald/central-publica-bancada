"""Summarize the accepted F posterior descriptively, without significance."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import numpy as np

here = Path(__file__).resolve().parent
ring = here.parents[2]
run = ring / "cache" / "E3_KERR220_DTAU_F_015"
data = run / "public_psd"
outdir = here / "branch_f"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    posterior = data / "PAIRED_POSTERIOR.npz"
    convergence = data / "CONVERGENCE.json"
    comparison = data / "COMPARISON.json"
    conv = json.loads(convergence.read_bytes())
    cmp = json.loads(comparison.read_bytes())
    assert conv["accepted_for_analysis"] is True
    assert cmp["sigma_eligible"] is False and cmp["z_calibrated"] is None
    assert cmp["posterior_sha256"] == sha(posterior)
    with np.load(posterior, allow_pickle=False) as arrays:
        assert set(arrays.files) == set(cmp["parameter_order"])
        d = np.asarray(arrays["dtau220"], dtype=float)
        mass = np.asarray(arrays["Mf"], dtype=float)
        spin = np.asarray(arrays["af"], dtype=float)
        assert len(d) == conv["posterior_samples"] == cmp["samples"]
        assert np.isfinite(d).all() and np.isfinite(mass).all() and np.isfinite(spin).all()
        assert np.all((-0.8 <= d) & (d <= 2))
        result = {
            "status": "DESCRIPTIVE_DIAGNOSTIC_NOT_SIGMA",
            "event": "GW250114_082203",
            "samples": int(len(d)),
            "dtau220_q05_q50_q95": np.quantile(d, [0.05, 0.5, 0.95]).tolist(),
            "dtau220_mean": float(np.mean(d)),
            "corr_dtau220_Mf": float(np.corrcoef(d, mass)[0, 1]),
            "corr_dtau220_af": float(np.corrcoef(d, spin)[0, 1]),
            "fraction_within_0p05_of_lower_prior_edge": float(np.mean(d < -0.75)),
            "fraction_within_0p05_of_upper_prior_edge": float(np.mean(d > 1.95)),
            "single_220_free_Mf_af_not_identifiable": True,
            "sigma_eligible": False,
            "z_calibrated": None,
            "input_sha256": {"posterior": sha(posterior), "convergence": sha(convergence),
                             "comparison": sha(comparison)},
            "script_sha256": sha(Path(__file__).resolve()),
        }
    outdir.mkdir(exist_ok=True)
    target = outdir / "DIAGNOSTIC.json"
    raw = (json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    with target.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert target.read_bytes() == raw
    print(json.dumps({"status": result["status"], "sha256": sha(target),
                      "samples": result["samples"], "q": result["dtau220_q05_q50_q95"]}))


if __name__ == "__main__":
    main()
