# -*- coding: utf-8 -*-
"""Critico de completude — refaz numeros centrais da SINTESE a partir dos arquivos da bancada
(so leitura) e das frentes. Calculo leve (numpy). Escreve REFEITOS.json nesta pasta."""
import json, math, hashlib, csv, os, sys
import numpy as np
from scipy import stats
from scipy.optimize import brentq

BANCADA = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
MEDIR = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\ordem013\bis\medir"
OUT = os.path.join(MEDIR, "CRITICO_completude", "REFEITOS.json")

ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
BETA = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)

def sha16(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]

R = {"beta_runtime": BETA, "fontes_sha16": {}}
Q90 = 1.6448536269514722  # z_0.95

# ---------- 1. catalogo da bancada: z_comb (filtro casado) dos 31 / 33 ----------
p220 = os.path.join(BANCADA, "C4_CATALOG_220.json")
pcomb = os.path.join(BANCADA, "C4_CATALOG_COMBINATION.json")
R["fontes_sha16"][p220] = sha16(p220)
R["fontes_sha16"][pcomb] = sha16(pcomb)
c220 = json.load(open(p220, encoding="utf-8"))
ccomb = json.load(open(pcomb, encoding="utf-8"))
sel31 = set(ccomb["selected_events"])
READINGS = ["R-B", "R-MOD", "R-RAIZ-0", "R-LIN"]

ev = []
for row in c220["rows"]:
    q = row["quantiles"]
    d05, d50, d95 = q["dtau220"]
    f05, f50, f95 = q["df220"]
    sig_tau = (d95 - d05) / (2 * Q90)
    sig_f = (f95 - f05) / (2 * Q90)
    preds = {}
    for r in row["rows"]:
        if r["reading"] in READINGS:
            preds[r["reading"]] = r["shift_05_50_95"][1]
    ev.append(dict(event=row["event"], in31=row["event"] in sel31, d50=d50, sig_tau=sig_tau,
                   f50=f50, sig_f=sig_f, spin=q["spin"][1], M=q["mass_detector"][1], pred=preds))

def comb(events):
    out = {}
    y = np.array([e["d50"] for e in events]); s = np.array([e["sig_tau"] for e in events]); w = 1 / s**2
    wmean = float((w * y).sum() / w.sum()); swm = float(1 / math.sqrt(w.sum()))
    out["_meta"] = dict(N=len(events), weighted_mean_dtau=wmean, sigma_weighted_mean=swm, z_vs_zero=wmean / swm,
                        sigma_min=float(s.min()), sigma_median=float(np.median(s)))
    for rd in READINGS:
        p = np.array([e["pred"][rd] for e in events])
        z_i = p / s
        z_matched = float(math.sqrt((z_i**2).sum()))  # E[z] se a leitura for verdadeira, offset fixo em 0
        # intercepto livre (Fisher da inclinacao a com obs = c + a*pred): I_aa = sum w p^2 - (sum w p)^2 / sum w
        Iaa = float((w * p**2).sum() - (w * p).sum()**2 / w.sum())
        z_slope = math.sqrt(Iaa)
        # z observado contra a predicao (offset fixo em 0): (wmean - pbar)/swm
        pbar = float((w * p).sum() / w.sum())
        z_obs_vs_pred = (wmean - pbar) / swm
        out[rd] = dict(z_matched=z_matched, N5_matched_same_mix=len(events) * (5 / z_matched)**2,
                       z_slope_free_intercept=z_slope, N5_slope_same_mix=len(events) * (5 / z_slope)**2,
                       pred_weighted_mean=pbar, z_obs_vs_pred_offset0=z_obs_vs_pred,
                       # N em que o desvio ATUAL (se persistir como vies comum) daria 5 sigma CONTRA a leitura
                       N_5sigma_contra_leitura_se_vies_persistir=len(events) * (5 / z_obs_vs_pred)**2 if z_obs_vs_pred > 0 else None)
    return out

R["catalogo_31"] = comb([e for e in ev if e["in31"]])
R["catalogo_33"] = comb(ev)
R["n_sigma_tau_le"] = {thr: sum(1 for e in ev if e["sig_tau"] <= thr) for thr in (0.06, 0.10, 0.15, 0.20)}
R["n_sigma_tau_le_31"] = {thr: sum(1 for e in ev if e["in31"] and e["sig_tau"] <= thr) for thr in (0.06, 0.10, 0.15, 0.20)}
gw = [e for e in ev if e["event"].startswith("GW250114")][0]
R["GW250114"] = dict(sig_tau=gw["sig_tau"], sig_f=gw["sig_f"], pred=gw["pred"],
                     z_per_reading={rd: abs(gw["pred"][rd]) / gw["sig_tau"] for rd in READINGS},
                     N5_like={rd: (5 * gw["sig_tau"] / abs(gw["pred"][rd]))**2 for rd in READINGS})

# ---------- 2. Fisher fonte fixa SNR40 (bancada C5_FISHER) ----------
pf = os.path.join(BANCADA, "C5_FISHER.json"); R["fontes_sha16"][pf] = sha16(pf)
fis = json.load(open(pf, encoding="utf-8"))
def find(o, key, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key: yield path + "/" + k, v
            yield from find(v, key, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from find(v, key, path + f"[{i}]")
R["C5_FISHER_top_keys"] = list(fis.keys())[:30]

# ---------- 3. limiar do LRT na fronteira ----------
# H0: LRT ~ 1/2 delta_0 + 1/2 chi2_1. P(LRT>c) = 1/2 P(chi2_1 > c) = p5 => c = z5^2 = 25
p5 = stats.norm.sf(5.0)
c_mix = brentq(lambda c: 0.5 * stats.chi2.sf(c, 1) - p5, 1, 60)
R["limiar_LRT"] = dict(p5_unilateral=p5, c_mistura_meia_delta0_meia_chi2_1=c_mix, c_chi2_1_puro=stats.chi2.isf(p5, 1),
                       z_equivalente_a_23p9_na_mistura=math.sqrt(23.9), p_na_mistura_para_23p9=0.5 * stats.chi2.sf(23.9, 1))

# ---------- 4. rota IV: N para 5 sigma na variancia de df (LRT hierarquico), MC vetorizado ----------
rng = np.random.default_rng(20260922)
def lrt_vec(Y, s2_meas, s2_grid):
    """LRT (mu perfilado) vetorizado: Y (n_mc, N), sigma_meas homogeneo."""
    n_mc, N = Y.shape
    # s2 = 0
    mu0 = Y.mean(axis=1, keepdims=True)
    l0 = -0.5 * (((Y - mu0)**2).sum(axis=1) / s2_meas + N * math.log(s2_meas))
    best = l0.copy()
    for s2 in s2_grid:
        v = s2_meas + s2
        mu = Y.mean(axis=1, keepdims=True)  # pesos iguais (homogeneo) => mu = media
        l = -0.5 * (((Y - mu)**2).sum(axis=1) / v + N * math.log(v))
        best = np.maximum(best, l)
    return 2 * (best - l0)

def power(N, sm, sj, n_mc, crit=25.0):
    Y = rng.normal(0, math.sqrt(sm**2 + sj**2), size=(n_mc, N))
    grid = np.geomspace(1e-7, 0.5, 300)
    L = lrt_vec(Y, sm**2, grid)
    return float((L > crit).mean())

sm = R["GW250114"]["sig_f"]
R["rota_IV"] = {"sigma_meas_GW250114": sm, "closed_form_N_score": {}, "poder_MC_LRT_crit25": {}}
for sj in (0.019, 0.0228, 0.03):
    R["rota_IV"]["closed_form_N_score"][str(sj)] = 50 * (sm / sj)**4
    for N in (20, 28, 33, 35, 45, 59):
        R["rota_IV"]["poder_MC_LRT_crit25"][f"sj={sj},N={N}"] = power(N, sm, sj, 4000)
# limiar 23.9 vs 25 no poder, no caso central
R["rota_IV"]["poder_MC_sj0.019_N59_crit23.9"] = None
Y = rng.normal(0, math.sqrt(sm**2 + 0.019**2), size=(4000, 59)); L = lrt_vec(Y, sm**2, np.geomspace(1e-7, 0.5, 300))
R["rota_IV"]["poder_MC_sj0.019_N59_crit23.9"] = float((L > 23.9).mean()); R["rota_IV"]["poder_MC_sj0.019_N59_crit25_repl"] = float((L > 25).mean())

# FPR sob H0 (sigma_jit = 0) para N = 59 com sigma homogeneo: cauda da mistura em caudas moderadas (2e5 draws)
Y0 = rng.normal(0, sm, size=(200000, 59)); L0 = lrt_vec(Y0, sm**2, np.geomspace(1e-7, 0.5, 300))
fpr = {}
for c in (2.706, 6.25, 9.0, 12.25, 16.0):
    fpr[str(c)] = dict(MC=float((L0 > c).mean()), mistura=0.5 * stats.chi2.sf(c, 1), n_hits=int((L0 > c).sum()))
R["rota_IV"]["FPR_H0_N59_sigma_homogeneo_2e5"] = fpr
R["rota_IV"]["nota"] = "MC e sigma_i homogeneo, mu perfilado; a calibracao a 2.9e-7 exigiria >= 1e8 draws (nao feito por ninguem)."

# ---------- 5. Poisson do 'GW250114-like' (1 evento) ----------
lo, hi = 0.5 * stats.chi2.ppf(0.05, 2 * 1), 0.5 * stats.chi2.ppf(0.95, 2 * (1 + 1))
anos = 21 / 14.482758620689655
R["taxa_GW250114_like"] = dict(contagem=1, anos_equiv=anos, taxa_pontual=1 / anos, IC90_contagem=[lo, hi],
                               IC90_taxa_por_ano=[lo / anos, hi / anos],
                               anos_O5_para_N5_RB_com_IC90=[[87.0 / (hi / anos * f**3), 50.0 / (lo / anos * f**3)] for f in (1.5625, 2.0625)],
                               nota="rendimento de eventos GW250114-like: UMA contagem; a taxa e um chute com IC90 de duas ordens de grandeza")

# ---------- 6. O5 ao fim de 3 anos: banda coerente (BBH) vs banda da sintese ----------
z31 = R["catalogo_31"]["R-B"]["z_matched"]; rate = 14.482758620689655
def z_o5(f_snr, g_vol, anos=3):
    return z31 * math.sqrt(anos * rate * g_vol**3 / 31) * f_snr
R["O5_3anos_RB"] = dict(sintese_min=z_o5(1.5625, 1.5625), sintese_max=z_o5(2.0625, 1.7857),
                        BBH_coerente_min=z_o5(1.5625, 1.5625), BBH_coerente_max=z_o5(1.7857, 1.7857),
                        C5_PSD_1p987_com_vol_BBH_max=z_o5(1.987, 1.7857))

# ---------- 7. custo de calibracao da rota III: injecoes para fixar c a |delta|/5 ----------
sig_inj_snr40 = 0.049739133245355165  # Fisher fonte fixa SNR40 (C5_FISHER via frente C)
piso = {rd: abs(R["GW250114"]["pred"][rd]) / 5 for rd in READINGS}
cpu_lo, cpu_hi = 81, 542  # CPU-h por PE pSEOBNRv4HM_PA (frente E, [DERIVED] sobre [KNOWN])
n_inj = {rd: (sig_inj_snr40 / piso[rd])**2 for rd in READINGS}
R["calibracao_c_por_injecao"] = dict(sigma_por_injecao_SNR40=sig_inj_snr40, piso=piso, n_injecoes_por_celula=n_inj,
    custo_CPU_h_por_celula=[{rd: [n_inj[rd] * cpu_lo, n_inj[rd] * cpu_hi]} for rd in READINGS],
    celulas_minimas="5 bins de SNR x 2 familias = 10 celulas (sem varrer massa/spin)",
    custo_CPU_h_10_celulas_RB=[10 * n_inj["R-B"] * cpu_lo, 10 * n_inj["R-B"] * cpu_hi],
    dias_parede_22w_10_celulas_RB=[10 * n_inj["R-B"] * cpu_lo / 22 / 24, 10 * n_inj["R-B"] * cpu_hi / 22 / 24],
    nota="calibracao do nuisance c(SNR) a precisao do piso: numero que a sintese nao tem")

# ---------- 8. N em que o vies atual vira 5 sigma CONTRA a leitura ----------
R["N_falsificacao_espuria_se_vies_persistir"] = {rd: R["catalogo_31"][rd]["N_5sigma_contra_leitura_se_vies_persistir"] for rd in READINGS}

# ---------- 9. rendimento pSEOBNR O4b: conferir o 14 no parse da tabela ----------
pp = os.path.join(MEDIR, "B_catalogos", "gwtc5_tgr_table2_3_parsed.json")
try:
    R["fontes_sha16"][pp] = sha16(pp)
    t = json.load(open(pp, encoding="utf-8"))
    R["parse_gwtc5_tabela"] = dict(tipo=type(t).__name__, n=len(t), amostra=json.dumps(t[:2] if isinstance(t, list) else list(t.items())[:2])[:600])
except Exception as e:
    R["parse_gwtc5_tabela"] = f"NAO LIDO: {e}"

json.dump(R, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
print(json.dumps(R, indent=1, ensure_ascii=False, default=str))
