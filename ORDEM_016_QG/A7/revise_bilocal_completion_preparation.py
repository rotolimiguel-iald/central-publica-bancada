"""Preserve the rejected oversized preparation; create a bounded v2."""
from pathlib import Path
import json,uuid
H=Path(__file__).resolve().parent
src=H/'prepare_bilocal_completion_units.py'
dst=H/'prepare_bilocal_completion_units_v2.py'
assert not dst.exists()
text=src.read_text('utf-8').replace("D=H/'orchestration_bilocal_completion'","D=H/'orchestration_bilocal_completion_v2'")
old="source=H/name;lines=source.read_text('utf-8-sig').splitlines()"
new=old+"\n            if name=='position_metric_bubble_engine.py':lines=lines[:123]\n            if name=='ghost_direct_position_engine.py':lines=lines[:51]"
assert text.count(old)==1;text=text.replace(old,new)
b=text.encode();tmp=dst.with_name(dst.name+'.tmp_'+uuid.uuid4().hex)
tmp.write_bytes(b);assert tmp.read_bytes()==b;tmp.replace(dst)
# First preview succeeded; preserve its exact unit and ID in v2, no remote dispatch.
d=H/'orchestration_bilocal_completion_v2';d.mkdir(exist_ok=True)
oldroot=H/'orchestration_bilocal_completion'
for p in oldroot.glob('kimi_spaceform_transvection_endpoint_recurrence*'):
    q=d/p.name;assert not q.exists();q.write_bytes(p.read_bytes())
note=dict(status='SUPERSEDED_BEFORE_ANY_SUBMISSION',reason='Second prompt exceeded 24000 characters',
          first_unit='Identical payload/request_id preserved in v2',
          oversized_unit='Not previewed successfully, never submitted; retained here, do not dispatch',
          replacement=str(d/'prepared_units.json'))
p=oldroot/'SUPERSEDED.json';assert not p.exists();p.write_text(json.dumps(note,indent=2),encoding='utf-8')
print(dst)
