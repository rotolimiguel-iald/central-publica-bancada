"""Read cached calibration HDF metadata and flag labels, never strain values."""
from pathlib import Path
import json,hashlib,h5py
from datetime import datetime,timezone
B=Path(__file__).resolve().parents[1]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
reg=json.loads((B/'bis/E2_DESIGN_DRAFT_003.json').read_bytes());cfg=reg['pe_jobs']['GW250114_PILOT'];rows=[]
for detector,files in cfg['data'].items():
    for kind in ('onsource','offsource'):
        p=B.parent/files[kind+'_path'];pin=sha(p)
        if pin!=files[kind+'_sha256']:raise ValueError('Calibration bytes differ')
        with h5py.File(p,'r') as h:
            strain=h['strain/Strain'];labels={}
            for n in ('quality/simple/DQShortnames','quality/injections/InjShortnames'):
                labels[n]=[x.decode() if isinstance(x,bytes) else str(x) for x in h[n][()]]
            rows.append({'detector':detector,'kind':kind,'sha256':pin,'strain_shape':strain.shape,
              'strain_dtype':str(strain.dtype),'labels':labels})
out=B/'bis/PILOT_HDF_METADATA_ONLY.json'
with out.open('x',encoding='utf-8') as f:json.dump({'status':'CALIBRATION_METADATA_ONLY_NO_STRAIN_VALUES_READ','utc':datetime.now(timezone.utc).isoformat(),'files':rows,'script_sha256':sha(Path(__file__))},f,indent=2)
print(json.dumps({'sha256':sha(out),'rows':rows}))
