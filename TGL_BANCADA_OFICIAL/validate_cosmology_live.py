"""Verify live cosmology requests, warm data custody, and unchanged GW residency."""
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "http://127.0.0.1:18766"


def request(url, payload=None):
    body = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(url, body, headers={"Content-Type": "application/json"})
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=20) as response:
        result = json.load(response)
    return result, 1000 * (time.perf_counter() - started)


def gw_signature(state):
    fields = ("status", "domain", "load_id", "loaded_files", "total_files", "resident_bytes")
    result = {key: state[key] for key in fields}
    result["strain_hashes"] = sorted(row["strain_array_sha256"] for row in state["series"])
    return result


def main():
    gw_before, _ = request("http://127.0.0.1:18765/api/universe/status")
    initial, _ = request(BASE + "/api/cosmology/status")
    assert initial["status"] == "ok"
    assert initial["dataset"]["n_points"] == 13
    assert initial["dataset"]["n_distinct_redshifts"] == 7
    assert initial["memory"]["source_reads_for_load"] == 2
    load_id = initial["memory"]["load_id"]
    calls = []
    for payload in ({}, {"H0": 73.0}, {"omega_m": 0.25}, {"redshift": 2.33},
                    {"H0": 100.0, "omega_m": 0.1, "rd_mpc": 120.0, "w0": -1.5, "wa": -1.0},
                    {"H0": 40.0, "omega_m": 0.5, "rd_mpc": 170.0, "w0": -0.5, "wa": 1.0}):
        result, elapsed = request(BASE + "/api/cosmology/evaluate", payload)
        assert result["status"] == "ok"
        assert result["memory"]["load_id"] == load_id
        assert result["memory"]["source_reads_since_load"] == 0
        assert result["chi2"]["method"] == "CHOLESKY_FULL_COVARIANCE"
        assert result["model"]["status"] == "EXPLORATORY_BACKGROUND_NOT_TGL_PREDICTION"
        calls.append({"parameters": payload, "http_ms": elapsed, "result": result})
    assert calls[0]["result"]["chi2"]["value"] != calls[1]["result"]["chi2"]["value"]
    assert abs(calls[0]["result"]["chi2"]["value"] - calls[3]["result"]["chi2"]["value"]) < 1e-10
    gw_after, _ = request("http://127.0.0.1:18765/api/universe/status")
    assert gw_signature(gw_before) == gw_signature(gw_after)
    report = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS_EXPLORATORY_UI_BACKEND_NOT_COSMOLOGICAL_FIT",
        "overview": initial, "calls": calls,
        "gw_unchanged": True, "gw": gw_signature(gw_after),
    }
    path = HERE / "state" / ("validation_cosmology_" + load_id + ".json")
    encoded = json.dumps(report, ensure_ascii=False, indent=2).encode()
    temp = path.with_suffix(".tmp")
    if path.exists() or temp.exists():
        raise FileExistsError("Receipt already exists; do not overwrite the measured run")
    with temp.open("xb") as output:
        output.write(encoded)
    if temp.stat().st_size != len(encoded):
        raise OSError("Truncated receipt")
    temp.replace(path)
    print(json.dumps({"receipt": str(path), "cosmology_load_id": load_id,
                      "gw_load_id": gw_after["load_id"], "gw_resident_bytes": gw_after["resident_bytes"],
                      "http_ms": [c["http_ms"] for c in calls],
                      "chi2": [c["result"]["chi2"]["value"] for c in calls]}, indent=2))


if __name__ == "__main__":
    main()
