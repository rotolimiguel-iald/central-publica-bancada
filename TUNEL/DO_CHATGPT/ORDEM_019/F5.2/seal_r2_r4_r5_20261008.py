"""Pin the new F5.2 c1 correction artifacts without overwriting prior evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CANDIDATE = ROOT / "CANDIDATO_R2_20261008"
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F4.3_F5.2")
FROZEN = Path(r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\10_frozen_neff_v1.py")
V1 = Path(r"C:\IALD\Bancada_Um\investigacao\preregistro_fase8_primordial\PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json")
INSTALLED = Path(r"C:\IALD\Bancada_Um\bancada\neff_canal.py")


def pin(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def put_new(path: Path, value: dict[str, object]) -> None:
    content = json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    with path.open("xb") as handle:
        handle.write(content)


def main() -> None:
    if (CANDIDATE / "__pycache__").exists():
        raise RuntimeError("residue __pycache__ in candidate")
    if pin(INSTALLED)["sha256"] != "42e9b680855c33004938aacb0899bf0f4ce1921705b04bd93d13ff150ba7541b":
        raise RuntimeError("installed Bancada channel changed")
    if pin(CANDIDATE / "neff_canal.py.bak_20261008_0950")["sha256"] != pin(INSTALLED)["sha256"]:
        raise RuntimeError("candidate's immediate byte backup differs from installed source")
    final_log = (CANDIDATE / "test_candidate_final.log").read_text(encoding="utf-8")
    probe_log = (CANDIDATE / "source_pin_probe_final.log").read_text(encoding="utf-8")
    if "exit_code: 0" not in final_log or "Ran 5 tests" not in final_log or "OK" not in final_log:
        raise RuntimeError("candidate test log is not green")
    if "exit_code: 0" not in probe_log or "be14d2e40592e55b0becd6cb332709e708dc094d8d46cc3c1cf8963b897d93d9" not in probe_log:
        raise RuntimeError("source SHA pin probe did not pass")
    errata = (ROOT / "ERRATA_C1_R2_R4_R5_20261008.md").read_text(encoding="utf-8")
    for required in ("2,81", "2,82", "2,96", "2,99", "DOE e NSF", "[OPEN — X16"):
        if required not in errata:
            raise RuntimeError("errata missing " + required)

    artifact_paths = [
        ROOT / "ERRATA_C1_R2_R4_R5_20261008.md",
        CANDIDATE / "neff_canal.py",
        CANDIDATE / "neff_canal.py.bak_20261008_0950",
        CANDIDATE / "test_candidate.py",
        CANDIDATE / "test_candidate_final.log",
        CANDIDATE / "source_pin_probe_final.log",
    ]
    source_paths = [
        FROZEN, V1, INSTALLED,
        AUDIT / "AUDITORIA_F4_3_F5_2_C1_20261007.md",
        *(AUDIT / "web" / name for name in (
            "2506.20707v1.txt", "2506.20707v2.txt",
            "2506.20707v1.html", "2506.20707v2.html",
            "2503.00636.txt", "2608.07453.txt", "cmb-s4.org.txt",
        )),
    ]
    result = {
        "unidade": "F5.2", "data": "2026-10-08", "status": "CANDIDATO_PARA_AUDITORIA_C1",
        "entrega": "Errata ao lado R2/R4/R5 e canal N_eff em sandbox com Yp BBN e livre; escolha X16 [OPEN]",
        "artefatos": [pin(path) for path in artifact_paths],
        "fontes_lidas": [pin(path) for path in source_paths],
        "testes": {"fail_closed": "5/5; exit 0; Python 3.14.3", "pin_real_da_pagina_v2": "exit 0"},
        "restricoes": [
            "original frozen, V1 Fase 8, um.py e neff_canal.py da Bancada intactos",
            "fonte D8 nao admitida; hipotese Yp depende de X16 do operador",
            "nenhum dado bruto/likelihood aberto; nenhum veredito de natureza; gate inalterado",
        ],
    }
    result_path = ROOT / "RESULTADO_R2_R4_R5_20261008.json"
    put_new(result_path, result)
    map_entry = {
        "tipo": "ERRATA", "rota_id": "neff.frozen_v1_08ago", "corrige": 795,
        "dominio": "FASE8_PRIMORDIAL", "titulo": "F5.2 — auditoria c1 R2/R4/R5: duas linhas Yp, cronologia e ator DOE/NSF",
        "pergunta": "O CMB-SPA do frozen e o calendário citado se sustentam nas fontes primárias pinadas?",
        "dados": ["Tabela 5 SPT-3G D1 v1/v2 e páginas SO/S4 custodiadas por SHA-256", "nenhum dado bruto ou likelihood aberto"],
        "metodo": "Confronto documental e candidato sandbox que exige SHA-256 da página v2; cinco testes fail-closed",
        "resultado": "CMB-SPA v2: 2.82±0.12 com Yp BBN ou 2.96 +0.21/-0.24 com Yp livre; a escolha X16 permanece OPEN. Frozen/V1 usam 2.97±0.12 de combinação inexistente. SO 0.045 vale no levantamento completo 2025–2034; CMB-S4 revisto teria 2033/2042 em cenário histórico, encerrado após decisão DOE/NSF de 09/07/2025.",
        "veredito": "F52_C1_ERRATA_PINNED__YP_CHOICE_OPEN__CANDIDATE_NOT_INSTALLED__NO_GATE_CHANGE",
        "estatuto": "REAL", "status": "EXAMINADA_COM_DEFEITO", "olhou_dados": False,
        "defeito": "A linha CMB-SPA 2.97±0.12 do frozen/V1 e o tens_now derivado não correspondem à Tabela 5 v1/v2; fontes D8 e hipótese Yp X16 pendentes.",
        "nao_refazer": "Não editar frozen, V1, um.py, canal instalado ou refazer Fisher/Nível 2; não abrir dados.",
        "proximo_passo": "c1 audita o candidato; operador decide X16 e D8 antes de qualquer instalação/uso decisório.",
        "onde": str(ROOT),
        "artefatos": [str(ROOT / "ERRATA_C1_R2_R4_R5_20261008.md"), str(CANDIDATE / "neff_canal.py"), str(result_path)],
        "refs": ["cmb.fisher_gates_e_prereg_so_s4_14ago"],
        "nota": "Evidência nova por SHA-256 em RESULTADO_R2_R4_R5_20261008.json; nenhum gate movido.",
    }
    map_path = ROOT / "MAPA_F52_R2_R4_R5_20261008.json"
    put_new(map_path, map_entry)
    print(json.dumps({"resultado": pin(result_path), "mapa_input": pin(map_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
