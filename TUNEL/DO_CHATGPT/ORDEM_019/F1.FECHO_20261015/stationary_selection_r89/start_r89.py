from support_r89 import ROOT, REF, ACTOR, call, check
check('PREFLIGHT')
s=call({'operation':'get','reference':REF},'GET_START','session_memory.py')
p=dict(s['p'])
p['phase']='stationarity_from_same_state_spectral_selection'
p['next_action']='Consume recovered spectral rule in same-P action: test whether its fixed-space condition constrains action stationarity or is automatic for the generator of that state. Reuse P5 positive and P16 negative branches. No repeated abstract identity question; full objective preserved.'
p['handles']=p.get('handles',[])+[{'id':'r89-source','status':'running','agent':'/root/r69_locality_bridge','task_id':'R16_INTEGRATED_P_H3'},{'id':'r89-formal','status':'running','agent':'/root/r69_calibration_bridge','task_id':'R16_INTEGRATED_P_H3'}]
call({'operation':'transition','reference':REF,'actor':ACTOR,'expected_revision':s['revision'],'event_id':'r89-stationarity-selection-started','changes':{'flow':p}},'START_TRANSITION','session_memory.py')
