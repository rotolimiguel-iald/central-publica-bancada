"""Read-only, pinned-runtime preflight for the single registered T04-C job."""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
here = Path(__file__).resolve().parent
ring = here.parents[2]
code = ring / "bis" / "e2_code_v1_1_2"
sys.path.insert(0, str(code))

from registration_guard import checked_registration, load_authorized_configuration, sha
from pe_runner import validate_config

reg, reg_hash = checked_registration()
view = load_authorized_configuration(reg, reg_hash)
name = "GW250114_PILOT_V2_S220_C1"
job = view["pe_jobs"][name]
validate_config(job)
assert job["mode"] == "calibration"
assert job["sampler"]["maxcall"] == 5_738_602
assert job["sampler"]["seed"] == 15_260_303
assert job["wall_budget_seconds"] == 28_800
assert job["sampler"]["workers"] == 24
assert not (ring / "cache" / job["output_directory_name"]).exists()
assert not (here / "branch_c").exists()
allocation = ring / "ORCAMENTO_015_v3.json"
assert sha(allocation) == view["_allocation_sha256"]
print(json.dumps({
    "status": "T04_C_PREFLIGHT_PASS_NO_SCIENCE",
    "job": name,
    "registration_sha256": reg_hash,
    "allocation_sha256": sha(allocation),
    "maxcall": job["sampler"]["maxcall"],
    "seed": job["sampler"]["seed"],
}))
