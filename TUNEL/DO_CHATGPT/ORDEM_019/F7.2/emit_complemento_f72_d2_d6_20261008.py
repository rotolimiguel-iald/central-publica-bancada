"""Emit the additive F7.2 D2-D6 correction without touching pinned sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader


BASE = Path(__file__).resolve().parent
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F7.2")
BANCADA = Path(r"C:\IALD\Bancada_Um\fontes_externas\F7.2")
REF72 = BASE / "fontes_literatura_r1" / "Esteban_Gago_GonzalezGarcia_Zapata_2026_arxiv_2605.13955v1.pdf"
JUNO = BASE / "V2_STAGING" / "fontes_primarias" / "Beccaria_Ternes_2026_arxiv_2606.13362v1.pdf"
TABLE = BASE / "V3_STAGING" / "fontes_externas" / "F7.2" / "documents" / "TABELA_DE_PODER_POR_CANAL_V3.md"
TABLE_COPY = BANCADA / "documents" / "TABELA_DE_PODER_POR_CANAL_V3.md"
RATIFICATION = AUDIT / "RECIBO_RATIFICACAO_COPIA_R8_C1_20261008.json"
ERRATA = BASE / "ERRATA_COMPLEMENTAR_D2_D6_C1_F72_20261008.md"
CUSTODY = BASE / "fontes_literatura_r1" / "REF72_CUSTODY_F72_20261008.json"
MANIFEST = BASE / "V3_STAGING" / "MANIFESTO_ERRATA_TABELA_V3_D5_20261008.json"
RESULT = BASE / "RESULTADO_COMPLEMENTO_D2_D6_F72_20261008.json"


def digest(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def write_new(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if path.read_bytes() != raw:
        raise RuntimeError(f"Byte verification failed: {path}")


def as_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def preflight() -> dict[str, object]:
    assert TABLE.read_bytes() == TABLE_COPY.read_bytes(), "V3 staging/Bancada copy diverged"
    ratification = json.loads(RATIFICATION.read_text(encoding="utf-8"))
    assert ratification["n_arquivos"] == 26
    assert "RATIFICACAO A POSTERIORI" in ratification["ato"]
    assert ratification["arquivos"]["documents\\TABELA_DE_PODER_POR_CANAL_V3.md"]["sha256"] == digest(TABLE)["sha256"]
    pdf = PdfReader(str(REF72))
    juno = PdfReader(str(JUNO))
    ref72_first = pdf.pages[0].extract_text() or ""
    ref72_table = pdf.pages[7].extract_text() or ""
    juno_refs = juno.pages[9].extract_text() or ""
    assert len(pdf.pages) == 14
    assert "Exploring neutrino loss with diffuse astrophysical neutrino fluxes" in ref72_first
    assert "TABLE I." in ref72_table and "IceCube 7.5-year HESE" in ref72_table
    assert "[72]" in juno_refs and "2605.13955" in juno_refs
    assert "esta tabela V2 foi preparada em sandbox" in TABLE.read_text(encoding="utf-8")
    assert "mensagem do operador" in (BASE / "LITERATURA_POS_JUNHO_F7_2_20261008.md").read_text(encoding="utf-8")
    assert "§III.B" in (BASE / "V3_STAGING" / "ERRATA_TABELA_V3_ANCORA_E_ESTADO_20261008.md").read_text(encoding="utf-8")
    assert "ratificou a posteriori" in (BASE / "V2_STAGING" / "README_V2_STAGING.md").read_text(encoding="utf-8")
    return {"ref72_pages": len(pdf.pages), "juno_ref72_pdf_page": 10, "ref72_table_pdf_page": 8}


def emit() -> None:
    checks = preflight()
    now = datetime.now(timezone.utc).isoformat()
    ref72_sha = digest(REF72)["sha256"]
    table_sha = digest(TABLE)["sha256"]
    receipt_sha = digest(RATIFICATION)["sha256"]

    custody = {
        "schema": "iald.f7_2.ref72_custody.v1",
        "created_utc": now,
        "status": "REAL_LOCAL_PDF_CUSTODY__KNOWN_PUBLISHED_CONTENT__NO_TGL_LIMIT",
        "source_url": "https://arxiv.org/pdf/2605.13955v1",
        "source_abstract_url": "https://arxiv.org/abs/2605.13955",
        "source_title": "Exploring neutrino loss with diffuse astrophysical neutrino fluxes",
        "authors": ["Ivan Esteban", "Alberto M. Gago", "M. C. Gonzalez-Garcia", "Gabriel D. Zapata"],
        "submitted": "2026-05-13",
        "pdf": digest(REF72),
        "inspection": {
            "pdf_pages": checks["ref72_pages"],
            "pdf_page_8": "Table I: IceCube 7.5-year HESE, gamma_0 attenuation limits by n and source scenario; 95% CL",
            "juno_pdf_page_10": "Reference [72] names all four authors and arXiv:2605.13955",
        },
        "model_boundary": "neutrino flux loss/attenuation; not JUNO pure dephasing gamma_21=gamma_31; tau_star_limit_s=null",
        "no_raw_data_opened": True,
        "no_gate_change": True,
    }
    write_new(CUSTODY, as_json(custody))

    errata = f"""# F7.2 — complemento aditivo D2–D6 da c1

[REAL documental, 08/10/2026] O Nós vivo (`consultar.py --unidade F7.2`) localiza a tabela por canal, o canal de neutrinos de junho (`n = −2`) e a v369 de relógios. A auditoria c1 `AUDITORIA_F7_2_C1_a91f9500.md` conferiu os 17 pinos da camada anterior e classificou D2 e D3 como feitos, D4 como apenas textual, D5 como parcial e D6 como pendente. Este complemento mantém os originais pinados.

## D2 — V2 já corrigida ao lado

[REAL] A leitura vigente do `V2_STAGING/README_V2_STAGING.md`, de `V2_STAGING/STAGING_RECEIPT_V2_ERRATA_AO_LADO_20261008.json` e de `V2_STAGING/ERRATA_CABECALHO_TABELA_V2_20261008.md` corrige o estado histórico «implantação pendente»: a V2 foi instalada em disco sem ato prévio e ratificada a posteriori pela c1. A tabela V2 e o recibo V2 originais seguem pinados. O MCP não foi recarregado.

## D3 — âncora da Eq. (6)

[KNOWN — Beccaria–Ternes, arXiv:2606.13362v1] A Eq. (6) está em §III.B, p. 3 do PDF. A Eq. (13) está em §IV.B, p. 5, e a Tabela I na p. 7. A numeração «§IV.2» na LITERATURA é a da versão HTML e se refere à seção dos resultados, não à Eq. (6). `V3_STAGING/ERRATA_TABELA_V3_ANCORA_E_ESTADO_20261008.md` e `ERRATA_ANCORAS_JUNO_REF72_E_ESTADO_F72_20261008.md` já trazem essa leitura. A tabela V3 e a cópia na Bancada mantêm os bytes `sha256={table_sha}`.

## D4 — referência [72] sob custódia

[REAL — custódia local; KNOWN — conteúdo da fonte] O PDF do artigo JUNO cita na referência [72], p. 10, Esteban, Gago, Gonzalez-Garcia e Zapata, *Exploring neutrino loss with diffuse astrophysical neutrino fluxes*, arXiv:2605.13955. O PDF público v1 do arXiv, submetido em 13/05/2026, foi guardado em `fontes_literatura_r1/` com `sha256={ref72_sha}`; o recibo é `REF72_CUSTODY_F72_20261008.json`. A Tabela I, p. 8, trata da atenuação de fluxo em IceCube HESE sob escolhas de fonte e energia. Esse `γ₀` de perda de neutrinos não é o `γ₂₁ = γ₃₁` de dephasing sem perda da linha JUNO. Não se infere limite de `τ★` da TGL; `τ★_limite = null` [OPEN].

## D5 — tabela V3 e manifesto em staging

[REAL] Onde a tabela V3 herdou «esta tabela V2 foi preparada em sandbox», leia-se: **a tabela V3 foi preparada em staging; as 26 fontes foram copiadas para a Bancada e ratificadas a posteriori pela c1; o canal V3 segue sem instalação e sem recarga do MCP**. O alvo pinado e esta correção estão ligados por `V3_STAGING/MANIFESTO_ERRATA_TABELA_V3_D5_20261008.json`, que permanece em staging. A ratificação consta em `RECIBO_RATIFICACAO_COPIA_R8_C1_20261008.json`, `sha256={receipt_sha}`. A cópia R8 foi aditiva e inerte na aferição c1; isso não autoriza nova gravação na Bancada.

## D6 — autoria da mensagem

[REAL documental] No parágrafo «Anomalia de referência» de `LITERATURA_POS_JUNHO_F7_2_20261008.md` e de sua cópia V3, onde se lê «mensagem do operador», leia-se **despacho da gerência c1 ao Codex**. A indicação do caminho `AUDITORIA_F7_2_C1_20261007.md` veio da c1; o relatório efetivamente lido tem sufixo `aed6e453`. Não atribuir ao operador o texto da gerência.

## Estado operacional e escrituração

[REAL — decisão c1] A frase da camada anterior de que a ratificação da cópia R8 «segue pendente» foi superada pelo evento 313 e pelo recibo c1 acima. Vale esta errata para `V2_STAGING/README_V2_STAGING.md`, `V2_STAGING/STAGING_RECEIPT_V2_ERRATA_AO_LADO_20261008.json`, `ERRATA_TABELA_V3_ESTADO_20261008.md`, `ERRATA_ANCORAS_JUNO_REF72_E_ESTADO_F72_20261008.md` e o registro histórico do mapa seq 850. O mapa e as superfícies de memória requerem lançamento próprio ao lado pela gerência da unidade; este arquivo não os altera.

[REAL — limite] Esta camada só cria arquivos no túnel. A tabela V3 pinada, a cópia na Bancada, os módulos, o MCP, `um.py`, os scripts de junho e o gate não foram alterados. Os resultados de modelos externos não são confirmação física.
"""
    write_new(ERRATA, errata.encode("utf-8"))

    manifest = {
        "schema": "iald.f7_2.v3_table_errata_manifest.v1",
        "created_utc": now,
        "status": "STAGING_ONLY__C1_REVIEW_PENDING__NO_BANCADA_WRITE",
        "target": digest(TABLE),
        "inert_bancada_copy_read_only": digest(TABLE_COPY),
        "c1_ratification_receipt": digest(RATIFICATION),
        "errata_current": digest(ERRATA),
        "errata_previous_v3": digest(BASE / "V3_STAGING" / "ERRATA_TABELA_V3_ANCORA_E_ESTADO_20261008.md"),
        "source_ref72_custody": digest(CUSTODY),
        "corrections": {
            "inherited_v2_sentence": "V3 prepared in staging; 26 sources copied and ratified by c1; V3 channel not installed or MCP reloaded",
            "juno_eq6": "Sec. III.B, PDF p. 3",
            "juno_eq13": "Sec. IV.B, PDF p. 5",
            "juno_table_i": "PDF p. 7",
            "literature_authority": "c1 management dispatch, not operator message",
        },
        "allowed_action": "Review this manifest and errata; no install, no MCP reload, no gate change",
    }
    write_new(MANIFEST, as_json(manifest))

    result = {
        "schema": "iald.f7_2.d2_d6_complement.v1",
        "created_utc": now,
        "unit": "F7.2",
        "claim_event": 372,
        "scope": "D2 and D3 existing erratas cited; D4 PDF custody; D5 new staging manifest; D6 attribution; c1 R8 ratification state",
        "artifacts_new": [digest(p) for p in (REF72, CUSTODY, ERRATA, MANIFEST)],
        "pinned_unchanged": [digest(p) for p in (TABLE, TABLE_COPY, RATIFICATION,
            BASE / "V2_STAGING" / "STAGING_RECEIPT_V2.json",
            BASE / "V2_STAGING" / "TABELA_DE_PODER_POR_CANAL_V2.md",
            BASE / "LITERATURA_POS_JUNHO_F7_2_20261008.md")],
        "checks": checks,
        "no_bancada_write": True,
        "no_mcp_reload": True,
        "no_gate_change": True,
        "no_raw_data_opened": True,
        "c1_audit_pending": True,
    }
    write_new(RESULT, as_json(result))
    print(json.dumps({"result": digest(RESULT), "artifacts_new": result["artifacts_new"]}, ensure_ascii=False, indent=2))


def check_only() -> None:
    preflight()
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    for item in result["artifacts_new"] + result["pinned_unchanged"]:
        actual = digest(Path(item["path"]))
        assert actual["sha256"] == item["sha256"] and actual["bytes"] == item["bytes"]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["target"]["sha256"] == digest(TABLE)["sha256"]
    assert manifest["inert_bancada_copy_read_only"]["sha256"] == digest(TABLE)["sha256"]
    print(json.dumps({"status": "PASS", "artifacts_new": len(result["artifacts_new"]), "pinned_unchanged": len(result["pinned_unchanged"]), "result": digest(RESULT)}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    check_only() if args.check_only else emit()
