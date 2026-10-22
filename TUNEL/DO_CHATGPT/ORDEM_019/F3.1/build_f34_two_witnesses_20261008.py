"""Build new documentary F3.4 sidecars without changing any pinned source."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
WORK = ROOT / "work" / "f9_pergunta_08out"
O18 = HERE.parents[1] / "ORDEM_018"

SOURCES = {
    "scalar_r4": HERE / "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R4.json",
    "joint_contract": O18 / "f9_executive_contract_preparation" / "CONTRATO_CONSOLIDADO.json",
    "comparison": O18 / "COMPARACAO_ESPECIFICACOES_F9.json",
    "operator_verbatim": WORK / "OPERADOR_08out_resposta_verbatim.txt",
    "operator_resolution": WORK / "F34_RESOLUCAO_OPERADOR_20261008.md",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(obj: object) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def pretty(obj: object) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def source_pin(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": str(path), "sha256": sha(data), "bytes": len(data)}


def put_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(path)
    with path.open("xb") as out:
        out.write(data)
        out.flush()
    if path.stat().st_size != len(data) or path.read_bytes() != data:
        raise OSError(f"New artifact did not round-trip: {path}")


def main() -> None:
    pins = {name: source_pin(path) for name, path in SOURCES.items()}
    operator = SOURCES["operator_verbatim"].read_text(encoding="utf-8")
    resolution = SOURCES["operator_resolution"].read_text(encoding="utf-8")
    assert "o fixo é o verbo" in operator and "o verbo é betatgl" in operator
    assert "Ratificação do operador" in resolution and "é isso mesmo" in resolution

    original = json.loads(SOURCES["scalar_r4"].read_text(encoding="utf-8"))
    joint = json.loads(SOURCES["joint_contract"].read_text(encoding="utf-8"))
    comparison = json.loads(SOURCES["comparison"].read_text(encoding="utf-8"))
    assert original["state"] == "RASCUNHO_NAO_CONGELADO"
    assert original["spec"]["pending_operator_decisions"][0].startswith("F3.4 ")
    assert joint["identity"]["request_id"] == "90da371b-f14a-4af6-9d6d-90b9619ba8d7"
    assert comparison["operational_resolution"]["do_not_pool_or_multiply_results"] is True

    derived = copy.deepcopy(original)
    spec = derived["spec"]
    prior_function = copy.deepcopy(spec["funcao_de_veredito"])
    spec["pending_operator_decisions"] = [
        item for item in spec["pending_operator_decisions"] if not item.startswith("F3.4 ")
    ]
    spec["especificacao_do_runner"][4] = (
        "R4 only after X13/NAT22, D-H, and c1 audit may the operator open "
        "P_primaria versus BG1; F3.4 is resolved by operator decision event 462"
    )
    spec["estado"] = "RASCUNHO_NAO_CONGELADO; F3.4 resolved; X13 before freeze; D-H before opening"
    spec["funcao_de_veredito_proposta"]["status"] = "NOT_EXECUTABLE_UNTIL_NAT22_D_J_AND_C1_AUDIT"
    spec["nao_decide"] = [item for item in spec["nao_decide"] if item != "F3.4 governing specification"]
    spec["token_estado"] = "RASCUNHO_NAO_CONGELADO__F3_4_RESOLVED__X13_D_J_PENDING__GATE_UNTOUCHED"
    spec["f34_duas_testemunhas"] = {
        "estatuto": "[INPUT] decisao do operador; [DERIVED] projecao documental",
        "fonte_operador": pins["operator_verbatim"],
        "fonte_ratificacao": pins["operator_resolution"],
        "quadro_f34": {"status": "FECHADA", "evento": 462},
        "fato_unico": "razao de Hubble sob a lei K = E(z*)^(2*beta_TGL/3)",
        "verbo_fixo": "beta_TGL = ALPHA_FINE_CODATA_2018 * sqrt(e) em runtime, mu q->0 Thomson",
        "nome": "variavel conforme o instrumento; posto, nao parametro da lei ajustado ao dado",
        "escalar": "testemunha propria, com esta funcao de veredito; nao julga ROOT90da",
        "conjunto": "testemunha propria, com sua funcao fixada antes de seu composto; nao julga o escalar",
        "regras": [
            "nao somar vereditos, significancias ou evidencias dos instrumentos",
            "nao emprestar poder, fonte admitida, congelamento ou abertura entre instrumentos",
            "ler os dois depoimentos lado a lado, cada qual por sua funcao previamente pinada",
        ],
        "pendencias_operador": ["X13", "D-H", "d72", "F3.3 abertura"],
        "token_D_J": "permanece D_J_PENDING na R4, sem cunhagem por este adendo",
        "congelamento": False,
        "abertura": False,
    }
    assert spec["funcao_de_veredito"] == prior_function
    assert spec["funcao_de_veredito"]["sha256"] == "98ba17095fc8f84d053f8b7ab18f8c0125db323aba930e487bcb49bea924c14d"
    derived["state"] = "RASCUNHO_DOCUMENTAL_F34_NAO_CONGELADO"
    derived["spec_sha256"] = sha(compact(spec))
    derived["derived_from"] = pins["scalar_r4"]
    derived["integration_note"] = (
        "Nova projecao documental: F3.2 R4 ainda pina a spec R4 original. "
        "Antes de composto real, c1 deve auditar e o runner/gate deve pinar a especificacao efetiva."
    )

    joint_addendum = {
        "schema": "ROOT90DA_F34_TWO_WITNESSES_ADDENDUM_V1",
        "state": "DOCUMENTARY_ADDENDUM_NO_FREEZE_NO_OPENING",
        "root90da_contract": pins["joint_contract"],
        "comparison_historical": pins["comparison"],
        "operator_verbatim": pins["operator_verbatim"],
        "operator_resolution": pins["operator_resolution"],
        "quadro_f34": {"status": "FECHADA", "evento": 462},
        "fact": "mesmo fato, a razao de Hubble, observado por instrumentos estatisticos diferentes",
        "fixed_verb": "beta_TGL = ALPHA_FINE_CODATA_2018 * sqrt(e) em runtime, sem ajuste ao dado",
        "variable_name": "posto relativo ao instrumento e sua leitura, segundo o operador [ONTO]",
        "joint_witness": "proposta conjunta ROOT90da; funcao de veredito propria fixada antes do seu composto",
        "scalar_witness": {"derived_spec_sha256": derived["spec_sha256"], "original_r4_sha256": pins["scalar_r4"]["sha256"]},
        "separation": {
            "no_judge_between_witnesses": True,
            "no_pool_or_multiply": True,
            "no_power_or_admission_transfer": True,
            "read_side_by_side": True,
        },
        "joint_state": {
            "contract_status": joint["status"],
            "not_operator_ratified_as_scientific_contract": True,
            "not_frozen_executable": True,
            "five_frequentist_tests_separate": True,
            "qualification_d72": "AGUARDA_OPERADOR; nao executar nesta entrega",
            "verdict_before_composite": "REQUIRED; a proposta ainda nao constitui abertura",
        },
        "other_operator_acts": ["X13", "D-H", "F3.3 abertura"],
        "observed_data_opened": False,
        "compound_computed": False,
        "gate_changed": False,
    }

    scalar_name = "PREREGISTRO_FASE9_V2_R4_F34_DUAS_TESTEMUNHAS_20261008.json"
    joint_name = "ROOT90DA_F34_DUAS_TESTEMUNHAS_20261008.json"
    scalar_bytes = pretty(derived)
    joint_bytes = pretty(joint_addendum)
    assert json.loads(scalar_bytes)["spec_sha256"] == sha(compact(json.loads(scalar_bytes)["spec"]))

    note = "\n".join([
        "# F3.4 ao lado: duas testemunhas da razão de Hubble",
        "",
        "[INPUT — decisão do operador, F3.4 fechada no evento 462] O escalar V1→V2 e o conjunto ROOT90da testemunham o mesmo fato. O Verbo fixo é β_TGL, posto sem ajuste. O Nome varia com a leitura. Nenhum instrumento julga o outro e seus resultados não se somam.",
        "",
        f"Fonte verbal: `{pins['operator_verbatim']['path']}` sha256 `{pins['operator_verbatim']['sha256']}`; ratificação: `{pins['operator_resolution']['path']}` sha256 `{pins['operator_resolution']['sha256']}`.",
        f"[REAL documental] A projeção V2 R4+F3.4 é `{scalar_name}` sha256 `{sha(scalar_bytes)}`. A R4 pinada permanece `{pins['scalar_r4']['sha256']}`. A função de veredito mantém exatamente o hash `98ba17095fc8f84d053f8b7ab18f8c0125db323aba930e487bcb49bea924c14d`.",
        f"[REAL documental] O conjunto recebe `{joint_name}` sha256 `{sha(joint_bytes)}`, sobre o contrato ROOT90da `{pins['joint_contract']['sha256']}`. Os cinco testes frequentistas continuam próprios; a função executável ainda exige qualificação e pin antes de qualquer composto.",
        "",
        "[OPEN] X13, D-H, d72 e a abertura continuam reservados ao operador. A R4 mantém D-J como nome pendente, sem inventar token. O runner F3.2 R4 ainda pina a spec R4 original e precisa de versão auditada para pinar esta projeção antes de execução real. Nada foi congelado ou aberto; nenhum gate mudou.",
        "",
    ]).encode("utf-8")
    note_name = "ADENDO_F34_DUAS_TESTEMUNHAS_20261008.md"

    result = {
        "schema": "F31_F34_TWO_WITNESSES_RESULT_V1",
        "unit": "F3.1",
        "status": "ENTREGUE_PARA_AUDITORIA_DOCUMENTAL",
        "quadro_f34": {"status": "FECHADA", "evento": 462},
        "sources": pins,
        "new_artifacts": {
            scalar_name: {"sha256": sha(scalar_bytes), "bytes": len(scalar_bytes)},
            joint_name: {"sha256": sha(joint_bytes), "bytes": len(joint_bytes)},
            note_name: {"sha256": sha(note), "bytes": len(note)},
        },
        "scalar_spec_sha256": derived["spec_sha256"],
        "scalar_verdict_function_sha256": spec["funcao_de_veredito"]["sha256"],
        "joint_contract_sha256": pins["joint_contract"]["sha256"],
        "unchanged_sources_verified": True,
        "frozen": False,
        "real_data_opened": False,
        "compound_computed": False,
        "gate_changed": False,
    }
    result_name = "RESULTADO_F31_F34_DUAS_TESTEMUNHAS_20261008.json"
    files = {
        scalar_name: scalar_bytes,
        joint_name: joint_bytes,
        note_name: note,
        result_name: pretty(result),
    }
    for name in files:
        if (HERE / name).exists():
            raise FileExistsError(HERE / name)
    for name, data in files.items():
        put_new(HERE / name, data)
    print(json.dumps({"created": {name: sha(data) for name, data in files.items()}, "scalar_spec_sha256": derived["spec_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
