"""Fase 9 V1.x staged runner: pinned, fabricated data only.

This is a statistical rehearsal, not an opening. The documentary gate reads
the V2 draft once and returns its pinned spec snapshot. No observed H0 center
enters a calculation, no verdict function is called, and no file is written.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from f9_reader_gate_v1x import ReaderGateError, verify_v1x_binding
from f9_runner_v1x_preflight import ALL_IDS, MU_DO_RITO, PRIMARY_IDS, _ids, _object


FIXTURE_ID = "F9_SYNTHETIC_FIXTURE_R2_20261008"
PINNED_FIXTURE_SHA256 = "3005b5a9f1e0cdb2886bd877621b0e3449835510eeaac6176827b1262105c6f9"
FAMILIES = ("P_primaria", "M_seis_masers_diagnostico", "N_sem_cefeidas")
BG_IDS = ("BG1", "BG2", "BG3")
PRIOR_BETA = (-0.05, 0.05)
PRIOR_SHIFT = (-0.15, 0.15)


def _finite(x: object, name: str, *, positive: bool = False) -> float:
    if isinstance(x, bool) or not isinstance(x, (float, int)):
        raise ReaderGateError(f"{name} must be numeric")
    v = float(x)
    if not math.isfinite(v) or (positive and v <= 0):
        raise ReaderGateError(f"{name} must be finite and valid")
    return v


def _cholesky(a: list[list[float]]) -> list[list[float]]:
    n = len(a)
    if not n or any(len(row) != n for row in a):
        raise ReaderGateError("covariance is not square")
    l = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            v = a[i][j] - sum(l[i][k] * l[j][k] for k in range(j))
            if i == j:
                if v <= 1e-12:
                    raise ReaderGateError("covariance is not positive definite")
                l[i][j] = math.sqrt(v)
            else:
                l[i][j] = v / l[j][j]
    return l


def _solve_spd(a: list[list[float]], b: list[float]) -> tuple[list[float], float]:
    l = _cholesky(a)
    n = len(b)
    if n != len(l):
        raise ReaderGateError("linear system dimension mismatch")
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(l[i][k] * y[k] for k in range(i))) / l[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(l[k][i] * x[k] for k in range(i + 1, n))) / l[i][i]
    return x, 2.0 * sum(math.log(l[i][i]) for i in range(n))


def gls(c: list[list[float]], y: list[float] | None = None) -> dict:
    n = len(c)
    w0, _ = _solve_spd(c, [1.0] * n)
    denom = sum(w0)
    if denom <= 0:
        raise ReaderGateError("GLS denominator nonpositive")
    weights = [v / denom for v in w0]
    result = {"sigma_comb": math.sqrt(1.0 / denom), "weights": weights}
    if y is not None:
        if len(y) != n:
            raise ReaderGateError("GLS observation dimension mismatch")
        mean = sum(a * b for a, b in zip(weights, y))
        residual = [v - mean for v in y]
        wr, _ = _solve_spd(c, residual)
        chi2 = sum(a * b for a, b in zip(residual, wr))
        result.update({"mean": mean, "chi2_int": chi2,
                       "dispersion_per_dof": chi2 / (n - 1) if n > 1 else None})
    return result


def covariance(spec: dict, ids: list[str], lambda_n: float, lambda_t: float) -> list[list[float]]:
    readers = spec["leitores"]
    amps = spec["covariancia"]["amplitudes_km_s_Mpc"]
    nmap = {"L1_sh0es_r22": "L1N", "L2_cchp": "L2N",
            "L3_sbf": "L3N", "L4_masers_6": "L4N"}
    tmap = {"L2_cchp": "L2T", "L3_sbf": "L3T"}
    if not 0 <= lambda_n <= 1 or not 0 <= lambda_t <= 1:
        raise ReaderGateError("covariance parameter outside preregistered box")
    c = [[0.0] * len(ids) for _ in ids]
    for i, left in enumerate(ids):
        if left not in readers:
            raise ReaderGateError(f"unknown reader: {left}")
        c[i][i] = _finite(readers[left].get("sigma"), f"{left}.sigma", positive=True) ** 2
        for j in range(i):
            right = ids[j]
            v = 0.0
            if left in nmap and right in nmap:
                v += lambda_n * amps[nmap[left]] * amps[nmap[right]]
            if left in tmap and right in tmap:
                v += lambda_t * amps[tmap[left]] * amps[tmap[right]]
            c[i][j] = c[j][i] = v
    _cholesky(c)
    return c


def grid_endpoints(spec: dict, ids: list[str]) -> dict:
    grid = spec["covariancia"]["grid"]
    best = {"minimum": None, "maximum": None}
    accepted = 0
    for ln in grid["lambda_N"]:
        for lt in grid["lambda_T"]:
            c = covariance(spec, ids, ln, lt)
            fit = gls(c)
            accepted += 1
            point = {"lambda_N": ln, "lambda_T": lt,
                     "sigma_comb": fit["sigma_comb"], "covariance": c,
                     "gls_weights": dict(zip(ids, fit["weights"])),
                     "negative_weights": [k for k, v in zip(ids, fit["weights"]) if v < 0]}
            for kind in best:
                old = best[kind]
                better = old is None or (point["sigma_comb"] < old["sigma_comb"] - 1e-12
                                         if kind == "minimum" else
                                         point["sigma_comb"] > old["sigma_comb"] + 1e-12)
                if better:
                    best[kind] = point
    if not accepted:
        raise ReaderGateError("empty covariance grid")
    return {"accepted": accepted, **best}


def scale_from_spec(spec: dict) -> dict:
    alpha = _finite(spec["beta"].get("alpha_read"), "alpha input", positive=True)
    beta = alpha * math.sqrt(math.e)
    if not math.isclose(beta, spec["beta"]["beta_runtime"], rel_tol=1e-12):
        raise ReaderGateError("runtime beta differs from draft")
    law = spec["lei"]
    z = _finite(law.get("z_star"), "z_star", positive=True)
    om = _finite(law.get("Omega_m"), "Omega_m", positive=True)
    orad = _finite(law.get("Omega_r"), "Omega_r", positive=True)
    e2 = orad * (1 + z) ** 4 + om * (1 + z) ** 3 + 1 - om - orad
    if e2 <= 0:
        raise ReaderGateError("E(z_star)^2 nonpositive")
    ln_e = math.log(math.sqrt(e2))
    k = math.exp((2 * beta / 3) * ln_e)
    if not math.isclose(k, law["K_frozen_V1"], rel_tol=1e-12):
        raise ReaderGateError("runtime K differs from frozen K")
    return {"alpha_input_from_pinned_spec": alpha,
            "alpha_provenance": "INPUT_PINNED_V2_DRAFT_GENERATOR; um.py not reread by staged runner",
            "beta_runtime": beta,
            "K_runtime": k, "K_frozen": law["K_frozen_V1"], "ln_E_star": ln_e}


def _marginal_ln_l(y: list[float], c: list[list[float]], mu: float,
                   s_bg: float, factors: list[float]) -> dict:
    n = len(y)
    if len(factors) != n:
        raise ReaderGateError("factor dimension mismatch")
    s = [[c[i][j] + s_bg * s_bg * factors[i] * factors[j]
          for j in range(n)] for i in range(n)]
    r = [y[i] - mu * factors[i] for i in range(n)]
    inv_r, logdet = _solve_spd(s, r)
    q = sum(a * b for a, b in zip(r, inv_r))
    full_logdet = logdet + n * math.log(2 * math.pi)
    return {"lnL": -0.5 * (q + full_logdet), "quadratic": q,
            "logdet_2piS": full_logdet}


def _golden_max(fn, lo: float, hi: float) -> tuple[float, float]:
    invphi = (math.sqrt(5) - 1) / 2
    x1, x2 = hi - invphi * (hi - lo), lo + invphi * (hi - lo)
    f1, f2 = fn(x1), fn(x2)
    for _ in range(150):
        if hi - lo < 1e-12:
            break
        if f1 < f2:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + invphi * (hi - lo); f2 = fn(x2)
        else:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - invphi * (hi - lo); f1 = fn(x1)
    candidates = [(fn(lo), lo), (fn(hi), hi), (f1, x1), (f2, x2)]
    best = max(candidates)
    return best[1], best[0]


def _profile_side(fn, peak: float, peak_value: float, bound: float) -> float | None:
    target = peak_value - 0.5
    if fn(bound) > target:
        return None
    lo, hi = sorted((peak, bound))
    for _ in range(90):
        mid = (lo + hi) / 2
        if (fn(mid) > target) == (bound > peak):
            lo = mid
        else:
            hi = mid
    return abs((lo + hi) / 2 - peak)


def _legendre_nodes_weights(n: int) -> list[tuple[float, float]]:
    if n < 100:
        raise ReaderGateError("lnB quadrature requires n >= 100")
    out = [None] * n
    for k in range(1, (n + 1) // 2 + 1):
        x = math.cos(math.pi * (k - 0.25) / (n + 0.5))
        for _ in range(30):
            p0, p1 = 1.0, x
            for j in range(2, n + 1):
                p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
            pn = p1
            dp = n * (x * pn - p0) / (x * x - 1)
            dx = pn / dp
            x -= dx
            if abs(dx) < 2e-15:
                break
        else:
            raise ReaderGateError("Gauss-Legendre root did not converge")
        w = 2 / ((1 - x * x) * dp * dp)
        out[k - 1] = (-x, w)
        out[n - k] = (x, w)
    return out


def _ln_evidence_uniform(fn, lo: float, hi: float, n: int) -> float:
    terms = []
    for x, w in _legendre_nodes_weights(n):
        b = (hi - lo) * x / 2 + (hi + lo) / 2
        terms.append((fn(b), w))
    peak = max(v for v, _ in terms)
    return peak + math.log(0.5 * sum(w * math.exp(v - peak) for v, w in terms))


def _signed_root(x: float) -> float:
    return math.copysign(math.sqrt(abs(x)), x)


def synthetic_statistics(spec: dict, ids: list[str], values: list[float],
                         c: list[list[float]], mu: float, sigma_bg: float,
                         scale: dict) -> dict:
    n = len(ids)
    k = scale["K_runtime"]
    beta = scale["beta_runtime"]
    ln_e = scale["ln_E_star"]
    tgl = _marginal_ln_l(values, c, mu, sigma_bg, [k] * n)
    lcdm = _marginal_ln_l(values, c, mu, sigma_bg, [1.0] * n)
    beta_fit = lambda b: _marginal_ln_l(
        values, c, mu, sigma_bg, [math.exp((2 * b / 3) * ln_e)] * n)["lnL"]
    bhat, lmax = _golden_max(beta_fit, *PRIOR_BETA)
    left = _profile_side(beta_fit, bhat, lmax, PRIOR_BETA[0])
    right = _profile_side(beta_fit, bhat, lmax, PRIOR_BETA[1])
    sigma_beta = (left + right) / 2 if left is not None and right is not None else None
    z_delta = (bhat - beta) / sigma_beta if sigma_beta is not None else None
    z_quad = _signed_root(lcdm["quadratic"] - tgl["quadratic"])
    z_with_det = _signed_root(-2 * lcdm["lnL"] + 2 * tgl["lnL"])
    cef = [1.0 if id_ == "L1_sh0es_r22" else 0.0 for id_ in ids]
    shift_fit = lambda sh: _marginal_ln_l(
        values, c, mu, sigma_bg, [1.0 + sh * v for v in cef])["lnL"]
    zb100 = _ln_evidence_uniform(beta_fit, *PRIOR_BETA, 100)
    zb200 = _ln_evidence_uniform(beta_fit, *PRIOR_BETA, 200)
    zs100 = _ln_evidence_uniform(shift_fit, *PRIOR_SHIFT, 100) if any(cef) else lcdm["lnL"]
    zs200 = _ln_evidence_uniform(shift_fit, *PRIOR_SHIFT, 200) if any(cef) else lcdm["lnL"]
    dispersion = gls(c, values)
    chi2 = dispersion["chi2_int"]
    # For this synthetic primary only, n=5 gives 4 degrees of freedom and
    # P(ChiSq_4 >= x) = exp(-x/2) * (1+x/2) exactly.
    p_dispersion = math.exp(-chi2 / 2) * (1 + chi2 / 2) if n == 5 else "NOT_IMPLEMENTED_FOR_THIS_DOF"
    return {
        "lnL_TGL": tgl, "lnL_LCDM": lcdm,
        "z_disc_quadratic": z_quad,
        "z_disc_with_logdet_diagnostic": z_with_det,
        "beta_hat": bhat, "beta_profile_minus": left, "beta_profile_plus": right,
        "sigma_beta_mean_sides": sigma_beta, "z_delta_profile_logdet": z_delta,
        "lnB_TGL_LCDM": tgl["lnL"] - lcdm["lnL"],
        "lnB_TGL_beta_free_n100": tgl["lnL"] - zb100,
        "lnB_TGL_beta_free_n200": tgl["lnL"] - zb200,
        "lnB_beta_quadrature_abs_diff": abs(zb100 - zb200),
        "lnB_TGL_cepheid_shift_n100": tgl["lnL"] - zs100,
        "lnB_TGL_cepheid_shift_n200": tgl["lnL"] - zs200,
        "lnB_shift_quadrature_abs_diff": abs(zs100 - zs200),
        "gls": dispersion,
        "p_dispersion": p_dispersion,
        "dispersion_rule_evaluation": "NO_VERDICT_THRESHOLD_NOT_PINNED; inspect both endpoints",
        "lnB_TGL_free_background": "NOT_IMPLEMENTED_REQUIRES_BANCADA_MOTOR",
    }


def _load_fixture(path: Path, expected_sha256: str) -> dict:
    if expected_sha256 != PINNED_FIXTURE_SHA256:
        raise ReaderGateError("synthetic fixture pin differs from reviewed fixture")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ReaderGateError("synthetic fixture hash mismatch")
    try:
        obj = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ReaderGateError("synthetic fixture unreadable") from exc
    if not isinstance(obj, dict) or obj.get("id") != FIXTURE_ID or obj.get("mode") != "synthetic_only" or obj.get("synthetic") is not True:
        raise ReaderGateError("real or unknown fixture mode refused")
    if set(obj) != {"id", "mode", "synthetic", "background", "primary_offsets", "center"}:
        raise ReaderGateError("synthetic fixture fields differ")
    if obj["center"] != 50.0 or obj["background"] != {"sigma": 0.4} or obj["primary_offsets"] != [0.7, -0.4, 0.2, -0.1, 1.0]:
        raise ReaderGateError("reviewed synthetic fixture values differ")
    return obj


def run_synthetic(binding_path: Path, binding_sha256: str, source_root: Path,
                  spec_sha256: str, fixture_path: Path, fixture_sha256: str,
                  *, mode: str = "synthetic_only") -> dict:
    if mode != "synthetic_only":
        raise ReaderGateError("real or unknown mode refused before documentary reading")
    fixture = _load_fixture(fixture_path, fixture_sha256)
    gate = verify_v1x_binding(binding_path, expected_binding_sha256=binding_sha256,
                              allowed_source_root=source_root,
                              expected_spec_sha256=spec_sha256)
    if gate.get("v2_frozen") is not False or gate.get("source_admission") != "OPEN" or gate.get("statistical_admission") != "OPEN":
        raise ReaderGateError("gate claimed freeze or admission")
    spec = _object(gate.get("spec_snapshot"), "single-read spec snapshot")
    if spec.get("mu_do_rito") != MU_DO_RITO:
        raise ReaderGateError("mu_do_rito differs")
    readers = _object(spec.get("leitores"), "readers")
    verified = _object(gate.get("verified_readers"), "documentary readers")
    if set(readers) != ALL_IDS or set(verified) != ALL_IDS:
        raise ReaderGateError("reader inventory differs")
    families = _object(spec.get("familias"), "families")
    if _ids(families, "P_primaria") != list(PRIMARY_IDS):
        raise ReaderGateError("primary family differs")
    if "L4_masers_6" in _ids(families, "P_primaria"):
        raise ReaderGateError("six masers entered decision family")
    if "L1b_sh0es_r25" not in _ids(families, "R_r25") or "L6_sirenes" not in _ids(families, "S_com_sirenes"):
        raise ReaderGateError("R25/siren family missing")
    if any(verified[r]["status"] != "REAL_DOCUMENTARY_HASH_ONLY" for r in PRIMARY_IDS):
        raise ReaderGateError("primary reader lacks documentary verification")
    if spec.get("state") not in (None, "RASCUNHO_NAO_CONGELADO"):
        raise ReaderGateError("spec state differs")
    scale = scale_from_spec(spec)
    center = _finite(fixture.get("center"), "synthetic center", positive=True)
    bg = _object(fixture.get("background"), "synthetic background")
    if set(bg) != {"sigma"}:
        raise ReaderGateError("synthetic background fields differ")
    bg_sigma = _finite(bg["sigma"], "synthetic background sigma", positive=True)
    offsets = fixture.get("primary_offsets")
    if not isinstance(offsets, list) or len(offsets) != len(PRIMARY_IDS):
        raise ReaderGateError("synthetic offsets malformed")
    offsets = [_finite(v, "synthetic offset") for v in offsets]
    # The fixture contains a made-up center and offsets, never observed H0 values.
    synthetic_y = [scale["K_runtime"] * center + d for d in offsets]
    boxes = {}
    for family in FAMILIES:
        ids = _ids(families, family)
        box = grid_endpoints(spec, ids)
        record = spec["covariancia"][{
            "P_primaria": "five_masers_decision",
            "M_seis_masers_diagnostico": "six_masers_diagnostic",
            "N_sem_cefeidas": "without_cepheids_diagnostic",
        }[family]]
        if box["accepted"] != record["accepted"]:
            raise ReaderGateError("covariance grid count differs from pinned draft")
        for side in ("minimum", "maximum"):
            if not math.isclose(box[side]["sigma_comb"], record[side]["sigma_comb"], abs_tol=1e-10):
                raise ReaderGateError("covariance endpoint differs from pinned draft")
            box[side]["power_only_sigma"] = {}
            for bgid in BG_IDS:
                bg_pin = spec["poder_previo"]["backgrounds"][bgid]
                power = (scale["K_runtime"] - 1) * bg_pin["H0"] / math.sqrt(
                    box[side]["sigma_comb"] ** 2 + (scale["K_runtime"] * bg_pin["sigma"]) ** 2)
                box[side]["power_only_sigma"][bgid] = power
                if not math.isclose(power, record[side]["power_only_sigma"][bgid], abs_tol=1e-9):
                    raise ReaderGateError("sigma-only power differs from pinned draft")
        boxes[family] = box
    primary = boxes["P_primaria"]
    synthetic = {}
    for side in ("minimum", "maximum"):
        synthetic[side] = synthetic_statistics(spec, list(PRIMARY_IDS), synthetic_y,
                                               primary[side]["covariance"], center,
                                               bg_sigma, scale)
    return {
        "stage": "SYNTHETIC_STATISTICAL_REHEARSAL_ONLY", "fixture_id": FIXTURE_ID,
        "fixture_sha256": fixture_sha256, "binding_sha256": gate["binding_sha256"],
        "spec_sha256": gate["spec_sha256"], "draft_v2_sha256": gate["draft_v2_sha256"],
        "scale": scale, "covariance_boxes": boxes, "synthetic_statistics": synthetic,
        "synthetic_fixture_center": center, "synthetic_fixture_offsets": offsets,
        "observed_H0_use_this_fixture": {
            "used": False,
            "basis": "Only K * the reviewed synthetic center 50.0 plus its five fixed offsets enter statistics; spec reader H0 values are never indexed.",
        },
        "data_opened": False,
        "n_alvos_declarados_primary": 0,
        "n_alvos_declarados_inventory": sum(v["status"] == "DECLARADO_UNVERIFIED" for v in verified.values()),
        "operator_admission": "PENDING_D_H", "spec_governance": "PENDING_F3_4",
        "executor_semantics": "PENDING_X13", "v2_frozen": False,
        "verdict": None, "gate_changed": False,
        "unimplemented": ["real-data execution", "operator source admission",
                          "free-background motor and Bayes factor",
                          "full likelihood recovery", "judgment token"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", required=True)
    parser.add_argument("--binding", type=Path, required=True)
    parser.add_argument("--binding-sha256", required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--spec-sha256", required=True)
    parser.add_argument("--synthetic-fixture", type=Path, required=True)
    parser.add_argument("--fixture-sha256", required=True)
    a = parser.parse_args()
    result = run_synthetic(a.binding, a.binding_sha256, a.source_root,
                           a.spec_sha256, a.synthetic_fixture,
                           a.fixture_sha256, mode=a.mode)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
