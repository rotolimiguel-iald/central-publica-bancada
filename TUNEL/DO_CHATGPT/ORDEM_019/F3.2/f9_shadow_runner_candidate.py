"""Fase 9 V1.x/V2 interface candidate: synthetic shadow preflight only.

No real-data entry point, output file, likelihood, verdict, or admission token is
implemented. A future frozen runner must use a separately pinned V1.x binding.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import f9_reader_gate as legacy_gate
from f9_reader_gate_v1x_candidate import ReaderGateError, verify_v1x_binding


SHADOW_SCHEMA = "F9_SHADOW_SYNTHETIC_CASE_CANDIDATE"
MU_DO_RITO = "q→0 (Thomson; Teorema da Escala)"
DECLARED_EXECUTOR_SEMANTICS = {
    "background": "marginalized",
    "z_delta": "profile_minus2logL_with_logdet",
    "lnB_quadrature_n_min": 100,
    "z_disc": "quadratic_form",
    "sigma_beta": "mean_of_asymmetric_sides",
}


def _inside(path: Path, root: Path, label: str) -> Path:
    resolved = legacy_gate._resolve_existing(path)
    if not resolved.is_relative_to(root):
        raise ReaderGateError(f"{label} outside synthetic fixture root")
    return resolved


def _finite_positive(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ReaderGateError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result) or result <= 0:
        raise ReaderGateError(f"{label} must be finite and positive")
    return result


def _assert_synthetic_binding(binding_path: Path, fixture_root: Path) -> None:
    binding, _ = legacy_gate._read_json(binding_path)
    if binding.get("synthetic_fixture") is not True:
        raise ReaderGateError("real documentary binding is not a synthetic fixture")
    pin = binding.get("frozen_v1x")
    if not isinstance(pin, dict) or not isinstance(pin.get("path"), str):
        raise ReaderGateError("synthetic frozen V1.x pin missing")
    frozen_path = _inside(Path(pin["path"]), fixture_root, "frozen V1.x")
    frozen, _ = legacy_gate._read_json(frozen_path)
    if frozen.get("synthetic_fixture") is not True:
        raise ReaderGateError("frozen V1.x is not synthetic")
    for record in binding.get("readers", []):
        if not isinstance(record, dict) or not isinstance(record.get("source"), dict):
            raise ReaderGateError("synthetic reader source pin malformed")
        source_path = record["source"].get("path")
        if not isinstance(source_path, str):
            raise ReaderGateError("synthetic reader source path missing")
        _inside(Path(source_path), fixture_root, "reader source")


def run_synthetic_shadow(
    case_path: Path,
    *,
    expected_case_sha256: str,
    fixture_root: Path,
) -> dict:
    """Read only pinned synthetic bytes and report two power endpoints.

    This is a protocol smoke test, not a Fase 9 result. Values supplied in the
    fixture are synthetic and are never mixed with the published centers.
    """
    root = legacy_gate._resolve_existing(fixture_root)
    case_path = _inside(case_path, root, "shadow case")
    case, raw = legacy_gate._read_json(case_path)
    if legacy_gate._digest(raw) != expected_case_sha256:
        raise ReaderGateError("shadow case hash mismatch")
    if case.get("schema") != SHADOW_SCHEMA or case.get("mode") != "SYNTHETIC_SHADOW_ONLY":
        raise ReaderGateError("real or unknown runner mode refused")
    if case.get("synthetic_fixture") is not True:
        raise ReaderGateError("case is not marked synthetic")
    if case.get("mu_do_rito") != MU_DO_RITO:
        raise ReaderGateError("mu_do_rito missing or different")
    if case.get("declared_executor_semantics") != DECLARED_EXECUTOR_SEMANTICS:
        raise ReaderGateError("executor semantics declaration missing or different")
    pin = case.get("binding")
    if not isinstance(pin, dict) or not isinstance(pin.get("path"), str):
        raise ReaderGateError("shadow binding pin missing")
    binding_path = _inside(Path(pin["path"]), root, "shadow binding")
    if not isinstance(pin.get("sha256"), str):
        raise ReaderGateError("shadow binding hash missing")
    _assert_synthetic_binding(binding_path, root)
    documentary = verify_v1x_binding(
        binding_path,
        expected_binding_sha256=pin["sha256"],
        allowed_source_root=root,
    )
    if len(documentary["verified_readers"]) != 5:
        raise ReaderGateError("five documentary readers required")

    power = case.get("synthetic_power")
    if not isinstance(power, dict):
        raise ReaderGateError("synthetic power inputs missing")
    k = _finite_positive(power.get("K"), "K")
    hbg = _finite_positive(power.get("H0_background"), "H0_background")
    sigma_bg = _finite_positive(power.get("sigma_background"), "sigma_background")
    sigma_min = _finite_positive(power.get("sigma_comb_min"), "sigma_comb_min")
    sigma_max = _finite_positive(power.get("sigma_comb_max"), "sigma_comb_max")
    if sigma_min > sigma_max:
        raise ReaderGateError("synthetic covariance endpoints reversed")
    numerator = abs(k - 1) * hbg

    def power_at(sigma_comb: float) -> float:
        return numerator / math.hypot(sigma_comb, k * sigma_bg)

    return {
        "mode": "SYNTHETIC_SHADOW_ONLY",
        "case_sha256": legacy_gate._digest(raw),
        "documentary_binding_sha256": documentary["binding_sha256"],
        "verified_reader_count": len(documentary["verified_readers"]),
        "power_at_min_sigma": power_at(sigma_min),
        "power_at_max_sigma": power_at(sigma_max),
        "statistical_admission": "OPEN",
        "verdict": "NONE_SYNTHETIC_PREFLIGHT",
        "executor_semantics_executed": False,
        "gate_changed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--synthetic-case", required=True, type=Path)
    parser.add_argument("--case-sha256", required=True)
    parser.add_argument("--fixture-root", required=True, type=Path)
    args = parser.parse_args()
    result = run_synthetic_shadow(
        args.synthetic_case,
        expected_case_sha256=args.case_sha256,
        fixture_root=args.fixture_root,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
