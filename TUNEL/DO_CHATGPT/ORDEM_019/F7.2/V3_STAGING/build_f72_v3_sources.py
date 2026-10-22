# -*- coding: utf-8 -*-
"""Stage an additive, relocatable F7.2 V3 source bundle. Never install it."""

from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
UNIT = HERE.parent
V2 = UNIT / "V2_STAGING"
V2_MANIFEST = V2 / "bancada" / "neutrino_fontes_f72_v2.json"
V2_CHANNEL = V2 / "bancada" / "neutrino_canal_v2.py"
R2_R3_JSON = UNIT / "EVIDENCIA_R2_R3_V369_ORDENS_20261008.json"
R1_MD = UNIT / "LITERATURA_POS_JUNHO_F7_2_20261008.md"
SN_PDF = UNIT / "fontes_literatura_r1" / "Ternes_Pagliaroli_Villante_2025_arxiv_2503.04573v1.pdf"
V2_MANIFEST_PIN = "b7beff016f070ba8bb4aa40866d512c885e9d2197703954cfad05137bfb29131"
V2_CHANNEL_PIN = "252de897ee9e43944cffc9adebe38da14aba6c2736e4cbb56e472f000ad159e5"
R2_R3_PIN = "5b7ccb4398f68cd34395a13688f97c0093a26632fce4536a4c4ebbf2392f4e62"
R1_PIN = "5bc58efc65a3c0f6c77e0c62e89da85782d51ed2a234fbad7bada484a2e7ddc2"
SN_PIN = "0510c49b7ff44a6b59aecde26faa972d6889606e72b5f66993198fc0740ea026"
ROOT = HERE / "fontes_externas" / "F7.2"
MODULE = HERE / "bancada" / "neutrino_canal_v3.py"
MANIFEST = HERE / "bancada" / "neutrino_fontes_f72_v3.json"
TABLE = ROOT / "documents" / "TABELA_DE_PODER_POR_CANAL_V3.md"
RECEIPT = HERE / "STAGING_RECEIPT_V3.json"
README = HERE / "README_V3_STAGING.md"

SCRIPT_NAMES = (
    "tgl_neutrino_decoherence.py", "tgl_neutrino_exponent_test.py",
    "tgl_dephasing_falsifier.py", "tgl_decoherence_contour.py",
    "tgl_dephasing_systems.py", "tgl_paper_unified.py",
)
DOC_FILENAMES = {
    "local_review_note": "REAPROVEITAMENTO_E_ERRATA.md",
    "local_confronted_review": "PARECER_KIMI_CONFERIDO.md",
    "channel_power_table": "TABELA_DE_PODER_POR_CANAL_V3.md",
    "juno_custody_v2": "JUNO_SOURCE_CUSTODY.json",
    "matter_validation": "MATTER_SOURCE_CUSTODY_VALIDATION.json",
    "neutrino_custody": "SOURCE_CUSTODY.json",
    "matter_custody": "MATTER_SOURCE_CUSTODY.json",
    "clock_v369_result": "v369_um_absoluto.json",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_pinned(path: Path, digest: str) -> bytes:
    data = path.read_bytes()
    if sha(data) != digest:
        raise ValueError(f"source pin differs: {path}")
    return data


def write_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(f"refusing overwrite: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp_{os.getpid()}")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if tmp.stat().st_size != len(data) or not data:
            raise OSError(f"bad temporary size: {path}")
        os.rename(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def read_entry(entry: dict, *, pdf: bool = False, python: bool = False) -> bytes:
    path = Path(entry["path"])
    data = path.read_bytes()
    if not data or sha(data) != entry["sha256"] or len(data) != entry["bytes"]:
        raise ValueError(f"V2 entry bytes/pin differ: {path}")
    if pdf and (not data.startswith(b"%PDF-") or len(data) < 1000):
        raise ValueError(f"invalid PDF header/size: {path}")
    if python:
        ast.parse(data.decode("utf-8-sig"), filename=str(path))
    return data


def replace_one(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"template replacement count is {text.count(old)}: {old[:80]!r}")
    return text.replace(old, new)


def replace_span(text: str, first: str, following: str, new: str) -> str:
    start = text.index(first)
    end = text.index(following, start)
    return text[:start] + new + text[end:]


def make_table(v2_text: str, evidence: dict) -> bytes:
    p1 = evidence["core_r2"]
    sr = evidence["sr87_requirement"]
    zn = evidence["zn67_matter"]
    juno = evidence["juno_G21_component_orders"]
    span = evidence["neutrino_range_orders"]
    text = replace_one(
        v2_text,
        "# F7.2 V2 — tabela de poder por canal, com análise Beccaria–Ternes dos primeiros dados JUNO",
        "# F7.2 V3 — tabela de poder por canal, fontes locais na Bancada",
    )
    text = replace_one(
        text,
        "**Estado:** [REAL — V2 em sandbox, fontes e hashes conferidos em 08/10/2026; implantação pendente da gerência].",
        "**Estado:** [REAL — V3 preparada em staging, fontes e hashes conferidos em 08/10/2026; implantação do canal pendente da c1].",
    )
    for old, new in (
        ("../REAPROVEITAMENTO_E_ERRATA.md", "REAPROVEITAMENTO_E_ERRATA.md"),
        ("../PARECER_KIMI_CONFERIDO.md", "PARECER_KIMI_CONFERIDO.md"),
        ("../MATTER_SOURCE_CUSTODY_VALIDATION.json", "MATTER_SOURCE_CUSTODY_VALIDATION.json"),
    ):
        if old in text:
            text = text.replace(old, new)
    addition = f"""

## Adendo V3 — leitura completa da v369 em ordens (R2/R3)

[REAL documental] A cópia v369 sob custódia local registra `core.clock_test_result_v369.P1.best_matter = {p1['best_matter']}` (⁶⁷Zn, Mössbauer), `best_matter_bound_kind = {p1['best_matter_bound_kind']}`, `best_matter_bound_orders = {p1['best_matter_bound_orders']:.9f}` e `tau_star_bound_best_s = {p1['best_matter_tau_star_bound_s']:.9e} s`. Esse τ★ é cota **NOMINAL dentro da leitura P1**; o core informa que o texto integral de Potzel 1976 não foi aberto. `P3.verdict = {p1['P3_verdict']}`: tempo estocástico universal não dá observável local de franja, largura ou razão de frequências. `root_law.kbar_rest_mass_excluded = true` exclui essa leitura da lei-raiz no core. A escolha física entre leituras está etiquetada `partition_tag = {p1['partition_tag']}` [OPEN].

[DERIVED condicional, τ★ = t_P, P1] O requisito de 5σ da v369 é para Sr `sr87_kim2025` com o σ de hoje: `Γ_pred = {sr['Gamma_pred_per_s']:.9e} s⁻¹`, `σ_excesso necessário = Γ_pred/5 = {sr['sigma_excess_5sigma_needed_per_s']:.9e} s⁻¹`, distância `{sr['deficit_5sigma_orders']:.9f}` ordens. O core dá `ℏω ≳ {sr['hbar_omega_needed_eV_at_todays_sigma']:.6f} eV` ou GHZ `N ≳ {sr['ghz_N_needed']:.6f}` como requisitos inferiores condicionais, não medidas.

[DERIVED condicional; NOMINAL] A melhor matéria do core tem `ω = {zn['omega_rad_s']:.9e} rad/s`, `Γ_pred = {zn['Gamma_pred_per_s']:.9e} s⁻¹`, cota nominal `{zn['Gamma_ub_nominal_per_s']:.9e} s⁻¹`: `log₁₀(cota/Γ_pred) = {zn['nominal_bound_deficit_orders']:.9f}` ordens. Usar o σ bruto como proxy de 5σ daria `{zn['sigma_reduction_raw_proxy_orders']:.9f}` ordens de redução, mas `sigma_excess_per_s = null`, `Z_expected = null` e `falsifiable = false`; isso **não é poder registrado**. A distância nominal de matéria fica {zn['less_than_sr_5sigma_orders_by']:.2f} ordens abaixo da distância 5σ do Sr, com estimadores e estatutos diferentes.

[DERIVED condicional, vácuo, `Kfac = 1`, `E₀ = 1 GeV`] A razão entre limites publicados dos modelos de neutrino e a taxa TGL hipotética fica de {span[0]:.2f} a {span[1]:.2f} ordens; no componente Γ₂₁ do cenário JUNO é {juno:.2f}. O cenário `Γ₂₁ = Γ₃₁` de Beccaria–Ternes não é a projeção demonstrada do operador TGL. Não se extrai limite de τ★ dessa razão; Fogli também usa dissipador solar distinto.

[OPEN — parede física da matéria interferométrica] Átomos, C₇₀ e nanopartículas carecem de `ω` efetivo por estado/caminho, mapa operador TGL `Γ→visibilidade`, separação dos ruídos e `σ_excesso` verificado. O `ω` nuclear do Mössbauer não preenche essa lacuna das franjas. Sem essa ponte e sem partição P1/P2/P3 resolvida, não há poder em ordens nem `τ★_limite` honesto para esses interferômetros. `NOT_FALSIFIED` nunca é creditação; o gate permanece intacto.

## Literatura posterior e SN1987A (contexto R1)

[KNOWN] A busca de literatura custodiada em `../context/LITERATURA_POS_JUNHO_F7_2_20261008.md` (SHA-256 `{R1_PIN}`) encontrou a cota JUNO acima como a mais recente diretamente comparável **na família de dissipador ali definida** até 08/10/2026. O artigo da Colaboração JUNO de 29/09/2026 traz parâmetros padrão de 207,2 dias vivos, sem nova cota publicada de `γ₂₁=γ₃₁`, `n=−2`; a conclusão da busca tem o alcance declarado no documento.

[KNOWN — modelo distinto] Ternes, Pagliaroli e Villante, arXiv:2503.04573v1, obtêm para SN1987A e `n=−2` `γ₀ < 3,1×10⁻⁴¹ GeV` (TI) ou `< 6,4×10⁻⁴¹ GeV` (TD), 90% CL, para **ν-loss**, isto é, supressão do fluxo total. O PDF contextual `../context/Ternes_Pagliaroli_Villante_2025_arxiv_2503.04573v1.pdf` tem SHA-256 `{SN_PIN}`. Esses números não são limites do dephasing sem perda do JUNO e não acrescentam linha nem `τ★_limite` ao canal.
"""
    return (text.rstrip() + addition).encode("utf-8")


def make_channel(v2_text: str, manifest_sha: str) -> bytes:
    text = replace_span(v2_text, "MANIFEST = ", "SCRIPT_NAMES = ", f'''MANIFEST = Path(__file__).with_name("neutrino_fontes_f72_v3.json")
MANIFEST_SHA256 = "{manifest_sha}"
SOURCE_ROOT = Path(__file__).resolve().parent.parent / "fontes_externas" / "F7.2"
PDF_ROOT = SOURCE_ROOT / "pdfs"
JUNO_NAME = "Beccaria_Ternes_2026_arxiv_2606.13362v1.pdf"
JUNO_SHA256 = "9212cd391d88846ee8065ac3ebf8ccb17be297417a86a22482fca858ed3be107"
''')
    docs = "DOC_PATHS = {\n" + "".join(
        f'    "{name}": SOURCE_ROOT / "documents" / "{filename}",\n'
        for name, filename in DOC_FILENAMES.items()
    ) + "}\n"
    text = replace_span(text, "DOC_PATHS = {", "PDF_CHANNELS = {", docs)
    text = replace_one(text, '"iald.f7_2.channel_sources.v3"', '"iald.f7_2.channel_sources.v4"')
    text = replace_span(text, '    if Path(manifest.get("source_root", "")).resolve()',
                        '    if frozenset(manifest.get("rejected_publisher_html", []))',
                        '''    if manifest.get("source_root_rel") != "../fontes_externas/F7.2":
        raise FonteRecusada("source root mismatch")
    if manifest.get("primary_pdf_subdir") != "pdfs":
        raise FonteRecusada("PDF root mismatch")
''')
    text = replace_one(text,
        '        path = Path(entry.get("path", ""))\n        if path.resolve() != (SOURCE_ROOT / name).resolve() or name in scripts:',
        '        path = SOURCE_ROOT / "scripts" / name\n        if entry.get("path") != f"scripts/{name}" or name in scripts:')
    text = replace_one(text,
        '        path = Path(entry.get("path", ""))\n        if path.resolve() != expected_path.resolve():',
        '        path = expected_path\n        if entry.get("path") != f"documents/{expected_path.name}":')
    text = replace_one(text,
        '        path = Path(entry.get("path", ""))\n        expected_pdf_path = JUNO_PDF if name == JUNO_NAME else PDF_ROOT / name\n        if path.resolve() != expected_pdf_path.resolve() or name in pdfs:',
        '        path = PDF_ROOT / name\n        if entry.get("path") != f"pdfs/{name}" or name in pdfs:')
    text = replace_one(text, '"mode": "READ_ONLY_SOURCE_PROVENANCE_V2"',
                       '"mode": "READ_ONLY_SOURCE_PROVENANCE_V3"')
    context_check = '''    context_sources = manifest.get("context_sources")
    expected_context = {
        "literature_review": ("LITERATURA_POS_JUNHO_F7_2_20261008.md", False),
        "sn1987a_nu_loss_pdf": ("Ternes_Pagliaroli_Villante_2025_arxiv_2503.04573v1.pdf", True),
    }
    if not isinstance(context_sources, dict) or set(context_sources) != set(expected_context):
        raise FonteRecusada("context source allowlist mismatch")
    for key, (filename, is_pdf) in expected_context.items():
        entry = context_sources[key]
        if entry.get("path") != f"context/{filename}":
            raise FonteRecusada(f"context path mismatch: {key}")
        path = SOURCE_ROOT / "context" / filename
        if is_pdf:
            _verify_pdf(path, entry.get("sha256"), entry.get("bytes"))
        else:
            result = _verify_source(path, entry.get("sha256"), python_source=False)
            if result["bytes"] != entry.get("bytes"):
                raise FonteRecusada(f"context byte count mismatch: {key}")
'''
    text = replace_one(text, '    projection = manifest.get("clock_v369_projection")',
                       context_check + '    projection = manifest.get("clock_v369_projection")')
    text = text.replace("F7.2 V2 staging channel", "F7.2 V3 self-contained channel")
    if "TUNEL" in text or "V2_STAGING" in text or "C:\\IALD" in text:
        raise ValueError("V3 module retains an external runtime path")
    ast.parse(text)
    return text.encode("utf-8")


def info(data: bytes) -> dict:
    return {"sha256": sha(data), "bytes": len(data)}


def main() -> None:
    v2_manifest_raw = load_pinned(V2_MANIFEST, V2_MANIFEST_PIN)
    v2_channel_raw = load_pinned(V2_CHANNEL, V2_CHANNEL_PIN)
    evidence_raw = load_pinned(R2_R3_JSON, R2_R3_PIN)
    r1_raw = load_pinned(R1_MD, R1_PIN)
    sn_raw = load_pinned(SN_PDF, SN_PIN)
    if not sn_raw.startswith(b"%PDF-") or len(sn_raw) != 656552:
        raise ValueError("SN1987A contextual PDF invalid")
    source = json.loads(v2_manifest_raw.decode("utf-8"))
    evidence = json.loads(evidence_raw.decode("utf-8"))
    if source.get("schema") != "iald.f7_2.channel_sources.v3" or source.get("unit") != "F7.2":
        raise ValueError("V2 schema/unit mismatch")
    if len(source["scripts"]) != 6 or len(source["primary_pdfs"]) != 10 or len(source["documents"]) != 8:
        raise ValueError("V2 source counts mismatch")
    if set(x["name"] for x in source["scripts"]) != set(SCRIPT_NAMES):
        raise ValueError("V2 script allowlist mismatch")
    if set(source["documents"]) != set(DOC_FILENAMES):
        raise ValueError("V2 document allowlist mismatch")
    if (source.get("raw_experimental_data_custodied") is not False
            or source.get("primary_article_pdfs_custodied") is not True):
        raise ValueError("V2 scope mismatch")
    destinations = [MODULE, MANIFEST, TABLE, RECEIPT, README]
    destinations += [ROOT / "scripts" / x["name"] for x in source["scripts"]]
    destinations += [ROOT / "pdfs" / x["name"] for x in source["primary_pdfs"]]
    destinations += [ROOT / "documents" / x for x in DOC_FILENAMES.values() if x != TABLE.name]
    destinations += [ROOT / "context" / R1_MD.name, ROOT / "context" / SN_PDF.name]
    if any(path.exists() for path in destinations):
        raise FileExistsError("V3 staging already populated; refusing partial overwrite")

    scripts = []
    pdfs = []
    documents = {}
    inventory = {}
    for entry in source["scripts"]:
        data = read_entry(entry, python=True)
        target = ROOT / "scripts" / entry["name"]
        write_new(target, data)
        inventory[str(target.relative_to(HERE)).replace("\\", "/")] = info(data)
        scripts.append({"name": entry["name"], "path": f"scripts/{entry['name']}", **info(data)})
    for entry in source["primary_pdfs"]:
        data = read_entry(entry, pdf=True)
        target = ROOT / "pdfs" / entry["name"]
        write_new(target, data)
        inventory[str(target.relative_to(HERE)).replace("\\", "/")] = info(data)
        pdfs.append({**entry, "path": f"pdfs/{entry['name']}"})
    for name, entry in source["documents"].items():
        data = read_entry(entry)
        if name == "channel_power_table":
            data = make_table(data.decode("utf-8"), evidence)
        target = ROOT / "documents" / DOC_FILENAMES[name]
        write_new(target, data)
        inventory[str(target.relative_to(HERE)).replace("\\", "/")] = info(data)
        documents[name] = {"path": f"documents/{DOC_FILENAMES[name]}", **info(data)}
    context_sources = {}
    for name, filename, data, kind in (
        ("literature_review", R1_MD.name, r1_raw, "LITERATURE_REVIEW"),
        ("sn1987a_nu_loss_pdf", SN_PDF.name, sn_raw, "PDF_CONTEXT_NU_LOSS_NOT_DEPHASING"),
    ):
        target = ROOT / "context" / filename
        write_new(target, data)
        inventory[str(target.relative_to(HERE)).replace("\\", "/")] = info(data)
        context_sources[name] = {"path": f"context/{filename}", "kind": kind, **info(data)}

    manifest = {**source, "schema": "iald.f7_2.channel_sources.v4",
                "source_root_rel": "../fontes_externas/F7.2", "primary_pdf_subdir": "pdfs",
                "scripts": scripts, "documents": documents, "primary_pdfs": pdfs,
                "context_sources": context_sources,
                "scope": "Local source copies only; no raw-data reanalysis or TGL tau-star limit."}
    for legacy in ("source_root", "primary_pdf_root", "juno_pdf_path"):
        manifest.pop(legacy, None)
    manifest_raw = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    module_raw = make_channel(v2_channel_raw.decode("utf-8"), sha(manifest_raw))
    write_new(MANIFEST, manifest_raw)
    write_new(MODULE, module_raw)
    inventory[str(MANIFEST.relative_to(HERE)).replace("\\", "/")] = info(manifest_raw)
    inventory[str(MODULE.relative_to(HERE)).replace("\\", "/")] = info(module_raw)

    readme = f"""# F7.2 V3 — pacote de fontes autocontido, sem implantação do canal

[REAL] Há 6 scripts originais de junho, 10 PDFs primários, 8 documentos do canal e 2 fontes contextuais R1 (relatório de literatura e PDF SN1987A) em `fontes_externas/F7.2/`, todos pinados por SHA-256 no manifesto `bancada/neutrino_fontes_f72_v3.json`. A tabela V3 deriva da V2 e incorpora R2/R3 e a distinção ν-loss/dephasing antes do pino. As demais cópias preservam bytes V2. Os caminhos do manifesto são relativos a `fontes_externas/F7.2`; o módulo deriva a raiz de sua própria localização, sem ler o túnel em runtime.

Destino futuro das fontes: `C:\\IALD\\Bancada_Um\\fontes_externas\\F7.2\\`. A cópia das fontes à Bancada é ato separado, somente aditivo. `bancada/neutrino_canal_v3.py` e o manifesto V3 são propostas para conferência c1; não foram instalados em `C:\\IALD\\Bancada_Um\\bancada`, nem ligados ao `mcp_um.py`, nem recarregados. O módulo preserva recusa fechada, 13 linhas, estatutos `[KNOWN]` publicados e `[DERIVED]` v369, `tau_star_limit_s = null`, `SEM_LIMITE_TGL` e `gate_effect = NONE`.

O recibo `STAGING_RECEIPT_V3.json` traz todos os hashes lidos. Os JSON históricos copiados podem conter caminhos de proveniência da época V1/V2; o canal V3 trata esses campos como texto custodiado e usa apenas os caminhos relativos allowlisted do manifesto.
""".encode("utf-8")
    write_new(README, readme)
    inventory[str(README.relative_to(HERE)).replace("\\", "/")] = info(readme)
    receipt = {
        "schema": "iald.f7_2.v3_source_staging_receipt.v1",
        "unit": "F7.2", "status": "STAGED_NOT_INSTALLED",
        "source_counts": {"scripts": 6, "primary_pdfs": 10, "documents": 8,
                          "context_docs": 1, "context_pdfs": 1},
        "copied_v2_manifest_sha256": V2_MANIFEST_PIN,
        "copied_v2_channel_sha256": V2_CHANNEL_PIN,
        "r2_r3_evidence_sha256": R2_R3_PIN,
        "r1_literature_sha256": R1_PIN,
        "sn1987a_pdf_sha256": SN_PIN,
        "table_derivation": "V2 table with R2/R3 adendum; V2 original untouched",
        "manifest_sha256_locked": sha(manifest_raw),
        "builder_sha256": sha(Path(__file__).read_bytes()),
        "files": inventory,
        "future_source_destination": r"C:\IALD\Bancada_Um\fontes_externas\F7.2",
        "channel_installed": False, "mcp_touched": False,
        "gate_effect": "NONE",
    }
    receipt_raw = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    write_new(RECEIPT, receipt_raw)
    print(json.dumps({"receipt": str(RECEIPT), "sha256": sha(receipt_raw),
                      "manifest_sha256": sha(manifest_raw), "module_sha256": sha(module_raw),
                      "files": len(inventory)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
