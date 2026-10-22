"""Append-only snapshots of trusted, server-produced cosmology evaluations.

The HTTP caller must evaluate client parameters on the backend before saving;
never pass a client-supplied evaluation or database path here. Structural checks
do not authenticate arbitrary dictionaries or independently reproduce chi2.
SHA-256 covers canonical UTF-8 JSON without the returned ``sha256`` field
(ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).
This detects corruption, not an attacker able to replace both data and digest.
Saving requires installed runtime source bytes to match its trusted import-time
ENGINE_SHA256, overview and evaluation pins. When ENGINE_COMPONENTS is present,
all component pins and their combined generation must also match before/after
the context snapshot. MISSING components must remain absent. This assumes that
the backend pins its sources at import; it is not a signed bytecode attestation.
Historical reads need neither runtime nor datasets, including older snapshots.
"""
from __future__ import annotations

from contextlib import closing
from datetime import datetime, timezone
import hashlib
import hmac
import importlib
import json
import math
from pathlib import Path
import re
import sqlite3
import unicodedata
import uuid


DB_PATH = Path(__file__).resolve().parent / "state" / "cosmology_scenarios.sqlite3"
SCHEMA_VERSION = "cosmology_scenario_v1"
EVALUATION_SCHEMA = "cosmology_background_v1"
MAX_RECORD_BYTES = 4 * 1024 * 1024
_SHA = re.compile(r"[0-9a-f]{64}\Z")


class ScenarioValidationError(ValueError):
    """Invalid label, identifier, evaluation, or backend provenance."""


class ScenarioIntegrityError(ValueError):
    """Stored bytes or database cannot be trusted; no partial result returned."""


class ScenarioNotFoundError(LookupError):
    """A valid scenario identifier was not found."""


def _canonical(value: object) -> str:
    try:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False)
        if len(text.encode("utf-8")) > MAX_RECORD_BYTES:
            raise ValueError("scenario exceeds storage size limit")
        return text
    except (TypeError, ValueError, UnicodeError, RecursionError) as exc:
        raise ScenarioValidationError(f"Invalid JSON: {exc}") from exc


def _label(value: str) -> str:
    if not isinstance(value, str) or not 1 <= len(value) <= 120:
        raise ScenarioValidationError("label must contain 1..120 characters")
    if not value.strip() or any(unicodedata.category(c).startswith("C") for c in value):
        raise ScenarioValidationError("label must be nonblank and contain no control characters")
    return value.strip()


def _identifier(value: str) -> str:
    try:
        parsed = uuid.UUID(value) if isinstance(value, str) else None
        if parsed is None or parsed.version != 4 or str(parsed) != value:
            raise ValueError("noncanonical UUID")
    except (ValueError, AttributeError) as exc:
        raise ScenarioValidationError("id must be a canonical UUID4") from exc
    return value


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ScenarioValidationError(message)


def _number(value: object) -> bool:
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


def _backend_context(evaluation: dict) -> tuple[dict, dict]:
    # Lazy import: browsing saved scenarios never imports the scientific runtime.
    runtime = importlib.import_module("cosmology_runtime")
    path = Path(runtime.__file__).resolve()
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    loaded_pin = getattr(runtime, "ENGINE_SHA256", None)
    _require(isinstance(loaded_pin, str) and bool(_SHA.fullmatch(loaded_pin)),
             "runtime import-time ENGINE_SHA256 missing or invalid")
    _require(hmac.compare_digest(digest, loaded_pin),
             "installed runtime source differs from import-time ENGINE_SHA256")
    components, generation = None, None
    if hasattr(runtime, "ENGINE_COMPONENTS"):
        declared = runtime.ENGINE_COMPONENTS
        _require(isinstance(declared, dict) and bool(declared), "invalid engine components")
        components = dict(declared)
        root = path.parent

        def verify_components():
            for name, pin in components.items():
                _require(isinstance(name, str) and bool(name) and "\\" not in name
                         and ":" not in name and "\x00" not in name
                         and all(part not in ("", ".", "..") for part in name.split("/")),
                         "unsafe engine component path")
                candidate = (root / name).resolve()
                _require(candidate.is_relative_to(root) and candidate != root,
                         "engine component escapes runtime root")
                _require(isinstance(pin, str) and (pin == "MISSING" or bool(_SHA.fullmatch(pin))),
                         f"invalid engine component pin: {name}")
                if pin == "MISSING":
                    _require(not candidate.exists(), f"previously MISSING engine component appeared: {name}")
                else:
                    _require(candidate.is_file(), f"engine component missing: {name}")
                    _require(hmac.compare_digest(hashlib.sha256(candidate.read_bytes()).hexdigest(), pin),
                             f"engine component changed: {name}")

        verify_components()
        _require(components.get(path.name) == loaded_pin, "engine components must pin the runtime itself")
        generation = hashlib.sha256("\n".join(
            f"{name}:{pin}" for name, pin in sorted(components.items())).encode("utf-8")).hexdigest()
        _require(getattr(runtime, "ENGINE_GENERATION", None) == generation,
                 "runtime engine generation mismatch")
    overview = json.loads(_canonical(runtime.overview()))
    _require(overview.get("status") == "ok", "backend overview unavailable")
    _require(overview.get("engine_sha256") == loaded_pin, "overview engine pin mismatch")
    dataset = overview.get("dataset", {})
    for key, filename in (("mean_sha256", runtime.MEAN_FILE),
                          ("covariance_sha256", runtime.COV_FILE)):
        pin = runtime.EXPECTED_SHA256[filename]
        _require(isinstance(pin, str) and bool(_SHA.fullmatch(pin))
                 and dataset.get(key) == pin, f"source pin mismatch: {key}")
    _require(path.read_bytes() == raw, "runtime source changed during snapshot")
    engine = {"path": str(path), "sha256": digest,
              "hash_scope": "INSTALLED_SOURCE_MATCHES_IMPORT_TIME_PIN"}
    if components is not None:
        verify_components()
        _require(runtime.ENGINE_COMPONENTS == components and runtime.ENGINE_GENERATION == generation,
                 "runtime engine metadata changed during snapshot")
        for name, receipt in (("overview", overview), ("evaluation", evaluation)):
            _require(receipt.get("engine_generation") == generation, f"{name} engine generation mismatch")
            _require(receipt.get("engine_components") == components, f"{name} engine components mismatch")
        engine.update(generation=generation, components=components,
                      hash_scope="INSTALLED_COMPONENTS_MATCH_IMPORT_TIME_PINS")
    return overview, engine


def _validate(evaluation: dict, overview: dict) -> None:
    try:
        _require(evaluation["status"] == overview["status"] == "ok", "only successful evaluations may be saved")
        _require(evaluation["schema_version"] == overview["schema_version"] == EVALUATION_SCHEMA,
                 "unsupported evaluation schema")
        model = evaluation["model"]
        _require(isinstance(model, dict) and all(isinstance(model[k], str) and model[k].strip()
                 for k in ("id", "status")), "model identity and status required")
        # Model identifiers are deliberately not restricted to today's CPL engine.
        params, rules = evaluation["parameters"], overview["parameters"]
        _require(isinstance(params, dict) and set(params) == set(rules), "parameter keys mismatch")
        for key, value in params.items():
            _require(_number(value) and rules[key]["min"] <= value <= rules[key]["max"],
                     f"invalid parameter: {key}")
        data = overview["dataset"]
        _require(evaluation["dataset_id"] == data["id"], "dataset identity mismatch")
        _require(evaluation["memory"]["load_id"] == overview["memory"]["load_id"],
                 "evaluation and overview come from different resident loads")
        rows, points = evaluation["observations"], data["points"]
        _require(isinstance(rows, list) and len(rows) == len(points) == data["n_points"] > 0,
                 "observation count mismatch")
        _require(evaluation["residual_definition"] == "predicted_minus_observed", "residual convention mismatch")
        for row, point in zip(rows, points):
            _require(all(row[key] == point[key] for key in ("z", "type", "observed", "sigma")),
                     "observation differs from pinned overview")
            _require(_number(row["predicted"]) and _number(row["residual"])
                     and math.isclose(row["residual"], row["predicted"] - row["observed"],
                                      rel_tol=1e-10, abs_tol=1e-10), "invalid residual")
        chi2 = evaluation["chi2"]
        _require(_number(chi2["value"]) and chi2["value"] >= 0
                 and type(chi2["n_points"]) is int and chi2["n_points"] == len(rows), "invalid chi2")
        _require(isinstance(chi2["method"], str) and bool(chi2["method"])
                 and chi2["status"] == overview["evaluation_status"], "chi2 method/status mismatch")
        _require(isinstance(evaluation["series"], list) and bool(evaluation["series"])
                 and all(isinstance(row, dict) for row in evaluation["series"]), "series required")
        _require(isinstance(evaluation["cursor"], dict)
                 and evaluation["cursor"]["z"] == params["redshift"], "cursor/input mismatch")
        _require(isinstance(evaluation["quadrature"], dict)
                 and _number(evaluation["elapsed_ms"]) and evaluation["elapsed_ms"] >= 0,
                 "execution receipt required")
    except (KeyError, TypeError, AttributeError, IndexError) as exc:
        raise ScenarioValidationError(f"Incomplete evaluation/overview: {exc}") from exc


def _summary(record: dict) -> dict:
    evaluation = record["evaluation"]
    return {"id": record["id"], "label": record["label"], "created_at_utc": record["created_at_utc"],
            "parameters": record["inputs"], "model_id": evaluation["model"]["id"],
            "model_status": evaluation["model"]["status"], "dataset_id": evaluation["dataset_id"],
            "chi2": evaluation["chi2"], "engine_sha256": record["provenance"]["engine"]["sha256"],
            "sha256": record["sha256"]}


def _decode(row: tuple) -> dict:
    identifier, text, digest = row
    try:
        _identifier(identifier)
        if not isinstance(digest, str) or not _SHA.fullmatch(digest):
            raise ValueError("invalid digest")
        if not hmac.compare_digest(hashlib.sha256(text.encode("utf-8")).hexdigest(), digest):
            raise ValueError("stored JSON SHA-256 mismatch")
        record = json.loads(text)
        if _canonical(record) != text:
            raise ValueError("stored JSON is not canonical")
        if record["id"] != identifier or record["schema_version"] != SCHEMA_VERSION or "sha256" in record:
            raise ValueError("stored identity/schema mismatch")
        _label(record["label"])
        _validate(record["evaluation"], record["overview"])
        if record["inputs"] != record["evaluation"]["parameters"]:
            raise ValueError("stored inputs mismatch")
        record["sha256"] = digest
        _summary(record)  # Missing fields must fail get and list alike.
        return record
    except (ValueError, TypeError, KeyError, AttributeError, UnicodeError, RecursionError) as exc:
        raise ScenarioIntegrityError(f"Corrupt scenario {identifier}: {exc}") from exc


def save_scenario(label: str, evaluation: dict, *, db_path: Path | str | None = None) -> dict:
    """Save a newly evaluated trusted backend result; return compact summary.

    db_path is a server/test configuration hook, never an HTTP input. No existing
    row is overwritten, including when a label or parameters repeat.
    """
    label = _label(label)
    _require(isinstance(evaluation, dict), "evaluation must be an object")
    evaluation = json.loads(_canonical(evaluation))
    try:
        overview, engine = _backend_context(evaluation)
    except (KeyError, TypeError, AttributeError) as exc:
        raise ScenarioValidationError(f"Invalid backend provenance: {exc}") from exc
    _require(evaluation.get("engine_sha256") == engine["sha256"], "evaluation engine pin mismatch")
    _validate(evaluation, overview)
    record = {"schema_version": SCHEMA_VERSION, "id": str(uuid.uuid4()), "label": label,
              "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
              "inputs": evaluation["parameters"], "evaluation": evaluation, "overview": overview,
              "provenance": {"engine": engine, "evaluation_origin": "TRUSTED_BACKEND_REQUIRED",
                             "data_hashes": {key: overview["dataset"][key]
                                             for key in ("mean_sha256", "covariance_sha256")}}}
    text = _canonical(record)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    path = Path(db_path) if db_path is not None else DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with closing(sqlite3.connect(path, timeout=10)) as connection:
            connection.execute("PRAGMA synchronous=FULL")
            with connection:
                connection.execute("CREATE TABLE IF NOT EXISTS scenarios "
                                   "(id TEXT PRIMARY KEY, record_json TEXT NOT NULL, sha256 TEXT NOT NULL)")
                for operation in ("UPDATE", "DELETE"):
                    connection.execute(f"CREATE TRIGGER IF NOT EXISTS scenarios_no_{operation.lower()} "
                                       f"BEFORE {operation} ON scenarios BEGIN "
                                       "SELECT RAISE(ABORT, 'scenarios are append-only'); END")
                connection.execute("INSERT INTO scenarios VALUES (?, ?, ?)", (record["id"], text, digest))
    except sqlite3.Error as exc:
        raise ScenarioIntegrityError(f"Scenario storage failed: {exc}") from exc
    record["sha256"] = digest
    return _summary(record)


def _read(identifier: str | None, db_path: Path | str | None) -> list[dict]:
    path = Path(db_path) if db_path is not None else DB_PATH
    if not path.exists():
        return []
    try:
        with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True, timeout=10)) as connection:
            if identifier is None:
                rows = connection.execute("SELECT id, record_json, sha256 FROM scenarios ORDER BY rowid DESC")
            else:
                rows = connection.execute("SELECT id, record_json, sha256 FROM scenarios WHERE id=?", (identifier,))
            return [_decode(row) for row in rows]
    except sqlite3.Error as exc:
        raise ScenarioIntegrityError(f"Scenario database unreadable: {exc}") from exc


def list_scenarios(*, db_path: Path | str | None = None) -> list[dict]:
    """List verified summaries, newest insertion first; fail on any corrupt row."""
    return [_summary(record) for record in _read(None, db_path)]


def get_scenario(id: str, *, db_path: Path | str | None = None) -> dict:
    """Return the full verified snapshot plus its export digest, or raise."""
    rows = _read(_identifier(id), db_path)
    if not rows:
        raise ScenarioNotFoundError(id)
    return rows[0]
