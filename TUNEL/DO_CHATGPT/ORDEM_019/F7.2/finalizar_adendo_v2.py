"""Seal the additive F7.2 V2 disk receipt and map input from measured files."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile


UNIT = Path(__file__).resolve().parent
STAGE = UNIT / "V2_STAGING"
BANCADA = Path(r"C:\IALD\Bancada_Um")
BACKUP = BANCADA / "mcp_um.py.bak_20261008_063112_484778_UTC"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {"caminho": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def create_once(path: Path, value: dict) -> None:
    if path.exists():
        raise FileExistsError(path)
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False) as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    if temporary.stat().st_size != len(raw):
        raise OSError("temporary result truncated")
    os.replace(temporary, path)
    if path.read_bytes() != raw:
        raise OSError("result mismatch after replace")


def main() -> None:
    stage_receipt = STAGE / "STAGING_RECEIPT_V2.json"
    stage = json.loads(stage_receipt.read_text(encoding="utf-8"))
    if stage["schema"] != "iald.f7_2.v2_staging_receipt.v1" or stage["tests_passed"] != 11:
        raise ValueError("wrong or untested V2 staging receipt")
    for relative, expected in stage["files"].items():
        if sha256(STAGE / relative) != expected:
            raise ValueError(f"staging drift: {relative}")
    live = {
        "channel": artifact(BANCADA / "bancada" / "neutrino_canal_v2.py"),
        "manifest": artifact(BANCADA / "bancada" / "neutrino_fontes_f72_v2.json"),
        "mcp": artifact(BANCADA / "mcp_um.py"),
        "mcp_backup": artifact(BACKUP),
    }
    if live["channel"]["sha256"] != stage["files"]["bancada/neutrino_canal_v2.py"]:
        raise ValueError("live channel differs from staging")
    if live["manifest"]["sha256"] != stage["files"]["bancada/neutrino_fontes_f72_v2.json"]:
        raise ValueError("live manifest differs from staging")
    if live["mcp"]["sha256"] != stage["files"]["mcp_um_v2.py"]:
        raise ValueError("live MCP differs from reviewed proposal")
    if live["mcp_backup"]["sha256"] != stage["v1_unchanged_hashes"]["live_mcp"]:
        raise ValueError("MCP byte backup differs from V1")

    result = {
        "unit": "F7.2",
        "kind": "ADDITIVE_JUNO_V2_DISK_DEPLOYMENT",
        "status": "INSTALLED_ON_DISK_PROCESS_NOT_RELOADED",
        "stage_receipt": artifact(stage_receipt),
        "stage_tests": {"passed": 11, "log": artifact(STAGE / "TESTE_V2.log")},
        "live": live,
        "local_query": {"ok": True, "rows": 13, "primary_pdfs": 10,
                        "overall_verdict": "SEM_LIMITE_TGL", "gate_effect": "NONE",
                        "all_tau_star_limit_s_null": True},
        "source": {"paper": "Beccaria and Ternes, arXiv:2606.13362v1",
                   "url": "https://arxiv.org/html/2606.13362",
                   "pdf": artifact(STAGE / "fontes_primarias" / "Beccaria_Ternes_2026_arxiv_2606.13362v1.pdf"),
                   "published_model_limit_GeV": 4.1e-27,
                   "hypotheses": "Gamma21=Gamma31; Gamma32=0; n=-2; E0=1 GeV; 90% CL"},
        "tgl_tau_star_limit_s": None,
        "mcp_process_reloaded": False,
        "um_py_linked": False,
        "raw_experimental_data_opened": False,
        "gate_changed": False,
        "remaining": ["operator and likelihood map in matter", "MCP reload", "um.py v392",
                      "source migration from tunnel", "c1 re-audit"],
    }
    result_path = UNIT / "RESULTADO_V2.json"
    create_once(result_path, result)

    evidence = [
        result_path, UNIT / "ERRATA_JUNO_2026.md", stage_receipt,
        STAGE / "TABELA_DE_PODER_POR_CANAL_V2.md", STAGE / "TESTE_V2.log",
        STAGE / "JUNO_SOURCE_CUSTODY.json", BANCADA / "bancada" / "neutrino_canal_v2.py",
        BANCADA / "bancada" / "neutrino_fontes_f72_v2.json", BANCADA / "mcp_um.py", BACKUP,
    ]
    map_entry = {
        "tipo": "ANOTACAO",
        "rota_id": "dephasing.f7_2_revisao_fontes_neutrinos_materia",
        "dominio": "DEPHASING",
        "titulo": "F7.2: linha JUNO 2026 e canal V2 instalados em disco, sem recarga MCP",
        "pergunta": "O limite n=-2 dos primeiros dados JUNO foi atualizado com proveniência e sem inferir tau-star TGL?",
        "dados": ["Beccaria–Ternes arXiv:2606.13362v1, PDF pinado por SHA; cenário Gamma21=Gamma31, Gamma32=0",
                  "Canal V2: dez PDFs, treze linhas; V1 e backup MCP preservados", "11 testes offline e consulta local instalada"],
        "metodo": "Adendo à tabela auditada; manifesto versionado pinado, verificação fail-closed, revisão independente, preview e deploy com backup byte a byte e CAS de usuário.",
        "resultado": "Cota publicada gamma<4,1e-27 GeV (90% CL) no modelo do artigo; tau_star_limit_s null em 13/13; canal e MCP V2 instalados em disco; processo MCP não recarregado.",
        "veredito": "F72_V2_JUNO_SOURCE_UPDATED__DISK_INSTALLED__SEM_LIMITE_TGL__MCP_NOT_RELOADED",
        "estatuto": "REAL documental; KNOWN limite do artigo; OPEN ponte TGL",
        "status": "EXAMINADA_COM_DEFEITO",
        "olhou_dados": False,
        "defeito": "Operador/likelihood TGL em matéria ausente; sem cota tau-star. Processo MCP ainda sem recarga; um.py v392 e migração R8 abertos.",
        "nao_refazer": "Não rederivar n=-2, repetir a revisão Kimi ou recalcular as fontes já auditadas.",
        "proximo_passo": "Gerência c1 reaudita V2; recarga MCP em janela segura; ligação um.py v392; pré-registro da ponte TGL antes de inferência física.",
        "onde": str(UNIT),
        "artefatos": [artifact(path) for path in evidence],
        "refs": ["dephasing.neutrinos_n_menos2_junho"],
        "nota": "ORDEM 019 ADENDO 004; a análise JUNO é fenomenológica de Beccaria–Ternes, não limite oficial TGL; gate NONE."
    }
    map_path = UNIT / "MAPA_ADENDO_V2_INPUT.json"
    create_once(map_path, map_entry)
    print(json.dumps({"result": artifact(result_path), "map_input": artifact(map_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
