"""DG-02 ceptico: onde esta a fronteira EDOM (f_550 GR > fmax_gen) na prior registrada do piloto,
e o que ela faz com GW250114 e com os candidatos cegos. So leitura de /opt e dos JSON; escreve so aqui."""
import json, sys, time, numpy as np
import lal, lalsimulation as ls
OUT = sys.argv[1]
REG = '/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/RINGDOWN_5SIGMA_V1.json'
reg = json.load(open(REG, encoding='utf-8'))
job = reg['pe_jobs']['GW250114_PILOT']
pri = job['priors']
approx = ls.SEOBNRv4

def f550(m1, m2, s1, s2):
    v = lal.CreateCOMPLEX16Vector(1)
    ls.SimIMREOBGenerateQNMFreqV2(v, m1, m2, [0., 0., s1], [0., 0., s2], 5, 5, 1, approx)
    return v.data[0].real / (2 * np.pi)

def f220(m1, m2, s1, s2):
    v = lal.CreateCOMPLEX16Vector(1)
    ls.SimIMREOBGenerateQNMFreqV2(v, m1, m2, [0., 0., s1], [0., 0., s2], 2, 2, 1, approx)
    return v.data[0].real / (2 * np.pi)

def finals(m1, m2, s1, s2):
    mf = lal.CreateREAL8Vector(1); af = lal.CreateREAL8Vector(1)  # not used directly
    r = ls.SimIMREOBFinalMassSpin(m1, m2, [0., 0., s1], [0., 0., s2], approx)
    # returns (status, finalMass fraction, finalSpin) in python binding
    return r

# ---- (a) prior draw, registered box, several seeds ----
res = {}
for seed in (20260923, 132203, 7, 99):
    rng = np.random.default_rng(seed)
    N = 2000; n1024 = n2048 = 0; mt_edom = []; chi_edom = []
    i = 0
    while i < N:
        m1 = rng.uniform(pri['mass_1']['minimum'], pri['mass_1']['maximum'])
        m2 = rng.uniform(pri['mass_2']['minimum'], pri['mass_2']['maximum'])
        q = m2 / m1
        if not (pri['mass_ratio']['minimum'] <= q <= pri['mass_ratio']['maximum']): continue
        s1 = rng.uniform(-0.99, 0.99); s2 = rng.uniform(-0.99, 0.99)
        f = f550(m1, m2, s1, s2)
        if f > 1024: n1024 += 1; mt_edom.append(m1 + m2); chi_edom.append((m1*s1+m2*s2)/(m1+m2))
        if f > 2048: n2048 += 1
        i += 1
    res['seed_%d' % seed] = dict(N=N, frac_f550_gt_1024=n1024 / N, frac_f550_gt_2048=n2048 / N,
                                 mtot_edom_max=max(mt_edom) if mt_edom else None,
                                 mtot_edom_median=float(np.median(mt_edom)) if mt_edom else None,
                                 chieff_edom_min=min(chi_edom) if chi_edom else None)
    print(seed, res['seed_%d' % seed], flush=True)

# ---- (a') cross-check: prediction f550>1024 == actual EDOM via bilby path (fmax 1024), 150 pts ----
from bilby.gw.source import lal_binary_black_hole
rng = np.random.default_rng(1)
fa = np.arange(0, 1024 + 1/16, 1/16)
agree = dis = 0; rows = []
for i in range(150):
    while True:
        m1 = rng.uniform(15, 100); m2 = rng.uniform(10, 100)
        if 0.125 <= m2 / m1 <= 1: break
    s1 = rng.uniform(-0.99, 0.99); s2 = rng.uniform(-0.99, 0.99)
    pred = f550(m1, m2, s1, s2) > 1024
    try:
        lal_binary_black_hole(fa, m1, m2, 500., abs(s1), 0. if s1 >= 0 else np.pi, 0., abs(s2), 0. if s2 >= 0 else np.pi, 0.,
                              1.0, 0.3, waveform_approximant='SEOBNRv4HM_PA', reference_frequency=20., minimum_frequency=20.,
                              maximum_frequency=1024., catch_waveform_errors=False)
        actual = False
    except Exception as e:
        actual = 'domain' in str(e).lower() or 'Input domain' in str(e)
    if pred == actual: agree += 1
    else: dis += 1; rows.append(dict(m1=m1, m2=m2, s1=s1, s2=s2, pred=pred, actual=actual))
res['crosscheck_pred_vs_bilby_fmax1024'] = dict(agree=agree, disagree=dis, disagreements=rows)
print('crosscheck', agree, dis, flush=True)

# ---- (b) GW250114 own-posterior corners and blind candidates: f550 for (Mf, af) ----
# Build map f550*Mf (dimensionless, in Hz*Msun) as function of af from equal-mass aligned draws.
def f550_of_Mf_af(Mf, af):
    # find spins s for m1=m2=M/2 giving final spin ~af, then scale by Mf: f*Mf invariant. Use bisection on s in (-0.99,0.99).
    lo, hi = -0.99, 0.99
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        st, mfrac, aff = ls.SimIMREOBFinalMassSpin(50., 50., [0., 0., mid], [0., 0., mid], approx)
        if aff < af: lo = mid
        else: hi = mid
    st, mfrac, aff = ls.SimIMREOBFinalMassSpin(50., 50., [0., 0., mid], [0., 0., mid], approx)
    f = f550(50., 50., mid, mid); f22 = f220(50., 50., mid, mid)
    Mf_ref = 100. * mfrac
    return f * Mf_ref / Mf, f22 * Mf_ref / Mf, aff

res['GW250114_own_posterior_corners'] = {}
for lab, Mf, af in (('q05', 69.26809, 0.67222921), ('q50', 74.57491, 0.76245903), ('q95', 79.882842, 0.83090604),
                    ('worst_lowMf_highaf', 69.26809, 0.83090604)):
    f5, f2, aff = f550_of_Mf_af(Mf, af)
    res['GW250114_own_posterior_corners'][lab] = dict(Mf=Mf, af=af, af_achieved=aff, f550_Hz=f5, f220_Hz=f2, EDOM_at_1024=f5 > 1024)
print(res['GW250114_own_posterior_corners'], flush=True)

blind = {}
for ev, d in reg['test_candidates'].items():
    Mf = d.get('GR_final_mass_detector_median'); af = d.get('GR_final_spin_median')
    if Mf is None or af is None: blind[ev] = dict(Mf=None); continue
    f5, f2, aff = f550_of_Mf_af(Mf, af)
    blind[ev] = dict(Mf=Mf, af=af, f550=f5, f220=f2, EDOM_1024=f5 > 1024, EDOM_2048=f5 > 2048, f220_above_1024_band=f2 > 1024)
res['blind_candidates_at_GR_median'] = blind
n = [b for b in blind.values() if b.get('Mf')]
res['blind_summary'] = dict(with_Mf=len(n), EDOM_1024=sum(b['EDOM_1024'] for b in n), EDOM_2048=sum(b['EDOM_2048'] for b in n),
                            f220_above_1024=sum(b['f220_above_1024_band'] for b in n), no_Mf=len(blind) - len(n))
print(res['blind_summary'], flush=True)
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o,'item') else str(o))
