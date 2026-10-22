"""Close the registered T10-A diagnostic and advance the Part-B budget."""
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RING = HERE.parents[2]
CHAT = RING.parent
OLD = RING / "ORCAMENTO_015_v10.json"
NEW = RING / "ORCAMENTO_015_v11.json"
PORTAO = RING / "PORTAO_DA_AMPLIACAO_V1.json"
PRE = HERE / "T10_A_PRE_REG.json"
PREPARED = HERE / "T10_A_PREPARED.json"
REPAIR = HERE / "T10_A_PRIOR_REPAIR_v2.json"
AUDIT = HERE / "T10_A_POSTERIOR_AUDIT.json"
FREE = HERE / "fit_free" / "RESULT.json"
FAILED = HERE / "fit_informed" / "RESULT.json"
INFORMED = HERE / "fit_informed_latent_v2" / "RESULT.json"
T09 = HERE.parent / "t09" / "T09_PREREQUISITE_RESULT.json"
RESULT = HERE / "T10_A_FINAL_RESULT.json"
HANDOFF = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_MEDIDA_T10_A_injecao.md"
WITNESS = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_ORCAMENTO_015_v11.md"
PROGRESS = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_016_PROGRESSO.md"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert path.read_bytes() == raw


def json_new(path, value):
    write_new(path, (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode())


def append_with_backup(path, extra):
    old = path.read_bytes()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    backup = path.with_name(path.name + ".bak_" + stamp)
    write_new(backup, old)
    temp = path.with_name(path.name + ".tmp_" + stamp)
    write_new(temp, old + extra)
    os.replace(temp, path)
    assert path.read_bytes() == old + extra


def main():
    pre = json.loads(PRE.read_bytes())
    prep = json.loads(PREPARED.read_bytes())
    repair = json.loads(REPAIR.read_bytes())
    free = json.loads(FREE.read_bytes())
    failed = json.loads(FAILED.read_bytes())
    informed = json.loads(INFORMED.read_bytes())
    audit = json.loads(AUDIT.read_bytes())
    assert pre["status"] == "PRE_REGISTERED_DIAGNOSTIC_NOT_BANK"
    assert repair["failed_attempt_produced_posterior"] is False
    assert free["status"] == informed["status"] == "DESCRIPTIVE_POSTERIOR_REQUIRES_REVIEW"
    assert failed["status"] == "FAILED_NO_POSTERIOR"
    assert free["data_sha256"] == informed["data_sha256"] == prep["data_sha256"]
    assert audit["pre_registration_sha256"] == sha(PRE)
    assert abs(audit["variants"]["free"]["delta_tau"]["std"] - free["posterior"]["sigma_inj_single_realization"]) < 1e-12
    assert abs(audit["variants"]["informed_latent_v2"]["delta_tau"]["std"] - informed["posterior"]["sigma_inj_single_realization"]) < 1e-12
    summed = sum(x["wall_seconds"] for x in (free, failed, informed))
    overhead_conservative = 10.0
    hours = (summed + overhead_conservative) / 3600
    order = json.loads(PORTAO.read_bytes())
    floors = order["systematic_conditions"]
    sigma = informed["posterior"]["sigma_inj_single_realization"]
    table = []
    for row in floors:
        floor = row["floor5_INPUT"]
        if floor is None:
            estimate = None
            why = "NO_NUMERIC_FLOOR"
        elif floor == 0:
            estimate = None
            why = "ZERO_FLOOR_FINITE_CALIBRATION_IMPOSSIBLE"
        else:
            estimate = math.ceil(10 * (sigma / abs(floor)) ** 2)
            why = "CONDITIONAL_PROXY_POSTERIOR_WIDTH_NOT_ENSEMBLE_SIGMA"
        table.append(dict(reading=row["reading"], floor5_INPUT=floor,
                          N_10x_proxy=estimate, status=why,
                          sigma_c=None, gate_green=False))
    result = dict(status="T10_A_PARTIAL_TWO_PRIORS_ONE_INJECTION_NO_SIGMA_C",
                  created_utc=datetime.now(timezone.utc).isoformat(),
                  nonblind=True, branch="T10_A", injection_count=1,
                  posterior_free=free["posterior"], posterior_informed=informed["posterior"],
                  posterior_width_ratio=audit["free_to_informed_delta_std_ratio"],
                  posterior_width_is_ensemble_scatter=False,
                  sigma_inj_ensemble=None, sigma_c=None,
                  failed_joint_prior_attempt=failed["error"],
                  failed_attempt_posterior=False,
                  cost=dict(process_wall_seconds=summed,
                            overhead_conservative_seconds=overhead_conservative,
                            machine_hours_accounted=hours,
                            first_fit_seconds=free["wall_seconds"],
                            informed_fit_seconds=informed["wall_seconds"],
                            failed_adapter_seconds=failed["wall_seconds"]),
                  ten_readings=table,
                  pins={str(path.relative_to(CHAT)): sha(path) for path in
                        (OLD, PORTAO, PRE, PREPARED, REPAIR, AUDIT, FREE, FAILED, INFORMED, T09)},
                  scope="synthetic Gaussian-colored public PSD; one 220 mode; no observed event PE",
                  next_branch="T10_A_PRIME_DATA_OR_B_NOISE",
                  gate_changed=False)
    json_new(RESULT, result)
    budget = json.loads(OLD.read_bytes())
    items = {r["item"]: r for r in budget["items"]}
    assert items["T10_calibration"]["actual_machine_hours"] == 0
    assert items["T10_calibration"]["allocated_machine_hours"] > hours
    items["T10_calibration"].update(actual_machine_hours=hours, job_started=True,
        status=result["status"], first_result_sha256=sha(RESULT))
    items["T09_440_free"].update(status="T09_NAO_PAGO_OPERATOR_BOX_B_LINE_ABSENT",
                                    final_receipt_sha256=sha(T09))
    budget["registered_utc"] = datetime.now(timezone.utc).isoformat()
    budget["supersedes_sha256"] = sha(OLD)
    budget["witness_relative_to_Chatgpt"] = WITNESS.relative_to(CHAT).as_posix()
    budget["allocated_machine_hours"] = sum(r["allocated_machine_hours"] for r in budget["items"])
    budget["accounting"]["intervals"].append(dict(target="T10_A_DIAGNOSTIC",
        receipt_relative_to_Chatgpt=RESULT.relative_to(CHAT).as_posix(),
        sha256=sha(RESULT), union_machine_hours=hours,
        accounting_statute="SUM_OF_NONOVERLAPPING_FIT_PROCESS_WALL_PLUS_10S_CONSERVATIVE_PREP_LAUNCH"))
    budget["accounting"]["machine_hours_spent"] = sum(r.get("actual_machine_hours", 0) for r in budget["items"])
    budget["T10_A_measurement"] = dict(result_sha256=sha(RESULT), posterior_audit_sha256=sha(AUDIT),
        free_width=free["posterior"]["sigma_inj_single_realization"],
        informed_width=sigma, sigma_c_unpaid=True, model_transfer_unpaid=True,
        no_gate=True)
    assert abs(budget["allocated_machine_hours"] - budget["authorized_machine_hours"]) < 1e-9
    assert budget["accounting"]["machine_hours_spent"] <= budget["authorized_machine_hours"]
    json_new(NEW, budget)
    opening = sha(CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_ABERTURA_operador.md")
    handoff = (f"[REAL — T-10 A, injeção diagnóstica NÃO-CEGA; sem gate]\n\n"
      f"Abertura ORDEM 015 SHA256 `{opening}`. Pré-registro SHA256 `{sha(PRE)}`; "
      f"injeção SHA256 `{sha(HERE / 'T10_A_INJECTION.npz')}`; auditoria posterior SHA256 `{sha(AUDIT)}`; "
      f"recibo final SHA256 `{sha(RESULT)}`. Uma injeção sintética Kerr 220, PSD pública, "
      f"SNR ótimo alvo 19,1, mesma realização de ruído em dois priors.\n\n"
      f"Massa/spin livres: posterior δτ₂₂₀ média {free['posterior']['mean']:.6f}, "
      f"desvio {free['posterior']['sigma_inj_single_realization']:.6f}, "
      f"q05/q50/q95 {free['posterior']['q05_q50_q95']}, custo {free['wall_seconds']:.3f}s. "
      f"Prior IMR conjunto: média {informed['posterior']['mean']:.6f}, "
      f"desvio {sigma:.6f}, q05/q50/q95 {informed['posterior']['q05_q50_q95']}, "
      f"custo {informed['wall_seconds']:.3f}s; redução de largura por fator "
      f"{audit['free_to_informed_delta_std_ratio']:.4f}. Valor injetado zero contido nos "
      f"dois intervalos de 90%.\n\n"
      f"Primeira implementação do prior conjunto falhou ANTES de posterior: {failed['error']}; "
      f"recibo SHA256 `{sha(FAILED)}`. Correção por variáveis gaussianas latentes, com a "
      f"mesma covariância pré-registrada, SHA256 `{sha(REPAIR)}`. O erro foi preservado. "
      f"O desvio padrão posterior de UMA injeção não é dispersão de recuperação de um banco: "
      f"σ_inj entre injeções e σ(c) residual permanecem null. A tabela das dez leituras "
      f"em `{RESULT.relative_to(CHAT).as_posix()}` usa a largura posterior APENAS como proxy "
      f"condicional de planejamento; nenhuma célula do gate fica verde. O prior informado "
      f"configura observável IMR–RD [INPUT a ratificar]; transferência ao pSEOB permanece aberta.\n\n"
      f"Máquina contabilizada {hours:.9f}h = soma das paredes dos três processos "
      f"({summed:.3f}s) + 10s conservadores de preparação/lançamento. "
      f"Orçamento v11 SHA256 `{sha(NEW)}`, gasto acumulado "
      f"{budget['accounting']['machine_hours_spent']:.9f}h de "
      f"{budget['authorized_machine_hours']:.9f}h. Próximo ramo T-10 A′/B conforme árvore.\n")
    write_new(HANDOFF, handoff.encode())
    witness = (f"[REAL] ORCAMENTO_015_v11 registrado após T10-A. Pai v10 SHA256 `{sha(OLD)}`; "
        f"v11 SHA256 `{sha(NEW)}`; T10-A SHA256 `{sha(RESULT)}`; T09 SHA256 `{sha(T09)}`. "
        f"Gasto total {budget['accounting']['machine_hours_spent']:.9f}h; autorizado/alocado "
        f"{budget['authorized_machine_hours']:.9f}h; T10 alocado "
        f"{items['T10_calibration']['allocated_machine_hours']:.9f}h e gasto {hours:.9f}h. "
        f"Sem σ(c) nem gate.\n")
    write_new(WITNESS, witness.encode())
    line = (f"\n{datetime.now(timezone.utc).isoformat()} | B/T10-A | MEDIDA parcial: "
        f"uma injeção, dois priors; larguras posteriores {free['posterior']['sigma_inj_single_realization']:.6f}/"
        f"{sigma:.6f}; σ(c) NÃO PAGO; prior conjunto v1 falhou e v2 corrigiu | "
        f"máquina {hours:.9f}h; acumulado {budget['accounting']['machine_hours_spent']:.9f}h | "
        f"recibo SHA256 {sha(RESULT)}; próximo T10 A′/B\n").encode()
    append_with_backup(PROGRESS, line)
    print(json.dumps(dict(result_sha256=sha(RESULT), budget_sha256=sha(NEW),
                          handoff_sha256=sha(HANDOFF), machine_hours=hours,
                          total_machine_hours=budget["accounting"]["machine_hours_spent"])))


if __name__ == "__main__":
    main()
