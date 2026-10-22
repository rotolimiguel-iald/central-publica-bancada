"""Candidate V1.x documentary gate; never grants statistical admission.

This deliberately reuses the byte reader, pin checker, and sigma transform from
the audited F3.2 gate. It does not call official_archive_check(), whose pin and
metadata belong to the historical V1. No real V1.x binding is installed here.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
import math
from pathlib import Path
import re

import f9_reader_gate as base


ReaderGateError = base.ReaderGateError
BINDING_SCHEMA = "F9_SCALAR_V1X_DOCUMENTARY_BINDING_CANDIDATE"
FROZEN_SCHEMA = "F9_SCALAR_V1X_CANDIDATE"
EXPECTED_READER_IDS = base.EXPECTED_READER_IDS
HISTORICAL_V1_SHA256 = "1893261e730994b3508d14dd2105f8aae3a764d3d217e28bd5939cb58f865273"
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def _object(value: object, name: str) -> dict:
    if not isinstance(value, dict):
        raise ReaderGateError(f"{name} must be an object")
    return value


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ReaderGateError(f"{name} must be nonempty text")
    return value


def _number(value: object, name: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ReaderGateError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0):
        raise ReaderGateError(f"{name} must be finite and valid")
    return result


def _pin(value: object, name: str) -> dict:
    pin = _object(value, name)
    _text(pin.get("path"), f"{name}.path")
    if isinstance(pin.get("bytes"), bool) or not isinstance(pin.get("bytes"), int) or pin["bytes"] <= 0:
        raise ReaderGateError(f"{name}.bytes must be positive integer")
    digest = _text(pin.get("sha256"), f"{name}.sha256")
    if not _SHA256.fullmatch(digest):
        raise ReaderGateError(f"{name}.sha256 malformed")
    return pin


def _window(value: object, expected: float, source: bytes, name: str) -> None:
    """Pin a verbatim source window containing the actual declared number."""
    window = _object(value, name)
    literal = _text(window.get("literal"), f"{name}.literal")
    numeral = _text(window.get("numeric_literal"), f"{name}.numeric_literal")
    if len(literal) > 4096 or len(numeral) > 64:
        raise ReaderGateError(f"{name} too long")
    try:
        lexical = Decimal(numeral.replace(",", "."))
    except InvalidOperation as exc:
        raise ReaderGateError(f"{name} has invalid numeric literal") from exc
    if not lexical.is_finite() or lexical != Decimal(str(expected)):
        raise ReaderGateError(f"{name} numeric literal differs from transcription")
    # Reject a generic anchor or a number embedded in another number.
    pattern = rf"(?<![0-9.,]){re.escape(numeral)}(?![0-9.,])"
    if re.search(pattern, literal) is None:
        raise ReaderGateError(f"{name} does not contain its numeric literal")
    if literal.encode("utf-8") not in source:
        raise ReaderGateError(f"{name} is absent from pinned source bytes")


def verify_v1x_binding(
    binding_path: Path,
    *,
    expected_binding_sha256: str,
    allowed_source_root: Path,
) -> dict:
    """Verify a separately pinned V1.x binding and all numeric source windows.

    This returns documentary status only. The source values are published
    summaries, not a reconstructed likelihood or an admitted covariance.
    """
    if not _SHA256.fullmatch(expected_binding_sha256):
        raise ReaderGateError("binding pin malformed")
    binding_path = base._resolve_existing(binding_path)
    binding, raw = base._read_json(binding_path)
    if base._digest(raw) != expected_binding_sha256:
        raise ReaderGateError("binding hash mismatch")
    if binding.get("schema") != BINDING_SCHEMA:
        raise ReaderGateError("unexpected V1.x binding schema")
    if binding.get("statistical_admission_decided") is not False:
        raise ReaderGateError("binding claims statistical admission")

    frozen_pin = _pin(binding.get("frozen_v1x"), "frozen_v1x")
    if frozen_pin["sha256"] == HISTORICAL_V1_SHA256:
        raise ReaderGateError("historical V1 cannot serve as V1.x")
    frozen_path = base._resolve_existing(Path(frozen_pin["path"]))
    frozen, frozen_raw = base._read_json(frozen_path)
    if len(frozen_raw) != frozen_pin["bytes"] or base._digest(frozen_raw) != frozen_pin["sha256"]:
        raise ReaderGateError("V1.x bytes/hash mismatch")
    if frozen.get("schema") != FROZEN_SCHEMA:
        raise ReaderGateError("frozen V1.x schema mismatch")
    try:
        frozen_readers = _object(frozen["spec"]["leitores"], "frozen readers")
    except (KeyError, TypeError) as exc:
        raise ReaderGateError("frozen V1.x reader schema incomplete") from exc
    if set(frozen_readers) != EXPECTED_READER_IDS:
        raise ReaderGateError("frozen V1.x reader ids differ")

    records = binding.get("readers")
    if not isinstance(records, list) or len(records) != len(EXPECTED_READER_IDS):
        raise ReaderGateError("binding reader list incomplete")
    ids = [_text(_object(r, "reader").get("reader_id"), "reader_id") for r in records]
    if len(set(ids)) != len(ids) or set(ids) != EXPECTED_READER_IDS:
        raise ReaderGateError("reader ids incomplete, duplicated or unexpected")

    root = base._resolve_existing(allowed_source_root)
    verified = {}
    for record in records:
        reader_id = record["reader_id"]
        source_pin = _pin(record.get("source"), f"{reader_id}.source")
        source_path = base._resolve_existing(Path(source_pin["path"]))
        if not source_path.is_relative_to(root):
            raise ReaderGateError(f"source outside archive: {reader_id}")
        source = base._pinned_bytes(source_path, source_pin)
        expected = _object(frozen_readers[reader_id], f"{reader_id}.frozen_metadata")
        if record.get("frozen_metadata") != expected:
            raise ReaderGateError(f"frozen metadata changed: {reader_id}")
        h0 = _number(record.get("H0_published"), f"{reader_id}.H0")
        components = record.get("sigma_published_components")
        if not isinstance(components, list) or not components:
            raise ReaderGateError(f"sigma components missing: {reader_id}")
        parts = [_number(x, f"{reader_id}.sigma_component", positive=True) for x in components]
        transform = _text(record.get("local_transform"), f"{reader_id}.local_transform")
        try:
            sigma = base._reconstruct_sigma(record)
        except (KeyError, TypeError, ValueError) as exc:
            raise ReaderGateError(f"invalid sigma transform: {reader_id}") from exc
        if not math.isclose(h0, _number(expected.get("H0"), f"{reader_id}.frozen_H0"), abs_tol=1e-12, rel_tol=0):
            raise ReaderGateError(f"H0 transcription mismatch: {reader_id}")
        if not math.isclose(sigma, _number(expected.get("sigma"), f"{reader_id}.frozen_sigma", positive=True), abs_tol=1e-12, rel_tol=0):
            raise ReaderGateError(f"sigma transcription mismatch: {reader_id}")
        windows = _object(record.get("numeric_windows"), f"{reader_id}.numeric_windows")
        _window(windows.get("H0"), h0, source, f"{reader_id}.H0_window")
        sigma_windows = windows.get("sigma_components")
        if not isinstance(sigma_windows, list) or len(sigma_windows) != len(parts):
            raise ReaderGateError(f"sigma source windows incomplete: {reader_id}")
        for index, (window, part) in enumerate(zip(sigma_windows, parts)):
            _window(window, part, source, f"{reader_id}.sigma_window_{index}")
        asymmetric = record.get("asymmetric_sigma")
        if transform == "arithmetic_mean":
            asymmetric = _object(asymmetric, f"{reader_id}.asymmetric_sigma")
            if len(parts) != 2 or asymmetric.get("plus") != parts[0] or asymmetric.get("minus") != parts[1]:
                raise ReaderGateError(f"asymmetric sigma sides changed: {reader_id}")
        elif asymmetric is not None:
            raise ReaderGateError(f"unexpected asymmetric sigma: {reader_id}")
        verified[reader_id] = {
            "source_sha256": base._digest(source),
            "source_bytes": len(source),
            "sigma_compression": transform,
            "asymmetric_sigma": asymmetric,
            "status": "REAL_DOCUMENTARY_HASH_ONLY",
            "statistical_admission": "OPEN",
        }
    return {
        "binding_sha256": base._digest(raw),
        "frozen_v1x_sha256": base._digest(frozen_raw),
        "verified_readers": verified,
        "statistical_admission": "OPEN",
        "cross_covariance": "OPEN",
        "v2_frozen": False,
    }
