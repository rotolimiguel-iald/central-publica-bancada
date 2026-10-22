import sys, json, resource
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
import lal, lalsimulation as ls
p=json.loads(sys.argv[1]); fmax=float(sys.argv[2])
d=lal.CreateDict()
ls.SimInspiralWaveformParamsInsertDTau220(d,p['dtau220']); ls.SimInspiralWaveformParamsInsertDTau440(d,p['dtau440'])
ls.SimInspiralWaveformParamsInsertDOmega220(d,p['domega220']); ls.SimInspiralWaveformParamsInsertDOmega440(d,p['domega440'])
try:
    hp,hc=ls.SimInspiralFD(p['mass_1']*lal.MSUN_SI,p['mass_2']*lal.MSUN_SI,0,0,p['chi_1'],0,0,p['chi_2'],
        p['luminosity_distance']*1e6*lal.PC_SI,p['theta_jn'],p['phase'],0.,0.,0.,1/16.,20.,fmax,20.,d,ls.pSEOBNRv4HM_PA)
    print(json.dumps({"status":"FINITE" if (abs(hp.data.data).max()>0) else "ZERO","n":len(hp.data.data)}))
except RuntimeError as e:
    print(json.dumps({"status":"LAL_ERROR","msg":str(e)[:120]}))
