"""Fase 9 V1.x runner preflight: documentary gate before any opening.

This stage deliberately has no observational data input or verdict path. The
future statistical stage requires a frozen V2, source admission and X13.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from f9_reader_gate_v1x_r52 import ReaderGateError, verify_v1x_binding


MU_DO_RITO = "q→0 (Thomson; Teorema da Escala)"
PRIMARY_IDS = (
    "L1_sh0es_r22",
    "L2_cchp",
    "L3_sbf",
    "L4_masers_5",
    "L5_tdcosmo",
)
ALL_IDS = frozenset(PRIMARY_IDS) | {
    "L1b_sh0es_r25", "L4_masers_6", "L6_sirenes"
}


def _object(value: object, label: str) -> dict:
    if not isinstance(value, dict):
        raise ReaderGateError(f"{label} must be an object")
    return value


def _ids(families: dict, name: str) -> list[str]:
    family = _object(families.get(name), f"family {name}")
    ids = family.get("ids")
    if not isinstance(ids, list) or not all(isinstance(x, str) for x in ids):
        raise ReaderGateError(f"family {name} ids malformed")
    if len(ids) != len(set(ids)):
        raise ReaderGateError(f"family {name} has duplicate ids")
    return ids


def declared_inventory_ids(verified: dict, admitted_ids: set[str] | None = None) -> list[str]:
    """Count the entire V1.x inventory under gate-failure AND no pinned admission."""
    if set(verified) != ALL_IDS:
        raise ReaderGateError("documentary gate inventory differs")
    admitted = set() if admitted_ids is None else set(admitted_ids)
    if not admitted.issubset(ALL_IDS):
        raise ReaderGateError("operator admission outside V1.x inventory")
    if admitted:
        raise ReaderGateError("R4 has no pinned D-H admission parser; future admission requires a new version")
    return sorted(
        reader_id for reader_id in ALL_IDS
        if _object(verified[reader_id], f"reader {reader_id}").get("status")
        != "REAL_DOCUMENTARY_HASH_ONLY" and reader_id not in admitted
    )


def prepare_v1x(
    binding_path: Path,
    *,
    expected_binding_sha256: str,
    allowed_source_root: Path,
    expected_spec_sha256: str | None = None,
) -> dict:
    """Verify pinned source bytes once and return a non-admitting preflight.

    The gate returns the spec snapshot from the same read whose bytes it pins;
    the runner never reopens the draft, avoiding the historical TOCTOU.
    """
    gate = verify_v1x_binding(
        binding_path,
        expected_binding_sha256=expected_binding_sha256,
        allowed_source_root=allowed_source_root,
        expected_spec_sha256=expected_spec_sha256,
    )
    if gate.get("v2_frozen") is not False or gate.get("source_admission") != "OPEN":
        raise ReaderGateError("draft gate claimed freeze or admission")
    spec = _object(gate.get("spec_snapshot"), "spec snapshot")
    readers = _object(spec.get("leitores"), "spec readers")
    if set(readers) != ALL_IDS:
        raise ReaderGateError("V1.x reader inventory differs")
    verified = _object(gate.get("verified_readers"), "verified readers")
    if set(verified) != ALL_IDS:
        raise ReaderGateError("documentary gate inventory differs")
    verified_ids = sorted(
        reader_id for reader_id, record in verified.items()
        if _object(record, f"reader {reader_id}").get("status") == "REAL_DOCUMENTARY_HASH_ONLY"
    )
    declared_ids = declared_inventory_ids(verified, admitted_ids=set())
    if not set(PRIMARY_IDS).issubset(verified_ids):
        raise ReaderGateError("decision reader lacks documentary verification")
    if spec.get("mu_do_rito") != MU_DO_RITO:
        raise ReaderGateError("mu_do_rito missing or different")
    families = _object(spec.get("familias"), "spec families")
    primary = _ids(families, "P_primaria")
    if primary != list(PRIMARY_IDS):
        raise ReaderGateError("primary must contain five masers and exclude the six")
    r25 = _ids(families, "R_r25")
    if "L1b_sh0es_r25" not in r25 or "L1_sh0es_r22" in r25:
        raise ReaderGateError("R_r25 does not replace L1 by L1b")
    sirens = _ids(families, "S_com_sirenes")
    if "L6_sirenes" not in sirens:
        raise ReaderGateError("S_com_sirenes omits L6")
    if "L4_masers_6" in primary:
        raise ReaderGateError("six masers cannot enter the decision family")

    # No D-H admission record exists. The declared count is the conjunction
    # of documentary failure and absent operator admission, not all readers.
    return {
        "stage": "V1X_DOCUMENTARY_PREFLIGHT_ONLY",
        "binding_sha256": gate["binding_sha256"],
        "spec_sha256": gate["spec_sha256"],
        "verified_reader_ids": verified_ids,
        "declared_unverified_reader_ids": declared_ids,
        "primary_reader_ids": primary,
        "n_alvos_declarados": len(declared_ids),
        "n_alvos_scope": "entire_V1x_inventory; gate_unverified AND no_pinned_operator_admission",
        "admitted_reader_ids": [],
        "operator_admission": "PENDING_D_H",
        "spec_governance": "F3_4_RESOLVED_TWO_WITNESSES",
        "executor_semantics": "PENDING_X13",
        "v2_frozen": False,
        "data_opened": False,
        "source_admission": "OPEN",
        "verdict": None,
        "gate_changed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binding", required=True, type=Path)
    parser.add_argument("--binding-sha256", required=True)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--spec-sha256", default=None)
    args = parser.parse_args()
    result = prepare_v1x(
        args.binding,
        expected_binding_sha256=args.binding_sha256,
        allowed_source_root=args.source_root,
        expected_spec_sha256=args.spec_sha256,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
