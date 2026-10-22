"""Read-only DESI DR2 BAO background explorer.

This is a flat matter+CPL dark-energy visualization at z <= 3. It is not a
TGL prediction, cosmological fit, or significance calculation. GW state is not
imported or touched. The two small local data copies are verified before being
held as immutable tuples in RAM.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import hashlib
import math
from pathlib import Path
from threading import Lock
import time
import uuid


SCHEMA_VERSION = "cosmology_background_v1"
ENGINE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
ENGINE_FILES = ("cosmology_runtime.py", "cosmology_v3_bridge.py", "workers/cosmology_v3_worker.py",
                "scientific_models/tgl_camb_worker_v3.py")
ENGINE_COMPONENTS = {name: hashlib.sha256((Path(__file__).parent / name).read_bytes()).hexdigest()
                     if (Path(__file__).parent / name).is_file() else "MISSING"
                     for name in ENGINE_FILES}
ENGINE_GENERATION = hashlib.sha256("\n".join(f"{name}:{pin}" for name, pin in sorted(ENGINE_COMPONENTS.items())).encode()).hexdigest()
MODEL_STATUS = "EXPLORATORY_BACKGROUND_NOT_TGL_PREDICTION"
DATASET_ID = "DESI_DR2_BAO_ALL_GCcomb"
C_KM_S = 299792.458
DATA_DIR = Path(__file__).resolve().parent / "data" / "cosmology"
MEAN_FILE = "desi_gaussian_bao_ALL_GCcomb_mean.txt"
COV_FILE = "desi_gaussian_bao_ALL_GCcomb_cov.txt"
EXPECTED_SHA256 = {
    MEAN_FILE: "9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585",
    COV_FILE: "252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509",
}
TYPE_MAP = {"DV_over_rs": "DV_over_rd", "DM_over_rs": "DM_over_rd",
            "DH_over_rs": "DH_over_rd"}
PARAMETERS = {
    "H0": (40.0, 100.0, 67.4, "km/s/Mpc"),
    "omega_m": (0.1, 0.5, 0.315, "dimensionless"),
    "rd_mpc": (120.0, 170.0, 147.09, "Mpc"),
    "w0": (-1.5, -0.5, -1.0, "dimensionless"),
    "wa": (-1.0, 1.0, 0.0, "dimensionless"),
    "redshift": (0.001, 3.0, 0.5, "dimensionless"),
}
_LOAD_LOCK = Lock()
_SOURCE_READS = 0


class CosmologyDataError(ValueError):
    """A local dataset is missing, changed, or structurally invalid."""


@dataclass(frozen=True)
class _Dataset:
    points: tuple[tuple[float, str, float, float], ...]
    covariance: tuple[tuple[float, ...], ...]
    cholesky: tuple[tuple[float, ...], ...]
    load_id: str
    loaded_source_bytes: int
    source_reads_at_load: int
    source_reads_for_load: int


def _verified_text(name: str) -> tuple[str, int]:
    global _SOURCE_READS
    try:
        raw = (DATA_DIR / name).read_bytes()
    except OSError as exc:
        raise CosmologyDataError(f"DESI data unavailable: {name}: {exc}") from exc
    _SOURCE_READS += 1
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256[name]:
        raise CosmologyDataError(f"DESI data SHA-256 mismatch: {name}")
    try:
        return raw.decode("utf-8"), len(raw)
    except UnicodeError as exc:
        raise CosmologyDataError(f"DESI data encoding invalid: {name}") from exc


def _cholesky(covariance: tuple[tuple[float, ...], ...]) -> tuple[tuple[float, ...], ...]:
    n = len(covariance)
    lower = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            value = covariance[i][j] - sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                if not math.isfinite(value) or value <= 0.0:
                    raise CosmologyDataError("DESI covariance is not positive definite")
                lower[i][j] = math.sqrt(value)
            else:
                lower[i][j] = value / lower[j][j]
    return tuple(tuple(row) for row in lower)


@lru_cache(maxsize=1)
def _cached_load_dataset() -> _Dataset:
    reads_before = _SOURCE_READS
    mean_text, mean_bytes = _verified_text(MEAN_FILE)
    cov_text, cov_bytes = _verified_text(COV_FILE)
    try:
        rows = []
        for line in mean_text.splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            z, value, source_type = line.split()
            if source_type not in TYPE_MAP:
                raise ValueError(f"unknown BAO observable: {source_type}")
            rows.append((float(z), TYPE_MAP[source_type], float(value)))
        if len(rows) != 13 or len({(z, kind) for z, kind, _ in rows}) != 13:
            raise ValueError("DESI mean must have 13 unique (z, type) rows")
        if any(not 0.0 < z <= 3.0 or not math.isfinite(value)
               for z, _, value in rows):
            raise ValueError("DESI mean contains invalid values")
        tokens = [float(token) for token in cov_text.split()]
        if len(tokens) != 13 * 13 or any(not math.isfinite(x) for x in tokens):
            raise ValueError("DESI covariance must be finite and 13x13")
        covariance = tuple(tuple(tokens[i * 13:(i + 1) * 13]) for i in range(13))
        if any(not math.isclose(covariance[i][j], covariance[j][i], rel_tol=1e-12, abs_tol=1e-14)
               for i in range(13) for j in range(i)):
            raise ValueError("DESI covariance is not symmetric")
        lower = _cholesky(covariance)
        points = tuple((z, kind, value, math.sqrt(covariance[i][i]))
                       for i, (z, kind, value) in enumerate(rows))
    except (ValueError, IndexError, ZeroDivisionError) as exc:
        raise CosmologyDataError(f"DESI data invalid: {exc}") from exc
    return _Dataset(points, covariance, lower, uuid.uuid4().hex,
                    mean_bytes + cov_bytes, _SOURCE_READS,
                    _SOURCE_READS - reads_before)


def _load_dataset() -> _Dataset:
    # lru_cache alone may compute a concurrent first miss twice. The lock keeps
    # one custody read pair and one immutable resident dataset per process.
    with _LOAD_LOCK:
        return _cached_load_dataset()


def _memory_receipt(data: _Dataset) -> dict:
    matrix_count = len(data.covariance) ** 2
    return {
        "load_id": data.load_id,
        "loaded_source_bytes": data.loaded_source_bytes,
        "source_reads_for_load": data.source_reads_for_load,
        "source_reads_total": _SOURCE_READS,
        "source_reads_since_load": _SOURCE_READS - data.source_reads_at_load,
        "matrix_numeric_elements": matrix_count,
        "matrix_numeric_payload_bytes": matrix_count * 8,
        "matrix_numeric_payload_note": "float64-equivalent numeric payload; not Python RSS",
        "cache": "IMMUTABLE_RAM_LRU_1",
    }


MODEL_IDS = ("FLAT_MATTER_CPL_BACKGROUND", "TGL_V3_TOTAL_FIXED_BETA", "V3_TOTAL_BETA_ZERO")


def _model(model_id: str = MODEL_IDS[0]) -> dict:
    if model_id in MODEL_IDS[1:]:
        return {
            "id": model_id,
            "status": "V3_TOTAL_FLUID_PRIMITIVE__CONDITIONAL",
            "domain": "0 <= z <= 3; flat; radiation+matter+Lambda; fixed Neff/TCMB; rd independent",
            "equation": "E(a)^2=rho(a)+beta*J(a); J(a)=integral_a^infinity 3*(rho+p)^2/(rho*a) da",
            "beta_mode": "fixed" if model_id == MODEL_IDS[1] else "zero",
            "branch": "Phi=1+beta*(rho+p)/rho; historical V3 branch, not reciprocal face",
            "normalization": "P(infinity)=rho_Lambda; C=0; Omega_Lambda solved by E(0)=1",
            "scope": "BACKGROUND_ONLY_NOT_FULL_CMB_PREDICTION",
        }

    return {
        "id": "FLAT_MATTER_CPL_BACKGROUND",
        "status": MODEL_STATUS,
        "domain": "0 <= z <= 3; no radiation or curvature",
        "equation": "E(z)^2=omega_m*(1+z)^3+(1-omega_m)*(1+z)^(3*(1+w0+wa))*exp(-3*wa*z/(1+z))",
    }


def _error(code: str, message: str, started: float) -> dict:
    return {"schema_version": SCHEMA_VERSION, "status": "error",
            "error": {"code": code, "message": message},
            "elapsed_ms": (time.perf_counter() - started) * 1000.0}


def overview() -> dict:
    """Return the frozen UI contract, all observations, and full covariance."""
    started = time.perf_counter()
    try:
        data = _load_dataset()
    except CosmologyDataError as exc:
        return _error("DATA_INTEGRITY", str(exc), started)
    result = {
        "schema_version": SCHEMA_VERSION, "status": "ok", "model": _model(),
        "engine_sha256": ENGINE_SHA256,
        "engine_generation": ENGINE_GENERATION, "engine_components": ENGINE_COMPONENTS,
        "models": [_model(item) for item in MODEL_IDS],
        "memory": _memory_receipt(data),
        "quadrature": {"method": "COMPOSITE_SIMPSON", "intervals": 256,
                       "cursor_refined_intervals": 512},
        "parameters": {key: {"min": low, "max": high, "default": default, "unit": unit}
                       for key, (low, high, default, unit) in PARAMETERS.items()},
        "dataset": {
            "id": DATASET_ID, "release_label": "DESI DR2 BAO, local CobayaSampler/bao_data copy",
            "release_commit_verified": False, "n_points": len(data.points),
            "n_distinct_redshifts": len({row[0] for row in data.points}),
            "mean_sha256": EXPECTED_SHA256[MEAN_FILE],
            "covariance_sha256": EXPECTED_SHA256[COV_FILE],
            "covariance_order": "same order as points",
            "points": [{"z": z, "type": kind, "observed": value, "sigma": sigma}
                       for z, kind, value, sigma in data.points],
            "covariance": [list(row) for row in data.covariance],
        },
        "evaluation_status": "VISUAL_DIAGNOSTIC_NOT_FIT_OR_SIGMA",
    }
    result["elapsed_ms"] = (time.perf_counter() - started) * 1000.0
    return result


def _parameters(payload: dict) -> dict[str, float]:
    if not isinstance(payload, dict):
        raise ValueError("payload must be a JSON object")
    unknown = set(payload) - set(PARAMETERS)
    if unknown:
        raise ValueError("unknown parameters: " + ", ".join(sorted(map(str, unknown))))
    parsed = {}
    for key, (low, high, default, _) in PARAMETERS.items():
        value = payload.get(key, default)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{key} must be a finite number")
        try:
            value = float(value)
        except (OverflowError, ValueError) as exc:
            raise ValueError(f"{key} must be a finite number") from exc
        if not math.isfinite(value) or not low <= value <= high:
            raise ValueError(f"{key} must be finite and within [{low}, {high}]")
        parsed[key] = value
    return parsed


def _e(z: float, p: dict[str, float]) -> float:
    one_plus_z = 1.0 + z
    de = (1.0 - p["omega_m"]) * math.exp(
        3.0 * (1.0 + p["w0"] + p["wa"]) * math.log1p(z)
        - 3.0 * p["wa"] * z / one_plus_z)
    return math.sqrt(p["omega_m"] * one_plus_z**3 + de)


def _comoving_distance_mpc(z: float, p: dict[str, float], intervals: int = 256) -> float:
    """Composite Simpson integral of c/H from 0 to z (even intervals)."""
    if z == 0.0:
        return 0.0
    if intervals < 2 or intervals % 2:
        raise ValueError("intervals must be even and >= 2")
    step = z / intervals
    total = 1.0 / _e(0.0, p) + 1.0 / _e(z, p)
    for i in range(1, intervals):
        total += (4.0 if i % 2 else 2.0) / _e(i * step, p)
    return C_KM_S / p["H0"] * step * total / 3.0


def _distances(z: float, p: dict[str, float]) -> dict:
    dm = _comoving_distance_mpc(z, p)
    dh = C_KM_S / (p["H0"] * _e(z, p))
    dv = (z * dm * dm * dh) ** (1.0 / 3.0) if z else 0.0
    rd = p["rd_mpc"]
    return {"z": z, "dm_mpc": dm, "dh_mpc": dh, "dv_mpc": dv,
            "dm_over_rd": dm / rd, "dh_over_rd": dh / rd, "dv_over_rd": dv / rd}


def _chi2(residual: list[float], lower: tuple[tuple[float, ...], ...]) -> float:
    whitened = []
    for i, value in enumerate(residual):
        projected = (value - sum(lower[i][j] * whitened[j] for j in range(i))) / lower[i][i]
        whitened.append(projected)
    return sum(x * x for x in whitened)


def _v3_require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError("Invalid V3 response: " + message)


def _v3_number(value, name: str) -> float:
    _v3_require(type(value) in (int, float), name + " must be numeric")
    _v3_require(math.isfinite(value), name + " must be finite")
    return value


def _v3_json(value) -> None:
    """Reject nonfinite/unsupported values even in additive receipt fields."""
    if isinstance(value, dict):
        for key, item in value.items():
            _v3_require(isinstance(key, str), "JSON keys must be strings")
            _v3_json(item)
    elif isinstance(value, list):
        for item in value:
            _v3_json(item)
    elif type(value) in (int, float):
        _v3_number(value, "receipt value")
    else:
        _v3_require(value is None or type(value) in (str, bool), "non-JSON receipt value")


def _v3_point(row: dict, rd: float) -> None:
    _v3_require(isinstance(row, dict), "distance row must be an object")
    z = _v3_number(row["z"], "z")
    _v3_require(0 <= z <= 3, "redshift outside displayed domain")
    for kind in ("dm", "dh", "dv"):
        mpc = _v3_number(row[kind + "_mpc"], kind + "_mpc")
        ratio = _v3_number(row[kind + "_over_rd"], kind + "_over_rd")
        # Broad unit/overflow guard, far outside this z<=3 Mpc interface's
        # distances; it is not a cosmological prior or a goodness-of-fit cut.
        _v3_require(0 <= mpc <= 1e9 and ratio >= 0, "invalid distance magnitude")
        _v3_require(math.isclose(ratio, mpc / rd, rel_tol=1e-10, abs_tol=1e-12),
                    kind + " Mpc/rd units mismatch")
    _v3_require(row["dh_mpc"] > 0, "D_H must be positive")
    if z == 0:
        _v3_require(row["dm_mpc"] == row["dv_mpc"] == 0, "nonzero distance at z=0")
    else:
        _v3_require(row["dm_mpc"] > 0 and row["dv_mpc"] > 0, "nonpositive distance at z>0")
    expected_dv = (z * row["dm_mpc"] ** 2 * row["dh_mpc"]) ** (1 / 3) if z else 0.0
    _v3_require(math.isclose(row["dv_mpc"], expected_dv, rel_tol=1e-10, abs_tol=1e-10),
                "D_V identity/units mismatch")


def _validate_v3_success(v3: dict, p: dict, model_id: str, redshifts: list[float]) -> dict:
    """Validate the entire worker receipt before observations or chi2 are used."""
    if isinstance(v3, dict) and (v3.get("status") != "ok" or "error" in v3):
        error = v3.get("error")
        message = error.get("message") if isinstance(error, dict) else error
        raise ValueError("V3 worker unavailable: " + str(message or "invalid success status"))
    _v3_require(isinstance(v3, dict) and v3.get("status") == "ok" and "error" not in v3,
                "worker did not return an unambiguous success")
    _v3_json(v3)
    pins = v3["source_hashes"]
    _v3_require(isinstance(pins, dict), "source_hashes must be an object")
    for key, component in (("scientific_model_sha256", "scientific_models/tgl_camb_worker_v3.py"),
                           ("adapter_worker_sha256", "workers/cosmology_v3_worker.py"),
                           ("bridge_sha256", "cosmology_v3_bridge.py")):
        expected = ENGINE_COMPONENTS.get(component)
        _v3_require(isinstance(expected, str) and len(expected) == 64
                    and pins.get(key) == expected, key + " differs from imported engine generation")

    _v3_require(_v3_number(v3["elapsed_ms"], "elapsed_ms") >= 0, "negative elapsed_ms")
    series, cursor, exact = v3["series"], v3["cursor"], v3["distances"]
    _v3_require(isinstance(exact, list), "exact distances must be a list")
    by_z = {}
    for row in exact:
        _v3_point(row, p["rd_mpc"])
        _v3_require(row["z"] not in by_z, "duplicate exact observation redshift")
        by_z[row["z"]] = row
    for z in redshifts:
        _v3_require(z in by_z, f"Missing exact observation redshift {z}")
    _v3_require(set(by_z) == set(redshifts), "unrequested exact observation redshift")

    _v3_require(isinstance(series, list) and len(series) == 121, "series must contain 121 points")
    for i, row in enumerate(series):
        _v3_point(row, p["rd_mpc"])
        _v3_require(math.isclose(row["z"], i * 3.0 / 120, rel_tol=0, abs_tol=1e-12),
                    "visual redshift grid mismatch")
    # The worker permits an E(0) residual up to 5e-6. This independent unit
    # anchor catches a uniformly rescaled Mpc/rd pair without re-solving V3.
    _v3_require(math.isclose(series[0]["dh_mpc"], C_KM_S / p["H0"], rel_tol=1e-5),
                "D_H(0) inconsistent with H0/Mpc units")
    _v3_point(cursor, p["rd_mpc"])
    _v3_require(cursor["z"] == p["redshift"], "cursor redshift mismatch")

    quadrature, details = v3["quadrature"], v3["details"]
    _v3_require(isinstance(quadrature, dict) and isinstance(details, dict), "execution metadata required")
    _v3_require(isinstance(quadrature.get("method"), str) and bool(quadrature["method"].strip()),
                "quadrature method required")
    for key in ("ngrid_pinned", "local_refined_points", "distance_intervals_pinned", "cursor_refined_intervals"):
        _v3_require(type(quadrature.get(key)) is int and quadrature[key] > 0, "invalid " + key)
    _v3_require(quadrature.get("local_z_range") == [0.0, 3.0], "quadrature domain mismatch")
    for z in quadrature["local_z_range"]:
        _v3_number(z, "quadrature redshift")
    for key in ("max_relative_e_refinement", "max_relative_second_friedmann_residual",
                "e0_residual", "cursor_dm_relative_delta"):
        _v3_require(_v3_number(quadrature[key], key) >= 0, "negative " + key)
    _v3_require(_v3_number(quadrature["min_e2_z0_to_3"], "min_e2_z0_to_3") > 0, "nonpositive E2")
    mode = "fixed" if model_id == MODEL_IDS[1] else "zero"
    _v3_require(details.get("model_id") == model_id and details.get("beta_mode") == mode,
                "worker model/beta mode mismatch")
    _v3_require(details.get("status") == "CONDITIONAL_V3_TOTAL_FLUID_BACKGROUND_ONLY", "worker scope mismatch")
    beta = _v3_number(details["beta"], "beta")
    _v3_require(beta == 0 if mode == "zero" else beta > 0, "beta inconsistent with selected mode")
    for key in ("omega_r", "omega_m_effective", "omega_lambda_closed", "background_build_ms"):
        _v3_require(_v3_number(details[key], key) >= 0, "negative " + key)
    _v3_require(_v3_number(details["c"], "c") == 0, "V3 requires C=0")
    _v3_require(math.isclose(details["omega_m_effective"], p["omega_m"], rel_tol=1e-10, abs_tol=1e-12),
                "worker matter density mismatch")
    _v3_require(type(details.get("background_cache_hit")) is bool, "cache receipt required")
    _v3_require(type(details.get("background_builds")) is int and details["background_builds"] > 0,
                "build receipt required")
    _v3_require(isinstance(details.get("assumptions"), list) and bool(details["assumptions"])
                and all(isinstance(item, str) and item.strip() for item in details["assumptions"]),
                "worker assumptions required")
    mapping = details["mapping"]
    _v3_require(isinstance(mapping, dict), "density mapping required")
    for key in ("ombh2", "omch2", "mnu_ev", "TCMB_K", "Neff"):
        _v3_require(_v3_number(mapping[key], key) >= 0, "negative " + key)
    _v3_require(isinstance(mapping.get("note"), str) and bool(mapping["note"].strip()), "mapping note required")
    return by_z


def evaluate(payload: dict) -> dict:
    """Evaluate a single background curve and the full-covariance residual."""
    started = time.perf_counter()
    try:
        if not isinstance(payload, dict):
            raise ValueError("payload must be an object")
        model_id = payload.get("model_id", MODEL_IDS[0])
        if model_id not in MODEL_IDS:
            raise ValueError("Unknown cosmology model")
        p = _parameters({key: value for key, value in payload.items() if key != "model_id"})
        if model_id != MODEL_IDS[0] and (p["w0"] != -1.0 or p["wa"] != 0.0):
            raise ValueError("V3 requires w0=-1 and wa=0 (Lambda)")
    except ValueError as exc:
        return _error("INVALID_INPUT", str(exc), started)
    try:
        data = _load_dataset()
    except CosmologyDataError as exc:
        return _error("DATA_INTEGRITY", str(exc), started)
    v3 = None
    if model_id == MODEL_IDS[0]:
        series = [_distances(i * 3.0 / 120, p) for i in range(121)]
        cursor = _distances(p["redshift"], p)
        refined = _comoving_distance_mpc(p["redshift"], p, intervals=512)
        quadrature = {"method": "COMPOSITE_SIMPSON", "intervals": 256,
                      "cursor_refined_intervals": 512,
                      "cursor_dm_relative_delta": abs(refined - cursor["dm_mpc"]) / refined}
        by_z = {item["z"]: item for item in series}
    else:
        try:
            from cosmology_v3_bridge import evaluate_background
            redshifts = sorted({row[0] for row in data.points})
            v3 = evaluate_background(p, "fixed" if model_id == MODEL_IDS[1] else "zero",
                                     redshifts=redshifts)
            by_z = _validate_v3_success(v3, p, model_id, redshifts)
            series, cursor, quadrature = v3["series"], v3["cursor"], v3["quadrature"]
        except Exception as exc:
            # Scientific worker failure is visible; never substitute CPL silently.
            return _error("V3_UNAVAILABLE", str(exc), started)
    observations = []
    residual = []
    field = {"DM_over_rd": "dm_over_rd", "DH_over_rd": "dh_over_rd",
             "DV_over_rd": "dv_over_rd"}
    for z, kind, observed, sigma in data.points:
        prediction = by_z.get(z)
        if prediction is None:
            if model_id != MODEL_IDS[0]:
                return _error("V3_UNAVAILABLE", f"Missing exact observation redshift {z}", started)
            prediction = _distances(z, p)
            by_z[z] = prediction
        predicted = prediction[field[kind]]
        difference = predicted - observed
        residual.append(difference)
        observations.append({"z": z, "type": kind, "observed": observed,
                             "sigma": sigma, "predicted": predicted, "residual": difference})
    result = {
        "schema_version": SCHEMA_VERSION, "status": "ok", "model": _model(model_id),
        "engine_sha256": ENGINE_SHA256,
        "engine_generation": ENGINE_GENERATION, "engine_components": ENGINE_COMPONENTS,
        "data_hashes": {"mean_sha256": EXPECTED_SHA256[MEAN_FILE],
                        "covariance_sha256": EXPECTED_SHA256[COV_FILE]},
        "memory": _memory_receipt(data),
        "parameters": p, "cursor": cursor, "series": series,
        "quadrature": quadrature,
        "dataset_id": DATASET_ID, "observations": observations,
        "residual_definition": "predicted_minus_observed",
        "chi2": {"value": _chi2(residual, data.cholesky), "n_points": 13,
                 "method": "CHOLESKY_FULL_COVARIANCE",
                 "status": "VISUAL_DIAGNOSTIC_NOT_FIT_OR_SIGMA"},
    }
    if v3 is not None:
        result["model"]["execution"] = v3["details"]
        result["model"]["source_hashes"] = v3["source_hashes"]
    result["elapsed_ms"] = (time.perf_counter() - started) * 1000.0
    return result
