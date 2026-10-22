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


res={}
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
json.dump(res, open(OUT, 'x'), indent=1, default=lambda o: o.item() if hasattr(o,'item') else str(o))
