# Uma realizacao x media de ensemble: o dephasing de Milburn num estado coerente macroscopico = difusao de fase
# (<e^{i phi}> = e^{-Gamma t}, <phi^2> = 2 Gamma t). Ajuste de seno amortecido (A, phi0, f, tau) por minimos quadrados,
# sem ruido de detector, janela [0, 6 tau]. Pergunta: o que o ajuste de UMA realizacao devolve para dtau e df?
import math, json, sys
import numpy as np
from scipy.optimize import least_squares
sys.stdout.reconfigure(encoding='utf-8')
ALPHA_CODATA_2018 = 7.2973525693e-3
BETA = ALPHA_CODATA_2018 * math.sqrt(math.e)
Q = 3.2051; w = 1.0; tau = 2 * Q / w          # unidades de 1/omega
x = BETA * 0.52398 * 3.2141                     # ramo B, a = 0.68 (Leaver): x = Gamma*tau
Gam = x / tau
t = np.linspace(0, 6 * tau, 3000); dt = t[1] - t[0]
rng = np.random.default_rng(1)
def model(p):
    A, ph, f, ta = p; return A * np.exp(-t / ta) * np.cos(f * t + ph)
out = {'x': x, 'pred_ensemble_dtau': -x / (1 + x)}
for label, D in (('ensemble_mean_<h>', None), ('single_realization', 2 * Gam)):
    dts, dfs = [], []
    nrep = 1 if D is None else 1500
    for r in range(nrep):
        if D is None:
            h = np.exp(-t / tau - Gam * t) * np.cos(w * t)
        else:
            phi = np.concatenate([[0.0], np.cumsum(rng.normal(0, math.sqrt(D * dt), len(t) - 1))])
            h = np.exp(-t / tau) * np.cos(w * t + phi)
        res = least_squares(lambda p: model(p) - h, [1.0, 0.0, w, tau], xtol=1e-12, ftol=1e-12)
        dts.append(res.x[3] / tau - 1); dfs.append(res.x[2] / w - 1)
    dts = np.array(dts); dfs = np.array(dfs)
    out[label] = dict(mean_dtau=float(dts.mean()), sd_dtau=float(dts.std()), mean_df=float(dfs.mean()), sd_df=float(dfs.std()))
    print(label, out[label])
print('ordem de grandeza sqrt(2x)/(2Q) =', math.sqrt(2 * x) / (2 * Q))
json.dump(out, open('fase_difusa_result.json', 'w'), indent=1)
