"""Copies with one weight-provider import changed, all graph algebra retained."""
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent
items=[]
old='from finite_angular_contact_engine import node_weights'
new='from flat_reference_weight_engine import node_weights'
for tag in ('metric','ghost'):
    p=H/f'finite_{tag}_pair_engine.py';q=H/f'flat_reference_{tag}_engine.py'
    text=p.read_text(encoding='utf-8');assert text.count(old)==1
    changed=text.replace(old,new)
    assert changed.replace(new,old)==text
    assert not q.exists();q.write_bytes(changed.encode())
    compile(changed,str(q),'exec')
    items.append(dict(source=str(p),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                      copy=str(q),copy_sha256=hashlib.sha256(q.read_bytes()).hexdigest(),
                      reverse_text_identical=True))
p=H/'flat_reference_inputs_manifest.json';assert not p.exists()
p.write_bytes(json.dumps(items,indent=2).encode())
print(json.dumps(dict(prepared=True,copies=len(items))))
