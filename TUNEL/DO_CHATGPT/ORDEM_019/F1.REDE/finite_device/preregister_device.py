"""Freeze the finite-device experiment before running any model calculation."""
from pathlib import Path
import datetime
import hashlib
import json

BASE = Path(__file__).resolve().parent
CENTRAL = Path(r"C:\IALD\Central de Patentes")

def pin(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def main():
    sources = {
        "superconductor": CENTRAL / "Patentes/PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex",
        "mqc_extract": BASE.parent / "sources/MQC_DESCRITIVO_EXTRACT_R1.txt",
        "mqc_source_manifest": BASE.parent / "sources/PRIMARY_SOURCES_R1.json",
        "alpha_source": CENTRAL / "Patentes/Skygrid/SkyGrid_Piloto/skygrid_sim/tgl_core.py",
        "prior_mqc_gkls": CENTRAL / "patents/BR102026003460-6_MQC/runner/one_mqc.py",
        "prior_mqc_geometry": CENTRAL / "patents/BR102026003460-6_MQC/prototype_src/mqc_simulacao_celula_elementar.py",
        "prior_mqc_run": CENTRAL / "patents/BR102026003460-6_MQC/results/2026-10-07T19-52-51/results.json",
        "prior_superconductor_runner": CENTRAL / "patents/BR102026003450-9_SUPERCONDUTOR/runner/one_supercondutor.py",
        "nos_survey": BASE.parent / "NOS_CONSULTA_R1.json",
    }
    p = {
        "unit": "F1.REDE", "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "statute": "INPUT parameters; synthetic structural test, no fit and no observed data",
        "source_pins": {k: pin(v) for k, v in sources.items()},
        "anchors": {"superconductor": "lines 340-389: GKLS equation, H_eff and a_out_dagger sigma_minus + sigma_plus a_in",
                    "mqc_extract": "PDF pages 4-7: 27-site geometry, three-level claim, master equation and root code",
                    "prior_mqc_gkls": "deepening_v2_gkls_fixed_point, 29/07: qutrit reset model and C=2|rho01|; cited, not re-run"},
        "geometry": {"coordinates": [-1, 0, 1], "counts": {"vertex": 8, "edge": 12, "face": 6, "center": 1},
                     "edge_rule": "INPUT: nearest-neighbour Manhattan distance 1 on 3x3x3 grid", "expected_edges": 54,
                     "quantum_27_site_hilbert_allocated": False},
        "model": {"factor_labels": ["in_mode_truncated", "out_mode_truncated", "OH_two_level"],
                  "factor_dims": [2, 2, 2], "hbar": 1.0, "omega_c": 1.0, "omega_OH": 1.2,
                  "g_JC": 0.15, "Omega": 0.07, "gamma_Lambda_values": [0.0, 0.3, 1.0],
                  "kappa_in": 0.03, "kappa_out": 0.04, "gamma_OH": 0.02, "gamma_dephasing": 0.01,
                  "dephasing_convention": "rate*D[sigma_z]; off-diagonal damping is 2*rate",
                  "beta": "ALPHA_FINE_CODATA_2018 * sqrt(e), parsed from pinned source in runtime",
                  "holo_rate": "beta * gamma_Lambda",
                  "units": "all dimensionless INPUT; not physical calibration",
                  "truncation": "0/1 photon cutoff, OH two levels; excludes MQC third state |Psi> and full bosonic CCR",
                  "conventional_jumps": ["a_in", "a_out", "sigma_minus", "sigma_z"],
                  "holographic_jump": "a_out_dagger @ sigma_minus + sigma_plus @ a_in"},
        "numerics": {"seed": 2026101327, "random_mixed_states": 12, "random_pure_states": 8,
                     "times": [0.0, 0.05, 0.2, 1.0, 5.0], "finite_difference_step": 1e-5,
                     "algebra_tolerance": 1e-12, "channel_tolerance": 1e-10,
                     "state_tolerance": 1e-10, "energy_identity_tolerance": 1e-11,
                     "energy_derivative_tolerance": 1e-7, "negative_witness_threshold": 1e-6},
        "tests": {
            "geometry": "FAIL unless 27 distinct sites, categories 8/12/6/1 and 54 declared graph edges",
            "local_algebras": "FAIL if any matrix-unit product, adjoint, unit, isotony embedding or disjoint commutator violates tolerance",
            "gkls": "FAIL if H non-Hermitian, trace generator not zero or action differs from direct formula",
            "cptp": "FAIL if exp(tL) Choi non-Hermitian, eigenvalue below -tol, output partial trace differs from identity",
            "states": "FAIL if evolved registered pure/mixed states lose trace/Hermiticity/positivity",
            "energy": "FAIL if Tr(H Lrho) differs from Tr(rho LdagH), finite-difference derivative or integrated ledger",
            "rates_negative_control": "PASS only when negative/nonfinite/bool rates visibly refused before exponentiation",
            "literal_coherence_negative_control": "PASS only when diag(1/2), offdiag(1-beta) rejected as not PSD",
            "normalized_coherence": "PASS if C=2|rho01|=1-beta with offdiag=(1-beta)/2 is PSD; no plateau generation claim",
            "root_code": "PASS negative control if phase-preserving amplitude square-root+normalization gives ensemble-dependent output for the same density; classical square-root/square decode remains exact",
            "truncation_control": "record [a,a_dagger]!=I; do not silently transfer full bosonic CCR"},
        "root_control": {"ensemble": "one half |0><0| plus one half |+><+| versus its spectral decomposition",
                         "map": "INPUT proposed quantum interpretation: psi_j -> phase(psi_j)*sqrt(abs(psi_j)), then normalize; source gives real sign/root code",
                         "claim_tested": "No single linear CPTP map can implement this normalized pure-state transformation for all inputs"},
        "stop_rule": "Record failures without parameter/tolerance adjustment; any repair gets a separately named addendum and new run",
        "no_claims": ["physical device realized", "information transport speed", "fidelity target", "5 sigma", "4D field net", "TGL confirmation"],
    }
    path = BASE / "PREREGISTRO_DEVICE_R1.json"
    raw = (json.dumps(p, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    with path.open("xb") as f: f.write(raw)
    freeze = {"created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "preregister": pin(path), "runner": pin(BASE / "run_finite_device.py"),
              "preregister_script": pin(Path(__file__).resolve()), "no_model_execution_yet": True}
    with (BASE / "FREEZE_DEVICE_R1.json").open("x", encoding="utf-8") as f:
        json.dump(freeze, f, indent=2, ensure_ascii=False, allow_nan=False)
    print(json.dumps(freeze, ensure_ascii=False))

if __name__ == "__main__": main()
