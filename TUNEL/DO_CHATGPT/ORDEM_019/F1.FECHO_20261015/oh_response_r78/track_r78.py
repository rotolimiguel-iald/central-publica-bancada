"""Record finite task handles with CAS without duplicating scientific conclusions."""
import sys
import support_r78 as s
def main():
    mode=sys.argv[1]; state=s.call({'operation':'get','reference':s.REF},'TRACK_'+mode+'_GET','session_memory.py')
    handles=list(state['p']['handles'])
    ids={'r78-response-draft':'/root/r69_calibration_bridge','r78-normalization-draft':'/root/r69_locality_bridge'}
    if mode=='start':
        assert not any(h.get('id') in ids for h in handles)
        handles += [{'id':i,'agent':a,'status':'running','unit':'F1.FECHO_20261015','scope_source':s.pin(s.ROOT/'ORIGEM_R78.txt')} for i,a in ids.items()]
    elif mode=='drafts_done':
        receipts={'r78-response-draft':s.ROOT/'PLAN_R78.json','r78-normalization-draft':s.ROOT/'NORMALIZACOES_R78.md'}
        for h in handles:
            if h.get('id') in ids:h.update(status='completed',result=s.pin(receipts[h['id']]))
    elif mode=='execution_start':
        assert not any(h.get('id')=='r78-response-execution' for h in handles)
        handles.append({'id':'r78-response-execution','status':'running','agent':'/root','unit':'F1.FECHO_20261015','plan':s.pin(s.ROOT/'PLAN_R78.json')})
    elif mode=='execution_done':
        for h in handles:
            if h.get('id')=='r78-response-execution':h.update(status='completed',result=s.pin(s.ROOT/'RESULT_R78.json'))
    else:raise ValueError(mode)
    flow=dict(state['p']);flow['handles']=handles
    s.call({'operation':'transition','reference':s.REF,'actor':s.ACTOR,'expected_revision':state['revision'],'event_id':'r78-track-'+mode,'changes':{'flow':flow}},'TRACK_'+mode+'_TRANSITION','session_memory.py')
    print(mode)
if __name__=='__main__':main()
