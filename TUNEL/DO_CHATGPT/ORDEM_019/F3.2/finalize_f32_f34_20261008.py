"""Seal the documentary F3.4 F3.2 candidate after its synthetic tests pass."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
F31 = HERE.parent / "F3.1"
PROJECTION = F31 / "PREREGISTRO_FASE9_V2_R4_F34_DUAS_TESTEMUNHAS_20261008.json"
NEW = [
    "VINCULO_DOCUMENTAL_V1X_F34_20261008.json",
    "f9_reader_gate_v1x_f34.py",
    "f9_runner_v1x_preflight_f34.py",
    "f9_runner_v1x_staged_f34.py",
    "test_f9_v1x_f34_20261008.py",
    "TESTE_F32_F34_20261008.log",
    "build_f32_f34_binding_20261008.py",
    "finalize_f32_f34_20261008.py",
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pin(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": str(path), "sha256": digest(data), "bytes": len(data)}


def pretty(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")


def write_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(path)
    with path.open("xb") as out:
        out.write(data)
        out.flush()
    if path.read_bytes() != data:
        raise OSError(f"Round-trip differs: {path}")


def main() -> None:
    projection = pin(PROJECTION)
    assert projection["sha256"] == "ca59870c4e840bf6c87b7b5051cc1b4e6ff25a88d026fca38893291fdd14153f"
    spec = json.loads(PROJECTION.read_bytes())
    assert spec["spec_sha256"] == "dbe01f4cef9e6d155d51cbf2930014289144761bb8b948a3b3195615bc609e1b"
    assert spec["spec"]["funcao_de_veredito"]["sha256"] == "98ba17095fc8f84d053f8b7ab18f8c0125db323aba930e487bcb49bea924c14d"

    binding = json.loads((HERE / NEW[0]).read_bytes())
    assert binding["draft_v2"]["sha256"] == projection["sha256"]
    assert binding["spec_sha256"] == spec["spec_sha256"]
    assert binding["f34_decision"]["no_pooling"] is True
    log = (HERE / "TESTE_F32_F34_20261008.log").read_text(encoding="utf-8")
    assert "EXIT_CODE: 0" in log and "Ran 6 tests" in log and "\nOK\n" in log
    assert "test_real_mode_refused_before_documentary_read" in log
    assert "test_synthetic_statistics_equal_r4_and_no_real_verdict" in log

    new_pins = [pin(HERE / name) for name in NEW]
    old_pins = [
        pin(HERE / "VINCULO_DOCUMENTAL_V1X_R4_20261008.json"),
        pin(HERE / "f9_reader_gate_v1x_r4.py"),
        pin(HERE / "f9_runner_v1x_preflight_r4.py"),
        pin(HERE / "f9_runner_v1x_staged_r4.py"),
    ]
    assert old_pins[0]["sha256"] == "54c456fc201b224220ac52724d5d6e52aac12485d6d911c96ff72b12c7c9982e"

    note = "\n".join([
        "# F3.2 — vínculo novo para a decisão F3.4",
        "",
        "[INPUT] F3.4 foi fechada pelo operador no evento 462: escalar e ROOT90da são duas testemunhas, com β_TGL fixo sem ajuste, sem soma e sem julgamento mútuo.",
        f"[REAL documental] A projeção escalar F3.4 tem sha256 `{projection['sha256']}` e spec interna `{spec['spec_sha256']}`. O novo vínculo F3.2 a lê uma só vez, confere bytes e o contrato F3.4, e mantém a função de veredito R4 sha256 `98ba17095fc8f84d053f8b7ab18f8c0125db323aba930e487bcb49bea924c14d`.",
        f"[REAL sintético] O log `{new_pins[5]['path']}` (sha256 `{new_pins[5]['sha256']}`) registra 6 testes, EXIT 0: as estatísticas sintéticas coincidem com a R4 anterior; o vínculo antigo e a falsa cláusula `no_pooling` são recusados; `mode=real` é recusado antes da leitura documental.",
        "",
        "[OPEN] A projeção F3.4 e esta camada F3.2 aguardam auditoria c1. Isto é candidato de sandbox no túnel, não pin congelado na Bancada. X13, D-H, d72 e a abertura continuam atos do operador. D-J segue nome pendente na spec; nenhum token final foi cunhado. O mock do fundo livre usa ΛCDM local deslocado e r_d sintético: só testa o encanamento.",
        "",
        "Nenhum dado observado foi aberto; não houve composto real nem mudança do gate. `NOT_FALSIFIED` não é `CONFIRMED`.",
        "",
    ]).encode("utf-8")
    note_name = "NOTA_F32_F34_VINCULO_20261008.md"
    result = {
        "schema": "F32_F34_BINDING_SYNTHETIC_RESULT_V1",
        "unit": "F3.2",
        "status": "ENTREGUE_PARA_AUDITORIA_C1",
        "quadro_f34": {"status": "FECHADA", "evento": 462},
        "scalar_projection": projection,
        "scalar_spec_sha256": spec["spec_sha256"],
        "verdict_function_sha256": spec["spec"]["funcao_de_veredito"]["sha256"],
        "prior_r4_pins_unchanged": old_pins,
        "new_artifacts": new_pins,
        "test_log": new_pins[5],
        "tests": {"count": 6, "exit_code": 0, "synthetic_statistics_equal_prior_r4": True,
                  "old_binding_refused": True, "false_no_pooling_refused": True,
                  "real_mode_refused_before_documentary_read": True},
        "required_sources_admitted": False,
        "v2_frozen": False,
        "real_data_opened": False,
        "real_compound_computed": False,
        "physical_verdict": None,
        "gate_changed": False,
        "remaining_operator_acts": ["X13", "D-H", "d72", "F3.3 abertura"],
        "qualification": "DOCUMENTARY_CANDIDATE_NOT_C1_AUDITED",
    }
    note_pin = {"path": str(HERE / note_name), "sha256": digest(note), "bytes": len(note)}
    result["new_artifacts"].append(note_pin)
    result_name = "RESULTADO_F32_F34_VINCULO_20261008.json"
    result_bytes = pretty(result)
    result_pin = {"path": str(HERE / result_name), "sha256": digest(result_bytes), "bytes": len(result_bytes)}
    entry = [{
        "tipo": "RESULTADO",
        "rota_id": "d1.fase9.f3_2_r1_hash_gate",
        "dominio": "D1_FUNDO_COSMOLOGICO",
        "status": "EM_CURSO",
        "titulo": "F3.2 F3.4: novo vinculo documental da projecao escalar, sem abertura",
        "pergunta": "O gate pode pinar a projecao F3.4 sem converter o candidato em congelamento ou abrir dados?",
        "dados": ["projecao V2 R4+F3.4 por hash", "R4 gate/runner pinados como base", "fixture sintetica R3 pinada"],
        "metodo": "Copia aditiva do gate/preflight/staged R4 com pin interno fixo da projecao F3.4, leitura unica da spec, seis testes sinteticos e recusa de modo real antes da leitura",
        "resultado": "6/6 testes EXIT 0; estatisticas sinteticas iguais as da R4; funcao de veredito preservada; 6 leitores documentais e 2 declarados; vinculo antigo e no_pooling falso recusados; dado real nao aberto",
        "veredito": "F32_F34_DOCUMENTARY_BINDING_SYNTHETIC_ONLY__REAL_MODE_REFUSED__NO_FREEZE_NO_OPENING",
        "estatuto": "REAL documental e sintetico; INPUT decisao F3.4; OPEN auditoria e atos do operador",
        "olhou_dados": False,
        "defeito": "A projecao F3.4 e este novo vinculo ainda nao foram auditados pela c1; nenhuma admissao D-H ou congelamento. O mock de fundo livre testa somente encanamento.",
        "nao_refazer": "Vinculo, gate, runner e evidencias R4 intactos; a nova camada usa os mesmos bytes documentais e fixture, sem novo composto real.",
        "proximo_passo": "c1 auditar o candidato F3.1/F3.2 em conjunto. X13 antecede congelamento; D-H antecede abertura; d72 e abertura sao atos separados do operador.",
        "onde": str(HERE),
        "artefatos": [result_pin["path"], note_pin["path"], new_pins[0]["path"], new_pins[1]["path"], new_pins[2]["path"], new_pins[3]["path"], new_pins[5]["path"]],
        "refs": ["d1.fase9.f3_1_semantica_v1x_leitores"],
        "nota": f"result sha256 {result_pin['sha256']}; binding sha256 {new_pins[0]['sha256']}; projection sha256 {projection['sha256']}; NOT_FALSIFIED nunca e CONFIRMED",
    }]
    map_name = "MAP_ENTRY_F32_F34_VINCULO_20261008.json"
    files = {note_name: note, result_name: result_bytes, map_name: pretty(entry)}
    for name in files:
        if (HERE / name).exists():
            raise FileExistsError(HERE / name)
    for name, data in files.items():
        write_new(HERE / name, data)
    print(json.dumps({"created": {name: digest(data) for name, data in files.items()}}, indent=2))


if __name__ == "__main__":
    main()
