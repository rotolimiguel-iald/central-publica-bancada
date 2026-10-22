"""Read-only artifact verification for the independent R57 review; no builds."""
from pathlib import Path
import datetime
import hashlib
import json
import re

OUT = Path(__file__).resolve().parent.parent
CHECKED = {}
MISMATCHES = []


def pin(path):
    p = Path(path)
    raw = p.read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def verify(item):
    p = item["path"]
    measured = CHECKED.setdefault(p, pin(p))
    good = measured["sha256"] == item["sha256"]
    if "bytes" in item:
        good = good and measured["bytes"] == item["bytes"]
    if not good:
        MISMATCHES.append({"expected": item, "measured": measured})
    return good


def walk(obj):
    if isinstance(obj, dict):
        if isinstance(obj.get("path"), str) and isinstance(obj.get("sha256"), str):
            verify(obj)
        for key, value in obj.items():
            if key not in {"dependencies", "LEAN_PATH", "command"}:
                walk(value)
    elif isinstance(obj, list):
        for value in obj:
            walk(value)


def read(rel):
    p = OUT / rel
    CHECKED[str(p)] = pin(p)
    return json.loads(p.read_text(encoding="utf-8"))


def axiom_report(text, expected):
    entries = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", text, re.S)
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    bad = [(name, body) for name, body in entries if set(x.strip() for x in body.split(",")) - allowed]
    assert len(entries) == expected, (len(entries), expected)
    assert not bad and "sorryAx" not in text and "error:" not in text, bad
    return {"count": len(entries), "declarations": [x[0] for x in entries], "only_allowed_trio": True}


def main():
    delivery = read("device_clock_r57/DELIVERY_R57.json")
    walk(delivery)
    clock = read("device_clock_r57/builds/20261017T092400_700789Z/RESULT.json")
    walk(clock)
    assert clock["exit_code"] == 0
    builds = [{"receipt": pin(OUT / "device_clock_r57/builds/20261017T092400_700789Z/RESULT.json"),
               "exit_code": 0, "seconds": clock["seconds"],
               "axioms": axiom_report(Path(clock["log"]["path"]).read_text(encoding="utf-8"), 6)}]
    selected = {"ModularFlowSpectrum", "TheImportedSecondQuantization", "PhysicalCompactNetCovarianceR1",
                "PhysicalCanonicalWedgeEqualityR3", "PhysicalCanonicalNetCompleteR1",
                "PhysicalCompactNetAssemblyR1", "LorentzFutureRepresentationR1"}
    for stamp, count in [("20261017T092256_582881Z", 3), ("20261017T092301_432915Z", 20)]:
        rel = f"device_continuum_r57/attempts/{stamp}/RECEIPT.json"
        rec = read(rel)
        walk(rec)
        start = read(f"device_continuum_r57/attempts/{stamp}/START_RECEIPT.json")
        assert start["source"] == rec["source"]
        assert start["source_original"] == rec["source_original"]
        assert rec["exit_code"] == 0 and rec["source_unchanged"]
        assert Path(rec["source"]["path"]).read_bytes() == Path(rec["source_original"]["path"]).read_bytes()
        deps = [x for x in rec["dependencies"] if Path(x["path"]).stem in selected]
        for item in deps:
            verify(item)
        log = next(x for x in rec["artifacts"] if Path(x["path"]).name == "BUILD.log")
        builds.append({"receipt": pin(OUT / rel), "exit_code": 0, "seconds": rec["seconds"],
                       "source": rec["source"], "source_original": rec["source_original"],
                       "start_final_source_pins_equal": True, "snapshot_equals_current": True,
                       "readonly_dependencies_unchanged_reported_by_builder": rec["readonly_dependencies_unchanged"],
                       "selected_dependency_pins_verified": len(deps),
                       "axioms": axiom_report(Path(log["path"]).read_text(encoding="utf-8"), count)})
    for rel in ["review_r57/R57_CLOCK_AND_CUSTODY_REVIEW_R1.json",
                "review_r57/R57_TABLE_CUSTODY_REVIEW_ADDENDUM_R1.json",
                "continuity_r57/SOURCE_JAN09_TABLE_CUSTODY_R57.json",
                "device_continuum_r57/PACKET_CANDIDATE_R1.json"]:
        obj = read(rel)
        if "review_r57/" not in rel:
            walk(obj)
    result = {"schema": "iald-r57-independent-pin-check/v1", "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "reviewer": "codex-mission-memory-review", "ok": not MISMATCHES,
              "scope": "Source/artifact bytes and selected reused dependency pins; no symbolic rerun or Lean build. Whole dependency stability is a builder-receipt statement, not independently rehashed here.",
              "builds": builds, "unique_files_measured": len(CHECKED),
              "pins": list(CHECKED.values()), "mismatches": MISMATCHES,
              "runner": pin(__file__)}
    dest = OUT / "review_r57/PIN_VERIFICATION_LAYER2_BASE_R1.json"
    with dest.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps({"result": pin(dest), "ok": result["ok"], "files": len(CHECKED),
                      "prints": [x["axioms"]["count"] for x in builds], "mismatches": MISMATCHES}, ensure_ascii=False))


if __name__ == "__main__":
    main()
