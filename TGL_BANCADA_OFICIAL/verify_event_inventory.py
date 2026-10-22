"""Reconcile documentary event identities with a specific resident-load receipt."""
import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(path):
    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8-sig")), hashlib.sha256(raw).hexdigest()


def verify(inventory_path, resident_path):
    inventory, inventory_sha = read(inventory_path)
    resident, resident_sha = read(resident_path)
    rows = {key: row for key, row in inventory["files"].items() if row["category"] == "strain"}
    series = {row["id"]: row for row in resident["series"]}
    if len(series) != len(resident["series"]):
        raise ValueError("Duplicate resident identifiers")
    if resident["status"] != "READY" or resident["loaded_files"] != resident["total_files"]:
        raise ValueError("Resident receipt is incomplete")
    if set(series) != {row["resident_id"] for row in rows.values()}:
        raise ValueError("Inventory does not describe this complete load")
    comparisons = 0
    for key, row in rows.items():
        current = series[row["resident_id"]]
        pairs = {
            "detector": (row["detector"], current["detector"]),
            "rows": (row["rows"], current["rows"]),
            "array hash": (row["strain_array_sha256_receipt"], current["strain_array_sha256"]),
            "bytes": (row["source_bytes_receipt"], current["source_bytes"]),
            "mtime": (row["source_mtime_ns_receipt"], current["source_mtime_ns"]),
            "start": (row["interval_gps_half_open"][0], current["gps_start"]),
            "duration": (row["duration_seconds"], current["duration_s"]),
            "sample rate": (row["sample_rate_hz"], 1 / current["dt_s"]),
        }
        for label, (old, new) in pairs.items():
            if old != new:
                raise ValueError(f"{key}: changed {label}")
            comparisons += 1
        if not row["event_id"] or not row["anchors"]:
            raise ValueError(f"{key}: missing documentary anchor")
    computed = {
        "resident_files": len(rows),
        "resident_event_ids": len({row["event_id"] for row in rows.values()}),
        "distinct_strain_array_hashes": len({row["strain_array_sha256_receipt"] for row in rows.values()}),
        "files_by_role": dict(Counter(row["role"] for row in rows.values())),
        "unique_onsource_detector_interval_pairs": len({
            (row["detector"], *row["interval_gps_half_open"])
            for row in rows.values() if row["role"] == "onsource"
        }),
    }
    for key, value in computed.items():
        if inventory["counts"][key] != value:
            raise ValueError(f"Incorrect inventory count: {key}")
    return {
        "status": "DOCUMENTARY_INVENTORY_MATCHES_RESIDENT_RECEIPT",
        "utc": datetime.now(timezone.utc).isoformat(),
        "inventory": {"path": str(inventory_path), "sha256": inventory_sha},
        "resident": {"path": str(resident_path), "sha256": resident_sha, "load_id": resident["load_id"]},
        "field_comparisons": comparisons,
        "recomputed_counts": computed,
        "scope": "Same array hashes, metadata and event anchors across load receipts; no large payload rehash or current-RAM measurement.",
        "independent_usable_events": "UNKNOWN_REQUIRES_REGISTERED_SELECTION_DQ_AND_CORRELATION_POLICY",
        "scientific_status": "NO_NEW_SIGNIFICANCE_OR_PHYSICAL_CONFIRMATION",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("resident_receipt", type=Path)
    args = parser.parse_args()
    result = verify(HERE / "state/EVENT_INVENTORY_018.json", args.resident_receipt)
    target = HERE / "state" / f"EVENT_INVENTORY_018_BINDING_{result['resident']['load_id']}.json"
    if target.exists():
        raise FileExistsError("A binding receipt already exists; preserve its provenance")
    raw = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    temp = target.with_suffix(".new")
    with temp.open("xb") as stream:
        stream.write(raw)
    if temp.stat().st_size != len(raw):
        raise OSError("Incomplete receipt")
    temp.replace(target)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
