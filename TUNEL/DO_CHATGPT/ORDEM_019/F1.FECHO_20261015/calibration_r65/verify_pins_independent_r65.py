"""Read-only custody audit of R65 sources and prospective append plan."""
from pathlib import Path
import hashlib
import json
import datetime as dt

BASE = Path(__file__).resolve().parent


def read(name):
    return json.loads((BASE / name).read_text(encoding="utf-8-sig"))


def pin(path):
    p = Path(path)
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


def verify(row):
    assert pin(row["path"])["sha256"] == row["sha256"], row["path"]
    if "bytes" in row:
        assert Path(row["path"]).stat().st_size == row["bytes"], row["path"]
    return pin(row["path"])


def main():
    manifests = []
    for name, keys in [("calibration/DELIVERY_CALIBRATION_R65.json", ["files", "reused"]), ("sources/DELIVERY_R1.json", ["artifacts"])]:
        document = read(name)
        checked = [verify(row) for key in keys for row in document[key]]
        manifests.append({"manifest": pin(BASE / name), "checked": checked})
    checks = []
    for name, key, style in [("calibration/SOURCE_PINS_AND_ANCHORS_R65.json", "sources", "numbered"), ("sources/SOURCE_PINS_AND_ANCHORS_R1.json", "scientific_sources", "plain")]:
        document = read(name)
        for source in document[key]:
            measured = verify(source)
            lines = Path(source["path"]).read_text(encoding="utf-8-sig").splitlines()
            anchors = source["anchors"] if style == "numbered" else source["excerpts"]
            for row in anchors:
                first = row["first_line"] if style == "numbered" else row["line_start"]
                last = row["last_line"] if style == "numbered" else row["line_end"]
                actual = "\n".join(f"{i}: {lines[i-1]}" for i in range(first, last + 1)) if style == "numbered" else "\n".join(lines[first-1:last])
                assert actual == row["text"], (source["path"], first, last)
                if "excerpt_utf8_lf_sha256" in row:
                    assert hashlib.sha256(actual.encode("utf-8")).hexdigest() == row["excerpt_utf8_lf_sha256"]
            checks.append({**measured, "manifest": name, "line_ranges_checked": len(anchors)})
    thermal = read("THERMAL_ROUTE_SOURCE_R65.json")
    verify(thermal["source"])
    lines = Path(thermal["source"]["path"]).read_text(encoding="utf-8-sig").splitlines()
    for anchor in thermal["anchors"]:
        assert "\n".join(lines[anchor["first"]-1:anchor["last"]]) == anchor["text"]
    canonical = [verify(row["expected"]) for row in read("CANONICAL_PINS_R65.json")["checks"]]
    plan = read("MEMORY_PLAN_R65.json")
    verify(plan["report"])
    verify(plan["applier"])
    prior = json.loads((BASE.parent / "output_field_r64/MEMORY_PLAN_R64.json").read_text(encoding="utf-8-sig"))
    assert len(plan["surfaces"]) == len({r["path"] for r in plan["surfaces"]}) == 8
    assert [r["path"] for r in plan["surfaces"]] == [r["path"] for r in prior["surfaces"]]
    baselines = []
    for row in plan["surfaces"]:
        verify(row["before"])
        verify(row["append"])
        raw = Path(row["path"]).read_bytes()
        extra = Path(row["append"]["path"]).read_bytes()
        assert len(raw) == row["before_bytes"]
        assert plan["marker"].encode() not in raw
        assert hashlib.sha256(raw + extra).hexdigest() == row["after_sha256"]
        baselines.append({"path": row["path"], "before_sha256": row["before"]["sha256"], "before_bytes": len(raw), "append_bytes": len(extra), "after_sha256": row["after_sha256"]})
    assert not (BASE / "MEMORY_APPLIED_R65.json").exists()
    receipt = {
        "status": "PASS_PIN_AND_LINE_CUSTODY",
        "reviewer": "codex-mission-memory-review",
        "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "manifests": manifests,
        "source_occurrences": len(checks),
        "unique_sources": len({r["path"] for r in checks}),
        "line_ranges_checked": sum(r["line_ranges_checked"] for r in checks),
        "sources": checks,
        "thermal_source": pin(BASE / "THERMAL_ROUTE_SOURCE_R65.json"),
        "canonical_pins": canonical,
        "memory_plan": pin(BASE / "MEMORY_PLAN_R65.json"),
        "memory_baselines": baselines,
        "scientific_sources_executed_or_imported": False,
        "new_simulations_or_ODE": False,
        "script": pin(__file__),
    }
    p = BASE / "INDEPENDENT_PIN_CHECK_R65.json"
    with p.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"receipt": pin(p), "sources": receipt["source_occurrences"], "unique_sources": receipt["unique_sources"], "ranges": receipt["line_ranges_checked"], "memory_surfaces": len(baselines)}))


if __name__ == "__main__":
    main()
