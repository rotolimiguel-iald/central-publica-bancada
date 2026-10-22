"""Create the additive F4.3 R4 decision correction and analytic screen.

This script never reads observational strain or writes outside its own folder.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from datetime import datetime
from pathlib import Path
from statistics import NormalDist


HERE = Path(__file__).resolve().parent
V2 = HERE / "PREREGISTRO_F4_3_V2.json"
V1 = Path(r"C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_05out\PREREGISTRO_RAMO_B_RINGDOWN_V1.json")
AUDIT = Path(r"C:\IALD\PROGRAMA_IALD\auditorias\F3.6.E1\AUDITORIA_F3_6_E1_C1_a4f6da3d.md")
MD = HERE / "ADENDO_C1_R4_F43_20261008.md"
V3 = HERE / "PREREGISTRO_F4_3_V3.json"
POWER = HERE / "PODER_ANALITICO_F43_R4_20261008.json"
RESULT = HERE / "RESULTADO_C1_F43_R4_20261008.json"
MAP = HERE / "MAPA_C1_R4_F43_20261008.json"


def pin(path: Path) -> dict:
    content = path.read_bytes()
    return {"path": str(path), "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}


def atomic_new(path: Path, payload: bytes) -> None:
    if path.exists():
        raise FileExistsError(path)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    if temp.stat().st_size != len(payload):
        raise IOError(f"short write: {temp}")
    os.replace(temp, path)


def dump_new(path: Path, value: dict) -> None:
    atomic_new(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def check_source(path: Path, expected_sha: str) -> dict:
    record = pin(path)
    if record["sha256"] != expected_sha:
        raise RuntimeError(f"source changed: {path}: {record['sha256']}")
    return record


def main() -> None:
    v2_pin = check_source(V2, "cf39d2a2fe919827b9a2e9ca48796c622675f81b54eebc598af8441bc53eaadc")
    v1_pin = check_source(V1, "86f98fcc124dd9cae04fdb06bd10c14175893253d5b139496bd4c05f109feee0")
    audit_pin = check_source(AUDIT, "8dd3a16090c02ca3a144f42ac95071670a49031ed39b2282551de0c3056d5361")
    previous = json.loads(V2.read_text(encoding="utf-8"))
    v1 = json.loads(V1.read_text(encoding="utf-8"))
    official = [item["token"] for item in v1["vereditos"]["ordem"]]
    if official != ["AWAITING_DATA", "INCONCLUSIVE_SYSTEMATICS", "NOT_FALSIFIED_UNDERPOWERED", "FALSIFIED_AT_5SIGMA", "NOT_FALSIFIED_POWERED"]:
        raise RuntimeError("unexpected V1 verdict vocabulary")
    for candidate in (MD, V3, POWER, RESULT, MAP):
        if candidate.exists():
            raise FileExistsError(candidate)

    nd = NormalDist()
    alpha = previous["v1_reconciliation_and_fwer"]["alpha_one_sided_per_relevant_null"]
    z_alpha = nd.inv_cdf(1 - alpha)
    z_90 = nd.inv_cdf(0.9)
    eta_90 = (z_alpha + z_90) ** 2
    power_eta25 = nd.cdf(math.sqrt(25.0) - z_alpha)
    power_eta_90 = nd.cdf(math.sqrt(eta_90) - z_alpha)
    eps = sys.float_info.epsilon
    now = datetime.now().astimezone().isoformat()
    analytic = {
        "id": "F43_R4_ANALYTIC_GAUSSIAN_SCREEN",
        "unit": "F4.3",
        "computed_at": now,
        "status": "DERIVED_CONDITIONAL_GAUSSIAN_SIMPLE__NOT_F43_D_POWER",
        "sources": {"v2": v2_pin, "v1": v1_pin, "audit": audit_pin},
        "model": "Simple known-template unit-variance Gaussian shift; one-sided z under alternative is N(sqrt(eta),1). Source/nuisance and waveform are fixed by assumption here; no D event or PSD is used.",
        "alpha_one_sided": alpha,
        "z_alpha": z_alpha,
        "power_formula": "Phi(sqrt(eta)-z_alpha)",
        "eta_25": {"eta": 25.0, "power": power_eta25, "interpretation": "median 5-sigma crossing only in the simple model"},
        "eta_for_90_percent_simple": {"eta": eta_90, "power": power_eta_90, "z_90": z_90},
        "eta_increment_440_1": "sqrt(1)=1 sigma of incremental distance in the simple model; relevance screen only",
        "rcond_1e_minus_10_over_binary64_eps": 1e-10 / eps,
        "rcond_sweep_required": [1e-12, 1e-10, 1e-8],
        "not_claimed": ["F4.3 exact-injection power", "D-set 90-percent recovery", "physical 5-sigma power", "permission to open D"],
    }
    dump_new(POWER, analytic)

    local_tokens = [
        "AWAITING_POWER",
        "DIAGNOSTIC_UNDERPOWERED_OR_NONIDENTIFIABLE",
        "DIAGNOSTIC_INCONCLUSIVE_SYSTEMATICS",
        "DIAGNOSTIC_BOTH_MODELS_REJECTED",
        "DIAGNOSTIC_CONFLICTS_V1",
        "DIAGNOSTIC_CORROBORATES_V1_SAME_DIRECTION",
        "DIAGNOSTIC_ONLY__NEITHER_REJECTED",
        "DIAGNOSTIC_ONLY__NO_V1_DIRECTION",
    ]
    v3 = {
        "id": "F4.3_220_PLUS_440_SHARED_SOURCE_V3_DESIGN_R4",
        "unit": "F4.3",
        "status": "PRE_REGISTERED_DESIGN__AWAITING_POWER__OPERATOR_REQUEST_SUSPENDED__NO_DATA_OPENED",
        "corrects_for_reading_only": v2_pin,
        "sources": {"v1_primary": v1_pin, "c1_audit": audit_pin, "analytic_screen": pin(POWER)},
        "clock_and_hypotheses": previous["clock"],
        "hypotheses": previous["hypotheses"],
        "primary_and_secondary": {
            "primary": "V1 full IMR with C3; its official verdict is preserved as a separate field",
            "secondary": "F4.3 ringdown-only; all DIAGNOSTIC_* tokens below are LOCAL, not V1 outputs",
            "C8": "one k and one M_f per event; never credit 221 to 440",
            "FWER": "same-direction corroboration requires V1 and F4.3 each to pass calibrated one-sided p <= alpha; intersection false claim <= alpha without independence",
            "alpha_one_sided": alpha,
        },
        "v1_official_base_tokens": official,
        "v1_official_suffix": "__GR_TENSION_REPORTED only on V1 NOT_FALSIFIED_POWERED when its own GR test meets V1 rule",
        "local_diagnostic_ordered_output": local_tokens,
        "local_aliases_retired": {
            "INCONCLUSIVE_SYSTEMATICS__BOTH_MODELS_REJECTED": "DIAGNOSTIC_BOTH_MODELS_REJECTED; joint reading INCONCLUSIVE_SYSTEMATICS, V1 field unchanged",
            "UNDERPOWERED_OR_NONIDENTIFIABLE": "DIAGNOSTIC_UNDERPOWERED_OR_NONIDENTIFIABLE; V1 NOT_FALSIFIED_UNDERPOWERED only if V1 itself fails its power gate",
            "NOT_FALSIFIED_POWERED from neither_rejected": "DIAGNOSTIC_ONLY__NEITHER_REJECTED; only V1 can emit official NOT_FALSIFIED_POWERED",
        },
        "decision_table": [
            {"when": "manifest incomplete or exact injected power absent", "diagnostic": "AWAITING_POWER", "joint_reading": "none; operator request suspended"},
            {"when": "exact injected recovery below 90% at one-sided 5 sigma, or 440 not identifiable", "diagnostic": "DIAGNOSTIC_UNDERPOWERED_OR_NONIDENTIFIABLE", "joint_reading": "no D opening from F4.3"},
            {"when": "calibration, coverage, bias, PSD, family or rcond stability fails", "diagnostic": "DIAGNOSTIC_INCONCLUSIVE_SYSTEMATICS", "joint_reading": "INCONCLUSIVE_SYSTEMATICS; V1 official token still recorded independently"},
            {"when": "F4.3 rejects both GR and pair B under their own calibrated nulls", "diagnostic": "DIAGNOSTIC_BOTH_MODELS_REJECTED", "joint_reading": "INCONCLUSIVE_SYSTEMATICS; do not choose either model"},
            {"when": "powered F4.3 points opposite to V1 primary direction", "diagnostic": "DIAGNOSTIC_CONFLICTS_V1", "joint_reading": "INCONCLUSIVE_SYSTEMATICS; no joint claim; V1 official token retained in separate field"},
            {"when": "powered F4.3 and V1 reject the same named null, each with calibrated one-sided p <= alpha", "diagnostic": "DIAGNOSTIC_CORROBORATES_V1_SAME_DIRECTION", "joint_reading": "corroboration of V1 only, never independent F4.3 credit"},
            {"when": "powered F4.3 rejects neither null", "diagnostic": "DIAGNOSTIC_ONLY__NEITHER_REJECTED", "joint_reading": "no official NOT_FALSIFIED_POWERED from F4.3"},
            {"when": "F4.3 directional signal but V1 has no compatible powered direction", "diagnostic": "DIAGNOSTIC_ONLY__NO_V1_DIRECTION", "joint_reading": "no joint claim"},
        ],
        "synthetic_screen": {
            "eta_formula": previous["synthetic_identifiability_screen_INPUT"]["eta_formula"],
            "eta_joint_25": "necessary median 5-sigma distance in ideal simple Gaussian shift; not 90-percent power",
            "eta_simple_90_percent": eta_90,
            "eta_increment_440_1": "minimal relevance floor, 1-sigma incremental distance; cannot independently imply detection",
            "rcond_reference": 1e-10,
            "rcond_sweep": [1e-12, 1e-10, 1e-8],
            "rcond_rule": "rank, eta screening verdict and diagnostic direction must be stable across sweep; otherwise DIAGNOSTIC_INCONCLUSIVE_SYSTEMATICS",
            "exact_required": "delta_tau = -x/(1+x), full IMR V1 C3 and common M_f,chi_f for 220+440",
            "decisive_power": "calibrated >=90% recovery at one-sided 5 sigma under exact injections and null coverage; analytic screen never substitutes",
        },
        "manifest_from_v2": previous["execution_manifest"],
        "power_status": {
            "F43_D_exact_injection": "NOT_MEASURED_FAIL_CLOSED",
            "reason": "V2 manifest leaves final event list, per-event PSD and hashes, windows, priors, start rule, waveform family/version/hash, covariance and injection seed/repetitions null. Existing O4 strain archive and older C7 injections do not specify this F4.3 joint 220+440 experiment.",
            "analytic_screen": "MEASURED_CONDITIONAL_SIMPLE_GAUSSIAN_ONLY",
            "operator_request": "SUSPENDED",
        },
        "no_observational_data_opened": True,
        "no_gate_change": True,
    }
    dump_new(V3, v3)

    md = f"""# F4.3 — R4 ao lado da V2 (08/10/2026)

Em nome de `codex-gerente-tgl`, após a auditoria c1 `{audit_pin['sha256']}`. O Nós Vivo apontou a rota `ringdown.modo_unico.degenerescencia` (seq 58/87/91), a QNM_GRID, a ORDEM 013 e o V1 selado do ramo B. A V2 `{v2_pin['sha256']}` continua íntegra; esta leitura aditiva governa o diagnóstico. [REAL documental] Nenhum strain ou PE do D foi aberto; o pedido ao operador continua SUSPENSO.

## Rótulos e precedência

O V1 tem os tokens oficiais `AWAITING_DATA`, `INCONCLUSIVE_SYSTEMATICS`, `NOT_FALSIFIED_UNDERPOWERED`, `FALSIFIED_AT_5SIGMA` e `NOT_FALSIFIED_POWERED` (com sufixo `__GR_TENSION_REPORTED` quando sua própria regra se cumpre). A F4.3 registra **outro campo**, `diagnostic_token`, limitado à lista `local_diagnostic_ordered_output` da V3. `DIAGNOSTIC_*`, `DIAGNOSTIC_UNDERPOWERED_OR_NONIDENTIFIABLE` e `DIAGNOSTIC_BOTH_MODELS_REJECTED` são rótulos **locais**, não palavras do V1. O antigo `INCONCLUSIVE_SYSTEMATICS__BOTH_MODELS_REJECTED` vira causa local `DIAGNOSTIC_BOTH_MODELS_REJECTED`, com leitura conjunta `INCONCLUSIVE_SYSTEMATICS`; `UNDERPOWERED_OR_NONIDENTIFIABLE` vira local e não retipa o V1. A F4.3 não emite `NOT_FALSIFIED_POWERED`: se nenhuma nula cair, emite `DIAGNOSTIC_ONLY__NEITHER_REJECTED` (se o portão de poder tiver passado).

Primeiro sai e se preserva o `v1_official_token` do IMR completo (C3). Se F4.3 apontar em sentido **oposto**, sai `DIAGNOSTIC_CONFLICTS_V1` e a leitura conjunta é `INCONCLUSIVE_SYSTEMATICS`; nenhum sinal é escolhido, nenhuma reivindicação conjunta é feita e a origem da discordância vai à revisão cética. Se coincidir, só `DIAGNOSTIC_CORROBORATES_V1_SAME_DIRECTION` após ambas as caudas calibradas passarem `p≤{alpha:.10g}` sob a mesma nula nomeada. Rejeição das duas nulidades pela F4.3 gera `DIAGNOSTIC_BOTH_MODELS_REJECTED`; nem o par B nem a RG é selecionado. C8 mantém um k e um M_f; 221 não conta para 440. O resultado da F4.3 isolado nunca altera o token V1.

## Limiar de triagem e poder

[DERIVED CONDICIONAL] Num deslocamento gaussiano simples, de template conhecido, `z|B ~ N(sqrt(η),1)` e `poder(η)=Φ(sqrt(η)−z_α)`. Para `α={alpha:.10g}`, `z_α={z_alpha:.9f}`; `η=25` dá `{power_eta25:.6f}` de chance de cruzar 5σ, **não** 90%. A chance de 90% pede `η≥{eta_90:.6f}` nesse modelo ideal. Por isso `η_joint≥25` é só uma triagem de distância mediana; a condição decisória é a recuperação ≥90% por injeções exatas, com nulos e cobertura. `η_increment_440≥1` cobra contribuição mínima de um desvio padrão geométrico do 440 após projeção; também não implica detecção. O cálculo reprodutível está em `{POWER.name}`, com fonte e limites.

`rcond=10⁻¹⁰` é referência de triagem em binary64, `{1e-10/eps:.0f}` vezes o epsilon de máquina. Não há justificativa para tratá-lo como constante física: o posto, η e a direção diagnóstica devem ser invariantes à varredura `{[1e-12,1e-10,1e-8]}`; se não forem, `DIAGNOSTIC_INCONCLUSIVE_SYSTEMATICS`. Em `x≈0,6`, só vale a injeção exata `δτ̂=−x/(1+x)`, com fonte comum e IMR C3; o Fisher linear é diagnóstico.

## Parede de execução atual

[OPEN] O poder **decisório do conjunto D não foi medido**. O manifesto V2 ainda deixa `null` a lista final e hash de eventos, PSD por evento/detector e seus hashes, janelas, priors, regra de início, família/versão/hash da forma de onda, covariância e semente/repetições de nulos. A casa tem acervo O4, QNM_GRID e injeções C7 anteriores, mas eles não definem por si a experiência conjunta F4.3 com 220+440 no relógio V1 e C3. A conta gaussiana acima mede somente o limite condicional do desenho; não certifica poder físico nem abre D. O portão vigente é `AWAITING_POWER`, com o pedido de autorização ao operador suspenso até manifesto pinado, injeções exatas, revisão cética e ato específico posterior.
"""
    atomic_new(MD, md.encode("utf-8"))

    result = {
        "unit": "F4.3",
        "member": "codex-gerente-tgl",
        "status": "R4_DELIVERED__AWAITING_POWER__OPERATOR_REQUEST_SUSPENDED",
        "as_of": now,
        "nos_vivo_reuse": "ringdown.modo_unico.degenerescencia; ORDEM 013/QNM_GRID/V1 Ramo B reused",
        "addressed": ["labels mapped as local diagnostic", "neither_rejected no longer emits official NOT_FALSIFIED_POWERED", "opposite-to-V1 rule", "eta/rcond mathematical rationale and stability sweep"],
        "remaining": ["F4.3 exact D-set injection power NOT_MEASURED; manifest fields listed in V3 remain null", "independent c1 reaudit", "operator-specific opening act after power"],
        "power_analytic_not_decisive": pin(POWER),
        "files": [pin(MD), pin(V3), pin(POWER), pin(Path(__file__)), v2_pin, v1_pin, audit_pin],
        "no_data_opened": True,
        "no_gate_change": True,
        "no_bancada_write": True,
    }
    dump_new(RESULT, result)
    map_entry = {
        "tipo": "ERRATA",
        "rota_id": "ringdown.modo_unico.degenerescencia",
        "dominio": "RINGDOWN",
        "titulo": "F4.3 R4: vocabulário diagnóstico e portão de poder antes do D",
        "pergunta": "Como conciliar os rótulos 220+440 com o V1 e justificar os limiares sem fingir poder medido?",
        "dados": [],
        "metodo": "Consulta Nós Vivo F4.3; leitura V1, V2, auditoria c1; cálculo analítico gaussiano condicional por script, sem strain ou PE.",
        "resultado": f"Rótulos F4.3 são locais, V1 oficial preservado; conflito de direções => INCONCLUSIVE_SYSTEMATICS conjunto. η=25 dá poder {power_eta25:.6f} no modelo gaussiano simples; 90% pede η≥{eta_90:.6f} nesse modelo. O poder F4.3 para D segue não medido, porque manifesto decisório contém campos null.",
        "veredito": "F43_R4_DESIGN_CORRECTED__AWAITING_POWER__OPERATOR_REQUEST_SUSPENDED__NO_DATA_OPENED",
        "estatuto": "DERIVED",
        "status": "EXAMINADA_COM_DEFEITO",
        "olhou_dados": False,
        "defeito": "Poder exato do conjunto D não medido; manifesto final/eventos/PSD/janelas/priors/início/família/covariância/semente pendentes; auditoria c1 da R4 pendente.",
        "nao_refazer": "Preservados V1/V2, QNM_GRID, Sonda c1 e ORDEM 013; não transportar Fisher de k=1 como poder V1.",
        "proximo_passo": "Pinar manifesto completo antes da injeção 220+440 exata/IMR C3; medir recuperação >=90% sob caudas calibradas; reauditar; só então reconsiderar pedido específico ao operador.",
        "onde": str(HERE),
        "artefatos": [pin(MD), pin(V3), pin(POWER), pin(RESULT)],
        "refs": ["ringdown.ramo_b_preregistro_v386"],
        "corrige": 842,
        "nota": "R4 ao lado, sem gate e sem dado D. A conta analítica não satisfaz o critério de poder da unidade.",
    }
    dump_new(MAP, map_entry)
    print(json.dumps({"power": pin(POWER), "v3": pin(V3), "md": pin(MD), "result": pin(RESULT), "map": pin(MAP)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
