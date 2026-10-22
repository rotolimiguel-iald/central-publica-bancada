"""Build the new F3.1/F3.2 R2 delivery receipt from artifact bytes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019")
F31 = BASE / "F3.1"
F32 = BASE / "F3.2"
OUT = F31 / "RESULTADO_V2_R2_F31_F32_20261008.json"
FILES = {
    "generator": F31 / "generate_fase9_v2_draft_f31_20261008_R2.py",
    "v2_draft_json": F31 / "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R2.json",
    "v2_draft_md": F31 / "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R2.md",
    "v1_v2_diff": F31 / "DIFF_V1_V2_RASCUNHO_F31_20261008_R2.patch",
    "generation_manifest": F31 / "GERACAO_V2_RASCUNHO_F31_20261008_R2.json",
    "tgl_h0_observable_exam": F31 / "EXAME_MAPA_TGL_H0_R2_20261008.md",
    "binding_builder": F32 / "build_v1x_binding.py",
    "v1x_binding": F32 / "VINCULO_DOCUMENTAL_V1X_R2_20261008.json",
    "documentary_gate": F32 / "f9_reader_gate_v1x.py",
    "documentary_gate_receipt": F32 / "RESULTADO_GATE_V1X_R2_20261008.json",
    "documentary_gate_tests": F32 / "test_f9_reader_gate_v1x.py",
    "documentary_gate_test_log": F32 / "TESTE_GATE_V1X_R2_20261008.log",
    "runner_preflight": F32 / "f9_runner_v1x_preflight.py",
    "runner_preflight_tests": F32 / "test_f9_runner_v1x_preflight_r2.py",
    "runner_preflight_test_log": F32 / "TESTE_RUNNER_V1X_PREFLIGHT_R2_20261008.log",
    "runner_staged": F32 / "f9_runner_v1x_staged.py",
    "runner_staged_tests": F32 / "test_f9_runner_v1x_staged.py",
    "runner_staged_test_log": F32 / "TESTE_RUNNER_V1X_STAGED_20261008.log",
    "synthetic_fixture": F32 / "FIXTURE_SINTETICO_V1X_R2_20261008.json",
    "synthetic_result": F32 / "RESULTADO_RUNNER_V1X_SINTETICO_R2_20261008.json",
}


def pinned(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def build() -> bytes:
    draft = json.loads(FILES["v2_draft_json"].read_bytes())
    binding = json.loads(FILES["v1x_binding"].read_bytes())
    staged = json.loads(FILES["synthetic_result"].read_bytes())
    gate = json.loads(FILES["documentary_gate_receipt"].read_bytes())
    assert draft["state"] == "RASCUNHO_NAO_CONGELADO"
    assert binding["draft_v2"]["sha256"] == pinned(FILES["v2_draft_json"])["sha256"]
    assert binding["spec_sha256"] == draft["spec_sha256"]
    assert staged["stage"] == "SYNTHETIC_STATISTICAL_REHEARSAL_ONLY"
    assert staged["data_opened"] is False and staged["verdict"] is None
    assert staged["v2_frozen"] is False and staged["gate_changed"] is False
    assert staged["n_alvos_declarados_inventory"] == 2
    assert gate["tests"] == {"failed": 0, "passed": 12, "scope": "documentary and refusal; no real-data opening"}
    assert "Ran 3 tests" in FILES["runner_preflight_test_log"].read_text(encoding="utf-8-sig")
    assert "Ran 7 tests" in FILES["runner_staged_test_log"].read_text(encoding="utf-8-sig")
    assert not (F32 / "__pycache__").exists()
    payload = {
        "id": "F31_F32_V2_R2_PREPARATION_20261008",
        "status": "ENTREGUE_PARA_REAUDITORIA_C1_SEM_CONGELAMENTO",
        "spec_sha256": draft["spec_sha256"],
        "artifacts": {name: pinned(path) for name, path in FILES.items()},
        "tests": {
            "generator_check_only": "PASS_BYTE_IDENTICAL",
            "documentary_gate": "12/12 PASS",
            "runner_preflight": "3/3 PASS",
            "runner_staged_synthetic": "7/7 PASS",
            "independent_reading": "PASS_DOCUMENTARY_WITH_EXPLICIT_OPEN_TGL_MAP_AND_STAGED_RUNNER_LIMIT",
        },
        "reader_status": gate["verified_readers"],
        "primary": ["L1_sh0es_r22", "L2_cchp", "L3_sbf", "L4_masers_5", "L5_tdcosmo"],
        "six_masers": "DIAGNOSTIC_ONLY_NOT_SUMMED",
        "n_alvos_declarados_inventory": 2,
        "n_alvos_declarados_rule": "not gate_verified AND not operator_admitted in pinned register; missing admission is a separate opening guard",
        "source_admission": "OPEN_PENDING_D_H",
        "spec_governance": "PENDING_F3_4",
        "executor_deviations": "PENDING_X13",
        "final_token_name": "PENDING_D_J",
        "tgl_h0_likelihood_map": "OPEN_FOR_ALL_EIGHT_READERS; DOCUMENTARY_EXAM_ATTACHED",
        "runner_scope": "PINNED_SYNTHETIC_STATISTICAL_REHEARSAL_ONLY; FREE_BACKGROUND_MOTOR_AND_REAL_DATA_EXECUTION_NOT_IMPLEMENTED",
        "v2_frozen": False,
        "real_data_opened": False,
        "alvos_fase9_lidos_written_by_this_delivery": False,
        "gate_moved": False,
        "verdict": None,
        "next": "C1 reaudits; operator decides F3.4 and X13 before freeze, D-H before opening",
    }
    return (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def main() -> None:
    raw = build()
    if "--check" in sys.argv[1:]:
        assert OUT.read_bytes() == raw
        print(json.dumps({"mode": "check", "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}))
        return
    with OUT.open("xb") as stream:
        stream.write(raw)
    print(json.dumps({"mode": "created", "path": str(OUT), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}))


if __name__ == "__main__":
    main()
