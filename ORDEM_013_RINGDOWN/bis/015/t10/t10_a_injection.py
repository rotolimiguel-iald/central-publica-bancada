"""Pre-registered T10-A diagnostic injection; never alters the Kerr F source."""
import os
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"

import argparse
import hashlib
import json
import math
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.linalg import cholesky, solve_triangular, toeplitz

HERE = Path(__file__).resolve().parent
RING = HERE.parents[2]
CHATGPT = RING.parent
SOURCE = RING / "bis" / "e3_kerr_dtau_f_015"
sys.path.insert(0, str(SOURCE))
from conditioning import public_psd_acf
from kerr_model import PARAMETERS, frequency_tau, geometry, make_likelihood, polarizations


def digest(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def write_new(path, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    with path.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    assert digest(path) == hashlib.sha256(raw).hexdigest()


def checked_inputs():
    pre = HERE / "T10_A_PRE_REG.json"
    cfg_path = SOURCE / "CONFIG.json"
    model = SOURCE / "kerr_model.py"
    conditioning = SOURCE / "conditioning.py"
    pre_data = json.loads(pre.read_bytes())
    cfg = json.loads(cfg_path.read_bytes())
    assert pre_data["status"] == "PRE_REGISTERED_DIAGNOSTIC_NOT_BANK"
    assert cfg["model"] == "Kerr220_two_independent_complex_branches_dtau220_diagnostic"
    pins = {str(p.relative_to(CHATGPT)): digest(p) for p in (pre, cfg_path, model, conditioning)}
    for detector in cfg["detectors"]:
        entry = cfg["public_psd"][detector]
        path = CHATGPT / entry["relative_to_Chatgpt"]
        assert digest(path) == entry["sha256"]
        pins[str(path.relative_to(CHATGPT))] = digest(path)
    assert pre_data["seed"] == 15260410
    return pre_data, cfg, pins


def base_blocks(cfg):
    import lal
    n = int(cfg["analysis_duration_s"] * cfg["sample_rate_hz"])
    assert n == 819
    fs = cfg["sample_rate_hz"]
    blocks = []
    for name in cfg["detectors"]:
        obj, delay, gmst = geometry(name, cfg)
        entry = cfg["public_psd"][name]
        acf = public_psd_acf(CHATGPT / entry["relative_to_Chatgpt"], cfg)
        cov = toeplitz(acf[:n]) / cfg["reference_amplitude"] ** 2
        cond = float(np.linalg.cond(cov))
        if not math.isfinite(cond) or cond > 1e12:
            raise ValueError("PSD covariance conditioning refused")
        chol = cholesky(cov, lower=True, check_finite=True)
        times = cfg["start_offset_s"] + np.arange(n) / fs
        blocks.append(dict(name=name, data=np.zeros(n), relative_times=times,
                           response=obj.response, gmst=gmst,
                           cholesky_scaled=chol, log_normalization=0.0,
                           covariance_condition_number=cond,
                           delay_relative_to_H1_s=delay))
    return blocks


def model_strain(block, cfg, x):
    import lal
    mass_time = lal.G_SI * lal.MSUN_SI / lal.C_SI ** 3
    hp, hc = polarizations(block["relative_times"], x, cfg, mass_time)
    fp, fc = lal.ComputeDetAMResponse(block["response"], cfg["ra"], cfg["dec"], x["psi"], block["gmst"])
    return fp * hp + fc * hc


def prepared():
    pre, cfg, pins = checked_inputs()
    inj = pre["injection"]
    x = dict(psi=inj["psi"], Mf=inj["Mf_detector_solar"], af=inj["af"],
             cosiota=inj["cosiota"], A2220_1=inj["A2220_1_unscaled"],
             A2220_2=inj["A2220_2_unscaled"], phi2220_1=inj["phi2220_1"],
             phi2220_2=inj["phi2220_2"], dtau220=inj["dtau220"])
    assert set(x) == set(PARAMETERS)
    blocks = base_blocks(cfg)
    base_norm = math.sqrt(sum(float(np.dot(y, y)) for y in (
        solve_triangular(b["cholesky_scaled"], model_strain(b, cfg, x) / cfg["reference_amplitude"], lower=True)
        for b in blocks)))
    factor = inj["target_optimal_network_snr"] / base_norm
    x["A2220_1"] *= factor
    x["A2220_2"] *= factor
    if max(x["A2220_1"], x["A2220_2"]) > cfg["priors"]["A2220_1"][1]:
        raise ValueError("Injection outside amplitude prior")
    rng = np.random.default_rng(pre["seed"])
    arrays = {}
    for b in blocks:
        noise = cfg["reference_amplitude"] * b["cholesky_scaled"] @ rng.standard_normal(len(b["relative_times"]))
        b["data"] = model_strain(b, cfg, x) + noise
        arrays["data_" + b["name"]] = b["data"]
    out = HERE / "T10_A_INJECTION.npz"
    with out.open("xb") as stream:
        np.savez_compressed(stream, **arrays)
        stream.flush()
        os.fsync(stream.fileno())
    receipt = dict(status="PREPARED_NONBLIND_DIAGNOSTIC", created_utc=datetime.now(timezone.utc).isoformat(),
                   input_pins=pins, injection_parameters=x, scale_factor=factor,
                   base_optimal_snr=base_norm, target_optimal_snr=inj["target_optimal_network_snr"],
                   data_sha256=digest(out), detectors=[dict(name=b["name"],
                   covariance_condition_number=b["covariance_condition_number"]) for b in blocks],
                   scope="synthetic Gaussian-colored public PSD, not real off-source noise, not bank, not sigma_c")
    write_new(HERE / "T10_A_PREPARED.json", receipt)
    print(json.dumps({"status": receipt["status"], "data_sha256": receipt["data_sha256"],
                      "amplitudes": [x["A2220_1"], x["A2220_2"]], "base_snr": base_norm}))


def fit(variant):
    import bilby
    from scipy.stats import norm
    pre, cfg, pins = checked_inputs()
    receipt_path = HERE / "T10_A_PREPARED.json"
    receipt = json.loads(receipt_path.read_bytes())
    if receipt["input_pins"] != pins or receipt["data_sha256"] != digest(HERE / "T10_A_INJECTION.npz"):
        raise ValueError("Injection custody changed")
    blocks = base_blocks(cfg)
    with np.load(HERE / "T10_A_INJECTION.npz") as arrays:
        for b in blocks:
            b["data"] = np.asarray(arrays["data_" + b["name"]], float)
    start = time.monotonic()
    cap = pre["hard_cap_hours_each"] * 3600
    def guard():
        if time.monotonic() - start >= cap - 30:
            raise TimeoutError("T10-A own hard cap")
    likelihood = make_likelihood(blocks, cfg, guard)
    original_log_likelihood = likelihood.log_likelihood
    def safe_log_likelihood(parameters=None):
        try:
            return original_log_likelihood(parameters)
        except ValueError as error:
            if str(error).startswith(("Invalid detector remnant", "Invalid inclination", "Invalid dtau220")):
                return -np.inf
            raise
    likelihood.log_likelihood = safe_log_likelihood
    prior = bilby.core.prior.PriorDict()
    for key, limits in cfg["priors"].items():
        if variant == "informed" and key in ("Mf", "af"):
            continue
        kwargs = {"boundary": "periodic"} if key in ("psi", "phi2220_1", "phi2220_2") else {}
        prior[key] = bilby.core.prior.Uniform(*limits, name=key, **kwargs)
    if variant == "informed":
        dist = bilby.core.prior.MultivariateGaussianDist(
            names=["Mf", "af"], mus=pre["informed_prior_mu"],
            covs=pre["informed_prior_covariance"])
        for key in ("Mf", "af"):
            prior[key] = bilby.core.prior.MultivariateGaussian(dist, name=key)
    assert set(prior) == set(PARAMETERS)
    seed = pre["seed"] + (1 if variant == "free" else 2)
    bilby.core.utils.random.seed(seed)
    np.random.seed(seed)
    output = HERE / ("fit_" + variant)
    output.mkdir(exist_ok=False)
    write_new(output / "START.json", dict(status="RUNNING_DIAGNOSTIC", variant=variant,
              start_utc=datetime.now(timezone.utc).isoformat(), seed=seed,
              prep_sha256=digest(receipt_path), data_sha256=receipt["data_sha256"],
              input_pins=pins, hard_cap_seconds=cap))
    def alarm_handler(_signal, _frame):
        raise TimeoutError("T10-A alarm hard cap")
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(int(cap))
    status = "FAILED_NO_POSTERIOR"
    error = None
    result = None
    try:
        s = pre["sampler"]
        result = bilby.run_sampler(likelihood=likelihood, priors=prior, sampler="dynesty",
                label="T10_A_" + variant, outdir=str(output), save="hdf5", plot=False,
                npool=1, nlive=s["nlive"], sample="rwalk", walks=s["walks"],
                maxcall=s["maxcall"], dlogz=s["dlogz"], seed=seed,
                resume=False, check_point=False, check_point_plot=False,
                print_progress=False, use_ratio=False)
        posterior = result.posterior
        if "dtau220" not in posterior or len(posterior) < 100:
            raise ValueError("Insufficient posterior samples")
        vals = np.asarray(posterior["dtau220"], float)
        if not np.isfinite(vals).all():
            raise ValueError("Nonfinite posterior")
        status = "DESCRIPTIVE_POSTERIOR_REQUIRES_REVIEW"
        posterior_summary = dict(n=int(len(vals)), mean=float(np.mean(vals)),
              sigma_inj_single_realization=float(np.std(vals, ddof=1)),
              q05_q50_q95=np.quantile(vals, [.05, .5, .95]).tolist())
    except Exception as exc:
        error = repr(exc)
        posterior_summary = None
    finally:
        signal.alarm(0)
        write_new(output / "RESULT.json", dict(status=status, variant=variant,
            finish_utc=datetime.now(timezone.utc).isoformat(), wall_seconds=time.monotonic()-start,
            error=error, posterior=posterior_summary,
            log_evidence=float(result.log_evidence) if result is not None else None,
            prep_sha256=digest(receipt_path), data_sha256=receipt["data_sha256"],
            gate_changed=False, sigma_c_eligible=False))
    print(json.dumps({"status": status, "variant": variant, "posterior": posterior_summary,
                      "error": error}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "free", "informed"))
    args = parser.parse_args()
    if args.command == "prepare":
        prepared()
    else:
        fit(args.command)
