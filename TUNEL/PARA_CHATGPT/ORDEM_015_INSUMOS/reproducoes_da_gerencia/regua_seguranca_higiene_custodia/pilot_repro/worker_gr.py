# control: RG point (all deformations = 0) at the same masses/spins as an aborting draw, to see whether the abort is deformation-driven
import sys,json,os,numpy as np
os.environ.setdefault("OMP_NUM_THREADS","1")
p=json.loads(sys.argv[1]); fmax=float(sys.argv[2]); zero=sys.argv[3]=="zero"
import lal, lalsimulation as ls
from bilby.gw.source import lal_binary_black_hole
f=np.linspace(0,2048,16*2048+1); d=lal.CreateDict()
for name,key in [("DTau220","dtau220"),("DTau440","dtau440"),("DOmega220","domega220"),("DOmega440","domega440")]:
    getattr(ls,"SimInspiralWaveformParamsInsert"+name)(d,0.0 if zero else float(p[key]))
c1,c2=p["chi_1"],p["chi_2"]
r=lal_binary_black_hole(f,p["mass_1"],p["mass_2"],p["luminosity_distance"],abs(c1),0. if c1>=0 else np.pi,0.,abs(c2),0. if c2>=0 else np.pi,0.,p["theta_jn"],p["phase"],waveform_approximant="pSEOBNRv4HM_PA",reference_frequency=20.0,minimum_frequency=20.0,maximum_frequency=fmax,catch_waveform_errors=True,lal_waveform_dictionary=d)
print("RESULT ok=",r is not None)
