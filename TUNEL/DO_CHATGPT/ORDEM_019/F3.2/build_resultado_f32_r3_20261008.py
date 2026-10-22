"""Create one immutable R3 receipt from pinned documentary/synthetic checks."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

import f9_reader_gate_v1x_r3 as gate
import f9_runner_v1x_preflight_r3 as pre
import f9_runner_v1x_staged_r3 as staged


HERE = Path(__file__).resolve().parent
F31_JSON = HERE.parent / "F3.1" / "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R3.json"
BINDING = HERE / "VINCULO_DOCUMENTAL_V1X_R3_20261008.json"
FIXTURE = HERE / "FIXTURE_SINTETICO_V1X_R3_20261008.json"
SOURCE_ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")
SPEC_SHA = "21a624f5c6e716b3b9a1b9301747b94ae74b82bed2502654885a0709ec9d0dcb"
F31_SHA = "34ee2e2004e72a83cb52dd40b38dc5faa4d1940baa429d3278a2f72ce5f30e50"
RESULT = HERE / "RESULTADO_GATE_RUNNER_V1X_R3_20261008.json"
TEST_LOG = HERE / "TESTE_F32_R3_20261008.log"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": digest(path)}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    if RESULT.exists() or TEST_LOG.exists():
        raise RuntimeError("R3 result or test log already exists")
    if digest(F31_JSON) != F31_SHA:
        raise RuntimeError("F3.1 R3 draft changed")
    start = now()
    tic = time.perf_counter()
    command = [sys.executable, "-B", "-m", "unittest", "-v",
               "test_f9_v1x_r3_20261008"]
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    run = subprocess.run(command, cwd=HERE, env=env,
                         text=True, capture_output=True, check=False)
    finish = now()
    elapsed = time.perf_counter() - tic
    log = (f"command={command!r}\ncwd={HERE}\nstart_utc={start}\n"
           f"end_utc={finish}\nseconds={elapsed:.6f}\nexit_code={run.returncode}\n"
           f"stdout:\n{run.stdout}\nstderr:\n{run.stderr}\n")
    with TEST_LOG.open("x", encoding="utf-8", newline="") as output:
        output.write(log)
    if run.returncode != 0 or "Ran 7 tests" not in log or "OK" not in log:
        raise RuntimeError("R3 tests failed; test log retained")
    gate_result = gate.verify_v1x_binding(
        BINDING, expected_binding_sha256=digest(BINDING),
        allowed_source_root=SOURCE_ROOT, expected_spec_sha256=SPEC_SHA,
    )
    before = pre.prepare_v1x(
        BINDING, expected_binding_sha256=digest(BINDING),
        allowed_source_root=SOURCE_ROOT, expected_spec_sha256=SPEC_SHA,
    )
    after = staged.run_synthetic(
        BINDING, digest(BINDING), SOURCE_ROOT, SPEC_SHA,
        FIXTURE, digest(FIXTURE), mode="synthetic_only",
    )
    declared = ["L1b_sh0es_r25", "L6_sirenes"]
    if before["n_alvos_declarados"] != 2 or after["n_alvos_declarados"] != 2:
        raise RuntimeError("preflight/staged declaration count diverged")
    if before["declared_unverified_reader_ids"] != declared or after["declared_unverified_reader_ids"] != declared:
        raise RuntimeError("declared inventory differs")
    if after["data_opened"] or after["verdict"] is not None:
        raise RuntimeError("synthetic execution claimed data opening or official verdict")
    if set(after["covariance_boxes"]) != {
        "P_primaria", "M_seis_masers_diagnostico", "N_sem_cefeidas",
        "R_r25", "S_com_sirenes",
    }:
        raise RuntimeError("family covariance coverage differs")
    proposed = after["synthetic_proposed_rule_output"]
    if (proposed["function_sha256"] != staged.PINNED_R3_VERDICT_SOURCE_SHA256
            or proposed["classification"] != "INCONCLUSIVE_SYSTEMATICS"):
        raise RuntimeError("pinned proposed verdict did not run as expected")
    errors = [
        stats["free_background_synthetic_mock"]["quadrature_abs_diff"]
        for family in after["synthetic_statistics"].values()
        for stats in family.values()
    ]
    lnbs = [
        stats["lnB_TGL_free_background_n100"]
        for family in after["synthetic_statistics"].values()
        for stats in family.values()
    ]
    if max(errors) > 1e-10 or not all(math.isfinite(value) for value in lnbs):
        raise RuntimeError("synthetic free-background quadrature failed")
    try:
        staged.run_synthetic(
            BINDING, digest(BINDING), SOURCE_ROOT, SPEC_SHA,
            FIXTURE, digest(FIXTURE), mode="real",
        )
    except gate.ReaderGateError:
        real_mode_refused = True
    else:
        raise RuntimeError("real mode accepted")
    independent = sorted(HERE.glob("test_f9_r3_independent*.py")) + sorted(
        HERE.glob("TESTE_R3_INDEPENDENTE*.log"))
    if len(independent) < 4:
        raise RuntimeError("independent G1-G5 scripts/logs not complete")
    files = [
        F31_JSON, BINDING, FIXTURE,
        HERE / "f9_reader_gate_v1x_r3.py",
        HERE / "f9_runner_v1x_preflight_r3.py",
        HERE / "f9_runner_v1x_staged_r3.py",
        HERE / "test_f9_v1x_r3_20261008.py",
        HERE / "build_resultado_f32_r3_20261008.py",
        HERE / "NOTA_R3_GATE_RUNNER_20261008.md",
        TEST_LOG,
        *independent,
    ]
    files = list(dict.fromkeys(files))
    result = {
        "unit": "F3.2",
        "delivery": "R3_ADDITIVE_CANDIDATE",
        "state": "RASCUNHO_NAO_CONGELADO",
        "created_utc": now(),
        "source_spec_sha256": SPEC_SHA,
        "doc_verified_count": sum(
            rec["status"] == "REAL_DOCUMENTARY_HASH_ONLY"
            for rec in gate_result["verified_readers"].values()),
        "declared_inventory_ids": declared,
        "n_alvos_declarados_preflight": before["n_alvos_declarados"],
        "n_alvos_declarados_staged": after["n_alvos_declarados"],
        "primary_rule1_synthetic_only": after["primary_rule1_if_applied"],
        "pinned_draft_function_sha256": proposed["function_sha256"],
        "pinned_draft_function_synthetic_token": proposed["draft_token_synthetic_only"],
        "covariance_families": sorted(after["covariance_boxes"]),
        "synthetic_free_background": {
            "prior_rd_Mpc": [130.0, 160.0],
            "motor": "SYNTHETIC_QUADRATIC_MOCK_NOT_CAMB_OR_REAL_BACKGROUND",
            "quadrature_n": [100, 200],
            "maximum_abs_difference": max(errors),
            "all_lnB_finite": True,
        },
        "tests": {"own_count": 7, "own_exit_code": run.returncode,
                  "own_seconds": elapsed, "independent_artifacts": len(independent),
                  "real_mode_refused": real_mode_refused},
        "data_opened": False,
        "official_verdict": None,
        "source_admission": "PENDING_D_H",
        "v2_frozen": False,
        "gate_changed": False,
        "limitations": [
            "F3.4 and X13 precede freeze",
            "D-H, D-J and c1 audit pending",
            "free background is quadratic synthetic fixture, not real CAMB likelihood",
            "covariances with sirens outside current box remain open",
            "no observed H0 centers used in synthetic calculations",
        ],
        "artifacts": [pin(path) for path in files],
    }
    raw = (json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
           + "\n").encode("utf-8")
    with RESULT.open("xb") as output:
        output.write(raw)
    if RESULT.read_bytes() != raw:
        raise RuntimeError("R3 receipt bytes differ after write")
    print(RESULT)
    print(hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()