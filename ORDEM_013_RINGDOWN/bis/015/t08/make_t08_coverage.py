"""Inventory 74 T08 candidates against public metadata, without inventing MAPs."""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2]
CHAT = HERE.parents[3]
CENSUS = BASE / "bis" / "e1_selection" / "CALIBRATION_AND_CANDIDATE_CENSUS.json"
PE = HERE / "T08_PE_METADATA_INDEX.json"
T07 = HERE.parent / "t07" / "T07_FINAL_RESULT.json"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

census = json.loads(CENSUS.read_bytes())["SNR_ge12_metadata_rows"]
pe = json.loads(PE.read_bytes())["rows"]
t07 = json.loads(T07.read_bytes())["rows"]
power_measured = {r["event"] for r in t07 if r["status"].startswith("MEASURED_")}
assert len(census) == 74
rows = []
for candidate in census:
    event = candidate["event"]
    hits = [(release, f) for release in pe for f in release["files"]
            if event in (f["key"] or "") and f["key"].endswith("combined_PEDataRelease.hdf5")]
    assert len(hits) <= 1, event
    release, file_info = hits[0] if hits else (None, None)
    rows.append({"event": event, "run": candidate["run"],
                 "network_SNR_GWOSC_metadata": candidate["SNR_network_GWOSC"],
                 "GR_input_eligibility_from_prior_census": candidate["GR_input_eligibility"],
                 "GR_remnant_median_available": candidate["GR_final_mass_detector_median"] is not None,
                 "GR_full_IMR_MAP_extracted_here": False,
                 "public_PE_record_id": release["record_id"] if release else None,
                 "public_PE_file_key": file_info["key"] if file_info else None,
                 "public_PE_file_bytes": file_info["size"] if file_info else None,
                 "public_PE_file_md5": file_info["checksum"] if file_info else None,
                 "PE_sample_file_downloaded_here": False,
                 "T07_public_strain_window_power_measured": event in power_measured,
                 "public_PSD_verified_for_T08": False,
                 "rho_inspiral_measured_here": None,
                 "rho_postinspiral_measured_here": None,
                 "T08_binary_selection": None,
                 "status": "PE_METADATA_AVAILABLE_MAP_AND_PSD_NOT_YET_CHECKED" if release else "NO_MATCHING_PE_FILE_IN_THREE_INDEXED_RELEASES"})
count_pe = sum(r["public_PE_record_id"] is not None for r in rows)
count_gr = sum(r["GR_remnant_median_available"] for r in rows)
count_power = sum(r["T07_public_strain_window_power_measured"] for r in rows)
assert (count_pe, count_gr, count_power) == (70, 66, 20)
report = {"status": "T08_PUBLIC_METADATA_COVERAGE_NO_SPLIT_SNR_OR_EPSILON_YET",
          "created_utc": datetime.now(timezone.utc).isoformat(),
          "census_sha256": sha(CENSUS), "public_PE_index_sha256": sha(PE),
          "T07_power_catalog_sha256": sha(T07),
          "counts": {"census": len(rows), "public_PE_file_listed": count_pe,
                     "public_PE_file_not_listed": len(rows) - count_pe,
                     "GR_remnant_median_in_census": count_gr,
                     "T07_window_power_overlap": count_power,
                     "GR_full_IMR_MAP_extracted_here": 0,
                     "rho_inspiral_postinspiral_measured_here": 0},
          "release_size_for_matched_events_GB": sum(r["public_PE_file_bytes"] or 0 for r in rows) / 1e9,
          "selection_rule_status": "ORDER_INPUT_GE8_BOTH_IS_STRICTER_THAN_GWTC3_AND_GWTC4_PAPER_GT6_BOTH",
          "source_urls": ["https://eprints.whiterose.ac.uk/id/eprint/234685/7/2112.06861v3.pdf",
                          "https://arxiv.org/pdf/2603.19019"],
          "rows": rows, "gate_changed": False}
path = HERE / "T08_PUBLIC_COVERAGE.json"
with path.open("xb") as stream:
    stream.write((json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode())
print(json.dumps({"sha256": sha(path), "counts": report["counts"],
                  "matched_GB": report["release_size_for_matched_events_GB"]}))
