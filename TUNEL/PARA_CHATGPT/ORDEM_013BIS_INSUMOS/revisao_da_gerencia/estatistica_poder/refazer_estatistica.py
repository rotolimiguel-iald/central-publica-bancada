# -*- coding: utf-8 -*-
"""Revisao adversarial — lente ESTATISTICA E PODER (ORDEM 013-bis §4.0, E0–E6).
Refaz por script os numeros centrais a partir do C4_CATALOG_220.json da bancada (so leitura)
e do CSV da frente A. Escreve so nesta pasta."""
import json, math, csv, hashlib, sys
from pathlib import Path
import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
BANCADA = Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN")
MEDIR = HERE.parent.parent / "medir"

def sha16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]

out = {"fontes_sha16": {}}
ALPHA = 7.2973525693e-3  # CODATA 2018
beta = ALPHA * math.sqrt(math.e)
out["beta_runtime"] = beta

# ---------- 1. catalogo 31 da bancada: z_comb, media ponderada, N5, N90, falsificador espurio ----------
cat = json.load(open(BANCADA / "C4_CATALOG_220.json"))
out["fontes_sha16"]["C4_CATALOG_220.json"] = sha16(BANCADA / "C4_CATALOG_220.json")
rows = cat["rows"]
R = ["R-B", "R-MOD", "R-RAIZ-0", "R-LIN"]
in31 = [r for r in rows if r.get("in31", True) and r["event"] not in ("GW191109_010717", "GW200208_130117")]
# a bancada marca in31 via 'catalog'? usamos a lista da frente C (33 menos os dois controles)
ev31 = []
for r in rows:
    q = r["quantiles"]["dtau220"]
    sig = (q[2] - q[0]) / (2 * 1.645)
    pred = {k: next(x for x in r["rows"] if x["reading"] == k)["shift_05_50_95"][1] for k in R}
    ev31.append(dict(event=r["event"], med=q[1], q05=q[0], q95=q[2], sig=sig, pred=pred))
excl = {"GW191109_010717", "GW200208_130117"}
e31 = [e for e in ev31 if e["event"] not in excl]
out["N_rows_total"] = len(ev31); out["N_31"] = len(e31)
sig = np.array([e["sig"] for e in e31]); med = np.array([e["med"] for e in e31])
w = 1 / sig**2
wm = float((w * med).sum() / w.sum()); swm = float(1 / math.sqrt(w.sum()))
out["media_ponderada_31"] = dict(wmean=wm, sigma=swm, z_vs_0=wm / swm)
res = {}
for k in R:
    pred = np.array([e["pred"][k] for e in e31])
    z_comb = float(math.sqrt(((pred / sig) ** 2).sum()))
    pw = float((w * pred).sum() / w.sum())
    z_obs = (wm - pw) / swm
    N5 = 31 * 25 / z_comb**2
    N5_contra = 31 * 25 / z_obs**2
    res[k] = dict(z_comb_offset0=z_comb, N5_mistura31_poder50=N5, N90_mistura31=N5 * (5 + stats.norm.ppf(0.9)) ** 2 / 25,
                  pred_wmean=pw, z_obs_vs_pred=float(z_obs), N_5sigma_contra_leitura_se_vies_persistir=float(N5_contra))
out["catalogo31_gauss"] = res
out["N_5sigma_contra_RG_se_vies_persistir"] = 31 * 25 / (wm / swm) ** 2
out["fator_N90_N50_filtro_casado"] = (5 + stats.norm.ppf(0.9)) ** 2 / 25
out["z_090"] = float(stats.norm.ppf(0.9))

# ---------- 2. GW250114 ----------
g = next(e for e in e31 if e["event"].startswith("GW250114"))
out["GW250114"] = dict(q05_50_95=[g["q05"], g["med"], g["q95"]], sigma_gauss=g["sig"],
                       z_i={k: abs(g["pred"][k]) / g["sig"] for k in R},
                       N5_like={k: 25 / (g["pred"][k] / g["sig"]) ** 2 for k in R},
                       N90_like={k: 25 / (g["pred"][k] / g["sig"]) ** 2 * out["fator_N90_N50_filtro_casado"] for k in R})

# ---------- 3. regressao c(sigma) = c0 + k*sigma (WLS 1/sigma^2) e Spearman ----------
X = np.vstack([np.ones_like(sig), sig]).T
W = np.diag(w)
cov = np.linalg.inv(X.T @ W @ X)
bhat = cov @ X.T @ W @ med
out["c_sigma_WLS_31"] = dict(c0=float(bhat[0]), c0_se=float(math.sqrt(cov[0, 0])), k=float(bhat[1]), k_se=float(math.sqrt(cov[1, 1])),
                             c0_vs_0_sigma=float(bhat[0] / math.sqrt(cov[0, 0])),
                             c0_vs_RB_pred_sigma=float((bhat[0] - res["R-B"]["pred_wmean"]) / math.sqrt(cov[0, 0])))
sp = stats.spearmanr(med, sig)
out["spearman_med_vs_sigma_31"] = [float(sp[0]), float(sp[1])]
n_pos = int((med > 0).sum()); out["n_medianas_positivas_31"] = n_pos

# ---------- 4. contagens por sigma ----------
out["n_sigma_le"] = {t: int((sig <= t).sum()) for t in (0.06, 0.10, 0.15, 0.20)}
out["sigma_mediana_31"] = float(np.median(sig))

# ---------- 5. limiar LRT mistura 1/2 delta0 + 1/2 chi2_1 ----------
p5 = float(stats.norm.sf(5)); out["p_5sigma_unilateral"] = p5
# P(LRT>c) = 1/2 P(chi2_1>c) = 1 - Phi(sqrt c)  => c = 25
out["LRT_crit_mistura"] = float(stats.norm.isf(p5) ** 2)
out["LRT_23p9_equivale_z"] = math.sqrt(23.9)

# ---------- 6. rota IV: peso 1/sigma^4 e forma fechada ----------
d2 = json.load(open(MEDIR / "D_realizacao_unica" / "d2_resultado.json"))
out["fontes_sha16"]["d2_resultado.json"] = sha16(MEDIR / "D_realizacao_unica" / "d2_resultado.json")
s31 = np.array(d2["sigma_meas_reference"]["sorted_31"]); s0 = s31[0]
out["peso_1_sobre_sigma4_em_GW250114"] = float(((s0 / s31) ** 4).sum())
out["peso_1_sobre_sigma2_em_GW250114_controle"] = float(((s0 / s31) ** 2).sum())
# forma fechada score: var(sigma_jit^2 hat) ~ 2 (s^2+sj^2)^2 / N  -> z = sj^2 sqrt(N/2)/(s^2+sj^2) ; N = 2*25*((s^2+sj^2)/sj^2)^2
def N_score(s, sj): return 2 * 25 * ((s**2 + sj**2) / sj**2) ** 2
out["N_score_forma_fechada"] = {str(sj): N_score(s0, sj) for sj in (0.01, 0.019, 0.0228, 0.03)}
out["N_score_mediana_0p0803_sj0p019"] = N_score(0.0803356, 0.019)

# ---------- 7. Poisson IC90 para 1 contagem em 1,45 ano ----------
lo = stats.chi2.ppf(0.05, 2) / 2; hi = stats.chi2.ppf(0.95, 4) / 2
out["poisson_IC90_1_contagem"] = dict(contagem=[lo, hi], por_ano=[lo / 1.45, hi / 1.45], anos_equiv=21 / 14.482758620689655)

# ---------- 8. banda O5: N5 e z ao fim de 3 anos ----------
z31 = {k: res[k]["z_comb_offset0"] for k in R}
zA = 0.6063  # A, sigma=std (o que a ordem cita)
rate = 14.482758620689655
def z_fim_O5(z0, g_snr, g_vol): return z0 * g_snr * math.sqrt(3 * rate * g_vol**3 / 31)
gB = (1.5625, 1.7857142857142858); gC5 = 1.987; gBNS = 2.0625
out["O5_z_RB_3anos"] = dict(
    min_BBH=z_fim_O5(zA, gB[0], gB[0]), max_BBH=z_fim_O5(zA, gB[1], gB[1]),
    C5_1p99_vol_BBH_max=z_fim_O5(zA, gC5, gB[1]), BNS_2p06_vol_BBH_max=z_fim_O5(zA, gBNS, gB[1]),
    N_eventos_3anos=[3 * rate * gB[0]**3, 3 * rate * gB[1]**3])
out["O5_z_RMOD_3anos"] = dict(min_BBH=z_fim_O5(1.0765, gB[0], gB[0]), max_BBH=z_fim_O5(1.0765, gB[1], gB[1]),
                              C5=z_fim_O5(1.0765, gC5, gB[1]), BNS=z_fim_O5(1.0765, gBNS, gB[1]))
out["O5_z_RRAIZ0_3anos"] = dict(min_BBH=z_fim_O5(1.12, gB[0], gB[0]), max_BBH=z_fim_O5(1.12, gB[1], gB[1]),
                                C5=z_fim_O5(1.12, gC5, gB[1]), BNS=z_fim_O5(1.12, gBNS, gB[1]))
N212 = 212.03
out["O5_N50_RB_GW250114_like"] = dict(BBH=[N212 / gB[1]**2, N212 / gB[0]**2], C5=N212 / gC5**2, BNS=N212 / gBNS**2)
out["O5_N50_RB_mistura"] = dict(BBH=[2110.36 / gB[1]**2, 2110.36 / gB[0]**2], C5=2110.36 / gC5**2, BNS=2110.36 / gBNS**2)

# ---------- 9. 3G: N com SNR_RD>=50 depende da ancora ----------
dmed = 0.0202412743  # B usa |pred| mediana
for anc in (40.0, 34.28):
    s50 = 0.058 * anc / 50; s100 = 0.058 * anc / 100
    out[f"3G_N5_RB_ancora_SNR{anc}"] = dict(N_SNR50=25 / (dmed / s50) ** 2, N_SNR100=25 / (dmed / s100) ** 2,
                                          N90_SNR50=25 / (dmed / s50) ** 2 * out["fator_N90_N50_filtro_casado"])
out["SNR_RD_equiv_GW250114_por_2_sobre_rho"] = 2 / 0.058

# ---------- 10. ajuste sigma(SNR) e o corte ----------
A_, p_ = 3.026648868069853, -0.8599154128207724
out["fit_sigma_at_SNR"] = {str(s): A_ * s**p_ for s in (53, 76.9, 78.6, 95)}
out["SNR_para_sigma"] = {str(t): (t / A_) ** (1 / p_) for t in (0.06, 0.10)}
out["resid_0p244_e_ln_nao_dex"] = dict(ln=0.24446, dex=0.24446 / math.log(10))

# ---------- 11. custo por evento e calibracao ----------
t_onda = 0.0975
out["cpu_h_evento_pSEOB"] = [3e6 * t_onda / 3600, 2e7 * t_onda / 3600]
out["cpu_h_evento_pSEOB_com_0p095"] = [3e6 * 0.095 / 3600, 2e7 * 0.095 / 3600]
piso = {k: abs(g["pred"][k]) / 5 for k in R}
n_inj = {k: (0.049739 / piso[k]) ** 2 for k in R}
out["piso"] = piso; out["n_injecoes_por_celula"] = n_inj
c = n_inj["R-B"] * np.array(out["cpu_h_evento_pSEOB"])
out["calibracao_RB_10_celulas_CPU_h"] = list(c * 10); out["dias_parede_22w"] = list(c * 10 / 22 / 24)
out["fator_6p7"] = out["cpu_h_evento_pSEOB"][1] / out["cpu_h_evento_pSEOB"][0]

# ---------- 12. 440 ----------
jm = json.load(open(BANCADA / "C4_JOINT_MODES.json"))
out["fontes_sha16"]["C4_JOINT_MODES.json"] = sha16(BANCADA / "C4_JOINT_MODES.json")
r440 = {x["reading"]: x["shift_440_05_50_95"][1] for x in jm["rows"] if x["reading"] in R}
r220 = {x["reading"]: x["shift_220_05_50_95"][1] for x in jm["rows"] if x["reading"] in R}
out["440"] = dict(shift440=r440, razao_440_sobre_220={k: r440[k] / r220[k] for k in R})

# ---------- 13. estimador SNR20 (N=50): erro padrao ----------
D = json.load(open(MEDIR / "D_realizacao_unica" / "D_consolidado.json"))
c2 = D["realizacao_unica_referencia_68p1_0p68"]["C2_RG_ruido_lido"]["SYNTHETIC_COLORED_OU_PLUS_WHITE"]
sd_est = (c2["dtau_q"][2] - c2["dtau_q"][0]) / (2 * 1.645)
out["estimador_SNR20"] = dict(mean=c2["mean_dtau"], mediana=c2["dtau_q"][1], sd_gauss_equiv=sd_est, se_mean_N50=sd_est / math.sqrt(50))

# ---------- 14. jitter: compatibilidade 0.0192 (N=50) vs 0.0228 ----------
out["jitter_sd_compat"] = dict(se_sd_N50=0.0192 / math.sqrt(2 * 50), z_0192_vs_0228=(0.0228 - 0.0192) / (0.0192 / math.sqrt(100)))

json.dump(out, open(HERE / "REFEITOS_REVISAO.json", "w"), indent=1, ensure_ascii=False, default=float)
print(json.dumps(out, indent=1, ensure_ascii=False, default=float))
