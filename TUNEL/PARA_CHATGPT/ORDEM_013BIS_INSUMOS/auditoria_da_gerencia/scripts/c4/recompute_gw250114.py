# Auditor C4: independent recomputation of ln B (R-B, R-RAIZ-0, R-LIN) for GW250114 pSEOBNR posterior
import numpy as np, math, json, hashlib
from scipy.stats import gaussian_kde
from scipy.special import logsumexp
ALPHA = 7.2973525693e-3           # CODATA 2018
BETA = ALPHA*math.sqrt(math.e)    # runtime, never literal
def bcw(a):
    wr = 1.5251 - 1.1568*(1-a)**0.1292
    Q = 0.7000 + 1.4187*(1-a)**(-0.4990)
    return wr, Q
def x_reading(a, reading):
    wr, Q = bcw(a)
    if reading == 'R-B':      return BETA*wr*Q            # 1/2 beta (GM/c^3) w^2 tau
    if reading == 'R-RAIZ-0': return BETA*Q               # Gamma = beta w/2
    if reading == 'R-LIN':    return 2*BETA*Q             # Gamma = beta w
    raise ValueError
d = np.load('post_GW250114_17018009__pSEOBNRv5PHM.npz')
df, dt, chi = d['domega220'], d['dtau220'], d['final_spin_non_evolved']
N = len(df)
out = {'N': N, 'beta_runtime': BETA,
       'quantiles_05_50_95': {k: np.quantile(v, [.05, .5, .95]).tolist() for k, v in [('df', df), ('dtau', dt), ('chi', chi)]},
       'sd_dtau': float(np.std(dt, ddof=1)), 'sd_df': float(np.std(df, ddof=1)),
       'corr_df_dtau': float(np.corrcoef(df, dt)[0, 1])}
rng = np.random.default_rng(20260922)
def lnB_shear(dfv, dtv, s, bw='scott'):
    base = gaussian_kde(np.vstack([dfv, dtv]), bw_method=bw)
    alt = gaussian_kde(np.vstack([dfv, dtv - s]), bw_method=bw)
    return float(alt.logpdf([[0.], [0.]])[0] - base.logpdf([[0.], [0.]])[0])
def lnB_marg(dtv, s, bw='scott'):
    return float(gaussian_kde(dtv - s, bw_method=bw).logpdf([0.])[0] - gaussian_kde(dtv, bw_method=bw).logpdf([0.])[0])
def lnB_gauss2(dfv, dtv, s):
    X = np.vstack([dfv, dtv]); mu = X.mean(1); C = np.cov(X); Ci = np.linalg.inv(C)
    def q(p): v = mu - p; return float(v @ Ci @ v)
    return -0.5*(q(np.array([0., np.median(s)])) - q(np.array([0., 0.])))
def lnB_3d(dfv, dtv, chv, reading, ngrid=81):
    k = gaussian_kde(np.vstack([dfv, dtv, chv]))
    cg = np.linspace(np.quantile(chv, 0.0005), np.quantile(chv, 0.9995), ngrid)
    g = np.array([-x_reading(c, reading)/(1+x_reading(c, reading)) for c in cg])
    num = k.logpdf(np.vstack([np.zeros_like(cg), g, cg])); den = k.logpdf(np.vstack([np.zeros_like(cg), np.zeros_like(cg), cg]))
    # trapezoid in log space
    w = np.gradient(cg)
    return float(logsumexp(num, b=w) - logsumexp(den, b=w))
def mean_conditional_ratio(dfv, dtv, chv, reading):
    # the ORDER's literal statistic: mean over posterior spin of p(0,g|chi)/p(0,0|chi) (3D KDE / 1D KDE); NOT a Bayes factor
    k3 = gaussian_kde(np.vstack([dfv, dtv, chv])); 
    sub = rng.choice(len(chv), 3000, replace=False)
    c = chv[sub]; g = -np.array([x_reading(a, reading)/(1+x_reading(a, reading)) for a in c])
    r = np.exp(k3.logpdf(np.vstack([np.zeros_like(c), g, c])) - k3.logpdf(np.vstack([np.zeros_like(c), np.zeros_like(c), c])))
    return float(np.log(np.mean(r)))
# GR HPD content: fraction of samples whose KDE density exceeds density at GR point (held-out style: half fit, half eval)
perm = rng.permutation(N); A, Bh = perm[:N//2], perm[N//2:]
kA = gaussian_kde(np.vstack([df[A], dt[A]]))
dens_eval = kA.logpdf(np.vstack([df[Bh], dt[Bh]])); dens_gr = kA.logpdf([[0.], [0.]])[0]
out['GR_HPD_content_heldout'] = float(np.mean(dens_eval > dens_gr))
rows = []
for reading in ['R-B', 'R-RAIZ-0', 'R-LIN']:
    x = np.array([x_reading(a, reading) for a in chi]); s = -x/(1+x)
    r = {'reading': reading, 'shift_q05_50_95': np.quantile(s, [.05, .5, .95]).tolist(),
         'shift_linear_median': float(-np.median(x))}
    r['lnB_shear2d_scott'] = lnB_shear(df, dt, s)
    r['lnB_shear2d_silverman'] = lnB_shear(df, dt, s, 'silverman')
    r['lnB_shear2d_bw0.7'] = lnB_shear(df, dt, s, gaussian_kde(np.vstack([df, dt])).scotts_factor()*0.7)
    r['lnB_shear2d_bw1.4'] = lnB_shear(df, dt, s, gaussian_kde(np.vstack([df, dt])).scotts_factor()*1.4)
    r['lnB_fixed_median_shift'] = lnB_shear(df, dt, np.full(N, np.median(s)))
    r['lnB_marginal_dtau'] = lnB_marg(dt, s)
    r['lnB_gauss2d'] = lnB_gauss2(df, dt, s)
    r['lnB_gauss1d_dtau'] = float(-0.5*(((dt.mean()-np.median(s))/dt.std(ddof=1))**2 - (dt.mean()/dt.std(ddof=1))**2))
    r['lnB_3dKDE_curve_integral'] = lnB_3d(df, dt, chi, reading)
    r['ln_mean_conditional_ratio_ORDER_literal'] = mean_conditional_ratio(df, dt, chi, reading)
    r['z_reading'] = float((np.median(dt) - np.median(s))/np.std(dt, ddof=1))
    r['z_GR'] = float(np.median(dt)/np.std(dt, ddof=1))
    r['correction_over_sigma'] = float(abs(np.median(s))/np.std(dt, ddof=1))
    boots = []
    for _ in range(200):
        i = rng.integers(0, N, N)
        boots.append(lnB_shear(df[i], dt[i], s[i]))
    r['lnB_bootstrap_025_50_975'] = np.quantile(boots, [.025, .5, .975]).tolist()
    rows.append(r); print(json.dumps(r), flush=True)
out['rows'] = rows
json.dump(out, open('recompute_gw250114_result.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'rows'}, indent=1))
