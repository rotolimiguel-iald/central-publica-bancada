"""Read back delivery, append-only memory and current mission; write one receipt."""
import json
from pathlib import Path
import support_r61 as s

def main():
    delivery=json.loads((s.ROOT/'DELIVERY_INTEGRATED_R61.json').read_text(encoding='utf-8'))
    checked=[]
    for row in delivery['evidence']:
        assert s.pin(row['path'])==row, row['path']
        checked.append(row)
    applied=json.loads((s.ROOT/'MEMORY_APPLIED_R61.json').read_text(encoding='utf-8'))
    for row in applied['surfaces']:
        for key in ['after','backup','append']:
            assert s.pin(row[key]['path'])==row[key]
        original=Path(row['backup']['path']).read_bytes()
        extra=Path(row['append']['path']).read_bytes()
        assert Path(row['after']['path']).read_bytes()==original+extra
        assert row['backup']['sha256']==row['before']['sha256']
    state=s.call('session_memory.py',{'operation':'get','reference':str(s.REF)},'CUSTODY_GET')
    handles=[h for h in state['p']['handles'] if h['id'] in ('r61-oh-custody',)]
    assert len(handles)==1 and all(h['status']=='completed' for h in handles)
    mission=s.project('CUSTODY_PROJECT')
    active={x['id']:x for x in mission['projection']['active']}
    assert active['R4']['lease']['id']=='dc77ee82-5303-491f-8515-62bc3e2a5248'
    assert active['R5']['status']=='working'
    receipt=s.new('FINAL_CUSTODY_R61.json',{
        'status':'PASS_CUSTODY_R4_RECOVERED',
        'delivery':s.pin(s.ROOT/'DELIVERY_INTEGRATED_R61.json'),
        'evidence_checked':len(checked),'memory_surfaces_checked':len(applied['surfaces']),
        'memory_prefixes_and_backups_verified':True,'handles':handles,
        'mission_receipt':mission['receipt'],'R4_reset_executed':True,
        'R4_R5_integrally_accepted':False,'gate_changed':False})
    print(receipt)

if __name__=='__main__':main()
