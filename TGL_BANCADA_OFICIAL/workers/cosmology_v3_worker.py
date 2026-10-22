"""Persistent WSL stdio adapter for the byte-pinned V3 background class.

Only FundoV3 is imported/used. In particular, derivados(), CAMB, and GW
resident modules are never called. One last background and its 121-point
curve remain in this process until a different background is requested.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy.integrate import cumulative_trapezoid


BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / "scientific_models" / "tgl_camb_worker_v3.py"
PIN = "72032b3abe1c537762291ac6086d8d2e6076c007373f87ae7363f942eb830ce3"
if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != PIN:
    raise SystemExit("scientific worker SHA-256 mismatch")
sys.path.insert(0, str(SOURCE.parent))
import tgl_camb_worker_v3 as W  # noqa: E402; the exact local copy only


_last_key = None
_last_model = None
_last_series = None
_last_checks = None
_builds = 0


def _point(model, z, rd):
    dm = float(model.DM([z])[0]) if z else 0.0
    dh = W.C_KMS / (model.H0 * float(model.E_de_z(z)))
    dv = (z * dm * dm * dh) ** (1.0 / 3.0) if z else 0.0
    return {"z": float(z), "dm_mpc": dm, "dh_mpc": dh, "dv_mpc": dv,
            "dm_over_rd": dm / rd, "dh_over_rd": dh / rd, "dv_over_rd": dv / rd}


def _local_refinement(model):
    """Refine the J integral only over 0<=z<=3, anchored at the pinned J(0)."""
    xlo = -math.log(4.0)
    dx = (W.X_MAX - W.X_MIN) / (W.NGRID - 1)
    n = 2 * math.ceil(-xlo / dx) + 1
    x = np.linspace(xlo, 0.0, n)
    rho, rpp = model._rho_rpp(x, model.OL)
    g = 3.0 * rpp * rpp / rho
    cumulative = cumulative_trapezoid(g, x, initial=0.0)
    j0 = float(np.interp(0.0, model.x, model.J))
    j_ref = j0 + cumulative[-1] - cumulative
    e2_ref = rho + model.beta * j_ref + model.c
    e2_base = np.interp(x, model.x, model.E2)
    relative_e = float(np.max(np.abs(np.sqrt(e2_ref) - np.sqrt(e2_base)) / np.sqrt(e2_ref)))
    # This local derivative check tests the same second-Friedmann identity as
    # FundoV3.residuo_segunda_equacao(), restricted to the displayed redshifts.
    e2_local = np.interp(x, model.x, model.E2)
    derivative = np.gradient(e2_local, x)
    target = -3.0 * (1.0 + model.beta * rpp / rho) * rpp
    interior = slice(3, -3)
    second = float(np.max(np.abs(derivative[interior] - target[interior]) /
                          np.maximum(np.abs(target[interior]), 1e-20)))
    e0 = float(model.E_de_z(0.0))
    return {"ngrid_pinned": W.NGRID, "local_refined_points": n,
            "local_z_range": [0.0, 3.0], "max_relative_e_refinement": relative_e,
            "max_relative_second_friedmann_residual": second,
            "e0_residual": abs(e0 - 1.0),
            "min_e2_z0_to_3": float(np.min(e2_base))}


def _build(request):
    global _last_key, _last_model, _last_series, _last_checks, _builds
    p = request["parameters"]
    beta = float(request["beta"])
    h2 = (p["H0"] / 100.0) ** 2
    key = (p["H0"], p["omega_m"], beta)
    hit = key == _last_key and _last_model is not None
    build_ms = 0.0
    if not hit:
        started = time.perf_counter()
        # Representative split only: the background class depends on the sum.
        model = W.FundoV3(p["H0"], 0.0, p["omega_m"] * h2, beta,
                          c=0.0, mnu=0.0, TCMB=2.7255, Neff=3.046)
        checks = _local_refinement(model)
        if (not math.isfinite(checks["max_relative_e_refinement"])
                or checks["e0_residual"] > 5e-6
                or checks["min_e2_z0_to_3"] <= 0.0
                or checks["max_relative_second_friedmann_residual"] > 1e-3
                or checks["max_relative_e_refinement"] > 1e-5):
            raise ValueError("V3 background self-check failed")
        zs = np.linspace(0.0, 3.0, 121)
        dms = model.DM(zs)
        es = model.E_de_z(zs)
        # Keep distances in Mpc; rd scaling is applied per request below.
        bare = []
        for z, dm, e in zip(zs, dms, es):
            z, dm = float(z), float(dm)
            dh = W.C_KMS / (model.H0 * float(e))
            bare.append((z, dm, dh, (z * dm * dm * dh) ** (1 / 3) if z else 0.0))
        _last_key, _last_model, _last_series, _last_checks = key, model, tuple(bare), checks
        _builds += 1
        build_ms = (time.perf_counter() - started) * 1000.0
    return _last_model, _last_series, _last_checks, hit, build_ms


def evaluate(request):
    started = time.perf_counter()
    p = request["parameters"]
    model, bare, checks, hit, build_ms = _build(request)
    rd = p["rd_mpc"]
    series = [{"z": z, "dm_mpc": dm, "dh_mpc": dh, "dv_mpc": dv,
               "dm_over_rd": dm / rd, "dh_over_rd": dh / rd, "dv_over_rd": dv / rd}
              for z, dm, dh, dv in bare]
    cursor = _point(model, p["redshift"], rd)
    distances = [_point(model, z, rd) for z in request["redshifts"]]
    u = np.linspace(0.0, math.log1p(p["redshift"]), 40001)
    refined_dm = W.C_KMS / model.H0 * float(np.trapezoid(np.exp(u) /
        np.interp(-u, model.x, model.E), u))
    quadrature = dict(checks, method="PINNED_TRAPEZOID_IN_LOG1P_Z",
                      distance_intervals_pinned=20000, cursor_refined_intervals=40000,
                      cursor_dm_relative_delta=abs(refined_dm - cursor["dm_mpc"]) / refined_dm)
    details = {
        "model_id": request["model_id"], "status": "CONDITIONAL_V3_TOTAL_FLUID_BACKGROUND_ONLY",
        "beta": request["beta"], "beta_mode": request["beta_mode"],
        "omega_r": model.Or, "omega_m_effective": model.Om,
        "omega_lambda_closed": model.OL, "c": 0.0,
        "mapping": {"ombh2": 0.0, "omch2": p["omega_m"] * (p["H0"] / 100.0) ** 2,
                    "mnu_ev": 0.0, "TCMB_K": 2.7255, "Neff": 3.046,
                    "note": "Representative density split for E/DM only; not a physical baryon estimate"},
        "assumptions": ["flat background with radiation, matter and Lambda",
                        "Phi_total=1+beta*(rho+p)/rho on the nonnegative-enthalpy branch",
                        "P(infinity)=rho_Lambda; C=0; H(z=0)=H0",
                        "w0=-1 and wa=0; no perturbation or CMB prediction",
                        "rd_mpc is an external visual scale"],
        "background_cache_hit": hit, "background_builds": _builds,
        "background_build_ms": build_ms,
    }
    return {"status": "ok", "series": series, "cursor": cursor,
            "distances": distances, "quadrature": quadrature, "details": details,
            "source_hashes": {"scientific_model_sha256": PIN},
            "elapsed_ms": (time.perf_counter() - started) * 1000.0}


def main():
    for line in sys.stdin:
        request = None
        try:
            request = json.loads(line)
            result = evaluate(request)
        except Exception as exc:
            result = {"status": "error", "error": {"code": "WORKER_EVALUATION", "message": str(exc)}}
        result["request_id"] = request.get("request_id") if isinstance(request, dict) else None
        sys.stdout.write(json.dumps(result, allow_nan=False, separators=(",", ":")) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
