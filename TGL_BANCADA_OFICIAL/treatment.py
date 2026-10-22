"""Read-only, versioned treatment record for a catalogued scientific source.

A treatment record is metadata, not a physical likelihood or a claim of
statistical independence. Large files are never hashed in full on selection.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import data_lab

SCHEMA_VERSION = "TGL_TREATMENT_V1"
SUPPORTED = {".fits", ".csv", ".dat", ".txt", ".npy", ".h5", ".hdf5"}
EDGE_BYTES = 65536


def edge_fingerprint(path: Path) -> dict:
    stat = path.stat()
    with path.open("rb") as source:
        first = source.read(EDGE_BYTES)
        source.seek(max(0, stat.st_size - EDGE_BYTES))
        last = source.read(EDGE_BYTES)
    digest = hashlib.sha256(
        str(stat.st_size).encode("ascii") + b"\0" + first + b"\0" + last
    ).hexdigest()
    return {"sha256": digest, "method": "SIZE_PLUS_FIRST_LAST_64K_NOT_FULL_FILE_HASH",
            "bytes_read_max": 2 * EDGE_BYTES,
            "scope": "CANDIDATE_DUPLICATE_ONLY_NOT_INTEGRITY_PROOF"}


def record(path: Path) -> dict:
    # A public caller must resolve the opaque id through data_lab.selected first.
    stat = path.stat()
    result = {"schema": SCHEMA_VERSION, "source_id": data_lab.file_id(path.resolve()),
              "source": {"path": str(path), "bytes": stat.st_size,
                         "mtime_ns": stat.st_mtime_ns, "format": path.suffix.lower(),
                         "edge_fingerprint": edge_fingerprint(path)},
              "treatment": {"operation": "METADATA_READ_ONLY", "status": "NOT_EVALUATED",
                            "rows": None, "columns": [], "units_policy": "UNKNOWN_IS_NOT_DIMENSIONLESS",
                            "quality": [], "sample_method": None},
              "statistics": {"status": "NOT_FIT", "independence": "NOT_ESTABLISHED",
                             "covariance": "NOT_KNOWN"}}
    if path.suffix.lower() not in SUPPORTED or path.name == data_lab.BAO_COV:
        result["treatment"].update(status="ADAPTER_PENDING", quality=["FORMAT_NOT_READ_BY_BENCH"])
        return result
    try:
        meta = data_lab.describe(path)
    except (OSError, ValueError, KeyError, OverflowError) as exc:
        result["treatment"].update(status="SCHEMA_REJECTED", quality=[str(exc)[:240]])
        return result
    columns = [{"name": c["name"], "unit": c["unit"] or "UNKNOWN"} for c in meta["columns"]]
    result["treatment"].update(status="SCHEMA_READABLE", rows=meta["rows"], columns=columns,
                               sample_method="FULL_13_POINT_SUMMARY" if meta["format"] ==
                               "DESI_BAO_MEAN_WITH_COVARIANCE" else "BOUNDED_PREVIEW_ON_REQUEST")
    if any(c["unit"] == "UNKNOWN" for c in columns):
        result["treatment"]["quality"].append("COLUMN_UNIT_UNKNOWN")
    if meta["format"] == "HDF5_NUMERIC":
        result["treatment"]["quality"].append("ROW_COUNT_IS_MAXIMUM_ACROSS_DATASETS")
    if meta["format"] == "DESI_BAO_MEAN_WITH_COVARIANCE":
        info = meta["_internal"]
        result["statistics"].update(covariance="FULL_13X13_VALIDATED_DIMENSIONS_SYMMETRY_DIAGONAL",
                                    independence="CORRELATED_WITHIN_THIS_VECTOR",
                                    covariance_path=info["covariance_path"],
                                    mean_sha256=info["mean_sha256"],
                                    covariance_sha256=info["covariance_sha256"])
    return result
