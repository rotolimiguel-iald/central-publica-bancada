# Auditor C4: independent recomputation of GWTC-5.0 pSEOB catalogue sums and common-deformation GR HPD content
import numpy as np, math, json, glob, os, time
from scipy.stats import gaussian_kde
ALPHA = 7.2973525693e-3; BETA = ALPHA*math.sqrt(math.e)
def bcw(a):
    return 1.5251 - 1.1568*(1-a)**0.1292, 0.7000 + 1.4187*(1-a)**(-0.4990)
def shift(a, reading):
    wr, Q = bcw(a)
    x = {'R-B': BETA*wr*Q, 'R-RAIZ-0': BETA*Q, 'R-LIN': 2*BETA*Q}[reading]
    return -x/(1+x)
controls = {'GW191109_010717', 'GW200208_130117'}
files = sorted(glob.glob('post_G5_*.npz'))
events = []
for f in files:
    ev = f.split('post_G5_')[1].split('__')[0]
    d = np.load(f); events.append((ev, d['domega220'], d['dtau220'], d['final_spin_non_evolved']))
print(len(events))
rows = []
t0 = time.time()
# grid for common deformation
gf = np.linspace(-0.05, 0.08, 131); gt = np.linspace(-0.10, 0.28, 191)
GF, GT = np.meshgrid(gf, gt, indexing='ij'); P = np.vstack([GF.ravel(), GT.ravel()])
logsum31 = np.zeros(P.shape[1]); logsum33 = np.zeros(P.shape[1]); lgr31 = 0.0; lgr33 = 0.0
for ev, df, dt, chi in events:
    X = np.vstack([df, dt]); k = gaussian_kde(X)
    base0 = k.logpdf([[0.], [0.]])[0]
    r = {'event': ev, 'N': len(df), 'dtau_q05_50_95': np.quantile(dt, [.05, .5, .95]).tolist(),
         'df_q05_50_95': np.quantile(df, [.05, .5, .95]).tolist(), 'chi_med': float(np.median(chi)),
         'min_chi': float(chi.min())}
    for rd in ['R-B', 'R-RAIZ-0', 'R-LIN']:
        s = np.array([shift(a, rd) for a in chi])
        alt = gaussian_kde(np.vstack([df, dt - s]))
        r[rd] = float(alt.logpdf([[0.], [0.]])[0] - base0)
    lp = k.logpdf(P)
    logsum33 += lp; lgr33 += base0
    if ev not in controls: logsum31 += lp; lgr31 += base0
    rows.append(r); print(ev, round(r['R-B'], 4), round(r['R-LIN'], 4), round(time.time()-t0, 1), flush=True)
def hpd(logsum, lgr):
    L = logsum - logsum.max(); p = np.exp(L); p /= p.sum()
    ref = np.exp(lgr - logsum.max())
    content = float(p[np.exp(L) > ref].sum())
    i = np.argmax(logsum); 
    # marginal quantiles
    p2 = p.reshape(GF.shape); mf = p2.sum(1); mt = p2.sum(0)
    q = lambda g, m, qq: float(np.interp(qq, np.cumsum(m)/m.sum(), g))
    return dict(GR_HPD_content=content, lnratio_GR_vs_peak=float(lgr - logsum.max()),
                df_q05_50_95=[q(gf, mf, x) for x in (.05, .5, .95)], dtau_q05_50_95=[q(gt, mt, x) for x in (.05, .5, .95)],
                mass_on_grid_edge=float(p2[0, :].sum()+p2[-1, :].sum()+p2[:, 0].sum()+p2[:, -1].sum()))
res = {'rows': rows,
       'sum31': {rd: float(sum(r[rd] for r in rows if r['event'] not in controls)) for rd in ['R-B', 'R-RAIZ-0', 'R-LIN']},
       'sum33': {rd: float(sum(r[rd] for r in rows)) for rd in ['R-B', 'R-RAIZ-0', 'R-LIN']},
       'common31': hpd(logsum31, lgr31), 'common33': hpd(logsum33, lgr33)}
json.dump(res, open('recompute_catalog_result.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'rows'}, indent=1))
