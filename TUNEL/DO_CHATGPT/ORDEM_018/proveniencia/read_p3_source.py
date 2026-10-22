from pathlib import Path
import json,hashlib,os
out=Path(__file__).resolve().parent
base=out.parent/'preregistros'/'conjunto_d'/'p3_preparacao'
r=json.loads((base/'RUNTIME_P3_READONLY.json').read_text())
names=['bilby/gw/source.py','bilby/gw/detector/detectors/H1.interferometer','bilby/gw/detector/detectors/L1.interferometer']
for suffix in names:
 row=next(x for x in r['files'] if x['path'].endswith('/'+suffix));raw=Path(row['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256']
 dest=out/'p3_runtime_snapshot'/suffix.replace('/','__');assert not dest.exists();tmp=dest.with_suffix('.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,dest)
 print(json.dumps({'name':suffix,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}))
