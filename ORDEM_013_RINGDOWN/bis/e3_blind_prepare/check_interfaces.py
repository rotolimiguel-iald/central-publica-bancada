"""Finite deterministic interface checks using selected pure AST functions.

No production import/main, active registry gate, files fetched, waveform or PE.
The load_jobs fixture uses in-memory paths and a MOCK witness verifier only.
"""
import ast
import copy
import hashlib
import json
import math
import re
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from build_readiness import HERE, B, ROOT, write, sha

CHECKS = []


def check(name, operation, rejected=False):
    try:
        value = operation()
    except (ValueError, KeyError) as error:
        if not rejected:
            raise
        CHECKS.append({"name": name, "pass": True, "expected_rejection": type(error).__name__})
    else:
        if rejected or value is False:
            raise RuntimeError("Finite check failed: " + name)
        CHECKS.append({"name": name, "pass": True})


def extract(path, names, namespace):
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    if {n.name for n in nodes} != set(names):
        raise ValueError("Missing exact pure function")
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), namespace)


def main():
    code = B / "bis/e2_code"
    names = ("mass_1", "mass_2", "chi_1", "chi_2", "luminosity_distance", "theta_jn", "phase", "ra", "dec", "psi", "geocent_time")
    ns = {"math": math, "re": re, "json": json, "datetime": datetime, "timezone": timezone,
          "PHYSICAL": names, "DEFORMATIONS": ("dtau220", "dtau440", "domega220", "domega440")}
    extract(code / "registration_guard.py", ["positive", "integer", "utc", "strict_json"], ns)
    extract(code / "pe_runner.py", ["validate_config"], ns)
    url_ns = {"urllib": urllib}
    extract(code / "fetch_registered.py", ["validate_url"], url_ns)
    url_ns["ALLOWED_HOSTS"] = {"gwosc.org", "www.gwosc.org", "zenodo.org"}
    reg = json.loads((B / "RINGDOWN_5SIGMA_V1.json").read_bytes())
    pilot = reg["pe_jobs"]["GW250114_PILOT"]
    check("registered pilot config structural only, no execution", lambda: ns["validate_config"](copy.deepcopy(pilot)))
    def config_change(name, value, sampler=False):
        c = copy.deepcopy(pilot)
        (c["sampler"] if sampler else c)[name] = value
        return ns["validate_config"](c)
    for name, value, sampler in (("workers", 29, True), ("check_point", True, True),
                                  ("check_point_plot", True, True), ("duration_s", float("nan"), False),
                                  ("minimum_frequency_hz", 0, False), ("quality_required", [], False),
                                  ("minimum_effective_samples", 0, True), ("seed", -1, True)):
        check("reject " + name, lambda n=name, v=value, s=sampler: config_change(n, v, s), rejected=True)
    check("core permits 25 workers; sidecar cap is separately 24", lambda: config_change("workers", 25, True))
    bad = copy.deepcopy(pilot)
    bad["priors"]["mass_1"] = 40.0
    check("reject fixed physical mass", lambda: ns["validate_config"](bad), rejected=True)
    for url in ("http://gwosc.org/a.hdf5", "https://evil.example/a.hdf5", "https://u:[dado pessoal removido]/a.hdf5", "https://gwosc.org/a.hdf5?token=x", "https://gwosc.org/a.hdf5#fragment"):
        check("fetch rejects " + url, lambda u=url: url_ns["validate_url"](u), rejected=True)
    readiness = json.loads((HERE / "METADATA_READINESS.json").read_bytes())
    count = 0
    for entry in readiness["targets"]:
        for detector in entry["detectors"]:
            for item in detector["files"]:
                check("registered fetch URL shape " + item["filename"], lambda u=item["url"]: url_ns["validate_url"](u))
                count += 1
    check("strict duplicate JSON refused", lambda: ns["strict_json"](b'{"x":1,"x":2}'), rejected=True)

    # Exercise exact extension functions with entirely synthetic state.
    store = {}
    class FakePath:
        def __init__(self, name): self.name = name
        def exists(self): return self.name in store
        def read_bytes(self): return json.dumps(store[self.name], sort_keys=True).encode()
    def fake_sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
    ns.update(contained=lambda name: FakePath(name), sha=fake_sha)
    witnesses = []
    def witness(path, digest, issued, label):
        if path != "MOCK_WITNESS" or label != "allocation_sha256":
            raise ValueError("Mock witness identity")
        witnesses.append((path, digest, issued, label))
    ns["check_witness"] = witness
    extract(code / "registration_guard.py", ["authorize_event", "validate_job_reviews", "load_jobs", "load_authorized_configuration"], ns)
    parent = "a" * 64
    fake_reg = {"registered_utc": "2020-01-01T00:00:00+00:00", "pe_jobs": {}, "downloads": {},
                "calibration_event_ids": ["MOCK_CAL"],
                "test_candidates": {"MOCK_TEST": {"eligible": True, "published_deformation_at_registration": False,
                                    "publication_census_scope": "MOCK_SCOPE", "data_quality_hold": False}},
                "allocation_policy": {"relative_to_Chatgpt": "MOCK_ALLOCATION", "max_job_wall_seconds": 28800}}
    store["MOCK_LICENSE"] = {"status": "MOCK_LICENSE"}
    store["MOCK_REVIEW"] = {"status": "MOCK_REVIEW"}
    extra = {"schema_version": "E2_PE_JOBS_V2", "parent_registration_sha256": parent,
             "jobs": {}, "downloads": {"MOCK_DOWNLOAD": {"license_receipt_relative_to_Chatgpt": "MOCK_LICENSE",
                       "license_receipt_sha256": fake_sha(FakePath("MOCK_LICENSE"))}}}
    def set_extra(value):
        store["MOCK_JOBS"] = copy.deepcopy(value)
        store["MOCK_ALLOCATION"] = {"parent_registration_sha256": parent,
             "registered_utc": "2021-01-01T00:00:00+00:00", "witness_relative_to_Chatgpt": "MOCK_WITNESS",
             "jobs_relative_to_Chatgpt": "MOCK_JOBS", "jobs_sha256": fake_sha(FakePath("MOCK_JOBS"))}
    set_extra(extra)
    check("exact loader accepts download-only extension jobs empty", lambda: "MOCK_DOWNLOAD" in ns["load_authorized_configuration"](fake_reg, parent)["downloads"])
    check("allocation witness called in fixture", lambda: bool(witnesses))
    store["MOCK_ALLOCATION"]["parent_registration_sha256"] = "b"*64
    check("wrong allocation parent refused", lambda: ns["load_jobs"](fake_reg,parent), rejected=True)
    set_extra(extra)
    store["MOCK_JOBS"]["schema_version"] = "wrong"
    check("changed jobs bytes refused", lambda: ns["load_jobs"](fake_reg,parent), rejected=True)
    set_extra(extra)
    store["MOCK_LICENSE"]["status"] = "CHANGED"
    check("changed per-file license receipt refused", lambda: ns["load_authorized_configuration"](fake_reg,parent), rejected=True)
    store["MOCK_LICENSE"]["status"] = "MOCK_LICENSE"
    review = {"relative_to_Chatgpt": "MOCK_REVIEW", "sha256": fake_sha(FakePath("MOCK_REVIEW")),
              "review_passed": True, "scope": "MOCK_ONLY", "reviewed_utc": "2021-01-01T00:00:00+00:00"}
    extended = copy.deepcopy(extra)
    extended["jobs"] = {"MOCK_NEW_JOB": {"event": "MOCK_TEST", "mode": "blind_test", "wall_budget_seconds": 100,
                                         "publication_metadata_review": review}}
    set_extra(extended)
    check("job extension loads with mock review, not actual admission", lambda: "MOCK_NEW_JOB" in ns["load_jobs"](fake_reg,parent))
    held = copy.deepcopy(fake_reg)
    held["test_candidates"]["MOCK_TEST"]["data_quality_hold"] = True
    check("held mock job requires independent resolution", lambda: ns["load_jobs"](held,parent), rejected=True)
    collision = copy.deepcopy(fake_reg)
    collision["pe_jobs"] = {"MOCK_NEW_JOB": {"mode": "calibration"}}
    check("static job replacement refused", lambda: ns["load_jobs"](collision,parent), rejected=True)
    too_long = copy.deepcopy(extended)
    too_long["jobs"]["MOCK_NEW_JOB"]["wall_budget_seconds"] = 28801
    set_extra(too_long)
    check("dynamic job above 8h refused", lambda: ns["load_jobs"](fake_reg,parent), rejected=True)
    pins = json.loads((HERE / "SOURCE_PINS.json").read_bytes())["sources_sha256_relative_to_Chatgpt"]
    for relative, digest in pins.items():
        check("source unchanged " + relative, lambda p=ROOT/relative, h=digest: sha(p)==h)
    write("FINITE_INTERFACE_CHECKS.json", {"status": "PASS_FINITE_METADATA_AND_MOCK_INTERFACES_NOT_ADMISSION",
          "checks": CHECKS, "count": len(CHECKS), "download_URLs_shape_checked": count,
          "source_sha256": {name: sha(code/name) for name in ("registration_guard.py", "fetch_registered.py", "pe_runner.py")},
          "script_sha256": sha(Path(__file__)),
          "limits": ["No frozen module imports or main functions", "Mock witness is not cryptographic/temporal authorization",
                     "No real candidate admitted by these tests", "No byte download, prior-wide LAL evaluation, strain, posterior or PE",
                     "Metadata SNR projections tested separately against 72 existing fit-grid scalars"]})
    print(json.dumps({"count": len(CHECKS), "status": "PASS", "download_URLs": count}))


if __name__ == "__main__":
    main()
