"""Bounded inventory of treatment routes for allowlisted scientific files.

This module does not inspect file schemas or establish duplicate identity or
statistical independence. It never invokes a dataset reader.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import data_lab
import treatment


MAX_FINGERPRINT_FILES = 256


def _reader_route(item: dict) -> str:
    """Mirror the routing decision in treatment.record without opening a reader."""
    return ("READY" if item["format"].lower() in treatment.SUPPORTED
            and item["name"] != data_lab.BAO_COV else "PENDING")


def coverage_report() -> dict:
    """Summarize one catalog snapshot with bounded duplicate candidate checks.

    A ready route means an adapter can be attempted, not that the particular
    file's schema is readable. Fingerprints are computed only for equal-size
    candidates, and at most MAX_FINGERPRINT_FILES are sampled per report.
    """
    items = data_lab.catalog()
    formats: dict[str, dict] = {}
    routes = {route: {"files": 0, "bytes": 0} for route in ("READY", "PENDING")}
    by_size: dict[int, list[dict]] = defaultdict(list)
    total_bytes = 0

    for item in items:
        size = item["bytes"]
        fmt = item["format"].lower()
        route = _reader_route(item)
        counts = formats.setdefault(fmt, {"files": 0, "bytes": 0,
                                           "reader_ready": 0, "reader_pending": 0})
        counts["files"] += 1
        counts["bytes"] += size
        counts["reader_ready" if route == "READY" else "reader_pending"] += 1
        routes[route]["files"] += 1
        routes[route]["bytes"] += size
        total_bytes += size
        by_size[size].append(item)

    for counts in formats.values():
        counts["reader_route"] = ("MIXED" if counts["reader_ready"] and
                                  counts["reader_pending"] else
                                  "READY" if counts["reader_ready"] else "PENDING")

    candidates = [(size, item) for size, group in sorted(by_size.items())
                  if len(group) > 1 for item in group]
    fingerprints: dict[tuple[int, str], list[dict]] = defaultdict(list)
    attempted = 0
    unreadable = []
    for size, item in candidates[:MAX_FINGERPRINT_FILES]:
        attempted += 1
        path = Path(item["path"])
        try:
            # The catalog is a snapshot. A changed file is not compared under
            # its old size, even if its edge fingerprint is still readable.
            if path.stat().st_size != size:
                unreadable.append({"id": item["id"], "reason": "SIZE_CHANGED"})
                continue
            fingerprint = treatment.edge_fingerprint(path)
        except OSError:
            unreadable.append({"id": item["id"], "reason": "READ_FAILED"})
            continue
        fingerprints[(size, fingerprint["sha256"])].append(item)

    groups = [
        {"bytes_each": size, "edge_fingerprint_sha256": digest,
         "files": [{"id": item["id"], "name": item["name"], "group": item["group"]}
                   for item in group]}
        for (size, digest), group in sorted(fingerprints.items()) if len(group) > 1
    ]
    return {
        "status": "CATALOG_METADATA_ONLY",
        "catalog": {"files": len(items), "bytes": total_bytes,
                    "max_files": data_lab.MAX_FILES,
                    "possibly_truncated": len(items) >= data_lab.MAX_FILES},
        "formats": dict(sorted(formats.items())),
        "reader_routes": routes,
        "schema_validation_status": "NOT_CHECKED_PER_FILE",
        "schema_validation_note": "Format route coverage does not validate any individual file schema.",
        "statistical_independence_status": "NOT_ESTABLISHED",
        "possible_duplicates": {
            "status": "CANDIDATES_ONLY_NOT_IDENTITY_OR_INDEPENDENCE",
            "method": "SIZE_PLUS_FIRST_LAST_64K_NOT_FULL_FILE_HASH",
            "fingerprint_bytes_read_max_per_file": 2 * treatment.EDGE_BYTES,
            "fingerprint_file_limit": MAX_FINGERPRINT_FILES,
            "same_size_candidate_files": len(candidates),
            "fingerprint_attempted_files": attempted,
            "fingerprinted_files": attempted - len(unreadable),
            "limit_skipped_files": len(candidates) - attempted,
            "changed_or_unreadable": unreadable,
            "groups": groups,
        },
    }
