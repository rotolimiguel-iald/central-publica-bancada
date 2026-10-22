"""Measure failed T07 events using pre-registered alternate PSDs or honest detector subsets."""
import hashlib
import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import measure_rho_catalog_v5 as base

INITIAL_PATH = HERE / "T07_RHO_CATALOG_RESULT_v5.json"
ALT_PATH = HERE / "T07_ALTERNATE_PLAN.json"
INITIAL = json.loads(INITIAL_PATH.read_bytes())
ALT = json.loads(ALT_PATH.read_bytes())
ALT_BY_KEY = {(r["event"], r["detector"]): r for r in ALT["files"]}
DEADLINE = datetime.fromisoformat("2026-09-27T10:28:21.3284588+00:00")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_alt(item):
    path = HERE / item["relative_path"]
    receipt = path.with_name(path.name + ".receipt.json")
    if not path.exists() or not receipt.exists():
        raise FileNotFoundError("ALTERNATE_UNPAID")
    record = json.loads(receipt.read_bytes())
    if record["plan_sha256"] != sha(ALT_PATH) or record["url"] != item["url"]:
        raise ValueError("ALTERNATE_RECEIPT_PLAN_MISMATCH")
    if record["sha256"] != base.sha(path):
        raise ValueError("ALTERNATE_RECEIPT_HASH_MISMATCH")
    return path, sha(receipt)


def recover(event):
    posterior, refs, tm, method = base.posterior_reference(event)
    rows = []
    skipped = []
    for (role, detector), on_item in base.BY_EVENT[event].items():
        if role != "onsource":
            continue
        if detector not in refs:
            skipped.append({"detector": detector, "reason": "NO_POSTERIOR_DETECTOR_TIME"})
            continue
        on_path, on_receipt = base.checked_file(on_item)
        original_item = base.BY_EVENT[event][("offsource", detector)]
        original_path, original_receipt = base.checked_file(original_item)
        tried = []
        chosen = None
        for label, path, receipt in (("original", original_path, original_receipt),):
            try:
                W, noise = base.fit_noise(path)
                chosen = (label, path, receipt, W, noise)
                break
            except Exception as exc:
                tried.append({"source": label, "error": type(exc).__name__ + ":" + str(exc)[:200]})
        if chosen is None and (event, detector) in ALT_BY_KEY:
            item = ALT_BY_KEY[(event, detector)]
            try:
                path, receipt = checked_alt(item)
                W, noise = base.fit_noise(path)
                chosen = ("alternate", path, receipt, W, noise)
            except Exception as exc:
                tried.append({"source": "alternate", "error": type(exc).__name__ + ":" + str(exc)[:200]})
        if chosen is None:
            skipped.append({"detector": detector, "reason": "NO_VALID_PRE_REGISTERED_PSD", "attempts": tried})
            continue
        label, noise_path, noise_receipt, W, noise = chosen
        requested = refs[detector] + 10 * tm
        norm, index, actual = base.measure_on(on_path, W, requested)
        rows.append({"detector": detector, "norm_squared": norm,
                     "noise_degrees_of_freedom": W.shape[0],
                     "requested_GPS": requested, "first_index": index,
                     "first_sample_GPS": actual,
                     "onsource_sha256": base.sha(on_path),
                     "noise_source": label, "offsource_sha256": base.sha(noise_path),
                     "onsource_receipt_sha256": on_receipt,
                     "offsource_receipt_sha256": noise_receipt,
                     **noise})
    if not rows:
        return {"status": "NO_USABLE_DETECTOR", "event": event,
                "skipped_detectors": skipped, "gate_changed": False}
    dof = sum(r["noise_degrees_of_freedom"] for r in rows)
    excess = sum(r["norm_squared"] for r in rows) - dof
    rho = math.sqrt(excess) if excess > 0 else None
    se = math.sqrt(2 * dof + 4 * excess) / (2 * rho) if rho and 2 * dof + 4 * excess > 0 else None
    return {"status": "MEASURED_POSITIVE_POWER_EXCESS" if rho else "MEASURED_NONPOSITIVE_POWER_EXCESS_NO_REAL_RHO",
            "event": event, "reference_method": method,
            "posterior_sha256": base.sha(posterior), "reference_tM_seconds": tm,
            "start_tM": 10, "detectors": rows,
            "skipped_detectors": skipped, "partial_network": bool(skipped),
            "excess_norm_squared": excess, "rho_power_estimate": rho,
            "approximate_standard_error_if_white_gaussian": se,
            "statistical_scope": "Same F4 per-detector whitened 10tM window power and dof subtraction; detector subset selected ONLY for registered quality failure, not signal. Posterior-median time proxy and farther alternate PSD increase systematic uncertainty. Not matched-filter SNR, z, sigma, or physical detection.",
            "gate_changed": False}


def main():
    out = HERE / "results_rho_salvage"
    out.mkdir(exist_ok=True)
    rows = []
    for old in INITIAL["rows"]:
        if old["status"] != "MEASUREMENT_FAILED":
            continue
        event = old["event"]
        if datetime.now(timezone.utc) >= DEADLINE:
            rows.append({"event": event, "status": "T07_DEADLINE_NOT_MEASURED"})
            continue
        started = time.monotonic()
        try:
            result = recover(event)
            raw = (json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
            path = out / (event + ".json")
            with path.open("xb") as handle:
                handle.write(raw)
            summary = {"event": event, "status": result["status"],
                       "rho": result.get("rho_power_estimate"),
                       "excess": result.get("excess_norm_squared"),
                       "detectors_used": [r["detector"] for r in result.get("detectors", [])],
                       "detectors_skipped": [r["detector"] for r in result["skipped_detectors"]],
                       "result_sha256": hashlib.sha256(raw).hexdigest()}
        except Exception as exc:
            summary = {"event": event, "status": "SALVAGE_FAILED",
                       "error": type(exc).__name__ + ":" + str(exc)[:240]}
        summary["wall_seconds"] = time.monotonic() - started
        rows.append(summary)
        print(json.dumps(summary), flush=True)
    report = {"status": "T07_RHO_QUALITY_SALVAGE", "created_utc": datetime.now(timezone.utc).isoformat(),
              "initial_catalog_sha256": sha(INITIAL_PATH), "alternate_plan_sha256": sha(ALT_PATH),
              "runner_sha256": sha(Path(__file__)), "rows": rows, "gate_changed": False}
    target = HERE / "T07_RHO_SALVAGE_RESULT.json"
    raw = (json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    with target.open("xb") as handle:
        handle.write(raw)
    print(json.dumps({"sha256": hashlib.sha256(raw).hexdigest(),
                      "measured": sum(r["status"].startswith("MEASURED_") for r in rows)}))


if __name__ == "__main__":
    main()
