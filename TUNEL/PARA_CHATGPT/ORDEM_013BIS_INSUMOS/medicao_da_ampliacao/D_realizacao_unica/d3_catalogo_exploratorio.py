# -*- coding: utf-8 -*-
"""FRENTE D (3): NAO-CEGO, EXPLORATORIO. O espalhamento observado das medianas de df220 entre eventos
e compativel com sigma_meas apenas? Variancia observada das medianas vs media dos sigma_i^2; score z;
MLE hierarquico gaussiano (mu, sigma_jit) com intervalo de perfil; LRT na fronteira.
Fontes: C4_CATALOG_220.json (GWTC-5.0, pSEOB, 33 = 31 + 2 controles), C4_GWTC3_220.json (18; 10 publicados).
Aproximacao gaussiana por quantis 05/95 [INPUT]; posteriores reais sao assimetricos e limitados pelo prior.
"""
import os, sys, json, math, hashlib
import numpy as np
from scipy.stats import chi2, norm
from scipy.optimize import minimize_scalar

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = r'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN'
Q90 = 1.6448536269514722

def sha16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]

def loglik(y, v, mu, s2):
    vv = v + s2
    return float(-0.5 * np.sum((y - mu) ** 2 / vv + np.log(vv)))

def pmu(y, v, s2):
    w = 1 / (v + s2)
    return float(np.sum(w * y) / np.sum(w))

def analyse(label, events, y, s, extra=None):
    y = np.asarray(y); s = np.asarray(s); v = s ** 2; N = len(y)
    mu0 = pmu(y, v, 0.)
    obs_var_medians = float(np.var(y, ddof=1))
    mean_s2 = float(np.mean(v))
    # score
    U = 0.5 * np.sum(((y - mu0) ** 2 - v) / v ** 2); I = 0.5 * np.sum(1 / v ** 2)
    z_score = float(U / math.sqrt(I))
    # chi2 de homogeneidade (mu ponderado)
    chi = float(np.sum((y - mu0) ** 2 / v)); dof = N - 1
    # MLE de s2 com perfil
    f = lambda s2: -loglik(y, v, pmu(y, v, s2), s2)
    r = minimize_scalar(f, bounds=(0., 25.), method='bounded', options=dict(xatol=1e-12))
    l0 = loglik(y, v, mu0, 0.); l1 = max(-r.fun, l0); s2_hat = r.x if -r.fun > l0 else 0.
    lrt = 2 * (l1 - l0)
    p_lrt = 0.5 * chi2.sf(lrt, 1) if lrt > 0 else 1.0
    # intervalo de perfil 90% para sigma_jit (LRT <= chi2_1(0.90)=2.706 -> limites)
    grid = np.linspace(0., 0.6, 6001)
    prof = np.array([loglik(y, v, pmu(y, v, g ** 2), g ** 2) for g in grid])
    ok = grid[prof >= l1 - 0.5 * 2.7055]
    ci90 = [float(ok.min()), float(ok.max())] if len(ok) else None
    # limite superior 95% unilateral (LRT <= 2.706 unilateral -> prof >= l1 - 1.353)
    ok95 = grid[prof >= l1 - 0.5 * 2.7055]
    ub95 = float(ok95.max()) if len(ok95) else None
    res = dict(label=label, N=N, events=list(events), medians=y.tolist(), sigma_i=s.tolist(),
               mu_weighted_H0=mu0, observed_variance_of_medians=obs_var_medians, mean_sigma_i2=mean_s2,
               ratio_obsvar_over_mean_sigma2=obs_var_medians / mean_s2,
               chi2_homogeneity=chi, dof=dof, p_chi2=float(chi2.sf(chi, dof)),
               score_z=z_score, sigma_jit_MLE=float(math.sqrt(s2_hat)), LRT=float(lrt), p_LRT_boundary=float(p_lrt),
               sigma_jit_profile_90=ci90, sigma_jit_upper_95_one_sided=ub95,
               mu_at_MLE=pmu(y, v, s2_hat))
    if extra: res.update(extra)
    print('== %s: N=%d | var(medianas)=%.5f  <sigma^2>=%.5f  razao=%.2f | chi2/dof=%.1f/%d p=%.3f | score z=%.2f | sigma_jit MLE=%.4f  90%%=%s  LRT=%.2f p=%.3g' % (
        label, N, obs_var_medians, mean_s2, obs_var_medians / mean_s2, chi, dof, res['p_chi2'], z_score, res['sigma_jit_MLE'], ci90, lrt, p_lrt))
    return res

def main():
    out = dict(status='EXPLORATORY_NONBLIND_GAUSSIAN_APPROX', sources_sha16={}, analyses=[])
    for f in ('C4_CATALOG_220.json', 'C4_CATALOG_COMBINATION.json', 'C4_GWTC3_220.json', 'C4_GWTC3_PUBLISHED_COMBINATION.json'):
        out['sources_sha16'][f] = sha16(os.path.join(BENCH, f))
    cat = json.load(open(os.path.join(BENCH, 'C4_CATALOG_220.json')))
    sel = json.load(open(os.path.join(BENCH, 'C4_CATALOG_COMBINATION.json')))['selected_events']
    rows = {r['event']: r for r in cat['rows']}
    def sig(q): return (q[2] - q[0]) / (2 * Q90)
    # (a) 31 selecionados, df220
    ev = [e for e in sel]
    y = [rows[e]['quantiles']['df220'][1] for e in ev]; s = [sig(rows[e]['quantiles']['df220']) for e in ev]
    out['analyses'].append(analyse('GWTC5_31_df220', ev, y, s))
    # (b) 31 sem GW250114 (o evento mais preciso domina)
    ev2 = [e for e in ev if e != 'GW250114_082203']
    y2 = [rows[e]['quantiles']['df220'][1] for e in ev2]; s2 = [sig(rows[e]['quantiles']['df220']) for e in ev2]
    out['analyses'].append(analyse('GWTC5_30_df220_sem_GW250114', ev2, y2, s2))
    # (c) os 10 mais precisos (sigma_df < mediana) -- onde o jitter de 2% teria peso
    order = sorted(ev, key=lambda e: sig(rows[e]['quantiles']['df220']))
    ev3 = order[:10]
    out['analyses'].append(analyse('GWTC5_10_mais_precisos_df220', ev3, [rows[e]['quantiles']['df220'][1] for e in ev3], [sig(rows[e]['quantiles']['df220']) for e in ev3]))
    # (d) dtau220 nos 31, para comparacao de canal
    out['analyses'].append(analyse('GWTC5_31_dtau220', ev, [rows[e]['quantiles']['dtau220'][1] for e in ev], [sig(rows[e]['quantiles']['dtau220']) for e in ev]))
    # (e) 33 com controles (GW191109, GW200208: df mediano 1.06 e 0.17 -> fora do prior util; so para registro)
    ev5 = [r['event'] for r in cat['rows']]
    out['analyses'].append(analyse('GWTC5_33_com_controles_df220', ev5, [rows[e]['quantiles']['df220'][1] for e in ev5], [sig(rows[e]['quantiles']['df220']) for e in ev5]))
    # (f) GWTC-3: 10 publicados e 18 do arquivo
    g3 = json.load(open(os.path.join(BENCH, 'C4_GWTC3_220.json')))
    pub = json.load(open(os.path.join(BENCH, 'C4_GWTC3_PUBLISHED_COMBINATION.json')))['selected_events']
    r3 = {r['event']: r for r in g3['rows']}
    out['analyses'].append(analyse('GWTC3_10_publicados_df220', pub, [r3[e]['quantiles']['df220'][1] for e in pub], [sig(r3[e]['quantiles']['df220']) for e in pub]))
    ev18 = list(r3.keys())
    out['analyses'].append(analyse('GWTC3_18_arquivo_df220', ev18, [r3[e]['quantiles']['df220'][1] for e in ev18], [sig(r3[e]['quantiles']['df220']) for e in ev18]))
    # (g) sensibilidade a assimetria: usar metade-larguras separadas (q50-q05, q95-q50) -> sigma = min/max
    for name, pick in (('sigma_min_halfwidth', min), ('sigma_max_halfwidth', max)):
        s_alt = [pick(rows[e]['quantiles']['df220'][1] - rows[e]['quantiles']['df220'][0], rows[e]['quantiles']['df220'][2] - rows[e]['quantiles']['df220'][1]) / Q90 for e in ev]
        out['analyses'].append(analyse('GWTC5_31_df220_' + name, ev, y, s_alt))
    # (h) Monte Carlo do nulo com estes 31 sigma_i: distribuicao do score z e do LRT sob H0 (calibracao do teste rapido)
    rng = np.random.default_rng(1)
    v = np.array(s) ** 2; zs = []; lr = []
    for k in range(4000):
        yy = rng.normal(0., np.sqrt(v))
        mu0 = pmu(yy, v, 0.)
        U = 0.5 * np.sum(((yy - mu0) ** 2 - v) / v ** 2); I = 0.5 * np.sum(1 / v ** 2); zs.append(U / math.sqrt(I))
    zs = np.array(zs)
    out['null_calibration_31'] = dict(score_z_mean=float(zs.mean()), score_z_sd=float(zs.std()), score_z_q95=float(np.quantile(zs, .95)),
                                      score_z_q99=float(np.quantile(zs, .99)), n_mc=4000,
                                      note='mu estimado: z do score sob H0 tem media ~-1/sqrt(2I)*... e cauda; usar p por MC, nao gaussiana')
    zobs = out['analyses'][0]['score_z']
    out['null_calibration_31']['p_MC_of_observed_z_31'] = float(np.mean(zs >= zobs))
    json.dump(out, open(os.path.join(HERE, 'd3_resultado.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('OK')

if __name__ == '__main__':
    main()
