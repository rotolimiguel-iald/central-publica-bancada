"""Record actual preparation/dispatch state without invoking executors."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, uuid

R=Path(__file__).resolve().parent
D=R/'orchestration_final_stage'
now=datetime.now(timezone.utc)
def write(p,raw):
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f'))
        with bak.open('xb') as f: f.write(old)
        assert bak.read_bytes()==old
    temp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with temp.open('xb') as f: f.write(raw)
    assert temp.read_bytes()==raw
    temp.replace(p)
catalog=json.loads((D/'prepared_units_v3.json').read_bytes())
for unit in catalog:
    p=Path(unit['payload']);assert hashlib.sha256(p.read_bytes()).hexdigest()==unit['payload_sha256']
receipt={'at':now.isoformat(),'status':'AWAITING_EXPLICIT_REVISED_PAYLOAD_APPROVAL',
         'catalog':str(D/'prepared_units_v3.json'),'units':[{'provider':u['provider'],'request_id':u['request_id'],'status':'NOT_SUBMITTED'} for u in catalog],
         'automatic_review_rejected':'Official message to coordinator dispatching revised payloads; sensitive scientific memory/excerpts require exact revised payload consent',
         'permission_question_pending':True,
         'kimi':{'job_id':'94bd0742-21ef-4116-a331-43bd2b3a99ce','execution_id':'5bf7dbb8-0016-4f42-9f3b-e02721053c86','status':'FAILED_REPORTED_BY_COORDINATOR','usage':None,'cost':None,'retry':False},
         'C6':'MEDIDA_TIMEBOX_EXHAUSTED','gate_changed':False}
write(D/'DISPATCH_STATUS.json',(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode())
p=R/'A7/CONTINUIDADE.json';state=json.loads(p.read_bytes())
state.update(at=now.isoformat(),pending_orchestration=receipt,
             next='Await revised-payload approval; continue local Part B in prescribed order; no C6 restart',
             remaining_full_goal=['C2.2 independent critique remains unpaid after terminal Kimi failure','ORDEM015 PartB ordered tree; T01 g/h pending and a-f acceptance review','final completion audit and both reports'])
state['T01_partial_report']=str(R.parent/'ORDEM_013_RINGDOWN/bis/015/t01_core/RELATORIO_PARCIAL.md')
write(p,(json.dumps(state,ensure_ascii=False,indent=2)+'\n').encode())
p=R.parent/'TUNEL/DO_CHATGPT/LEDGER_016.jsonl'
old=p.read_bytes();entry=json.dumps({'at':now.isoformat(),'event':'REVISED_EXTERNAL_DISPATCH_APPROVAL_BLOCKED','receipt':str(D/'DISPATCH_STATUS.json'),'external_calls':0},ensure_ascii=False)+'\n'
write(p,old+entry.encode())
assert p.stat().st_size>len(old)
print(json.dumps({'status':receipt['status'],'units':receipt['units'],'memory_backed_up':True}))
