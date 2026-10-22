"""Read installed public PE interfaces; no waveforms, likelihood or sampling."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
from pathlib import Path
import inspect,json,hashlib
import bilby
B=Path(__file__).resolve().parents[1]
items={'PriorDict_init':bilby.core.prior.PriorDict.__init__,
       'PriorDict_conversion':bilby.core.prior.PriorDict.evaluate_constraints,
       'WaveformGenerator_init':bilby.gw.WaveformGenerator.__init__,
       'Interferometer_set_strain':bilby.gw.detector.Interferometer.set_strain_data_from_gwpy_timeseries,
       'PSD_init':bilby.gw.detector.PowerSpectralDensity.__init__,
       'GW_likelihood_init':bilby.gw.likelihood.GravitationalWaveTransient.__init__}
r={}
for name,obj in items.items():
    path=Path(inspect.getfile(obj));r[name]={'signature':str(inspect.signature(obj)),
      'path':str(path),'file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source':inspect.getsource(obj)}
out=B/'bis/E2_BILBY_PE_INTERFACES.json'
with out.open('x',encoding='utf-8') as f:json.dump(r,f,indent=2)
print(json.dumps({k:v['signature'] for k,v in r.items()}))
