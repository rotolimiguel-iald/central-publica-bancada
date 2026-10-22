"""Read-only T-15 qualification and cost audit. Writes one new JSON result."""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
CHATGPT = HERE.parents[3]
RING = CHATGPT / "ORDEM_013_RINGDOWN"
T10 = RING / "bis" / "015" / "t10"

SOURCES = {
    "order_T15": CHATGPT / "TUNEL" / "PARA_CHATGPT" / "ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md",
    "budget_v12": RING / "ORCAMENTO_015_v12.json",
    "unravelings": RING / "tgl_ringdown_unravelings.py",
    "template": RING / "tgl_ringdown_template.py",
    "prediction": RING / "tgl_ringdown_prediction.py",
    "T10_final": T10 / "T10_FINAL_RESULT.json",
    "T10_posterior_audit": T10 / "T10_A_POSTERIOR_AUDIT.json",
    "T10_noise": T10 / "T10_B_RESULT.json",
    "T10_Aprime_rank": T10 / "T10_APRIME_SPECTRAL_RANK.json",
    "T10_bank": T10 / "T10_C_BANK_RESULT_v4.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    prereg = read_json(HERE / "T15_PRE_REG.json")
    for key, path in SOURCES.items():
        actual = sha256(path)
        if actual != prereg["source_pins_sha256"][key]:
            raise RuntimeError(f"Source changed: {key} {actual}")

    budget = read_json(SOURCES["budget_v12"])
    t10 = read_json(SOURCES["T10_final"])
    noise = read_json(SOURCES["T10_noise"])
    posterior = read_json(SOURCES["T10_posterior_audit"])
    rank = read_json(SOURCES["T10_Aprime_rank"])
    bank = read_json(SOURCES["T10_bank"])
    allocation = next(item for item in budget["items"] if item["item"] == "T15_sigma_jit_rec")
    detector = {row["detector"]: row for row in noise["rows"]}
    limit = prereg["known_before_execution"]["conditioning_limit"]
    h1 = detector["H1"]["b2_condition"]
    l1 = detector["L1"]["b2_condition"]
    measured_s = posterior["variants"]["free"]["delta_tau"]["n"]
    assert measured_s > 100  # one observed posterior, not an ensemble
    fit_seconds = read_json(T10 / "fit_free" / "RESULT.json")["wall_seconds"]
    proxy_seconds = 638.34  # order T-15; INPUT proxy for older Kerr V2
    n = prereg["design_if_all_gates_pass"]["n_total"]
    workers = budget["accounting"]["simultaneous_process_limit"]

    def costs(seconds: float, fits: int) -> dict:
        return {
            "fits": fits,
            "single_fit_seconds": seconds,
            "serial_cpu_hours": fits * seconds / 3600,
            "ideal_worker_lower_bound_hours": fits * seconds / (workers * 3600),
            "whole_wave_wall_hours": math.ceil(fits / workers) * seconds / 3600,
        }

    result = {
        "status": "MEDIDA_INFEASIBLE_UNDER_CURRENT_PROTOCOL_NO_PILOT",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "prereg_sha256": sha256(HERE / "T15_PRE_REG.json"),
        "source_pins_verified": True,
        "noise": {
            "condition_limit": limit,
            "H1_B2": h1,
            "H1_pass": h1 <= limit,
            "H1_excess_percent": 100 * (h1 / limit - 1),
            "L1_B2": l1,
            "L1_pass": l1 <= limit,
            "real_H1L1_network_qualified": h1 <= limit and l1 <= limit,
            "H1_B3_regularized_input_only": detector["H1"]["b3_status"],
        },
        "instrument": {
            "fitted_parameter_T10_A": "dtau220",
            "requested_parameter_T15": "delta_f_hat",
            "same_observable": False,
            "Brownian_phase_is_seeded_stochastic_phase_not_deterministic_frequency_shift": True,
            "one_mode_free_Mf_af_independent_log_f_log_tau_observables": 2,
            "one_mode_free_Mf_af_delta_f_parameters": 3,
            "structural_rank_upper_bound": 2,
            "structural_nullity_lower_bound": 1,
            "T10_free_dtau_posterior_sd_one_realization": posterior["variants"]["free"]["delta_tau"]["std"],
            "T10_informed_dtau_posterior_sd_one_realization": posterior["variants"]["informed_latent_v2"]["delta_tau"]["std"],
            "posterior_sd_is_not_ensemble_sigma": True,
            "Aprime_rank_with_hypothetical_440": rank["rank"],
            "Aprime_actual_440_injected_amplitude": 0,
            "T10_bank_waveforms": len(bank["rows"]),
            "T10_bank_recovered": 0,
            "sigma_jit_rec": None,
            "sigma_sys_delta_f_hat": None,
        },
        "budget": {
            "authorized_machine_hours": budget["authorized_machine_hours"],
            "spent_machine_hours_before_T15": budget["accounting"]["machine_hours_spent"],
            "envelope_remaining_hours_arithmetic_not_unallocated": budget["authorized_machine_hours"] - budget["accounting"]["machine_hours_spent"],
            "T15_allocated_machine_hours": allocation["allocated_machine_hours"],
            "T15_spent_machine_hours_before": allocation["actual_machine_hours"],
            "workers_limit": workers,
            "n_Brownian_injections": n,
            "n_per_family": n // 2,
            "single_recovery_measured_T10_A_synthetic_dtau_proxy": costs(fit_seconds, n),
            "single_recovery_order_Kerr_V2_638s_proxy": costs(proxy_seconds, n),
            "paired_GR_Brownian_measured_T10_A_synthetic_dtau_proxy": costs(fit_seconds, 2 * n),
            "paired_GR_Brownian_order_Kerr_V2_638s_proxy": costs(proxy_seconds, 2 * n),
            "caveat": "The measured T10-A runtime is one synthetic-noise dtau posterior. Neither it nor 638.34s measures real-noise Brownian delta_f recovery, overhead or convergence.",
        },
        "decision": {
            "pilot_injections_run": 0,
            "posterior_fits_run_T15": 0,
            "reason": ["H1_B2_CONDITION_FAIL", "DELTA_F_ESTIMATOR_ABSENT_IN_T10", "ONE_MODE_FREE_MF_AF_NONIDENTIFIABLE"],
            "minimum_protocol_changes": [
                "Qualify H1+L1 real off-source covariance under the fixed threshold, or explicitly change the target to L1-only with a new pre-registration.",
                "Implement and freeze a delta_f220 estimator and paired GR/Brownian recovery with seeded phase/noise and convergence checks.",
                "Supply independent remnant information from a ratified inspiral prior (label IMR-RD), or inject and measure a nonzero second mode with free Mf/af and demonstrate posterior identifiability.",
            ],
            "no_single_scalar_change_suffices": True,
            "gate_changed": False,
        },
    }
    if allocation["allocated_machine_hours"] != 1.0 or len(bank["rows"]) != 10:
        raise RuntimeError("Unexpected allocation or source bank count")
    out = HERE / "T15_MEDIDA.json"
    with out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    print(out)


if __name__ == "__main__":
    main()
