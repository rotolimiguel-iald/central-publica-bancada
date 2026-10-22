import sys, json, numpy as np, time, os
os.environ.setdefault("OMP_NUM_THREADS","1")
seed=int(sys.argv[1]); fmax=float(sys.argv[2]) if len(sys.argv)>2 else 1024.0
rng=np.random.default_rng(seed)
# priors of the registered pilot (RINGDOWN_5SIGMA_V1.json /pe_jobs/GW250114_PILOT and pilot log)
while True:
    m1=rng.uniform(15,100); m2=rng.uniform(10,100)
    if 0.125<=m2/m1<=1: break
p=dict(mass_1=m1,mass_2=m2,chi_1=rng.uniform(-0.99,0.99),chi_2=rng.uniform(-0.99,0.99),
       luminosity_distance=rng.uniform(100,2000),theta_jn=float(np.arccos(rng.uniform(-1,1))),
       phase=rng.uniform(0,2*np.pi),dtau220=rng.uniform(-0.8,2),dtau440=rng.uniform(-0.8,4),
       domega220=rng.uniform(-0.8,2),domega440=rng.uniform(-0.8,2))
print("PARAMS",json.dumps(p),flush=True)
import lal, lalsimulation as ls
from bilby.gw.source import lal_binary_black_hole
duration=16; fs=4096
f=np.linspace(0,fs/2,int(duration*fs/2)+1)
d=lal.CreateDict()
for name,key in [("DTau220","dtau220"),("DTau440","dtau440"),("DOmega220","domega220"),("DOmega440","domega440")]:
    getattr(ls,"SimInspiralWaveformParamsInsert"+name)(d,float(p[key]))
t0=time.perf_counter()
c1,c2=p["chi_1"],p["chi_2"]
r=lal_binary_black_hole(f,p["mass_1"],p["mass_2"],p["luminosity_distance"],abs(c1),0. if c1>=0 else np.pi,0.,abs(c2),0. if c2>=0 else np.pi,0.,p["theta_jn"],p["phase"],
    waveform_approximant="pSEOBNRv4HM_PA",reference_frequency=20.0,minimum_frequency=20.0,maximum_frequency=fmax,catch_waveform_errors=True,lal_waveform_dictionary=d)
dt=time.perf_counter()-t0
print("RESULT",json.dumps(dict(ok=r is not None,seconds=dt,finite=bool(r is not None and np.isfinite(r["plus"]).all()))),flush=True)
