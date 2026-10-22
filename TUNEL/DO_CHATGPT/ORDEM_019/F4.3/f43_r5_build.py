"""Build only new, documentary F4.3 R5 artifacts; never open data D."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
V1 = Path(r"C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_05out\PREREGISTRO_RAMO_B_RINGDOWN_V1.json")
C7 = Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C7_INJECTION_REPRODUCTION_v3_2\MANIFEST.json")
PSD = C7.parent / "assets/ORDEM_013_RINGDOWN/cache/psd/aLIGO_O4_high_asd.txt"
V3 = ROOT / "PREREGISTRO_F4_3_V3.json"
INV = ROOT / "f43_r4_inventory.py"
VERDICT = ROOT / "f43_r5_verdict.py"
EXPECTED = {
    V1: "86f98fcc124dd9cae04fdb06bd10c14175893253d5b139496bd4c05f109feee0",
    C7: "649b6dcc239101c9da50159790630318d370999df58bb637271ee4c7176b6d35",
    PSD: "eb5ec9b081c3d86d2f4257b9aff6a57566d168b8a95e5e57b7909eebad021780",
    V3: "5822e92a5ceba9d773df163191ffdab7e238ada9236dc77f9f959797e40a18ca",
}
def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
def pin(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": digest(path)}
def freeze(name: str, value: dict) -> Path:
    path = ROOT / name
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(raw)
    assert digest(path) == hashlib.sha256(raw).hexdigest()
    return path
for path, expected in EXPECTED.items():
    if digest(path) != expected:
        raise SystemExit(f"source hash mismatch: {path}")
v1 = json.loads(V1.read_text(encoding="utf-8"))
d = v1["conjuntos"]["D"]
events = d["elegiveis_sem_hold"]
assert len(events) == 10 and set(events) == set(d["eventos_elegiveis"]) - set(d["com_data_quality_hold"])
medians = {row["evento"]: {"Mf_det_msun": row["Mf_det_mediana_GR"],
                           "chi_f": row["chi_f_mediana_GR"],
                           "SNR_rede": row["SNR_rede_GWOSC"]}
           for row in d["previsao_da_hipotese_por_evento_INFORMACAO_CEGA"] if row["evento"] in events}
assert len(medians) == 10
event_file = freeze("F43_R5_EVENTS_FOR_SYNTHETIC_POWER_20261008.json", {
    "status": "INPUT_FROZEN_SYNTHETIC_COHORT_ONLY__NOT_D_OPENING",
    "source": pin(V1), "selection": "V1 D eligible without the four published quality holds",
    "events": events, "blind_v1_medians": medians,
    "if_real_D_list_differs": "stop and preregister a new cohort before power or opening",
})
psd_map = {event: {det: {"curve": "aLIGO_O4_high_asd.txt",
                          "source_sha256": digest(PSD), "interpretation": "ASD squared to PSD"}
                   for det in ("H1", "L1")} for event in events}
psd_file = freeze("F43_R5_PSD_DESIGN_MAP_20261008.json", {
    "status": "INPUT_DESIGN_NOT_EVENT_OFFSOURCE", "source_C7": pin(C7),
    "curve_source": pin(PSD), "map": psd_map,
    "frequency_hz": {"lower": 20, "upper_exclusive": 2048, "sample_rate": 4096},
})
window_file = freeze("F43_R5_WINDOWS_20261008.json", {
    "status": "INPUT_SYNTHETIC_DESIGN",
    "time_unit": "t_M = G*M_f,det/c^3, using V1 blind median M_f,det per event",
    "primary": {"start": "IMR_peak + 10*t_M", "end": "IMR_peak + 80*t_M"},
    "sensitivity": {"start": "IMR_peak + 12*t_M", "end": "IMR_peak + 80*t_M"},
    "events": {event: {"Mf_det_msun": medians[event]["Mf_det_msun"],
                       "primary_start_tM": 10, "sensitivity_start_tM": 12,
                       "end_tM": 80} for event in events},
    "rule": "same window in H1/L1 and in both hypotheses; start sensitivity is paired",
})
prior_file = freeze("F43_R5_PRIORS_20261008.json", {
    "status": "INPUT_SYNTHETIC_DESIGN",
    "common_source": {"Mf_det_msun": "Uniform(0.5,2.0)*V1_blind_median_per_event",
                      "chi_f": "Uniform(0,0.98)",
                      "shared_extrinsic_parameters": "same source in H1/L1 and 220/440"},
    "mode_nuisance": {"A220": "log_uniform(1e-3,1)*reference_IMR_amplitude",
                      "A440_over_A220": "Uniform(0,1)",
                      "phase220_rad": "Uniform(0,2*pi)",
                      "phase440_rad": "Uniform(0,2*pi)"},
    "nulls": ["Kerr_220_440_GR", "B_220_440_V1_clock"],
    "B_deformation": {"delta_tau_220": "fixed -x220/(1+x220)",
                      "delta_tau_440": "fixed -x440/(1+x440)",
                      "x": "beta_runtime*(2*pi/kappa_hat(chi_f))*N_mode(chi_f); no fit of beta"},
    "nuisance_reference": "c(sigma)=c0+kc*sigma profiled under both nulls per V1 C6",
    "boundary_rule": "if prior clips either prediction, stop with INCONCLUSIVE_SYSTEMATICS",
})
waveform_file = freeze("F43_R5_WAVEFORM_CONTRACT_20261008.json", {
    "status": "INPUT_DESIGN_PINNED__EXECUTABLE_SHARED_SOURCE_ADAPTER_OPEN",
    "family": "pSEOBNRv4HM_PA full IMR V1 base plus shared-source 220/440 damping adapter",
    "version": "F43_R5_CONTRACT_1, based on V1 primary C3",
    "source_v1": pin(V1),
    "common_mass_spin": True, "full_imr_required": True,
    "frequencies": "Kerr 220 and 440 from common M_f,chi_f",
    "damping": "tau_B,lm=tau_GR,lm*(1-x_lm/(1+x_lm)); exact additive-rate envelope",
    "amplitude_phase": "separate per mode, common source geometry",
    "forbidden": ["ringdown-only as primary", "221 counted as 440",
                  "linear Fisher substituted for x~0.6 exact injections"],
    "acceptance": "adapter must produce common-source IMR waveform and pass null/recovery tests; this contract hash is not an executable waveform hash",
})
campaign_file = freeze("F43_R5_CAMPAIGN_20261008.json", {
    "status": "INPUT_PRE_REGISTERED_NOT_RUN",
    "seed": 43052026,
    "signal_injections_per_null": 10000,
    "null_repetitions_per_named_null": 10000000,
    "rng": "NumPy PCG64DXSM; record installed NumPy and generator version before run",
    "calibration": "one-sided alpha=2.8665e-7; exact IMR injections and independent null-tail calibration; if tail precision/coverage fails => INCONCLUSIVE_SYSTEMATICS",
    "recovery_gate": "lower 95% binomial bound of recovery >=0.90 at calibrated 5 sigma",
    "rcond_sweep": [1e-12,1e-10,1e-8],
    "no_execution_in_R5": True,
})
fields = {
    "event_list_final_pinned": events,
    "event_list_hash": digest(event_file),
    "psd_per_event_and_detector": psd_map,
    "psd_hashes": {"map": digest(psd_file), "curve": digest(PSD)},
    "analysis_windows": json.loads(window_file.read_text(encoding="utf-8")),
    "window_hashes": {"all_events": digest(window_file)},
    "priors_and_bounds": json.loads(prior_file.read_text(encoding="utf-8")),
    "prior_hash": digest(prior_file),
    "start_time_rule": "IMR peak + 10 t_M primary; +12 t_M paired sensitivity; end +80 t_M",
    "waveform_family_and_version": "pSEOBNRv4HM_PA full IMR + F43_R5_CONTRACT_1 shared-source 220/440 adapter",
    "waveform_hash": digest(waveform_file),
    "detector_covariance": "H1/L1 independent Gaussian project-noise blocks, one event block; no cross-event covariance; common signal parameters",
    "injection_seed_and_null_repetitions": {"seed": 43052026, "signal_per_null": 10000,
                                             "null_per_named_null": 10000000},
}
assert len(fields) == 13 and all(value is not None for value in fields.values())
spec = {
    "id": "F4.3_220_PLUS_440_R5_DOCUMENTARY",
    "unit": "F4.3",
    "status": "DESIGN_PINNED__AWAITING_EXACT_POWER__OPERATOR_REQUEST_SUSPENDED",
    "sources": {"V1": pin(V1), "C7": pin(C7), "V3_R4": pin(V3),
                "R4_inventory_generator": pin(INV)},
    "artifacts": {k: pin(v) for k,v in {
        "events": event_file, "psd": psd_file, "windows": window_file,
        "priors": prior_file, "waveform_contract": waveform_file,
        "campaign": campaign_file, "verdict_function": VERDICT}.items()},
    "fields_13": fields,
    "field_scope": "All 13 design fields are non-null and pinned; waveform_hash pins the contract, not an executable full-IMR implementation; real D event list must be rechecked before opening.",
    "power_regime": "C7 aLIGO O4 high design ASD squared to PSD for H1/L1, V1 blind medians; no hdf5 opened",
    "power_rule": "V1 eta>=25 is |delta_pred|/sigma_used>=5, median 5-sigma separation only; F4.3 demands >=90% exact-injection recovery at one-sided 5 sigma, stricter than V1",
    "local_order": ["AWAITING_POWER","DIAGNOSTIC_UNDERPOWERED_OR_NONIDENTIFIABLE",
                    "DIAGNOSTIC_INCONCLUSIVE_SYSTEMATICS","DIAGNOSTIC_BOTH_MODELS_REJECTED",
                    "DIAGNOSTIC_CONFLICTS_V1","DIAGNOSTIC_CORROBORATES_V1_SAME_DIRECTION",
                    "DIAGNOSTIC_ONLY__NEITHER_REJECTED","DIAGNOSTIC_ONLY__NO_V1_DIRECTION"],
    "opposite_threshold": "exactly one F4.3 null rejected at one-sided p<=2.8665e-7; V1 rejected named null differs",
    "precedence_explanation": "first matching local row wins. UNDERPOWERED precedes INCONCLUSIVE because exact power is a prerequisite for this secondary diagnostic; systematics failures remain in matched_rows. V1 official order and public token are unchanged.",
    "public_field": "v1_official_token_public_unchanged",
    "local_field": "diagnostic_token_local",
    "current_inputs": {"manifest_complete": False, "exact_power_run": False,
                       "reason": "full IMR shared-source adapter and exact injection campaign are not built/run"},
    "no_data_opened": True, "no_gate_change": True,
}
spec_file = freeze("PREREGISTRO_F4_3_V4_R5_20261008.json", spec)
print(json.dumps({"spec": pin(spec_file), "artifact_count": 7,
                  "fields_nonnull": len(fields), "PSD_sha256": digest(PSD)}, ensure_ascii=False))