"""Create new F7.2 c1-correction evidence and a separate map input."""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path

UNIT = Path(__file__).resolve().parent
STAGE = UNIT / "V3_STAGING"
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F7.2")
ORIGINAL = Path(r"C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py")
RESULT = UNIT / "RESULTADO_CORRECOES_C1_F72_20261008.json"
MAP_INPUT = UNIT / "MAPA_CORRECOES_C1_F72_20261008_INPUT.json"
README = UNIT / "STAGING" / "README_DEPLOY.md"
README_BACKUP = UNIT / "STAGING" / "README_DEPLOY.md.bak_20261008_110943_832789_UTC"


def art(path: Path) -> dict:
    raw = path.read_bytes()
    return {"caminho": str(path), "sha256": sha256(raw).hexdigest(), "bytes": len(raw)}


def write_new(path: Path, value: dict) -> dict:
    encoded = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())
    assert path.read_bytes() == encoded
    return art(path)


def main() -> None:
    if RESULT.exists() or MAP_INPUT.exists():
        raise RuntimeError("result or map input already exists; do not overwrite evidence")
    staging = json.loads((STAGE / "STAGING_RECEIPT_V3.json").read_text(encoding="utf-8"))
    validation = json.loads((STAGE / "VALIDACAO_V3_CENTRAL.json").read_text(encoding="utf-8"))
    migration = json.loads((UNIT / "SOURCE_MIGRATION_RECEIPT_V3.json").read_text(encoding="utf-8"))
    assert staging["source_counts"] == {"scripts": 6, "primary_pdfs": 10, "documents": 8, "context_docs": 1, "context_pdfs": 1}
    assert validation["status"] == "PASS" and validation["rows"] == 13 and validation["source_files_verified"] == 26
    assert validation["tampered_manifest_rejected"] and validation["tampered_script_rejected"]
    assert validation["all_tau_star_null"] and validation["gate_effect"] == "NONE"
    assert migration["file_count"] == 26 and len(migration["files"]) == 26
    assert migration["channel_or_manifest_installed"] is False and migration["mcp_touched_or_reloaded"] is False
    assert all(row["source"]["sha256"] == row["destination"]["sha256"] for row in migration["files"])
    original = ORIGINAL.read_bytes()
    assert b"'tau_star_bound_neutrino_s': 7.8e-10" in original
    before = README_BACKUP.read_bytes()
    after = README.read_bytes()
    assert before.count(b"\x0b") == 1 and b"\x0b" not in after
    assert before.replace(b"project_fisica\x0b369_um_absoluto.json", b"project_fisica\\v369_um_absoluto.json") == after
    artifacts = [
        UNIT / "LITERATURA_POS_JUNHO_F7_2_20261008.md",
        UNIT / "fontes_literatura_r1" / "Ternes_Pagliaroli_Villante_2025_arxiv_2503.04573v1.pdf",
        UNIT / "EVIDENCIA_R2_R3_V369_ORDENS_20261008_V2.md",
        UNIT / "EVIDENCIA_R2_R3_V369_ORDENS_20261008.json",
        UNIT / "ERRATA_LITERAL_J4B_F72_20261008.md",
        UNIT / "ERRATA_TABELA_V3_ESTADO_20261008.md",
        UNIT / "V2_STAGING" / "TABELA_DE_PODER_POR_CANAL_V2.md",
        STAGE / "fontes_externas" / "F7.2" / "documents" / "TABELA_DE_PODER_POR_CANAL_V3.md",
        STAGE / "bancada" / "neutrino_canal_v3.py",
        STAGE / "bancada" / "neutrino_fontes_f72_v3.json",
        STAGE / "STAGING_RECEIPT_V3.json",
        STAGE / "VALIDACAO_V3_CENTRAL.json",
        UNIT / "SOURCE_MIGRATION_RECEIPT_V3.json",
        README,
        README_BACKUP,
        AUDIT / "AUDITORIA_F7_2_C1_RELATORIO_aed6e453.md",
        AUDIT / "AUDITORIA_F7_2_C1_20261007.md",
        ORIGINAL,
    ]
    pinned = [art(path) for path in artifacts]
    result = {
        "schema": "iald.f7_2.c1_corrections.v1",
        "unit": "F7.2",
        "time_utc": datetime.now(timezone.utc).isoformat(),
        "status": "ENTREGUE_PARA_REAUDITORIA_C1",
        "nos_vivo_consultado": True,
        "already_present": "V2 on disk: JUNO 4.1e-27 GeV (n=-2, E0=1 GeV, 90% CL), corrected R4 PDF anchors and R5 statuses, 13 rows, all tau-star null; c1 ratified V2 on 2026-10-08 after noting the earlier unauthorized deploy.",
        "R1": {"deeper_search": True, "juno_already_in_v2": True, "sn1987a": "nu-loss contextual model, not a dephasing replacement", "published_limits_statute": "KNOWN"},
        "R2_R3": {"sr_deficit_orders": 12.457634837, "mossbauer_bound_orders": 9.269626166, "mossbauer_power": "OPEN_NO_SIGMA_EXCESS_OR_Z", "neutrino_conditional_range_orders": [38.07, 45.82], "juno_conditional_orders": 39.77, "assumptions": "tau_star=t_P; Kfac=1; vacuum; no operator/likelihood map; not a TGL bound"},
        "R4_R5": "Already corrected in V2 table and channel; V3 preserves these readings.",
        "R6": "June tgl_paper_unified.py line 18393 is literal 7.8e-10, not calculated; original unchanged; errata beside it for the map.",
        "R8": {"source_files_copied": 26, "destination": r"C:\IALD\Bancada_Um\fontes_externas\F7.2", "v3_manifest_pin": staging["manifest_sha256_locked"], "v3_channel_staged_only": True, "existing_bancada_files_unchanged": True, "c1_installation_review_pending": True},
        "R9": {"old_sha256": sha256(before).hexdigest(), "new_sha256": sha256(after).hexdigest(), "backup_identical_to_old": True, "VT_replaced_with_literal_backslash_v": True},
        "audit_reference_anomaly": {"path_in_request_is_python_script": True, "effective_report": "AUDITORIA_F7_2_C1_RELATORIO_aed6e453.md", "both_hashes_measured": True},
        "scope": {"mcp_process_reloaded": False, "mcp_or_existing_channels_touched_in_this_correction": False, "um_py_linked": False, "raw_experimental_data_opened": False, "gate_effect": "NONE", "tau_star_limit_s": None},
        "artifacts": pinned,
    }
    result_art = write_new(RESULT, result)
    map_entry = {
        "tipo": "ANOTACAO",
        "rota_id": "dephasing.f7_2_revisao_fontes_neutrinos_materia",
        "dominio": "DEPHASING",
        "titulo": "F7.2: ressalvas c1 R1-R6/R8/R9 tratadas; 26 fontes copiadas, V3 pinada em staging",
        "pergunta": "O adendo F7.2 incorpora o limite JUNO, lê a v369 inteira e preserva a proveniência sem inferir cota TGL?",
        "dados": ["V2 JUNO/R4/R5 já existente e ratificada pela c1", "R1 busca posterior com SN1987A tipado como nu-loss", "R2/R3 chaves v369 e contas condicionais", "R6 literal J.4b l.18393", "R8 bundle 26 fontes com pino V3", "R9 correção 0x0b com backup"],
        "metodo": "Nós Vivo consultado; PDFs/fontes primárias e core lidos, cálculos com hipóteses nomeadas; V3 validada em staging com recusa de adulteração; cópia aditiva 26/26 por SHA-256 e comparação byte a byte dos arquivos protegidos da Bancada.",
        "resultado": "JUNO 4,1e-27 GeV em seu modelo n=-2 já na V2; SN1987A é nu-loss distinto. Sr 12,46 ordens, Mössbauer nominal 9,27, neutrinos condicionais 38,07–45,82. Original de junho intacto; README corrigido com backup; 26 fontes em Bancada_Um/fontes_externas/F7.2. Módulo/manifesto V3 preparados, ainda não instalados.",
        "veredito": "F72_CORRECOES_C1_ENTREGUES__FONTES_V3_COPIADAS__CANAL_V3_STAGING__SEM_LIMITE_TGL__GATE_NONE",
        "estatuto": "REAL documental; KNOWN limites publicados; DERIVED contas condicionais; OPEN ponte operador/canal",
        "status": "EXAMINADA_COM_DEFEITO",
        "olhou_dados": False,
        "defeito": "Canal e manifesto V3 aguardam conferência/ato c1 para instalação; processo MCP não foi recarregado; um.py v392 é da gerência; sem operador TGL em matéria ou omega/visibilidade para franjas. A referência de auditoria citada pelo pedido aponta script Python; relatório real pinado em arquivo distinto.",
        "nao_refazer": "Não repetir os 14 números da auditoria V1, a linha JUNO V2, o parecer Kimi ou as 11 provas V2. Não converter cotas de modelos distintos em tau-star.",
        "proximo_passo": "c1 confere recibos e decide instalação V3; gerência trata recarga MCP e ligação um.py v392. A ponte física segue aberta e exige pré-registro antes de veredito de natureza.",
        "onde": str(UNIT),
        "artefatos": [result_art] + [x for x in pinned if Path(x["caminho"]).name in {"LITERATURA_POS_JUNHO_F7_2_20261008.md", "EVIDENCIA_R2_R3_V369_ORDENS_20261008_V2.md", "ERRATA_LITERAL_J4B_F72_20261008.md", "STAGING_RECEIPT_V3.json", "VALIDACAO_V3_CENTRAL.json", "SOURCE_MIGRATION_RECEIPT_V3.json", "README_DEPLOY.md", "README_DEPLOY.md.bak_20261008_110943_832789_UTC"}],
        "refs": ["dephasing.neutrinos_n_menos2_junho"],
        "nota": "Ressalvas corrigidas ao lado; V2 ratificada a posteriori pela c1, V3 apenas preparada. NOT_FALSIFIED não é creditação. O número corrige a frase.",
    }
    map_art = write_new(MAP_INPUT, map_entry)
    print(json.dumps({"result": result_art, "map_input": map_art, "artifact_count": len(pinned)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
