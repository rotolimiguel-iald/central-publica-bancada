"""Durable local JSON exports; no HTTP, browser, or resident GW dependencies.

Public failures raise ValueError. Comparison accepts only six numeric inputs and
optional model_id, then calls the trusted runtime twice. Exports are exploratory,
not preregistrations, fits, or significance estimates. SHA-256 covers canonical
UTF-8 JSON excluding the top-level sha256 field, using the scenario serializer.
It detects corruption, not replacement of both content and digest by an attacker.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import hmac
import importlib
import json
import os
from pathlib import Path
import tempfile
import uuid

import cosmology_scenarios as scenarios


EXPORT_DIR = Path(__file__).resolve().parent / "state" / "exports"
SCHEMA_VERSION = "cosmology_export_v1"
_NUMERIC_KEYS = frozenset(("H0", "omega_m", "rd_mpc", "w0", "wa", "redshift"))


def _copy(value):
    return json.loads(scenarios._canonical(value))


def _export_path(identifier: str) -> Path:
    identifier = scenarios._identifier(identifier)
    root = Path(EXPORT_DIR).resolve()
    path = root / (identifier + ".json")
    scenarios._require(not path.is_symlink() and path.resolve().parent == root,
                       "export path escapes configured directory")
    return path


def _parameters(value: dict) -> dict:
    scenarios._require(isinstance(value, dict), "parameters must be an object")
    keys = set(value)
    scenarios._require(keys in (_NUMERIC_KEYS, _NUMERIC_KEYS | {"model_id"}),
                       "parameters require six numeric fields and optional model_id only")
    for key in _NUMERIC_KEYS:
        scenarios._require(scenarios._number(value[key]), f"invalid numeric parameter: {key}")
    if "model_id" in value:
        scenarios._require(isinstance(value["model_id"], str) and bool(value["model_id"].strip()),
                           "model_id must be a nonempty string")
    return _copy(value)


def _checked_result(evaluation: dict, request: dict) -> dict:
    evaluation = _copy(evaluation)
    scenarios._require(isinstance(evaluation, dict) and evaluation.get("status") == "ok",
                       "backend calculation did not succeed")
    overview, engine = scenarios._backend_context(evaluation)
    scenarios._validate(evaluation, overview)
    scenarios._require(evaluation.get("engine_sha256") == engine["sha256"], "evaluation engine mismatch")
    hashes = {key: overview["dataset"][key] for key in ("mean_sha256", "covariance_sha256")}
    scenarios._require(evaluation.get("data_hashes") == hashes, "evaluation data hashes mismatch")
    scenarios._require(evaluation["parameters"] == {key: request[key] for key in _NUMERIC_KEYS},
                       "backend evaluated different parameters")
    expected_model = request.get("model_id", overview["model"]["id"])
    scenarios._require(evaluation["model"]["id"] == expected_model, "backend evaluated a different model")
    return {"request_parameters": _copy(request), "evaluation": evaluation, "overview": overview,
            "provenance": {"engine": engine, "data_hashes": hashes}}


def _publish(kind: str, payload: dict, provenance: dict) -> dict:
    identifier = str(uuid.uuid4())
    record = {"schema_version": SCHEMA_VERSION, "id": identifier, "kind": kind,
              "status": "exploratory", "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
              "payload": payload, "data_hashes": provenance["data_hashes"], "engine": provenance["engine"]}
    canonical = scenarios._canonical(record).encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()
    record["sha256"] = digest
    raw = scenarios._canonical(record).encode("utf-8")
    path = _export_path(identifier)
    scenarios._require(not path.exists(), "export UUID collision; existing file preserved")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=path.parent, prefix=".export-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        scenarios._require(temporary.stat().st_size == len(raw), "incomplete export write")
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return {"id": identifier, "path": str(path), "sha256": digest,
            "download_url": "/api/cosmology/exports/" + identifier}


def export_scenario(id: str) -> dict:
    """Export a hash-verified historical scenario; never re-evaluate it."""
    try:
        record = scenarios.get_scenario(scenarios._identifier(id))
        return _publish("scenario", {"scenario": record}, record["provenance"])
    except Exception as exc:
        raise ValueError(f"Scenario export failed: {exc}") from exc


def export_comparison(reference_parameters: dict, current_parameters: dict) -> dict:
    """Re-evaluate reference A/current B with the same engine and data pins."""
    try:
        reference_request = _parameters(reference_parameters)
        current_request = _parameters(current_parameters)
        runtime = importlib.import_module("cosmology_runtime")
        reference = _checked_result(runtime.evaluate(_copy(reference_request)), reference_request)
        current = _checked_result(runtime.evaluate(_copy(current_request)), current_request)
        # Check A again after B: source changes during either calculation fail closed.
        reference = _checked_result(reference["evaluation"], reference_request)
        scenarios._require(reference["provenance"] == current["provenance"],
                           "comparison requires the same engine generation and source hashes")
        scenarios._require(reference["overview"]["dataset"] == current["overview"]["dataset"],
                           "comparison dataset mismatch")
        a, b = reference["evaluation"]["chi2"], current["evaluation"]["chi2"]
        scenarios._require(all(a[key] == b[key] for key in ("method", "n_points", "status")),
                           "comparison chi2 conventions differ")
        payload = {"reference": reference, "current": current, "delta_chi2": b["value"] - a["value"],
                   "delta_chi2_definition": "current_minus_reference",
                   "interpretation": "DESCRIPTIVE_NOT_FIT_OR_SIGNIFICANCE"}
        return _publish("comparison", payload, reference["provenance"])
    except Exception as exc:
        raise ValueError(f"Comparison export failed: {exc}") from exc


def get_export(uuid: str) -> dict:
    """Read the complete export and verify its digest; never create files."""
    try:
        path = _export_path(uuid)
        with path.open("rb") as stream:
            raw = stream.read(scenarios.MAX_RECORD_BYTES + 1)
        scenarios._require(len(raw) <= scenarios.MAX_RECORD_BYTES, "export exceeds size limit")
        record = json.loads(raw.decode("utf-8"))
        scenarios._require(isinstance(record, dict), "invalid export object")
        scenarios._require(scenarios._canonical(record).encode("utf-8") == raw, "export JSON is not canonical")
        digest = record.pop("sha256")
        expected = hashlib.sha256(scenarios._canonical(record).encode("utf-8")).hexdigest()
        scenarios._require(isinstance(digest, str) and bool(scenarios._SHA.fullmatch(digest))
                           and hmac.compare_digest(digest, expected), "export SHA-256 mismatch")
        scenarios._require(record["id"] == uuid and record["schema_version"] == SCHEMA_VERSION
                           and record["status"] == "exploratory" and record["kind"] in ("scenario", "comparison")
                           and isinstance(record["payload"], dict), "export identity/schema mismatch")
        record["sha256"] = digest
        return record
    except Exception as exc:
        raise ValueError(f"Export read failed: {exc}") from exc
