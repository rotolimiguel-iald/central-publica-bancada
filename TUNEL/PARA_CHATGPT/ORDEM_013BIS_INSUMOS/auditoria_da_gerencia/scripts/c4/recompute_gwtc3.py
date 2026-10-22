import numpy as np, math, json, glob
from scipy.stats import gaussian_kde
ALPHA = 7.2973525693e-3; BETA = ALPHA*math.sqrt(math.e)
def bcw(a): return 1.5251 - 1.1568*(1-a)**0.1292, 0.7000 + 1.4187*(1-a)**(-0.4990)
def shift(a, rd):
    wr, Q = bcw(a); x = {'R-B': BETA*wr*Q, 'R-RAIZ-0': BETA*Q, 'R-LIN': 2*BETA*Q}[rd]; return -x/(1+x)
sel = ['S150914','S170104','S190519bj','S190521r','S190630ag','S190828j','S190910s','S200129m','S200224ca','S200311bg']
gf = np.linspace(-0.12, 0.15, 136); gt = np.linspace(-0.3, 0.6, 181)
GF, GT = np.meshgrid(gf, gt, indexing='ij'); P = np.vstack([GF.ravel(), GT.ravel()])
ls = np.zeros(P.shape[1]); lgr = 0.; sums = {'R-B': 0., 'R-RAIZ-0': 0., 'R-LIN': 0.}; rows = []
for ev in sel:
    d = np.load('g3_rin_%s_pseobnrv4hm.npz' % ev); df, dt, chi = d['domega220'], d['dtau220'], d['chi']
    k = gaussian_kde(np.vstack([df, dt])); b0 = k.logpdf([[0.], [0.]])[0]; r = {'ev': ev, 'N': len(df), 'chi_min': float(chi.min())}
    for rd in sums:
        s = np.array([shift(min(max(a, 0.0), 0.999), rd) for a in chi])
        r[rd] = float(gaussian_kde(np.vstack([df, dt - s])).logpdf([[0.], [0.]])[0] - b0); sums[rd] += r[rd]
    ls += k.logpdf(P); lgr += b0; rows.append(r); print(r, flush=True)
L = ls - ls.max(); p = np.exp(L); p /= p.sum(); ref = np.exp(lgr - ls.max())
print('sums', sums, 'GR_HPD_grid', float(p[np.exp(L) > ref].sum()), 'edge', float(p.reshape(GF.shape)[[0,-1],:].sum()+p.reshape(GF.shape)[:,[0,-1]].sum()))
json.dump({'rows': rows, 'sums': sums, 'GR_HPD_grid': float(p[np.exp(L) > ref].sum())}, open('recompute_gwtc3_result.json', 'w'), indent=1)
