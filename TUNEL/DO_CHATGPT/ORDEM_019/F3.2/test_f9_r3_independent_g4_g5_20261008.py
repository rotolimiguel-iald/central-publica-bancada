"""Independent synthetic-only G4/G5 probe for Fase 9 R3."""

from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path

import f9_reader_gate_v1x_r3 as gate
import f9_runner_v1x_staged_r3 as staged


HERE = Path(__file__).resolve().parent
BINDING = HERE / "VINCULO_DOCUMENTAL_V1X_R3_20261008.json"
FIXTURE = HERE / "FIXTURE_SINTETICO_V1X_R3_20261008.json"
SOURCE_ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    binding = json.loads(BINDING.read_text(encoding="utf-8"))
    spec = json.loads(Path(binding["draft_v2"]["path"]).read_text(encoding="utf-8"))["spec"]
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert fixture["free_background_mock"]["prior_rd_Mpc"] == [130.0, 160.0]
    args = (BINDING, sha(BINDING), SOURCE_ROOT, binding["spec_sha256"], FIXTURE, sha(FIXTURE))
    output = staged.run_synthetic(*args)
    assert output["stage"] == "SYNTHETIC_STATISTICAL_REHEARSAL_ONLY"
    assert output["verdict"] is None and output["data_opened"] is False
    assert output["v2_frozen"] is False and output["gate_changed"] is False
    proposed = output["synthetic_proposed_rule_output"]
    assert proposed["status"] == "EXACT_PINNED_DRAFT_FUNCTION_ON_SYNTHETIC_FIXTURE_ONLY"
    assert proposed["function_sha256"] == spec["funcao_de_veredito"]["sha256"]
    assert output["synthetic_proposed_rule_output"]["classification"] == "INCONCLUSIVE_SYSTEMATICS"
    mapped = proposed["input"]["maximum"]
    actual_max = output["synthetic_statistics"]["P_primaria"]["maximum"]
    actual_min = output["synthetic_statistics"]["P_primaria"]["minimum"]
    assert mapped["lnB_lcdm"] == actual_max["lnB_TGL_LCDM"]
    assert mapped["lnB_fundo_livre"] == actual_max["lnB_TGL_free_background_n100"]
    assert actual_max["lnB_TGL_free_background_n100"] != actual_min["lnB_TGL_free_background_n100"]
    function, _ = staged.load_pinned_proposed_verdict(spec)
    mock = copy.deepcopy(proposed["input"])
    mock["n_alvos_declarados"] = 0
    mock["required_sources_admitted"] = True
    mock["beta_livre_no_limite"] = False
    mock["dispersao_endpoints"] = {key: {"chi2_por_gl": 1.0, "p": 0.5}
                                    for key in ("minimum", "maximum")}
    mock["minimum"] = {"z_delta": 0.1, "sigma_z_por_alvo": [(1.04, 0.0)]}
    mock["maximum"].update({"poder_previo": 6.0, "z_disc": 5.1,
                             "lnB_lcdm": 5.1, "lnB_livre": 0.0,
                             "lnB_shift": 0.0, "lnB_fundo_livre": 0.5,
                             "poder_nao_cefeida": 4.0})
    discriminating = function(mock)
    assert "DISCRIMINATES_FROM_LCDM" in discriminating
    assert "NOT_DISCRIMINATED_FROM_FREE_BACKGROUND" in discriminating
    mock["maximum"]["lnB_lcdm"] = 4.9
    not_discriminating = function(mock)
    assert "DISCRIMINATES_FROM_LCDM" not in not_discriminating
    boxes = output["covariance_boxes"]
    statistics = output["synthetic_statistics"]
    assert set(boxes) == set(statistics) == {
        "P_primaria", "M_seis_masers_diagnostico", "N_sem_cefeidas", "R_r25", "S_com_sirenes"
    }
    r_ids = spec["familias"]["R_r25"]["ids"]
    r_cov = boxes["R_r25"]["maximum"]["covariance"]
    i = {name: r_ids.index(name) for name in r_ids}
    coupling_l2 = r_cov[i["L1b_sh0es_r25"]][i["L2_cchp"]]
    coupling_l3 = r_cov[i["L1b_sh0es_r25"]][i["L3_sbf"]]
    assert coupling_l2 > 0 and coupling_l3 > 0
    assert math.isclose(r_cov[i["L1b_sh0es_r25"]][i["L1b_sh0es_r25"]], 0.93**2, abs_tol=1e-12)
    siren_ids = spec["familias"]["S_com_sirenes"]["ids"]
    siren_cov = boxes["S_com_sirenes"]["maximum"]["covariance"]
    siren_i = siren_ids.index("L6_sirenes")
    assert len(siren_cov) == len(siren_ids) == 6
    assert math.isclose(siren_cov[siren_i][siren_i], 11.25**2, abs_tol=1e-12)
    assert all(siren_cov[siren_i][j] == siren_cov[j][siren_i] == 0
               for j in range(len(siren_ids)) if j != siren_i)
    max_quadrature_diff = 0.0
    for family in boxes:
        for side in ("minimum", "maximum"):
            row = statistics[family][side]
            a, b = row["lnB_TGL_free_background_n100"], row["lnB_TGL_free_background_n200"]
            assert math.isfinite(a) and math.isfinite(b)
            max_quadrature_diff = max(max_quadrature_diff, abs(a-b))
    assert max_quadrature_diff < 1e-10
    try:
        staged.run_synthetic(*args, mode="real")
    except gate.ReaderGateError as exc:
        real_refusal = str(exc)
    else:
        raise AssertionError("real mode accepted")
    print(json.dumps({
        "G4_R25_L1b_L2": coupling_l2, "G4_R25_L1b_L3": coupling_l3,
        "G4_siren_cross_terms": 0, "G5_prior_rd_Mpc": [130.0, 160.0],
        "G5_families": sorted(statistics), "G5_max_n100_n200_abs_diff": max_quadrature_diff,
        "G5_primary_lnB_free_n100_min": statistics["P_primaria"]["minimum"]["lnB_TGL_free_background_n100"],
        "G5_synthetic_classification": output["synthetic_proposed_rule_output"]["classification"],
        "G5_controlled_n0_high_lnB_token": discriminating,
        "G5_controlled_n0_low_lnB_token": not_discriminating,
        "G5_official_verdict": output["verdict"], "G5_real_mode_refusal": real_refusal,
        "data_opened": output["data_opened"], "gate_changed": output["gate_changed"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
