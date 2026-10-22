"""Verify manifest bytes and safe paths; no physics or computation implied."""
from pathlib import Path,PurePosixPath
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_bytes());seen=set()
for row in manifest['files']:
    name=row['path'];rel=PurePosixPath(name)
    if rel.is_absolute() or '..' in rel.parts or '\\' in name or name in seen:raise ValueError('Unsafe or duplicate manifest entry')
    seen.add(name);p=(root/name).resolve()
    if not p.is_relative_to(root) or not p.is_file() or (root/name).is_symlink():raise ValueError('Missing/escaped file')
    raw=p.read_bytes()
    if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('Changed file: '+name)
print(json.dumps(dict(status='PASS',files=len(seen),scope='Byte identity only; not scientific or physical certification')))
