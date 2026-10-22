"""Prepare the two F3.1/F3.2 route records from the new receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019")
F31 = BASE / "F3.1"
F32 = BASE / "F3.2"
RESULT = F31 / "RESULTADO_V2_R2_F31_F32_20261008.json"
GATE = F32 / "RESULTADO_GATE_V1X_R2_20261008.json"
STAGED = F32 / "RESULTADO_RUNNER_V1X_SINTETICO_R2_20261008.json"
OUT = F31 / "MAP_ENTRY_V2_R2_F31_F32_20261008.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    receipt = json.loads(RESULT.read_bytes())
    assert receipt["v2_frozen"] is False and receipt["real_data_opened"] is False
    rows = [
        {
            "tipo": "RESULTADO", "rota_id": "d1.fase9.f3_1_semantica_v1x_leitores",
            "dominio": "D1_FUNDO_COSMOLOGICO", "status": "ENTREGUE",
            "titulo": "F3.1 V2 R2 gerada por R7 e entregue sem congelar",
            "pergunta": "A V2 R2 incorpora a semântica c1 e mantém a abertura fechada?",
            "dados": ["V1 histórico pinado", "auditoria c1 F3.1/F3.2", "fontes documentais pinadas", "nenhum centro observado reprocessado"],
            "metodo": "Gerador novo e diff V1→V2 por script; grade fixa de covariância e poder só com σ; exame ao lado do mapa H0→TGL; 12+3+7 testes de gate/runner sintético",
            "resultado": "Cinco masers decisórios, seis diagnósticos; pontas adversas GLS; draft JSON/MD e diff reproduzidos; vínculo de bytes e runner sintético ligados; mapa quantitativo H0→TGL ainda OPEN",
            "veredito": "RASCUNHO_V2_R2_NAO_CONGELADO_ENTREGUE_PARA_REAUDITORIA_C1",
            "estatuto": "REAL documental e sintético; OPEN admissão e mapa quantitativo",
            "olhou_dados": False,
            "defeito": "F3.4 e X13 precedem congelamento; D-H precede abertura; D-J nomeia token; fundo livre do runner staged não implementado",
            "nao_refazer": "Preservar V1 e evidências anteriores; nenhuma nova chamada MiMo; não gravar ALVOS_FASE9_LIDOS.json",
            "proximo_passo": "c1 reauditar R2; operador decide F3.4/X13; só então congelar e auditar antes de F3.3",
            "onde": str(F31),
            "artefatos": [str(RESULT), str(F31 / "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008_R2.json"), str(F31 / "DIFF_V1_V2_RASCUNHO_F31_20261008_R2.patch"), str(F31 / "EXAME_MAPA_TGL_H0_R2_20261008.md")],
            "refs": ["d1.fase9.f3_2_r1_hash_gate", "d1.fase9.f3_auditoria_cetica_c1_07out"],
            "nota": f"RESULTADO novo SHA-256 {sha(RESULT)}; spec {receipt['spec_sha256']}; NOT_FALSIFIED nunca é confirmação.",
        },
        {
            "tipo": "RESULTADO", "rota_id": "d1.fase9.f3_2_r1_hash_gate",
            "dominio": "D1_FUNDO_COSMOLOGICO", "status": "EM_CURSO",
            "titulo": "F3.2 vínculo V1.x R2 e runner sintético após auditoria c1",
            "pergunta": "O gate exige bytes e âncoras numéricas corretas antes de qualquer abertura?",
            "dados": ["V2 R2 não congelada", "PDF Pesce e projeção p.6 pinados", "5 fontes com números", "fixture sintético fabricado"],
            "metodo": "Gate V1.x sem official_archive_check do V1; draft lido uma vez; 12 recusas/aceitação e 3 testes de integração; runner estatístico sintético 7/7",
            "resultado": "Seis leitores REAL documental por hash, L1b/L6 DECLARADO; cinco primários verificados; modo real recusado; resultado sintético com verdict=null e data_opened=false",
            "veredito": "CANDIDATO_GATE_RUNNER_V1X_R2_TESTADO_PENDENTE_REAUDITORIA_C1",
            "estatuto": "REAL documental e sintético; sem admissão estatística",
            "olhou_dados": False,
            "defeito": "Fonte L1b/L6 e admissão D-H pendentes; fundo livre e veredito real não implementados; V2 não congelada",
            "nao_refazer": "Gate f9_reader_gate.py original byte a byte intacto; não chamar official_archive_check para certificar V1.x",
            "proximo_passo": "c1 reauditar; completar contrato após F3.4/X13/D-H antes de F3.3",
            "onde": str(F32), "artefatos": [str(GATE), str(STAGED), str(F32 / "VINCULO_DOCUMENTAL_V1X_R2_20261008.json"), str(F32 / "f9_runner_v1x_staged.py")],
            "refs": ["d1.fase9.f3_1_semantica_v1x_leitores"],
            "nota": f"Gate SHA-256 {sha(GATE)}; ensaio sintético SHA-256 {sha(STAGED)}; achados D1 a D6 da seq 696.",
        },
    ]
    raw = (json.dumps(rows, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with OUT.open("xb") as stream:
        stream.write(raw)
    print(json.dumps({"path": str(OUT), "sha256": hashlib.sha256(raw).hexdigest(), "records": len(rows)}))


if __name__ == "__main__":
    main()
