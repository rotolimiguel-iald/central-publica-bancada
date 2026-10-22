# -*- coding: utf-8 -*-
"""Auditor da gerencia (frente E0/E1) — REFAZ por script, a partir do C4_CATALOG_220.json da bancada
(sha16 conferido) e dos insumos da gerencia (so leitura), os numeros do portao e do nuisance.
Escreve SOMENTE em scratchpad/aud013bis/E0_E1/REFEITOS_E0_E1.json."""
import json, math, hashlib, os, sys
import numpy as np
from scipy import stats

B = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
G = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_013BIS_INSUMOS\medicao_da_ampliacao"
OUT = os.path.dirname(os.path.abspath(__file__))
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
BETA = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
Z90 = stats.norm.ppf(0.95)          # 1.6448536...
N90_FACTOR = (5 + stats.norm.ppf(0.90))**2 / 25   # (5+1.2816)^2/25 = 1.5783
READINGS = ["R-B", "R-MOD", "R-RAIZ-0", "R-LIN"]

def sha16(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]

R = {"beta_runtime": BETA, "N90_factor": N90_FACTOR, "fontes_sha16": {}}
def src(p):
    R["fontes_sha16"][p] = sha16(p); return p

c220 = json.load(open(src(os.path.join(B, "C4_CATALOG_220.json")), encoding="utf-8"))
assert R["fontes_sha16"][os.path.join(B, "C4_CATALOG_220.json")] == "93bdc413130d294a", "sha do C4_CATALOG_220 divergente"
ccomb = json.load(open(src(os.path.join(B, "C4_CATALOG_COMBINATION.json")), encoding="utf-8"))
sel31 = set(ccomb["selected_events"])
summ = json.load(open(src(os.path.join(G, "A_poder_eventos", "samples_summary.json")), encoding="utf-8"))
std_full = {(r["catalog"], r["event"]): r for r in summ["rows"]}
rend = json.load(open(src(os.path.join(G, "B_catalogos", "RENDIMENTO_E_5SIGMA.json")), encoding="utf-8"))
join = json.load(open(src(os.path.join(B, "bis", "e0_metadata", "SNR_JOIN_FOR_A.json")), encoding="utf-8"))

# ---------- eventos GWTC-5.0 (33) ----------
ev = []
for row in c220["rows"]:
    q = row["quantiles"]; d05, d50, d95 = q["dtau220"]; f05, f50, f95 = q["df220"]
    s = std_full.get(("GWTC5.0", row["event"]))
    ev.append(dict(event=row["event"], cat="GWTC5", in31=row["event"] in sel31, d50=d50,
                   sig_q90=(d95 - d05) / (2 * Z90), sig_std=s["dtau220"]["std"] if s else None,
                   sigf_q90=(f95 - f05) / (2 * Z90), sigf_std=s["df220"]["std"] if s else None,
                   pred={r["reading"]: r["shift_05_50_95"][1] for r in row["rows"] if r["reading"] in READINGS}))
# ---------- GWTC-3 (18) -> os 6 so-GWTC-3 para a uniao 39 ----------
try:
    c3 = json.load(open(src(os.path.join(B, "C4_GWTC3_220.json")), encoding="utf-8"))
    names5 = {e["event"] for e in ev}
    ev3 = []
    for row in c3["rows"]:
        q = row["quantiles"]; d05, d50, d95 = q["dtau220"]
        s = std_full.get(("GWTC3", row["event"])) or std_full.get(("GWTC-3", row["event"]))
        ev3.append(dict(event=row["event"], cat="GWTC3", in31=False, d50=d50, sig_q90=(d95 - d05) / (2 * Z90),
                        sig_std=s["dtau220"]["std"] if s else None,
                        pred={r["reading"]: r["shift_05_50_95"][1] for r in row["rows"] if r["reading"] in READINGS}))
    only3 = [e for e in ev3 if e["event"] not in names5]
    R["GWTC3_rows"] = len(ev3); R["GWTC3_only_for_union"] = [e["event"] for e in only3]
except Exception as exc:
    ev3, only3 = [], []; R["GWTC3_rows"] = f"NAO LIDO: {exc}"

def comb(events, conv):
    key = "sig_q90" if conv == "q90" else "sig_std"
    events = [e for e in events if e.get(key) is not None]
    y = np.array([e["d50"] for e in events]); s = np.array([e[key] for e in events]); w = 1 / s**2
    N = len(events); wmean = float((w * y).sum() / w.sum()); swm = float(1 / math.sqrt(w.sum()))
    out = {"_meta": dict(N=N, I=float(w.sum()), GW250114_equiv=float(w.sum() * 0.058**2),
                         weighted_mean=wmean, se=swm, z_vs_zero=wmean / swm,
                         N_5sigma_contra_RG_se_vies_persistir=N * (5 / (wmean / swm))**2,
                         sigma_median=float(np.median(s)), sigma_min=float(s.min()))}
    for rd in READINGS:
        p = np.array([e["pred"][rd] for e in events]); z = math.sqrt(((p / s)**2).sum())
        N50 = N * (5 / z)**2; N90 = N90_FACTOR * N50
        Iaa = float((w * p**2).sum() - (w * p).sum()**2 / w.sum()); zs = math.sqrt(Iaa)
        pbar = float((w * p).sum() / w.sum()); zobs = (wmean - pbar) / swm
        out[rd] = dict(z_comb=z, N50=N50, N90=N90, I90=N90 * float(np.mean(w)), GW250114_equiv_90=N90 * float(np.mean(w)) * 0.058**2,
                       z_slope=zs, N50_slope=N * (5 / zs)**2, z_obs_vs_pred_offset0=zobs,
                       N_spurious50=N * (5 / zobs)**2)
    return out

R["calibracao"] = {}
for name, events in (("GWTC5_31", [e for e in ev if e["in31"]]), ("GWTC5_33", ev), ("UNION39", ev + only3)):
    R["calibracao"][name] = {conv: comb(events, conv) for conv in ("q90", "std")}

# ---------- GW250114, pisos ----------
gw = [e for e in ev if e["event"].startswith("GW250114")][0]
R["GW250114"] = dict(sig_q90=gw["sig_q90"], sig_std=gw["sig_std"], sigf_q90=gw["sigf_q90"], sigf_std=gw["sigf_std"], pred=gw["pred"],
                     N50_like={rd: (5 * gw["sig_std"] / abs(gw["pred"][rd]))**2 for rd in READINGS},
                     N90_like={rd: N90_FACTOR * (5 * gw["sig_std"] / abs(gw["pred"][rd]))**2 for rd in READINGS},
                     piso_5={rd: abs(gw["pred"][rd]) / 5 for rd in READINGS}, piso_15={rd: abs(gw["pred"][rd]) / 15 for rd in READINGS})
R["n_sigma_le"] = {conv: {thr: sum(1 for e in ev if e[conv] is not None and e[conv] <= thr) for thr in (0.06, 0.10, 0.15, 0.20)} for conv in ("sig_q90", "sig_std")}

# ---------- nuisance c(sigma) = c0 + k sigma (WLS em medianas), subamostras ----------
def wls(events, key):
    events = [e for e in events if e.get(key) is not None]
    y = np.array([e["d50"] for e in events]); s = np.array([e[key] for e in events]); w = 1 / s**2
    X = np.column_stack([np.ones(len(y)), s]); cov = np.linalg.inv(X.T @ (w[:, None] * X)); b = cov @ X.T @ (w * y)
    rho = stats.spearmanr(s, y)
    subs = {}
    for cut in (0.15, 0.20, 0.25):
        m = s < cut
        if m.sum() >= 3:
            subs[f"sigma<{cut}"] = dict(n=int(m.sum()), wmean=float((w[m] * y[m]).sum() / w[m].sum()), se=float(1 / math.sqrt(w[m].sum())))
    return dict(N=len(y), c0=float(b[0]), se_c0=float(math.sqrt(cov[0, 0])), k=float(b[1]), se_k=float(math.sqrt(cov[1, 1])),
                spearman=[float(rho[0]), float(rho[1])], subamostras=subs, n_pos=int((y > 0).sum()))
R["nuisance_WLS"] = {name: {conv: wls(events, conv) for conv in ("sig_q90", "sig_std")}
                     for name, events in (("GWTC5_31", [e for e in ev if e["in31"]]), ("GWTC5_33", ev))}

# ---------- sigma(SNR): a tabela 2x2 (fonte do SNR x definicao da largura) ----------
snr_tgr = {e[0]: e[1] for e in rend["sigma_vs_snr_fit_31"]["events"]}
snr_gwosc_raw = {v["event"]: v["network_matched_filter_snr"] for v in join["events"] if v.get("network_matched_filter_snr") is not None}
snr_gwosc = {}
for e in ev:
    nm = e["event"]
    if nm in snr_gwosc_raw: snr_gwosc[nm] = float(snr_gwosc_raw[nm])
    elif nm.split("_")[0] in snr_gwosc_raw: snr_gwosc[nm] = float(snr_gwosc_raw[nm.split("_")[0]])
def fit_ln(pairs):
    x = np.log([p[0] for p in pairs]); y = np.log([p[1] for p in pairs])
    res = stats.linregress(x, y); resid = y - (res.intercept + res.slope * x)
    return dict(N=len(pairs), A=float(math.exp(res.intercept)), p=float(res.slope), resid_sd_ln=float(np.std(resid, ddof=2)),
                sigma_at=[{"SNR": s_, "median_sigma": float(math.exp(res.intercept) * s_**res.slope)} for s_ in (30, 53, 76.9, 78.6, 95)])
e31 = [e for e in ev if e["in31"]]
R["sigma_vs_SNR_2x2"] = {}
for src_name, table in (("SNR_TGR_tabela2", snr_tgr), ("SNR_GWOSC", snr_gwosc)):
    for conv in ("sig_q90", "sig_std"):
        pairs = [(table[e["event"]], e[conv]) for e in e31 if e["event"] in table and e[conv] is not None]
        R["sigma_vs_SNR_2x2"][f"{src_name}__{conv}"] = fit_ln(pairs) if len(pairs) >= 5 else f"so {len(pairs)} pares"
R["SNR_GWOSC_lidos"] = len(snr_gwosc)

# ---------- rota IV: checagem rapida do N90 (sigma_jit 0.0228; N=38 vs 39), LRT>25 ----------
rng = np.random.default_rng(20260923)
def lrt_vec(Y, s2m, grid):
    N = Y.shape[1]; mu0 = Y.mean(axis=1, keepdims=True)
    l0 = -0.5 * (((Y - mu0)**2).sum(axis=1) / s2m + N * math.log(s2m)); best = l0.copy()
    for s2 in grid:
        v = s2m + s2; l = -0.5 * (((Y - mu0)**2).sum(axis=1) / v + N * math.log(v)); best = np.maximum(best, l)
    return 2 * (best - l0)
sm = gw["sigf_std"]; grid = np.geomspace(1e-7, 0.5, 300)
R["rota_IV_poder_MC_8000"] = {}
for sj, Ns in ((0.019, (59, 61)), (0.0228, (38, 39)), (0.03, (21, 22))):
    for N in Ns:
        Y = rng.normal(0, math.sqrt(sm**2 + sj**2), size=(8000, N))
        R["rota_IV_poder_MC_8000"][f"sj={sj},N={N}"] = float((lrt_vec(Y, sm**2, grid) > 25).mean())

json.dump(R, open(os.path.join(OUT, "REFEITOS_E0_E1.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
print(json.dumps(R, indent=1, ensure_ascii=False, default=str))
