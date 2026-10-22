# -*- coding: utf-8 -*-
"""ORDEM 013 - frente NUMEROS (levantamento para a gerencia; SOMENTE LEITURA na casa).
Auditoria dimensional do texto de 'confrontacao' + a lei da casa aplicada ao QNM 220 + energia modular
+ propagacao + sensibilidade grosseira. beta NUNCA literal: ALPHA_CODATA_2018 * sqrt(e) em runtime.
Constantes: G, hbar, c, k_B lidas de scipy.constants (scipy 1.18 = CODATA 2022; para G, hbar, c, k_B os
valores sao numericamente IDENTICOS aos de CODATA 2018). alpha e DIGITADO de CODATA 2018 (o de scipy e 2022).
M_sun via GM_sun nominal IAU 2015 B3 [KNOWN]. Nada aqui escreve fora da pasta deste script."""
import os, sys, json, math, hashlib
import numpy as np
import scipy, scipy.constants as sc

HERE = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
GW = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\gw"
PATHS = {
    "um.py": os.path.join(NOS, "um.py"),
    "um_absoluto.json": os.path.join(NOS, "um_absoluto.json"),
    "ringdown_dephasing_v2.py": os.path.join(NOS, "eco_ancorado_v1", "ringdown_dephasing_v2.py"),
    "RINGDOWN_DEPHASING_V2_RESULT.json": os.path.join(GW, "RINGDOWN_DEPHASING_V2_RESULT.json"),
    "RINGDOWN_DEPHASING_V1_RESULT.json": os.path.join(GW, "RINGDOWN_DEPHASING_V1_RESULT.json"),
    "gwtc_full_catalog.csv": r"C:\IALD\projetos_pyhton\IALD\gwtc_full_catalog.csv",
    "tgl_paper_unified.py": r"C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py",
    "TEXTO_CONFRONTACAO": os.path.join(HERE, "..", "..", "TEXTO_CONFRONTACAO_OPERADOR_21SET_VERBATIM.md"),
}

def sha256(p, bs=1 << 22):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(bs), b""): h.update(b)
    return h.hexdigest()

OUT = {"script": os.path.abspath(__file__), "scipy": scipy.__version__, "python": sys.version.split()[0]}
OUT["sha256"] = {k: sha256(p) for k, p in PATHS.items()}

# ---------------- constantes ----------------
ALPHA_CODATA_2018 = 7.2973525693e-3          # digitado (CODATA 2018); scipy traz o de 2022
BETA = ALPHA_CODATA_2018 * math.sqrt(math.e)  # runtime
G, HBAR, C, KB = sc.G, sc.hbar, sc.c, sc.k
GM_SUN = 1.3271244e20                          # IAU 2015 B3 nominal [KNOWN]
MSUN = GM_SUN / G
M_PL = math.sqrt(HBAR * C / G); T_P = math.sqrt(HBAR * G / C ** 5); E_P = M_PL * C ** 2
MPC = 1e6 * sc.parsec
OUT["constants"] = dict(alpha_CODATA2018=ALPHA_CODATA_2018, alpha_scipy=sc.fine_structure, beta=BETA, G=G, hbar=HBAR, c=C, kB=KB,
                        GM_sun_IAU=GM_SUN, M_sun_kg=MSUN, M_Pl_kg=M_PL, t_P_s=T_P, E_P_J=E_P, Mpc_m=MPC)

# ---------------- dados do programa (lidos, nunca de memoria) ----------------
v2 = json.load(open(PATHS["RINGDOWN_DEPHASING_V2_RESULT.json"], encoding="utf-8"))
g150 = [r for r in v2["per_series"] if r.get("event") == "GW150914"][0]
core = json.load(open(PATHS["um_absoluto.json"], encoding="utf-8"))["core"]
clock = core["clock_test_result_v369"]; rd2 = core["ringdown_dephasing_result_v2"]
TAU_STAR_CLOCK95 = clock["P1"]["tau_star_bound_clock_95_s"]
OUT["read_from_program"] = dict(GW150914_Mf_det=g150["Mf_det"], GW150914_a_f=g150["a_f"], GW150914_f_gr=g150["f_gr"],
                                GW150914_tau_gr_ms=g150["tau_gr_ms"], GW150914_delta_pred_B=g150["delta_pred_B"], GW150914_delta_pred_A=g150["delta_pred_A"],
                                V2_stack_3ms=v2["stacks"]["3.0"], V2_verdict=rd2["verdict"], V2_reasons=rd2.get("reasons"),
                                clock_tau_star_bound_95_s=TAU_STAR_CLOCK95, clock_tau_star_bound_95_in_tP=clock["P1"]["tau_star_bound_clock_95_in_tP"],
                                clock_root_law=clock["root_law"], clock_verdict=clock["verdict"])
# catalogo do programa: GW150914 z, D_L, M_f fonte
import csv
cat = {r["commonName"]: r for r in csv.DictReader(open(PATHS["gwtc_full_catalog.csv"], encoding="utf-8"))}
c150 = cat["GW150914"]
OUT["catalog_GW150914"] = {k: c150[k] for k in ("version", "catalog.shortName", "redshift", "luminosity_distance", "luminosity_distance_lower", "luminosity_distance_upper", "final_mass_source", "mass_1_source", "mass_2_source", "chi_eff")}
OUT["catalog_has_GW250114"] = "GW250114" in cat
OUT["catalog_n_events"] = len(cat)

# ---------------- QNM 220: ajuste de Berti-Cardoso-Will 2006 COPIADO de ringdown_dephasing_v2.py:38-40 ----------------
def berti(Mf_det_msun, a):
    a = min(max(a, 0.0), 0.998); mw = 1.5251 - 1.1568 * (1 - a) ** 0.1292; q = 0.7000 + 1.4187 * (1 - a) ** (-0.4990)
    f0 = mw * C ** 3 / (2 * math.pi * G * Mf_det_msun * MSUN); return f0, q / (math.pi * f0), q, mw

def kerr_TH(M_msun, a):
    """T_H de Kerr [KNOWN]: k_B T_H = hbar c^3/(G M) * sqrt(1-a^2) / (4 pi (1+sqrt(1-a^2))). Retorna (T_K, Omega_H rad/s, r_+ m)."""
    M = M_msun * MSUN; s = math.sqrt(1 - a * a); rp = G * M / C ** 2 * (1 + s)
    kT = HBAR * C ** 3 / (G * M) * s / (4 * math.pi * (1 + s))
    Om = a * C / (2 * rp)            # Omega_H = a c / (2 r_+) com a adimensional
    return kT / KB, Om, rp, kT

EVENTS = {
    # nome: (M_fonte, a, z, D_L lista Mpc, estatuto)
    "M60_Schw": dict(M_src=60.0, a=0.0, z=0.0, DL=[], st="[INPUT do texto colado: M ~ 60 Msun; a=0 para S_BH de Schwarzschild]"),
    "GW150914_programa": dict(M_det=g150["Mf_det"], a=g150["a_f"], z=float(c150["redshift"]), DL=[410.0, float(c150["luminosity_distance"])],
                              st="[REAL lido] Mf_det e a_f do RINGDOWN_DEPHASING_V2_RESULT.json (EOB SEOBNRv4 de m1,m2,chi_eff do catalogo); z e D_L=470 do catalogo GWTC-2.1 do programa; D_L=410 = valor GWTC-1 [KNOWN, a conferir]"),
    "GW150914_texto": dict(M_src=62.0, a=0.67, z=float(c150["redshift"]), DL=[410.0], st="[INPUT da ordem: M_f~62, a~0,67 (fonte)]"),
    "GW250114_lit": dict(M_src=62.7, a=0.68, z=0.09, DL=[440.0],
                         st="[KNOWN via fonte secundaria (Wikipedia 'GW250114', cita o suplemento Abac+ PRL 10.1103/kw5g-d732): M_f=62,7(+1,0/-1,1), chi_f=0,68(+-0,01), z=0,09; D_L~440 Mpc; a conferir na primaria]. O programa NAO tem GW250114 no catalogo nem no um.py"),
}
for k, e in EVENTS.items():
    if "M_det" not in e: e["M_det"] = e["M_src"] * (1 + e["z"])
    if "M_src" not in e: e["M_src"] = e["M_det"] / (1 + e["z"])

res = {}
for name, e in EVENTS.items():
    r = dict(status=e["st"], M_src=e["M_src"], M_det=e["M_det"], a=e["a"], z=e["z"])
    M = e["M_src"] * MSUN
    # (1) auditoria dimensional
    r["M_over_MPl"] = M / M_PL
    r["M_over_MPl_sq"] = (M / M_PL) ** 2
    r["S_BH_Schw_4pi_MMPl2"] = 4 * math.pi * (M / M_PL) ** 2
    r["S_BH_Kerr"] = 2 * math.pi * (M / M_PL) ** 2 * (1 + math.sqrt(1 - e["a"] ** 2))
    r["GM_over_c3_s_src"] = G * M / C ** 3
    r["GM_over_c3_in_tP"] = (G * M / C ** 3) / T_P      # identico a M/M_Pl
    r["M_over_MPl2_natural"] = {"valor_em_unidades_de_Planck": M / M_PL, "dimensao": "1/massa = tempo (hbar=c=1); em SI: M/M_Pl^2 [kg^-1] x hbar/c^2 = GM/c^3 [s]",
                                "em_s": (M / M_PL ** 2) * HBAR / C ** 2, "em_eV^-1": (M / M_PL ** 2) * (sc.e / C ** 2), "em_GeV^-1": (M / M_PL ** 2) * (1e9 * sc.e / C ** 2)}
    TK, Om, rp, kT = kerr_TH(e["M_src"], e["a"])
    r["T_H_K_src"] = TK
    r["K_BH_total_Mc2_over_kTH"] = M * C ** 2 / kT   # 'energia modular' do BH inteiro (Gibbs K=H/T)
    # (2) QNM 220 no referencial do detector (como o programa)
    f0, tau, Q, mw = berti(e["M_det"], e["a"]); w = 2 * math.pi * f0
    r["QNM"] = dict(f220_Hz=f0, omega220_rad_s=w, tau220_ms=tau * 1e3, Q220=Q, M_omega_geom=mw, omega_tau=w * tau)
    gm_det = G * e["M_det"] * MSUN / C ** 3
    branches = {"A_tP": T_P, "tP_over_beta": T_P / BETA, "B_GMf_c3_det": gm_det, "clock95_bound": TAU_STAR_CLOCK95}
    rb = {}
    for bn, ts in branches.items():
        Gam = 0.5 * BETA * ts * w ** 2
        rb[bn] = dict(tau_star_s=ts, tau_star_in_tP=ts / T_P, Gamma_per_s=Gam, Gamma_over_omega=Gam / w, Gamma_tau220=Gam * tau,
                      delta_lin_programa=-Gam * tau, delta_exato=-Gam * tau / (1 + Gam * tau), tau_deph_s=1 / Gam)
    r["lei_da_casa"] = rb
    r["delta_B_forma_fechada"] = -BETA * mw * Q           # = -(1/2) beta (GM/c^3) w^2 tau, pois w tau = 2Q e (GM/c^3) w = mw
    # (3) energia modular do modo
    TKd, Omd, rpd, kTd = kerr_TH(e["M_det"], e["a"])     # detector: omega e T_H no mesmo referencial (a razao e invariante)
    r["K_mode_omega_over_TH"] = HBAR * w / kTd
    r["K_mode_superrad_(omega-2OmegaH)_over_TH"] = HBAR * (w - 2 * Omd) / kTd
    r["Omega_H_det_rad_s"] = Omd; r["T_H_K_det"] = TKd
    # leituras da lei-raiz do PROPRIO programa (um.py 191254-191256: Gamma = beta/(2 hbar) (hw)^2/(sqrt(E_lo+hw)+sqrt(E_lo))^2)
    hw = HBAR * w
    def root(E_lo): return (BETA / (2 * HBAR)) * hw * hw / (math.sqrt(E_lo + hw) + math.sqrt(E_lo)) ** 2
    rr = {}
    for ln, El in (("E_lo=0 (vacuo; linear)", 0.0), ("E_lo=E_P/4 (canonica, tau*=t_P)", 0.25 * E_P), ("E_lo=E_P (k1=1 do modulo P6)", E_P), ("E_lo=M_f c^2 (fundo = massa do BH)", e["M_det"] * MSUN * C ** 2)):
        Gm = root(El); rr[ln] = dict(Gamma_per_s=Gm, Gamma_over_omega=Gm / w, Gamma_tau220=Gm * tau, delta_lin=-Gm * tau)
    r["lei_raiz_do_programa"] = rr
    # (4) propagacao
    rp_ = {}
    for DL in e["DL"]:
        Dc = DL * MPC / C
        d = dict(D_L_Mpc=DL, D_over_c_s=Dc)
        for bn, ts in branches.items():
            Gam = 0.5 * BETA * ts * w ** 2; x = Gam * Dc
            d[bn] = dict(Gamma_D_over_c=x, exp_minus=math.exp(-x) if x < 700 else 0.0, log10_exp=-x / math.log(10))
        d["tau_star_para_GammaD_c_igual_1_s"] = 1.0 / (0.5 * BETA * w ** 2 * Dc)
        d["tau_star_para_GammaD_c_igual_1_in_tP"] = d["tau_star_para_GammaD_c_igual_1_s"] / T_P
        rp_["%g" % DL] = d
    r["propagacao"] = rp_
    res[name] = r
OUT["eventos"] = res

# reproducao do numero do programa com as constantes DELE (ringdown_dephasing_v2.py:22-23): G=6.674e-11, MSUN=1.98892e30
Gp, MSp, Cp = 6.674e-11, 1.98892e30, 2.99792458e8
a = g150["a_f"]; mw = 1.5251 - 1.1568 * (1 - a) ** 0.1292; q = 0.7 + 1.4187 * (1 - a) ** (-0.4990)
f0p = mw * Cp ** 3 / (2 * math.pi * Gp * g150["Mf_det"] * MSp); taup = q / (math.pi * f0p); gmp = Gp * g150["Mf_det"] * MSp / Cp ** 3
OUT["reproducao_GW150914_constantes_do_programa"] = dict(f_gr=f0p, tau_gr_ms=taup * 1e3, delta_B=-0.5 * BETA * gmp * (2 * math.pi * f0p) ** 2 * taup,
                                                         delta_B_json=g150["delta_pred_B"], diff=(-0.5 * BETA * gmp * (2 * math.pi * f0p) ** 2 * taup) - g150["delta_pred_B"])
# delta_B depende SO do spin
OUT["delta_B_vs_spin"] = {("a=%.2f" % aa): -BETA * (1.5251 - 1.1568 * (1 - aa) ** 0.1292) * (0.7 + 1.4187 * (1 - aa) ** (-0.4990)) for aa in (0.0, 0.3, 0.5, 0.6, 0.67, 0.68, 0.7, 0.8, 0.9)}
OUT["delta_rootvacuo_vs_spin_(-beta*Q)"] = {("a=%.2f" % aa): -BETA * (0.7 + 1.4187 * (1 - aa) ** (-0.4990)) for aa in (0.0, 0.67, 0.68, 0.9)}

# candidatos a '10^76'
M60 = 60 * MSUN; w60 = 2 * math.pi * berti(60.0, 0.67)[0]
cands = {
    "M/M_Pl (60 Msun)": M60 / M_PL, "(M/M_Pl)^2 (60 Msun)": (M60 / M_PL) ** 2, "S_BH=4pi(M/M_Pl)^2 (60 Msun)": 4 * math.pi * (M60 / M_PL) ** 2,
    "K_BH=Mc^2/kT_H=8pi(M/M_Pl)^2 (60 Msun, Schw)": 8 * math.pi * (M60 / M_PL) ** 2,
    "S_BH (1 Msun)": 4 * math.pi * (MSUN / M_PL) ** 2, "M/M_Pl^2 em GeV^-1": (M60 / M_PL ** 2) * (1e9 * sc.e / C ** 2), "M/M_Pl^2 em eV^-1": (M60 / M_PL ** 2) * (sc.e / C ** 2),
    "M/M_Pl^2 em kg^-1 (SI cru)": M60 / M_PL ** 2, "GM/c^3 em s": G * M60 / C ** 3, "numero de nucleons": M60 / sc.m_p,
    "Mc^2/(hbar w220) (a=0.67)": M60 * C ** 2 / (HBAR * w60), "beta*Mc^2/hbar em s^-1 (jump rate da leitura modular)": BETA * M60 * C ** 2 / HBAR,
}
OUT["candidatos_10e76"] = {k: dict(valor=v, log10=math.log10(v), distancia_de_76_em_decadas=math.log10(v) - 76) for k, v in cands.items()}

# (1b) algebra de dimensoes (expoentes M, L, T)
def dim(Mx=0, Lx=0, Tx=0): return np.array([Mx, Lx, Tx], dtype=float)
D = {"beta": dim(), "K=-ln Delta": dim(), "Gamma (taxa)": dim(Tx=-1), "M": dim(Mx=1), "M_Pl": dim(Mx=1), "hbar": dim(1, 2, -1), "c": dim(0, 1, -1), "G": dim(-1, 3, -2)}
beta_K = D["beta"] + D["K=-ln Delta"]
M_over_MPl2_SI = D["M"] - 2 * D["M_Pl"]
M_over_MPl2_times_hbar_over_c2 = M_over_MPl2_SI + D["hbar"] - 2 * D["c"]
OUT["dimensoes"] = dict(beta_K=beta_K.tolist(), Gamma=D["Gamma (taxa)"].tolist(), beta_K_e_taxa=bool(np.all(beta_K == D["Gamma (taxa)"])),
                        M_over_MPl2_SI_kg=M_over_MPl2_SI.tolist(), M_over_MPl2_x_hbar_over_c2=M_over_MPl2_times_hbar_over_c2.tolist(),
                        beta_M_over_MPl2_e_taxa=bool(np.all(M_over_MPl2_times_hbar_over_c2 == D["Gamma (taxa)"])),
                        nota="beta*<K> tem dimensao [M^0 L^0 T^0]: e numero puro, nao taxa. M/M_Pl^2 (hbar=c=1) tem dimensao de TEMPO ([T^1] apos x hbar/c^2 = GM/c^3), logo beta*M/M_Pl^2 seria um tempo, nunca uma taxa. Para virar taxa, beta*<K> precisa de uma escala: Gamma = beta*<K>/t_unit.")

# (G) checagem GKSL finita: L = sqrt(beta c) sqrt(n) sobre estado coerente |alpha|^2 = N
def gksl_check(N, c=1.0):
    nmax = int(N + 12 * math.sqrt(N) + 40); n = np.arange(nmax)
    from math import lgamma
    amp = np.exp(-N / 2 + n * 0.5 * math.log(N) - 0.5 * np.array([lgamma(k + 1) for k in n])) if N > 0 else (n == 0).astype(float)
    psi = amp.astype(complex); psi /= np.linalg.norm(psi); rho = np.outer(psi, psi.conj())
    a_op = np.diag(np.sqrt(np.arange(1, nmax)), 1).astype(complex)
    Lop = np.diag(np.sqrt(BETA * c * n)).astype(complex); LdL = Lop.conj().T @ Lop
    Lrho = Lop @ rho @ Lop.conj().T - 0.5 * (LdL @ rho + rho @ LdL)
    ea = np.trace(a_op @ rho); dea = np.trace(a_op @ Lrho)
    rate = float(-(dea / ea).real)
    jump = float(np.trace(LdL @ rho).real)
    return {"N": N, "nmax": nmax, "taxa_de_decaimento_de_<a>": rate,
            "previsto_raiz_(beta c/2)(sqrt(N+1)-sqrt(N))^2": 0.5 * BETA * c * (math.sqrt(N + 1) - math.sqrt(N)) ** 2,
            "previsto_assintotico_beta_c/(8N)": BETA * c / (8 * N), "taxa_de_saltos_Tr(LdL rho)": jump, "beta_c_N": BETA * c * N,
            "razao_saltos_sobre_decoerencia": jump / rate}
OUT["gksl_finito"] = [gksl_check(N) for N in (4.0, 16.0, 64.0, 256.0)]

# (H) numero de quanta do modo (ordem de grandeza) e leitura coerente
for name, E_rad_msun, st in (("GW150914_programa", 3.0, "[KNOWN, Abbott+2016 PRL 116 061102: E_rad = 3,0 +- 0,5 Msun c^2]"),
                             ("GW250114_lit", 33.6 + 32.2 - 62.7, "[DERIVED de m1=33,6, m2=32,2, M_f=62,7 (fonte secundaria, a conferir)]")):
    w = res[name]["QNM"]["omega220_rad_s"]; tau = res[name]["QNM"]["tau220_ms"] * 1e-3
    Nq = E_rad_msun * MSUN * C ** 2 / (HBAR * w)
    Gc = 0.5 * BETA * w * (math.sqrt(Nq + 1) - math.sqrt(Nq)) ** 2 if Nq < 1e30 else BETA * w / (8 * Nq)
    res[name]["leitura_coerente"] = dict(E_rad_Msun=E_rad_msun, E_rad_status=st, N_quanta_a_omega220=Nq, Gamma_coerente_per_s=Gc, Gamma_coerente_tau220=Gc * tau,
                                         nota="leitura modular (K = hbar w n/(k_B T_H), tempo modular -> fisico por k_B T_H/hbar): Gamma_<a> = (beta w/2)(sqrt(N+1)-sqrt(N))^2 ~ beta w/(8N) [DERIVED aqui; nao esta no programa]")

# (I) sensibilidade grosseira
sig_list = {
    "0.30 (cenario)": 0.30, "0.20 (cenario)": 0.20, "0.10 (cenario)": 0.10,
    "V2 do programa, 15 series empilhadas (1 sigma, REAL lido)": v2["stacks"]["3.0"]["sigma"],
    "GWTC-4.0 hierarquico: dtau220 = 0.16 +0.18/-0.16 (90%) -> 1 sigma ~ 0.17/1.645 [KNOWN via arXiv:2509.08099, a conferir]": 0.17 / 1.645,
    "GW250114 pSEOBNR: dtau220 = -0.01 +0.10/-0.09 (90%) -> 1 sigma ~ 0.095/1.645 [KNOWN via arXiv:2509.08099, a conferir]": 0.095 / 1.645,
}
dB = res["GW250114_lit"]["lei_da_casa"]["B_GMf_c3_det"]["delta_lin_programa"]
dB150 = res["GW150914_programa"]["lei_da_casa"]["B_GMf_c3_det"]["delta_lin_programa"]
dC = res["GW250114_lit"]["lei_raiz_do_programa"]["E_lo=0 (vacuo; linear)"]["delta_lin"]
sens = {}
for k, s in sig_list.items():
    sens[k] = dict(sigma=s, ramoB_a068=dict(delta=dB, z=abs(dB) / s, lnB_meio_z2=0.5 * (dB / s) ** 2, N_eventos_para_5sigma=(5 * s / abs(dB)) ** 2),
                   raiz_vacuo_a068=dict(delta=dC, z=abs(dC) / s, lnB_meio_z2=0.5 * (dC / s) ** 2, N_eventos_para_5sigma=(5 * s / abs(dC)) ** 2))
OUT["sensibilidade"] = sens
OUT["sigma_necessario"] = dict(ramoB_5sigma=abs(dB) / 5, ramoB_3sigma=abs(dB) / 3, ramoB_lnB_5=abs(dB) / math.sqrt(10), ramoB_lnB_8=abs(dB) / 4,
                               raizvacuo_5sigma=abs(dC) / 5,
                               SNR_rd_equivalente_ramoB_5sigma_se_sigma_prop_1_sobre_SNR=80 * (0.095 / 1.645) / (abs(dB) / 5),
                               nota="escala sigma ~ 1/SNR a partir de GW250114 (SNR de rede ~80, sigma ~0,058): estimativa grosseira [DERIVED]")
OUT["GW250114_central_vs_ramos"] = dict(delta_obs=-0.01, sigma=0.095 / 1.645, z_vs_GR=-0.01 / (0.095 / 1.645), z_vs_B=(-0.01 - dB) / (0.095 / 1.645), z_vs_raizvacuo=(-0.01 - dC) / (0.095 / 1.645))
OUT["GWTC4_central_vs_ramos"] = dict(delta_obs=0.16, sigma=0.17 / 1.645, z_vs_GR=0.16 / (0.17 / 1.645), z_vs_B=(0.16 - dB150) / (0.17 / 1.645), z_vs_raizvacuo=(0.16 - dC) / (0.17 / 1.645))

p = os.path.join(HERE, "numeros_ordem013_result.json")
tmp = p + ".tmp"; json.dump(OUT, open(tmp, "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=float); os.replace(tmp, p)
print("OK", p, os.path.getsize(p))
