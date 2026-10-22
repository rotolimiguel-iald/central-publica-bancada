# -*- coding: utf-8 -*-
"""FRENTE D (2): o teste populacional da largura de delta_f_hat e o seu poder.

Modelo [INPUT]: y_i = mediana de df220 do evento i ~ N(mu, sigma_i^2 + s2), s2 = sigma_jit^2 >= 0.
H0: s2 = 0 (RG, ou TGL com desenrolamento sem jitter). H1: s2 > 0.
Teste 1 (score, forma fechada): U = 1/2 sum[(y_i-mu)^2 - sigma_i^2]/sigma_i^4, I = 1/2 sum 1/sigma_i^4,
   z = U/sqrt(I); sob H1, E[z] ~= s2 * sqrt(sum 1/sigma_i^4 / 2)  (mu conhecido; com mu estimado perde ~1 gl).
Teste 2 (LRT na fronteira): 2[l(mu_hat,s2_hat) - l(mu_hat0,0)] ~ 1/2 delta_0 + 1/2 chi2_1 sob H0.
Limiar 5 sigma unilateral: p = 2.8665e-7. Poder = P(rejeitar | s2), por Monte Carlo.
sigma_i vem dos quantis 05/95 publicados, (q95-q05)/(2*1.6449) [aproximacao gaussiana; INPUT].
"""
import os, sys, json, math, hashlib
import numpy as np
from scipy.stats import norm, chi2
from scipy.optimize import minimize_scalar

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = r'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN'
Z5 = 5.0
P5 = norm.sf(Z5)                       # 2.8665e-7 unilateral
LRT_CRIT = chi2.isf(2 * P5, 1)         # mistura 1/2 chi2_1: P(LRT>c) = 1/2 P(chi2_1>c) = P5
Q90 = 1.6448536269514722

def sha16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]

def sigma_from_q(q05, q95):
    return (q95 - q05) / (2 * Q90)

def loglik(y, s_i2, mu, s2):
    v = s_i2 + s2
    return float(-0.5 * np.sum((y - mu) ** 2 / v + np.log(v)))

def profile_mu(y, s_i2, s2):
    w = 1 / (s_i2 + s2)
    return float(np.sum(w * y) / np.sum(w))

def lrt_stat(y, s_i2, s2_max=10.):
    l0 = loglik(y, s_i2, profile_mu(y, s_i2, 0.), 0.)
    f = lambda s2: -loglik(y, s_i2, profile_mu(y, s_i2, s2), s2)
    r = minimize_scalar(f, bounds=(0., s2_max), method='bounded', options=dict(xatol=1e-12))
    s2_hat = r.x if -r.fun > l0 else 0.
    l1 = max(-r.fun, l0)
    return 2 * (l1 - l0), s2_hat

def score_z(y, s_i2):
    mu = profile_mu(y, s_i2, 0.)
    U = 0.5 * np.sum(((y - mu) ** 2 - s_i2) / s_i2 ** 2)
    I = 0.5 * np.sum(1 / s_i2 ** 2)
    return float(U / math.sqrt(I))

def n_for_5sigma_score(sigma_meas, sigma_jit):
    """Forma fechada (sigma homogeneo, mu conhecido): z = s2/sigma^2 sqrt(N/2) = 5 -> N = 50 (sigma/sigma_jit)^4."""
    return 50. * (sigma_meas / sigma_jit) ** 4

def power_mc(N, sigma_meas, sigma_jit, n_mc, rng, s2_max=10.):
    s_i2 = np.full(N, sigma_meas ** 2)
    hits = 0
    stats = np.empty(n_mc)
    for k in range(n_mc):
        y = rng.normal(0., np.sqrt(s_i2 + sigma_jit ** 2))
        stats[k], _ = lrt_stat(y, s_i2, s2_max)
        hits += stats[k] > LRT_CRIT
    return hits / n_mc, float(np.median(stats))

def n_for_power(sigma_meas, sigma_jit, target, rng, n_mc=300):
    """Menor N (busca geometrica + refinamento) com poder >= target no LRT a 5 sigma."""
    n0 = max(4, int(n_for_5sigma_score(sigma_meas, sigma_jit)))
    lo, hi = None, None
    N = n0
    for _ in range(40):
        pw, _ = power_mc(N, sigma_meas, sigma_jit, n_mc, rng)
        if pw >= target:
            hi = N
            if lo is not None and hi - lo <= max(1, int(0.05 * hi)):
                break
            N = int(N / 1.4) if lo is None else (lo + hi) // 2
        else:
            lo = N
            if hi is not None and hi - lo <= max(1, int(0.05 * hi)):
                break
            N = int(N * 1.4) + 1 if hi is None else (lo + hi) // 2
        if N > 200000:
            return None
    return hi

def main():
    rng = np.random.default_rng(20260922)
    out = dict(threshold=dict(z=Z5, p_one_sided=P5, LRT_crit_boundary_mixture=float(LRT_CRIT)), sources_sha16={}, cases=[])
    # ---- sigma_meas de referencia lidos do catalogo
    cat = json.load(open(os.path.join(BENCH, 'C4_CATALOG_220.json')))
    comb = json.load(open(os.path.join(BENCH, 'C4_CATALOG_COMBINATION.json')))
    out['sources_sha16']['C4_CATALOG_220.json'] = sha16(os.path.join(BENCH, 'C4_CATALOG_220.json'))
    out['sources_sha16']['C4_CATALOG_COMBINATION.json'] = sha16(os.path.join(BENCH, 'C4_CATALOG_COMBINATION.json'))
    sel = set(comb['selected_events'])
    sig = {r['event']: sigma_from_q(r['quantiles']['df220'][0], r['quantiles']['df220'][2]) for r in cat['rows']}
    sig_sel = np.array([sig[e] for e in sorted(sel)])
    s_gw250114 = sig['GW250114_082203']
    s_median31 = float(np.median(sig_sel))
    out['sigma_meas_reference'] = dict(GW250114_pSEOB=s_gw250114, median_31_GWTC5=s_median31,
                                       min_31=float(sig_sel.min()), max_31=float(sig_sel.max()),
                                       sorted_31=sorted(float(v) for v in sig_sel))
    print('sigma_meas GW250114 = %.4f ; mediana dos 31 = %.4f' % (s_gw250114, s_median31))
    # ---- grade: sigma_meas x sigma_jit -> N (score fechado) e N por MC (poder 50% e 90%)
    grid_meas = [('GW250114-like', s_gw250114), ('GWTC5-median-like', s_median31),
                 ('sigma 0.005', 0.005), ('sigma 0.010', 0.010), ('sigma 0.020', 0.020), ('sigma 0.030', 0.030), ('sigma 0.050', 0.050)]
    for label, sm in grid_meas:
        for sj in (0.010, 0.019, 0.030):
            n_score = n_for_5sigma_score(sm, sj)
            row = dict(sigma_meas_label=label, sigma_meas=sm, sigma_jit=sj, N_score_closed_form=n_score)
            if n_score <= 20000:
                n50 = n_for_power(sm, sj, 0.5, rng)
                n90 = n_for_power(sm, sj, 0.9, rng) if (n50 is not None and n50 <= 5000) else None
                row.update(N_LRT_power50=n50, N_LRT_power90=n90)
            else:
                row.update(N_LRT_power50=None, N_LRT_power90=None, note='N > 20000: nao simulado')
            out['cases'].append(row)
            print(label, 'sj=%.3f' % sj, 'N_score=%.1f' % n_score, 'N50=%s N90=%s' % (row.get('N_LRT_power50'), row.get('N_LRT_power90')), flush=True)
    # ---- o catalogo real como esta: z esperado se sigma_jit fosse 0.019 com ESTES sigma_i (31 selecionados)
    s_i2 = sig_sel ** 2
    for sj in (0.010, 0.019, 0.030):
        ez = sj ** 2 * math.sqrt(np.sum(1 / s_i2 ** 2) / 2)
        out.setdefault('expected_z_with_current_31_sigmas', {})[str(sj)] = ez
    # quantos eventos "GW250114-like" equivalem ao catalogo inteiro (peso 1/sigma^4)
    out['catalog_31_weight_in_GW250114_units'] = float(np.sum(1 / s_i2 ** 2) / (1 / s_gw250114 ** 4))
    # ---- ganho relativo do canal df vs dtau (mesmo jitter browniano, GW250114)
    r250 = [r for r in cat['rows'] if r['event'] == 'GW250114_082203'][0]
    s_dtau = sigma_from_q(r250['quantiles']['dtau220'][0], r250['quantiles']['dtau220'][2])
    out['channel_comparison_GW250114'] = dict(sigma_df=s_gw250114, sigma_dtau=s_dtau,
        ratio_z_per_event_df_over_dtau_for_jit_0p019_df_0p022_dtau=float((0.019 / s_gw250114) ** 2 / (0.022 / s_dtau) ** 2))
    json.dump(out, open(os.path.join(HERE, 'd2_resultado.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('OK')

if __name__ == '__main__':
    main()
