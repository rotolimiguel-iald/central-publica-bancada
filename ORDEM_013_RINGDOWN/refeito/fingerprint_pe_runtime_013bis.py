"""Fingerprint installed scientific code, not data or secrets; read-only /opt."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.metadata as metadata
import hashlib,json,sys,time
B=Path(__file__).resolve().parents[1]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
    return h.hexdigest()
start=time.perf_counter();entries={};versions={}
for name in ['bilby','dynesty','lalsuite','numpy','scipy','h5py','gwpy','astropy','pandas']:
    d=metadata.distribution(name);versions[name]=d.version
    if d.files is None:raise ValueError('Distribution has no installed-file inventory '+name)
    for rel in d.files:
        if not (str(rel).endswith('.py') or '.so' in Path(str(rel)).name):continue
        p=Path(d.locate_file(rel)).resolve()
        if not p.is_relative_to('/opt/lal_env'):raise ValueError('Unexpected scientific code outside existing environment')
        if not p.is_file():raise FileNotFoundError(p)
        entries[str(p)]={'sha256':sha(p),'bytes':p.stat().st_size,'distribution':name}
exe=Path(sys.executable).resolve()
doc={'status':'READ_ONLY_SCIENTIFIC_RUNTIME_FINGERPRINT','utc':datetime.now(timezone.utc).isoformat(),
 'python_version':sys.version,'python_executable':str(exe),'python_executable_sha256':sha(exe),
 'distributions':versions,'files':entries,'wall_seconds':time.perf_counter()-start,
 'scope':'All inventoried .py/shared libraries in nine named scientific distributions. OS libraries/transitive unlisted packages are not hermetically captured; no data copied or environments changed.'}
p=B/'bis/E2_SCIENTIFIC_RUNTIME_MANIFEST.json'
with p.open('x',encoding='utf-8') as f:json.dump(doc,f,indent=2,allow_nan=False)
print(json.dumps({'files':len(entries),'bytes_hashed':sum(v['bytes'] for v in entries.values()),'sha256':sha(p),'wall_seconds':doc['wall_seconds']}))
