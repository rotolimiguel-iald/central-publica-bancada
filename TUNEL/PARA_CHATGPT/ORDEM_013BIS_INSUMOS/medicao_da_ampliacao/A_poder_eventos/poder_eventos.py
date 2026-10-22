"""FRENTE A - O poder contra o numero de eventos, nos posteriores reais (ORDEM 013-bis, portao do poder).
Le SO os artefatos da bancada (read-only) + as amostras extraidas por extract_samples_wsl.py.
Escreve CSV/JSON somente nesta pasta. beta = ALPHA_FINE_CODATA_2018*sqrt(e) em runtime (nunca literal).
"""
import json, csv, hashlib, math, os, sys
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN")
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
BETA = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
Z5 = 5.0
READINGS = ["R-B", "R-MOD", "R-RAIZ-0", "R-LIN"]

def sha16(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()[:16]

fontes = {}
def load(p):
    p = Path(p); fontes[str(p)] = sha16(p)
    return json.load(open(p, encoding="utf-8"))

# ---------- fontes ----------
summ = load(HERE / "samples_summary.json")
cat220 = load(SRC / "C4_CATALOG_220.json")
comb = load(SRC / "C4_CATALOG_COMBINATION.json")
g3 = load(SRC / "C4_GWTC3_220.json")
g3comb = load(SRC / "C4_GWTC3_COMBINATION.json")
g3pub = load(SRC / "C4_GWTC3_PUBLISHED_COMBINATION.json")
fisher = load(SRC / "C5_FISHER.json")
pyring = load(SRC / "C4_PYRING.json")
c2 = load(SRC / "C2_TRAJECTORY_RECOVERY.json")
csv_path = SRC / "C7_INDEPENDENT/tables/event_reading_predictions.csv"
fontes[str(csv_path)] = sha16(csv_path)
pred_csv = {}
for r in csv.DictReader(open(csv_path, encoding="utf-8")):
    pred_csv[(r["event"], r["reading"])] = float(r["delta_tau"])
npz_path = HERE / "samples_thin.npz"; fontes[str(npz_path)] = sha16(npz_path)
thin = np.load(npz_path)

# predicoes medianas por evento x leitura: GWTC-5.0 do CSV (== C4_CATALOG_220 median_prediction), GWTC-3-only de C4_GWTC3_220 (mediana do shift amostra a amostra)
pred = {}
for row in cat220["rows"]:
    for rr in row["rows"]:
        pred[(row["event"], rr["reading"])] = dict(median_prediction=rr["median_prediction"]["delta_tau_ensemble_exact"],
                                                   shift_median=rr["shift_05_50_95"][1], shift_05_95=(rr["shift_05_50_95"][0], rr["shift_05_50_95"][2]))
for row in g3["rows"]:
    for rr in row["rows"]:
        key = (row["event"], rr["reading"])
        if key not in pred:
            pred[key] = dict(median_prediction=rr.get("median_prediction", {}).get("delta_tau_ensemble_exact", rr["shift_05_50_95"][1]),
                             shift_median=rr["shift_05_50_95"][1], shift_05_95=(rr["shift_05_50_95"][0], rr["shift_05_50_95"][2]))
# cruzamento CSV x C4 (deve bater)
max_dev = max(abs(pred_csv[k] - pred[k]["median_prediction"]) for k in pred_csv if k in pred)

# ---------- verificacao propria da formula R-B (uma amostra): x = beta * (t_M*omega) * Q ; delta_tau = -x/(1+x) ----------
mp = next(rr for rr in cat220["rows"][0]["rows"] if rr["reading"] == "R-B")["median_prediction"]
x_own = BETA * mp["omega_mass"] * mp["quality"]
rb_check = dict(event=cat220["rows"][0]["event"], x_bancada=mp["x"], x_own=x_own, delta_own=-x_own / (1 + x_own),
                delta_bancada=mp["delta_tau_ensemble_exact"], beta_runtime_bancada=mp["beta_runtime"], beta_runtime_own=BETA)

# ---------- conjuntos ----------
sel31 = list(comb["selected_events"]); ctrl2 = list(comb["additional_control_events"])
all33 = [r["event"] for r in cat220["rows"]]
older6 = list(g3["duplicate_reconciliation"]["older_only"])
g3_18 = [r["event"] for r in g3["rows"]]
g3_10 = list(g3pub["selected_events"])
assert set(sel31 + ctrl2) == set(all33)
union39 = all33 + older6
GW250114 = "GW250114_082203"

rows = {r["event"]: r for r in summ["rows"]}

# ---------- 1) por evento: sigma, pred, z ----------
per_event = []
for ev in union39:
    r = rows[ev]
    q = r["dtau220"]["q05_16_50_84_95"]; qf = r["df220"]["q05_16_50_84_95"]
    sig_std = r["dtau220"]["std"]; sig68 = (q[3] - q[1]) / 2; sig90 = (q[4] - q[0]) / (2 * 1.645)
    sigf_std = r["df220"]["std"]; sigf68 = (qf[3] - qf[1]) / 2; sigf90 = (qf[4] - qf[0]) / (2 * 1.645)
    d = dict(event=ev, catalog=r["catalog"], N=r["N"], in_sel31=ev in sel31, in_all33=ev in all33, in_gwtc3_18=ev in g3_18, in_gwtc3_10=ev in g3_10,
             spin_median=r["spin"]["median"], mass_det_median=r["mass_detector"]["median"], z_median=r["redshift"]["median"],
             dtau_median=q[2], dtau_mean=r["dtau220"]["mean"], sigma_dtau_std=sig_std, sigma_dtau_68=sig68, sigma_dtau_90=sig90,
             df_median=qf[2], sigma_df_std=sigf_std, sigma_df_68=sigf68, sigma_df_90=sigf90, corr_df_dtau=r["corr_df_dtau"],
             dtau440_free=bool(r["dtau440_std"]) if r["dtau440_std"] is not None else None)
    for rd in READINGS:
        p = pred[(ev, rd)]["median_prediction"]
        d[f"pred_{rd}"] = p
        d[f"z_{rd}_std"] = abs(p) / sig_std
        d[f"z_{rd}_68"] = abs(p) / sig68
        d[f"zobs_{rd}"] = (q[2] - p) / sig_std  # (mediana observada - predicao)/sigma  [NAO-CEGO]
    d["zobs_GR"] = q[2] / sig_std
    per_event.append(d)

with open(HERE / "A1_por_evento.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(per_event[0].keys())); w.writeheader(); w.writerows(per_event)

# ---------- 2) poder combinado ----------
def combos(events, sigkey="sigma_dtau_std"):
    out = {}
    E = [d for d in per_event if d["event"] in events]
    sig = np.array([d[sigkey] for d in E]); w = 1 / sig**2
    sigma_comb = 1 / math.sqrt(w.sum())
    dt = np.array([d["dtau_median"] for d in E])
    mean_w = float((w * dt).sum() / w.sum())
    out["_meta"] = dict(N=len(E), sigma_comb=sigma_comb, weighted_mean_dtau_obs=mean_w, z_weighted_mean_vs_GR=mean_w / sigma_comb,
                        n_positive_median=int((dt > 0).sum()))
    for rd in READINGS:
        p = np.array([d[f"pred_{rd}"] for d in E]); z = np.abs(p) / sig
        z_matched = math.sqrt(float((z**2).sum()))          # filtro casado (pred conhecida, sinal conhecido)
        pbar = float((w * p).sum() / w.sum())
        z_common = abs(pbar) / sigma_comb                    # teste da media ponderada com pred media
        # tendencia com intercepto livre: Var(s) = 1/sum w (p - pbar)^2
        lever = float((w * (p - pbar)**2).sum())
        z_slope = math.sqrt(lever) if lever > 0 else 0.0
        # ajuste real (NAO-CEGO): dtau = c + s*p
        A = np.vstack([np.ones_like(p), p]).T; W = np.diag(w)
        cov = np.linalg.inv(A.T @ W @ A); beta_hat = cov @ A.T @ W @ dt
        chi2_fit = float(((dt - A @ beta_hat)**2 * w).sum())
        out[rd] = dict(z_matched=z_matched, z_common_mean=z_common, pred_weighted_mean=pbar, z_slope_fisher=z_slope,
                       N_for_5sigma_matched_same_mix=len(E) * (Z5 / z_matched)**2 if z_matched > 0 else None,
                       N_for_5sigma_slope_same_mix=len(E) * (Z5 / z_slope)**2 if z_slope > 0 else None,
                       fit_intercept=float(beta_hat[0]), fit_slope=float(beta_hat[1]), fit_sigma_intercept=math.sqrt(cov[0, 0]),
                       fit_sigma_slope=math.sqrt(cov[1, 1]), fit_chi2=chi2_fit, fit_dof=len(E) - 2,
                       z_obs_weighted_mean_vs_pred=(mean_w - pbar) / sigma_comb,
                       pred_min=float(p.min()), pred_max=float(p.max()), pred_std_unweighted=float(p.std(ddof=1)))
    return out

sets = {"sel31_GWTC5": sel31, "all33_GWTC5": all33, "union39_GWTC5+GWTC3only": union39, "GWTC3_18": g3_18, "GWTC3_10_published": g3_10, "GWTC3_only6": older6}
combined = {k: combos(v) for k, v in sets.items()}
combined_68 = {k: combos(v, "sigma_dtau_68") for k, v in sets.items()}

# comparacao com a auditoria: sigma_comb ~0.036 do posterior de deformacao comum (90%: [+0.015,+0.134])
cd = next(c for c in comb["common_deformation_GR_diagnostics"] if c["selection"] == "release_figure_selection_31" and c["draws"] == 8192)
q90 = cd["posterior_quantiles"]["dtau220"]
audit = dict(common_dtau_31_median=q90[1], common_dtau_31_90=(q90[0], q90[2]), sigma_common_from_90=(q90[2] - q90[0]) / (2 * 1.645),
             z_RB_vs_sigma_common=abs(pred_csv[("GW150914_095045", "R-B")]) / ((q90[2] - q90[0]) / (2 * 1.645)),
             GR_HPD_content=cd["GR_HPD_content"])

# ---------- 3) lei de escala: eventos "como a mediana" e "como o GW250114" ----------
scaling = {}
ratios = {r["psd"]: r["snr_ratio_to_O4"] for r in fisher["same_source_R_B"]}
for rd in READINGS:
    z33 = np.array([d[f"z_{rd}_std"] for d in per_event if d["in_all33"]])
    z31 = np.array([d[f"z_{rd}_std"] for d in per_event if d["in_sel31"]])
    zg = next(d[f"z_{rd}_std"] for d in per_event if d["event"] == GW250114)
    zmed = float(np.median(z31)); zbest = float(z31.max())
    ent = dict(z_median_event_sel31=zmed, z_GW250114=zg, z_best_event_sel31=zbest,
               best_event=next(d["event"] for d in per_event if d["in_sel31"] and d[f"z_{rd}_std"] == zbest),
               N5_like_median_O4=(Z5 / zmed)**2, N5_like_GW250114_O4=(Z5 / zg)**2,
               N5_like_median_68=(Z5 / float(np.median([d[f"z_{rd}_68"] for d in per_event if d["in_sel31"]])))**2)
    for psd, rt in ratios.items():
        ent[f"N5_like_median_{psd}"] = (Z5 / (zmed * rt))**2
        ent[f"N5_like_GW250114_{psd}"] = (Z5 / (zg * rt))**2
        ent[f"z_comb_sel31_{psd}_same_population"] = combined["sel31_GWTC5"][rd]["z_matched"] * rt
        ent[f"z_slope_sel31_{psd}_same_population"] = combined["sel31_GWTC5"][rd]["z_slope_fisher"] * rt
    scaling[rd] = ent

# ---------- 4) alavanca do teste de tendencia: distribuicao de spin/massa/pred ----------
spins = np.array([d["spin_median"] for d in per_event if d["in_all33"]]); masses = np.array([d["mass_det_median"] for d in per_event if d["in_all33"]])
lever = dict(spin_q05_50_95=[float(x) for x in np.quantile(spins, [.05, .5, .95])], spin_min_max=(float(spins.min()), float(spins.max())),
             mass_det_q05_50_95=[float(x) for x in np.quantile(masses, [.05, .5, .95])], mass_min_max=(float(masses.min()), float(masses.max())))
for rd in READINGS:
    p = np.array([d[f"pred_{rd}"] for d in per_event if d["in_all33"]])
    lever[rd] = dict(pred_min=float(p.min()), pred_median=float(np.median(p)), pred_max=float(p.max()), pred_std=float(p.std(ddof=1)),
                     relative_spread_std_over_absmean=float(p.std(ddof=1) / abs(p.mean())), ratio_max_over_min=float(p.min() / p.max()))
# sensibilidade do pred R-B ao spin a partir das amostras (dentro de um evento, GW250114): correlacao pred x spin nao esta no npz; usamos os shift_05_95 da bancada
lever["RB_shift_05_95_GW250114"] = pred[(GW250114, "R-B")]["shift_05_95"]
lever["RB_shift_05_95_GW150914"] = pred[("GW150914_095045", "R-B")]["shift_05_95"]

# ---------- 6) variancia excedente em delta_f (jitter previsto sd~0.019 por evento) ----------
c2rb = None
for r in c2["rows"]:
    if r.get("reading") == "R-B":
        c2rb = r; break
# procurar sd_df dentro do row R-B (estrutura aninhada) - so leitura para registrar; o valor usado vem da tarefa (0.0192) e e conferido se achado
def find_keys(o, pat, path=""):
    hits = []
    if isinstance(o, dict):
        for k, v in o.items():
            if pat in k.lower() and not isinstance(v, (dict, list)): hits.append((path + "/" + k, v))
            hits += find_keys(v, pat, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o[:50]): hits += find_keys(v, pat, path + f"[{i}]")
    return hits
sd_hits = find_keys(c2rb, "sd") if c2rb else []
mean_hits = find_keys(c2rb, "mean") if c2rb else []
SIG_JIT = 0.0192  # [DERIVED condicional ao desenrolamento; da auditoria/C2] - conferido abaixo se o campo existir
def z_excess_var(sigmas, v):
    r = 1 + v / np.asarray(sigmas)**2
    return math.sqrt(float((r - 1 - np.log(r)).sum()))   # sqrt(E[2 ln LR]) sob a alternativa; ~ sqrt(N/2) v/sigma^2 p/ v<<sigma^2
excess = {}
for key in ["sigma_df_std", "sigma_df_68", "sigma_df_90"]:
    s33 = np.array([d[key] for d in per_event if d["in_all33"]]); s31 = np.array([d[key] for d in per_event if d["in_sel31"]])
    sg = next(d[key] for d in per_event if d["event"] == GW250114); smed = float(np.median(s31))
    zg = z_excess_var([sg], SIG_JIT**2); zm = z_excess_var([smed], SIG_JIT**2)
    excess[key] = dict(sigma_df_GW250114=sg, sigma_df_median_sel31=smed, z_per_event_GW250114=zg, z_per_event_median=zm,
                       N5_like_GW250114=(Z5 / zg)**2, N5_like_median=(Z5 / zm)**2,
                       z_comb_sel31=z_excess_var(s31, SIG_JIT**2), z_comb_all33=z_excess_var(s33, SIG_JIT**2),
                       small_v_approx_N5_like_GW250114=2 * (Z5 * (sg**2 + SIG_JIT**2) / SIG_JIT**2)**2 / 1 if False else None)
    # sensibilidade: O5/ET/CE (sigma_meas/ratio)
    for psd, rt in ratios.items():
        zg2 = z_excess_var([sg / rt], SIG_JIT**2); zm2 = z_excess_var([smed / rt], SIG_JIT**2)
        excess[key][f"N5_like_GW250114_{psd}"] = (Z5 / zg2)**2; excess[key][f"N5_like_median_{psd}"] = (Z5 / zm2)**2
# observado (NAO-CEGO): dispersao das medianas de df entre eventos vs sigma_i (variancia excedente medida, estimador de momentos)
dfm = np.array([d["df_median"] for d in per_event if d["in_sel31"]]); sdf = np.array([d["sigma_df_std"] for d in per_event if d["in_sel31"]])
w = 1 / sdf**2; mu = (w * dfm).sum() / w.sum()
obs_excess = dict(N=len(dfm), weighted_mean_df=float(mu), chi2_null=float(((dfm - mu)**2 * w).sum()), dof=len(dfm) - 1,
                  var_moment_estimate=float(((dfm - mu)**2 - sdf**2).mean()), note="estimador de momentos ingenuo; sigma_i posteriores nao-gaussianos; NAO-CEGO")

# pyRing GW250114 (secundario)
pq = pyring["quantiles"]["dtau220"]; pr = next(r for r in pyring["rows"] if r["reading"] == "R-B")
pyr = dict(N=pyring["N"], dtau_median=pq[1], sigma_90=(pq[2] - pq[0]) / (2 * 1.645), pred_RB_median=pr["shift_05_50_95"][1],
           z_RB=abs(pr["shift_05_50_95"][1]) / ((pq[2] - pq[0]) / (2 * 1.645)))

# Fisher da bancada (referencia): z_RB por SNR
fz = {(r["snr_ringdown"]): r["z_local"] for r in fisher["records"] if r["psd"] == "O4" and r["reading"] == "R-B" and r["scenario"] == "MASS_SPIN_FIXED_OPTIMISTIC"}
fisher_ref = dict(z_RB_O4_by_snr=fz, N5_snr40=fisher and next(r["identical_independent_events_for_median_5sigma"] for r in fisher["records"] if r["psd"] == "O4" and r["reading"] == "R-B" and r["scenario"] == "MASS_SPIN_FIXED_OPTIMISTIC" and r["snr_ringdown"] == 40.0),
                  snr_ratio_to_O4=ratios, z_RB_same_source={r["psd"]: r["z_local"] for r in fisher["same_source_R_B"]})

out = dict(frente="A", beta_runtime=BETA, rb_formula_check=rb_check, csv_vs_c4_max_abs_dev=max_dev,
           sets={k: len(v) for k, v in sets.items()}, combined_sigma_std=combined, combined_sigma_68=combined_68, audit_comparison=audit,
           scaling=scaling, lever=lever, excess_variance_df=excess, excess_variance_observed_sel31=obs_excess,
           c2_rb_fields_sd=sd_hits[:20], c2_rb_fields_mean=mean_hits[:20], sig_jit_used=SIG_JIT,
           pyring_GW250114=pyr, fisher_reference=fisher_ref, fontes_sha16=fontes,
           estatutos=dict(sigma_i="[REAL] largura do posterior LVK (pSEOBNRv5PHM / pseob-rd / pSEOBNRv4HM), NAO-CEGO",
                          pred_i="[DERIVED] condicional ao relogio [INPUT] (R-B) / [CONJECTURE] (R-MOD, R-LIN) / condicional (R-RAIZ-0); lidas do artefato da bancada, formula R-B conferida",
                          z_comb="[DERIVED] filtro casado gaussiano com sigma_i posteriores; ignora sistematica de familia e vies do estimador",
                          escala_O5_ET_CE="[DERIVED] mesma populacao, razao de SNR de fonte fixa (C5 same_source_R_B), um detector; cenario, nao cronograma",
                          excesso_var="[DERIVED] condicional ao desenrolamento (sd_jit=0.0192) e a sigma_i nulos calibrados"))
json.dump(out, open(HERE / "A_poder_eventos.json", "w", encoding="utf-8"), indent=1, default=float)

# tabela 5 sigma (CSV)
with open(HERE / "A2_tabela_5sigma.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["leitura", "quantidade", "valor", "condicao"])
    for rd in READINGS:
        s = scaling[rd]; c = combined["sel31_GWTC5"][rd]; c39 = combined["union39_GWTC5+GWTC3only"][rd]
        w.writerow([rd, "z_comb_sel31_O4 (filtro casado, offset=0)", f"{c['z_matched']:.3f}", "31 eventos GWTC-5.0, sigma_i=std posterior"])
        w.writerow([rd, "z_comb_all33_O4", f"{combined['all33_GWTC5'][rd]['z_matched']:.3f}", "33"])
        w.writerow([rd, "z_comb_union39_O4", f"{c39['z_matched']:.3f}", "33+6 GWTC-3-only"])
        w.writerow([rd, "z_slope_sel31_O4 (tendencia, offset livre)", f"{c['z_slope_fisher']:.3f}", "Fisher da inclinacao"])
        w.writerow([rd, "N_5sigma_like_median_O4", f"{s['N5_like_median_O4']:.0f}", "eventos como a mediana dos 31"])
        w.writerow([rd, "N_5sigma_like_GW250114_O4", f"{s['N5_like_GW250114_O4']:.0f}", "eventos como o GW250114"])
        w.writerow([rd, "N_5sigma_same_mix_matched_O4", f"{c['N_for_5sigma_matched_same_mix']:.0f}", "catalogo como o dos 31, offset=0"])
        w.writerow([rd, "N_5sigma_same_mix_slope_O4", f"{c['N_for_5sigma_slope_same_mix']:.0f}", "catalogo como o dos 31, offset livre"])
        for psd in ["O5", "ET", "CE"]:
            w.writerow([rd, f"N_5sigma_like_GW250114_{psd}", f"{s[f'N5_like_GW250114_{psd}']:.1f}", f"SNR x{ratios[psd]:.2f}, mesma fonte"])
            w.writerow([rd, f"N_5sigma_like_median_{psd}", f"{s[f'N5_like_median_{psd}']:.0f}", f"SNR x{ratios[psd]:.2f}, mesma populacao"])
            w.writerow([rd, f"N_5sigma_same_mix_slope_{psd}", f"{len(sel31) * (Z5 / s[f'z_slope_sel31_{psd}_same_population'])**2:.0f}", "offset livre, mesma populacao"])
    e = excess["sigma_df_std"]
    w.writerow(["df-jitter", "N_5sigma_like_GW250114_O4", f"{e['N5_like_GW250114']:.0f}", f"sigma_df={e['sigma_df_GW250114']:.4f}, sd_jit={SIG_JIT}"])
    w.writerow(["df-jitter", "N_5sigma_like_median_O4", f"{e['N5_like_median']:.0f}", f"sigma_df={e['sigma_df_median_sel31']:.4f}"])
    w.writerow(["df-jitter", "z_comb_sel31_O4", f"{e['z_comb_sel31']:.3f}", "31 reais"])
    for psd in ["O5", "ET", "CE"]:
        w.writerow(["df-jitter", f"N_5sigma_like_GW250114_{psd}", f"{e[f'N5_like_GW250114_{psd}']:.1f}", "mesma fonte"])
        w.writerow(["df-jitter", f"N_5sigma_like_median_{psd}", f"{e[f'N5_like_median_{psd}']:.0f}", "mesma populacao"])

print(json.dumps(dict(rb_check=rb_check, csv_dev=max_dev, audit=audit, sets=out["sets"]), indent=1, default=float))
for k in sets:
    m = combined[k]["_meta"]; print(k, "N", m["N"], "sigma_comb %.4f" % m["sigma_comb"], "wmean_dtau %.4f" % m["weighted_mean_dtau_obs"], "z_vs_GR %.2f" % m["z_weighted_mean_vs_GR"], "n_pos", m["n_positive_median"])
    for rd in READINGS:
        c = combined[k][rd]
        print("   %-9s z_matched %.3f z_common %.3f z_slope %.3f | fit s=%.2f+-%.2f c=%.3f+-%.3f chi2/dof %.1f/%d | N5 matched %.0f slope %.0f" % (
            rd, c["z_matched"], c["z_common_mean"], c["z_slope_fisher"], c["fit_slope"], c["fit_sigma_slope"], c["fit_intercept"], c["fit_sigma_intercept"], c["fit_chi2"], c["fit_dof"],
            c["N_for_5sigma_matched_same_mix"], c["N_for_5sigma_slope_same_mix"]))
print("SCALING"); print(json.dumps(scaling, indent=1, default=float))
print("LEVER"); print(json.dumps(lever, indent=1, default=float))
print("EXCESS"); print(json.dumps(excess["sigma_df_std"], indent=1, default=float)); print(json.dumps(obs_excess, indent=1, default=float))
print("C2 sd fields", sd_hits[:12]); print("C2 mean fields", mean_hits[:12])
print("PYRING", pyr); print("FISHER_REF", fisher_ref)
print("FONTES", json.dumps(fontes, indent=1))
