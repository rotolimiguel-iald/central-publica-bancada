from support_r84 import *
g=call({'operation':'get','reference':REF},'GET_START_FRESH','session_memory.py')
handles=g['p']['handles']
for ident,agent in [('r84-action-builder','/root/r69_calibration_bridge'),('r84-p-variations','/root/r69_locality_bridge')]:
    assert not any(h['id']==ident for h in handles)
    handles.append({'id':ident,'status':'running','agent':agent,'task_id':TASK,'no_repeat':True,'source':pin(ROOT/'ORIGEM.txt')})
r=call({'operation':'transition','reference':REF,'actor':ACTOR,'expected_revision':g['revision'],'event_id':'r84-construction-started','changes':{'flow':{'handles':handles,'phase':'integrated_action_and_P_variations','next_action':'Derive integrated variation and examine stationarity/variation coverage without assuming H3.'}}},'CONSTRUCTION_START','session_memory.py')
print(r['receipt'])
