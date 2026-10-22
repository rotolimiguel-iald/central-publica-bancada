"""Custody summary only: does not import or execute any stage or E6 producer."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os

here=Path(__file__).resolve().parent
root=here.parents[2]

def pin(path):
    raw=path.read_bytes()
    if len(raw)>25_000_000:raise ValueError('Size')
    return dict(path=path.relative_to(root).as_posix(),sha256=hashlib.sha256(raw).hexdigest())

def checked(ref):
    path=(root/ref['path']).resolve()
    if not path.is_relative_to(root) or pin(path)!=ref:raise ValueError('Changed pin')
    return ref

handoff=json.loads((here/'STAGE_CHAIN_HANDOFF_V1.json').read_bytes())
stages={}
for stage,name in [('E3.2','E3_2'),('E3.3','E3_3'),('TEST','TEST')]:
    detail=handoff['details'][stage]
    stages[stage]=dict(GO=pin(here/(name+'_OPERATOR_GO_RECORD_001.json')),
        adapter=checked(handoff['reviewed_stages'][stage]),review=checked(detail['review']),
        request=checked(detail['request']),finalization=checked(detail['finalization']),
        artifact=checked(detail['artifact']),outcome=detail['outcome'],bindings=detail['bindings'])
value=dict(schema='E3_STAGE_CHAIN_FINAL_MANIFEST_V1',status='DOCUMENTARY_STAGE_CHAIN_FINALIZED',
    created_utc=datetime.now(timezone.utc).isoformat(),stages=stages,
    helper=checked(handoff['helper']),preparation_manifest=checked(handoff['preparation_manifest']),
    helper_review=pin(here.parent/'e6_review/E3_WALL_HELPER_INDEPENDENT_REVIEW_V1.md'),
    handoff=pin(here/'STAGE_CHAIN_HANDOFF_V1.json'),manifest_writer=pin(Path(__file__).resolve()),
    TEST_verdict='AWAITING_DATA',TEST_cells=180,physical_fields_null=True,physical_calibration_paid=False,
    cost_per_converged_PE=None,scope='Custody of existing GO/helper/reviews/adapters only; no new approval or gate',
    E6_rerun_by_this_task=False,
    downstream_E6={'status':'REPORTED_EXECUTED_BY_PRINCIPAL_NOT_AUDITED_HERE',
        'run_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/bis/e6_prepare_v3/runs/wall_actual_001',
        'reported_time_UTC':'23:29:13','independent_review':'B ongoing per principal'},order_completed=False)
target=here/'STAGE_CHAIN_FINAL_MANIFEST_V1.json';raw=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
temporary=target.with_suffix('.pending')
with temporary.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
if temporary.stat().st_size!=len(raw) or len(raw)>25_000_000:raise ValueError('Size')
os.link(temporary,target);temporary.unlink()
print(json.dumps(pin(target)))
