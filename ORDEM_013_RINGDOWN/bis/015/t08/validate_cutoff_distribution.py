"""Compare source-defined posterior-median Kerr ISCO split with Table 7."""
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import h5py
import lal
import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = next(HERE.glob("*GW231206_233901*combined_PEDataRelease.hdf5"))
PILOT = HERE / "GW231206_SPLIT_SNR_PILOT.json"
with h5py.File(SOURCE, "r") as h5:
    x = h5["C00:IMRPhenomXPHM-SpinTaylor/posterior_samples"][:]
a = np.asarray(x["final_spin_non_evolved"])
m = np.asarray(x["final_mass_non_evolved"])
valid = np.isfinite(a) & np.isfinite(m) & (a >= 0) & (a < 1) & (m > 0)
assert valid.sum() > 10000
a = a[valid]
m = m[valid]
z1 = 1 + np.cbrt(1-a*a) * (np.cbrt(1+a) + np.cbrt(1-a))
z2 = np.sqrt(3*a*a + z1*z1)
risco = 3 + z2 - np.sqrt((3-z1)*(3+z1+2*z2))
fcut = 1/(np.pi*m*lal.MTSUN_SI*(risco**1.5+a))
pilot = json.loads(PILOT.read_bytes())
ml = int(np.nanargmax(x["log_likelihood"]))
map_sample = int(np.nanargmax(x["log_likelihood"] + x["log_prior"]))
result = {
    "status": "T08_SOURCE_CUTOFF_DISTRIBUTION_MEASURED_ON_ONE_PUBLIC_PE_PRODUCT",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "source_sha256": pilot["source_sha256"],
    "pilot_sha256": hashlib.sha256(PILOT.read_bytes()).hexdigest(),
    "n_posterior_samples": int(len(x)), "n_valid_remnants": int(valid.sum()),
    "posterior_median_Kerr_ISCO_Hz": float(np.median(fcut)),
    "posterior_05_95_Kerr_ISCO_Hz": [float(v) for v in np.quantile(fcut, [0.05, 0.95])],
    "max_sample_logposterior_index": map_sample,
    "max_sample_likelihood_index": ml,
    "max_sample_logposterior_recorded_network_optimal_snr": float(x["network_optimal_snr"][map_sample]),
    "max_sample_likelihood_recorded_network_optimal_snr": float(x["network_optimal_snr"][ml]),
    "published_GWTC4_Table7_cutoff_Hz": 113.0,
    "source_url": "https://arxiv.org/pdf/2603.19019",
    "interpretation": "Posterior-median cutoff follows current GWTC4 convention, but this catalog PE product may differ from the IMRCT product; agreement is descriptive, not identity of pipelines.",
    "gate_changed": False,
}
path = HERE / "GW231206_CUTOFF_VALIDATION.json"
with path.open("xb") as stream:
    stream.write((json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode())
print(json.dumps({"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                  "posterior_median_Hz": result["posterior_median_Kerr_ISCO_Hz"],
                  "published_Hz": result["published_GWTC4_Table7_cutoff_Hz"]}))
