"""Apply the F4 whitened 10 tM window power definition event by event.

The detector peak for other events is the posterior median detector time,
while GW250114 uses the exact F4 registered reference. This difference is
declared in every row. Raw excess power is retained even when nonpositive.
"""
import hashlib
import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
import h5py
import numpy as np
from scipy.signal import periodogram

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from prepare_empirical_noise import polynomial_whitener  # reuse the pinned F4 algorithm
from tgl_ringdown_prediction import scales


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


PLAN_PATH = HERE / "T07_DOWNLOAD_PLAN_v3.json"
PLAN = json.loads(PLAN_PATH.read_bytes())
SUP_PLAN_PATH = HERE / "T07_SUPPLEMENT_PLAN.json"
SUP_PLAN = json.loads(SUP_PLAN_PATH.read_bytes())
ITEMS = PLAN["files"] + SUP_PLAN["files"]
BY_EVENT = {}
for item in ITEMS:
    BY_EVENT.setdefault(item["event"], {})[(item["role"], item["detector"])] = item
F4 = json.loads((ROOT / "REGISTRO_C6.json").read_bytes())
N = F4["interval_samples"]
assert N == 410
assert sha(ROOT / "prepare_empirical_noise.py")
assert sha(ROOT / "refeito" / "measure_power_gate_013bis_v2.py")
DEADLINE = datetime.fromisoformat("2026-09-27T10:28:21.3284588+00:00")


def posterior_reference(event):
    path = ROOT / "cache/public/21454847/extracted/pSEOB/metafiles" / f"pSEOB_{event}_Prod0.h5"
    if not path.exists():
        raise FileNotFoundError("Public posterior missing: " + str(path))
    with h5py.File(path, "r") as handle:
        groups = [key for key in handle if "posterior_samples" in handle[key]]
        if len(groups) != 1: raise ValueError("AMBIGUOUS_POSTERIOR_GROUP")
        data = handle[groups[0]+"/posterior_samples"]
        fields = data.dtype.names
        needed = ["final_mass_non_evolved"] + [f"{d}_time" for d in ("H1", "L1", "V1")]
        available = {key: np.asarray(data[key], dtype=float) for key in needed if key in fields}
    mass = available["final_mass_non_evolved"]
    mass = mass[np.isfinite(mass) & (mass > 0)]
    if len(mass) == 0:
        raise ValueError("NO_POSITIVE_REMNANT_MASS")
    references = {}
    for detector in ("H1", "L1", "V1"):
        key = f"{detector}_time"
        if key not in available:
            continue
        values = available[key]
        values = values[np.isfinite(values) & (values > 1e9)]
        if len(values):
            references[detector] = float(np.median(values))
    ref_method = "POSTERIOR_MEDIAN_DETECTOR_TIME_AND_REMNANT_MASS_PROXY_FOR_F4_PEAK"
    t_mass = float(scales(float(np.median(mass)), "CODATA2018_IAU2015")[0])
    if event == "GW250114_082203":
        references = F4["reference_peak_GPS"]
        t_mass = F4["reference_tM_seconds"]
        ref_method = "EXACT_F4_REGISTERED_PEAK_AND_TM"
    return path, references, t_mass, ref_method


def checked_file(item):
    path = HERE / item["relative_path"]
    receipt = path.with_name(path.name + ".receipt.json")
    if not path.exists() or not receipt.exists():
        raise FileNotFoundError("UNPAID_STRAIN_FILE:" + item["relative_path"])
    data = json.loads(receipt.read_bytes())
    if data["plan_sha256"] not in (sha(PLAN_PATH), sha(HERE / "T07_DOWNLOAD_PLAN.json"), sha(SUP_PLAN_PATH)) or data["url"] != item["url"]:
        raise ValueError("STRAIN_RECEIPT_PLAN_MISMATCH")
    if data["sha256"] != sha(path) or data["bytes"] != path.stat().st_size:
        raise ValueError("STRAIN_RECEIPT_HASH_MISMATCH")
    return path, sha(receipt)


def quality_good(handle):
    quality = np.asarray(handle["quality/simple/DQmask"][:], dtype=int)
    injections = np.asarray(handle["quality/injections/Injmask"][:], dtype=int)
    qnames = [v.decode() if isinstance(v, bytes) else str(v) for v in handle["quality/simple/DQShortnames"][:]]
    inames = [v.decode() if isinstance(v, bytes) else str(v) for v in handle["quality/injections/InjShortnames"][:]]
    qneeded = ("DATA", "CBC_CAT1", "CBC_CAT2", "CBC_CAT3")
    ineeded = ("NO_CBC_HW_INJ", "NO_BURST_HW_INJ", "NO_DETCHAR_HW_INJ", "NO_STOCH_HW_INJ")
    qmask = sum(1 << qnames.index(key) for key in qneeded)
    imask = sum(1 << inames.index(key) for key in ineeded)
    return ((quality & qmask) == qmask) & ((injections & imask) == imask)


def fit_noise(path):
    with h5py.File(path, "r") as handle:
        start = float(handle["meta/GPSstart"][()])
        strain = handle["strain/Strain"]
        fs = 1 / float(strain.attrs["Xspacing"])
        if fs != 4096:
            raise ValueError("UNEXPECTED_FS")
        good = quality_good(handle)
        train = np.asarray(strain[:2048 * 4096], dtype=float) * 1e21
        if not np.all(np.isfinite(train)):
            raise ValueError("NONFINITE_TRAIN")
        spectra = []
        for second in range(0, 2048 - 4 + 1, 2):
            if not np.all(good[second:second + 4]):
                continue
            _, psd = periodogram(train[second * 4096:(second + 4) * 4096], fs=4096,
                                 window="hann", detrend="constant", scaling="density")
            spectra.append(psd)
        if len(spectra) < 512:
            raise ValueError("INSUFFICIENT_CLEAN_4S_PSD_WINDOWS:" + str(len(spectra)))
        spectra = np.asarray(spectra)
        even = 2 * np.arange(1, (len(spectra) - 1) // 2 + 1)
        median_bias = 1 + np.sum(1 / (even + 1) - 1 / even)
        median = np.median(spectra, axis=0) / median_bias
        if np.any(median <= 0):
            raise ValueError("NONPOSITIVE_PSD")
        W, dcov, inverse = polynomial_whitener(median, 4096, N)
        residual = float(np.max(abs(inverse @ dcov @ inverse.T - np.eye(len(W)))))
        if residual > 1e-5:
            raise ValueError("WHITENING_RESIDUAL:" + str(residual))
        # F4's held-out segment scheme diagnoses off-source stationarity.
        chis = []
        for second in range(2048, 4094, 8):
            if not good[second]:
                continue
            begin = second * 4096 + 1536
            y = np.asarray(strain[begin:begin + 2 * N:2], dtype=float) * 1e21
            if len(y) == N and np.all(np.isfinite(y)):
                z = W @ y
                chis.append(float(z @ z / len(W)))
        return W, {"offsource_gps_start": start, "training_windows": len(spectra),
                   "whitening_residual": residual, "held_out_count": len(chis),
                   "held_out_reduced_chisquare_median": float(np.median(chis)) if chis else None}


def measure_on(path, W, requested):
    with h5py.File(path, "r") as handle:
        gps0 = float(handle["meta/GPSstart"][()])
        raw = handle["strain/Strain"]
        fs = 1 / float(raw.attrs["Xspacing"])
        if fs != 4096:
            raise ValueError("UNEXPECTED_ONSOURCE_FS")
        first = math.ceil((requested - gps0) * fs)
        if first < 0 or first + 2 * N > len(raw):
            raise ValueError("RHO_WINDOW_OUTSIDE_STRAIN")
        y = np.asarray(raw[first:first + 2 * N:2], dtype=float) * 1e21
    z = W @ y
    return float(z @ z), first, gps0 + first / 4096


def measure(event):
    rows = []
    skipped_detectors = []
    posterior, refs, tm, ref_method = posterior_reference(event)
    for (role, detector), on_item in BY_EVENT[event].items():
        if role != "onsource":
            continue
        off_item = BY_EVENT[event][("offsource", detector)]
        if detector not in refs:
            skipped_detectors.append({"detector": detector, "reason": "NO_FINITE_DETECTOR_TIME_IN_PUBLIC_POSTERIOR"})
            continue
        on_path, on_receipt = checked_file(on_item)
        off_path, off_receipt = checked_file(off_item)
        W, noise = fit_noise(off_path)
        requested = refs[detector] + 10 * tm
        norm, index, actual = measure_on(on_path, W, requested)
        rows.append({"detector": detector, "norm_squared": norm,
                     "noise_degrees_of_freedom": W.shape[0],
                     "requested_GPS": requested, "first_index": index,
                     "first_sample_GPS": actual,
                     "onsource_sha256": sha(on_path), "offsource_sha256": sha(off_path),
                     "onsource_receipt_sha256": on_receipt,
                     "offsource_receipt_sha256": off_receipt,
                     **noise})
    if not rows: raise ValueError("NO_DETECTOR_WITH_PUBLIC_TIME")
    dof = sum(row["noise_degrees_of_freedom"] for row in rows)
    excess = sum(row["norm_squared"] for row in rows) - dof
    rho = math.sqrt(excess) if excess > 0 else None
    se = math.sqrt(2 * dof + 4 * excess) / (2 * rho) if rho and 2 * dof + 4 * excess > 0 else None
    result = {
        "status": "MEASURED_POSITIVE_POWER_EXCESS" if rho is not None else "MEASURED_NONPOSITIVE_POWER_EXCESS_NO_REAL_RHO",
        "event": event, "reference_method": ref_method,
        "posterior_sha256": sha(posterior), "reference_tM_seconds": tm,
        "start_tM": 10, "detectors": rows, "skipped_detectors": skipped_detectors,
        "excess_norm_squared": excess, "rho_power_estimate": rho,
        "approximate_standard_error_if_white_gaussian": se,
        "statistical_scope": "Whitened finite-window power excess minus noise dof, as F4; not matched-filter SNR or detection significance. Gaussian stationary uncertainty only; event-to-event PSD systematics not included.",
        "gate_changed": False,
    }
    return result


def main():
    out_dir = HERE / "results_rho"
    out_dir.mkdir(exist_ok=True)
    rows = []
    events = list(BY_EVENT)
    for event in events:
        if datetime.now(timezone.utc) >= DEADLINE:
            rows.append({"event": event, "status": "T07_DEADLINE_NOT_MEASURED"})
            continue
        started = time.monotonic()
        try:
            result = measure(event)
            raw = (json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
            path = out_dir / (event + ".json")
            with path.open("xb") as handle:
                handle.write(raw)
            summary = {"event": event, "status": result["status"],
                       "rho": result["rho_power_estimate"],
                       "excess": result["excess_norm_squared"],
                       "result_sha256": hashlib.sha256(raw).hexdigest()}
        except Exception as exc:
            summary = {"event": event, "status": "MEASUREMENT_FAILED",
                       "error": type(exc).__name__ + ":" + str(exc)[:240]}
        summary["wall_seconds"] = time.monotonic() - started
        rows.append(summary)
        print(json.dumps(summary), flush=True)
    report = {"status": "T07_RHO_POWER_CATALOG_ATTEMPT", "created_utc": datetime.now(timezone.utc).isoformat(),
              "plan_sha256": sha(PLAN_PATH), "runner_sha256": sha(Path(__file__)),
              "F4_source_sha256": sha(ROOT / "refeito" / "measure_power_gate_013bis_v2.py"),
              "noise_algorithm_sha256": sha(ROOT / "prepare_empirical_noise.py"),
              "rows": rows, "excluded_events": [r for r in PLAN["skipped"] if r["event"] not in {"GW150914_095045", "GW231206_233901"}], "supplement_plan_sha256": sha(SUP_PLAN_PATH), "gate_changed": False}
    path = HERE / "T07_RHO_CATALOG_RESULT_v5.json"
    raw = (json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    with path.open("xb") as handle:
        handle.write(raw)
    print(json.dumps({"catalog_sha256": hashlib.sha256(raw).hexdigest(),
                      "measured": sum(r["status"].startswith("MEASURED_") for r in rows),
                      "errors": sum(r["status"] == "MEASUREMENT_FAILED" for r in rows)}))


if __name__ == "__main__":
    main()
