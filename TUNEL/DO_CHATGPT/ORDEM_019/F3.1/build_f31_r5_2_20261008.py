"""Build an additive F3.1 R5.2 with numeric validation before verdict precedence."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCALAR_R51 = HERE / "PREREGISTRO_FASE9_V2_R5_1_F31_20261008.json"
JOINT_R51 = HERE / "ROOT90DA_F34_R5_1_D72_20261008.json"
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F3.1\AUDITORIA_F3_1_C1_a47334e0.md")
PINS = {
    SCALAR_R51: "f73bee1d8b45c43575e73bea8f4adf10724d039f1b96a50542cd7e70ae100c60",
    JOINT_R51: "291ed202132a2d6f67e3aa6925b609158ad85c0eb6b7863ef14d6d1d64274976",
    AUDIT: "c5b9b5214cc22877b5984466a7a2f3a340b43c8924ca14b9ab93ea4b722f5649",
}

VALIDATION = '''    allowed_flags = {
        "r.required_sources_admitted", "r.beta_livre_no_limite", "r.use_novel_parametros"
    }

    def finite(value):
        try:
            return math.isfinite(value)
        except (OverflowError, TypeError, ValueError):
            return False

    def scan(value, path):
        if isinstance(value, bool):
            if path not in allowed_flags:
                raise ValueError("INVALID_NUMERIC_INPUT:" + path)
        elif type(value) in (int, float):
            if not finite(value):
                raise ValueError("INVALID_NUMERIC_INPUT:" + path)
        elif isinstance(value, dict):
            for key, child in value.items():
                if not isinstance(key, str):
                    raise ValueError("INVALID_INPUT_KEY:" + path)
                scan(child, path + "." + key)
        elif isinstance(value, (list, tuple)):
            for index, child in enumerate(value):
                scan(child, path + "[" + str(index) + "]")
        elif value is None or isinstance(value, str):
            return
        else:
            raise ValueError("INVALID_INPUT_TYPE:" + path)

    def number(mapping, key, path):
        value = mapping.get(key) if isinstance(mapping, dict) else None
        if type(value) not in (int, float) or not finite(value):
            raise ValueError("INVALID_NUMERIC_INPUT:" + path)
        return value

    if not isinstance(r, dict):
        raise ValueError("INVALID_INPUT_TYPE:r")
    scan(r, "r")
    for flag in ("required_sources_admitted", "beta_livre_no_limite", "use_novel_parametros"):
        if type(r.get(flag)) is not bool:
            raise ValueError("INVALID_BOOLEAN_INPUT:r." + flag)
    if not isinstance(r.get("fundo"), str) or not r["fundo"]:
        raise ValueError("INVALID_INPUT_TYPE:r.fundo")
    n_local = number(r, "n_local", "r.n_local")
    n_alvos = number(r, "n_alvos_declarados", "r.n_alvos_declarados")
    if type(n_local) is not int or n_local < 1:
        raise ValueError("INVALID_NUMERIC_INPUT:r.n_local")
    if type(n_alvos) is not int or n_alvos < 0:
        raise ValueError("INVALID_NUMERIC_INPUT:r.n_alvos_declarados")
    low, high = r.get("minimum"), r.get("maximum")
    number(low, "z_delta", "r.minimum.z_delta")
    for key in ("poder_previo", "z_disc", "lnB_lcdm", "lnB_livre", "lnB_shift",
                "lnB_fundo_livre", "poder_nao_cefeida"):
        number(high, key, "r.maximum." + key)
    pairs = low.get("sigma_z_por_alvo") if isinstance(low, dict) else None
    if not isinstance(pairs, (list, tuple)) or not pairs:
        raise ValueError("INVALID_NUMERIC_INPUT:r.minimum.sigma_z_por_alvo")
    for index, pair in enumerate(pairs):
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError("INVALID_NUMERIC_INPUT:r.minimum.sigma_z_por_alvo[" + str(index) + "]")
        for field, value in enumerate(pair):
            if type(value) not in (int, float) or not finite(value):
                raise ValueError("INVALID_NUMERIC_INPUT:r.minimum.sigma_z_por_alvo["
                                 + str(index) + "][" + str(field) + "]")
        if pair[0] <= 0:
            raise ValueError("INVALID_NUMERIC_INPUT:r.minimum.sigma_z_por_alvo[" + str(index) + "][0]")
    endpoints_for_validation = r.get("dispersao_endpoints")
    if isinstance(endpoints_for_validation, dict):
        for name, row in endpoints_for_validation.items():
            if isinstance(row, dict):
                for key in ("chi2_por_gl", "p"):
                    if key in row:
                        value = number(row, key, "r.dispersao_endpoints." + name + "." + key)
                        if (key == "chi2_por_gl" and value < 0) or (key == "p" and not 0 <= value <= 1):
                            raise ValueError("INVALID_NUMERIC_INPUT:r.dispersao_endpoints."
                                             + name + "." + key)
'''


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def source_pin(path: Path) -> dict[str, object]:
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
            raise OSError("written bytes differ")
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def baseline() -> dict:
    return {
        "fundo": "BG1", "n_local": 5, "n_alvos_declarados": 0,
        "required_sources_admitted": True, "beta_livre_no_limite": False,
        "use_novel_parametros": True,
        "dispersao_endpoints": {
            "minimum": {"chi2_por_gl": 1.0, "p": 0.5},
            "maximum": {"chi2_por_gl": 1.0, "p": 0.5},
        },
        "minimum": {"z_delta": 0.5, "sigma_z_por_alvo": [(1.04, 0.0)]},
        "maximum": {"poder_previo": 6.0, "z_disc": 6.2, "lnB_lcdm": 6.0,
                    "lnB_livre": 0.0, "lnB_shift": 2.0,
                    "lnB_fundo_livre": 0.5, "poder_nao_cefeida": 4.0},
    }


def tests(source: str) -> list[dict[str, object]]:
    namespace: dict = {}
    exec(compile(source, "<F3.1-R5.2-verdict>", "exec"), namespace)
    decide = namespace["veredito_fase9_v2_r5_2_proposta"]
    cases: list[dict[str, object]] = []

    def rejected(name: str, mutate, path: str) -> None:
        row = baseline()
        mutate(row)
        try:
            token = decide(row)
        except ValueError as exc:
            if str(exc) != "INVALID_NUMERIC_INPUT:" + path:
                raise AssertionError((name, path, str(exc))) from exc
            cases.append({"name": name, "expected_error": str(exc), "rejected": True})
            return
        raise AssertionError((name, "invalid numeric input accepted", token))

    for key in ("poder_previo", "z_disc", "lnB_lcdm", "lnB_livre", "lnB_shift",
                "lnB_fundo_livre", "poder_nao_cefeida"):
        rejected(key + "_nan", lambda r, k=key: r["maximum"].update({k: float("nan")}), "r.maximum." + key)
        rejected(key + "_bool", lambda r, k=key: r["maximum"].update({k: True}), "r.maximum." + key)
    rejected("z_delta_nan", lambda r: r["minimum"].update(z_delta=float("nan")), "r.minimum.z_delta")
    rejected("z_delta_bool", lambda r: r["minimum"].update(z_delta=False), "r.minimum.z_delta")
    rejected("power_posinf", lambda r: r["maximum"].update(poder_previo=float("inf")), "r.maximum.poder_previo")
    rejected("z_disc_neginf", lambda r: r["maximum"].update(z_disc=-float("inf")), "r.maximum.z_disc")
    rejected("n_local_bool", lambda r: r.update(n_local=True), "r.n_local")
    rejected("n_alvos_bool", lambda r: r.update(n_alvos_declarados=False), "r.n_alvos_declarados")
    rejected("chi2_bool", lambda r: r["dispersao_endpoints"]["minimum"].update(chi2_por_gl=True),
             "r.dispersao_endpoints.minimum.chi2_por_gl")
    rejected("p_bool", lambda r: r["dispersao_endpoints"]["maximum"].update(p=False),
             "r.dispersao_endpoints.maximum.p")
    rejected("chi2_inf", lambda r: r["dispersao_endpoints"]["minimum"].update(chi2_por_gl=float("inf")),
             "r.dispersao_endpoints.minimum.chi2_por_gl")
    rejected("sigma_nan", lambda r: r["minimum"].update(sigma_z_por_alvo=[(float("nan"), 0.0)]),
             "r.minimum.sigma_z_por_alvo[0][0]")
    rejected("reader_z_bool", lambda r: r["minimum"].update(sigma_z_por_alvo=[(1.04, True)]),
             "r.minimum.sigma_z_por_alvo[0][1]")
    rejected("unknown_numeric_inf", lambda r: r.update(extra_numeric=float("inf")), "r.extra_numeric")

    controls = [
        ("baseline_discriminates", lambda r: None, "DISCRIMINATES_FROM_LCDM_AT_6SIGMA"),
        ("power_truncated", lambda r: r["maximum"].update(poder_previo=4.999), "POWER_P4P9_OF_5_SIGMA"),
        ("dispersion_missing", lambda r: r.update(dispersao_endpoints={}), "INCONCLUSIVE_SYSTEMATICS"),
        ("lnB_below_5", lambda r: r["maximum"].update(lnB_lcdm=4.99), "NOT_DISCRIMINATED_FROM_LCDM_LNB_BELOW_5"),
    ]
    for name, mutate, expected in controls:
        row = baseline()
        mutate(row)
        token = decide(row)
        if expected not in token:
            raise AssertionError((name, expected, token))
        cases.append({"name": name, "expected_token_part": expected, "token": token, "passed": True})
    return cases


def build() -> dict[str, bytes]:
    sources = {"scalar_r5_1": source_pin(SCALAR_R51),
               "joint_r5_1": source_pin(JOINT_R51),
               "audit_a47334e0": source_pin(AUDIT)}
    previous = json.loads(SCALAR_R51.read_text(encoding="utf-8"))
    old_spec = previous["spec"]
    assert previous["spec_sha256"] == sha(compact(old_spec))
    prior_function = old_spec["funcao_de_veredito"]["fonte"]
    assert old_spec["funcao_de_veredito"]["sha256"] == sha(prior_function.encode("utf-8"))
    anchor = '    base = "TGL_FASE9_RAZAO_DE_HUBBLE_V2_R5_DRAFT__"'
    if prior_function.count(anchor) != 1:
        raise ValueError("R5.1 function anchor changed")
    function = prior_function.replace(anchor, VALIDATION + "\n" + anchor, 1)
    function = function.replace("veredito_fase9_v2_r5_proposta", "veredito_fase9_v2_r5_2_proposta", 1)
    function = function.replace("V2_R5_DRAFT__", "V2_R5_2_DRAFT__", 1)
    assert "INVALID_NUMERIC_INPUT" in function
    cases = tests(function)

    scalar = copy.deepcopy(previous)
    scalar["id"] = "PREREG_FASE9_RAZAO_DE_HUBBLE_V2_DRAFT_F31_20261008_R5_2"
    scalar["state"] = "RASCUNHO_DOCUMENTAL_R5_2_NAO_CONGELADO"
    scalar["derived_from"] = sources["scalar_r5_1"]
    scalar["integration_note"] = (
        "R5.2 valida todos os campos numericos antes de qualquer precedencia; NaN, +/-inf e bool "
        "em campo numerico geram ValueError visivel. X13 e D-H antecedem o congelamento; "
        "abertura requer ato separado. F3.2 deve pinar esta fonte apos auditoria c1."
    )
    spec = scalar["spec"]
    spec["id"] = scalar["id"]
    spec["generated_from"]["R5_1_registered"] = sources["scalar_r5_1"]
    spec["generated_from"]["audit_a47334e0"] = sources["audit_a47334e0"]
    spec["funcao_de_veredito"]["fonte"] = function
    spec["funcao_de_veredito"]["sha256"] = sha(function.encode("utf-8"))
    spec["funcao_de_veredito"]["nome"] = "veredito_fase9_v2_r5_2_proposta"
    spec["funcao_de_veredito"]["numeric_precedence_guard"] = (
        "Every numeric input must be finite and not bool before any verdict precedence; "
        "invalid input raises ValueError INVALID_NUMERIC_INPUT:path, never a NOT_FALSIFIED token"
    )
    spec["funcao_de_veredito"]["testes_sinteticos_r5_2"] = [case["name"] for case in cases]
    spec["funcao_de_veredito"]["se_abrir_hoje"]["token_counterfactual_synthetic"] = (
        "TGL_FASE9_RAZAO_DE_HUBBLE_V2_R5_2_DRAFT__INCONCLUSIVE_SYSTEMATICS"
        "__D1B__FUNDO_BG1__NOT_BLIND_TO_DATA_STATED__NOT_A_CONFIRMATION__GATE_UNTOUCHED"
    )
    spec["token_base_provisorio"] = "TGL_FASE9_RAZAO_DE_HUBBLE_V2_R5_2_DRAFT__LAW_D1B__BG1"
    spec["token_estado"] = "RASCUNHO_R5_2__NUMERIC_FAIL_CLOSED__X13_D_H_BEFORE_FREEZE__GATE_UNTOUCHED"
    assert spec["source_admission"]["freezing_guard"].startswith("BLOCK_FREEZE_UNLESS_X13_AND_D_H")
    assert spec["covariancia"]["components"]["SBF_0p031"]["bibliographic_origin"] == "[OPEN]"
    scalar["spec_sha256"] = sha(compact(spec))

    joint = copy.deepcopy(json.loads(JOINT_R51.read_text(encoding="utf-8")))
    joint["schema"] = "ROOT90DA_F34_TWO_WITNESSES_ADDENDUM_R5_2"
    joint["derived_from"] = sources["joint_r5_1"]
    joint["scalar_witness"]["derived_spec_sha256"] = scalar["spec_sha256"]
    joint["scalar_witness"]["r5_2_verdict_function_sha256"] = spec["funcao_de_veredito"]["sha256"]
    assert "d72" in joint["other_operator_acts"]

    scalar_name = "PREREGISTRO_FASE9_V2_R5_2_F31_20261008.json"
    joint_name = "ROOT90DA_F34_R5_2_D72_20261008.json"
    test_name = "TESTE_F31_R5_2_NUMERIC_20261008.json"
    note_name = "ADENDO_F31_R5_2_NUMERIC_FAIL_CLOSED_20261008.md"
    result_name = "RESULTADO_F31_V2_R5_2_20261008.json"
    files = {
        scalar_name: pretty(scalar),
        joint_name: pretty(joint),
        test_name: pretty({"schema": "F31_R5_2_NUMERIC_TESTS_V1", "synthetic_only": True,
                           "function_sha256": spec["funcao_de_veredito"]["sha256"],
                           "passed": len(cases), "cases": cases, "real_data_opened": False}),
        note_name: (
            "# F3.1 R5.2 — números válidos antes da precedência\n\n"
            "[REAL — teste sintético] A auditoria c1 a47334e0 mostrou que NaN em poder, z_delta, "
            "z_disc e lnB_lcdm atravessava a função R5/R5.1. A fonte R5.2 recusa, antes da "
            "precedência, todo valor numérico não finito ou booleano, inclusive dispersão e leitores. "
            "A recusa é ValueError com caminho; não emite token de veredito.\n\n"
            "[OPEN] A origem bibliográfica do fator 0,031 permanece aberta. X13 e D-H continuam "
            "pré-requisitos do congelamento; d72 e a abertura são atos separados do operador. "
            "Esta entrega não congela, não abre dado e não move o gate.\n"
        ).encode("utf-8"),
    }
    result = {
        "schema": "F31_V2_R5_2_RESULT_V1", "unit": "F3.1", "status": "ENTREGUE_PARA_REAUDITORIA_C1",
        "sources": sources, "generator": source_pin(Path(__file__)),
        "new_artifacts": {name: {"sha256": sha(data), "bytes": len(data)} for name, data in files.items()},
        "scalar_spec_sha256": scalar["spec_sha256"],
        "scalar_verdict_function_sha256": spec["funcao_de_veredito"]["sha256"],
        "synthetic_tests_passed": len(cases),
        "numeric_invalid_raises_before_precedence": True,
        "factor_0p031_bibliographic_origin": "OPEN",
        "frozen": False, "real_data_opened": False, "compound_computed": False, "gate_changed": False,
    }
    files[result_name] = pretty(result)
    return files


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
