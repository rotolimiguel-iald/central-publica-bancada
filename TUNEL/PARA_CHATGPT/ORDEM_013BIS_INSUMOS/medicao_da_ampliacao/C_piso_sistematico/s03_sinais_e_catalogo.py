"""Frente C — (a) sinais corretos a -> delta_tau_hat (a=1 => delta<0); (b) o +0.07 do catalogo contra a largura
por evento; (c) N por leitura para eventos tipo GW250114; (d) tabela final de condicao. Somente leitura da bancada."""
import json, os, math, hashlib
import numpy as np
from scipy import stats
B = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
OUT = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(OUT, "C_piso_medicoes.json"), encoding="utf-8"))
eff = R["efeito_delta_tau_hat_GW250114_mediana_posterior"]
READINGS = ["R-B", "R-MOD", "R-RAIZ-0", "R-LIN"]
S = {}

# (a) sinais: delta_tau_hat = a_hat * eff[reading]  (eff negativo)
S["a_sinais_familia_RB_noiseless"] = {k: dict(a_hat_median=v["median"], dtau_hat_median=v["median"] * eff["R-B"], dtau_hat_min=v["max"] * eff["R-B"], dtau_hat_max=v["min"] * eff["R-B"]) for k, v in R["B_familia_direcao_RB_noiseless_a_hat"].items()}
S["a_sinais_modelo_QNM_por_t0_RB"] = [dict(start_tM=c["start_tM"], dtau_SEOB=c["a_hat_SEOB"] * eff["R-B"], dtau_Phenom=c["a_hat_Phenom"] * eff["R-B"], media=0.5 * (c["a_hat_SEOB"] + c["a_hat_Phenom"]) * eff["R-B"], dif_familias=(c["a_hat_SEOB"] - c["a_hat_Phenom"]) * eff["R-B"]) for c in R["C_modelo_QNM_220_440_vs_FULL_IMR_por_t0_RB"] if c["start_tM"] <= 20]
ov = R["C_overtones_a_hat_10M_FULL_IMR"]
S["a_sinais_overtones_10M_RB"] = {fit: {fam: a * eff["R-B"] for fam, a in d.items()} | {"dif_familias_dtau": (d["SEOBN"] - d["IMRPh"]) * eff["R-B"]} for fit, d in ov.items()}

# (b) catalogo: mediana por evento vs sigma por evento
def cat_sigma_dep(key):
    c = R[key]; evs = c["events"]
    med = np.array([e["med"] for e in evs]); sig = np.array([e["sig"] for e in evs]); w = 1 / sig ** 2
    N = len(evs)
    # regressao ponderada med = c0 + k*sig ; intercepto = extrapolacao a sigma -> 0 (SNR -> inf)
    X = np.column_stack([np.ones(N), sig]); W = np.diag(w)
    cov = np.linalg.inv(X.T @ W @ X); b = cov @ X.T @ W @ med
    # nao ponderada tambem
    ols = stats.linregress(sig, med)
    # subamostras por largura
    subs = {}
    for cut in (0.15, 0.2, 0.25):
        m = sig < cut
        if m.sum() >= 3:
            ww = w[m]; subs[f"sigma<{cut}"] = dict(n=int(m.sum()), wmean=float((ww * med[m]).sum() / ww.sum()), sig_wmean=float(1 / math.sqrt(ww.sum())), n_pos=int((med[m] > 0).sum()))
    npos = int((med > 0).sum())
    binom_p = float(stats.binomtest(npos, N, 0.5, alternative="greater").pvalue)
    # assimetria media do posterior (q95-q50)-(q50-q05) e sua relacao com a mediana
    asym = np.array([e["asym"] for e in evs])
    return dict(N=N, wls_intercept_sigma0=float(b[0]), wls_intercept_se=float(math.sqrt(cov[0, 0])), wls_slope_per_sigma=float(b[1]), wls_slope_se=float(math.sqrt(cov[1, 1])),
                ols_intercept=float(ols.intercept), ols_slope=float(ols.slope), ols_p=float(ols.pvalue), ols_r=float(ols.rvalue),
                subamostras=subs, n_pos=npos, binom_p_greater=binom_p, mean_asym=float(asym.mean()), spearman_asym_vs_med=[float(v) for v in stats.spearmanr(asym, med)],
                eventos_ordenados_por_sigma=[dict(event=e["event"][:15], med=round(e["med"], 4), sig=round(e["sig"], 4), spin=round(e["spin"], 3), M=round(e["mass"], 1)) for e in sorted(evs, key=lambda e: e["sig"])])
for key in ("F_catalogo_GWTC5_31", "F_catalogo_GWTC5_33", "F_catalogo_GWTC3_18", "F_catalogo_GWTC3_10"):
    S["b_" + key] = cat_sigma_dep(key)

# (c) N por leitura: eventos tipo GW250114 (sigma 0.058, pSEOB LVK) e SNR40 fonte fixa, e 3G (aud_4: z_RB ET 3.86, CE 7.03 mesma fonte)
sig_gw = R["GW250114_sigma_dtau220_gauss_equiv"]; sig40 = R["G_fisher_sigma_dtau_SNR40_fonte_fixa"]
c31 = R["F_catalogo_GWTC5_31"]
S["c_N_5sigma_por_leitura"] = {}
for rd in READINGS:
    d = abs(eff[rd])
    S["c_N_5sigma_por_leitura"][rd] = dict(
        efeito=eff[rd], piso_sigma_sist_comum=d / 5,
        N_eventos_tipo_GW250114_sigma0058=(5 * sig_gw / d) ** 2,
        N_eventos_SNR40_fonte_fixa_Fisher=(5 * sig40 / d) ** 2,
        N_eventos_catalogo_O4_sigma_mediana_0241=(5 * c31["median_of_sigmas"] / d) ** 2,
        N_eventos_catalogo_O4_intercepto_livre=c31["trend_intercept_free"][rd]["N_5sigma_free_intercept_same_population"],
        N_eventos_catalogo_O4_intercepto_fixo=c31["trend_intercept_free"][rd]["N_5sigma_fixed_intercept_same_population"],
        lever_arm_pred_sd=c31["trend_intercept_free"][rd]["lever_arm_weighted_sd_pred"],
        z_1evento_ET_mesma_fonte_fixa=3.86 * d / abs(eff["R-B"]), z_1evento_CE_mesma_fonte_fixa=7.03 * d / abs(eff["R-B"]),
        z_1evento_O5_mesma_fonte_fixa=0.80 * d / abs(eff["R-B"]))

# (d) tabela de condicao: componentes sistematicos (magnitude em delta_tau_hat) vs piso por leitura
comp = {
    "familia_SEOBxPhenom_noiseless_mesma_fonte_mediana_abs": {rd: float(np.median([abs(t["noiseless_dtau"]) for t in R["C5_IMR_cells_identifiable"] if t["kind"] == "OPP" and t["reading"] == rd])) for rd in READINGS},
    "familia_SEOBxPhenom_noiseless_mesma_fonte_range_abs": [min(abs(t["noiseless_dtau"]) for t in R["C5_IMR_cells_identifiable"] if t["kind"] == "OPP"), max(abs(t["noiseless_dtau"]) for t in R["C5_IMR_cells_identifiable"] if t["kind"] == "OPP")],
    "familia_com_ruido_SNR40_mediana_abs": {rd: R["B_familia_resumo"][rd]["opp_SNR40_bias_dtau_abs"]["median"] for rd in READINGS},
    "familia_outras_fontes_residuo_x_efeitoRB_nonlinear_summary": [0.66 * abs(eff["R-B"]), 4.86 * abs(eff["R-B"])],
    "modelo_QNM_10M_media_familias_dtau": 0.5 * (ov["220_440"]["SEOBN"] + ov["220_440"]["IMRPh"]) * eff["R-B"],
    "modelo_QNM_span_6M_12M_abs": [min(abs(c["media"]) for c in S["a_sinais_modelo_QNM_por_t0_RB"] if c["start_tM"] <= 12), max(abs(c["media"]) for c in S["a_sinais_modelo_QNM_por_t0_RB"] if c["start_tM"] <= 12)],
    "overtone_221_nuisance_dif_familias_10M": S["a_sinais_overtones_10M_RB"]["220_221_440"]["dif_familias_dtau"],
    "t0_6M_vs_10M_LVK_Kerr220_ringdown_only_dtau_equiv": [x["dtau_hat_vs_10M"] for x in R["D_t0_LVK_release_Kerr_M_chi_por_t0_e_equivalente_df_dtau_vs_10M"] if x["model"] == "Fundamental 220" and x["start_tM"] == 6.0][0],
    "t0_12M_vs_10M_LVK_Kerr220": [x["dtau_hat_vs_10M"] for x in R["D_t0_LVK_release_Kerr_M_chi_por_t0_e_equivalente_df_dtau_vs_10M"] if x["model"] == "Fundamental 220" and x["start_tM"] == 12.0][0],
    "estimador_SNR20_GR_C2_sintetico": R["E_C2_vies_GR_com_ruido"]["mean_dtau_GR"],
    "estimador_SNR40_mesma_familia_C5_mediana_abs": {rd: R["B_familia_resumo"][rd]["same_SNR40_bias_dtau_abs"]["median"] for rd in READINGS},
    "estimador_SNR200_mesma_familia_C5_mediana_abs": {rd: R["B_familia_resumo"][rd]["same_SNR200_bias_dtau_abs"]["median"] for rd in READINGS},
    "mistura_2familias_SNR40_C5_mediana_abs": {rd: R["B_familia_resumo"][rd]["mix_SNR40_bias_dtau_abs"]["median"] for rd in READINGS},
    "catalogo_GWTC5_31_shift_comum_wmean": c31["weighted_mean_dtau"], "catalogo_GWTC5_31_shift_comum_se": c31["sigma_weighted_mean"],
    "catalogo_GWTC5_31_excesso_variancia": c31["tau_excess"],
    "PSD_H1_L1_vs_design_variacao_relativa_sigma_sem_vies_medido": R["H_PSD_variacao_relativa_sigma"],
}
S["d_componentes_sistematicos_dtau_hat"] = comp
tabela = {}
for rd in READINGS:
    d = abs(eff[rd]); piso = d / 5
    itens = {
        "familia (mesma fonte, sem ruido)": comp["familia_SEOBxPhenom_noiseless_mesma_fonte_mediana_abs"][rd],
        "familia (outras fontes, cota)": comp["familia_outras_fontes_residuo_x_efeitoRB_nonlinear_summary"][1],
        "modelo QNM-sum 10M": abs(comp["modelo_QNM_10M_media_familias_dtau"]),
        "t0 6M vs 10M (ringdown-only)": abs(comp["t0_6M_vs_10M_LVK_Kerr220_ringdown_only_dtau_equiv"]),
        "estimador SNR20 (C2)": abs(comp["estimador_SNR20_GR_C2_sintetico"]),
        "estimador SNR40 mesma familia (C5)": comp["estimador_SNR40_mesma_familia_C5_mediana_abs"][rd],
        "estimador SNR200 mesma familia (C5)": comp["estimador_SNR200_mesma_familia_C5_mediana_abs"][rd],
        "catalogo shift comum (LVK pSEOB)": comp["catalogo_GWTC5_31_shift_comum_wmean"],
    }
    tabela[rd] = dict(efeito=eff[rd], piso=piso, itens={k: dict(valor=v, razao_sobre_piso=v / piso, abaixo_do_piso=v < piso) for k, v in itens.items()},
                      n_itens_acima_do_piso=sum(v >= piso for v in itens.values()), n_itens=len(itens))
S["d_tabela_condicao"] = tabela

json.dump(S, open(os.path.join(OUT, "C_piso_sinais_catalogo.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=float)
print(json.dumps({k: v for k, v in S.items() if not k.startswith("b_")}, indent=1, ensure_ascii=False, default=float)[:9000])
for k in S:
    if k.startswith("b_"):
        v = dict(S[k]); ev = v.pop("eventos_ordenados_por_sigma")
        print("\n##", k, json.dumps(v, ensure_ascii=False, default=float))
        if k.endswith("31"):
            for e in ev: print("   ", e)
