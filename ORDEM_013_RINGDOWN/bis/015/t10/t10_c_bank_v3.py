"""Generate the preregistered T10-C synthetic GR bank without fitting."""
import hashlib
import json
import math
import os
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[variable] = "1"

import numpy as np
from scipy.linalg import cholesky, solve_triangular, toeplitz

HERE = Path(__file__).resolve().parent
RING = HERE.parents[2]
CHAT = RING.parent
sys.path.insert(0, str(RING / "bis" / "e3_kerr_dtau_f_015"))
from conditioning import public_psd_acf
from kerr_model import geometry


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


def reference_blocks(cfg):
    import lal
    n = int(cfg["sample_rate_hz"] * cfg["analysis_duration_s"])
    blocks = []
    for name in cfg["detectors"]:
        obj, delay, gmst = geometry(name, cfg)
        item = cfg["public_psd"][name]
        source = CHAT / item["relative_to_Chatgpt"]
        assert sha(source) == item["sha256"]
        acf = public_psd_acf(source, cfg)
        cov = toeplitz(acf[:n]) / cfg["reference_amplitude"]**2
        eigen = np.linalg.eigvalsh(cov)
        assert eigen[0] > 0 and eigen[-1] / eigen[0] <= 1e12
        blocks.append(dict(name=name, response=obj.response, gmst=gmst,
                           delay=delay, cholesky=cholesky(cov, lower=True)))
    return blocks


def waveforms(family, source, config):
    import lal
    import lalsimulation as lalsim
    approximant = lalsim.GetApproximantFromString(family)
    def generate(isolate_22):
        params = lal.CreateDict()
        if isolate_22:
            modes = lalsim.SimInspiralCreateModeArray()
            lalsim.SimInspiralModeArrayActivateMode(modes, 2, 2)
            lalsim.SimInspiralWaveformParamsInsertModeArray(params, modes)
        hp, hc = lalsim.SimInspiralChooseTDWaveform(
            source["mass1"] * lal.MSUN_SI, source["mass2"] * lal.MSUN_SI,
            0., 0., source["spin1z"], 0., 0., source["spin2z"],
            403. * 1e6 * lal.PC_SI, .6, .37, 0., 0., 0.,
            1. / 4096., 20., 20., params, approximant)
        t = float(hp.epoch) + np.arange(hp.data.length) * hp.deltaT
        return t, np.asarray(hp.data.data, dtype=float), np.asarray(hc.data.data, dtype=float)
    t, hp, hc = generate(False)
    t22, p22, c22 = generate(True)
    peak = float(t22[int(np.argmax(p22**2 + c22**2))])
    times = config["start_offset_s"] + np.arange(int(config["sample_rate_hz"] * config["analysis_duration_s"])) / config["sample_rate_hz"]
    if times[0] + peak < t[0] or times[-1] + peak > t[-1]:
        raise ValueError("Full-waveform tail does not cover registered analysis segment")
    plus = np.interp(times + peak, t, hp)
    cross = np.interp(times + peak, t, hc)
    if not np.isfinite([plus, cross]).all():
        raise ValueError("Nonfinite waveform")
    return times, plus, cross, peak


def main():
    import lal
    start = time.monotonic()
    def timeout(_sig, _frame):
        raise TimeoutError("T10-C own 1h machine hard cap")
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(3600)
    registry = RING / "RINGDOWN_5SIGMA_V1_1_3.json"
    assert sha(registry) == "74a2c8b656244ff4e127add5186199454c8248ef84b1b1050e72de09ed765515"
    plan = json.loads(registry.read_bytes())["t10_bank_v1_1_3"]
    cfg_path = RING / "bis" / "e3_kerr_dtau_f_015" / "CONFIG.json"
    cfg = json.loads(cfg_path.read_bytes())
    blocks = reference_blocks(cfg)
    out = RING / "cache" / "t10_c_bank_v1_1_3_v3"
    out.mkdir(exist_ok=False)
    rows = []
    error = None
    for index, snr_target in enumerate(plan["snr_bin_order"]):
        for family_index, family in enumerate(plan["family_order"]):
            if time.monotonic() - start >= 3590:
                error = "TIMEOUT_BEFORE_NEXT_CASE"
                break
            seed = 15260430 + 10 * index + family_index
            try:
                times, plus, cross, peak = waveforms(family, plan["sources_by_bin"][index], cfg)
                signals = {}
                whitened_norm2 = 0.
                for block in blocks:
                    fp, fc = lal.ComputeDetAMResponse(block["response"], cfg["ra"], cfg["dec"], .5, block["gmst"])
                    model_wave = fp * plus + fc * cross
                    whitened = solve_triangular(block["cholesky"], model_wave / cfg["reference_amplitude"], lower=True)
                    whitened_norm2 += float(whitened @ whitened)
                    signals[block["name"]] = model_wave
                base_snr = math.sqrt(whitened_norm2)
                if not base_snr > 0:
                    raise ValueError("Zero source SNR")
                scale = snr_target / base_snr
                rng = np.random.default_rng(seed)
                arrays = {"relative_time_s": times, "plus": plus * scale, "cross": cross * scale}
                for block in blocks:
                    name = block["name"]
                    noise = cfg["reference_amplitude"] * block["cholesky"] @ rng.standard_normal(len(times))
                    arrays["signal_" + name] = signals[name] * scale
                    arrays["noise_" + name] = noise
                    arrays["data_" + name] = signals[name] * scale + noise
                target = out / f"bin{index:02d}_{family}.npz"
                with target.open("xb") as stream:
                    np.savez_compressed(stream, **arrays)
                    stream.flush()
                    os.fsync(stream.fileno())
                rows.append(dict(bin=index, family=family, seed=seed, target_optimal_snr=snr_target,
                                 measured_optimal_snr=float(scale * base_snr), scale=scale,
                                 peak_reference_s=peak, parameters=plan["sources_by_bin"][index],
                                 file_relative_to_Chatgpt=str(target.relative_to(CHAT)).replace("\\", "/"),
                                 sha256=sha(target), size_bytes=target.stat().st_size))
                print(json.dumps({"bin": index, "family": family, "snr": snr_target, "sha256": rows[-1]["sha256"]}), flush=True)
            except Exception as exc:
                error = repr(exc)
                break
        if error is not None:
            break
    signal.alarm(0)
    result = dict(status="T10_C_BANK_CREATED" if len(rows) == 10 else "T10_C_PARTIAL_FAILED",
                  created_utc=datetime.now(timezone.utc).isoformat(), wall_seconds=time.monotonic()-start,
                  registry_sha256=sha(registry), config_sha256=sha(cfg_path), rows=rows,
                  expected_cells=10, error=error, no_PE=True, sigma_c=None, gate_changed=False,
                  scope="Synthetic GR family bank only; no deformed waveform or recovery")
    new_json(HERE / "T10_C_BANK_RESULT_v3.json", result)
    print(json.dumps({"status": result["status"], "cells": len(rows), "wall_seconds": result["wall_seconds"], "error": error}))


if __name__ == "__main__":
    main()
