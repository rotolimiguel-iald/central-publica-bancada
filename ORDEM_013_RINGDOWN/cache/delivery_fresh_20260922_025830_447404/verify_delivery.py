"""Verify every shipped byte before running this research delivery."""
from pathlib import Path, PurePosixPath
import hashlib
import json

root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_bytes())
for row in manifest['files']:
    rel=PurePosixPath(row['path'])
    if rel.is_absolute() or '..' in rel.parts or chr(92) in row['path']:
        raise ValueError('Unsafe manifest path')
    path=(root/row['path']).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('Missing or escaped file: '+row['path'])
    raw=path.read_bytes()
    if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:
        raise ValueError('Changed file: '+row['path'])
print(json.dumps(dict(status='PASS',files=len(manifest['files']),scope='Byte custody, not scientific or physical certification')))
