"""Independent re-run of one E2 null cell (GWTC5_31_R_B_T5M_GN) and of the route-IV null (exact + MC).

Own implementation of the projection algebra (not importing the bancada's code), different seed.
Reads only DATASET.json and NUISANCE_V1.json (pinned inputs of the registry).
"""
import json, math, time
import numpy as np
from scipy.stats import norm, chi2, beta
from scipy.integrate import quad
from pathlib import Path
BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN")
ds = json.loads((BASE / 'bis/e0_core/DATASET.json').read_bytes())
nu = json.loads((BASE / 'NUISANCE_V1.json').read_bytes())
reg = json.loads((BASE / 'RINGDOWN_5SIGMA_V1.json').read_text(encoding='utf-8-sig'))
cell = reg['nulls']['cells']['GWTC5_31_R_B_T5M_GN']
lookup = {r['product_id']: r for r in ds['rows']}
rows = [lookup[k] for k in ds['sets'][cell['population']]]
N = cell['N_target_balanced_catalog']; idx = np.arange(N) % len(rows)
delta = np.array([r['predictions'][cell['reading']]['delta_tau'] for r in rows])[idx]
sigma = np.array([r['stats']['dtau']['std_ddof1'] for r in rows])[idx]
X = np.column_stack((np.ones(N), sigma)); V = np.array(nu['synthetic_E2_nuisance_INPUT']['sigma_model']['covariance'])
# Own derivation: y = delta*a + X c + e, e~N(0,diag(sigma^2)), c~N(m,V). Marginal covariance C = D + X V X^T.
# matched-filter z = delta^T C^-1 (y - X m) / sqrt(delta^T C^-1 delta). Under null (a=0): z ~ N(0,1) if Gaussian.
C = np.diag(sigma ** 2) + X @ V @ X.T
Ci_delta = np.linalg.solve(C, delta); info = float(delta @ Ci_delta); w = Ci_delta / math.sqrt(info)
noise_frac = float(np.sum((w * sigma) ** 2)); nuis_frac = float((X.T @ w) @ V @ (X.T @ w))
out = {'cell': 'GWTC5_31_R_B_T5M_GN', 'N': N, 'information_with_nuisance': info,
       'noise_variance_fraction': noise_frac, 'nuisance_variance_fraction': nuis_frac, 'sum': noise_frac + nuis_frac,
       'bancada': {'noise': 0.3312342541930797, 'nuisance': 0.6687657458072589, 'info': 0.7373675032816482,
                   'p_emp': 7.727e-05, 'p_analytic': 7.751183655491336e-05}}
# analytic tail: conditional on U ~ chi2_5, z ~ N(0, 3a/U + b)
a, b = noise_frac, nuis_frac
p_an, err = quad(lambda u: norm.sf(5 / math.sqrt(3 * a / u + b)) * chi2.pdf(u, 5), 0, np.inf, epsabs=1e-13, epsrel=1e-9, limit=300)
out['p_analytic_own'] = p_an
# MC with own seed, 1e8 draws in chunks
rng = np.random.default_rng(20260923); draws = 100_000_000; chunk = 5_000_000; k = 0; used = 0; t0 = time.time()
while used < draws:
    n = min(chunk, draws - used)
    e = rng.standard_normal(n) * np.sqrt(3 / rng.chisquare(5, n))
    z = math.sqrt(a) * e + math.sqrt(b) * rng.standard_normal(n)
    k += int(np.sum(z > 5)); used += n
out['mc'] = {'draws': used, 'exceed': k, 'p_emp': k / used, 'UL95': float(beta.ppf(0.95, k + 1, used - k)),
             'CI95': [float(beta.ppf(0.025, k, used - k + 1)), float(beta.ppf(0.975, k + 1, used - k))], 'wall_s': time.time() - t0}
out['gaussian_reference_p5'] = float(norm.sf(5)); out['t5_inflation_factor'] = p_an / norm.sf(5)
# ROUTE IV exact null for homoscedastic population (GW250114_actual_width): all sigma_i equal -> LRT closed form.
# v = sigma^2 + q; MLE q_hat = max(0, S2 - sigma^2), S2 = (1/N) sum (y - ybar)^2; LRT = N[(S2/sigma^2) - 1 - ln(S2/sigma^2)] if S2>sigma^2.
# Under null N*S2/sigma^2 ~ chi2_{N-1}. Solve LRT(r)=25 for r = S2/sigma^2 > 1, then p = P(chi2_{N-1} > N r).
from scipy.optimize import brentq
iv = {}
for Nn in (22, 39, 61):
    g = lambda r: Nn * (r - 1 - math.log(r)) - 25.0
    r_star = brentq(g, 1 + 1e-9, 1e6)
    p_exact = float(chi2.sf(Nn * r_star, Nn - 1))
    # also asymptotic half-chi2_1
    iv[f'N={Nn}'] = {'r_star_S2_over_sigma2': r_star, 'p_exact_null_LRT_gt_25': p_exact,
                     'p_asymptotic_half_chi2_1': 0.5 * float(chi2.sf(25, 1)), 'draws_needed_for_10_exceedances': 10 / p_exact}
# quick MC check for N=22 with 1e7 draws (own code), sigma = GW250114 df width
prov = json.loads((BASE / 'bis/E0_ROUTE_IV_POWER_v2.json').read_bytes())
sig114 = [r['sigma_df'] for r in prov['per_event'] if r['event'] == 'GW250114_082203'][0]
rng = np.random.default_rng(7); Nn = 22; draws = 10_000_000; k = 0; mx = 0.0; t0 = time.time()
for _ in range(draws // 1_000_000):
    y = rng.standard_normal((1_000_000, Nn)) * sig114
    S2 = y.var(axis=1)  # ddof=0 -> (1/N) sum (y-ybar)^2
    r = S2 / sig114 ** 2; lrt = np.where(r > 1, Nn * (r - 1 - np.log(np.maximum(r, 1e-300))), 0.0)
    k += int(np.sum(lrt > 25)); mx = max(mx, float(lrt.max()))
iv['mc_N=22'] = {'sigma_df_GW250114': sig114, 'draws': draws, 'exceed': k, 'max_LRT': mx, 'UL95': float(beta.ppf(0.95, k + 1, draws - k)),
                 'bancada_1e6': {'exceed': 0, 'max_LRT': 18.43, 'UL95': 2.9957e-06}, 'wall_s': time.time() - t0}
out['route_IV'] = iv
print(json.dumps(out, indent=1))
