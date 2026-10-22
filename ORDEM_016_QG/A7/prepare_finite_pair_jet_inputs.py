"""Add an explicit test-jet input in copies of the already measured pair engines."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for kind in ('metric','ghost'):
    src=H/f'finite_{kind}_pair_engine.py';dst=H/f'finite_{kind}_pair_engine_v2.py'
    assert not dst.exists()
    text=src.read_text('utf-8-sig')
    signature=('def finite_node(A, B, p, x, order):' if kind=='metric'
               else 'def finite_node(A,B,p,x,order):')
    new_signature=signature[:-2]+', jet_provider=external_jets):'
    assert text.count(signature)==1 and text.count('jets=external_jets(')==1
    updated=text.replace(signature,new_signature).replace('jets=external_jets(','jets=jet_provider(')
    assert updated.replace(new_signature,signature).replace('jets=jet_provider(','jets=external_jets(')==text
    compile(updated,str(dst),'exec')
    data=updated.encode();tmp=dst.with_name(dst.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(data);assert tmp.read_bytes()==data;tmp.replace(dst)
    rows.append(dict(source=str(src),source_sha256=sha(src),copy=str(dst),copy_sha256=sha(dst),
                     change='Only injectable external jet provider; default exactly prior function'))
p=H/'finite_pair_jet_inputs_manifest.json';assert not p.exists()
data=json.dumps(dict(at=datetime.now(timezone.utc).isoformat(),copies=rows),indent=2).encode()
tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);tmp.write_bytes(data);assert tmp.read_bytes()==data;tmp.replace(p)
print(json.dumps(rows))
