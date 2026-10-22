"""Finite scalar contracts only. No waveform, strain, PE, or posterior inputs."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'): os.environ[key]='1'
from pathlib import Path
import sys,json,hashlib,itertools,time,inspect
from datetime import datetime,timezone
import numpy as np
import lal,lalsimulation as ls
import astropy.units as u
from astropy.cosmology import Planck18

HERE=Path(__file__).resolve().parent
B=HERE.parents[1]
CODE=B/'bis/e2_code'
sys.path.insert(0,str(CODE))
from remnant_conversion import derive
from registration_guard import publish_new
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
started=time.perf_counter()
metadata=B/'bis/E2_REMNANT_BRIDGE_INPUT.json'
cfg={'remnant_conversion_INPUT':json.loads(metadata.read_text())}
columns={'mass_1':np.array([40.,80.]),'mass_2':np.array([30.,60.]),
         'chi_1':np.array([.3,.3]),'chi_2':np.array([-.2,-.2]),
         'luminosity_distance':np.array([400.,800.])}
calls=[]
derived,receipt=derive(columns,cfg,lambda:calls.append(True))
ratio=float(derived['final_mass_detector'][1]/derived['final_mass_detector'][0])
spin_difference=float(derived['final_spin'][1]-derived['final_spin'][0])
inverse=Planck18.luminosity_distance(derived['redshift']).to_value(u.Mpc)
relative=float(np.max(np.abs(inverse/columns['luminosity_distance']-1)))
if not abs(ratio-2)<1e-12 or not abs(spin_difference)<1e-12 or relative>1e-7 or not calls:
    raise RuntimeError('Scalar remnant contract failed')
original=ls.SimIMREOBFinalMassSpin
negative=[]
try:
    for value in ([.95,.7],[1,.95,.7],[0,float('nan'),.7]):
        ls.SimIMREOBFinalMassSpin=lambda *a,_value=value,**kw:_value
        try:derive(columns,cfg,lambda:None)
        except ValueError as exc:negative.append(str(exc))
        else:raise RuntimeError('Malformed remnant return accepted')
finally:ls.SimIMREOBFinalMassSpin=original

# Endpoint Cartesian product plus minimum masses. q<=1 enforced as in prior.
# These checks are finite corners, not a proof of every interior LAL bound.
rows=[]
for m1,m2,s1,s2 in itertools.product((15.,100.),(10.,100.),(-.99,.99),(-.99,.99)):
    if not .125<=m2/m1<=1:continue
    inspiral=float(ls.SimInspiralChirpTimeBound(20.,m1*lal.MSUN_SI,m2*lal.MSUN_SI,s1,s2))
    merger=float(ls.SimInspiralMergeTimeBound(m1*lal.MSUN_SI,m2*lal.MSUN_SI))
    bound=float(ls.SimInspiralFinalBlackHoleSpinBound(s1,s2))
    tail=float(ls.SimInspiralRingdownTimeBound((m1+m2)*lal.MSUN_SI,bound))*5.
    if not np.isfinite([inspiral,merger,tail]).all():raise RuntimeError('Nonfinite scalar bound')
    # Both trigger prior extremes, ±22 ms detector delay; max dtau440=4.
    for trigger in (1420878141.2-.15,1420878141.2+.15):
        low=trigger-.022-inspiral-merger;high=trigger+.022+tail
        rows.append(dict(mass_1=m1,mass_2=m2,chi_1=s1,chi_2=s2,trigger=trigger,
          inspiral_s=inspiral,merger_s=merger,tail_with_max_dtau_s=tail,
          earliest_GPS=low,latest_GPS=high))
windows=[]
for duration,start in ((8.,1420878135.),(16.,1420878127.),(32.,1420878111.)):
    left=min(r['earliest_GPS']-(start+.2) for r in rows)
    right=min(start+duration-.2-r['latest_GPS'] for r in rows)
    windows.append(dict(duration_s=duration,start_GPS=start,left_margin_s=left,right_margin_s=right,passes_corners=min(left,right)>=0))
sources={str(p):sha(p) for p in (Path(__file__),metadata,CODE/'remnant_conversion.py',CODE/'pe_runner.py',CODE/'pseob_source.py',Path(ls.__file__),Path(lal.__file__),Path(cfg['remnant_conversion_INPUT']['cosmology_source_path']))}
result=dict(status='SCALAR_CONTRACTS_ONLY_NO_PE',created_utc=datetime.now(timezone.utc).isoformat(),
  source_sha256=sources,wall_seconds=time.perf_counter()-started,
  remnant=dict(input={k:v.tolist() for k,v in columns.items()},derived={k:v.tolist() for k,v in derived.items()},
    mass_scaling_ratio=ratio,spin_scaling_difference=spin_difference,inverse_distance_max_relative=relative,
    malformed_return_rejections=negative,receipt=receipt),
  temporal=dict(scope='Finite prior corners only, not exhaustive interior certification; no waveform support measured',
    detector_delay_bound_s=.022,roll_off_s=.2,dtau_multiplier=5.,rows=rows,windows=windows,
    required_earliest_GPS=min(r['earliest_GPS'] for r in rows),required_latest_GPS=max(r['latest_GPS'] for r in rows)))
publish_new(HERE/'TEMPORAL_REMNANT_SCALAR_TEST.json',result)
print(json.dumps(dict(windows=windows,remnant={k:result['remnant'][k] for k in ('mass_scaling_ratio','spin_scaling_difference','inverse_distance_max_relative')},wall_seconds=result['wall_seconds'])))
