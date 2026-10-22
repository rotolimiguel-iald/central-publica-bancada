"""Optional metadata-only candidate renderer. NOT EXECUTED during preparation.

This is not a launcher, scientific validator, E2 activation verifier, or scheduler.
Outputs never go to active allocation/jobs/witness paths. No production imports.
See GENERATOR_INPUT.md; complete scientific/config review remains mandatory.
"""
import argparse
import hashlib
import json
import math
import os
import re
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
ROOT = BASE.parent
LIMIT = 25_000_000
HEX = re.compile(r"[0-9a-f]{64}\Z")
SLUG = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,100}\Z")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("Nonfinite JSON constant: " + value)


def local_path(value, parent=ROOT):
    require(isinstance(value, str) and value.strip(), "Missing relative path")
    normalized = value.replace("\\", "/")
    require(not Path(normalized).is_absolute() and ":" not in normalized,
            "Relative paths only")
    path = (ROOT / normalized).resolve()
    require(path.is_relative_to(parent.resolve()), "Path outside allowed subtree")
    return path


def read_json(path):
    require(path.is_file() and path.stat().st_size <= LIMIT, "Missing or oversized JSON")
    raw = path.read_bytes()
    require(len(raw) <= LIMIT, "JSON grew beyond limit")
    value = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_object,
                       parse_constant=reject_constant)
    require(isinstance(value, dict), "JSON object required")
    return value, hashlib.sha256(raw).hexdigest()


def pinned_json(reference, expected_name):
    require(isinstance(reference, dict) and HEX.fullmatch(reference["sha256"]), "Bad pin")
    path = local_path(reference["relative_to_Chatgpt"])
    require(path.name == expected_name, "Only designated metadata filenames may be read")
    value, digest = read_json(path)
    require(digest == reference["sha256"], "Metadata pin changed")
    return value, path, digest


def utc(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(result.tzinfo is not None and result.utcoffset().total_seconds() == 0,
            "Explicit UTC required")
    return result


def positive(value):
    require(type(value) in (int, float) and math.isfinite(value) and value > 0,
            "Positive finite numeric value required")
    return value


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def publish_exclusive(path, raw):
    # Pending bytes retained visibly if linking/publication fails.
    pending = path.with_name(path.name + ".pending")
    with pending.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    require(pending.stat().st_size == len(raw), "Incomplete candidate write")
    os.link(pending, path)
    pending.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proposal", type=Path)
    args = parser.parse_args()
    proposal_path = args.proposal.resolve()
    require(proposal_path.is_relative_to(HERE), "Proposal must be inside this sidecar")
    proposal, proposal_hash = read_json(proposal_path)
    require(proposal["schema_version"] == "E3_ALLOCATION_PROPOSAL_V1", "Wrong proposal schema")
    require(SLUG.fullmatch(proposal["slug"]), "Unsafe candidate slug")
    reg, _, digest = pinned_json(proposal["registration"], "RINGDOWN_5SIGMA_V1.json")
    require(reg["status"] == "REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST", "Not registered E2")
    # Activation is deliberately not certified here; the frozen controller owns that check.
    budget_ref = {"relative_to_Chatgpt": reg["budget_relative_to_Chatgpt"], "sha256": reg["budget_sha256"]}
    budget, _, budget_hash = pinned_json(budget_ref, "PART_B_BUDGET_START.json")
    controller, controller_path, controller_hash = pinned_json(proposal["pilot_controller"], "CONTROLLER.json")
    convergence, convergence_path, convergence_hash = pinned_json(proposal["pilot_convergence"], "PRIVATE_CONVERGENCE.json")
    require(controller_path.parent == convergence_path.parent, "Pilot receipts from different jobs")
    require(controller["registration_sha256"] == convergence["registration_sha256"] == digest, "Pilot parent differs")
    require(controller["job"] in reg["pe_jobs"], "Pilot must be a static registered job")
    require(reg["pe_jobs"][controller["job"]]["mode"] == "calibration" and controller["blind"] is False,
            "Only nonblind calibration cost receipts are accepted")
    require(controller["status"] == "CHILD_COMPLETED_REQUIRES_REVIEW" and controller["returncode"] == 0
            and controller["cleanup"]["group_absent"] is True, "Incomplete pilot controller")
    require(convergence["accepted_for_analysis"] is True, "Partial cost is not converged-pilot cost")
    pilot_wall = positive(controller["wall_seconds"])
    cost = convergence["cost"]
    for name in ("sampler_ncall", "likelihood_calls", "source_calls"):
        require(type(cost[name]) is int and cost[name] >= 0, "Missing distinct pilot counters")
    now = datetime.now(timezone.utc)
    issued = utc(proposal["allocation_registered_utc"])
    require(utc(reg["registered_utc"]) <= utc(controller["started_utc"])
            <= utc(controller["finished_utc"]) <= issued <= now, "Invalid cost/allocation chronology")
    deadline = utc(budget["hard_deadline_utc"])
    remaining = (deadline - now).total_seconds()
    require(remaining > 0, "Global deadline expired")
    policy = reg["allocation_policy"]
    allocation_target = local_path(policy["relative_to_Chatgpt"], BASE)
    require(not allocation_target.exists(), "Existing allocation: successor requires separate review")
    jobs_target = local_path(proposal["jobs_relative_to_Chatgpt"], BASE)
    witness_target = local_path(proposal["witness_relative_to_Chatgpt"], ROOT / "TUNEL" / "DO_CHATGPT")
    require(not jobs_target.exists() and not witness_target.exists(), "Future destinations must be new")
    require(jobs_target != allocation_target and not jobs_target.is_relative_to(HERE), "Invalid publication target")
    jobs = proposal["jobs"]
    require(isinstance(jobs, dict) and jobs, "Explicit nonempty jobs decision required")
    order = proposal["ordered_job_names"]
    require(isinstance(order, list) and len(order) == len(jobs) and set(order) == set(jobs), "Order must contain every job once")
    require(not set(jobs).intersection(reg["pe_jobs"]), "Cannot replace a static job")
    schema, _ = read_json(HERE / "CONTRACT_SCHEMA.json")
    slugs = {job["output_directory_name"] for job in reg["pe_jobs"].values()}
    total_wall = 0.0
    for name in order:
        cfg = jobs[name]
        require(SLUG.fullmatch(name), "Unsafe job name")
        require(set(schema["job_required"]) <= set(cfg), "Incomplete config")
        require(cfg["variant"] in ("pilot_all_four_free", "220_plus_440_free")
                and cfg["fixed_deformation_parameters"] == {}, "This sidecar requires all four deviations free")
        require(cfg["privacy_mode"] == "procedural_same_host", "Privacy contract differs")
        wall = positive(cfg["wall_budget_seconds"])
        require(wall <= min(28800, positive(policy["max_job_wall_seconds"])), "Wall cap exceeded")
        workers = cfg["sampler"]["workers"]
        require(type(workers) is int and 1 <= workers <= 24, "Worker cap exceeded")
        slug = cfg["output_directory_name"]
        require(SLUG.fullmatch(slug) and slug not in slugs and not (BASE / "cache" / slug).exists(), "Output reused/unsafe")
        slugs.add(slug)
        require(set(cfg["priors"]) == set(schema["prior_names_exact"]), "Exact prior names required")
        require(all(isinstance(p, dict) and set(schema["free_prior_required"]) <= set(p)
                    for p in cfg["priors"].values()), "Free prior dictionaries required")
        require(set(schema["sampler_required"]) <= set(cfg["sampler"]), "Incomplete sampler")
        for flag in schema["sampler_optional_required_false_if_present"]:
            require(cfg["sampler"].get(flag, False) is False, "Checkpoint forbidden")
        event = cfg["event"]
        if cfg["mode"] == "blind_test":
            entry = reg["test_candidates"][event]
            require(event not in reg["calibration_event_ids"] and entry["eligible"] is True
                    and entry["published_deformation_at_registration"] is False, "Ineligible blind event")
            require(type(entry["data_quality_hold"]) is bool, "Explicit DQ hold required")
            require("publication_metadata_review" in cfg and cfg.get("injection") is None, "Blind-job review/injection contract")
            if entry["data_quality_hold"]:
                require("data_quality_resolution" in cfg, "Unresolved DQ hold")
            # Source hashes and review chronology are checked by frozen load_jobs, not simulated here.
        else:
            require(cfg["mode"] == "calibration" and event in reg["calibration_event_ids"], "Unknown calibration event")
        if cfg.get("injection") is not None:
            inj = cfg["injection"]
            require(set(schema["injection_required"]) <= set(inj), "Incomplete injection")
            require(inj["family"] in schema["injection_families"] and inj["noise_kind"] == "REAL_OFFSOURCE", "Unsupported injection")
            require(cfg["event_GPS"] == reg["event_reference_GPS"][event], "Event anchor changed")
            if inj["family"] == "IMRPhenomXPHM":
                require(all(inj["parameters"][k] == 0 for k in ("dtau220", "dtau440", "domega220", "domega440")), "Non-GR XPHM not implemented")
        total_wall += wall
    reserve = positive(proposal["global_reserve_seconds"])
    require(total_wall + reserve <= remaining, "Serial ceilings and reserve exceed remaining deadline")
    documentation = proposal["decision_documentation"]
    required_docs = {"five_alternatives", "per_job_cost_and_information", "unpaid", "stopping_rules",
                     "selection_rationale", "pilot_independent_review", "reserve_rationale"}
    require(required_docs <= set(documentation), "Missing decision documentation")
    require(len(documentation["five_alternatives"]) == 5, "All five alternatives required")
    require(set(documentation["per_job_cost_and_information"]) == set(jobs), "Missing per-job cost/information documentation")
    jobs_payload = {"schema_version": "E2_PE_JOBS_V2", "parent_registration_sha256": digest,
                    "jobs": {name: jobs[name] for name in order}, "downloads": {}}
    jobs_raw = encoded(jobs_payload)
    allocation = {"parent_registration_sha256": digest, "registered_utc": issued.isoformat(),
                  "witness_relative_to_Chatgpt": proposal["witness_relative_to_Chatgpt"],
                  "jobs_relative_to_Chatgpt": proposal["jobs_relative_to_Chatgpt"],
                  "jobs_sha256": hashlib.sha256(jobs_raw).hexdigest(),
                  "status": "CANDIDATE_NOT_PUBLISHED",
                  "preparation": {"as_of_utc": now.isoformat(), "budget_sha256": budget_hash,
                    "hard_deadline_utc": deadline.isoformat(), "remaining_wall_seconds_at_render": remaining,
                    "serial_job_ceilings_seconds": total_wall, "global_reserve_seconds": reserve,
                    "ordered_job_names": order, "pilot_controller_sha256": controller_hash,
                    "pilot_convergence_sha256": convergence_hash, "observed_pilot_controller_wall_seconds": pilot_wall,
                    "observed_pilot_counters": {k: cost[k] for k in ("sampler_ncall", "likelihood_calls", "source_calls")},
                    "decision_documentation_INPUT_NOT_CERTIFIED": documentation,
                    "limitations": "Not activation/config/science approval; recheck deadline and gates before publication"}}
    allocation_raw = encoded(allocation)
    receipt = {"status": "CANDIDATES_ONLY_NO_WITNESS_NO_LAUNCH", "proposal_sha256": proposal_hash,
               "renderer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "files_sha256": {"JOBS_V2.CANDIDATE.json": hashlib.sha256(jobs_raw).hexdigest(),
                                "ORCAMENTO_40H.CANDIDATE.json": hashlib.sha256(allocation_raw).hexdigest()}}
    destination = HERE / "candidates" / proposal["slug"]
    destination.parent.mkdir(exist_ok=True)
    destination.mkdir(exist_ok=False)
    for name, raw in (("JOBS_V2.CANDIDATE.json", jobs_raw), ("ORCAMENTO_40H.CANDIDATE.json", allocation_raw),
                      ("CANDIDATE_RECEIPT.json", encoded(receipt))):
        publish_exclusive(destination / name, raw)


if __name__ == "__main__":
    main()
