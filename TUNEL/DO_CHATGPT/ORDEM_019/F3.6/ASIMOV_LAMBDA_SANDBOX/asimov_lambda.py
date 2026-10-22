"""Local tangent Fisher diagnostic for D1 control 2 at the Lambda point.

No observed means or likelihood are loaded. The V3 worker is copied only as a
reference for the beta response; CAMB supplies the beta=0 CPL background.
"""

from __future__ import annotations

import json
import math
import platform
import sys
import time
from pathlib import Path

import camb
import numpy as np
from scipy.integrate import cumulative_trapezoid

import tgl_camb_worker_v3_reference as v3


C = 299792.458
ALPHA_FINE_CODATA_2018 = 0.0072973525693
BETA_TGL = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
FIDUCIAL = np.array([67.5, 0.02237, 0.1200, 0.0, -1.0, 0.0])
SCALES = np.array([1.0, 0.0005, 0.005, 0.005, 0.05, 0.05])
DESI_ROWS = [
    (0.295, "DV", 0.15, None),
    (0.510, "DM", 0.25, -0.445), (0.510, "DH", 0.61, -0.445),
    (0.706, "DM", 0.32, -0.420), (0.706, "DH", 0.60, -0.420),
    (0.930, "DM", 0.28, -0.389), (0.930, "DH", 0.35, -0.389),
    (1.317, "DM", 0.69, -0.444), (1.317, "DH", 0.42, -0.444),
    (1.491, "DV", 0.67, None),
    (2.330, "DM", 0.94, -0.477), (2.330, "DH", 0.17, -0.477),
]
PLANCK_INV_CHEN = np.array([
    [94392.3971, -1360.4913, 1664517.2916],
    [-1360.4913, 161.4349, 3671.6180],
    [1664517.2916, 3671.6180, 79719182.5162],
])
PLANCK_COV_V3 = np.array([
    [2.1167e-05, 3.4659e-05, -4.5466e-08],
    [3.4659e-05, 8.0901e-03, -1.6087e-06],
    [-4.5466e-08, -1.6087e-06, 2.2497e-08],
])


def covariance(corrected: bool) -> np.ndarray:
    """The two covariance choices are labelled; only the corrected one is primary."""
    pc = np.linalg.inv(PLANCK_INV_CHEN) if corrected else PLANCK_COV_V3
    dc = np.diag([r[2] ** 2 for r in DESI_ROWS])
    if corrected:
        for i in (1, 3, 5, 7, 10):
            rho = DESI_ROWS[i][3]
            assert rho == DESI_ROWS[i + 1][3]
            dc[i, i + 1] = dc[i + 1, i] = rho * DESI_ROWS[i][2] * DESI_ROWS[i + 1][2]
    cov = np.zeros((15, 15))
    cov[:3, :3] = pc
    cov[3:, 3:] = dc
    np.linalg.cholesky(cov)
    return cov


def camb_reference(theta: np.ndarray, mnu: float):
    H0, wb, wc, _beta, w0, wa = (float(x) for x in theta)
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=H0, ombh2=wb, omch2=wc, mnu=mnu,
                       tau=0.0544, TCMB=2.7255, nnu=3.046)
    pars.InitPower.set_params(ns=0.9649, As=2.1e-9)
    pars.set_dark_energy(w=w0, wa=wa, dark_energy_model="ppf")
    pars.set_for_lmax(20, lens_potential_accuracy=0)
    res = camb.get_background(pars)
    derived = res.get_derived_params()
    return res, derived


def camb_observables(theta: np.ndarray, mnu: float, map_r: str) -> tuple[np.ndarray, dict]:
    H0, wb, wc, beta, _w0, _wa = (float(x) for x in theta)
    res, d = camb_reference(theta, mnu)
    zs = float(d["zstar"])
    rd = float(d["rdrag"])
    rs = float(d["rstar"])
    dm_star = float(res.angular_diameter_distance(zs)) * (1 + zs)
    omega_m = (wb + wc + mnu / 93.14) / (H0 / 100.0) ** 2
    r_multiplier = math.sqrt(1 + beta) if map_r == "effective" else 1.0
    planck = [math.sqrt(omega_m) * H0 / C * dm_star * r_multiplier,
              math.pi * dm_star / rs, wb]
    desi = []
    for z, kind, _sigma, _rho in DESI_ROWS:
        dm = float(res.angular_diameter_distance(z)) * (1 + z)
        dh = C / float(res.hubble_parameter(z))
        desi.append(dm / rd if kind == "DM" else
                    dh / rd if kind == "DH" else
                    (z * dm * dm * dh) ** (1.0 / 3.0) / rd)
    return np.array(planck + desi), {"res": res, "derived": d, "dm_star": dm_star,
                                    "omega_m": omega_m, "rstar": rs, "rdrag": rd}


def beta_kernel(theta: np.ndarray, mnu: float, composition: str, res):
    """Exact CAMB-neutrino beta tangent K(u) at Lambda and H(1)=H0.

    With u=ln(1+z), rho_total=E_CAMB**2 and rho+p=(d rho/du)/3.
    At Lambda the CPL enthalpy is zero, so A and Bprime have identical
    beta-direction factors. Using CAMB rho removes V3's neutrino double count.
    """
    H0, _wb, _wc, _beta, w0, wa = (float(x) for x in theta)
    assert w0 == -1.0 and wa == 0.0 and composition in {"A", "Bprime"}
    u = np.linspace(0.0, math.log1p(1.0e8), 80001)
    z = np.expm1(u)
    rho = (np.asarray(res.hubble_parameter(z), float) / H0) ** 2
    total_rpp = np.gradient(rho, u, edge_order=2) / 3.0
    # The dark-energy enthalpy vanishes at Lambda. The branches are evaluated
    # separately to test the expected equality, rather than substituting it.
    dark_energy_rpp = np.zeros_like(total_rpp)  # w0=-1, wa=0
    non_de_rpp = total_rpp - dark_energy_rpp
    factor_rpp = total_rpp if composition == "A" else non_de_rpp
    g = 3.0 * total_rpp * np.abs(factor_rpp) / rho
    k = cumulative_trapezoid(g, u, initial=0.0)
    return u, k, {"rho": rho, "rpp": total_rpp,
                  "K_at_0": float(k[0]),
                  "integrand_at_0": float(g[0])}


def beta_observables(theta: np.ndarray, mnu: float, composition: str,
                     map_r: str, beta: float, n_grid: int = 16001) -> tuple[np.ndarray, dict]:
    """Numerical Lambda-direction observable model, with CAMB at beta=0."""
    H0, wb, wc = (float(x) for x in theta[:3])
    baseline, meta = camb_observables(theta, mnu, map_r="bare")
    res = meta["res"]
    d = meta["derived"]
    zs, zd = float(d["zstar"]), float(d["zdrag"])
    u_kernel, k_grid, kernel_meta = beta_kernel(theta, mnu, composition, res)

    def integrals(z_lo: float, z_hi: float):
        u = np.linspace(math.log1p(z_lo), math.log1p(z_hi), n_grid)
        z = np.expm1(u)
        e0 = np.asarray(res.hubble_parameter(z), float) / H0
        k = np.interp(u, u_kernel, k_grid)
        e2 = e0 * e0 + beta * k
        if not np.all(e2 > 0):
            raise ValueError("nonpositive E2")
        return u, z, e0, np.sqrt(e2), k

    u, z, e0, e, k = integrals(0.0, zs)
    dm_integrand = C / H0 * np.exp(u) / e
    dm_cum = cumulative_trapezoid(dm_integrand, u, initial=0.0)
    dm_star = float(dm_cum[-1])
    # Preserve CAMB normalization at beta=0 while using the differential effect.
    dm_star += meta["dm_star"] - float(cumulative_trapezoid(C / H0 * np.exp(u) / e0, u, initial=0.0)[-1])

    def sound(z_lo: float, r_camb: float):
        uu, zz, e0s, es, _k = integrals(z_lo, 1.0e8)
        ogh2 = v3._omega_r_h2()[1]
        rb = 3.0 * wb / (4.0 * ogh2 * (1.0 + zz))
        cs = C / np.sqrt(3.0 * (1.0 + rb))
        i0 = float(np.trapezoid(cs * np.exp(uu) / (H0 * e0s), uu))
        ib = float(np.trapezoid(cs * np.exp(uu) / (H0 * es), uu))
        return r_camb * ib / i0

    rs = sound(zs, meta["rstar"])
    rd = sound(zd, meta["rdrag"])
    omega_m = meta["omega_m"]
    r_multiplier = math.sqrt(1.0 + beta) if map_r == "effective" else 1.0
    planck = [math.sqrt(omega_m) * H0 / C * dm_star * r_multiplier,
              math.pi * dm_star / rs, wb]

    desi = []
    for zz, kind, _sigma, _rho in DESI_ROWS:
        uz = math.log1p(zz)
        dm = float(np.interp(uz, u, dm_cum))
        dm += float(res.angular_diameter_distance(zz)) * (1 + zz) - float(
            np.interp(uz, u, cumulative_trapezoid(C / H0 * np.exp(u) / e0, u, initial=0.0)))
        ezz = math.sqrt((float(res.hubble_parameter(zz)) / H0) ** 2 +
                         beta * float(np.interp(uz, u_kernel, k_grid)))
        dh = C / (H0 * ezz)
        desi.append(dm / rd if kind == "DM" else
                    dh / rd if kind == "DH" else
                    (zz * dm * dm * dh) ** (1.0 / 3.0) / rd)
    out = np.array(planck + desi)
    return out, {"E0_at_0": 1.0, "K_at_0": kernel_meta["K_at_0"],
                 "K_over_E2_zstar": float(np.interp(math.log1p(zs), u_kernel, k_grid) /
                                           (float(res.hubble_parameter(zs)) / H0) ** 2),
                 "dm_star_baseline": meta["dm_star"], "zstar": zs}


def compute(mnu: float, step: float = 0.01) -> dict:
    theta = FIDUCIAL.copy()
    # The same synthetic Lambda mean is used for all covariance/map choices.
    mean, meta = camb_observables(theta, mnu, "bare")
    derivatives = []
    for j in (0, 1, 2, 4, 5):
        tp = theta.copy(); tm = theta.copy()
        tp[j] += step * SCALES[j]; tm[j] -= step * SCALES[j]
        yp, _ = camb_observables(tp, mnu, "bare")
        ym, _ = camb_observables(tm, mnu, "bare")
        derivatives.append((yp - ym) / (2 * step * SCALES[j]))
    beta_diff = {}
    check = {}
    for composition in ("A", "Bprime"):
        p, pp = beta_observables(theta, mnu, composition, "bare", +1e-4)
        q, qq = beta_observables(theta, mnu, composition, "bare", -1e-4)
        beta_diff[composition] = (p - q) / 2e-4
        y0, _ = beta_observables(theta, mnu, composition, "bare", 0.0)
        check[composition] = {"baseline_max_abs": float(np.max(np.abs(y0 - mean))),
                              "K_at_0": pp["K_at_0"], "K_over_E2_zstar": pp["K_over_E2_zstar"],
                              "asymmetry_dbeta_max_abs": float(np.max(np.abs((p + q) / 2 - y0)))}
    beta_same = float(np.max(np.abs(beta_diff["A"] - beta_diff["Bprime"])))
    # Derivative order: H0, wb, wc, beta, w0, wa.
    cases = {}
    for comp in ("A", "Bprime"):
        for map_r in ("bare", "effective"):
            cols = list(derivatives[:3]) + [beta_diff[comp].copy()] + list(derivatives[3:])
            if map_r == "effective":
                cols[3][0] += 0.5 * mean[0]
            J = np.column_stack(cols) * SCALES
            for corrected in (False, True):
                cov = covariance(corrected)
                L = np.linalg.cholesky(cov)
                Jw = np.linalg.solve(L, J)
                singular = np.linalg.svd(Jw, compute_uv=False)
                rank = int(np.linalg.matrix_rank(Jw))
                condition = float(singular[0] / singular[-1])
                key = f"{comp}_{map_r}_{'corrected' if corrected else 'v3_cov'}"
                if rank < 6 or not math.isfinite(condition) or condition > 1e12:
                    cases[key] = {"status": "SINGULAR_OR_ILL_CONDITIONED", "rank": rank,
                                  "condition": condition}
                    continue
                F = Jw.T @ Jw
                invF = np.linalg.inv(F)
                sigma = float(SCALES[3] * math.sqrt(invF[3, 3]))
                one = float(SCALES[3] / math.sqrt(F[3, 3]))
                corr = invF / np.sqrt(np.outer(np.diag(invF), np.diag(invF)))
                cases[key] = {"status": "MEASURED_LOCAL_FISHER", "sigma_beta": sigma,
                              "sigma_beta_fixed_others": one, "sigma_over_beta": sigma / BETA_TGL,
                              "gate": "UNDERPOWERED_DO_NOT_OPEN_DATA" if sigma >= BETA_TGL
                              else "POWER_GATE_PASSED_PENDING_MODEL_DECISION",
                              "rank": rank, "condition": condition,
                              "corr_beta_w0": float(corr[3, 4]),
                              "corr_beta_wa": float(corr[3, 5])}
    return {"mnu_eV": mnu, "fiducial": theta.tolist(), "derivative_step_scaled": step,
            "beta_runtime": BETA_TGL, "n_observables": 15, "n_parameters": 6,
            "A_Bprime_beta_jacobian_max_abs": beta_same,
            "check": check, "cases": cases,
            "baseline_planck_R": float(mean[0]), "baseline_planck_lA": float(mean[1])}


def main() -> None:
    t0 = time.time()
    runs = [compute(0.06), compute(0.0)]
    report = {"protocol": "F3.6_ASIMOV_LAMBDA_TANGENT_V1", "status": "NUMERICAL_DIAGNOSTIC",
              "runtime_s": time.time() - t0, "python": platform.python_version(),
              "camb": camb.__version__, "numpy": np.__version__,
              "source_urls": ["https://arxiv.org/html/2404.03002",
                              "https://arxiv.org/html/1808.05724"],
              "observed_means_used": False,
              "observed_means_literal_exposure": True,
              "limitations": ["Local tangent at beta=0,w0=-1,wa=0 only; no off-Lambda CPL model",
                              "Beta tangent uses CAMB total H(a), including massive-neutrino evolution; mnu=0 is a sensitivity control",
                              "Compressed Planck distance priors and DESI DR1 BAO, not full CMB likelihood",
                              "No synthetic-noise injection/recovery and no observed-data fit"],
              "runs": runs}
    out = Path(__file__).with_name("RESULTADO_ASIMOV_LAMBDA.json")
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    tmp.replace(out)
    print(json.dumps({"runtime_s": report["runtime_s"],
                      "runs": [{"mnu_eV": r["mnu_eV"],
                                "A_Bprime_beta_jacobian_max_abs": r["A_Bprime_beta_jacobian_max_abs"],
                                "cases": r["cases"]} for r in runs]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
