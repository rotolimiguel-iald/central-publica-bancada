"""Witness the measured T04-C failure and reserve the single H retry."""
from __future__ import annotations

import copy
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESK = HERE.parent
RING = DESK.parents[1]
CHATGPT = RING.parent
OUT = CHATGPT / "TUNEL" / "DO_CHATGPT"
OLD_JOB = "GW250114_PILOT_V2_S220_C1"
NEW_JOB = "GW250114_PILOT_V2_S220_H1"
NEW_OUTPUT = "E3_PSEOB_PILOT_V2_S220_H1"
NEW_SEED = 15260404


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_bytes())


def encoded(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if path.stat().st_size != len(data):
        raise OSError(f"Incomplete new artifact: {path}")


def main() -> None:
    registration_path = RING / "RINGDOWN_5SIGMA_V1_1_2.json"
    allocation_path = RING / "ORCAMENTO_015_v3.json"
    old_config_path = DESK / "E2_PE_JOBS_ALLOCATION_015_V3.json"
    result_path = HERE / "branch_c" / "RESULT.json"
    cache = RING / "cache" / "E3_PSEOB_PILOT_V2_S220_C1"
    controller_path = cache / "CONTROLLER.json"
    convergence_path = cache / "PRIVATE_CONVERGENCE.json"
    analyst_path = cache / "ANALYST_STATUS.json"
    edom_path = cache / "EDOM_LOG.jsonl"
    order_path = CHATGPT / "TUNEL" / "PARA_CHATGPT" / "ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md"
    opening_path = OUT / "ENTREGA_016_ABERTURA_operador.md"

    assert sha(opening_path) == "216a1a7d6b29548a4a47f5aa22f67e953d04f56d2e00bc3e505487d68df0f57a"
    assert sha(order_path) == "c903681d01eec5ed8d55b7fe69e061a79b3a7b73eecede8f895cfb2d127f75a3"
    assert sha(registration_path) == "a02c4224b0c832a85e8eaef736197754235aa573290760bb2307ad6ac4c713b4"
    assert sha(allocation_path) == "be8dde137351c5add245daca8bd68b6ad5f6238708a230fbaab829dc6788b4ea"
    assert sha(result_path) == "9663242560623d92e933bdab82ca176022f6b3606ee285aceea6c8a9eecaea36"
    assert sha(convergence_path) == "c1d291f30c44212e70f9adee519d03c02f2344167308442f719b772269dc832b"

    prior = read(allocation_path)
    config = copy.deepcopy(read(old_config_path))
    result = read(result_path)
    controller = read(controller_path)
    conv = read(convergence_path)
    analyst = read(analyst_path)
    assert result["allocation_sha256"] == sha(allocation_path)
    assert result["registration_sha256"] == sha(registration_path)
    assert result["controller_receipt_sha256"] == sha(controller_path)
    assert result["cleanup_confirmed"] is True and result["budget_stopped"] is False
    assert controller["cleanup"]["group_absent"] is True
    assert controller["status"] == conv["status"] == analyst["status"] == "PARTIAL_MAXCALL_NOT_ACCEPTED"
    assert conv["accepted_for_analysis"] is False and analyst["accepted"] is False
    assert conv["posterior_samples"] == 1 and conv["ess"] < conv["minimum_ess"]
    assert conv["cost"]["edom"]["edom"] == 0 and sha(edom_path) == conv["cost"]["edom"]["log_sha256"]
    assert NEW_JOB not in config["jobs"] and not (RING / "cache" / NEW_OUTPUT).exists()
    assert not (HERE / "branch_h").exists()

    rate = conv["ncall"] / conv["cost"]["wall_seconds"]
    maxcall = min(math.floor(0.9 * 28_800 * rate), 9_000_000)
    assert maxcall > conv["cost"]["maxcall_nominal"] and maxcall < 9_000_000
    now = datetime.now(timezone.utc).isoformat()
    job = copy.deepcopy(config["jobs"][OLD_JOB])
    job["label"] = NEW_JOB
    job["output_directory_name"] = NEW_OUTPUT
    job["sampler"]["seed"] = NEW_SEED
    job["sampler"]["nlive"] = 1024
    job["sampler"]["maxcall"] = maxcall
    assert job["wall_budget_seconds"] == 28_800 and job["sampler"]["workers"] == 24
    config["jobs"][NEW_JOB] = job
    config["scope"] = "ONE_T04_BRANCH_H_RETRY;SAME_SOURCE_PRIORS_AND_GRID;NEW_ID_SEED_NLIVE_MAXCALL_ONLY"
    config_path = DESK / "E2_PE_JOBS_ALLOCATION_015_V4.json"

    budget = copy.deepcopy(prior)
    budget["registered_utc"] = now
    budget["supersedes_sha256"] = sha(allocation_path)
    budget["parent_registration_sha256"] = sha(registration_path)
    budget["witness_relative_to_Chatgpt"] = "TUNEL/DO_CHATGPT/ENTREGA_015_ORCAMENTO_015_v4.md"
    budget["jobs_relative_to_Chatgpt"] = config_path.relative_to(CHATGPT).as_posix()
    budget["jobs_sha256"] = hashlib.sha256(encoded(config)).hexdigest()
    items = {item["item"]: item for item in budget["items"]}
    assert items["T04_branch_C"]["allocated_machine_hours"] == 8.0
    assert items["T10_calibration"]["allocated_machine_hours"] == 12.0
    c_hours = result["machine_hours"]
    assert abs(c_hours - result["wall_seconds"] / 3600) < 1e-10
    items["T04_branch_C"].update(actual_machine_hours=c_hours, allocated_machine_hours=c_hours,
                                   job_started=True, status=controller["status"],
                                   final_receipt_sha256=sha(result_path))
    new_t10 = 12.0 - (c_hours - prior["unallocated_machine_hours"])
    assert 0 < new_t10 < 12
    items["T10_calibration"]["allocated_machine_hours"] = new_t10
    budget["items"].append(dict(item="T04_branch_H", allocated_machine_hours=8.0,
        estimated_wall_hours=maxcall / rate / 3600,
        estimate_source="ORDEM015 H/C formula with measured T04-C sampler calls per wall second",
        estimate_statute="DERIVED_FROM_REAL_RATE_NOT_CONVERGENCE_FORECAST",
        actual_machine_hours=0.0, job_started=False, job=NEW_JOB,
        registered_maxcall=maxcall, registered_nlive=1024))
    total = sum(item["allocated_machine_hours"] for item in budget["items"])
    assert total <= budget["authorized_machine_hours"] + 1e-9
    assert abs(total - budget["authorized_machine_hours"]) < 1e-9
    budget["allocated_machine_hours"] = total
    budget["unallocated_machine_hours"] = max(0.0, budget["authorized_machine_hours"] - total)
    spent = prior["accounting"]["machine_hours_spent"] + c_hours
    assert spent < total
    budget["accounting"]["intervals"].append(dict(target="T04_branch_C",
        receipt_relative_to_Chatgpt=result_path.relative_to(CHATGPT).as_posix(),
        sha256=sha(result_path), union_machine_hours=c_hours,
        CPU_seconds=result["children_cpu_seconds"]))
    budget["accounting"]["machine_hours_spent"] = spent
    budget["reallocation_reason"] = "Measured T04-C maxcall partial; H is the single residual retry with nlive1024; unused C reserve returned and T10 reserve reduced"
    budget["reallocation_changes"] = dict(T04_branch_C=dict(old=8.0,new=c_hours),
        T10_calibration=dict(old=12.0,new=new_t10),T04_branch_H=dict(old=0.0,new=8.0))
    budget["branch_H_measurement"] = dict(branch_C_receipt_sha256=sha(result_path),
        branch_C_controller_sha256=sha(controller_path),
        branch_C_convergence_sha256=sha(convergence_path),
        branch_C_ncall=conv["ncall"],branch_C_wall_seconds=conv["cost"]["wall_seconds"],
        r_sampler_calls_per_job_wall_second=rate,maxcall=maxcall,nlive=1024,
        delta_logz_observed=conv["delta_logz"],ess_observed=conv["ess"],
        posterior_samples_observed=conv["posterior_samples"],posterior_accepted=False,
        convergence_not_predicted=True)
    budget["prerequisites_unpaid"] = ["T04_BRANCH_H_INDEPENDENT_REVIEW_AND_LAUNCH_PREFLIGHT"]
    budget["gate_changed"] = False
    budget_path = RING / "ORCAMENTO_015_v4.json"
    witness_path = OUT / "ENTREGA_015_ORCAMENTO_015_v4.md"
    medida_path = OUT / "ENTREGA_015_MEDIDA_T04_C_maxcall.md"
    for path in (medida_path, config_path, witness_path, budget_path):
        assert not path.exists(), f"Do not overwrite registered artifact: {path}"

    note = (
        "[REAL — T04-C não aceito; DERIVED — classificação residual H]\n\n"
        f"Abertura016SHA256: {sha(opening_path)}. ORDEM015SHA256: {sha(order_path)}. "
        f"Comando: {' '.join(read(HERE / 'branch_c' / 'PLAN.json')['command'])}. "
        f"RESULT SHA256 {sha(result_path)}; CONTROLADOR {sha(controller_path)}; "
        f"CONVERGÊNCIA {sha(convergence_path)}; ANALYST_STATUS {sha(analyst_path)}; "
        f"PROCESS.log {result['log_sha256']}; EDOM_LOG {sha(edom_path)}.\n\n"
        f"Job {OLD_JOB}: RC supervisor {result['returncode']}, RC controlador {controller['returncode']}; "
        f"status {controller['status']}. {conv['ncall']} chamadas em {conv['cost']['wall_seconds']:.6f} s de amostrador "
        f"(r={rate:.9f}/s); delta_logz={conv['delta_logz']:.6f} para limiar {conv['threshold']}; "
        f"ESS={conv['ess']:.6f} para mínimo {conv['minimum_ess']}; "
        f"posterior_samples={conv['posterior_samples']}. Posterior não aceito. "
        f"EDOM={conv['cost']['edom']['edom']}, fração {conv['cost']['edom']['fraction']}; "
        f"parede supervisor={result['wall_seconds']:.6f} s ({c_hours:.12f} h), "
        f"CPU filhos={result['children_cpu_seconds']:.6f} s; limpeza confirmada.\n\n"
        "A condição literal de D (status PARTIAL_LOW_ESS/PARTIAL_TOO_FEW_POSTERIOR_SAMPLES) não foi emitida. "
        "E exige aborto nativo; RC 2/3 aqui é recusa controlada de posterior, não aborto nativo. "
        "H cobre o estado residual PARTIAL_MAXCALL_NOT_ACCEPTED após C: uma única repetição com novo ID/seed, "
        f"nlive=1024 e maxcall={maxcall} pela fórmula C, teto 8 h; configuração/priors e grade preservados. "
        "A extrapolação de duração não prediz convergência. Próximo: testemunha v4, revisão independente e preflight; "
        "depois uma única execução H. Nenhum sigma, posterior ou gate inferido.\n"
    )
    witness = (
        "[REAL — custo de C; DERIVED — fórmula H; INPUT — realocação]\n\n"
        f"allocation_sha256: {hashlib.sha256(encoded(budget)).hexdigest()}\nregistered_utc: {now}\n\n"
        f"Abertura016SHA256: {sha(opening_path)}. Pai v3: {sha(allocation_path)}. "
        f"Registro: {sha(registration_path)}. Job novo {NEW_JOB}, seed {NEW_SEED}, nlive 1024, "
        f"maxcall {maxcall}; saída {NEW_OUTPUT}. Total alocado {total:.12f} h de "
        f"{budget['authorized_machine_hours']:.12f} h; gasto medido {spent:.12f} h. "
        f"T10 fica com {new_t10:.12f} h nesta alocação. Configuração científica, priors e grade de C preservados. "
        "Esta testemunha não lança H, não aceita posterior e não move gate.\n"
    )
    # The allocation appears last: readers of the numbered chain then see a complete witness/config.
    new(medida_path, note.encode("utf-8"))
    new(config_path, encoded(config))
    new(witness_path, witness.encode("utf-8"))
    new(budget_path, encoded(budget))
    assert sha(config_path) == budget["jobs_sha256"]
    assert sha(budget_path) in witness
    print(json.dumps(dict(status="T04_H_REGISTERED_NOT_LAUNCHED",job=NEW_JOB,
        maxcall=maxcall,nlive=1024,rate=rate,c_hours=c_hours,
        budget_sha256=sha(budget_path),witness_sha256=sha(witness_path),
        medida_sha256=sha(medida_path),allocated_hours=total,spent_hours=spent)))


if __name__ == "__main__":
    main()
