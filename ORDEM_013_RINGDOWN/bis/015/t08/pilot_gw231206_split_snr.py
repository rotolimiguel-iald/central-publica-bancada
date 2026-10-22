"""Source-controlled split *optimal* waveform SNR pilot; no catalog claim."""
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import h5py
import lal
import numpy as np
from pycbc.detector import Detector
from pycbc.waveform import get_fd_waveform

HERE = Path(__file__).resolve().parent
EVENT = "GW231206_233901"
SOURCE = next(HERE.glob("*GW231206_233901*combined_PEDataRelease.hdf5"))
RECEIPT = HERE / "GW231206_GR_PE_DOWNLOAD_RECEIPT.json"
expected = json.loads(RECEIPT.read_bytes())
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == expected["sha256"]

with h5py.File(SOURCE, "r") as h5:
    group = h5["C00:IMRPhenomXPHM-SpinTaylor"]
    posterior = group["posterior_samples"][:]
    score = posterior["log_likelihood"] + posterior["log_prior"]
    index = int(np.nanargmax(score))
    sample = posterior[index]
    meta = group["meta_data/meta_data"]
    low = float(meta["f_low"][()][0])
    ref = float(meta["f_ref"][()][0])
    high = float(meta["f_final"][()][0])
    df = float(meta["delta_f"][()][0])
    psds = {detector: np.asarray(group["psds"][detector]) for detector in ("H1", "L1")}

a = float(sample["final_spin_non_evolved"])
mrem = float(sample["final_mass_non_evolved"])
assert 0 <= a < 1 and mrem > 0
z1 = 1 + (1-a*a)**(1/3) * ((1+a)**(1/3) + (1-a)**(1/3))
z2 = math.sqrt(3*a*a + z1*z1)
risco = 3 + z2 - math.sqrt((3-z1)*(3+z1+2*z2))
fcut = 1 / (math.pi * mrem * lal.MTSUN_SI * (risco**1.5 + a))

hp, hc = get_fd_waveform(
    approximant="IMRPhenomXPHM",
    mass1=float(sample["mass_1"]), mass2=float(sample["mass_2"]),
    spin1x=float(sample["spin_1x"]), spin1y=float(sample["spin_1y"]),
    spin1z=float(sample["spin_1z"]), spin2x=float(sample["spin_2x"]),
    spin2y=float(sample["spin_2y"]), spin2z=float(sample["spin_2z"]),
    distance=float(sample["luminosity_distance"]),
    inclination=float(sample["iota"]), coa_phase=float(sample["phase"]),
    delta_f=df, f_lower=low, f_final=high, f_ref=ref)

frequencies = np.arange(len(hp), dtype=float) * df
valid = (frequencies >= low) & (frequencies <= high)
parts = {"inspiral": valid & (frequencies < fcut),
         "postinspiral": valid & (frequencies >= fcut), "total": valid}
detectors = {}
for name, noise in psds.items():
    assert noise.shape[1] == 2
    n = min(len(noise), len(hp))
    assert (n - 1) * df >= high
    assert np.max(np.abs(noise[:n, 0] - frequencies[:n])) < 1e-8
    sn = noise[:n, 1]
    assert np.all(np.isfinite(sn[valid[:n]])) and np.all(sn[valid[:n]] > 0)
    fp, fc = Detector(name).antenna_pattern(float(sample["ra"]), float(sample["dec"]),
                                             float(sample["psi"]), float(sample["geocent_time"]))
    strain = fp * np.asarray(hp[:n]) + fc * np.asarray(hc[:n])
    power = 4 * df * np.abs(strain)**2 / sn
    detectors[name] = {k: float(np.sqrt(np.sum(power[mask[:n]]))) for k, mask in parts.items()}

network = {part: float(np.sqrt(sum(detectors[name][part]**2 for name in detectors)))
           for part in parts}
assert all(math.isfinite(v) for v in network.values())
assert abs(network["total"]**2 - network["inspiral"]**2 - network["postinspiral"]**2) < 1e-6
result = {
    "status": "T08_PILOT_WAVEFORM_OPTIMAL_SPLIT_SNR_NOT_YET_VALIDATED_AGAINST_LVK",
    "created_utc": datetime.now(timezone.utc).isoformat(), "event": EVENT,
    "source_sha256": expected["sha256"], "download_receipt_sha256": hashlib.sha256(RECEIPT.read_bytes()).hexdigest(),
    "posterior_group": "C00:IMRPhenomXPHM-SpinTaylor", "max_sample_log_posterior_index": index,
    "max_sample_log_likelihood": float(sample["log_likelihood"]),
    "max_sample_log_prior": float(sample["log_prior"]),
    "source_waveform_approximant": "IMRPhenomXPHM", "PSD_source": "same LVK public PE HDF5",
    "f_low_Hz": low, "f_ref_Hz": ref, "f_high_Hz": high, "delta_f_Hz": df,
    "f_cut_Kerr_ISCO_Hz": fcut, "f_cut_source": "Kerr remnant ISCO computed from max-sample final_mass_non_evolved/final_spin_non_evolved; not GWTC4 posterior-median cutoff",
    "remnant_mass_detector_Msun": mrem, "remnant_spin": a,
    "detector_optimal_snr": detectors, "network_optimal_snr": network,
    "LVK_posterior_sample_network_optimal_snr": float(sample["network_optimal_snr"]),
    "LVK_GWTC4_Table7_fcut_Hz": 113.0,
    "LVK_GWTC4_Table7_rho_full": 21.9,
    "LVK_GWTC4_Table7_rho_inspiral": 16.5,
    "LVK_GWTC4_Table7_rho_postinspiral": 14.4,
    "LVK_table_source": "https://arxiv.org/pdf/2603.19019",
    "interpretation": "Formula computes optimal template norm, not observed matched-filter projection. Calibration marginalization, waveform conventions, MAP selection, window cutoff and PSD versions can differ from LVK Table 7; compare before acceptance.",
    "gate_changed": False,
}
path = HERE / "GW231206_SPLIT_SNR_PILOT.json"
with path.open("xb") as stream:
    stream.write((json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode())
print(json.dumps({"result_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                  "cutoff_Hz": fcut, "network": network,
                  "posterior_sample_network_optimal_snr": result["LVK_posterior_sample_network_optimal_snr"]}))
