"""Keep the radial denominator independent until all derivatives finish."""
from pathlib import Path
import hashlib,json,uuid
H=Path(__file__).resolve().parent
p=H/'einstein_test_field_engine.py';q=H/'einstein_radial_aux_engine.py'
assert not q.exists()
txt=p.read_text('utf-8').replace('from curved_source_jet_engine import x,metric1',
 'from curved_source_jet_engine import x,metric1,z as radial_z,L as radial_log')
old='return ex(s.diff(f,x[i])+q[i]*f)'
new='return ex(s.diff(f,x[i])+2*x[i]*(s.diff(f,radial_z)+s.diff(f,radial_log)/radial_z)+q[i]*f)'
assert txt.count(old)==1;txt=txt.replace(old,new)
b=txt.encode();t=q.with_name(q.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(q)
print(json.dumps(dict(source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
 successor_sha256=hashlib.sha256(q.read_bytes()).hexdigest(),change='Auxiliary radial chain rule only; no change to Einstein coefficients')))
