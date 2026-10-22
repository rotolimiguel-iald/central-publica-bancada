# -*- coding: utf-8 -*-
"""FRENTE D (1): o que o modelo de REALIZACAO UNICA preve, por evento, e de que depende.

Somente leitura da bancada; escreve apenas nesta pasta. beta em runtime (nunca literal).
Estatutos: a media de ensemble <a>(t) = <a>(0) e^{-i w t - Gamma t} e o UNICO objeto fixado
pela GKSL [DERIVED]; a estatistica de (df, dtau) ajustados numa realizacao depende do
desenrolamento escolhido [INPUT/CONJECTURE], do estimador, da janela e do ruido.
Estimador: o mesmo da bancada (projecao variavel, df em [-.5,.5], log(tau/tauGR) em [-2,2]).
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'; os.environ['OMP_NUM_THREADS'] = '1'
import sys, math, json, hashlib, time
import numpy as np
from scipy.optimize import least_squares

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = r'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN'
sys.path.insert(0, BENCH)  # importa (so leitura) os modulos da bancada
from tgl_ringdown_prediction import prediction, beta_tgl, kerr_mode  # noqa: E402

def sha16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]

SOURCES = {os.path.join(BENCH, f): sha16(os.path.join(BENCH, f)) for f in
           ('tgl_ringdown_prediction.py', 'tgl_ringdown_template.py', 'tgl_ringdown_unravelings.py',
            'trajectory_recovery.py', 'C2_TRAJECTORY_RECOVERY.json')}
BETA = beta_tgl()
assert abs(BETA - 7.2973525693e-3 * math.sqrt(math.e)) < 1e-18

FS = 4096.

def fit(t, y, omega, tau):
    """Projecao variavel identica em forma a trajectory_recovery.fit (ruido branco -> whitener = I)."""
    def residual(p):
        angle = omega * (1 + p[0]) * t
        env = np.exp(-t / (tau * np.exp(p[1])))
        basis = np.column_stack([env * np.cos(angle), env * np.sin(angle)])
        amp = np.linalg.lstsq(basis, y, rcond=None)[0]
        return y - basis @ amp
    best = None
    for start in (0., -.03, .03):
        r = least_squares(residual, [start, 0.], bounds=([-.5, -2.], [.5, 2.]),
                          ftol=1e-10, xtol=1e-10, gtol=1e-10, max_nfev=100)
        if best is None or r.cost < best.cost:
            best = r
    return float(best.x[0]), float(np.expm1(best.x[1]))

def phase_process(kind, gamma, t, rng, n):
    """Processos de fase com a MESMA media E e^{i phi_t} = e^{-Gamma t}; realizacoes diferentes."""
    dt = np.diff(np.r_[0., t])
    if kind == 'brownian':          # var 2 Gamma t
        return np.cumsum(rng.normal(size=(n, len(t))) * np.sqrt(2 * gamma * dt), axis=1)
    if kind == 'cauchy':            # escala Gamma t; sem variancia
        return np.cumsum(rng.standard_cauchy(size=(n, len(t))) * gamma * dt, axis=1)
    if kind.startswith('kick_'):    # saltos de Poisson de fase +-theta a taxa lam: lam(1-cos theta)=Gamma
        theta = float(kind.split('_')[1]) * math.pi
        lam = gamma / (1 - math.cos(theta))
        counts = rng.poisson(lam * dt, size=(n, len(t)))
        signs = rng.choice([-1., 1.], size=(n, len(t)))
        return np.cumsum(counts * theta * signs, axis=1)
    raise ValueError(kind)

def run_cell(mass, spin, reading, kind, n_rep, window_tau, snr, seed, use_exact_window_samples=None):
    p = prediction(mass, spin, reading)
    omega, tau, gamma = p['omega_rad_s'], p['tau_gr_s'], p['gamma_per_s']
    if use_exact_window_samples:
        t = np.arange(use_exact_window_samples) / FS
    else:
        t = np.arange(int(round(window_tau * tau * FS))) / FS
    rng = np.random.default_rng(seed)
    phase0 = 0.37
    carrier = np.exp(-t / tau) * np.exp(1j * (omega * t + phase0))
    if kind == 'ensemble_deterministic':
        factors = np.exp(-gamma * t)[None, :]
        n_rep_eff = 1 if snr is None else n_rep
        factors = np.repeat(factors, n_rep_eff, axis=0)
    else:
        n_rep_eff = n_rep
        factors = np.exp(1j * phase_process(kind, gamma, t, rng, n_rep))
    clean = (carrier[None, :] * factors).real
    if snr is not None:
        amp = snr / np.linalg.norm(carrier.real)     # ruido branco unitario -> SNR = ||h||
        y = amp * clean + rng.normal(size=clean.shape)
    else:
        y = clean
    dfs, dts = [], []
    for row in y:
        a, b = fit(t, row, omega, tau)
        dfs.append(a); dts.append(b)
    dfs, dts = np.array(dfs), np.array(dts)
    mad = lambda v: float(1.4826 * np.median(np.abs(v - np.median(v))))
    return dict(mass=mass, spin=spin, reading=reading, unraveling=kind, n_rep=n_rep_eff,
                window_tau=float(t[-1] / tau), n_samples=len(t), snr=snr,
                x=gamma * tau, Q=p['quality'], f_hz=p['f_gr_hz'], tau_ms=tau * 1e3,
                ensemble_dtau=-gamma * tau / (1 + gamma * tau),
                mean_df=float(dfs.mean()), sd_df=float(dfs.std(ddof=1)), mad_df=mad(dfs),
                q05_50_95_df=np.quantile(dfs, [.05, .5, .95]).tolist(),
                mean_dtau=float(dts.mean()), sd_dtau=float(dts.std(ddof=1)), mad_dtau=mad(dts),
                se_mean_dtau=float(dts.std(ddof=1) / math.sqrt(len(dts))),
                q05_50_95_dtau=np.quantile(dts, [.05, .5, .95]).tolist(),
                gerencia_envelope_sd_df=0.7 * math.sqrt(2 * gamma * tau) / (2 * p['quality']))

def main():
    t0 = time.time()
    out = dict(beta_runtime=BETA, sources_sha16=SOURCES, fs_hz=FS,
               estimator='variable projection; df in [-.5,.5], log(tau/tauGR) in [-2,2]; 3 starts; white noise',
               parts={})
    NREP = 600
    # ---- Parte A: o desenrolamento (mesma media de ensemble, realizacoes diferentes), referencia da C2
    A = []
    for reading, kinds in (('R-B', ['ensemble_deterministic', 'brownian', 'cauchy', 'kick_0.5', 'kick_1.0']),
                           ('R-RAIZ-0', ['brownian', 'kick_0.5']),
                           ('R-MOD', ['brownian']),
                           ('R-LIN', ['brownian', 'cauchy'])):
        for k in kinds:
            if reading == 'R-MOD':
                # R-MOD exige QNM exato; usa o valor exato lido da grade da bancada (QNM_GRID.json)
                grid = json.load(open(os.path.join(BENCH, 'QNM_GRID.json')))['modes']['220']
                from scipy.interpolate import CubicSpline
                q = CubicSpline(grid['spins'], np.array(grid['real']) + 1j * np.array(grid['imag']))(.68)
                pr = prediction(68.1, .68, 'R-MOD', qnm_dimensionless=complex(q))
                # reutiliza run_cell com um patch local: injeta gamma/omega/tau via reading generico
                cell = run_cell_custom(68.1, .68, pr, k, NREP, 128, 3)
            else:
                cell = run_cell(68.1, .68, reading, k, NREP, None, None, 3, use_exact_window_samples=128)
            A.append(cell); print('A', reading, k, 'sd_df %.4f mad_df %.4f mean_dtau %.4f (ens %.4f) sd_dtau %.4f' % (
                cell['sd_df'], cell['mad_df'], cell['mean_dtau'], cell['ensemble_dtau'], cell['sd_dtau']), flush=True)
    out['parts']['A_unraveling_dependence_ref_68p1_0p68_128samples'] = A
    # ---- Parte B: escala com spin e janela (browniano, R-B), massa fixa; e com massa a janela fixa
    B = []
    for spin in (0.5, 0.68, 0.8, 0.9):
        for w in (3, 6, 10):
            c = run_cell(68.1, spin, 'R-B', 'brownian', 400, w, None, 5)
            B.append(c); print('B spin', spin, 'win', w, 'x %.4f Q %.2f sd_df %.4f env %.4f mean_dtau %.4f/%.4f' % (
                c['x'], c['Q'], c['sd_df'], c['gerencia_envelope_sd_df'], c['mean_dtau'], c['ensemble_dtau']), flush=True)
    for mass in (40., 68.1, 120.):
        c = run_cell(mass, .68, 'R-B', 'brownian', 400, 6, None, 7)
        B.append(c); print('B mass', mass, 'sd_df %.4f mean_dtau %.4f' % (c['sd_df'], c['mean_dtau']), flush=True)
    out['parts']['B_scaling_spin_window_mass'] = B
    # ---- Parte C: SNR (ruido branco), RG vs R-B browniano; quadratura
    C = []
    for snr in (10., 20., 40., 100.):
        g = run_cell(68.1, .68, 'R-GLOBAL', 'ensemble_deterministic', 400, None, snr, 11, use_exact_window_samples=128)
        b = run_cell(68.1, .68, 'R-B', 'brownian', 400, None, snr, 11, use_exact_window_samples=128)
        quad = math.sqrt(max(b['sd_df'] ** 2 - g['sd_df'] ** 2, 0.))
        C.append(dict(snr=snr, GR=g, RB=b, sd_df_excess_quadrature=quad))
        print('C snr', snr, 'GR sd_df %.4f mean_df %.4f mean_dtau %.4f | R-B sd_df %.4f mean_dtau %.4f | excesso quad %.4f' % (
            g['sd_df'], g['mean_df'], g['mean_dtau'], b['sd_df'], b['mean_dtau'], quad), flush=True)
    out['parts']['C_snr_white_noise'] = C
    # ---- numeros da C2 lidos do arquivo (nao recomputados)
    c2 = json.load(open(os.path.join(BENCH, 'C2_TRAJECTORY_RECOVERY.json')))
    lido = {}
    for r in c2['rows']:
        key = r['reading'] + ('' if r.get('occupation') is None else '_N%d' % r['occupation'])
        lido[key] = {c['detector_noise']: dict(mean_df=c['mean_df'], sd_df=c['standard_deviation_of_fitted_df'],
                                                mean_dtau=c['mean_dtau'], dtau_q=c['dtau_05_50_95'], N=c['N'])
                     for c in r['comparisons']}
    out['C2_lido'] = lido
    out['elapsed_s'] = time.time() - t0
    json.dump(out, open(os.path.join(HERE, 'd1_resultado.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('OK', out['elapsed_s'])

def run_cell_custom(mass, spin, pr, kind, n_rep, n_samples, seed):
    """Variante para leituras que exigem QNM exato (R-MOD): recebe a predicao pronta."""
    omega, tau, gamma = pr['omega_rad_s'], pr['tau_gr_s'], pr['gamma_per_s']
    t = np.arange(n_samples) / FS
    rng = np.random.default_rng(seed)
    carrier = np.exp(-t / tau) * np.exp(1j * (omega * t + 0.37))
    factors = np.exp(1j * phase_process(kind, gamma, t, rng, n_rep))
    y = (carrier[None, :] * factors).real
    dfs, dts = [], []
    for row in y:
        a, b = fit(t, row, omega, tau); dfs.append(a); dts.append(b)
    dfs, dts = np.array(dfs), np.array(dts)
    mad = lambda v: float(1.4826 * np.median(np.abs(v - np.median(v))))
    return dict(mass=mass, spin=spin, reading=pr['reading'], unraveling=kind, n_rep=n_rep, window_tau=float(t[-1] / tau),
                n_samples=n_samples, snr=None, x=gamma * tau, Q=pr['quality'], f_hz=pr['f_gr_hz'], tau_ms=tau * 1e3,
                ensemble_dtau=-gamma * tau / (1 + gamma * tau), mean_df=float(dfs.mean()), sd_df=float(dfs.std(ddof=1)),
                mad_df=mad(dfs), q05_50_95_df=np.quantile(dfs, [.05, .5, .95]).tolist(), mean_dtau=float(dts.mean()),
                sd_dtau=float(dts.std(ddof=1)), mad_dtau=mad(dts), se_mean_dtau=float(dts.std(ddof=1) / math.sqrt(len(dts))),
                q05_50_95_dtau=np.quantile(dts, [.05, .5, .95]).tolist(),
                gerencia_envelope_sd_df=0.7 * math.sqrt(2 * gamma * tau) / (2 * pr['quality']))

if __name__ == '__main__':
    main()
