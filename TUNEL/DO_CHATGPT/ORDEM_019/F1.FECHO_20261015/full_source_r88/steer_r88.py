from support_r88 import ROOT, REF, ACTOR, call, pin
s=call({'operation':'get','reference':REF},'GET_STEERING','session_memory.py')
p=dict(s['p'])
p['phase']='existing_spectral_rule_recovery_and_hessian_current'
p['next_action']='Operator answered: reuse terminal satisfaction/payment and negative-gradient spectrum of spectral triple. Locate existing typed operation and consumers; do not repeat abstract identity question. Complete Hessian current in parallel; R16 remains working.'
p['handles']=[dict(h,status='completed',receipt=pin(ROOT/'source/SOURCE_PINS_R88.json')) if h.get('id')=='r88-source' else h for h in p.get('handles',[])]
p['handles'].append({'id':'r88-spectral-reuse','status':'running','agent':'/root/r69_locality_bridge','task_id':'R16_INTEGRATED_P_H3'})
e=pin(ROOT/'OPERATOR_SPECTRAL_RULE_REPLY_R88.json')
call({'operation':'transition','reference':REF,'actor':ACTOR,'expected_revision':s['revision'],'event_id':'r88-operator-spectral-rule-steering','changes':{'records':[{'id':'r88-operator-spectral-rule','kind':'decision','statute':'INPUT','sources':[{'kind':'artifact','ref':e['path'],'sha256':e['sha256']}],'text':(ROOT/'OPERATOR_STEERING_R88.txt').read_text(encoding='utf-8')}],'flow':p}},'STEERING_TRANSITION','session_memory.py')
