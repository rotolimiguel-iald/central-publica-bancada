"""Read installed public runtime interfaces; no likelihood, waveform or PE call."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['PYTHONDONTWRITEBYTECODE']='1'
from pathlib import Path
from datetime import datetime,timezone
import importlib.metadata,inspect,json,hashlib
import bilby,lalsimulation,dynesty
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
out=B/'bis/E2_RUNTIME_STATIC_INSPECTION.json'
if out.exists():raise FileExistsError(out)
sources={}
for obj in [bilby.gw.source.lal_binary_black_hole,bilby.gw.source._base_lal_cbc_fd_waveform,bilby.run_sampler]:
    p=inspect.getsourcefile(obj);sources[obj.__name__]=dict(path=p,sha256=sha(p),signature=str(inspect.signature(obj)),source=inspect.getsource(obj))
setters=[n for n in dir(lalsimulation) if 'Insert' in n and any(k in n for k in ['DTau220','DTau440','DOmega220','DOmega440'])]
d=dict(status='READ_ONLY_RUNTIME_INTERFACES__NO_WAVEFORM_OR_PE_EXECUTED',utc=datetime.now(timezone.utc).isoformat(),versions={name:importlib.metadata.version(name) for name in ['bilby','dynesty','lalsuite','h5py','numpy','scipy']},setters=setters,sources=sources,code_sha256=sha(__file__))
with out.open('xb') as f:f.write((json.dumps(d,indent=2)+'\n').encode())
print(json.dumps(dict(path=str(out),sha256=sha(out),versions=d['versions'],setters=setters)))
