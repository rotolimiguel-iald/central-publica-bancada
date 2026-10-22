"""Add the current X13 plus D-H freeze guard to the pinned F3.1 R5."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
R5 = HERE / "PREREGISTRO_FASE9_V2_R5_F31_20261008.json"
JOINT_R5 = HERE / "ROOT90DA_F34_R5_D72_20261008.json"
RESULT_R5 = HERE / "RESULTADO_F31_V2_R5_20261008.json"
PINS = {
    R5: "ab84d493c9ac54083eb78495e19e9da93782392ca5ffa5981e5ac7c83ce76f09",
    JOINT_R5: "d96f2611664571e872df789a4b4cdc83e4de9d77a8f5a3debcf5e620263f1b6f",
    RESULT_R5: "f1acc82406dfcd27d80d1538eabb18ec5467592b770a2495738842811fd18550",
}

PREFLIGHT = '''def preflight_congelamento_f31_r5_1(r):
    """Documentary guard only; this function never freezes or opens a test."""
    if r.get("x13_operator_decision_pinned") is not True:
        return "REFUSE_FREEZE__X13_OPERATOR_DECISION_MISSING"
    if r.get("dh_operator_admission_pinned") is not True:
        return "REFUSE_FREEZE__D_H_OPERATOR_ADMISSION_MISSING"
    if r.get("c1_audit_r5_1_passed") is not True:
        return "REFUSE_FREEZE__C1_AUDIT_MISSING"
    return "ELIGIBLE_FOR_SEPARATE_C1_FREEZE_PROCEDURE__NO_ACTION_TAKEN"
'''


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(obj: object) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty(obj: object) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def pinned(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    actual = sha(data)
    if path in PINS and actual != PINS[path]:
        raise ValueError(f"source pin changed: {path}: {actual}")
    return {"path": str(path), "sha256": actual, "bytes": len(data)}


def put_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(path)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
        if Path(temporary).stat().st_size != len(data):
            raise OSError("temporary size mismatch")
        os.replace(temporary, path)
        if path.read_bytes() != data:
            raise OSError("write verification failed")
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def build() -> dict[str, bytes]:
    sources = {"scalar_r5": pinned(R5), "joint_r5": pinned(JOINT_R5),
               "result_r5": pinned(RESULT_R5)}
    previous = json.loads(R5.read_text(encoding="utf-8"))
    old_spec = previous["spec"]
    assert sha(compact(old_spec)) == previous["spec_sha256"]
    old_function = copy.deepcopy(old_spec["funcao_de_veredito"])

    scalar = copy.deepcopy(previous)
    scalar["id"] = "PREREG_FASE9_RAZAO_DE_HUBBLE_V2_DRAFT_F31_20261008_R5_1"
    scalar["state"] = "RASCUNHO_DOCUMENTAL_R5_1_NAO_CONGELADO"
    scalar["derived_from"] = sources["scalar_r5"]
    scalar["integration_note"] = (
        "X13 e D-H sao requisitos ANTES do congelamento, conforme despacho c1 vigente. "
        "Esta camada documental nao congela, nao admite fontes e nao abre dados. "
        "F3.2 requer novo pin depois da auditoria c1."
    )
    spec = scalar["spec"]
    spec["id"] = scalar["id"]
    spec["estado"] = "RASCUNHO_NAO_CONGELADO; X13 e D-H antes do congelamento; abertura exige ato posterior"
    spec["token_estado"] = "RASCUNHO_R5_1__X13_D_H_BEFORE_FREEZE__D72_AND_OPENING_PENDING__GATE_UNTOUCHED"
    spec["generated_from"]["R5_registered"] = sources["scalar_r5"]
    spec["source_admission"]["freezing_guard"] = (
        "BLOCK_FREEZE_UNLESS_X13_AND_D_H_OPERATOR_ACTS_PINNED; c1 audit also required"
    )
    spec["source_admission"]["opening_guard"] = (
        "BLOCK_OPENING_UNLESS_D_H_OPERATOR_ADMISSION_PINNED_AND_SEPARATE_OPERATOR_OPENING_ACT"
    )
    spec["pending_operator_decisions"] = [
        "X13 executor deviations before freeze",
        "D-H source admission before freeze",
        "D-J final token name",
        "d72 qualification in Codex interface",
        "F3.3 opening after frozen audited V2",
    ]
    spec["freeze_preflight"] = {
        "status": "DOCUMENTARY_GUARD_NOT_EXECUTED_ON_REAL_INPUT",
        "source": PREFLIGHT,
        "sha256": sha(PREFLIGHT.encode("utf-8")),
        "requires": ["X13 operator decision pinned", "D-H operator admission pinned", "c1 R5.1 audit"],
        "current": "REFUSE_FREEZE__X13_OPERATOR_DECISION_MISSING",
        "eligible_token_does_not_freeze": True,
    }
    assert spec["funcao_de_veredito"] == old_function
    scalar["spec_sha256"] = sha(compact(spec))

    joint = copy.deepcopy(json.loads(JOINT_R5.read_text(encoding="utf-8")))
    joint["schema"] = "ROOT90DA_F34_TWO_WITNESSES_ADDENDUM_R5_1"
    joint["derived_from"] = sources["joint_r5"]
    joint["scalar_witness"]["derived_spec_sha256"] = scalar["spec_sha256"]
    joint["freeze_prerequisites"] = ["X13 operator decision pinned", "D-H operator admission pinned", "c1 audit"]
    assert "d72" in joint["other_operator_acts"]

    namespace: dict = {}
    exec(compile(PREFLIGHT, "<F3.1-R5.1-freeze-preflight>", "exec"), namespace)
    decide = namespace["preflight_congelamento_f31_r5_1"]
    rows = [
        ({}, "REFUSE_FREEZE__X13_OPERATOR_DECISION_MISSING"),
        ({"x13_operator_decision_pinned": True}, "REFUSE_FREEZE__D_H_OPERATOR_ADMISSION_MISSING"),
        ({"x13_operator_decision_pinned": True, "dh_operator_admission_pinned": True},
         "REFUSE_FREEZE__C1_AUDIT_MISSING"),
        ({"x13_operator_decision_pinned": True, "dh_operator_admission_pinned": True,
          "c1_audit_r5_1_passed": True}, "ELIGIBLE_FOR_SEPARATE_C1_FREEZE_PROCEDURE__NO_ACTION_TAKEN"),
        ({"x13_operator_decision_pinned": 1, "dh_operator_admission_pinned": True,
          "c1_audit_r5_1_passed": True}, "REFUSE_FREEZE__X13_OPERATOR_DECISION_MISSING"),
    ]
    cases = []
    for inputs, expected in rows:
        actual = decide(inputs)
        if actual != expected:
            raise AssertionError((inputs, expected, actual))
        cases.append({"inputs": inputs, "expected": expected, "actual": actual})

    scalar_name = "PREREGISTRO_FASE9_V2_R5_1_F31_20261008.json"
    joint_name = "ROOT90DA_F34_R5_1_D72_20261008.json"
    tests_name = "TESTE_F31_R5_1_FREEZE_20261008.json"
    note_name = "ERRATA_F31_R5_FREEZE_GUARD_20261008.md"
    result_name = "RESULTADO_F31_V2_R5_1_20261008.json"
    scalar_bytes = pretty(scalar)
    joint_bytes = pretty(joint)
    tests_bytes = pretty({"schema": "F31_R5_1_FREEZE_PREFLIGHT_TESTS_V1", "synthetic_only": True,
                          "source_sha256": spec["freeze_preflight"]["sha256"],
                          "passed": len(cases), "cases": cases, "freeze_executed": False})
    note_bytes = (
        "# F3.1 R5.1 — errata ao lado da guarda de congelamento\n\n"
        "[INPUT — despacho c1 de 08/10/2026, fim de tarde] O congelamento espera X13 e D-H, "
        "ambos atos do operador. A R5 preservava a frase herdada 'D-H before opening', insuficiente "
        "para este ponto. A R5.1 exige X13 e D-H antes do congelamento; D-H continua necessario "
        "tambem antes da abertura, que requer ato proprio.\n\n"
        "[REAL documental] O preflight tipado recusa a ausencia de qualquer um desses atos e da "
        "auditoria c1; cinco casos sinteticos passaram. O retorno de elegibilidade nao congela. "
        "A funcao cientifica R5 e seus 20 testes permanecem byte a byte iguais.\n\n"
        "[OPEN] Origem bibliografica do fator 0,031. Nenhum dado real, composto, congelamento ou "
        "gate foi tocado.\n"
    ).encode("utf-8")
    artifacts = {scalar_name: scalar_bytes, joint_name: joint_bytes,
                 tests_name: tests_bytes, note_name: note_bytes}
    result = {
        "schema": "F31_V2_R5_1_RESULT_V1", "unit": "F3.1", "status": "ENTREGUE_PARA_REAUDITORIA_C1",
        "sources": sources, "generator": pinned(Path(__file__)),
        "new_artifacts": {name: {"sha256": sha(data), "bytes": len(data)} for name, data in artifacts.items()},
        "scalar_spec_sha256": scalar["spec_sha256"],
        "scientific_verdict_function_sha256_unchanged": old_function["sha256"],
        "freeze_preflight_sha256": spec["freeze_preflight"]["sha256"],
        "synthetic_freeze_refusal_cases_passed": len(cases),
        "x13_and_dh_before_freeze": True, "d72_in_other_operator_acts": True,
        "factor_0p031_bibliographic_origin": "OPEN",
        "frozen": False, "real_data_opened": False, "compound_computed": False, "gate_changed": False,
    }
    artifacts[result_name] = pretty(result)
    return artifacts


def main() -> None:
    files = build()
    check = "--check" in sys.argv[1:]
    for name, data in files.items():
        path = HERE / name
        if check:
            if path.read_bytes() != data:
                raise AssertionError(f"generated bytes differ: {path}")
        else:
            put_new(path, data)
    print(json.dumps({"mode": "check" if check else "create",
                      "artifacts": {name: sha(data) for name, data in files.items()}}, indent=2))


if __name__ == "__main__":
    main()
