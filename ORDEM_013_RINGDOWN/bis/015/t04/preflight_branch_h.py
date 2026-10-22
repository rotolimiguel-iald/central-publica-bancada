"""Read-only proof that the single T04-H job is witnessed and unchanged scientifically."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESK = HERE.parent
RING = DESK.parents[1]
CHATGPT = RING.parent
CODE = RING / "bis" / "e2_code_v1_1_2"
sys.path.insert(0, str(CODE))
from registration_guard import checked_registration, load_authorized_configuration


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    reg, pin = checked_registration()
    view = load_authorized_configuration(reg, pin)
    budget_path = RING / "ORCAMENTO_015_v4.json"
    config_path = DESK / "E2_PE_JOBS_ALLOCATION_015_V4.json"
    prior_path = DESK / "E2_PE_JOBS_ALLOCATION_015_V3.json"
    result_path = HERE / "branch_c" / "RESULT.json"
    conv_path = RING / "cache" / "E3_PSEOB_PILOT_V2_S220_C1" / "PRIVATE_CONVERGENCE.json"
    b = json.loads(budget_path.read_bytes())
    config = json.loads(config_path.read_bytes())
    previous = json.loads(prior_path.read_bytes())
    result = json.loads(result_path.read_bytes())
    conv = json.loads(conv_path.read_bytes())
    name = "GW250114_PILOT_V2_S220_H1"
    old = "GW250114_PILOT_V2_S220_C1"
    assert pin == "a02c4224b0c832a85e8eaef736197754235aa573290760bb2307ad6ac4c713b4"
    assert view["_allocation_sha256"] == sha(budget_path)
    assert b["jobs_sha256"] == sha(config_path)
    assert b["supersedes_sha256"] == sha(RING / "ORCAMENTO_015_v3.json")
    assert config["jobs"][old] == previous["jobs"][old]
    assert view["pe_jobs"][name] == config["jobs"][name]
    assert result["cleanup_confirmed"] is True and result["controller_receipt"]["status"] == "PARTIAL_MAXCALL_NOT_ACCEPTED"
    assert conv["accepted_for_analysis"] is False
    assert b["accounting"]["intervals"][-1]["sha256"] == sha(result_path)
    assert b["accounting"]["intervals"][-1]["union_machine_hours"] == result["machine_hours"]
    cfg = copy.deepcopy(config["jobs"][name])
    reference = copy.deepcopy(config["jobs"][old])
    assert cfg["sampler"]["seed"] != reference["sampler"]["seed"]
    assert cfg["sampler"]["nlive"] == 1024 and reference["sampler"]["nlive"] == 512
    assert cfg["sampler"]["maxcall"] == 6449148
    for key in ("label", "output_directory_name"):
        cfg[key] = reference[key]
    for key in ("seed", "nlive", "maxcall"):
        cfg["sampler"][key] = reference["sampler"][key]
    assert cfg == reference, "H changed source, priors, data, detector, or grid"
    assert not (RING / "cache" / "E3_PSEOB_PILOT_V2_S220_H1").exists()
    assert not (HERE / "branch_h").exists()
    items = {item["item"]: item for item in b["items"]}
    assert items["T04_branch_C"]["actual_machine_hours"] == result["machine_hours"]
    assert items["T04_branch_H"]["allocated_machine_hours"] == 8.0
    assert items["T10_calibration"]["allocated_machine_hours"] > 0
    assert abs(sum(item["allocated_machine_hours"] for item in b["items"]) - b["authorized_machine_hours"]) < 1e-9
    assert b["accounting"]["machine_hours_spent"] < b["authorized_machine_hours"]
    print(json.dumps(dict(status="T04_H_PREFLIGHT_PASS_NOT_LAUNCHED",job=name,
        registration_sha256=pin,allocation_sha256=sha(budget_path),
        configuration_sha256=sha(config_path),source_priors_grid_unchanged=True,
        new_seed=reference["sampler"]["seed"] != config["jobs"][name]["sampler"]["seed"],
        maxcall=config["jobs"][name]["sampler"]["maxcall"],nlive=1024)))


if __name__ == "__main__":
    main()
