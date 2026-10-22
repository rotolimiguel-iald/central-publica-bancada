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


res = {}
for seed in (99,):
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


json.dump(res, open(OUT, "x"), indent=2, default=lambda o: o.item() if hasattr(o,"item") else str(o))
