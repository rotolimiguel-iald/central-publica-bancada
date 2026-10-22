"""Small source-only controls: zero deformation, nonzero damping, invalid support."""
from __future__ import annotations

import ast
import importlib.util
import json
from pathlib import Path

import numpy as np
import lal

RING = Path(__file__).resolve().parents[3]
OLD = RING / "bis" / "e3_kerr_continuation"
NEW = RING / "bis" / "e3_kerr_dtau_f_015"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> None:
    for name in ("conditioning.py", "controller.py", "custody.py", "kerr_model.py", "runner.py"):
        ast.parse((NEW / name).read_text(encoding="utf-8"))
    old = load("kerr_old_source_only", OLD / "kerr_model.py")
    new = load("kerr_dtau_f_source_only", NEW / "kerr_model.py")
    cfg_old = json.loads((OLD / "CONFIG.json").read_bytes())
    cfg_new = json.loads((NEW / "CONFIG.json").read_bytes())
    assert tuple(new.PARAMETERS[:-1]) == tuple(old.PARAMETERS)
    assert new.PARAMETERS[-1] == "dtau220"
    assert set(cfg_new["priors"]) == set(new.PARAMETERS)
    assert cfg_new["priors"]["dtau220"] == [-0.8, 2.0]
    assert cfg_old["qnm_coefficients"] == cfg_new["qnm_coefficients"]
    x = dict(psi=0.2, Mf=75.0, af=0.75, cosiota=0.3, A2220_1=1.0,
             A2220_2=0.0, phi2220_1=0.4, phi2220_2=0.0)
    mass_time = lal.G_SI * lal.MSUN_SI / lal.C_SI**3
    times = cfg_old["start_offset_s"] + np.array([0.0, 0.003, 0.010, 0.025])
    hp0, hc0 = old.polarizations(times, x, cfg_old, mass_time)
    y = dict(x, dtau220=0.0)
    hp1, hc1 = new.polarizations(times, y, cfg_new, mass_time)
    baseline_error = max(np.max(np.abs(hp1-hp0)), np.max(np.abs(hc1-hc0)))
    assert baseline_error == 0.0, baseline_error
    z = dict(x, dtau220=0.5)
    hp2, hc2 = new.polarizations(times, z, cfg_new, mass_time)
    _, tau = old.frequency_tau(x["Mf"], x["af"], cfg_old["qnm_coefficients"], mass_time)
    old_h = hp0 + 1j * hc0
    new_h = hp2 + 1j * hc2
    expected = np.exp((times - cfg_old["start_offset_s"]) * (1/tau - 1/(1.5*tau)))
    ratio = new_h / old_h
    assert np.allclose(ratio, expected, rtol=1e-12, atol=1e-12)
    assert np.max(np.abs(new_h[1:] - old_h[1:])) > 0
    negative_branch = dict(x, A2220_1=0.0, A2220_2=1.0)
    n0p, n0c = old.polarizations(times, negative_branch, cfg_old, mass_time)
    n1p, n1c = new.polarizations(times, dict(negative_branch, dtau220=0.5), cfg_new, mass_time)
    negative_ratio = (n1p + 1j*n1c) / (n0p + 1j*n0c)
    assert np.allclose(negative_ratio, expected, rtol=1e-12, atol=1e-12)
    detector, _, gmst = new.geometry("H1", cfg_new)
    fp, fc = lal.ComputeDetAMResponse(detector.response, cfg_new["ra"], cfg_new["dec"],
                                     x["psi"], gmst)
    synthetic = fp*hp1 + fc*hc1
    block = dict(relative_times=times, response=detector.response, gmst=gmst,
                 data=synthetic, cholesky_scaled=np.eye(len(times)), log_normalization=0.0)
    likelihood = new.make_likelihood([block], cfg_new, lambda: None)
    ll0 = likelihood.log_likelihood(y)
    llshift = likelihood.log_likelihood(z)
    assert abs(ll0) < 1e-24
    assert llshift < ll0 - 1e-14, (ll0, llshift)
    for invalid in (-1.0, -1.1, float("nan")):
        try:
            new.polarizations(times, dict(x, dtau220=invalid), cfg_new, mass_time)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Invalid dtau220 accepted: {invalid}")
    print(json.dumps(dict(status="KERR_DTAU_SOURCE_CONTROLS_PASS",
                          baseline_max_abs_error=float(baseline_error),
                          nonzero_ratio_max_error=float(np.max(np.abs(ratio-expected))),
                          negative_branch_ratio_max_error=float(np.max(np.abs(negative_ratio-expected))),
                          likelihood_zero=ll0, likelihood_shifted=llshift,
                          invalid_rejected=3, posterior_or_sigma_measured=False)))


if __name__ == "__main__":
    main()
