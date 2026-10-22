# -*- coding: utf-8 -*-
"""Generate an unfrozen Phase 9 V2 draft from pinned V1 and uncertainty inputs."""
from __future__ import annotations
import copy, difflib, hashlib, json, math, os, re, sys, tempfile
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
V1 = Path(r"C:\IALD\Bancada_Um\investigacao\preregistro_fase9_hubble\PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.json")
DESIGN = Path(r"C:\IALD\Central de Patentes\work\scratch_6da8f00d\fase9_hubble\desenho\FASE9_DESENHO_RESULTADO.json")
UM = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")
PESCE = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_maser_anchor_alternative\sources\masers_2001.09213v2.pdf")
PINS = {V1: "1893261e730994b3508d14dd2105f8aae3a764d3d217e28bd5939cb58f865273", DESIGN: "d9cde56af2465fa8958dcaa2b70301658b281f1e2ab09988a302beb68dbc3f08", PESCE: "c9f2d2b626fee60d77928856d217a2cbe546f06c69cd9e7ac804f4ab652e731a"}
STEM = "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V2_RASCUNHO_F31_20261008"
IDS5 = ("L1_sh0es_r22", "L2_cchp", "L3_sbf", "L4_masers_5", "L5_tdcosmo")
GRID = tuple(i / 20 for i in range(21))

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def source(path: Path) -> tuple[bytes, str]:
    data = path.read_bytes()
    hash_value = digest(data)
    if path in PINS and hash_value != PINS[path]:
        raise ValueError(f"Input pin mismatch: {path}: {hash_value}")
    return data, hash_value

def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

def pretty(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + "\n"

def gls_point(ids: tuple[str, ...], sigmas: dict[str, float], amps: dict[str, float], ln: float, lt: float, six: bool) -> dict | None:
    matrix = np.diag([sigmas[name] ** 2 for name in ids]).astype(float)
    cross = {("L1_sh0es_r22", "L2_cchp"): ln * amps["L1N"] * amps["L2N"], ("L1_sh0es_r22", "L3_sbf"): ln * amps["L1N"] * amps["L3N"], ("L2_cchp", "L3_sbf"): ln * amps["L2N"] * amps["L3N"] + lt * amps["L2T"] * amps["L3T"]}
    if six:
        for name, component in (("L1_sh0es_r22", "L1N"), ("L2_cchp", "L2N"), ("L3_sbf", "L3N")):
            cross[(name, "L4_masers_6")] = ln * amps[component] * amps["L4N"]
    for (left, right), value in cross.items():
        if left in ids and right in ids:
            i, j = ids.index(left), ids.index(right)
            matrix[i, j] += value
            matrix[j, i] += value
    eigen_min = float(np.linalg.eigvalsh(matrix)[0])
    if eigen_min <= 1e-12:
        return None
    one = np.ones(len(ids))
    solved = np.linalg.solve(matrix, one)
    norm = float(one @ solved)
    weights = solved / norm
    return {"lambda_N": ln, "lambda_T": lt, "sigma_comb": 1 / math.sqrt(norm), "minimum_eigenvalue": eigen_min, "covariance": matrix.tolist(), "gls_weights": {name: float(weight) for name, weight in zip(ids, weights)}, "negative_weights": [name for name, weight in zip(ids, weights) if weight < -1e-12]}

def endpoints(ids: tuple[str, ...], sigmas: dict[str, float], amps: dict[str, float], six: bool) -> dict:
    result = {"minimum": None, "maximum": None, "accepted": 0, "rejected": 0}
    for ln in GRID:
        for lt in GRID:
            point = gls_point(ids, sigmas, amps, ln, lt, six)
            if point is None:
                result["rejected"] += 1
                continue
            result["accepted"] += 1
            for edge, direction in (("minimum", -1), ("maximum", 1)):
                old = result[edge]
                if old is None or direction * (point["sigma_comb"] - old["sigma_comb"]) > 1e-12:
                    result[edge] = point
    if result["minimum"] is None:
        raise ValueError("No positive-definite point in fixed grid")
    return result

def build() -> tuple[dict, str, str, dict]:
    raw_v1, v1_sha = source(V1)
    old = json.loads(raw_v1.decode("utf-8"))["spec"]
    raw_design, design_sha = source(DESIGN)
    design = json.loads(raw_design.decode("utf-8"))
    raw_um, um_sha = source(UM)
    _, pesce_sha = source(PESCE)
    alpha_match = re.search(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", raw_um, re.M)
    if not alpha_match:
        raise ValueError("Runtime alpha absent")
    alpha = float(alpha_match.group(1))
    beta = alpha * math.sqrt(math.e)
    zstar = float(old["lei"]["z_star"])
    matter = float(design["reproducoes"]["Omega_m_bancada"])
    radiation = float(design["sensibilidade"]["bancada"]["Omega_r"])
    expansion = math.sqrt(matter * (1 + zstar) ** 3 + radiation * (1 + zstar) ** 4 + 1 - matter - radiation)
    K = expansion ** (2 * beta / 3)
    frozen_K = float(old["lei"]["K_no_fundo_nu"])
    if abs(K - frozen_K) > 1e-10 or abs(beta - float(old["beta"]["beta_runtime"])) > 1e-14:
        raise ValueError("Runtime beta/K differs from frozen V1")
    pins = {"V1_generated": {"path": str(V1), "sha256": v1_sha}, "design": {"path": str(DESIGN), "sha256": design_sha}, "Pesce_PDF": {"path": str(PESCE), "sha256": pesce_sha}, "um_py_alpha_only": {"path": str(UM), "sha256": um_sha}}

    readers = copy.deepcopy(old["leitores"])
    types = {
        "L1_sh0es_r22": ("primary_ladder", ["NGC4258", "SN_Ia_Pantheon_flow"]),
        "L1b_sh0es_r25": ("R_r25_replacement_only", ["NGC4258", "SN_Ia_Pantheon_flow"]),
        "L2_cchp": ("CCHP_TRGB_only_24_SN_Ia", ["NGC4258", "TRGB_anchor", "SN_Ia_flow", "HST_LMC_MW_SMC_secondary"]),
        "L3_sbf": ("TRGB_to_SBF_without_Cepheid_or_SN_Ia_calibration", ["NGC4258", "TRGB_anchor"]),
        "L5_tdcosmo": ("time_delay_lenses_Pantheon_Omega_m_prior", ["Pantheon_Omega_m_prior"]),
        "L6_sirenes": ("S_com_sirenes_diagnostic_only", []),
    }
    for name, (role, shared) in types.items():
        readers[name].update({"reader_id": name, "typed_role": role, "shared_components": shared, "source_admission": "PENDING_D_H"})
    readers["L2_cchp"].update({"tipo": "CCHP TRGB only, 24 SN Ia calibrators", "sigma_components": {"stat": 1.22, "sys": 1.33, "SN": 0.70}, "compression": "sqrt(stat^2+sys^2+SN^2), local Gaussian"})
    readers["L3_sbf"].update({"sigma_components": {"stat": 0.7, "sys": 2.3}, "compression": "sqrt(stat^2+sys^2), local Gaussian"})
    readers["L5_tdcosmo"].update({"sigma_plus": 3.9, "sigma_minus": 3.3, "compression": "mean asymmetric sides, local Gaussian"})
    six = readers.pop("L4_masers")
    readers["L4_masers_5"] = {"reader_id": "L4_masers_5", "H0": 73.6, "sigma": 3.05, "sigma_plus": 3.1, "sigma_minus": 3.0, "compression": "mean asymmetric sides, local Gaussian", "tipo": "five geometric masers excluding NGC4258", "typed_role": "primary_decision_reader", "shared_components": [], "NGC4258_in_sample": False, "source_path": str(PESCE), "source_sha256": pesce_sha, "source_locator": "Pesce+2020 PDF Table 2, fiducial (1), page 6: 73.6 +3.1/-3.0", "source_admission": "PENDING_D_H", "status": "REAL_DOCUMENTARY_NOT_STATISTICALLY_ADMITTED"}
    six.update({"reader_id": "L4_masers_6", "typed_role": "six_maser_diagnostic_only", "shared_components": ["NGC4258"], "NGC4258_in_sample": True, "source_path": str(PESCE), "source_sha256": pesce_sha, "source_locator": "Pesce+2020 PDF Table 2, page 6: 73.9 +/-3.0", "source_admission": "PENDING_D_H", "compression": "published symmetric sigma; never combined with five-maser reader"})
    readers["L4_masers_6"] = six
    for entry in readers.values():
        for obsolete in ("grupo_SN", "grupo_4258", "cefeida"):
            entry.pop(obsolete, None)
    families = copy.deepcopy(old["familias"])
    for family in families.values():
        family["ids"] = ["L4_masers_5" if name == "L4_masers" else name for name in family["ids"]]
    families["P_primaria"]["papel"] = "only decision family: five masers, never summed with six"
    families["M_seis_masers_diagnostico"] = {"ids": ["L4_masers_6" if name == "L4_masers_5" else name for name in families["P_primaria"]["ids"]], "papel": "six masers replace five, diagnostic only"}
    sigmas = {name: float(entry["sigma"]) for name, entry in readers.items()}
    if abs(sigmas["L2_cchp"] - math.sqrt(1.22 ** 2 + 1.33 ** 2 + 0.70 ** 2)) > 1e-12 or abs(sigmas["L3_sbf"] - math.hypot(0.7, 2.3)) > 1e-12 or abs(sigmas["L5_tdcosmo"] - 3.6) > 1e-12:
        raise ValueError("Local compression mismatch")
    reference = K * float(old["fundos"]["BG1"]["H0"])
    fraction = lambda mag: math.log(10) * mag / 5
    n4258 = math.hypot(0.024, 0.022)
    trgb = 0.025
    amps = {"L1N": min(sigmas["L1_sh0es_r22"], reference * fraction(n4258)), "L2N": 1.33 * n4258 / math.hypot(n4258, trgb), "L2T": 1.33 * trgb / math.hypot(n4258, trgb), "L3N": 2.3 * fraction(0.032) / 0.031, "L3T": 2.3 * fraction(0.033) / 0.031, "L4N": min(sigmas["L4_masers_6"], reference * fraction(n4258))}
    five = endpoints(IDS5, sigmas, amps, False)
    ids6 = tuple("L4_masers_6" if name == "L4_masers_5" else name for name in IDS5)
    six_result = endpoints(ids6, sigmas, amps, True)
    without_ceph = endpoints(tuple(name for name in IDS5 if name != "L1_sh0es_r22"), sigmas, amps, False)
    backgrounds = {name: {"H0": float(old["fundos"][name]["H0"]), "sigma": float(old["fundos"][name]["sigma"])} for name in ("BG1", "BG2", "BG3")}
    def power(sigma: float, bg: str) -> float:
        entry = backgrounds[bg]
        return (K - 1) * entry["H0"] / math.hypot(sigma, K * entry["sigma"])
    for result in (five, six_result, without_ceph):
        for edge in ("minimum", "maximum"):
            result[edge]["power_only_sigma"] = {bg: power(result[edge]["sigma_comb"], bg) for bg in backgrounds}
    gls_bound = power(min(sigmas[name] for name in IDS5), "BG1")
    if not 0.803 < five["minimum"]["sigma_comb"] < 0.804 or not 0.949 < five["maximum"]["sigma_comb"] < 0.950 or not 0.998 < six_result["maximum"]["sigma_comb"] < 1.000:
        raise ValueError("Grid endpoints differ from c1 audit")
    observable = {
        "rule": "Examine source-level H0 conversion under TGL before statistical admission; K predicts background-to-local relation and does not post-correct published centers.",
        "status": "OPEN_MAP_FOR_ALL_LOCAL_READERS",
        "readers": {
            "L1_sh0es_r22": "Published SN/Cepheid local H0; TGL flow likelihood map OPEN.",
            "L1b_sh0es_r25": "R25/JWST replacement; TGL flow likelihood map OPEN.",
            "L2_cchp": "TRGB-only with 24 SN Ia; TGL flow likelihood map OPEN.",
            "L3_sbf": "TRGB-to-SBF, velocity-flow H0 conversion; TGL map OPEN.",
            "L4_masers_5": "Pesce Eq.1 assumes flat LCDM Omega_m=0.315; source says Omega_m in [0,0.5] changes distances by about <=1%; TGL map OPEN.",
            "L4_masers_6": "Same Pesce Eq.1 issue; shares NGC4258 anchor; diagnostic only.",
            "L5_tdcosmo": "Time delay with Pantheon+ Omega_m restriction in flat LCDM; TGL likelihood map OPEN.",
            "L6_sirenes": "Siren distance-redshift likelihood map OPEN; diagnostic only.",
        },
    }
    spec = {
        "id": "PREREG_FASE9_RAZAO_DE_HUBBLE_V2_DRAFT_F31_20261008", "state": "RASCUNHO_NAO_CONGELADO", "generated_from": pins,
        "mu_do_rito": "q→0 (Thomson; Teorema da Escala)",
        "beta": {"rule": "ALPHA_FINE_CODATA_2018 × sqrt(e) at runtime", "alpha_read": alpha, "beta_runtime": beta, "status": "DERIVED_WITH_ALPHA_INPUT"},
        "lei": {"form": "K=E(z_star)^(2*beta/3)", "z_star": zstar, "Omega_m": matter, "Omega_r": radiation, "K_recomputed": K, "K_frozen_V1": frozen_K, "absolute_difference": abs(K-frozen_K), "free_parameters_of_law": 0},
        "fundos": copy.deepcopy(old["fundos"]), "leitores": readers, "familias": families, "achados": "achados D1 a D6 da seq 696", "observable_TGL_H0_map": observable,
        "covariancia": {
            "status": "CONDITIONAL_SENSITIVITY_BOX_NOT_MEASURED_COVARIANCE",
            "diagonal": "published local sigmas already include component budgets; do not add components twice",
            "components": {"CCHP_NGC4258_mag": [0.024, 0.022], "CCHP_TRGB_anchor_mag": 0.025, "CCHP_sys": 1.33, "SBF_NGC4258_mag_DECLARADO_web": 0.032, "SBF_TRGB_mag_DECLARADO_web": 0.033, "SBF_sys": 2.3, "SH0ES_NGC4258": "cap at sigma_L1; per-anchor budget OPEN", "SN_L1_L2": "OPEN, not in main box", "Pantheon_L1_L5": "OPEN, not in main box", "HST_LMC_MW_SMC": "secondary dependency, coefficient OPEN"},
            "amplitudes_km_s_Mpc": amps,
            "matrix_rule": "C12=lambda_N*L1N*L2N; C13=lambda_N*L1N*L3N; C23=lambda_N*L2N*L3N+lambda_T*L2T*L3T; six-maser diagnostic adds lambda_N*LiN*L4N for i=1..3; five-maser L4 has zero NGC4258 coupling by construction",
            "grid": {"lambda_N": list(GRID), "lambda_T": list(GRID), "iteration_order": "lambda_N outer, lambda_T inner", "positive_definite_only": True, "minimum_eigenvalue_threshold": 1e-12, "tie_tolerance_sigma": 1e-12, "tie_rule": "first point in iteration order", "precision": "float64 numpy.linalg.solve/eigvalsh"},
            "endpoint_rule": {"falsification_and_tension": "minimum sigma_comb", "discrimination_and_power": "maximum sigma_comb over grid, possibly interior", "dispersion": "INCONCLUSIVE if either endpoint fails", "negative_GLS_weights": "report IDs at both endpoints", "central_correlation": None},
            "five_masers_decision": five, "six_masers_diagnostic": six_result, "without_cepheids_diagnostic": without_ceph,
        },
        "poder_previo": {"formula": "(K-1)*H0_bg/sqrt(sigma_comb^2+(K*sigma_bg)^2)", "uses_only": "sigmas and background, no local reader H0 centers", "backgrounds": backgrounds, "primary_five": {edge: five[edge]["power_only_sigma"] for edge in ("minimum", "maximum")}, "six_diagnostic": {edge: six_result[edge]["power_only_sigma"] for edge in ("minimum", "maximum")}, "no_cepheids_diagnostic": {edge: without_ceph[edge]["power_only_sigma"] for edge in ("minimum", "maximum")}, "GLS_sigma_upper_bound": min(sigmas[name] for name in IDS5), "BG1_power_lower_bound": gls_bound, "primary_BG1_covariance_underpowered": False, "BG2_BG3_and_no_cepheids_underpowered_possible": True},
        "D5_local_compression": "CCHP, SBF, TDCOSMO and five-maser sigmas are local symmetric Gaussian approximations; they neither recover the original likelihood nor prove independence (achado D5 da seq 696). Preserve published asymmetric sides in binding.",
        "D5_sensitivities_from_c1_audit": {"TDCOSMO_sigma_3p9_BG1_six_diagnostic": 5.439, "SBF_total_only_BG1": 5.718, "status": "DECLARADO_AUDIT_NOT_RECALCULATED_HERE"},
        "estatisticas_executor_observado_sujeito_NAT22": {"background": "marginalized", "z_delta": "profile -2lnL including log determinant", "lnB": "quadrature n>=100, compare 100 versus 200", "V1_lnB_TGL_vs_beta_free_erratum": {"old_25_point": 2.24, "converged": 1.97, "status": "AUDITED_ERRATUM_NOT_NEW_COMPOSITE"}, "z_disc": "quadratic form, historical 4.2837; log determinant variant 4.2818 diagnostic", "sigma_beta": "mean of asymmetric sides", "operator_word": "NAT22_PENDING"},
        "funcao_de_veredito_proposta": {"status": "NOT_EXECUTABLE_UNTIL_F3_4_NAT22_D_J_AND_C1_AUDIT", "order": ["INCONCLUSIVE_SYSTEMATICS if any reader lacks BOTH gate verification and pinned operator admission, or dispersion fails at either endpoint", "FALSIFIED_AT_5SIGMA at minimum-sigma endpoint using V1 thresholds", "TENSION_3_TO_5_SIGMA at minimum-sigma endpoint", "NOT_FALSIFIED_UNDERPOWERED if power at maximum-sigma endpoint <5", "DISCRIMINATION only if all V1 thresholds hold at maximum-sigma endpoint", "otherwise NOT_FALSIFIED_POWERED"], "n_alvos_declarados": "count readers lacking either verified gate OR operator admission in pinned register; documentary link alone never decrements", "single_reader_trigger": {"threshold_sigma": 1.0, "primary_active": False, "minimum_primary_sigma": min(sigmas[name] for name in IDS5)}, "ladder_systematic_suffix": {"condition": "lnB_shift<0 and power_without_Cepheids>=5", "status": "FAIL_CLOSED_INACTIVE_WHEN_POWER_LT_5"}, "final_token_name": "OPERATOR_D_J_PENDING", "not_falsified_never_confirmation": True},
        "source_admission": {"status": "D_H_PENDING_BEFORE_OPENING", "L4_new_source": "Pesce PDF pinned; F3.2 must require Table 2 numeric anchor and both asymmetric sides", "SBF_section_III_3": "DECLARADO_WEB_NO_LOCAL_INTEGRAL_BYTES", "TDCOSMO_section_VIII_2_1": "DECLARADO_WEB_NO_LOCAL_INTEGRAL_BYTES"},
        "runner_contract": {"new_V1x_binding_and_gate": "REQUIRED; old official_archive_check pins V1 semantics and must not be used", "read_source_bytes_once": True, "no_target_ledger_write": True, "real_data_opened": False},
        "pending_operator_decisions": ["F3.4 governing scalar V2 versus ROOT90da", "NAT22 executor deviations", "D_J final token name", "D_H source admission before opening", "F3.3 opening after frozen audited V2"],
        "gate": "UNTOUCHED",
    }
    document = {"id": spec["id"], "state": spec["state"], "spec_sha256": digest(canonical(spec)), "spec_sha256_formula": "sha256(json.dumps(spec,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8'))", "spec": spec}
    lines = [
        "# Pré-registro Fase 9 — V2 proposta por gerador novo (R7)", "",
        f"**Estado:** `RASCUNHO_NAO_CONGELADO`. **Spec SHA-256:** `{document['spec_sha256']}`.", "",
        "[REAL documental] Gerado do V1 pinado. Não admite fonte, não abre dado, não roda composto e não move gate. F3.4 e NAT-22 precisam da palavra do operador antes de congelar; D-H precede a abertura e D-J dá o nome final ao token.", "",
        "## Lei e leitores", "",
        f"`mu_do_rito: q→0 (Thomson; Teorema da Escala)`. β₀=α(0)√e em runtime = `{beta:.18f}`; K recalculado=`{K:.16f}`; K V1=`{frozen_K:.16f}`; diferença=`{abs(K-frozen_K):.3e}`.", "",
        "L4 decisório usa os **cinco** masers sem NGC 4258: `73,6 +3,1/−3,0` (Pesce+2020, Tabela 2, PDF pinado). Os seis são diagnóstico separado e nunca somados. L1b só substitui L1 na réplica R25; L6 é diagnóstico de sirenes. L2 é TRGB sozinho, com 24 SN Ia; L3 não depende de Cefeidas ou SN Ia como calibração; L5 partilha a restrição de Ωm do Pantheon+.", "",
        "**Mapa TGL do observável:** a conversão dos H0 publicados de todos os leitores locais precisa de exame de verossimilhança sob TGL antes da admissão. A Eq. 1 de Pesce usa ΛCDM plano, Ωm=0,315; a fonte diz que Ωm∈[0;0,5] muda a distância em ≲1%. Isso não valida automaticamente o mapa TGL. Veja `observable_TGL_H0_map` no JSON.", "",
        "## Covariância e poder (só σ)", "",
        "Componentes: NGC 4258 `0,024⊕0,022` mag; TRGB na âncora `0,025` mag; sistemático CCHP `1,33`; SBF `0,032/0,033` mag [DECLARADO web]; SH0ES capado em σ_L1. SN L1–L2, Pantheon+ L1–L5 e âncoras HST secundárias seguem [OPEN]. A grade fixa λ_N, λ_T∈{0;0,05;…;1}, retém matrizes positivas e desempata pela primeira ocorrência. Sem correlação central.", "",
        "| Família | σ mínimo | Poder BG1/BG2/BG3 no mínimo | σ máximo | Poder BG1/BG2/BG3 no máximo | λ_N,λ_T no máximo |",
        "|---|---:|---|---:|---|---|",
    ]
    for title, result in (("Cinco decisório", five), ("Seis diagnóstico", six_result), ("Sem Cefeidas diagnóstico", without_ceph)):
        lo, hi = result["minimum"], result["maximum"]
        display = lambda point: "/".join(f"{point['power_only_sigma'][bg]:.3f}" for bg in ("BG1", "BG2", "BG3"))
        lines.append(f"| {title} | {lo['sigma_comb']:.4f} | {display(lo)} | {hi['sigma_comb']:.4f} | {display(hi)} | {hi['lambda_N']:.2f},{hi['lambda_T']:.2f} |")
    lines += ["", f"Cota GLS: σ_comb≤min σᵢ=`{min(sigmas[name] for name in IDS5):.2f}`; poder BG1≥`{gls_bound:.3f}`. UNDERPOWERED por covariância não ocorre no primário × BG1 sob este contrato; pode ocorrer em BG2/BG3 ou sem Cefeidas. A ponta adversa de discriminação é o máximo na grade, possivelmente interior, não o canto. Pesos GLS, negativos e autovalor mínimo de ambas as pontas estão no JSON. Falsificação e tensão usam σ mínimo; dispersão falha em qualquer ponta.", "", "## D5, executor e veredito", "", "As σ de CCHP, SBF, TDCOSMO e L4 cinco são compressões locais gaussianas simétricas: não recuperam a verossimilhança original nem provam independência (**achado D5 da seq 696**). Preservar lados publicados +3,1/−3,0 e +3,9/−3,3 no vínculo. Sensibilidades c1: TDCOSMO lado 3,9 → 5,439 em diagnóstico de seis; SBF sem decomposição web → 5,718.", "", "NAT-22 pendente. Executor observado: fundo marginalizado; z_δ por perfil −2lnL com log-det; lnB com n≥100 e conferência 100/200; z_disc por forma quadrática (histórico 4,2837; log-det diagnóstico 4,2818); σ_β média dos lados. Errata V1 ao lado: lnB(TGL/β-livre) convergido 1,97, não 2,24 com n=25.", "", "`n_alvos_declarados` conta leitores sem **ambos** gate verificado e admissão do operador em registro pinado; vínculo documental sozinho não reduz a contagem (**achado D6 da seq 696**). Gatilho de leitor único σ≤1,0 inativo no primário (mínimo 1,04). Sufixo da sistemática da escada exige poder sem Cefeidas≥5 e hoje permanece fail-closed. D-J nomeia o token final. Citar **achados D1 a D6 da seq 696**.", "", "Nenhum `ALVOS_FASE9_LIDOS.json` é produzido. Nada é congelado nem aberto. `NOT_FALSIFIED` nunca é creditação.", ""]
    markdown = "\n".join(lines)
    diff = "".join(difflib.unified_diff(pretty(old).splitlines(keepends=True), pretty(spec).splitlines(keepends=True), fromfile=f"V1_generated_sha256_{v1_sha}", tofile=f"V2_draft_spec_sha256_{document['spec_sha256']}"))
    payloads = {STEM + ".json": pretty(document).encode("utf-8"), STEM + ".md": markdown.encode("utf-8"), "DIFF_V1_V2_RASCUNHO_F31_20261008.patch": diff.encode("utf-8")}
    manifest = {"state": "RASCUNHO_NAO_CONGELADO", "input_pins": pins, "spec_sha256": document["spec_sha256"], "outputs": {name: {"sha256": digest(data), "bytes": len(data)} for name, data in payloads.items()}, "only_sigma_power": True, "real_data_opened": False, "gate_changed": False, "frozen": False}
    payloads["GERACAO_V2_RASCUNHO_F31_20261008.json"] = pretty(manifest).encode("utf-8")
    return document, payloads

def write_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite evidence: {path}")
    fd, temp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as target:
            target.write(data)
            target.flush()
            os.fsync(target.fileno())
        if Path(temp).stat().st_size != len(data):
            raise IOError("Temporary size mismatch")
        os.replace(temp, path)
        if digest(path.read_bytes()) != digest(data):
            raise IOError("Output hash mismatch")
    finally:
        if os.path.exists(temp):
            os.unlink(temp)

def main() -> None:
    document, payloads = build()
    if "--check-only" not in sys.argv[1:]:
        for name in payloads:
            if (HERE / name).exists():
                raise FileExistsError(f"Evidence already exists: {HERE / name}")
        for name, data in payloads.items():
            write_new(HERE / name, data)
    print(pretty({"mode": "check_only" if "--check-only" in sys.argv[1:] else "written", "spec_sha256": document["spec_sha256"], "five_sigma_min": document["spec"]["covariancia"]["five_masers_decision"]["minimum"]["sigma_comb"], "five_sigma_max": document["spec"]["covariancia"]["five_masers_decision"]["maximum"]["sigma_comb"], "files": {name: digest(data) for name, data in payloads.items()}}))

if __name__ == "__main__":
    main()
