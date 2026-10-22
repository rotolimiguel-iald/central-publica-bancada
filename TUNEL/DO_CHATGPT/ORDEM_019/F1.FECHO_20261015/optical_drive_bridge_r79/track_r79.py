"""Record finite task handles with CAS without duplicating scientific conclusions."""
import sys
import support_r79 as s
def main():
    mode=sys.argv[1]; state=s.call({'operation':'get','reference':s.REF},'TRACK_'+mode+'_GET','session_memory.py')
    handles=list(state['p']['handles'])
    ids={'r79-cut-derivation':'/root/r69_calibration_bridge','r79-material-map':'/root/r69_locality_bridge'}
    if mode=='start':
        assert not any(h.get('id') in ids for h in handles)
        handles += [{'id':i,'agent':a,'status':'running','unit':'F1.FECHO_20261015','scope_source':s.pin(s.ROOT/'ORIGEM_R79.txt')} for i,a in ids.items()]
    elif mode=='drafts_done':
        receipts={'r79-cut-derivation':s.ROOT/'PLAN_R79.json','r79-material-map':s.ROOT/'MATERIAL_IDENTIFICATION_R79.md'}
        for h in handles:
            if h.get('id') in ids:h.update(status='completed',result=s.pin(receipts[h['id']]))
    elif mode=='execution_start':
        assert not any(h.get('id')=='r79-response-execution' for h in handles)
        handles.append({'id':'r79-response-execution','status':'running','agent':'/root','unit':'F1.FECHO_20261015','plan':s.pin(s.ROOT/'PLAN_R79.json')})
    elif mode=='execution_done':
        for h in handles:
            if h.get('id')=='r79-response-execution':h.update(status='completed',result=s.pin(s.ROOT/'RESULT_R79.json'))
    else:raise ValueError(mode)
    flow=dict(state['p']);flow['handles']=handles
    s.call({'operation':'transition','reference':s.REF,'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r79-track-'+mode,'changes':{'flow':flow}},'TRACK_'+mode+'_TRANSITION','session_memory.py')
    print(mode)
if __name__=='__main__':main()
