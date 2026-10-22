"""Record the measured T04 failure and witness the one permitted branch-C job."""
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
OLD_JOB = "GW250114_PILOT_V2_S220"
NEW_JOB = "GW250114_PILOT_V2_S220_C1"
NEW_OUTPUT = "E3_PSEOB_PILOT_V2_S220_C1"
NEW_SEED = 15260303


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read(path: Path) -> dict:
    return json.loads(path.read_bytes())


def new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if path.stat().st_size != len(data):
        raise OSError(f"Incomplete new artifact: {path}")


def encode(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def main() -> None:
    registration_path = RING / "RINGDOWN_5SIGMA_V1_1_2.json"
    allocation_path = RING / "ORCAMENTO_015_v2.json"
    old_config_path = DESK / "E2_PE_JOBS_ALLOCATION_015_V2.json"
    pilot_path = HERE / "pilot" / "RESULT.json"
    qualification_path = HERE / "QUALIFICATION_DELIVERY.json"
    convergence_path = RING / "cache" / OLD_JOB.replace("GW250114_PILOT_V2_S220", "E3_PSEOB_PILOT_V2_S220") / "PRIVATE_CONVERGENCE.json"
    controller_path = convergence_path.parent / "CONTROLLER.json"
    registration = read(registration_path)
    previous = read(allocation_path)
    old_config = read(old_config_path)
    pilot = read(pilot_path)
    qualification = read(qualification_path)
    convergence = read(convergence_path)
    controller = read(controller_path)

    assert pilot["registration_sha256"] == digest(registration_path)
    assert pilot["allocation_sha256"] == digest(allocation_path)
    assert pilot["controller_receipt_sha256"] == digest(controller_path)
    assert pilot["cleanup_confirmed"] is True and pilot["budget_stopped"] is False
    assert controller["cleanup"]["group_absent"] is True
    assert controller["status"] == convergence["status"] == "PARTIAL_MAXCALL_NOT_ACCEPTED"
    assert convergence["accepted_for_analysis"] is False
    assert convergence["ess"] < convergence["minimum_ess"]
    assert convergence["posterior_samples"] < registration["pe_jobs"][OLD_JOB]["sampler"]["minimum_posterior_samples"]
    assert convergence["cost"]["edom"]["edom"] == 0
    assert qualification["status"] == "T04_QUALIFICATION_MEASURED_PILOT_NOT_YET_LAUNCHED"
    assert previous["allocated_machine_hours"] == 34.2
    assert registration["pe_jobs"][OLD_JOB]["sampler"]["maxcall"] == 3_000_000
    assert NEW_JOB not in registration["pe_jobs"] and NEW_JOB not in old_config["jobs"]
    assert not (RING / "cache" / NEW_OUTPUT).exists()

    r = convergence["cost"]["sampler_ncall"] / convergence["cost"]["wall_seconds"]
    maxcall = min(math.floor(0.9 * 28_800 * r), 9_000_000)
    assert maxcall == 5_738_602 and maxcall > 3_000_000
    pilot_hours = pilot["wall_seconds"] / 3600
    qualification_hours = qualification["accounted_T04_qualification_hours"]
    assert abs(pilot_hours - pilot["machine_hours"]) < 1e-10
    now = datetime.now(timezone.utc).isoformat()

    new_job = copy.deepcopy(registration["pe_jobs"][OLD_JOB])
    new_job["label"] = NEW_JOB
    new_job["output_directory_name"] = NEW_OUTPUT
    new_job["sampler"]["seed"] = NEW_SEED
    new_job["sampler"]["maxcall"] = maxcall
    config = copy.deepcopy(old_config)
    config["jobs"][NEW_JOB] = new_job
    config["scope"] = "ONE_T04_BRANCH_C_RETRY;SAME_SOURCE_PRIORS_AND_GRID;NEW_ID_SEED_MAXCALL_ONLY"
    config_path = DESK / "E2_PE_JOBS_ALLOCATION_015_V3.json"

    allocation = copy.deepcopy(previous)
    allocation["registered_utc"] = now
    allocation["supersedes_sha256"] = digest(allocation_path)
    allocation["parent_registration_sha256"] = digest(registration_path)
    allocation["witness_relative_to_Chatgpt"] = "TUNEL/DO_CHATGPT/ENTREGA_015_ORCAMENTO_015_v3.md"
    allocation["jobs_relative_to_Chatgpt"] = config_path.relative_to(CHATGPT).as_posix()
    items = {item["item"]: item for item in allocation["items"]}
    assert items["T04_pilot_220"]["allocated_machine_hours"] == 8
    assert items["T10_calibration"]["allocated_machine_hours"] == 15
    items["T04_pilot_220"].update(
        allocated_machine_hours=pilot_hours,
        actual_machine_hours=pilot_hours,
        job_started=True,
        status=controller["status"],
        final_receipt_sha256=digest(pilot_path),
    )
    items["T04_runner_qualification"].update(
        actual_machine_hours=qualification_hours,
        job_started=True,
        status="T04_ADAPTER_400_QUALIFIED",
        final_receipt_sha256=digest(HERE / "qualify" / "RESULT.json"),
    )
    items["T10_calibration"]["allocated_machine_hours"] = 12.0
    allocation["items"].append({
        "item": "T04_branch_C",
        "allocated_machine_hours": 8.0,
        "estimated_wall_hours": maxcall / r / 3600,
        "estimate_source": "Measured sampler_ncall / sampler wall_seconds from the rejected T04 pilot",
        "estimate_statute": "DERIVED_FROM_REAL_RATE_NOT_CONVERGENCE_FORECAST",
        "actual_machine_hours": 0.0,
        "job_started": False,
        "job": NEW_JOB,
        "registered_maxcall": maxcall,
    })
    total = sum(item["allocated_machine_hours"] for item in allocation["items"])
    spent = previous["accounting"]["machine_hours_spent"] + qualification_hours + pilot_hours
    assert abs(total - 34.96690831932667) < 1e-9
    assert total <= allocation["authorized_machine_hours"]
    assert spent < total and spent < allocation["authorized_machine_hours"]
    allocation["allocated_machine_hours"] = total
    allocation["unallocated_machine_hours"] = allocation["authorized_machine_hours"] - total
    allocation["reallocation_reason"] = "Measured C branch after maxcall, not accepted posterior; return unused pilot reserve and reassign three T10 hours"
    allocation["reallocation_changes"] = {
        "T04_pilot_220": {"old": 8.0, "new": pilot_hours},
        "T10_calibration": {"old": 15.0, "new": 12.0},
        "T04_branch_C": {"old": 0.0, "new": 8.0},
    }
    allocation["branch_C_measurement"] = {
        "pilot_receipt_sha256": digest(pilot_path),
        "convergence_sha256": digest(convergence_path),
        "controller_sha256": digest(controller_path),
        "r_sampler_calls_per_job_wall_second": r,
        "maxcall": maxcall,
        "expected_wall_seconds_at_same_rate": maxcall / r,
        "delta_logz_observed": convergence["delta_logz"],
        "ess_observed": convergence["ess"],
        "posterior_samples_observed": convergence["posterior_samples"],
        "posterior_accepted": False,
        "convergence_not_predicted": True,
    }
    allocation["accounting"]["intervals"].extend([
        {"target": "T04_qualification", "receipt_relative_to_Chatgpt": qualification_path.relative_to(CHATGPT).as_posix(), "sha256": digest(qualification_path), "union_machine_hours": qualification_hours},
        {"target": "T04_pilot_220", "receipt_relative_to_Chatgpt": pilot_path.relative_to(CHATGPT).as_posix(), "sha256": digest(pilot_path), "union_machine_hours": pilot_hours, "CPU_seconds": pilot["children_cpu_seconds"]},
    ])
    allocation["accounting"]["machine_hours_spent"] = spent
    allocation["prerequisites_unpaid"] = ["T04_BRANCH_C_INDEPENDENT_REVIEW_AND_LAUNCH_PREFLIGHT"]
    allocation["gate_changed"] = False
    budget_path = RING / "ORCAMENTO_015_v3.json"
    witness_path = OUT / "ENTREGA_015_ORCAMENTO_015_v3.md"
    medida_path = OUT / "ENTREGA_015_MEDIDA_T04_maxcall.md"
    for p in (config_path, budget_path, witness_path, medida_path):
        assert not p.exists(), f"Do not overwrite registered artifact: {p}"

    new(config_path, encode(config))
    allocation["jobs_sha256"] = digest(config_path)
    new(budget_path, encode(allocation))
    witness = (
        "[REAL — custo do piloto; DERIVED — novo teto; INPUT — realocação]\n\n"
        f"allocation_sha256: {digest(budget_path)}\nregistered_utc: {now}\n\n"
        f"Pai: {digest(allocation_path)}. Registro: {digest(registration_path)}. "
        f"Job novo {NEW_JOB}, seed {NEW_SEED}, maxcall {maxcall}; saída {NEW_OUTPUT}. "
        f"Total alocado {total:.12f} h de {allocation['authorized_machine_hours']:.12f} h; "
        f"gasto medido {spent:.12f} h. T10 passa a 12 h. "
        "A configuração de fonte, priors e grade foi copiada sem alteração; nenhum posterior foi aceito. "
        "Esta testemunha não lança o job, não move o gate e não mede significância física.\n"
    )
    new(witness_path, witness.encode("utf-8"))
    medida = (
        "[REAL — T04 piloto não aceito; DERIVED — ramo C]\n\n"
        f"Job {OLD_JOB}; resultado SHA256 {digest(pilot_path)}; controlador SHA256 {digest(controller_path)}; "
        f"convergência SHA256 {digest(convergence_path)}; log SHA256 {pilot['log_sha256']}. "
        f"Comando registrado: {pilot['controller_receipt']['job']} via run_controlled.py, supervisor T04 v3. "
        f"RC supervisor {pilot['returncode']}, RC controlador {controller['returncode']}. "
        f"Status {controller['status']}; {convergence['cost']['sampler_ncall']} chamadas em "
        f"{convergence['cost']['wall_seconds']:.6f} s de amostrador; "
        f"delta_logz {convergence['delta_logz']:.6f}, ESS {convergence['ess']:.6f}, "
        f"posterior_samples {convergence['posterior_samples']}. "
        f"Custo de parede supervisor {pilot['wall_seconds']:.6f} s; CPU filhos {pilot['children_cpu_seconds']:.6f} s; "
        f"EDOM {convergence['cost']['edom']['edom']}; limpeza confirmada. "
        f"Ramo C: r={r:.9f} chamadas/s e maxcall={maxcall}; novo ID/seed testemunhados em {witness_path.name}. "
        "A extrapolação é só de duração, não de convergência. Próximo: revisão independente/preflight; então uma única execução C. "
        "Nenhum posterior, sigma ou gate é inferido desta rodada.\n"
    )
    new(medida_path, medida.encode("utf-8"))
    print(json.dumps({
        "status": "T04_C_REGISTERED_NOT_LAUNCHED", "job": NEW_JOB,
        "maxcall": maxcall, "allocation_sha256": digest(budget_path),
        "witness_sha256": digest(witness_path), "measured_spent_hours": spent,
        "allocated_hours": total, "remaining_authorized_hours": allocation["authorized_machine_hours"] - spent,
    }))


if __name__ == "__main__":
    main()
