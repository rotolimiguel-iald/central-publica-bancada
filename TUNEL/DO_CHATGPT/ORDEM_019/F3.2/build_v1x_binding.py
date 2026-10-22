"""Build a new immutable documentary binding for a non-frozen Fase 9 V2 draft.

Reads only the published-source archive and the supplied draft. Never creates
ALVOS_FASE9_LIDOS.json, statistical admission, or a verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

from f9_reader_gate_v1x import BINDING_SCHEMA, ReaderGateError


ARCHIVE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
OLD_BINDING = ARCHIVE / "f9_scalar_reader_sources" / "VINCULO_DOCUMENTAL_CINCO_LEITORES.json"
MASER_DIR = ARCHIVE / "f9_maser_anchor_alternative"
PDF = MASER_DIR / "sources" / "masers_2001.09213v2.pdf"
PAGE6 = MASER_DIR / "sources" / "page_6.txt"
RECEIPT = MASER_DIR / "SOURCE_RECEIPT.json"
OLD_IDS = {
    "L1_sh0es_r22": "L1_sh0es_r22",
    "L2_cchp": "L2_cchp",
    "L3_sbf": "L3_sbf",
    "L5_tdcosmo": "L5_tdcosmo",
}
LEXICAL = {
    "L1_sh0es_r22": ("73.04", "1.04"),
    "L2_cchp": ("70.39", "1.22", "1.33", "0.70"),
    "L3_sbf": ("73.8", "0.7", "2.3"),
    "L5_tdcosmo": ("71.6", "3.9", "3.3"),
}


def _pin(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": str(path.resolve(strict=True)), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def _window(literal: str, numeral: str) -> dict:
    return {"literal": literal, "numeric_literal": numeral}


def _record(reader_id: str, metadata: dict, *, old: dict | None = None) -> dict:
    h0 = metadata["H0"]
    if old is not None:
        components = old["sigma_published_components"]
        transform = old["local_transform"]
        source_path = Path(old["source"]["path"])
        source = source_path.read_text(encoding="utf-8")
        anchor = old["short_literal_anchor"]
        position = source.find(anchor)
        if position < 0:
            raise ReaderGateError(f"old source anchor absent: {reader_id}")
        literal = source[max(0, position - 80):position + 220]
        numerals = LEXICAL[reader_id]
        if not all(numeral in literal for numeral in numerals):
            raise ReaderGateError(f"numeric window incomplete: {reader_id}")
        record = {
            "reader_id": reader_id,
            "draft_metadata": metadata,
            "documentary_status": "REAL_DOCUMENTARY_HASH_ONLY",
            "source": _pin(source_path),
            "H0_published": h0,
            "sigma_published_components": components,
            "local_transform": transform,
            "numeric_windows": {
                "H0": _window(literal, numerals[0]),
                "sigma_components": [_window(literal, numeral) for numeral in numerals[1:]],
            },
        }
        if transform == "arithmetic_mean":
            record["asymmetric_sigma"] = {"plus": components[0], "minus": components[1]}
        return record
    if reader_id in ("L1b_sh0es_r25", "L6_sirenes"):
        return {
            "reader_id": reader_id,
            "draft_metadata": metadata,
            "documentary_status": "DECLARADO_UNVERIFIED",
            "H0_published": h0,
            "sigma_published_components": [metadata["sigma"]],
            "local_transform": "identity",
            "source_status_reason": "Published-source bytes not pinned in this binding; D-H pending",
        }
    if reader_id in ("L4_masers_5", "L4_masers_6"):
        if reader_id.endswith("_5"):
            literal = "NGC 4258\n73.6+3.1\n−3.0"
            numerals = ("73.6", "3.1", "3.0")
            components = [3.1, 3.0]
        else:
            literal = "Fit using all galaxies:\n73.9+3.0\n−3.0"
            numerals = ("73.9", "3.0", "3.0")
            components = [3.0, 3.0]
        if literal.encode("utf-8") not in PAGE6.read_bytes():
            raise ReaderGateError(f"Table 2 literal absent: {reader_id}")
        return {
            "reader_id": reader_id,
            "draft_metadata": metadata,
            "documentary_status": "REAL_DOCUMENTARY_HASH_ONLY",
            "source": _pin(PDF),
            "text_projection": _pin(PAGE6),
            "projection_receipt": _pin(RECEIPT),
            "published_table": "Pesce et al. 2020 Table 2 page 6; treatment (1)",
            "H0_published": h0,
            "sigma_published_components": components,
            "local_transform": "arithmetic_mean",
            "asymmetric_sigma": {"plus": components[0], "minus": components[1]},
            "numeric_windows": {
                "H0": _window(literal, numerals[0]),
                "sigma_components": [_window(literal, numeral) for numeral in numerals[1:]],
            },
        }
    raise ReaderGateError(f"unmapped draft reader: {reader_id}")


def build(draft_path: Path, output: Path) -> dict:
    if output.exists():
        raise ReaderGateError(f"refuse evidence overwrite: {output}")
    draft_raw = draft_path.read_bytes()
    draft = json.loads(draft_raw.decode("utf-8"))
    if draft.get("state") != "RASCUNHO_NAO_CONGELADO":
        raise ReaderGateError("draft must remain non-frozen")
    spec = draft["spec"]
    old = json.loads(OLD_BINDING.read_bytes().decode("utf-8"))
    old_records = {record["reader_id"]: record for record in old["readers"]}
    records = []
    for reader_id, metadata in spec["leitores"].items():
        old_record = old_records[OLD_IDS[reader_id]] if reader_id in OLD_IDS else None
        records.append(_record(reader_id, metadata, old=old_record))
    binding = {
        "schema": BINDING_SCHEMA,
        "scope": "Documentary V2 draft binding only; no D-H admission, covariance or real-data opening",
        "draft_v2": _pin(draft_path),
        "spec_sha256": draft["spec_sha256"],
        "readers": records,
        "statistical_admission_decided": False,
        "source_admission_decided": False,
        "alvos_fase9_lidos_created": False,
        "maser_5_decisory_6_diagnostic_never_summed": True,
        "findings_reference": "achados D1 a D6 da seq 696",
    }
    raw = (json.dumps(binding, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, prefix=".v1x-binding-", suffix=".tmp", delete=False) as temp:
        temp.write(raw)
        temp.flush()
        os.fsync(temp.fileno())
        staged = Path(temp.name)
    try:
        if staged.stat().st_size != len(raw) or output.exists():
            raise ReaderGateError("binding staging failed or destination appeared")
        os.replace(staged, output)
    finally:
        staged.unlink(missing_ok=True)
    return _pin(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft-v2", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.draft_v2, args.output), sort_keys=True))
