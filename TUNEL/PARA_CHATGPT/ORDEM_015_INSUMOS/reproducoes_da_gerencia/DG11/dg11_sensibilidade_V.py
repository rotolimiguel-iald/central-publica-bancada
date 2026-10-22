"""DG-11: sensibilidade da FPR sintetica (celulas E2) a escolha da covariancia V de c(sigma).
Somente leitura; reimplementa a projecao de synthetic_null.py (Woodbury) e a cauda analitica de null_runner.py.
"""
import json, math, hashlib
import numpy as np
from scipy.integrate import quad
from scipy.stats import norm, chi2

BASE = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
def sha(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest()

nu = json.load(open(BASE+r"\NUISANCE_V1.json"))
ds = json.load(open(BASE+r"\bis\e0_core\DATASET.json"))
reg = json.load(open(BASE+r"\RINGDOWN_5SIGMA_V1.json"))
print("NUISANCE_V1.json", sha(BASE+r"\NUISANCE_V1.json")[:16])
print("DATASET.json", sha(BASE+r"\bis\e0_core\DATASET.json")[:16])
print("RINGDOWN_5SIGMA_V1.json", sha(BASE+r"\RINGDOWN_5SIGMA_V1.json")[:16])

cd = nu['conditional_diagnostics']
# candidate V's per population
def V_kde(group, bw):
    for f in cd['fits']:
        if f['reading']=='GR' and f['group']==group and f['bandwidth_factor']==bw and f['covariate']=='sigma':
            return np.array(f['result']['covariance']), f['result']['stderr'][0]
    raise KeyError
def V_wls(group):
    m = cd['management_WLS_controls'][group]['median_q90_1.6449']
    return np.array(m['covariance']), m['stderr'][0]

def components(delta, sigma, X, V):
    W = 1/(sigma*sigma)
    ev,Q = np.linalg.eigh(V); L = Q@np.diag(np.sqrt(np.maximum(ev,0)))
    U = X@L; rhs = W*delta
    solved = rhs - W*(U@np.linalg.solve(np.eye(2)+U.T@(W[:,None]*U), U.T@rhs))
    I = float(delta@solved); w = solved/np.sqrt(I)
    a = float(np.sum((w*sigma)**2)); b = float((X.T@w)@V@(X.T@w))
    assert abs(a+b-1) < 1e-7
    return a, b, I

def tail_t5(a, b):
    v,_ = quad(lambda u: norm.sf(5/math.sqrt(3*a/u+b))*chi2.pdf(u,5), 0, np.inf, epsabs=1e-12, epsrel=1e-9, limit=200)
    return v

p5 = norm.sf(5)
lookup = {r['product_id']: r for r in ds['rows']}
out = {}
for cell_id, cell in reg['nulls']['cells'].items():
    if cell['kind'] != 'matched_projection' or cell['model'] == 'gaussian':
        continue
    pop = cell['population']; rd = cell['reading']; N = cell['N_target_balanced_catalog']
    rows = [lookup[k] for k in ds['sets'][pop]]
    idx = np.arange(N) % len(rows)
    delta = np.array([r['predictions'][rd]['delta_tau'] for r in rows])[idx]
    sigma = np.array([r['stats']['dtau']['std_ddof1'] for r in rows])[idx]
    X = np.column_stack((np.ones(N), sigma))
    # recorded result
    rec = json.load(open(BASE+r"\bis\RESULT_E2_NULL_"+cell_id+".json"))
    rec_p = rec['result']['analytic_tail_control']['p']; rec_a = rec['result']['components']['noise_variance_fraction']
    res = {}
    for label,(V,se) in {
        'kde_0.7': V_kde(pop,0.7), 'kde_1.0_registrado': V_kde(pop,1.0), 'kde_1.4': V_kde(pop,1.4), 'WLS_q90': V_wls(pop),
        'V_zero': (np.zeros((2,2)),0.0), 'V_x10': (10*V_kde(pop,1.0)[0], math.sqrt(10)*V_kde(pop,1.0)[1]),
    }.items():
        a,b,I = components(delta, sigma, X, V)
        p = tail_t5(a,b)
        res[label] = dict(SE_c0=se, a=a, b=b, I=I, p_t5=p, p_over_p5=p/p5)
    out[cell_id] = dict(N=N, recorded_a=rec_a, recorded_p=rec_p, variants=res)
    print(f"\n{cell_id} N={N} recorded a={rec_a:.4f} p={rec_p:.3e}")
    for k,v in res.items():
        print(f"  {k:20s} SE_c0={v['SE_c0']:.4f} a={v['a']:.4f} b={v['b']:.4f} I={v['I']:.3f} p_t5={v['p_t5']:.3e} (x{v['p_over_p5']:.1f} p5)")

# Gaussian: exact regardless of V (analytic); show I dependence for the gaussian cells (power)
print("\nGaussiano: FPR = Phi_bar(5) =", p5, "independente de V por construcao (Z padronizado com C = D + X V X^T).")
json.dump(out, open(r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\aud013bis\DG11\dg11_resultado.json",'w'), indent=1)
