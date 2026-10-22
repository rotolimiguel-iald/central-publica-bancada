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
# ---- (a') cross-check: prediction f550>1024 == actual EDOM via bilby path (fmax 1024), 150 pts ----
from isolated_waveform import lal_binary_black_hole
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


json.dump(res, open(OUT,"x"), indent=2)
