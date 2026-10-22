"""Close T08 conservatively at its measured boundary, then continue order tree."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAT = HERE.parents[3]
def load(name):
    path = HERE / name
    return json.loads(path.read_bytes()), hashlib.sha256(path.read_bytes()).hexdigest()

start, start_sha = load("T08_START.json")
coverage, coverage_sha = load("T08_PUBLIC_COVERAGE.json")
pe, pe_sha = load("T08_PE_METADATA_INDEX.json")
pilot, pilot_sha = load("GW231206_SPLIT_SNR_PILOT.json")
cutoff, cutoff_sha = load("GW231206_CUTOFF_VALIDATION.json")
download, download_sha = load("GW231206_GR_PE_DOWNLOAD_RECEIPT.json")
audit, audit_sha = load("T08_MIMO_SCIENTIFIC_AUDIT.json")
note = CHAT / "TUNEL" / "DO_CHATGPT" / "ENTREGA_015_MEDIDA_T08_fontes_e_piloto.md"
note_sha = hashlib.sha256(note.read_bytes()).hexdigest()
assert coverage["counts"]["census"] == 74
assert coverage["counts"]["public_PE_file_listed"] == 70
assert download["sha256"] == pilot["source_sha256"]
assert cutoff["pilot_sha256"] == pilot_sha
end = datetime.now(timezone.utc)
begin = datetime.fromisoformat(start["registered_utc"])
spent = (end - begin).total_seconds() / 3600
assert 0 < spent < 2
bytes_per_sec = download["bytes"] / download["wall_seconds"]
forecast = coverage["release_size_for_matched_events_GB"] * 1e9 / bytes_per_sec / 3600
result = {
    "status": "T08_MEDIDA_PARTIAL_ONE_GR_SPLIT_SNR_PILOT_NO_74_SELECTION_NO_EPSILON_ALPHA",
    "created_utc": end.isoformat(), "machine_hours_conservative_start_to_finalizer": spent,
    "start_sha256": start_sha, "coverage_sha256": coverage_sha,
    "PE_metadata_index_sha256": pe_sha, "pilot_sha256": pilot_sha,
    "cutoff_validation_sha256": cutoff_sha, "public_PE_download_receipt_sha256": download_sha,
    "mimo_audit_sha256": audit_sha, "source_note_sha256": note_sha,
    "counts": coverage["counts"],
    "public_PE_70_matched_files_total_GB": coverage["release_size_for_matched_events_GB"],
    "one_file_observed_download_bytes_per_second": bytes_per_sec,
    "sequential_all_files_forecast_hours_at_one_file_rate": forecast,
    "forecast_scope": "Rough transfer-only extrapolation, excludes per-event waveform analysis and rate variation; not a job reservation.",
    "pilot_network_optimal_SNR": pilot["network_optimal_snr"],
    "pilot_f_ISCO_max_sample_Hz": pilot["f_cut_Kerr_ISCO_Hz"],
    "pilot_f_ISCO_posterior_median_Hz": cutoff["posterior_median_Kerr_ISCO_Hz"],
    "LVK_Table7_split_SNR": [pilot["LVK_GWTC4_Table7_rho_inspiral"],
                              pilot["LVK_GWTC4_Table7_rho_postinspiral"]],
    "pilot_reproduces_LVK_Table7": False,
    "selection_threshold_status": "ORDER_GE8_GE8_AS_STRICTER_INTERNAL_RULE; PRIMARY_GWTC3_GWTC4_IMRCT_GT6_GT6",
    "selection_74_purchased": False,
    "epsilon_theta_with_CI_purchased": False,
    "alpha_Lambda_by_reading_purchased": False,
    "gate_changed": False,
    "next_branch": "T09_CHECK_PREREQUISITES_THEN_T10",
}
target = HERE / "T08_FINAL_RESULT.json"
with target.open("xb") as stream:
    stream.write((json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode())
print(json.dumps({"result_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                  "machine_hours": spent, "forecast_transfer_only_hours": forecast,
                  "next": result["next_branch"]}))
