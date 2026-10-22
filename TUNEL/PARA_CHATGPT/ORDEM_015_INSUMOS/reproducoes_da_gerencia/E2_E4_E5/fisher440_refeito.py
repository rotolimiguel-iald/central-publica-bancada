"""Independent Fisher of the fractional damping-time deformation of the 440 mode.

Reproduces the bancada's number (sigma(delta_tau_440) ~ 0.2001 at isolated rho_440 = 10,
profile FIXED_SOURCE_FREQUENCY; ~0.2007 with free frequency) from first principles:
damped sinusoid h(t) = A e^{-t/tau} cos(2 pi f t + phi), t >= 0, white noise, Fisher
Gamma_ij = (2/S) int dh_i dh_j dt, rho^2 = (2/S) int h^2 dt. Fractional tau: theta = ln tau.
QNM of the R-MOD reference row (GW250114-like remnant): f = 534.0018 Hz, tau = 3.94069 ms, Q = 6.611.
Also computed with a coloured PSD (aLIGO O4 design ASD from the pinned cache file) to show the PSD dependence at fixed rho.
"""
import json, math
import numpy as np
from pathlib import Path

f0 = 534.0017964533197; tau0 = 0.003940694361603494; Q = math.pi * f0 * tau0
delta_by_reading = {'R-B': -0.08216064025655216, 'R-MOD': -0.19599710827326722,
                    'R-RAIZ-0': -0.07367832435841462, 'R-LIN': -0.13724468993530575}

def fisher_white(free_f=True, rho=10.0, phi=0.3):
    dt = 1.0 / (64 * f0); T = 40 * tau0; t = np.arange(0, T, dt)
    A = 1.0
    env = np.exp(-t / tau0); c = np.cos(2 * np.pi * f0 * t + phi); s = np.sin(2 * np.pi * f0 * t + phi)
    h = A * env * c
    d = {'lnA': h, 'phi': -A * env * s, 'lntau': h * (t / tau0)}
    if free_f:
        d['lnf'] = -A * env * s * 2 * np.pi * f0 * t
    names = list(d)
    G = np.array([[np.sum(d[a] * d[b]) * dt for b in names] for a in names])
    norm = np.sum(h * h) * dt  # (2/S) factor cancels once we scale to rho
    G = G / norm * rho ** 2
    C = np.linalg.inv(G)
    return names, math.sqrt(C[names.index('lntau'), names.index('lntau')])

def fisher_coloured(asd_path, free_f=True, rho=10.0, phi=0.3):
    a = np.loadtxt(asd_path); fr, asd = a[:, 0], a[:, 1]
    dt = 1.0 / 8192; T = 2.0; n = int(T / dt); t = np.arange(n) * dt
    env = np.exp(-t / tau0); c = np.cos(2 * np.pi * f0 * t + phi); s = np.sin(2 * np.pi * f0 * t + phi)
    h = env * c
    d = {'lnA': h, 'phi': -env * s, 'lntau': h * (t / tau0)}
    if free_f:
        d['lnf'] = -env * s * 2 * np.pi * f0 * t
    ff = np.fft.rfftfreq(n, dt); S = np.interp(ff, fr, asd) ** 2
    mask = (ff >= 20) & (ff <= 2000)
    def inner(x, y):
        X = np.fft.rfft(x) * dt; Y = np.fft.rfft(y) * dt
        return 4 * np.sum((X[mask] * np.conj(Y[mask])).real / S[mask]) * (ff[1] - ff[0])
    names = list(d)
    G = np.array([[inner(d[a], d[b]) for b in names] for a in names]); norm = inner(h, h)
    G = G / norm * rho ** 2; C = np.linalg.inv(G)
    return names, math.sqrt(C[names.index('lntau'), names.index('lntau')])

out = {'f440_Hz': f0, 'tau440_s': tau0, 'Q440': Q}
for free_f in (False, True):
    names, sig = fisher_white(free_f)
    out[f'white_sigma_lntau_rho10_free_f={free_f}'] = {'params': names, 'sigma': sig}
psd_dir = Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\psd")
for name in ['aLIGO_O4_high_asd.txt', 'Aplus_asd.txt']:
    p = psd_dir / name
    if p.exists():
        try:
            for free_f in (False, True):
                names, sig = fisher_coloured(p, free_f)
                out[f'{name}_sigma_lntau_rho10_free_f={free_f}'] = sig
        except Exception as e:
            out[name] = 'ERR ' + repr(e)
# N for 5 sigma from sigma at rho=10 (bancada convention: N50 = (5/z)^2, N90 = N50*(6.28/5)^2)
sig = out['white_sigma_lntau_rho10_free_f=False']['sigma']
tab = {}
for r, dl in delta_by_reading.items():
    z = abs(dl) / sig; n50 = (5 / z) ** 2; n90 = n50 * ((5 + 1.2816) / 5) ** 2
    tab[r] = {'delta_tau440': dl, 'z_per_event_rho440=10': z, 'N50': n50, 'N90': n90}
out['N_for_5sigma_via_440_at_rho440=10_white'] = tab
out['bancada_reference'] = {'sigma_FIXED_SOURCE_FREQUENCY_O4_rho10': 0.20011479377458105,
                            'sigma_FREE_FREQUENCY_FIXED_TAU_GR_O4_rho10': 0.200744, 'N90_R-MOD': 41.13, 'N90_R-B': 235.55}
# what rho_440 does GW250114 actually give? the 440 is ~ (few %) of the 220 power; isolated rho_440 ~ few for O4.
print(json.dumps(out, indent=1))
