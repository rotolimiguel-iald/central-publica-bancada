"""Reconcile T10 A'/B/C/D/E/F without treating diagnostic data as sigma(c)."""
import copy
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RING = HERE.parents[2]
CHAT = RING.parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def new_json(path, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    with Path(path).open("xb") as out:
        out.write(raw)
        out.flush()
        os.fsync(out.fileno())


def main():
    base = RING / "ORCAMENTO_015_v11.json"
    budget = json.loads(base.read_bytes())
    assert budget["accounting"]["machine_hours_spent"] < budget["authorized_machine_hours"]
    a = json.loads((HERE / "T10_A_FINAL_RESULT.json").read_bytes())
    aprime = json.loads((HERE / "T10_APRIME_SPECTRAL_RANK.json").read_bytes())
    b = json.loads((HERE / "T10_B_RESULT.json").read_bytes())
    c = json.loads((HERE / "T10_C_BANK_RESULT_v4.json").read_bytes())
    assert a["sigma_c"] is None and aprime["rank"] == 3 and len(c["rows"]) == 10
    assert [r["b2_status"] for r in b["rows"]] == ["REFUSED_CONDITIONING", "ACCEPTED_COVARIANCE_DIAGNOSTIC_ONLY"]
    registry = RING / "RINGDOWN_5SIGMA_V1_1_3.json"
    assert c["registry_sha256"] == sha(registry)
    for row in c["rows"]:
        assert sha(CHAT / row["file_relative_to_Chatgpt"]) == row["sha256"]
    c_fail = [HERE / "T10_C_PREP_FAILURE.json", HERE / "T10_C_BANK_RESULT.json", HERE / "T10_C_BANK_RESULT_v3.json"]
    t04c = json.loads((RING / "bis" / "015" / "t04" / "branch_c" / "CONVERGENCE_REVIEW.json").read_bytes()) if (RING / "bis" / "015" / "t04" / "branch_c" / "CONVERGENCE_REVIEW.json").exists() else None
    item = next(x for x in budget["items"] if x["item"] == "T10_calibration")
    # Command walls were returned by the executable tool; conservative, sequential, no overlaps.
    observed_command_walls = [5.6206761, 3.4310147, 1.8400481, 2.6340752, 5.8284516]
    bc_hours = sum(observed_command_walls) / 3600.0
    status = "T10_MEDIDA_BANK_GENERATED_NO_TRANSFER_OR_SIGMA_C"
    result = {
        "status": status,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "A": {"status": a["status"], "sigma_c": None, "posterior_width_ratio": a["posterior_width_ratio"]},
        "A_prime": {"status": "SPECTRAL_RANK_ONLY_PE_NOT_PAID", "rank": aprime["rank"],
                    "note": "The same A injection has zero true 440 amplitude; spectral rank does not imply measured multimode information",
                    "estimated_PE_cost_hours_INPUT": [0.25, 1.0]},
        "B": {"status": "B1_FAILED_B2_H1_REFUSED_B3_REGULARIZED_B4_SYNTHETIC",
              "H1_condition_B2": b["rows"][0]["b2_condition"],
              "H1_condition_B3": b["rows"][0]["b3_condition"],
              "L1_condition_B2": b["rows"][1]["b2_condition"],
              "real_network_covariance_qualified": False},
        "C": {"status": "BANK_GENERATION_PAID_RECOVERY_NOT_PAID", "cells": len(c["rows"]),
              "bins": [19.1, 17.0, 15.0, 13.0, 12.0], "families": 2,
              "sigma_c_from_bank": None},
        "D": {"status": "NOT_PAID_NO_QUALIFIED_PSEOB_RECOVERY_IN_T04",
              "t04_branch_c_machine_hours_measured": 6.410089644876389,
              "t04_branch_c_posterior_accepted": False,
              "two_three_transfer_forecast_machine_hours_DERIVED": [12.820179289752778, 19.23026893462917],
              "note": "Balance could fund two such runtimes; lacking a converged pSEOB estimator, no valid transfer is measurable under the current T04 instrument. This is a qualification limitation, not budget exhaustion."},
        "E": {"status": "NOT_TRIGGERED_A_CONVERGED", "additional_cost_hours": 0},
        "F": {"status": "COSTS_AND_UNPAID_REGISTERED", "A_machine_hours": a["cost"]["machine_hours_accounted"],
              "BC_observed_command_wall_seconds": observed_command_walls,
              "BC_machine_hours": bc_hours,
              "D_two_three_transfer_forecast_machine_hours": [12.820179289752778, 19.23026893462917]},
        "sigma_inj_ensemble": None, "sigma_c": None, "gate_changed": False,
        "ten_readings_status": "ALL_RED_OR_UNDERPOWERED; NO sigma(c) MEASURED",
        "pins": {str(path.relative_to(CHAT)).replace("\\", "/"): sha(path) for path in [
            HERE / "T10_A_FINAL_RESULT.json", HERE / "T10_APRIME_SPECTRAL_RANK.json",
            HERE / "T10_B_PRE_REG.json", HERE / "T10_B_RESULT.json",
            HERE / "T10_B_PREREG_TIME_ERRATA.md", registry,
            HERE / "T10_C_BANK_RESULT_v4.json", *c_fail,
            RING / "bis" / "015" / "t04" / "branch_c" / "RESULT.json"]},
    }
    result_path = HERE / "T10_FINAL_RESULT.json"
    new_json(result_path, result)
    item["actual_machine_hours"] += bc_hours
    item["status"] = status
    item["final_receipt_sha256"] = sha(result_path)
    budget["accounting"]["intervals"].append(dict(target="T10_BC_DIAGNOSTIC_AND_BANK",
        receipt_relative_to_Chatgpt=str(result_path.relative_to(CHAT)).replace("\\", "/"),
        sha256=sha(result_path), union_machine_hours=bc_hours,
        accounting_statute="SUM_OF_SEQUENTIAL_OBSERVED_TOOL_COMMAND_WALLS"))
    budget["accounting"]["machine_hours_spent"] += bc_hours
    assert budget["accounting"]["machine_hours_spent"] < budget["authorized_machine_hours"]
    budget["T10_BC_measurement"] = dict(result_sha256=sha(result_path), machine_hours=bc_hours,
        bank_cells=10, real_noise_qualified=False, sigma_c_unpaid=True, gate_changed=False)
    budget["supersedes_sha256"] = sha(base)
    budget["registered_utc"] = datetime.now(timezone.utc).isoformat()
    budget["witness_relative_to_Chatgpt"] = "TUNEL/DO_CHATGPT/ENTREGA_015_ORCAMENTO_015_v12.md"
    budget_path = RING / "ORCAMENTO_015_v12.json"
    new_json(budget_path, budget)
    opening = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_016_ABERTURA_operador.md"
    handoff = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_P_calibracao_T10.md"
    text = ("[REAL — T10 parcial; banco sintético pago, σ(c) não pago]\n\n"
            f"Abertura da ORDEM016 SHA256 {sha(opening)}. Não-cego. A′: posto espectral 3, "
            "PE multimodo não executada; a mesma injeção de A é 220 puro. "
            f"B2: H1 condição {b['rows'][0]['b2_condition']:.6g} > 1e12; L1 {b['rows'][1]['b2_condition']:.6g}. "
            "B3 carregamento diagonal é INPUT, sem equivalência a ruído real; B4 continua sintético. "
            "C: 10/10 células GR geradas por duas famílias nos bins registrados, sem recuperação PE. "
            "D: sem posterior pSEOB qualificado no T04; custo 2–3 × 6,410089644876389h medido como previsão; não foi lançado. "
            "E: A convergiu, portanto não acionado. F: tabela de custos e pendências no recibo.\n\n"
            f"Recibo T10 SHA256 {sha(result_path)}; orçamento v12 SHA256 {sha(budget_path)}; "
            f"registro V1.1.3 SHA256 {sha(registry)}. "
            "Reprodução: executar os scripts t10_a_injection_v2.py, t10_b_noise.py e t10_c_bank_v4.py "
            "com as pré-inscrições correspondentes; `finalize_t10_bc.py` reconcilia os artefatos. "
            "Tentativas falhas preservadas: prior conjunto v1; gerador C v1 (sombra de variável), "
            "v2 (PyCBC ausente) e v3 (cauda não tratada). "
            "Axiomas: N/A — sem Lean. Gate inalterado.\n")
    with handoff.open("xb") as f:
        f.write(text.encode())
    witness = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_ORCAMENTO_015_v12.md"
    with witness.open("xb") as f:
        f.write(("[REAL — atualização aditiva do orçamento]\n\n"
                 f"supersedes ORCAMENTO_015_v11.json sha256 {sha(base)}\n"
                 f"registered_utc: {budget['registered_utc']}\n"
                 f"allocation_sha256: {sha(budget_path)}\n"
                 f"Máquina usada {budget['accounting']['machine_hours_spent']:.9f}h de {budget['authorized_machine_hours']:.9f}h. "
                 "T10-B/C: 0,005376h, soma conservadora das cinco paredes de comandos sequenciais.\n").encode())
    progress = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_016_PROGRESSO.md"
    old = progress.read_bytes()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    backup = progress.with_name(progress.name + ".bak_" + stamp)
    with backup.open("xb") as f:
        f.write(old)
    assert sha(backup) == hashlib.sha256(old).hexdigest()
    line = (f"\n{datetime.now(timezone.utc).isoformat()} | B/T10 | MEDIDA: A 2 priors, A′ posto espectral sem PE, "
            f"B ruído real não qualificado, C banco 10/10 gerado, D transferência não paga; σ(c)=null, gate intacto "
            f"| máquina acumulada {budget['accounting']['machine_hours_spent']:.9f}h | recibo SHA256 {sha(result_path)}; próximo T14\n")
    temp = progress.with_name(progress.name + ".tmp_" + stamp)
    with temp.open("xb") as f:
        f.write(old + line.encode())
    assert temp.stat().st_size > len(old)
    os.replace(temp, progress)
    print(json.dumps({"result_sha256": sha(result_path), "budget_sha256": sha(budget_path),
                      "handoff_sha256": sha(handoff), "machine_hours": budget["accounting"]["machine_hours_spent"]}))


if __name__ == "__main__":
    main()
