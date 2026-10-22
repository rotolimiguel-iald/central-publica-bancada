"""Frente C — O PISO SISTEMATICO QUE NAO ENCOLHE COM N.
Somente leitura da pasta da bancada; escreve apenas nesta pasta.
Tudo numpy/scipy leve. beta calculado em runtime, nunca literal.
"""
import json, os, math, hashlib, sys
import numpy as np
from scipy import stats
from scipy.special import erf

B = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
OUT = os.path.dirname(os.path.abspath(__file__))
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
BETA = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)

def sha16(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()[:16]

SRC = {}
def L(fn):
    p = os.path.join(B, fn)
    SRC[fn] = sha16(p)
    return json.load(open(p, encoding="utf-8"))

R = {"beta_runtime": BETA, "sources_sha16": SRC}
READINGS = ["R-B", "R-MOD", "R-RAIZ-0", "R-LIN"]

# ------------------------------------------------------------------ A. efeitos por leitura (GW250114)
cat = L("C4_CATALOG_220.json")
ev = {r["event"]: r for r in cat["rows"]}
gw = [k for k in ev if k.startswith("GW250114")][0]
eff = {}
for row in ev[gw]["rows"]:
    if row["reading"] in READINGS:
        eff[row["reading"]] = row["shift_05_50_95"][1]
R["efeito_delta_tau_hat_GW250114_mediana_posterior"] = eff
R["GW250114_posterior_dtau220_q05_50_95"] = ev[gw]["quantiles"]["dtau220"]
sig_gw = (ev[gw]["quantiles"]["dtau220"][2] - ev[gw]["quantiles"]["dtau220"][0]) / (2 * 1.6449)
R["GW250114_sigma_dtau220_gauss_equiv"] = sig_gw

# ------------------------------------------------------------------ B. sistematica de familia (C5_IMR_RECOVERY)
imr = L("C5_IMR_RECOVERY.json")
cells = [c for c in imr["results"] if c["absolute_bias"] is not None]
fam = {}
for c in cells:
    key = (c["psd"], c["reading"], c["SNR"], c["injected_a"], c["injection_family"], c["recovery"])
    fam[key] = c
def kind(c):
    if c["recovery"] == "EQUAL_FAMILY_MIXTURE":
        return "MIX"
    return "SAME" if c["recovery"] == c["injection_family"] else "OPP"
tab = []
for c in cells:
    d = abs(eff.get(c["reading"], float("nan")))
    tab.append(dict(psd=c["psd"], reading=c["reading"], SNR=c["SNR"], a=c["injected_a"],
                    inj=c["injection_family"], rec=c["recovery"], kind=kind(c),
                    bias_a=c["absolute_bias"], noiseless_a_hat=c["noiseless_a_hat"],
                    cov90=c["coverage_90"], power=c["power_proxy"],
                    bias_dtau=c["absolute_bias"] * d, noiseless_dtau=c["noiseless_a_hat"] * d,
                    lnB_mean=c["lnB"]["mean"], lnB_sd=c["lnB"]["standard_deviation"]))
R["C5_IMR_cells_identifiable"] = tab
# resumo: sistematica de familia SEM ruido (deterministica) em unidades de a e em delta_tau_hat
opp = [t for t in tab if t["kind"] == "OPP"]
same = [t for t in tab if t["kind"] == "SAME"]
mix = [t for t in tab if t["kind"] == "MIX"]
def summ(lst, key):
    v = np.array([t[key] for t in lst], float)
    return dict(n=len(v), median=float(np.median(v)), mean=float(v.mean()), min=float(v.min()), max=float(v.max()))
fam_summary = {}
for rd in READINGS:
    o = [t for t in opp if t["reading"] == rd]
    s = [t for t in same if t["reading"] == rd]
    m = [t for t in mix if t["reading"] == rd]
    fam_summary[rd] = dict(
        efeito=eff[rd],
        opp_noiseless_a_hat=summ(o, "noiseless_a_hat"),
        opp_noiseless_dtau=summ(o, "noiseless_dtau"),
        opp_bias_a_abs=summ(o, "bias_a"),
        opp_bias_dtau_abs=summ(o, "bias_dtau"),
        opp_SNR40_bias_dtau_abs=summ([t for t in o if t["SNR"] == 40], "bias_dtau"),
        same_SNR40_bias_a_abs=summ([t for t in s if t["SNR"] == 40], "bias_a"),
        same_SNR40_bias_dtau_abs=summ([t for t in s if t["SNR"] == 40], "bias_dtau"),
        same_SNR200_bias_dtau_abs=summ([t for t in s if t["SNR"] == 200], "bias_dtau"),
        same_SNR600_bias_dtau_abs=summ([t for t in s if t["SNR"] == 600], "bias_dtau"),
        mix_SNR40_bias_dtau_abs=summ([t for t in m if t["SNR"] == 40], "bias_dtau"),
        opp_noiseless_by_direction={f"{t['inj'][:4]}->{t['rec'][:4]}|{t['psd']}|SNR{int(t['SNR'])}|a{int(t['a'])}": t["noiseless_a_hat"] for t in o},
    )
R["B_familia_resumo"] = fam_summary
# sinal (direcao) da sistematica de familia: SEOB inj -> Phenom rec e vice-versa
dirs = {}
for t in opp:
    if t["reading"] == "R-B":
        dirs.setdefault(f"{t['inj']}->{t['rec']}", []).append(t["noiseless_a_hat"])
R["B_familia_direcao_RB_noiseless_a_hat"] = {k: dict(median=float(np.median(v)), min=float(min(v)), max=float(max(v)), n=len(v)) for k, v in dirs.items()}

# ------------------------------------------------------------------ C. inadequacao do modelo (soma de QNMs) e overtones, por t0
bias_abl = L("C5_BIAS_ABLATION.json")
ovt = L("C5_OVERTONE_ABLATION.json")
d_RB = abs(eff["R-B"])
t0tab = {}
for x in bias_abl["results"]:
    if x["fit"] == "220_PLUS_440" and x["content"] == "FULL_IMR":
        t0tab.setdefault(x["start_tM"], {})[x["family"]] = x["a_hat"]
c_tab = []
for t0 in sorted(t0tab):
    fs = t0tab[t0]
    if len(fs) == 2:
        s, p = fs["SEOBNRv4HM"], fs["IMRPhenomXPHM"]
        c_tab.append(dict(start_tM=t0, a_hat_SEOB=s, a_hat_Phenom=p, dtau_SEOB=s * d_RB, dtau_Phenom=p * d_RB,
                          family_diff_a=s - p, family_diff_dtau=(s - p) * d_RB, mean_model_bias_dtau=0.5 * (s + p) * d_RB))
R["C_modelo_QNM_220_440_vs_FULL_IMR_por_t0_RB"] = c_tab
ov_tab = {}
for x in ovt["results"]:
    if x["content"] == "FULL_IMR":
        ov_tab.setdefault(x["fit"], []).append(dict(start_tM=x["start_tM"], family=x["family"][:5], a_hat=x["a_hat"],
                                                    dtau=x["a_hat"] * d_RB, sigma_a=x["local_sigma_a"], z=x["local_z_R_B_at_SNR40"], boundary=x["profile_boundary"]))
R["C_overtones_FULL_IMR"] = ov_tab
# custo em sigma de adicionar overtones (z em SNR40, media por fit)
R["C_overtones_custo_z_SNR40_media_por_fit"] = {k: float(np.mean([e["z"] for e in v])) for k, v in ov_tab.items()}
R["C_overtones_a_hat_10M_FULL_IMR"] = {k: {e["family"]: e["a_hat"] for e in v if e["start_tM"] == 10.0} for k, v in ov_tab.items()}

# ------------------------------------------------------------------ D. t0 em dado real (LVK Kerr220 por t0) -> (df, dtau) equivalentes via BCW
py = L("C6_PYRING_START_COMPARISON.json")
f1, f2, f3 = 1.5251, -1.1568, 0.1292
q1, q2, q3 = 0.7000, 1.4187, -0.4990
def bcw(M, a):
    w = f1 + f2 * (1 - a) ** f3
    Q = q1 + q2 * (1 - a) ** q3
    lnf = -math.log(M) + math.log(w)
    lntau = math.log(M) + math.log(Q) - math.log(w)
    return lnf, lntau
rel = {}
for x in py["results"]:
    rel[(x["release_model"], x["start_tM"])] = (x["mass_detector_05_50_95"][1], x["spin_05_50_95"][1])
dtab = []
for model in sorted(set(k[0] for k in rel)):
    ref = rel[(model, 10.0)]
    lf0, lt0 = bcw(*ref)
    for (m, t0), (M, a) in sorted(rel.items()):
        if m != model:
            continue
        lf, lt = bcw(M, a)
        dtab.append(dict(model=model, start_tM=t0, M=M, chi=a, df_hat_vs_10M=math.exp(lf - lf0) - 1, dtau_hat_vs_10M=math.exp(lt - lt0) - 1))
R["D_t0_LVK_release_Kerr_M_chi_por_t0_e_equivalente_df_dtau_vs_10M"] = dtab
c6 = L("C6_RESULTS.json")
c6tab = {}
for x in c6["results"]:
    if x["amplitude_prior_sd_strain"] == 1e-20:
        c6tab.setdefault(x["reading"], {})[x["start_tM"]] = dict(lnB=x["lnB_vs_GR"], M=x["mass_05_50_95"][1], chi=x["spin_05_50_95"][1])
R["D_C6_lnB_por_t0_por_leitura_sd1e-20"] = c6tab
R["D_C6_lnB_span_t0"] = {rd: dict(min=min(v[t]["lnB"] for t in v), max=max(v[t]["lnB"] for t in v)) for rd, v in c6tab.items()}

# ------------------------------------------------------------------ E. vies do estimador em SNR baixo (C2)
c2 = L("C2_TRAJECTORY_RECOVERY.json")
etab = {}
for row in c2["rows"]:
    rd = row["reading"]
    if rd in READINGS or rd == "R-A":
        for cmp in row["comparisons"]:
            etab.setdefault(rd, {})[cmp["detector_noise"]] = dict(mean_dtau=cmp["mean_dtau"], q_dtau=cmp["dtau_05_50_95"], sd_df=cmp["standard_deviation_of_fitted_df"], mean_df=cmp["mean_df"], ens_dtau=row["ensemble_fit"]["dtau"])
R["E_C2_estimador_SNR20_sintetico"] = etab
ea = etab["R-A"]["SYNTHETIC_COLORED_OU_PLUS_WHITE"]
R["E_C2_vies_GR_com_ruido"] = dict(mean_dtau_GR=ea["mean_dtau"], sigma_evento_equiv=(ea["q_dtau"][2] - ea["q_dtau"][0]) / (2 * 1.6449), GR_reference_SNR=c2["GR_reference_SNR"])
R["E_C2_vies_RB_com_ruido"] = dict(mean_dtau=etab["R-B"]["SYNTHETIC_COLORED_OU_PLUS_WHITE"]["mean_dtau"], verdade=etab["R-B"]["NONE"]["ens_dtau"],
                                    vies=etab["R-B"]["SYNTHETIC_COLORED_OU_PLUS_WHITE"]["mean_dtau"] - etab["R-B"]["NONE"]["ens_dtau"])

# ------------------------------------------------------------------ F. catalogo GWTC-5.0 (33) e GWTC-3 (18): analise por evento
def catalog_analysis(rows, label, sel=None):
    out = {"label": label}
    evs = []
    for r in rows:
        if sel is not None and r["event"] not in sel:
            continue
        q = r["quantiles"]["dtau220"]
        qf = r["quantiles"]["df220"]
        med, lo, hi = q[1], q[0], q[2]
        sig = (hi - lo) / (2 * 1.6449)
        preds = {row["reading"]: row["shift_05_50_95"][1] for row in r["rows"] if row["reading"] in READINGS}
        evs.append(dict(event=r["event"], med=med, lo=lo, hi=hi, sig=sig, asym=(hi - med) - (med - lo),
                        spin=r["quantiles"]["spin"][1], mass=r["quantiles"]["mass_detector"][1],
                        df_med=qf[1], df_sig=(qf[2] - qf[0]) / (2 * 1.6449), preds=preds, GR_HPD=r.get("GR_HPD_content")))
    N = len(evs)
    med = np.array([e["med"] for e in evs]); sig = np.array([e["sig"] for e in evs]); w = 1 / sig ** 2
    wm = float((w * med).sum() / w.sum()); swm = float(1 / math.sqrt(w.sum()))
    chi2 = float((w * (med - wm) ** 2).sum())
    # DerSimonian-Laird excesso de variancia
    Q = chi2; C = w.sum() - (w ** 2).sum() / w.sum()
    tau2 = max(0.0, (Q - (N - 1)) / C)
    out.update(N=N, weighted_mean_dtau=wm, sigma_weighted_mean=swm, z_common_shift_vs_zero=wm / swm,
               chi2_common=chi2, dof=N - 1, p_chi2=float(1 - stats.chi2.cdf(chi2, N - 1)), tau2_excess=float(tau2), tau_excess=float(math.sqrt(tau2)),
               n_median_positive=int((med > 0).sum()), median_of_sigmas=float(np.median(sig)), min_sigma=float(sig.min()), mean_asym=float(np.mean([e["asym"] for e in evs])),
               spearman_med_vs_sigma=[float(v) for v in stats.spearmanr(med, sig)],
               pearson_med_vs_sigma=[float(v) for v in stats.pearsonr(med, sig)])
    # media simples e erro padrao (nao ponderada), como um teste frequentista rudimentar
    out.update(mean_dtau=float(med.mean()), sem_dtau=float(med.std(ddof=1) / math.sqrt(N)), sd_dtau=float(med.std(ddof=1)))
    # prior-volume: mediana de gaussiana centrada em 0 com sigma_L truncada a [-0.8, 2.0]
    def trunc_median(sL, lo=-0.8, hi=2.0):
        a, b = lo / sL, hi / sL
        Fa, Fb = stats.norm.cdf(a), stats.norm.cdf(b)
        return float(stats.norm.ppf(Fa + 0.5 * (Fb - Fa)) * sL)
    # para cada evento, sigma_L tal que a largura truncada reproduza sig (aprox: usar sig direto)
    pv = [trunc_median(e["sig"]) for e in evs]
    out["prior_volume_median_shift_per_event"] = dict(mean=float(np.mean(pv)), median=float(np.median(pv)), max=float(np.max(pv)), weighted=float((w * np.array(pv)).sum() / w.sum()))
    # tendencia com intercepto livre, por leitura: med_i = c + a * pred_i
    trend = {}
    for rd in READINGS:
        p = np.array([e["preds"][rd] for e in evs])
        X = np.column_stack([np.ones(N), p])
        W = np.diag(w)
        cov = np.linalg.inv(X.T @ W @ X)
        beta_hat = cov @ X.T @ W @ med
        # intercepto fixo em zero
        cov0 = 1 / (w * p * p).sum()
        a0 = float((w * p * med).sum() * cov0)
        sig_a_free = float(math.sqrt(cov[1, 1])); sig_a_fix = float(math.sqrt(cov0))
        lever = float(np.sqrt(np.average((p - np.average(p, weights=w)) ** 2, weights=w)))
        trend[rd] = dict(c_hat=float(beta_hat[0]), sig_c=float(math.sqrt(cov[0, 0])), a_hat_free=float(beta_hat[1]), sig_a_free=sig_a_free,
                         a_hat_fixed0=a0, sig_a_fixed0=sig_a_fix, pred_mean=float(p.mean()), pred_min=float(p.min()), pred_max=float(p.max()),
                         lever_arm_weighted_sd_pred=lever,
                         N_5sigma_free_intercept_same_population=float(N * (5 * sig_a_free) ** 2),
                         N_5sigma_fixed_intercept_same_population=float(N * (5 * sig_a_fix) ** 2))
    out["trend_intercept_free"] = trend
    out["events"] = [{k: v for k, v in e.items() if k != "preds"} | {"pred_RB": e["preds"]["R-B"]} for e in evs]
    return out
sel31 = set(L("C4_CATALOG_COMBINATION.json")["selected_events"])
R["F_catalogo_GWTC5_33"] = catalog_analysis(cat["rows"], "GWTC-5.0 all 33")
R["F_catalogo_GWTC5_31"] = catalog_analysis(cat["rows"], "GWTC-5.0 release selection 31", sel31)
g3 = L("C4_GWTC3_220.json")
rows3 = g3.get("rows") or g3.get("results")
sel10 = set(L("C4_GWTC3_PUBLISHED_COMBINATION.json")["selected_events"])
R["F_catalogo_GWTC3_18"] = catalog_analysis(rows3, "GWTC-3 all 18")
R["F_catalogo_GWTC3_10"] = catalog_analysis(rows3, "GWTC-3 Table 13 (10)", sel10)

# ------------------------------------------------------------------ G. estatistica: N para 5 sigma por leitura (sem sistematica)
fis = L("C5_FISHER.json")
recs = [r for r in fis["records"] if r.get("scenario", "").startswith("MASS_SPIN_FIXED")] if isinstance(fis.get("records"), list) else []
sigma40 = None
for r in recs:
    if r.get("psd") == "O4" and r.get("reading") == "R-B" and abs(r.get("snr_ringdown", 0) - 40) < 1e-9:
        sigma40 = r["sigma_delta_local"]
R["G_fisher_sigma_dtau_SNR40_fonte_fixa"] = sigma40
c31 = R["F_catalogo_GWTC5_31"]
g = {}
for rd in READINGS:
    d = abs(eff[rd])
    g[rd] = dict(efeito=eff[rd],
                 N_5sigma_SNR40_fonte_fixa=(5 * sigma40 / d) ** 2 if sigma40 else None,
                 N_5sigma_catalogo_real_sigma_mediana=(5 * c31["median_of_sigmas"] / d) ** 2,
                 N_5sigma_catalogo_real_shift_comum=(5 * c31["sigma_weighted_mean"] * math.sqrt(c31["N"]) / d) ** 2,
                 N_5sigma_catalogo_real_com_excesso_var=((5 / d) ** 2) * (c31["median_of_sigmas"] ** 2 + c31["tau2_excess"]),
                 piso_exigido_sigma_sist_comum=d / 5)
R["G_estatistico_N_5sigma"] = g

# ------------------------------------------------------------------ H. tabela do piso: sistematica comum vs efeito/5
fam_sys_dtau = {rd: fam_summary[rd]["opp_noiseless_dtau"]["median"] for rd in READINGS}
fam_sys_dtau_abs = {rd: float(np.median([abs(t["noiseless_dtau"]) for t in opp if t["reading"] == rd])) for rd in READINGS}
model_bias_10M = [c for c in c_tab if c["start_tM"] == 10.0][0]
model_bias_span = dict(min=min(abs(c["mean_model_bias_dtau"]) for c in c_tab if c["start_tM"] in (6, 8, 10, 10.5, 12)), max=max(abs(c["mean_model_bias_dtau"]) for c in c_tab if c["start_tM"] in (6, 8, 10, 10.5, 12)))
t0_220 = [x for x in dtab if x["model"] == "Fundamental 220"]
t0_sys = max(abs(x["dtau_hat_vs_10M"]) for x in t0_220)
piso = {}
for rd in READINGS:
    d = abs(eff[rd]); lim = d / 5
    comp = {
        "familia_SEOBxPhenom_noiseless_mesma_fonte": fam_sys_dtau_abs[rd],
        "familia_dependente_da_fonte_range_x_efeitoRB": [0.66 * d_RB, 4.86 * d_RB],
        "modelo_QNM_vs_IMR_10M_media_familias": abs(model_bias_10M["mean_model_bias_dtau"]),
        "modelo_QNM_vs_IMR_span_6M_12M": model_bias_span,
        "t0_6M_12M_ringdown_only_LVK_Kerr220": t0_sys,
        "estimador_SNR20_GR_C2": abs(ea["mean_dtau"]),
        "catalogo_shift_comum_GWTC5_31": c31["weighted_mean_dtau"],
        "catalogo_excesso_variancia_tau": c31["tau_excess"],
        "PSD_H1_vs_L1_vs_design_sigma_rel": None,
    }
    piso[rd] = dict(efeito=eff[rd], limite_sigma_sist_comum=lim, componentes=comp,
                    razao_efeito_sobre_familia=d / fam_sys_dtau_abs[rd] if fam_sys_dtau_abs[rd] else None,
                    razao_efeito_sobre_modeloQNM_10M=d / abs(model_bias_10M["mean_model_bias_dtau"]),
                    razao_efeito_sobre_shift_catalogo=d / c31["weighted_mean_dtau"],
                    condicao_hoje_familia=fam_sys_dtau_abs[rd] < lim,
                    condicao_hoje_modeloQNM_10M=abs(model_bias_10M["mean_model_bias_dtau"]) < lim,
                    condicao_hoje_shift_catalogo_sem_intercepto=c31["weighted_mean_dtau"] < lim,
                    condicao_hoje_t0=t0_sys < lim)
R["H_piso_por_leitura"] = piso
# PSD: sigma relativo entre PSDs (Fisher empirico)
fe = L("C5_FISHER_EMPIRICAL.json")
zs = {r["psd"]: r["z_local"] for r in fe["same_source_R_B"]}
R["H_PSD_z_RB_SNR40_H1_L1"] = zs
zref = None
for r in fis["records"]:
    if r.get("psd") == "O4" and r.get("reading") == "R-B" and abs(r.get("snr_ringdown", 0) - 40) < 1e-9 and r.get("scenario", "").startswith("MASS_SPIN_FIXED"):
        zref = r["z_local"]
R["H_PSD_z_RB_SNR40_design_ref"] = zref
if zref:
    R["H_PSD_variacao_relativa_sigma"] = {k: (zref / v - 1) for k, v in zs.items()}

json.dump(R, open(os.path.join(OUT, "C_piso_medicoes.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=float)
print("OK -> C_piso_medicoes.json ; beta_runtime =", BETA)
print("SRC:", json.dumps(SRC, indent=0))
