"""Generate the ORDEM015 Part B closing report from pinned local receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


CHATGPT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
AUDIT = CHATGPT / "ORDEM_013_RINGDOWN/bis/015/closing_audit"
DEST = CHATGPT / "TUNEL/DO_CHATGPT/ENTREGA_015_RELATORIO_FINAL.md"
PROVENANCE = AUDIT / "ENTREGA_015_RELATORIO_FINAL_PROVENIENCIA.json"

INPUTS = {
    "matriz_T01_T13": "ORDEM_013_RINGDOWN/bis/015/closing_audit/T01_T13_CLOSING_AUDIT.json",
    "matriz_T16_T19": "ORDEM_013_RINGDOWN/bis/015/closing_audit/T16_T19_CLOSING_AUDIT.json",
    "T14_B": "ORDEM_013_RINGDOWN/bis/015/t14/T14_B_RESULT.json",
    "T15": "ORDEM_013_RINGDOWN/bis/015/t15/T15_MEDIDA.json",
    "orcamento_v13": "ORDEM_013_RINGDOWN/ORCAMENTO_015_v13.json",
    "nota_T19": "TUNEL/DO_CHATGPT/ENTREGA_015_T19_ATUALIZACAO_DADO_PUBLICO.md",
    "ordem": "TUNEL/PARA_CHATGPT/ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: str) -> dict:
    return json.loads((CHATGPT / path).read_text(encoding="utf-8-sig"))


def fmt(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(", ", ": "))


def main() -> None:
    if DEST.exists() or PROVENANCE.exists():
        raise FileExistsError("Destination exists; no overwrite performed")
    source_hashes = {name: sha(CHATGPT / path) for name, path in INPUTS.items()}
    a = read_json(INPUTS["matriz_T01_T13"])
    later = read_json(INPUTS["matriz_T16_T19"])
    t14 = read_json(INPUTS["T14_B"])
    t15 = read_json(INPUTS["T15"])
    budget = read_json(INPUTS["orcamento_v13"])
    t19_note = (CHATGPT / INPUTS["nota_T19"]).read_text(encoding="utf-8-sig")
    assert budget["order_sha256"] == source_hashes["ordem"]
    assert a["source_sha256"]["order"] == source_hashes["ordem"]
    assert later["source_sha256"]["Chatgpt/" + INPUTS["ordem"]] == source_hashes["ordem"]
    assert budget["accounting"]["machine_hours_spent"] > 0
    assert budget["accounting"]["machine_hours_spent"] < budget["authorized_machine_hours"]
    assert t14["machine_hours_charged_conservative"] == next(
        i["union_machine_hours"] for i in budget["accounting"]["intervals"]
        if i["target"] == "T14_PYSEOBNR_LOCAL_INSTALL_AND_API"
    )
    assert t15["decision"]["pilot_injections_run"] == 0
    assert "strain H1, L1 e V1" in t19_note and "censo negativo" in t19_note

    verified: dict[str, str] = {}

    def verify(relative: str, expected: str) -> None:
        relative = relative.removeprefix("Chatgpt/")
        actual = sha(CHATGPT / relative)
        if actual != expected:
            raise ValueError(f"SHA256 differs: {relative}: {actual} != {expected}")
        verified[relative] = actual

    for row in a["targets"]:
        for item in row["evidence"]:
            verify(item["path_relative_to_Chatgpt"], item["sha256"])
    for item in t14["sources"]:
        verify(item["relative_to_Chatgpt"], item["sha256"])
    for item in budget["accounting"]["intervals"]:
        verify(item["receipt_relative_to_Chatgpt"], item["sha256"])
    for relative, expected in later["source_sha256"].items():
        verify(relative, expected)
    verify("ORDEM_013_RINGDOWN/bis/015/t15/T15_PRE_REG.json", t15["prereg_sha256"])
    verify(budget["source_receipt_relative_to_Chatgpt"], budget["source_receipt_sha256"])
    verify(budget["jobs_relative_to_Chatgpt"], budget["jobs_sha256"])
    for name, relative in INPUTS.items():
        verified[relative] = source_hashes[name]

    lines = [
        "[REAL — auditoria documental local de bytes e recibos; DERIVED — classificações e aritmética; KNOWN — atualização pública T19 conforme nota fonte; OPEN — inferência física e dados futuros]",
        "",
        "# ORDEM015 Parte B — relatório final",
        "",
        "A integração abaixo fecha a prestação de contas documental da Parte B. `PAGO` significa aceitação apenas no escopo expresso do alvo; `PARCIAL` preserva requisitos científicos abertos; `NÃO_PAGO` preserva bloqueios ou execução ausente. Não houve neste fechamento nova PE, injeção, alteração de fonte canônica ou movimento de gate.",
        "",
        "## Alvos T01–T19",
        "",
        "| Alvo | Estatuto | Medição/entrega e limite | Máquina debitada | Evidência conferida |",
        "|---|---|---|---:|---|",
    ]
    for row in a["targets"]:
        number = row["target"]
        evidence = ", ".join("`" + Path(e["path_relative_to_Chatgpt"]).name + "`" for e in row["evidence"])
        content = (f"{row['proof']} Números do recibo: {fmt(row['essential_numbers'])}. "
                   f"Limite: {row['limit']}")
        hours = row["machine_cost"]["actual_heavy_machine_hours_v12"]
        lines.append(f"| {number} | {row['state']} | {content} | {hours:.12g} h | {evidence} |")

    t14_state = "PAGO — só instalação/API" if t14["install_rc"] == 0 and t14["finite_waveforms"] > 0 and not t14["PE_posterior"] else "PARCIAL/ABERTO"
    t14_details = (f"pyseobnr {t14['version']}; instalação rc={t14['install_rc']}, {t14['finite_waveforms']} formas finitas; "
                   f"L2 relativo Δτ={t14['dtau_relative_L2_whole_overlap']}, Δω={t14['domega_relative_L2_whole_overlap']}; "
                   f"tempos por forma (s)={fmt(t14['cost_per_form_seconds'])}. {t14['warmup_notice']} "
                   f"Posterior PE={fmt(t14['PE_posterior'])}; sigma(c)={fmt(t14['sigma_c'])}. "
                   f"Cobrança conservadora inclui intervalos ociosos: {t14['accounting_statute']}.")
    lines.append(f"| T14 | {t14_state} | {t14_details} | {t14['machine_hours_charged_conservative']:.12g} h | `T14_B_RESULT.json`, fontes internas rehasheadas |")

    t15_state = "NÃO_PAGO" if t15["decision"]["pilot_injections_run"] == 0 and t15["decision"]["posterior_fits_run_T15"] == 0 else "PARCIAL"
    t15_details = (f"{t15['status']}; H1 B2={t15['noise']['H1_B2']} > limite {t15['noise']['condition_limit']}; "
                   f"L1 B2={t15['noise']['L1_B2']}. Observável T10={t15['instrument']['fitted_parameter_T10_A']}, "
                   f"solicitado={t15['instrument']['requested_parameter_T15']}; rank≤{t15['instrument']['structural_rank_upper_bound']}, "
                   f"nulidade≥{t15['instrument']['structural_nullity_lower_bound']}. "
                   f"Injeções piloto={t15['decision']['pilot_injections_run']}; ajustes T15={t15['decision']['posterior_fits_run_T15']}; "
                   f"σ_jit,rec={fmt(t15['instrument']['sigma_jit_rec'])}; σ_sys(δf̂)={fmt(t15['instrument']['sigma_sys_delta_f_hat'])}. "
                   f"Bloqueios={fmt(t15['decision']['reason'])}. Proxy para 50 ajustes: "
                   f"{fmt(t15['budget']['single_recovery_measured_T10_A_synthetic_dtau_proxy'])}; "
                   f"proxy pareado para 100 ajustes: {fmt(t15['budget']['paired_GR_Brownian_order_Kerr_V2_638s_proxy'])}; "
                   "estimativas condicionais, sem rodada T15.")
    lines.append(f"| T15 | {t15_state} | {t15_details} | {next(i['actual_machine_hours'] for i in budget['items'] if i['item']=='T15_sigma_jit_rec'):.12g} h | `T15_MEDIDA.json`, pré-registro rehasheado |")

    for number in ("T16", "T17", "T18"):
        state = later["states"][number]
        detail = "; ".join(state["missing_or_unmet_prerequisites_verified"])
        estimates = {k: v for k, v in state.items() if "estimated" in k or "derived" in k or k.endswith("formula")}
        lines.append(f"| {number} | {state['state']} | {detail} Custos condicionais [DERIVED/INPUT]: {fmt(estimates)}. {state.get('arithmetic_note','')} | 0 h | `T16_T19_CLOSING_AUDIT.json`, ordem e recibos rehasheados |")

    old_t19 = later["states"]["T19"]
    t19_state = "PARCIAL / AWAITING_CENSUS_AND_FUTURE_DATA" if "strain H1, L1 e V1" in t19_note and "censo negativo" in t19_note else old_t19["state"]
    lines.append(f"| T19 | {t19_state} | Strain público de GW250207_115645 listado em H1/L1/V1 (4096 s, 4/16 kHz), conforme atualização de fonte oficial de 27/09. Nenhum download/PE nesta nota. Censo negativo, GWTC-6/O4c, O5 e leitura bilateral/κ continuam OPEN; L5 unilateral não é confirmação. Custo de execução T19={fmt(old_t19['machine_hours'])} (desconhecido). | não aferido | `ENTREGA_015_T19_ATUALIZACAO_DADO_PUBLICO.md`; `T16_T19_CLOSING_AUDIT.json` |")

    spent = budget["accounting"]["machine_hours_spent"]
    authorized = budget["authorized_machine_hours"]
    remaining = authorized - spent
    lines += [
        "",
        "## Orçamento, custos e veredito",
        "",
        f"[REAL] Orçamento v13: **{spent} h debitadas / {authorized} h autorizadas**; saldo aritmético [DERIVED] **{remaining} h**. Alocação integral {budget['allocated_machine_hours']} h, sem horas não alocadas ({budget['unallocated_machine_hours']} h). Regra contábil: `{budget['accounting']['rule']}`. O saldo não constitui nova autorização ou prova de convergência. T14 consumiu cobrança conservadora de {t14['machine_hours_charged_conservative']} h, limitada a instalação e API.",
        "",
        "[REAL/DERIVED] Custos de trabalho leve, CPU e bancada descritos em cada linha não se somam às horas de máquina v13. T01 registra USD 3.0821417664 **parciais**, total USD `null`; T11 registra custo de coordenação USD `null`. T09 prevê 2,6–3,3 h por piloto, condicional a autorização, teto estimado de 8 h; T16 prevê 7,8–9,9 h para três eventos (a prosa original traz 9,8 h, mas 3 × 3,3 = 9,9). T17: 1.512–9.672 CPU-h para R-LIN/R-MOD/R-RAIZ-0 e 134.820–166.920 CPU-h para R-B, sem execução. T18: 1–3 h de máquina e 2–4 h de bancada para 2a, mais 1 dia de bancada para 2b se autorizada. Previsões não são gastos; T19 não tem estimativa executável aferida.",
        "",
        "[OPEN] `sigma(c)=null`; não há z conjunto calibrado de 5σ nesta entrega. Sigmas de canais, eventos ou leituras não são somáveis. T03, T04, T08, T10, T15 e T16 deixam calibração, convergência, seleção ou cegueira por pagar. Não emitir `CONFIRMED` ou `PROVED`; `NOT_FALSIFIED` não se converte em confirmação. [REAL] `gate_changed=false` nos recibos T14, T15 e orçamento v13; nenhum artefato deste fechamento o move.",
        "",
        "## Fontes primárias e integridade",
        "",
        "Os SHA-256 abaixo foram calculados dos bytes locais nesta execução, não copiados de memória. Os recibos referenciados pelas matrizes, pelo orçamento e por T14/T15 foram confrontados com seus SHA-256 declarados; a lista completa está na proveniência nova ao lado do gerador.",
        "",
        "| Fonte | SHA-256 calculado |",
        "|---|---|",
    ]
    for name, relative in INPUTS.items():
        lines.append(f"| `{relative}` | `{source_hashes[name]}` |")
    lines += ["", "[DECLARADO] A nota T19 relata consulta a páginas oficiais GWOSC/IGWN; este fechamento valida a nota local e suas referências, sem repetir consulta remota nem auditar os arquivos de strain.", ""]

    payload = "\n".join(lines).encode("utf-8")
    with DEST.open("xb") as handle:
        handle.write(payload)
    if DEST.stat().st_size != len(payload):
        raise IOError("Report size mismatch")
    provenance = {
        "report_relative_to_Chatgpt": str(DEST.relative_to(CHATGPT)).replace("\\", "/"),
        "report_sha256": sha(DEST),
        "sources_sha256": source_hashes,
        "verified_receipts_sha256": verified,
        "verified_receipts_count": len(verified),
        "generated_rows": [x["target"] for x in a["targets"]] + ["T14", "T15", "T16", "T17", "T18", "T19"],
    }
    with PROVENANCE.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(provenance, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps({"report": str(DEST), "sha256": provenance["report_sha256"], "verified_receipts": len(verified), "provenance": str(PROVENANCE)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
