"""Independent receipt/arithmetic audit; never imports or reruns the campaign."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import math

BASE = Path(__file__).resolve().parent


def read(name):
    return json.loads((BASE / name).read_text(encoding="utf-8-sig"))


def pin(path):
    p = Path(path)
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def verify(row):
    p = Path(row["path"])
    actual = pin(p)
    assert actual["sha256"] == row["sha256"], str(p)
    if "bytes" in row:
        assert p.stat().st_size == row["bytes"], str(p)
    return actual


def close(a, b, tolerance=1e-12):
    assert abs(a - b) <= tolerance, (a, b, tolerance)
    return abs(a - b)


def complex_value(value):
    return complex(value["re"], value["im"])


def decode(rows, field):
    xx, pp, xp, px = [rows[k][field][0][1] for k in ("XX", "PP", "XP", "PX")]
    return complex(xx - pp, xp + px) / 2, complex(xx + pp, xp - px) / 2


def main():
    source_manifest = read("sources/FOCAL_SOURCE_PINS_R1.json")
    source_checks = []
    for row in source_manifest["sources"]:
        measured = verify(row)
        lines = Path(row["path"]).read_text(encoding="utf-8-sig").splitlines()
        for anchor in row.get("anchors", []):
            actual = "\n".join(f"{i}: {lines[i-1]}" for i in range(anchor["first"], anchor["last"] + 1))
            assert actual == anchor["text"]
        source_checks.append({**measured, "anchors": len(row.get("anchors", []))})
    deliveries = {}
    for name, field in [("sources/DELIVERY_R1.json", "files"), ("output/DELIVERY_OUTPUT_R64.json", "evidence"), ("output/FREEZE_R64.json", "files"), ("output/PLAN_OUTPUT_R64.json", "sources")]:
        deliveries[name] = [verify(row) for row in read(name)[field]]
    canonical = [verify(row["expected"]) for row in read("CANONICAL_PINS_R64.json")["checks"]]
    result = read("output/RESULT_OUTPUT_R64.json")
    start = read("output/START_R64.json")
    freeze = read("output/FREEZE_R64.json")
    command = read("output/COMMAND_RESULT_R64.json")
    preexec = read("PREEXEC_REVIEW_R64.json")
    delivery = read("output/DELIVERY_OUTPUT_R64.json")
    assert command["exit_code"] == 0 and command["execution_count"] == delivery["execution_count"] == 1
    assert result["status"] == "PASS_CONDITIONAL_FILTERED_OUTPUT"
    assert len(result["checks"]) == len({x["name"] for x in result["checks"]}) == 89
    relation_counts = {"le": 0, "gt": 0}
    for check in result["checks"]:
        assert math.isfinite(check["value"]) and math.isfinite(check["bound"])
        expected = check["value"] <= check["bound"] if check["relation"] == "le" else check["value"] > check["bound"]
        assert check["passed"] is expected and expected
        relation_counts[check["relation"]] += 1
    assert delivery["checks"]["total"] == delivery["checks"]["passed"] == 89
    verify(result["freeze"])
    verify(start["freeze"])
    dates = [preexec["created_utc"], freeze["created_utc"], command["started_utc"], result["started_utc"], result["ended_utc"], command["ended_utc"]]
    assert [dt.datetime.fromisoformat(x) for x in dates] == sorted(dt.datetime.fromisoformat(x) for x in dates)
    assert start["started_utc"] == result["started_utc"]
    assert (BASE / "output/STDERR_R64.txt").read_bytes() == b""
    stdout = json.loads((BASE / "output/STDOUT_R64.txt").read_text(encoding="utf-8-sig"))
    assert stdout["checks"] == 89 and stdout["failed"] == []
    verify(stdout["result"])
    check_receipt = read("INTEGRATION_R64_CHECK_RESULT.json")
    assert check_receipt["exit_code"] == 0 and check_receipt["result"]["result"]["ready"]
    assert check_receipt["result"]["result"]["receipt"]["revision"] == freeze["mission_revision"] == 471

    # Closed-form arithmetic against the existing result only. No ODE or model import.
    controls = result["controls"]
    probability = -math.expm1(-1)
    arithmetic = {
        "emission_probability": close(controls["p_emitted"], probability),
        "single_second": close(controls["single"]["second"][0][0], 0.5 + probability, 1e-8),
        "vacuum_second": close(controls["vacuum"]["second"][0][0], 0.5, 1e-8),
        "ordered_kernel": close(complex_value(controls["ordered_QRT"]), math.exp(-0.5)),
        "pair_target": close(complex_value(controls["C_emitted"]), probability * complex(1, 1) / (2 * math.sqrt(2)), 1e-8),
        "pair_B_zero": close(complex_value(controls["B_emitted"]), 0, 1e-8),
    }
    assert controls["noise_omitted"]["second"][0][0] == 0
    full = result["full_model"]
    rows = full["phase_runs"]
    centered_residual = 0.0
    for value in rows.values():
        for i in range(2):
            for j in range(2):
                centered_residual = max(centered_residual, close(value["covariance"][i][j], value["second"][i][j] - value["means"][i] * value["means"][j]))
    for field, suffix in [("second", ""), ("covariance", "_centered")]:
        c, b = decode(rows, field)
        arithmetic["C_decode" + suffix] = close(c, complex_value(full["C_filtered" + suffix]))
        arithmetic["B_decode" + suffix] = close(b, complex_value(full["B_filtered" + suffix]))
    arithmetic["centering"] = centered_residual
    report = (BASE / "RELATORIO_R64.txt").read_text(encoding="utf-8-sig")
    for name in ("C_filtered", "B_filtered", "C_filtered_centered", "B_filtered_centered"):
        assert str(full[name]) in report, name

    plan = read("MEMORY_PLAN_R64.json")
    assert len(plan["surfaces"]) == 8 and len({r["path"] for r in plan["surfaces"]}) == 8
    prior = json.loads((BASE.parent / "physical_receiver_r63/MEMORY_PLAN_R63.json").read_text(encoding="utf-8-sig"))
    assert [r["path"] for r in plan["surfaces"]] == [r["path"] for r in prior["surfaces"]]
    verify(plan["report"])
    verify(plan["applier"])
    baselines = []
    for row in plan["surfaces"]:
        verify(row["before"])
        verify(row["append"])
        raw = Path(row["path"]).read_bytes()
        extra = Path(row["append"]["path"]).read_bytes()
        assert len(raw) == row["before_bytes"]
        assert plan["marker"].encode() not in raw
        assert hashlib.sha256(raw + extra).hexdigest() == row["after_sha256"]
        baselines.append({"path": row["path"], "before_sha256": hashlib.sha256(raw).hexdigest(), "before_bytes": len(raw), "append_bytes": len(extra), "expected_after_sha256": row["after_sha256"]})
    assert not (BASE / "MEMORY_APPLIED_R64.json").exists()
    projection = read("REVIEWER_PROJECT_FINAL_R64.json")["result"]["projection"]
    output = {
        "status": "PASS_RECEIPTS_AND_RECORDED_ARITHMETIC",
        "reviewer": "codex-mission-memory-review",
        "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "constructor_checks_recomputed_from_recorded_values": {"count": 89, "relations": relation_counts},
        "constructor_campaign_reexecuted": False,
        "new_ODE_or_model_import": False,
        "scalar_and_decoder_residuals": arithmetic,
        "source_pins_and_line_anchors": source_checks,
        "delivery_and_freeze_pins": deliveries,
        "canonical_pins": canonical,
        "timeline": dates,
        "command_exit_code": 0,
        "calculation_seconds": result["seconds"],
        "memory_baselines": baselines,
        "mission_revision": projection["revision"],
        "mission_state_sha256": projection["state_sha256"],
        "script": pin(__file__),
    }
    dest = BASE / "INDEPENDENT_CUSTODY_R64.json"
    with dest.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(output, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"artifact": pin(dest), "sources": len(source_checks), "anchors": sum(r["anchors"] for r in source_checks), "checks": relation_counts, "memory_surfaces": len(baselines), "revision": projection["revision"]}))


if __name__ == "__main__":
    main()
