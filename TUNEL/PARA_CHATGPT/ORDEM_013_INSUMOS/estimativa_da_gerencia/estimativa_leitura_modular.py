# -*- coding: utf-8 -*-
# ESTIMATIVA DA GERENCIA (a refazer pela bancada) -- a leitura "modular do horizonte" da lei da casa no QNM 220.
# ESTATUTO: [CONJECTURE -- hipotese da gerencia de 21/09/2026; NAO e' canone nem leitura do operador] + [DERIVED sob a hipotese -- conta de envelope].
# [KNOWN, referencias de memoria NAO lidas pela gerencia -- conferir na fonte]: Bisognano-Wichmann (J. Math. Phys. 16, 985, 1975; 17, 303, 1976) vale
# para a cunha de Minkowski; Sewell (Ann. Phys. 141, 201, 1982) para o horizonte bifurcado estatico (Schwarzschild, Hartle-Hawking); Kay & Wald
# (Phys. Rep. 207, 49, 1991) provam a INEXISTENCIA de estado estacionario Hadamard em Kerr (a != 0) -- NAO ha Hartle-Hawking de Kerr, e o estado de
# Unruh nao e' KMS no exterior. Logo a identificacao abaixo, para a != 0, e' [CONJECTURE] ou parede. O mesmo relogio (periodo KMS do horizonte
# local) aplicado a um relogio de laboratorio e' a alternativa Unruh-g, EXCLUIDA pelos relogios v369 se a lei for universal.
# Hipotese [a derivar ou refutar]: K_partial = gerador modular do exterior (so' [KNOWN] em a = 0, Hartle-Hawking):
#   K = (2 pi / kappa_H) (H_Killing - Omega_H J)/hbar  =>  por quantum do modo (l=m=2): Delta K = 2 pi (omega - m Omega_H)/kappa_H
# Forma de Milburn no tempo modular s (d rho/ds = -(beta/2)[K,[K,rho]]), convertida ao tempo de Killing t = s * 2pi/kappa_H:
#   Gamma_amp = (kappa_H/2pi) * (beta/2) * (Delta K)^2 = (1/2) beta * (2 pi/kappa_H) * (omega - m Omega_H)^2
# isto e', a lei da casa com tau* = 2 pi/kappa_H (o periodo KMS) e omega -> omega - m Omega_H. Convencao de Gamma (amplitude vs coerencia): A FIXAR.
# Comparacao: ramo A (tau* = t_P), ramo B (tau* = G M_f/c^3, forma do ringdown_dephasing_v2.py), leitura "beta/t_M" (hipotetica).
import math, json, sys
sys.stdout.reconfigure(encoding='utf-8')
ALPHA = 7.2973525693e-3; BETA = ALPHA * math.sqrt(math.e)
G = 6.67430e-11; C = 299792458.0; HBAR = 1.054571817e-34; GM_SUN = 1.32712440018e20
T_P = math.sqrt(HBAR * G / C ** 5)
def berti(a):   # l=m=2, n=0 -- Berti, Cardoso & Will 2006 (coeficientes conferidos na fonte pela frente de literatura)
    Mw = 1.5251 - 1.1568 * (1 - a) ** 0.1292; Q = 0.7000 + 1.4187 * (1 - a) ** (-0.4990); return Mw, Q
out = {}
for nome, Mdet, a in (('GW250114 (M_det 68.1, chi 0.68)', 68.1, 0.68), ('GW150914 do programa (67.74, 0.671)', 67.7375, 0.67122), ('a=0 (60 Msun)', 60.0, 0.0), ('a=0.9 (60 Msun)', 60.0, 0.9)):
    tM = GM_SUN * Mdet / C ** 3
    Mw, Q = berti(a); w = Mw / tM; tau = 2 * Q / w
    rp = 1 + math.sqrt(1 - a * a)                                 # r_+/M
    kappa = math.sqrt(1 - a * a) / (2 * rp) / tM                 # 1/s
    OmH = a / (2 * rp) / tM
    tauKMS = 2 * math.pi / kappa
    wco = w - 2 * OmH
    x = {}
    for ramo, g in (('A tau*=t_P', 0.5 * BETA * T_P * w * w), ('B tau*=GM/c^3', 0.5 * BETA * tM * w * w),
                    ('MODULAR tau*=2pi/kappa_H, omega-2Omega_H', 0.5 * BETA * tauKMS * wco * wco),
                    ('MODULAR sem co-rotacao (omega)', 0.5 * BETA * tauKMS * w * w), ('hipotetica beta/t_M', BETA / tM)):
        xt = g * tau
        x[ramo] = {'Gamma_per_s': g, 'Gamma_over_omega': g / w, 'x=Gamma*tau': xt, 'delta_lin': -xt, 'delta_exato': -xt / (1 + xt)}
    out[nome] = {'f220_Hz': w / (2 * math.pi), 'tau220_ms': tau * 1e3, 'Q': Q, 'kappa_H_per_s': kappa, 'tauKMS_over_tM': tauKMS / tM,
                 'Omega_H_per_s': OmH, '(omega-2OmegaH)/omega': wco / w, 'K_mode_corot=2pi(w-2Om)/kappa': 2 * math.pi * wco / kappa, 'ramos': x}
print('beta =', BETA)
for k, v in out.items():
    print('\n==', k, '| f %.1f Hz tau %.3f ms Q %.3f | 2pi/kappa = %.2f t_M | (w-2Om)/w = %.3f | K_mode = %.2f' % (
        v['f220_Hz'], v['tau220_ms'], v['Q'], v['tauKMS_over_tM'], v['(omega-2OmegaH)/omega'], v['K_mode_corot=2pi(w-2Om)/kappa']))
    for r, d in v['ramos'].items():
        print('   %-45s Gamma %.3e /s  Gamma/w %.2e  x %.3e  delta_exato %.4f' % (r, d['Gamma_per_s'], d['Gamma_over_omega'], d['x=Gamma*tau'], d['delta_exato']))
json.dump(out, open(__file__.replace('.py', '_result.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
