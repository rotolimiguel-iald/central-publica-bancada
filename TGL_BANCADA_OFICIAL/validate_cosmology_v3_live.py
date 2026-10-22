"""Verify deployed V3 + scenario roundtrip without restarting resident GW."""
import hashlib
import json
import math
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from validate_cosmology_live import gw_signature

HERE = Path(__file__).resolve().parent
BASE = "http://127.0.0.1:18766/api/cosmology"


def request(path, data=None):
    req = urllib.request.Request(path, None if data is None else json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


def main():
    overview = request(BASE + "/status")
    file = HERE / "state" / ("validation_cosmology_v3_" + overview["engine_generation"][:16] + ".json")
    if file.exists():
        print("Receipt already present: " + str(file))
        return
    before = json.loads((HERE / "state/cosmos_v3_gw_before.json").read_text())["gw"]
    common = {key: value["default"] for key, value in overview["parameters"].items()}
    cases = [
        ("zero", {"model_id": "V3_TOTAL_BETA_ZERO"}),
        ("fixed", {"model_id": "TGL_V3_TOTAL_FIXED_BETA"}),
        ("cursor", {"model_id": "TGL_V3_TOTAL_FIXED_BETA", "redshift": 2.33}),
        ("scale", {"model_id": "TGL_V3_TOTAL_FIXED_BETA", "rd_mpc": 150}),
        ("hubble", {"model_id": "TGL_V3_TOTAL_FIXED_BETA", "H0": 73}),
        ("extreme_low", {"model_id": "TGL_V3_TOTAL_FIXED_BETA", "H0": 40, "omega_m": .1}),
        ("extreme_high", {"model_id": "TGL_V3_TOTAL_FIXED_BETA", "H0": 100, "omega_m": .5}),
    ]
    calls = {}
    for name, changes in cases:
        result = request(BASE + "/evaluate", {**common, **changes})
        assert result["status"] == "ok", result
        assert result["engine_generation"] == overview["engine_generation"]
        assert result["memory"]["load_id"] == overview["memory"]["load_id"]
        assert result["memory"]["source_reads_since_load"] == 0
        assert result["chi2"]["method"] == "CHOLESKY_FULL_COVARIANCE"
        assert len(result["observations"]) == 13
        assert [(p["z"], p["type"]) for p in result["observations"]] == [
            (p["z"], p["type"]) for p in overview["dataset"]["points"]]
        assert result["model"]["status"] == "V3_TOTAL_FLUID_PRIMITIVE__CONDITIONAL"
        q = result["quadrature"]
        assert q["e0_residual"] < 5e-6 and q["max_relative_e_refinement"] < 1e-5
        calls[name] = result
    assert calls["fixed"]["model"]["execution"]["beta"] == 7.2973525693e-3 * math.sqrt(math.e)
    assert calls["zero"]["model"]["execution"]["beta"] == 0
    assert calls["fixed"]["chi2"] == calls["cursor"]["chi2"]
    assert calls["cursor"]["model"]["execution"]["background_cache_hit"]
    assert calls["scale"]["model"]["execution"]["background_cache_hit"]
    assert calls["zero"]["observations"] != calls["fixed"]["observations"]
    saved = []
    for name, label in (("zero", "V3 · referência β = 0"), ("fixed", "V3 · β fixo α√e")):
        inputs = {**common, "model_id": calls[name]["model"]["id"]}
        candidates = request(BASE + "/scenarios")["scenarios"]
        existing = [item for item in candidates if item["label"] == label
                    and item["engine_sha256"] == overview["engine_sha256"]
                    and item["parameters"] == common]
        summary = existing[0] if existing else request(BASE + "/scenarios", {"label": label, "parameters": inputs})
        record = request(BASE + "/scenarios/" + summary["id"])
        assert record["evaluation"]["chi2"] == calls[name]["chi2"]
        payload = {key: val for key, val in record.items() if key != "sha256"}
        digest = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                separators=(",", ":"), allow_nan=False).encode()).hexdigest()
        assert digest == record["sha256"]
        saved.append(summary)
    exported = request(BASE + "/exports", {
        "reference_parameters": {**common, "model_id": "V3_TOTAL_BETA_ZERO"},
        "current_parameters": {**common, "model_id": "TGL_V3_TOTAL_FIXED_BETA"}})
    assert Path(exported["path"]).is_file(), "Export not persisted on host"
    archive = request("http://127.0.0.1:18766" + exported["download_url"])
    assert archive, "Export viewer returned empty data"
    after = gw_signature(request("http://127.0.0.1:18765/api/universe/status"))
    assert before == after, "GW resident load changed"
    report = {"created_utc": datetime.now(timezone.utc).isoformat(), "status": "PASS_CONDITIONAL_V3_AND_SCENARIOS",
              "overview": overview, "calls": calls, "saved_scenarios": saved,
              "gw_unchanged": True, "gw": after, "export": exported,
              "statistical_scope": "MANUAL_PARAMETERS_NOT_FIT_OR_SIGMA"}
    encoded = json.dumps(report, ensure_ascii=False, indent=2).encode()
    tmp = file.with_suffix(".tmp")
    with tmp.open("xb") as out:
        out.write(encoded)
    assert tmp.stat().st_size == len(encoded)
    tmp.replace(file)
    print(json.dumps({"receipt": str(file), "chi2": {key: val["chi2"]["value"] for key, val in calls.items()},
                      "milliseconds": {key: val["elapsed_ms"] for key, val in calls.items()},
                      "gw_load_id": after["load_id"], "scenarios": saved}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
