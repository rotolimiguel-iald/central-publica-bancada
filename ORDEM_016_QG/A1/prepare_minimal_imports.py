"""Prepare a separate import-only variant; never claim byte-identical reproduction."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parent
source=root/'v31/ContratoQG_v31.lean'
out=root/'minimal_imports/ContratoQG_v31_Minimal.lean'
out.parent.mkdir(exist_ok=True)
raw=source.read_bytes()
lines=raw.splitlines(keepends=True)
original=b''.join(lines[:6])
assert all(line.startswith(b'import ') for line in lines[:6])
body=b''.join(lines[6:])
imports=('import TGL.ModularRealization\nimport TGLExt.PoincareGroup\n'
         'import TGLExt.Solder4D\nimport TGLExt.ModularFlowLevel\n').encode()
result=imports+body
assert not out.exists()
tmp=out.with_suffix('.lean.tmp')
with tmp.open('xb') as f:f.write(result)
assert tmp.read_bytes()==result
tmp.rename(out)
digest=lambda x:hashlib.sha256(x).hexdigest()
data={'status':'REAL','source':str(source),'source_sha256':digest(raw),
      'variant':str(out),'variant_sha256':digest(result),
      'body_unchanged_byte_for_byte':out.read_bytes()[len(imports):]==body,
      'body_sha256':digest(body),'removed_import_block':original.decode(),
      'new_import_block':imports.decode(),
      'scope':'A-1.b type preparation; not A-1.a exact reproduction; no contract field changed',
      'diagnosis':'TGL.ModularRealization alone loaded under 8 GiB; discard unused aggregate imports in separate source'}
receipt=out.parent/'preparation.json'
assert not receipt.exists()
tmp=receipt.with_suffix('.json.tmp')
content=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
with tmp.open('xb') as f:f.write(content)
assert tmp.read_bytes()==content
tmp.rename(receipt)
print(json.dumps(data,ensure_ascii=False))
