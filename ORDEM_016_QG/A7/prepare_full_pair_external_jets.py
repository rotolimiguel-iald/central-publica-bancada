"""Generalize immutable point engines to independent first external jets."""
from pathlib import Path
import hashlib,json,uuid
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fresh(p,text):
    assert not p.exists(),p;b=text.encode();t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
spec=[('ghost','bilocal_ghost_pair_engine.py','bilocal_ghost_external_jets.py'),
      ('metric','bilocal_metric_pair_engine_v2.py','bilocal_metric_external_jets.py')]
records=[]
for kind,source,target in spec:
    src=H/source;dst=H/target;txt=src.read_text('utf-8')
    old=f'def {kind}_ward_point(point,T,progress=None,jets=None):'
    new=f'def {kind}_ward_point(point,T,progress=None,jets=None,derivative_index=None):'
    assert txt.count(old)==1;txt=txt.replace(old,new)
    if kind=='ghost':
        old='AX=G.vertex(tuple(T))[0]'
        new='AX=G.vertex(tuple(T))[0] if derivative_index is None else G.vertex(tuple(T))[1][derivative_index]'
    else:
        old='AX=[M.vertex_data(tuple(T))[0],lincomb((F(-1),M.potential(tuple(T))))]'
        new='AX=([M.vertex_data(tuple(T))[0],lincomb((F(-1),M.potential(tuple(T))))] if derivative_index is None else [M.vertex_data(tuple(T))[1][derivative_index],empty(50)])'
    assert txt.count(old)==1;txt=txt.replace(old,new)
    fresh(dst,txt);records.append(dict(source=str(src),source_sha256=sha(src),target=str(dst),sha256=sha(dst)))
fresh(H/'bilocal_external_jets_generation.json',json.dumps(records,indent=2))
print(json.dumps(records))
