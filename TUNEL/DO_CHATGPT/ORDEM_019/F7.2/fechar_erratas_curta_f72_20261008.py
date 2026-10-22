"""Write additive F7.2 errata and a read-only dependency snapshot.

The script never writes to Bancada_Um or to the pinned scientific sources.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
V2 = ROOT / "V2_STAGING"
V3 = ROOT / "V3_STAGING"
ARTIGO = Path(r"C:\IALD\Artigo\Haja_Luz")
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F7.2")
README = V2 / "README_V2_STAGING.md"
RECEIPT = V2 / "STAGING_RECEIPT_V2.json"
TABLE = V2 / "TABELA_DE_PODER_POR_CANAL_V2.md"
JUNO = V2 / "fontes_primarias" / "Beccaria_Ternes_2026_arxiv_2606.13362v1.pdf"
CUSTODY = V2 / "JUNO_SOURCE_CUSTODY.json"
RATIFICATION = AUDIT / "RECIBO_RATIFICACAO_DEPLOY_V2_C1_20261008.json"


def digest(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def new_file(path: Path, raw: bytes) -> None:
    if path.exists():
        raise FileExistsError(path)
    tmp = path.with_name(path.name + ".tmp_" + os.urandom(4).hex())
    with tmp.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if not raw or len(tmp.read_bytes()) != len(raw):
        raise RuntimeError(f"short write: {path}")
    os.replace(tmp, path)


def new_text(path: Path, value: str) -> None:
    new_file(path, value.encode("utf-8"))


def new_json(path: Path, value: object) -> None:
    new_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def require_hash(path: Path, expected: str) -> None:
    actual = digest(path)["sha256"]
    if actual != expected:
        raise RuntimeError(f"pin differs: {path}: {actual} != {expected}")


def main() -> None:
    require_hash(RECEIPT, "10fc874e65a8cc64fb7cdc28dedd96e927dae0f57a06a683c3a382b75799f183")
    require_hash(README, "6b7442471a77c37c4703fc2567ff3c81669686196406b2776fde042e924e7e72")
    require_hash(TABLE, "f2376aea770e877dd43dead67d186a2da326e4ae7076b2f66574a0d00bccd5fd")
    require_hash(JUNO, "9212cd391d88846ee8065ac3ebf8ccb17be297417a86a22482fca858ed3be107")
    require_hash(CUSTODY, "e612ed7ada21723cd2701a4923fde300c88513f15be3336d00c8f39113777bad")
    require_hash(RATIFICATION, "08541b694268d550a3705a6a17d5d620da745baf6929680f6286952c2f9a79f3")

    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%d_%H%M%S_%f_UTC")
    base = README.read_bytes()
    backup = README.with_name(README.name + ".bak_" + stamp)
    new_file(backup, base)
    if backup.read_bytes() != base:
        raise RuntimeError("README backup differs")
    append = """

## Errata ao lado — 08/10/2026

[REAL — recibo c1 08541b69…] As frases acima «sem implantação», «não foi executado» e «implantação pendente» descrevem o staging original, não o estado posterior. O `--apply` da V2 foi executado sem ato prévio da c1; a gerência ratificou a posteriori a implantação **em disco**. O processo MCP não foi recarregado e não há resultado de invocação da ferramenta V2 em produção. Nenhum `--apply` futuro na Bancada tem autorização implícita.

[REAL — reauditoria c1, mapa seq 841] A cópia posterior de 26 fontes para `Bancada_Um/fontes_externas/F7.2` também ocorreu sem ato da c1. Ela é aditiva e inerte segundo a auditoria, mas sua ratificação ou retirada é decisão pendente da gerência. Este adendo não escreve na Bancada, não instala o canal V3 e não recarrega o MCP.

[KNOWN — Beccaria–Ternes, arXiv:2606.13362v1] Onde o primeiro parágrafo associa a Eq. (6) à §IV.B, leia-se **Eq. (6), §III.B, p. 3 do PDF**. A Eq. (13) está na §IV.B, p. 5; a Tabela I, p. 7. A tabela V2 e seu recibo original seguem pinados; suas erratas ficam nos arquivos vizinhos. O gate permanece intacto.
""".replace("\n", "\r\n").encode("utf-8")
    tmp = README.with_name(README.name + ".tmp_" + os.urandom(4).hex())
    with tmp.open("xb") as stream:
        stream.write(base + append)
        stream.flush()
        os.fsync(stream.fileno())
    if not tmp.read_bytes().startswith(base) or tmp.stat().st_size <= len(base):
        raise RuntimeError("README append verification failed")
    os.replace(tmp, README)

    new_json(V2 / "STAGING_RECEIPT_V2_ERRATA_AO_LADO_20261008.json", {
        "schema": "iald.f7_2.v2_receipt_adjacent_errata.v1",
        "unit": "F7.2",
        "created_utc": now.isoformat(),
        "historical_receipt": {"path": str(RECEIPT), **digest(RECEIPT)},
        "historical_status_STAGED_NOT_DEPLOYED": "true when receipt was created; false for the later disk state",
        "disk_deploy_v2": "ratified_after_the_fact_by_c1",
        "c1_ratification": {"path": str(RATIFICATION), **digest(RATIFICATION)},
        "mcp_process_reloaded": False,
        "v3_source_copy": "26 files copied later without c1 act; c1 decision pending",
        "future_apply_rule": "explicit c1 act required",
        "readme_before": {"path": str(backup), **digest(backup)},
        "readme_after": {"path": str(README), **digest(README)},
        "table_and_custody_untouched": True,
        "gate_effect": "NONE",
    })

    new_text(V2 / "ERRATA_CABECALHO_TABELA_V2_20261008.md", """# Errata ao lado do cabeçalho da tabela V2 — F7.2

[REAL] A `TABELA_DE_PODER_POR_CANAL_V2.md` mantém os bytes e o SHA do recibo original. A expressão «preparada em sandbox» no cabeçalho descreve a produção da tabela, não o estado do canal. A V2 foi instalada em disco sem ato prévio e ratificada a posteriori pela c1 (recibo `08541b69…`); o processo MCP não foi recarregado.

[KNOWN] A âncora da Eq. (6) de Beccaria–Ternes é §III.B, p. 3 do PDF, enquanto a Eq. (13) é §IV.B, p. 5, e a Tabela I está na p. 7. O limite publicado é `γ21 = γ31 < 4,1 × 10⁻²⁷ GeV`, `n = −2`, `E0 = 1 GeV`, 90% CL, no cenário do artigo. Nenhuma cota `τ★` da TGL é extraída. Esta errata não muda os valores da tabela, o canal ou o gate.
""")

    new_text(ROOT / "ERRATA_ANCORAS_JUNO_REF72_E_ESTADO_F72_20261008.md", """# F7.2 — âncoras JUNO, referência [72] e estado da Bancada

[KNOWN] No PDF de Beccaria–Ternes, arXiv:2606.13362v1, a Eq. (6) está em §III.B, p. 3; define o fator `γij L (E/E0)^n` com `E0 = 1 GeV`. A Eq. (13), em §IV.B, p. 5, e a Tabela I, p. 7, dão `γ21 = γ31 < 4,1 × 10⁻²⁷ GeV`, `n = −2`, a 90% CL. A indicação «§IV.2» na nota de literatura é a numeração HTML da seção que aparece como **§IV.B** no PDF; ela não localiza a Eq. (6). Esta errata vale também para a tabela V3 pinada e sua cópia na Bancada; nenhuma das duas foi alterada.

[KNOWN] A referência [72] do artigo JUNO, Esteban, Gago, Gonzalez-Garcia e Zapata, arXiv:2605.13955v1 (13/05/2026), trata de atenuação/perda de fluxo de neutrinos astrofísicos difusos (`ν-loss`). Para `n = −2`, `E0 = 1 GeV`, a Tabela 1 fornece limites de `γ0` para hipóteses de fontes e atenuação; esse parâmetro não é o `γ21 = γ31` de dephasing do JUNO. O artigo é anterior a junho e entra como contexto de modelo, não como atualização posterior nem como substituto do limite JUNO. O SN1987A de arXiv:2503.04573v1 também testa `ν-loss` em outra família.

[REAL — busca delimitada] A varredura de literatura posterior a junho encontrou arXiv:2608.25069 (recast ALP, amortecimento líder `L² E⁰`) e arXiv:2609.37895 (análise JUNO de parâmetros padrão, sem ajuste `γ` para `n = −2` no resumo). Nesta busca não apareceu uma cota publicada diretamente comparável que substitua Beccaria–Ternes; isso não prova inexistência. Fontes primárias: https://arxiv.org/pdf/2606.13362 ; https://arxiv.org/html/2605.13955v1 ; https://arxiv.org/pdf/2503.04573v1 ; https://arxiv.org/abs/2608.25069 ; https://arxiv.org/abs/2609.37895 .

[REAL — processo] A c1 ratificou a posteriori apenas a implantação V2 em disco. A cópia subsequente de 26 fontes para `Bancada_Um/fontes_externas/F7.2` ocorreu sem ato da c1, conforme reauditoria seq 841. A decisão de ratificar ou retirar essas cópias segue com a gerência. O canal V3 permanece no staging; MCP não recarregado. Nenhum novo arquivo foi escrito na Bancada por esta camada.
""")

    new_text(V3 / "ERRATA_TABELA_V3_ANCORA_E_ESTADO_20261008.md", """# Errata ao lado da tabela V3 pinada

[KNOWN] Onde o cabeçalho de `fontes_externas/F7.2/documents/TABELA_DE_PODER_POR_CANAL_V3.md` diz «Eq. (6), §IV.B», leia-se «Eq. (6), §III.B, p. 3 do PDF». A Eq. (13) é §IV.B, p. 5, e a Tabela I é p. 7. Onde a nota de literatura diz «§IV.2», essa é a numeração HTML da §IV.B do PDF.

[REAL] Onde a tabela V3 herdou «esta tabela V2 foi preparada em sandbox», leia-se: tabela V3 gerada e pinada em staging; a cópia de suas fontes na Bancada ocorreu sem ato da c1 e aguarda decisão dela. O módulo e manifesto V3 não foram instalados, e o processo MCP não foi recarregado. A errata ao lado da cópia na Bancada depende de ato específico da c1. Nenhum byte da tabela pinada foi alterado aqui.
""")

    frozen = [TABLE, CUSTODY, JUNO, ROOT / "REAPROVEITAMENTO_E_ERRATA.md",
              ROOT / "PARECER_KIMI_CONFERIDO.md", ROOT / "MATTER_SOURCE_CUSTODY_VALIDATION.json",
              V3 / "fontes_externas" / "F7.2" / "documents" / "v369_um_absoluto.json"]
    frozen.extend(sorted((ROOT / "fontes_primarias").iterdir()))
    v3_manifest = json.loads((V3 / "bancada" / "neutrino_fontes_f72_v3.json").read_text(encoding="utf-8"))
    script_checks = []
    for script in v3_manifest["scripts"]:
        path = ARTIGO / script["name"]
        meta = digest(path)
        if meta != {"sha256": script["sha256"], "bytes": script["bytes"]}:
            raise RuntimeError(f"June script differs from V3 pin: {path}")
        frozen.append(path)
        script_checks.append(str(path))
    entries = [{"path": str(path), **digest(path)} for path in frozen]
    new_json(ROOT / "FREEZE_DEPENDENCIAS_V2_F72_20261008.json", {
        "schema": "iald.f7_2.frozen_dependencies.v1",
        "created_utc": now.isoformat(),
        "unit": "F7.2",
        "scope": "read-only snapshot; no protected dependency modified",
        "registered_v2_pin_checks": "receipt, V2 table, JUNO PDF and JUNO custody matched before writing errata",
        "june_scripts_checked_against_v3_manifest": script_checks,
        "files": entries,
    })

    print(json.dumps({
        "readme_before": digest(backup),
        "readme_after": digest(README),
        "backup": str(backup),
        "receipt_unchanged": digest(RECEIPT),
        "table_unchanged": digest(TABLE),
        "frozen_count": len(entries),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
