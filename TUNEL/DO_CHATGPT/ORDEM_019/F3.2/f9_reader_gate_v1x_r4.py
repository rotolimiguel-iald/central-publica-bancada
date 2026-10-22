"""R4 fail-closed documentary gate for the Fase 9 V2 draft and V1.x readers.

It reuses the audited byte reader and does not call official_archive_check(),
whose pin and metadata belong to historical V1. No admission or verdict.
"""

from __future__ import annotations

import copy
from decimal import Decimal, InvalidOperation
import hashlib
import json
import math
from pathlib import Path
import re

import f9_reader_gate as base


ReaderGateError = base.ReaderGateError
BINDING_SCHEMA = "F9_SCALAR_V1X_DOCUMENTARY_BINDING_V2_DRAFT"
EXPECTED_READER_IDS = frozenset({
    "L1_sh0es_r22", "L1b_sh0es_r25", "L2_cchp", "L3_sbf",
    "L4_masers_5", "L4_masers_6", "L5_tdcosmo", "L6_sirenes",
})
PRIMARY_READER_IDS = frozenset({
    "L1_sh0es_r22", "L2_cchp", "L3_sbf", "L4_masers_5", "L5_tdcosmo",
})
DECLARED_ONLY_IDS = frozenset({"L1b_sh0es_r25", "L6_sirenes"})
MASER_READER_IDS = frozenset({"L4_masers_5", "L4_masers_6"})
PESCE_PDF_SHA256 = "c9f2d2b626fee60d77928856d217a2cbe546f06c69cd9e7ac804f4ab652e731a"
PESCE_PAGE6_SHA256 = "e5a8eef8c099fa01b9d2d761567e7b22a5a66c8332f10b5c16dde24a4cf79d7a"
MASER_TABLE_LITERALS = {
    "L4_masers_5": "NGC 4258\n73.6+3.1\n−3.0",
    "L4_masers_6": "Fit using all galaxies:\n73.9+3.0\n−3.0",
}
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
    # A bare numeral is ambiguous in the CCHP source (1.33 occurs three
    # times). The quote must carry a recognisable source label as context.
    if len(literal) < 16 or re.search(r"[A-Za-z]{3,}", literal) is None:
        raise ReaderGateError(f"{name} lacks minimum source context")
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
    occurrences = source.count(literal.encode("utf-8"))
    if occurrences == 0:
        raise ReaderGateError(f"{name} is absent from pinned source bytes")
    if occurrences != 1:
        raise ReaderGateError(f"{name} is ambiguous in pinned source bytes: {occurrences} occurrences")


def _signed_source_sides(windows: dict, h0: float, plus: float, minus: float,
                         reader_id: str) -> None:
    """Bind both uncertainty sides to the signs next to H0 in source text.

    Matching two unsigned numerals separately accepts a coherent exchange of
    plus and minus in the binding. This check consumes the pinned H0 window,
    which is also required to occur verbatim in pinned source bytes.
    """
    row = _object(windows.get("H0"), f"{reader_id}.H0_window")
    literal = _text(row.get("literal"), f"{reader_id}.H0_window.literal")
    center = re.escape(str(h0))
    upper = re.escape(str(plus))
    lower = re.escape(str(minus))
    signed_row = (
        rf"(?<![0-9.,]){center}(?![0-9.,])[^0-9]{{0,12}}"
        rf"\+{upper}(?![0-9.,])[^0-9]{{0,12}}[-−]{lower}(?![0-9.,])"
    )
    if re.search(signed_row, literal) is None:
        raise ReaderGateError(f"source signs do not bind asymmetric sides: {reader_id}")


def _pinned_file(value: object, name: str, root: Path | None = None) -> tuple[dict, Path, bytes]:
    pin = _pin(value, name)
    path = base._resolve_existing(Path(pin["path"]))
    if root is not None and not path.is_relative_to(root):
        raise ReaderGateError(f"{name} outside archive")
    raw = base._pinned_bytes(path, pin)
    return pin, path, raw


def _source_text(record: dict, reader_id: str, root: Path) -> tuple[bytes, bytes]:
    source_pin, source_path, source = _pinned_file(record.get("source"), f"{reader_id}.source", root)
    if reader_id not in MASER_READER_IDS:
        if record.get("text_projection") is not None or record.get("projection_receipt") is not None:
            raise ReaderGateError(f"unexpected projection: {reader_id}")
        return source, source
    if source_path.suffix.lower() != ".pdf":
        raise ReaderGateError(f"maser source must be pinned PDF: {reader_id}")
    if source_pin["sha256"] != PESCE_PDF_SHA256:
        raise ReaderGateError(f"maser PDF pin differs from Pesce archive: {reader_id}")
    projection_pin, _, projection = _pinned_file(
        record.get("text_projection"), f"{reader_id}.text_projection", root
    )
    if projection_pin["sha256"] != PESCE_PAGE6_SHA256:
        raise ReaderGateError(f"maser Table 2 projection pin differs: {reader_id}")
    _, _, receipt_raw = _pinned_file(
        record.get("projection_receipt"), f"{reader_id}.projection_receipt", root
    )
    try:
        receipt = json.loads(receipt_raw.decode("utf-8"), object_pairs_hook=base._unique_object)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ReaderGateError("PDF extraction receipt unreadable") from exc
    receipt = _object(receipt, "PDF extraction receipt")
    if receipt.get("sha256") != source_pin["sha256"] or receipt.get("bytes") != source_pin["bytes"]:
        raise ReaderGateError("PDF extraction receipt does not bind source")
    pages = receipt.get("extracted_pages")
    if not isinstance(pages, list) or not any(
        isinstance(page, dict)
        and page.get("page") == 6
        and page.get("sha256") == projection_pin["sha256"]
        and page.get("bytes") == projection_pin["bytes"]
        for page in pages
    ):
        raise ReaderGateError("PDF extraction receipt does not bind page 6")
    return source, projection


def verify_v1x_binding(
    binding_path: Path,
    *,
    expected_binding_sha256: str,
    allowed_source_root: Path,
    expected_spec_sha256: str | None = None,
) -> dict:
    """Verify new V1.x documentary binding; return its single-read V2 spec snapshot.

    Source byte verification is not operator admission, likelihood reconstruction,
    independence, a real-data opening, or a frozen preregistration.
    """
    if not isinstance(expected_binding_sha256, str) or not _SHA256.fullmatch(expected_binding_sha256):
        raise ReaderGateError("binding pin malformed")
    binding_path = base._resolve_existing(binding_path)
    binding, binding_raw = base._read_json(binding_path)
    if base._digest(binding_raw) != expected_binding_sha256:
        raise ReaderGateError("binding hash mismatch")
    if binding.get("schema") != BINDING_SCHEMA:
        raise ReaderGateError("unexpected V1.x binding schema")
    if binding.get("statistical_admission_decided") is not False or binding.get("source_admission_decided") is not False:
        raise ReaderGateError("binding claims admission")

    draft_pin = _pin(binding.get("draft_v2"), "draft_v2")
    if draft_pin["sha256"] == HISTORICAL_V1_SHA256:
        raise ReaderGateError("historical V1 cannot serve as V1.x")
    draft_path = base._resolve_existing(Path(draft_pin["path"]))
    # Read the draft exactly once: the same bytes yield the pin, spec, and return snapshot.
    draft, draft_raw = base._read_json(draft_path)
    if len(draft_raw) != draft_pin["bytes"] or base._digest(draft_raw) != draft_pin["sha256"]:
        raise ReaderGateError("V2 draft bytes/hash mismatch")
    if draft.get("state") != "RASCUNHO_NAO_CONGELADO":
        raise ReaderGateError("V2 draft state is not the expected non-frozen state")
    spec = _object(draft.get("spec"), "draft spec")
    spec_raw = json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    spec_sha256 = hashlib.sha256(spec_raw).hexdigest()
    if draft.get("spec_sha256") != spec_sha256 or binding.get("spec_sha256") != spec_sha256:
        raise ReaderGateError("V2 spec hash mismatch")
    if expected_spec_sha256 is not None and expected_spec_sha256 != spec_sha256:
        raise ReaderGateError("independent V2 spec pin mismatch")
    readers = _object(spec.get("leitores"), "draft readers")
    if set(readers) != EXPECTED_READER_IDS:
        raise ReaderGateError("V2 reader ids differ")
    families = _object(spec.get("familias"), "draft families")
    primary = _object(families.get("P_primaria"), "primary family")
    primary_ids = primary.get("ids")
    if not isinstance(primary_ids, list) or not all(isinstance(item, str) for item in primary_ids):
        raise ReaderGateError("V2 primary family ids malformed")
    if set(primary_ids) != PRIMARY_READER_IDS or len(primary_ids) != 5:
        raise ReaderGateError("V2 primary family must use five distinct readers")

    records = binding.get("readers")
    if not isinstance(records, list) or len(records) != len(EXPECTED_READER_IDS):
        raise ReaderGateError("binding reader list incomplete")
    ids = [_text(_object(record, "reader").get("reader_id"), "reader_id") for record in records]
    if len(set(ids)) != len(ids) or set(ids) != EXPECTED_READER_IDS:
        raise ReaderGateError("reader ids incomplete, duplicated or unexpected")

    root = base._resolve_existing(allowed_source_root)
    verified = {}
    for record in records:
        reader_id = record["reader_id"]
        expected = _object(readers[reader_id], f"{reader_id}.draft_metadata")
        if record.get("draft_metadata") != expected:
            raise ReaderGateError(f"draft metadata changed: {reader_id}")
        h0 = _number(record.get("H0_published"), f"{reader_id}.H0")
        components = record.get("sigma_published_components")
        if not isinstance(components, list) or not components:
            raise ReaderGateError(f"sigma components missing: {reader_id}")
        parts = [_number(x, f"{reader_id}.sigma_component", positive=True) for x in components]
        transform = _text(record.get("local_transform"), f"{reader_id}.local_transform")
        try:
            sigma = base._reconstruct_sigma(record)
        except (KeyError, TypeError, ValueError, OverflowError) as exc:
            raise ReaderGateError(f"invalid sigma transform: {reader_id}") from exc
        if not math.isclose(h0, _number(expected.get("H0"), f"{reader_id}.draft_H0"), abs_tol=1e-12, rel_tol=0):
            raise ReaderGateError(f"H0 transcription mismatch: {reader_id}")
        if not math.isclose(sigma, _number(expected.get("sigma"), f"{reader_id}.draft_sigma", positive=True), abs_tol=1e-12, rel_tol=0):
            raise ReaderGateError(f"sigma transcription mismatch: {reader_id}")
        asymmetric = record.get("asymmetric_sigma")
        if transform == "arithmetic_mean":
            asymmetric = _object(asymmetric, f"{reader_id}.asymmetric_sigma")
            if len(parts) != 2 or asymmetric.get("plus") != parts[0] or asymmetric.get("minus") != parts[1]:
                raise ReaderGateError(f"asymmetric sigma sides changed: {reader_id}")
            if ("sigma_plus" in expected or "sigma_minus" in expected) and (expected.get("sigma_plus") != parts[0] or expected.get("sigma_minus") != parts[1]):
                raise ReaderGateError(f"asymmetric sides disagree with draft metadata: {reader_id}")
        elif asymmetric is not None:
            raise ReaderGateError(f"unexpected asymmetric sigma: {reader_id}")

        status = record.get("documentary_status")
        if status == "DECLARADO_UNVERIFIED" and reader_id in DECLARED_ONLY_IDS:
            if record.get("source") is not None or record.get("numeric_windows") is not None:
                raise ReaderGateError(f"unverified reader claims source evidence: {reader_id}")
            verified[reader_id] = {
                "status": status, "source_sha256": None,
                "sigma_compression": transform, "asymmetric_sigma": asymmetric,
                "statistical_admission": "OPEN",
            }
            continue
        if status != "REAL_DOCUMENTARY_HASH_ONLY":
            raise ReaderGateError(f"reader documentary status invalid: {reader_id}")
        source, source_text = _source_text(record, reader_id, root)
        windows = _object(record.get("numeric_windows"), f"{reader_id}.numeric_windows")
        if reader_id in MASER_READER_IDS:
            table_literal = MASER_TABLE_LITERALS[reader_id]
            h0_window = _object(windows.get("H0"), f"{reader_id}.H0_window")
            if h0_window.get("literal") != table_literal:
                raise ReaderGateError(f"maser Table 2 row missing: {reader_id}")
        _window(windows.get("H0"), h0, source_text, f"{reader_id}.H0_window")
        if transform == "arithmetic_mean":
            _signed_source_sides(windows, h0, parts[0], parts[1], reader_id)
        sigma_windows = windows.get("sigma_components")
        if not isinstance(sigma_windows, list) or len(sigma_windows) != len(parts):
            raise ReaderGateError(f"sigma source windows incomplete: {reader_id}")
        for index, (window, part) in enumerate(zip(sigma_windows, parts)):
            if reader_id in MASER_READER_IDS and _object(window, f"{reader_id}.sigma_window_{index}").get("literal") != MASER_TABLE_LITERALS[reader_id]:
                raise ReaderGateError(f"maser Table 2 sigma row missing: {reader_id}")
            _window(window, part, source_text, f"{reader_id}.sigma_window_{index}")
            if reader_id == "L2_cchp" and index == 1:
                context = _object(window, f"{reader_id}.sigma_window_{index}")["literal"]
                if not all(token in context for token in ("TRGB", "H_0", "(sys)")):
                    raise ReaderGateError("CCHP 1.33 source window lacks sys/TRGB context")
        verified[reader_id] = {
            "status": status, "source_sha256": base._digest(source),
            "sigma_compression": transform, "asymmetric_sigma": asymmetric,
            "statistical_admission": "OPEN",
        }
    if any(verified[reader_id]["status"] != "REAL_DOCUMENTARY_HASH_ONLY" for reader_id in PRIMARY_READER_IDS):
        raise ReaderGateError("a primary reader lacks documentary hash verification")
    return {
        "binding_sha256": base._digest(binding_raw),
        "draft_v2_sha256": base._digest(draft_raw),
        "spec_sha256": spec_sha256,
        "spec_snapshot": copy.deepcopy(spec),
        "verified_readers": verified,
        "statistical_admission": "OPEN",
        "source_admission": "OPEN",
        "cross_covariance": "OPEN",
        "v2_frozen": False,
    }


verify_readers = verify_v1x_binding
