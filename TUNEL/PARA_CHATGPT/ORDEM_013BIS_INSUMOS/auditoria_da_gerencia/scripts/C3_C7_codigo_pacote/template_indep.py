import sys, json, math
sys.path.insert(0, r'C:/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/ordem013/auditoria/C3_C7_codigo_pacote/mod')
import numpy as np
from scipy.optimize import least_squares
from tgl_ringdown_template import ringdown
from tgl_ringdown_prediction import prediction
M, a, z = 68.28733524825364, 0.6784704444609746, 0.0842531803391908
t = np.arange(0, 0.06, 1/16384)
out = {}
for rd in ('R-B', 'R-LIN', 'R-RAIZ-0'):
    p = prediction(M, a, rd, redshift=z)
    h = ringdown(t, M, a, rd, 1.0, phase=0.4, inclination=0.0, redshift=z)
    y = h['plus'] - 1j*h['cross']
    def res(v):
        f, tau, A, ph = v
        m = A*np.exp(-t/tau)*np.exp(-1j*(2*np.pi*f*t+ph))
        r = y - m
        return np.r_[r.real, r.imag]
    s = least_squares(res, [p['f_gr_hz']*1.01, p['tau_gr_s']*0.9, 1.0, 0.3], xtol=1e-15, ftol=1e-15, gtol=1e-15)
    f, tau = s.x[0], s.x[1]
    out[rd] = dict(dtau_fit=tau/p['tau_gr_s']-1, dtau_pred=p['delta_tau'], df_fit=f/p['f_gr_hz']-1)
    # media de realizacoes brownianas (so leituras quadraticas)
    if rd == 'R-B':
        acc = np.zeros_like(y)
        for sd in range(400):
            hr = ringdown(t, M, a, rd, 1.0, phase=0.4, observable='brownian_phase', seed=sd, redshift=z)
            acc += hr['plus'] - 1j*hr['cross']
        acc /= 400
        env_ratio = np.abs(acc[::200])/np.abs(y[::200])
        out[rd]['mean_realization_over_ensemble_envelope_maxdev'] = float(np.max(np.abs(env_ratio-1)))
print(json.dumps(out, indent=1))
