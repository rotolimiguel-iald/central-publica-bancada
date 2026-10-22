import os, lal, lalsimulation as ls
print("LAL_DATA_PATH=", os.environ.get("LAL_DATA_PATH"))
names = ["IMRPhenomXPHM","IMRPhenomXHM","IMRPhenomD","IMRPhenomTPHM","IMRPhenomXO4a","SEOBNRv4","SEOBNRv4HM"]
for n in names:
    try:
        a = ls.SimInspiralGetApproximantFromString(n)
    except Exception as e:
        print(n, "UNKNOWN", type(e).__name__); continue
    # try generate TD waveform quickly
    p = lal.CreateDict()
    m1, m2 = 35*lal.MSUN_SI, 30*lal.MSUN_SI
    try:
        if n in ("IMRPhenomXAS","IMRPhenomXPHM","IMRPhenomXHM","IMRPhenomD","SEOBNRv5_ROM","SEOBNRv5HM_ROM","SEOBNRv4_ROM","SEOBNRv4HM_ROM","NRHybSur3dq8","IMRPhenomXO4a"):
            hp, hc = ls.SimInspiralChooseFDWaveform(m1,m2,0,0,0.1,0,0,0.1,400e6*lal.PC_SI,0,0,0,0,0,1/8.,20.,1024.,20.,p,a)
        else:
            hp, hc = ls.SimInspiralChooseTDWaveform(m1,m2,0,0,0.1,0,0,0.1,400e6*lal.PC_SI,0,0,0,0,0,1/2048.,20.,20.,p,a)
        print(n, "OK", hp.data.length)
    except Exception as e:
        print(n, "FAIL", str(e)[:120])
