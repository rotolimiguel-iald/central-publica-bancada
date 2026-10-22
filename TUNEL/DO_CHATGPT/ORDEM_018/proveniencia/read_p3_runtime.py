"""Read runtime bytes only; never imports scientific modules or executes a pipeline."""
from pathlib import Path
import json,hashlib,sys,datetime,os
out=Path(__file__).resolve().parent
b=out.parent/'preregistros'/'conjunto_d'/'p3_preparacao'
r=json.loads((b/'RUNTIME_P3_READONLY.json').read_text())
files=[]
for row in r['files']:
    p=Path(row['path']);raw=p.read_bytes();h=hashlib.sha256(raw).hexdigest()
    files.append({'path':str(p),'sha256':h,'bytes':len(raw),'matches_pin':h==row['sha256'] and len(raw)==row['bytes']})
assert all(x['matches_pin'] for x in files)
i=json.loads((b/'INTERPRETER_PIN.json').read_text());raw=Path(i['path']).read_bytes();ih=hashlib.sha256(raw).hexdigest();assert ih==i['sha256']
selected=['bilby/gw/likelihood/base.py','bilby/gw/waveform_generator.py','bilby/gw/detector/networks.py','bilby/gw/detector/psd.py','dynesty/dynesty.py','dynesty/sampler.py','dynesty/utils.py']
snapshot=out/'p3_runtime_snapshot';snapshot.mkdir(exist_ok=True)
for suffix in selected:
    row=next(x for x in r['files'] if x['path'].endswith('/'+suffix))
    dest=snapshot/suffix.replace('/','__');raw=Path(row['path']).read_bytes()
    if dest.exists():assert dest.read_bytes()==raw
    else:
        tmp=dest.with_suffix('.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,dest)
result={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'RUNTIME_BYTES_MATCH_READ_ONLY','files':files,'interpreter':dict(i,actual_sha256=ih),'scientific_imports':False,'PE':False,'native_waveform':False,'observed_data':False}
p=out/'REVISAO_P3_RUNTIME.json';assert not p.exists();raw=(json.dumps(result,indent=2)+'\n').encode();tmp=p.with_suffix('.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,p)
print(json.dumps({'status':result['status'],'count':len(files),'receipt_sha256':hashlib.sha256(raw).hexdigest(),'source_snapshots':len(selected)}))
