# Revisor adversarial (fisica e numeros) -- ORDEM 013. Somente leitura na casa; escreve so aqui.
import math, json, sys, hashlib
import numpy as np
from scipy.linalg import sqrtm, expm
from scipy.stats import poisson
from scipy.integrate import quad
sys.stdout.reconfigure(encoding='utf-8')
R = {}
ALPHA_CODATA_2018 = 7.2973525693e-3
BETA = ALPHA_CODATA_2018 * math.sqrt(math.e)
G = 6.67430e-11; C = 299792458.0; HBAR = 1.054571817e-34; GM_SUN = 1.32712440018e20
MSUN = GM_SUN / G; MPL = math.sqrt(HBAR * C / G); TP = math.sqrt(HBAR * G / C ** 5)
print('beta runtime', BETA)

# (a) dimensional audit
M60 = 60 * MSUN
tGM = G * M60 / C ** 3
R['a'] = dict(GM_over_c3_60Msun_s=tGM, in_tP=tGM / TP, Msun_over_MPl_sq=(MSUN / MPL) ** 2,
              S_BH_1Msun=4 * math.pi * (MSUN / MPL) ** 2, M60_over_MPl_sq=(M60 / MPL) ** 2)
print('(a)', R['a'])


# (b) GKSL: L = sqrt(beta) sqrt(K); full Liouvillian (column-stacking vec)
def liouv(Ls, H=None):
    d = Ls[0].shape[0]; I = np.eye(d); Lv = np.zeros((d * d, d * d), complex)
    if H is not None:
        Lv += -1j * (np.kron(I, H) - np.kron(H.T, I))
    for L in Ls:
        LdL = L.conj().T @ L
        Lv += np.kron(L.conj(), L) - 0.5 * np.kron(I, LdL) - 0.5 * np.kron(LdL.T, I)
    return Lv


rng = np.random.default_rng(7)
k = np.sort(rng.uniform(0.2, 9.0, 6)); d = len(k)
Uh = np.linalg.qr(rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d)))[0]
K = Uh @ np.diag(k) @ Uh.conj().T
L = math.sqrt(BETA) * sqrtm(K)
ev = np.linalg.eigvals(liouv([L]))
pred = np.array([-0.5 * BETA * (math.sqrt(ki) - math.sqrt(kj)) ** 2 for ki in k for kj in k])
R['b_liouv_max_abs_resid'] = float(np.max(np.abs(np.sort(ev.real) - np.sort(pred))))
print('(b) Liouvillian eig vs -1/2 beta (sqrt ki - sqrt kj)^2: max resid', R['b_liouv_max_abs_resid'],
      'max |imag|', float(np.max(np.abs(ev.imag))))
c = 0.37
Lc = L + c * np.eye(d)
R['b_gauge_diff'] = float(np.max(np.abs(liouv([Lc]) - liouv([L]))))
rho = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d)); rho = rho @ rho.conj().T; rho /= np.trace(rho)
R['b_jump_rate'] = dict(beta_meanK=float(BETA * np.trace(K @ rho).real),
                        TrLdLrho=float(np.trace(L.conj().T @ L @ rho).real),
                        TrLcdLcrho_same_master_eq=float(np.trace(Lc.conj().T @ Lc @ rho).real))
print('(b) gauge L -> L + c*1: max |Liouvillian diff|', R['b_gauge_diff'], '| jump rates', R['b_jump_rate'])
for kbar in (1e1, 1e3, 1e6):
    dk = 1.0; r = 0.5 * BETA * (math.sqrt(kbar + dk / 2) - math.sqrt(kbar - dk / 2)) ** 2
    print('(b) IR kbar', kbar, 'rate', r, 'beta dk^2/(8 kbar)', BETA * dk ** 2 / (8 * kbar), 'ratio', r / (BETA * dk ** 2 / (8 * kbar)))


def rate_a(N, law):
    nmax = int(N + 12 * math.sqrt(N) + 30); n = np.arange(nmax)
    cn = np.sqrt(poisson.pmf(n, N))
    wts = np.sqrt(n[1:]) * cn[1:] * cn[:-1]
    if law == 'root':
        g = 0.5 * BETA * (np.sqrt(n[1:]) - np.sqrt(n[:-1])) ** 2
    else:
        g = 0.5 * BETA * (n[1:] - n[:-1]) ** 2.0
    return float(np.sum(wts * g) / np.sum(wts))


R['b_coherent'] = {}
for N in (16, 64, 256, 4096):
    rr = rate_a(N, 'root'); rm = rate_a(N, 'milburn')
    R['b_coherent'][N] = dict(root_rate=rr, beta_over_8N=BETA / (8 * N), ratio=rr / (BETA / (8 * N)), milburn_rate=rm, beta_over_2=BETA / 2)
    print('(b) coherent N', N, 'root rate', rr, 'beta/8N', BETA / (8 * N), 'ratio', round(rr / (BETA / (8 * N)), 5), '| Milburn', rm, 'beta/2', BETA / 2)
dim = 70; n = np.arange(dim); Ln = math.sqrt(BETA) * np.diag(np.sqrt(n)); a_op = np.diag(np.sqrt(n[1:]), 1)
Lv = liouv([Ln]); N0 = 16
cn = np.sqrt(poisson.pmf(n, N0)); cn /= np.linalg.norm(cn); rho0 = np.outer(cn, cn)
dt = 1e-2
rho_t = (expm(Lv * dt) @ rho0.reshape(-1, order='F')).reshape(dim, dim, order='F')
a0 = np.trace(a_op @ rho0).real; at = np.trace(a_op @ rho_t).real
R['b_coherent_liouv_N16'] = dict(rate=float(-math.log(at / a0) / dt), beta_over_8N=BETA / (8 * N0))
print('(b) full Liouvillian (dim 70) N=16: <a> rate', R['b_coherent_liouv_N16'])

# (d) ramo B with the program's constants
Gp = 6.674e-11; MSUNp = 1.98892e30


def berti_p(Mf_det, a):
    a = min(max(a, 0.0), 0.998); mw = 1.5251 - 1.1568 * (1 - a) ** 0.1292; q = 0.7000 + 1.4187 * (1 - a) ** (-0.4990)
    f0 = mw * C ** 3 / (2 * math.pi * Gp * Mf_det * MSUNp); return f0, q / (math.pi * f0), q


Mf, af = 67.73752907959711, 0.6712194217379245
f_gr, tau_gr, q_gr = berti_p(Mf, af); w_gr = 2 * math.pi * f_gr; gm = Gp * Mf * MSUNp / C ** 3
dB = -0.5 * BETA * gm * w_gr ** 2 * tau_gr
R['d_GW150914'] = dict(delta_B=dB, json=-0.019962060309612117, diff=dB - (-0.019962060309612117), f=f_gr, tau_ms=tau_gr * 1e3)
print('(d) GW150914 delta_B', repr(dB), 'diff vs JSON', dB - (-0.019962060309612117))


def bcw(a):
    return 1.5251 - 1.1568 * (1 - a) ** 0.1292, 0.7000 + 1.4187 * (1 - a) ** (-0.4990)


LK = json.load(open('leaver_kerr_result.json'))


def leav(a):
    e = LK[f'{a:.6f}']; return e['M_omega_R'], e['Q']


R['d_spin'] = {}
for a in (0.0, 0.5, 0.6, 0.65, 0.68, 0.7, 0.8, 0.9, 0.95, 0.99):
    Mw, Q = bcw(a); dl = -BETA * Mw * Q
    Mwe, Qe = leav(a); dle = -BETA * Mwe * Qe
    R['d_spin'][a] = dict(bcw=dl, leaver=dle, rel=(dl / dle - 1))
    print(f'(d) a={a}: delta_B BCW {dl:.5f}  Leaver {dle:.5f}  rel {dl / dle - 1:+.4f}')

# (e) V2 JSON
p = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw\RINGDOWN_DEPHASING_V2_RESULT.json"
b = open(p, 'rb').read(); st = json.loads(b)['stacks']['3.0']
R['e'] = dict(sha16=hashlib.sha256(b).hexdigest()[:16], delta_tau=st['delta_tau'], sigma=st['sigma'], z_vs_GR=st['z_vs_GR'],
              pred_B=st['delta_pred_B'], power_B=st['power_B'], bias=st['mean_bias_rel'], power_check=abs(st['delta_pred_B']) / st['sigma'])
print('(e)', R['e'])

# (f) 90% -> 1 sigma; z; lnB
z90 = 1.6448536269514722
sig = 0.5 * (0.10 + 0.09) / z90; dB68 = -BETA * bcw(0.68)[0] * bcw(0.68)[1]
z = abs(dB68) / sig; obs = -0.01
lnB_obs = (obs ** 2 - (obs - dB68) ** 2) / (2 * sig ** 2)
R['f'] = dict(sigma=sig, deltaB_068=dB68, z=z, lnB_expected_if_B=0.5 * z * z, lnB_expected_if_GR=-0.5 * z * z, sd_lnB=z,
              lnB_observed_point=lnB_obs, N5=(sig / (abs(dB68) / 5)) ** 2, sigma_needed_5=abs(dB68) / 5,
              SNR_total_needed=80 * sig / (abs(dB68) / 5), SNR_postmerger_needed=40 * sig / (abs(dB68) / 5))
occ = math.log(abs(dB68) / (math.sqrt(2 * math.pi) * sig))
R['f']['vallisneri_laplace_prior_width_deltaB'] = dict(Delta_over_sigma=abs(dB68) / sig, lnB=0.5 * z * z + 0.5 - occ)


def lnB_free(dhat):
    num = quad(lambda aa: math.exp(-(dhat - aa * dB68) ** 2 / (2 * sig ** 2)), 0, 1)[0]
    return math.log(num / math.exp(-dhat ** 2 / (2 * sig ** 2)))


xs = np.linspace(dB68 - 6 * sig, dB68 + 6 * sig, 801); wts = np.exp(-(xs - dB68) ** 2 / (2 * sig ** 2)); wts /= wts.sum()
R['f']['lnB_free_a01_expected_if_B'] = float(np.sum(wts * np.array([lnB_free(x) for x in xs])))
print('(f)', json.dumps(R['f'], indent=1))
s4 = 0.11 / z90
for nm, dv in (('GR', 0.0), ('B', dB68), ('MOD_corot_068', -0.0378), ('hip_beta_tM', -0.1277), ('MOD_sem_corot', -0.376)):
    print(f'(f) GWTC-4 conjunto 0.17+-{s4:.4f}: z({nm}) = {(0.17 - dv) / s4:.2f}; GW250114 -0.01+-{sig:.4f}: z = {(obs - dv) / sig:+.2f}')


# (g) modular reading
def modular(a, qfun):
    Mw, Q = qfun(a); rp = 1 + math.sqrt(1 - a * a); kap = math.sqrt(1 - a * a) / (2 * rp); Om = a / (2 * rp)
    wco = Mw - 2 * Om; tauK = 2 * math.pi / kap
    G_co = 0.5 * BETA * tauK * wco ** 2; G_no = 0.5 * BETA * tauK * Mw ** 2; tau = 2 * Q / Mw
    return dict(Mw=Mw, Q=Q, wco_over_w=wco / Mw, tauKMS_over_M=tauK, Gco_over_w=G_co / Mw, x_co=G_co * tau,
                dex_co=-(G_co * tau) / (1 + G_co * tau), Gno_over_w=G_no / Mw, x_no=G_no * tau,
                dex_no=-(G_no * tau) / (1 + G_no * tau), K_mode_co=tauK * wco)


R['g'] = {}
for a in (0.0, 0.5, 0.6, 0.68, 0.7, 0.8, 0.9, 0.95, 0.99):
    mb = modular(a, bcw); ml = modular(a, leav)
    R['g'][a] = dict(bcw=mb, leaver=ml)
    print(f"(g) a={a}: (w-2Om)/w BCW {mb['wco_over_w']:.4f} Leaver {ml['wco_over_w']:.4f} | delta_MOD BCW {mb['dex_co']:.4f} Leaver {ml['dex_co']:.4f} "
          f"| G/w co {ml['Gco_over_w']:.2e} | sem co-rot: G/w {ml['Gno_over_w']:.3f} x {ml['x_no']:.3f} delta {ml['dex_no']:.3f}")
for a in (0.0, 0.68, 0.9):
    Mw, Q = leav(a); x = BETA * Mw * Q
    print(f'(g) ramo B a={a}: Gamma/omega={0.5 * BETA * Mw:.2e}, x={x:.4f}, x/(2Q)={x / (2 * Q):.2e}')
json.dump(R, open('revisao_numeros_result.json', 'w'), indent=1, default=float)
