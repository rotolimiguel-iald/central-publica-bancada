import json, math
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
BETA = ALPHA_FINE_CODATA_2018*math.sqrt(math.e)
L = {float(k): complex(*v) for k, v in json.load(open('leaver_out.json')).items()}
def bcw(chi):
    f = 1.5251 - 1.1568*(1-chi)**0.1292
    q = 0.7000 + 1.4187*(1-chi)**(-0.4990)
    return f, q
def rmod(chi, w):  # geometric units M=1
    r = math.sqrt(1-chi*chi); kap = r/(2*(1+r)); OH = chi/(2*(1+r))
    nu = w.real - 2*OH; tau = 1/abs(w.imag)
    x = math.pi*BETA*nu*nu*tau/kap
    x_nocorot = math.pi*BETA*w.real**2*tau/kap
    return dict(nu=nu, kappa=kap, OmegaH=OH, x=x, d_exact=-x/(1+x), x_nocorot=x_nocorot, d_nocorot=-x_nocorot/(1+x_nocorot))
print('beta', BETA)
rows = {}
for chi in [0.0, 0.6712194217379245, 0.68, 0.6784704444609746, 0.9]:
    w = L[chi]; Q = w.real/(2*abs(w.imag))
    fb, qb = bcw(chi)
    dB_bcw = -BETA*fb*qb; dB_leaver = -BETA*w.real*Q
    raiz_x = BETA*Q
    rm = rmod(chi, w)
    # BCW control for R-MOD
    wb = complex(fb, -fb/(2*qb))
    rmb = rmod(chi, wb)
    rows[chi] = dict(Mw_leaver=[w.real, w.imag], Q_leaver=Q, Mw_bcw=fb, Q_bcw=qb, dB_linear_bcw=dB_bcw, dB_linear_leaver=dB_leaver,
                     raiz0_x_leaver=raiz_x, raiz0_d_exact=-raiz_x/(1+raiz_x), raiz0_x_bcw=BETA*qb, rmod=rm, rmod_bcw=rmb)
    print(f"chi={chi:.4f} Mw={w.real:.6f} Q={Q:.5f} | dB_lin BCW={dB_bcw:.5f} Leaver={dB_leaver:.5f} | RAIZ0 x={raiz_x:.5f} d={-raiz_x/(1+raiz_x):.5f} | RMOD nu={rm['nu']:.5f} x={rm['x']:.5f} d={rm['d_exact']:.5f} (BCW d={rmb['d_exact']:.5f}) nocorot d={rm['d_nocorot']:.4f}")
json.dump(rows, open('recompute_out.json','w'), indent=1)
# Sr root-law vacuum rate check
nu_Sr = 429228004229873.0  # Hz, 87Sr clock transition [KNOWN]
print('Sr root k=0 Gamma=beta*omega/2 =', BETA*2*math.pi*nu_Sr/2)
# units / 1e76
G=6.67430e-11; c=299792458.0; hbar=1.054571817e-34; GMsun=1.32712440041e20
Msun=GMsun/G; mP=math.sqrt(hbar*c/G); tP=math.sqrt(hbar*G/c**5)
tM60=60*GMsun/c**3
print('tM60 s',tM60,'tM60/tP',tM60/tP,'(Msun/mP)^2',(Msun/mP)**2,'(60Msun/mP)^2',(60*Msun/mP)**2, 'S_BH(Msun)/4pi=(Msun/mP)^2*... ', 4*math.pi*(Msun/mP)**2/(4*math.pi))
# Gamma=beta/t_M reading for GW250114 (dimensionally fixed text), x=beta*tau/t_M
w=L[0.6784704444609746]; tau=1/abs(w.imag)
x=BETA*tau; print('Gamma=beta/tM: x=',x,'d=',-x/(1+x))
