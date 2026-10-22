from support_r90 import ROOT, REF, ACTOR, call, check
check('PREFLIGHT')
s=call({'operation':'get','reference':REF},'GET_START','session_memory.py')
p=dict(s['p']);p['phase']='full_objective_audit_and_acom_source_recovery'
p['next_action']='Resolve the concrete ACOM v18/spectral representation reference using indexed scientific sources; audit all three original goal requirements against current evidence. No repeat of completed builds or abstract identity question; no smaller surrogate goal.'
p['handles']=p.get('handles',[])+[{'id':'r90-source','status':'running','agent':'/root/r69_locality_bridge','task_id':'R16_INTEGRATED_P_H3'}]
call({'operation':'transition','reference':REF,'actor':ACTOR,'expected_revision':s['revision'],'event_id':'r90-full-objective-audit-started','changes':{'flow':p}},'START_TRANSITION','session_memory.py')
