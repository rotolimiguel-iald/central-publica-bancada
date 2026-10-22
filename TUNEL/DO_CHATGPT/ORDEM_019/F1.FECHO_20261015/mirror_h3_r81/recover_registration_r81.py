"""Finish only mission bookkeeping after duplicate receipt-name refusal.
No build, memory append, board or map registration is repeated.
"""
from pathlib import Path
import json,hashlib
from support_r81 import ROOT,REF,ACTOR,TASK,pin,new,project,call
delivery=ROOT/'DELIVERY_R81.json'
reg=json.loads((ROOT/'REGISTRATION_R81.json').read_text(encoding='utf-8'))
assert reg['delivery']==pin(delivery)
for key in ['map','board']:
 assert pin(reg[key]['path'])==reg[key]
 result=json.loads(Path(reg[key]['path']).read_text(encoding='utf-8'));assert result['exit_code']==0
extra=(ROOT/'MEMORY_APPEND_R81.txt').read_bytes()
applied=json.loads((ROOT/'MEMORY_APPLIED_R81.json').read_text(encoding='utf-8'))
for row in applied['surfaces']:
 p=Path(row['after']['path']);backup=Path(row['backup']['path'])
 assert pin(backup)==row['backup'] and pin(p)==row['after']
 assert p.read_bytes()==backup.read_bytes()+extra
new('REGISTRATION_RECOVERY_NOTE.json',{'reason':'FileExistsError: helper tried to create SUBMIT_SYNC_REQUEST.json twice; refusal before submit. Memory8/map/board had completed. Originals retained.','repeat_build':False,'repeat_memory':False,'repeat_map_board':False,'verified_delivery':pin(delivery)})
p=project('RECOVER_SUBMIT_SYNC');task=next(x for x in p['projection']['active'] if x['id']==TASK)
assert task['status'] not in ['review_pending','satisfied']
call({'operation':'submit','reference':REF,'actor':ACTOR,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'event_id':'r81-submit-recovered','task_id':TASK,'lease_id':task['lease']['id'],'evidence':[pin(delivery),pin(ROOT/'REVIEW_R81.json')]},'RECOVER_SUBMIT')
s=call({'operation':'get','reference':REF},'RECOVER_GET','session_memory.py')
flow=dict(s['p']);flow['phase']='h3_recovery_coefficient_reviewed'
flow['next_action']='R81 revisada: recuperacao do registro existe; equivalencia B=eta*A2 compilada. Derivar coeficiente da inducedArea da mesma dinamica/fonte, todo ponto/direcao. OH adiado; H3 universal OPEN. R13 entregue para aceite distinto; nada5sigma calculado.'
flow['handles']=list(flow.get('handles',[]))+[{'id':'r81-lean-coefficient','status':'completed','no_repeat':True,'unit':'F1.FECHO_20261015','receipt':pin(ROOT/'BUILD_R1.json')}]
call({'operation':'transition','reference':REF,'actor':ACTOR,'expected_revision':s['revision'],'event_id':'r81-recovery-h3-recorded','changes':{'records':[{'id':'r81-recovery-h3','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(delivery),'sha256':pin(delivery)['sha256']},{'kind':'artifact','ref':str(ROOT/'ORIGEM.txt'),'sha256':pin(ROOT/'ORIGEM.txt')['sha256']}],'text':extra.decode('utf-8')}],'flow':flow}},'RECOVER_TRANSITION','session_memory.py')
p=project('RECOVER_POST');new('POST_DELIVERY_VERIFIED_R81.json',{'delivery':pin(delivery),'memory_surfaces_verified':8,'receipt':p['receipt'],'task':next(x for x in p['projection']['active'] if x['id']==TASK)})
print(json.dumps(p['receipt'],ensure_ascii=False))
