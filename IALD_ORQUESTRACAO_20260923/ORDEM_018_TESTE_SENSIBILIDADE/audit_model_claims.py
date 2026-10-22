"""Pin local result fields before correcting provider claims about significance."""

import hashlib
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from iald_orchestrator.safe_files import save_json, utc_now

HERE = Path(__file__).resolve().parent
RESULT = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json")
C0 = BASE.parent / "ORDEM_013_RINGDOWN/C0_ADENDO_FRASES_PUBLICAS.md"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    result_bytes = RESULT.read_bytes()
    core = json.loads(result_bytes)["core"]
    c0_bytes = C0.read_bytes()
    c0_text = c0_bytes.decode("utf-8")
    if "correção/σ 0.343377425" not in c0_text:
        raise RuntimeError("R-B source assertion could not be verified.")
    if "isso não é Bayes factor nem teste calibrado" not in c0_text:
        raise RuntimeError("R-B caveat could not be verified.")
    dephasing = core["ringdown_dephasing_result_v2"]
    echo = core["gw_echo_rite"]
    void_projection = core["void_floor_v3"]["power_projection"]
    void_kappa = core["void_floor_v3_kappa"]
    void_v11 = core["void_floor_v11"]
    nmc = core["nmc_shapiro"]
    if abs(dephasing["power_B"] - 0.17785138901257008) > 1e-14:
        raise RuntimeError("Dephasing power changed.")
    receipt = {
        "at": utc_now(),
        "source_result": {"path": str(RESULT), "sha256": sha256(result_bytes),
                          "bytes": len(result_bytes)},
        "source_c0": {"path": str(C0), "sha256": sha256(c0_bytes),
                      "bytes": len(c0_bytes), "line": 29},
        "ringdown_dephasing_result_v2": {
            key: dephasing.get(key) for key in
            ("verdict", "outcome", "n_events", "z_vs_GR", "z_vs_B",
             "power_B", "start_systematic", "sigma_combined")
        },
        "gw_echo_rite": {
            "verdict": echo["verdict"],
            "delay_law": echo["delay_law"],
            "stack": {key: echo["stack"].get(key) for key in
                      ("power_sigma", "z_det", "z_excl_1", "n_used",
                       "outcome", "mismatch_max_abs")},
        },
        "void_floor_v3_projection": {
            key: void_projection.get(key) for key in
            ("fisher_measured_full_cov", "variance_reduction_needed_for_powered", "reading")
        },
        "void_floor_v3_kappa": {
            "verdict": void_kappa["verdict"],
            "fisher_floor": void_kappa["values"].get("fisher_floor"),
            "void_signal_expected_snr": void_kappa["values"].get("void_signal_expected_snr"),
        },
        "void_floor_v11": {
            "verdict": void_v11["verdict"],
            "primary": {key: void_v11["primary"].get(key)
                        for key in ("rhat_cal", "sigma", "L5", "powered")},
        },
        "nmc_shapiro": {
            key: nmc.get(key) for key in ("verdict", "n_events", "nmc_dt_s")
        },
        "local_corrections": [
            "0.177851389 is dephasing branch-B conditional power, not an observed echo detection Z.",
            "0.343377425 is ensemble R-B correction over sample SD, not a calibrated discovery statistic.",
            "The gw_echo_rite is inconclusive due to systematics; its separate conditional power is 2.53438 of 5 sigma.",
            "Scaling factors 790 and 212 computed from those two numbers do not estimate required event counts or power.",
            "Void kappa is inconclusive due to systematics, with fisher_floor zero; its own power remains uncalculated.",
            "NMC-Shapiro is awaiting data with zero events; future projections are not current-data power.",
        ],
    }
    save_json(HERE / "wave2/source_corrections.json", receipt)
    print(json.dumps({"result_sha256": receipt["source_result"]["sha256"],
                      "c0_sha256": receipt["source_c0"]["sha256"],
                      "dephasing_power_B": dephasing["power_B"],
                      "echo_outcome": echo["stack"]["outcome"]}))


if __name__ == "__main__":
    main()
