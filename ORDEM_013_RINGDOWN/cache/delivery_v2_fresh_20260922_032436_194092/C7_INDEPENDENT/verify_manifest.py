"""Check every shipped file; generated outputs are outside this manifest."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_bytes())
for row in manifest['files']:
    p=root/row['path']
    if p.stat().st_size!=row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
        raise RuntimeError('Package changed: '+row['path'])
print(json.dumps(dict(status='PASS',files=len(manifest['files']))))
