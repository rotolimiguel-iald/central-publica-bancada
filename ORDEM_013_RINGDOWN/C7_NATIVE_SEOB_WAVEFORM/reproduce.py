"""Replay the portable generator against full PyCBC polarizations."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'MANIFEST.json').read_bytes())
for row in manifest['files']:
    if hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()!=row['sha256']:
        raise ValueError('Package integrity failed:'+row['path'])
sys.path.insert(0,str(ROOT))
import numpy as np
import lalsimulation as ls
import tgl_native_ringdown as api
import stable_peak_imr_model as reference

inputs=json.loads((ROOT/'VALIDATION_INPUTS.json').read_bytes())
if ls.SimulationVCSInfo.vcsId!=inputs['lal_commit']:
    raise ValueError('Reproduction uses a different LAL source commit; validate explicitly before accepting')
rows=[]
for source in inputs['sources']:
    x=np.array([np.log(source['mass']),np.log(source['q']),source['s1'],source['s2'],source['inclination'],source['phase'],.6])
    times=np.arange(410)/2048+.0034
    for rate in (8192,16384):
        prepared=api.prepare_ringdown(x,times,sample_rate=rate)
        for reading in ('R-B','R-RAIZ-0','R-LIN','R-MOD'):
            for strength in (0.,.37,1.):
                rp,rc,meta=reference.polarizations('SEOBNRv4HM',x,times,reading,strength,rate)
                for distance,psi in ((403.,0.),(650.,.31)):
                    hp,hc,out=api.polarizations(prepared,reading=reading,strength=strength,distance_mpc=distance,polarization_rad=psi)
                    cp,sp=np.cos(2*psi),np.sin(2*psi)
                    expected=np.array([cp*rp-sp*rc,sp*rp+cp*rc])*403./distance*1e-21
                    actual=np.array([hp,hc])
                    error=float(np.linalg.norm(actual-expected)/np.linalg.norm(expected))
                    rows.append(dict(source=source['name'],rate=rate,reading=reading,strength=strength,
                        distance=distance,psi=psi,relative_error=error,passes=bool(error<=1e-6)))
        reference.source_curves.cache_clear()
        print(json.dumps(dict(source=source['name'],rate=rate,done=True)),flush=True)
guards=[]
bad=[dict(strength=-1.),dict(distance_mpc=0.),dict(distance_mpc=float('nan')),
     dict(reading='R-RAIZ-COHERENT'),dict(reading='unknown'),dict(phase=float('nan'))]
for change in bad:
    args=dict(reading='R-B',strength=1.,distance_mpc=403.);args.update(change)
    try:
        api.polarizations(prepared,**args)
    except ValueError:
        guards.append(True)
    else:
        guards.append(False)
out=dict(status='PASS_PORTABLE_NATIVE_WAVEFORM' if all(r['passes'] for r in rows) and all(guards) else 'FAIL_PORTABLE_NATIVE_WAVEFORM',
         count=len(rows),max_relative_error=max(r['relative_error'] for r in rows),guards=guards,rows=rows,
         scientific_acceptance=False,lal_commit=ls.SimulationVCSInfo.vcsId,
         scope='Numerical waveform/phase/distance/polarization equivalence, not posterior calibration or physical confirmation')
run=ROOT/'cache'/('replay_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'));run.mkdir(parents=True)
raw=(json.dumps(out,indent=2)+'\n').encode();p=run/'RESULT.json';temp=p.with_suffix('.tmp');temp.write_bytes(raw)
if temp.stat().st_size!=len(raw):raise ValueError('Short result write')
temp.replace(p)
print(json.dumps({k:v for k,v in out.items() if k!='rows'},ensure_ascii=False),flush=True)
print(json.dumps(dict(result=str(p))),flush=True)
if out['status']!='PASS_PORTABLE_NATIVE_WAVEFORM':raise ValueError('Portable waveform check failed')
