"""Read the two completed posterior files; descriptive checks only."""
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import bilby
import numpy as np

HERE = Path(__file__).resolve().parent
PRE = json.loads((HERE / "T10_A_PRE_REG.json").read_bytes())
OUT = HERE / "T10_A_POSTERIOR_AUDIT.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summary(values):
    arr = np.asarray(values, float)
    if len(arr) < 100 or not np.isfinite(arr).all():
        raise ValueError("Invalid posterior samples")
    return dict(n=int(len(arr)), mean=float(arr.mean()), std=float(arr.std(ddof=1)),
                q05_q50_q95=np.quantile(arr, [.05, .5, .95]).tolist())


def main():
    paths = {name: HERE / ("fit_" + name) / ("T10_A_" + name + "_result.hdf5")
             for name in ("free", "informed_latent_v2")}
    results = {}
    for name, path in paths.items():
        result = bilby.result.read_in_result(filename=str(path))
        d = np.asarray(result.posterior["dtau220"], float)
        item = dict(hdf5_sha256=sha(path), delta_tau=summary(d),
                    log_evidence=float(result.log_evidence),
                    log_evidence_err=float(result.log_evidence_err),
                    sampler=str(result.sampler),
                    num_likelihood_evaluations=int(result.num_likelihood_evaluations))
        if name == "free":
            mf = np.asarray(result.posterior["Mf"], float)
            af = np.asarray(result.posterior["af"], float)
        else:
            z = np.column_stack((np.asarray(result.posterior["zMf"], float),
                                 np.asarray(result.posterior["zAf"], float)))
            physical = np.asarray(PRE["informed_prior_mu"], float) + z @ np.linalg.cholesky(
                        np.asarray(PRE["informed_prior_covariance"], float)).T
            mf, af = physical.T
        item.update(Mf=summary(mf), af=summary(af),
                    corr_d_Mf=float(np.corrcoef(d, mf)[0, 1]),
                    corr_d_af=float(np.corrcoef(d, af)[0, 1]),
                    delta_true_in_90pct=bool(np.quantile(d, .05) <= 0 <= np.quantile(d, .95)),
                    fraction_near_delta_prior_lower=float(np.mean(d < -0.75)),
                    fraction_near_delta_prior_upper=float(np.mean(d > 1.95)))
        results[name] = item
    std_ratio = results["free"]["delta_tau"]["std"] / results["informed_latent_v2"]["delta_tau"]["std"]
    receipt = dict(status="DESCRIPTIVE_TWO_PRIOR_COMPARISON_NOT_SIGMA_C",
                   created_utc=datetime.now(timezone.utc).isoformat(),
                   pre_registration_sha256=sha(HERE / "T10_A_PRE_REG.json"),
                   injection_sha256=sha(HERE / "T10_A_INJECTION.npz"),
                   free_to_informed_delta_std_ratio=float(std_ratio),
                   variants=results,
                   limitations=["one Gaussian-noise realization only; posterior SD is not ensemble recovery scatter",
                                "prior-informed fit changes the observable to IMR-RD and needs operator ratification",
                                "no pSEOB transfer, no sigma_c, no physical significance", 
                                "Bayes evidences cannot be treated as independent-event evidence or a TGL-vs-GR comparison"],
                   gate_changed=False)
    data = (json.dumps(receipt, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    with OUT.open("xb") as stream:
        stream.write(data)
    print(json.dumps({"sha256": sha(OUT), "ratio": std_ratio,
                      "free_std": results["free"]["delta_tau"]["std"],
                      "informed_std": results["informed_latent_v2"]["delta_tau"]["std"]}))


if __name__ == "__main__":
    main()
